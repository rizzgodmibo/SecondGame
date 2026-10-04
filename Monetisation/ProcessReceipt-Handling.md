---
tags: [monetisation/receipts, systems/data]
status: draft
updated: 2026-10-04
confidence: high
---
# ProcessReceipt Handling (Developer Products)

## TL;DR
- Assign **exactly one** `MarketplaceService.ProcessReceipt` callback, in one server `Script`. Alternatively, use the newer `MarketplaceService:BindReceiptHandler(Enum.ReceiptType.DeveloperProduct, fn, filter?)`. Bound handlers take precedence, and anything unmatched falls through to `ProcessReceipt`.
- **Idempotency key = `receiptInfo.PurchaseId`.** Store recent PurchaseIds **in the same saved document as the granted goods**, and grant + record them in one atomic write. If the ID is already present, return `PurchaseGranted` without granting again.
- Return `PurchaseGranted` **only after the grant is durably saved**. Return `NotProcessedYet` in every other case: player not present, data not loaded, session not owned, save failed, unknown product, or an error was thrown.
- There are no time-based retries. A `NotProcessedYet` receipt is re-delivered only when the player **makes another purchase or rejoins**. It is never refunded or expired.
- The same receipt **can run on two servers at once** (the player hops servers mid-callback). Session locking (ProfileStore) or `UpdateAsync` on the purchase record is what prevents a double grant.
- **Never** grant from `PromptProductPurchaseFinished`. It fires on cancel too, and it is client-observable.

## How Roblox delivers receipts (creator-docs, 2026-10)
- The callback fires for every unresolved purchase when: (1) a purchase completes, (2) a successful purchase prompt appears, (3) the **user joins a server**.
- The user must be **in the server** for the callback to run. The result can still be recorded after they leave.
- **No timeout.** The callback may yield for as long as the server lives, so it is fine to wait for a DataStore save.
- Several pending receipts are delivered in **non-deterministic order**.
- **No callback set → receipts are auto-acknowledged** and are gone forever. Never publish a game that sells products before the handler exists.
- Returning `PurchaseGranted` can still fail to record on the backend. The receipt then stays unresolved and will be re-delivered, so idempotency is mandatory, not optional.
- `receiptInfo` fields: `PurchaseId`, `PlayerId`, `ProductId`, `PlaceIdWherePurchased`, `CurrencySpent` (actual R$ paid, already reflecting price tests, regional pricing and Plus discounts), `CurrencyType`, `ProductPurchaseChannel` (`InExperience`, `ExperienceDetailsPage`, `AdReward`, `CommerceProduct`).
- **Rewarded video ad rewards and commerce-product bundles also arrive here** (`AdReward` / `CommerceProduct`, `CurrencySpent` = 0 for ads ⚠️ verify). Exclude them from revenue analytics.
- External sales from the Store tab (and from Shop listing surfaces) require a working handler. Test mode charges **real Robux**.

## Implementation (ProfileStore-style session-locked data)

Lives in `ServerScriptService/Monetisation/ReceiptProcessor.server.luau`. It assumes a `PlayerData` module (see [[Data-Persistence-DataStores-And-ProfileStore]]) that exposes the loaded, session-locked profile. The profile shape matches ProfileStore: `.Data`, `.LastSavedData`, `:IsActive()`, `:Save()`, `.OnAfterSave`. ⚠️ verify: these member names against the ProfileStore version you vendor (loleris/ProfileStore).

```lua
--!strict
-- ServerScriptService/Monetisation/ReceiptProcessor.server.luau
local MarketplaceService = game:GetService("MarketplaceService")
local Players = game:GetService("Players")
local AnalyticsService = game:GetService("AnalyticsService")
local ServerScriptService = game:GetService("ServerScriptService")

type Signal = { Wait: (self: any) -> ...any }
type PlayerDataShape = {
	Coins: number,
	PurchaseIds: { string }, -- rolling idempotency log, saved WITH the goods
	[string]: any,
}
type Profile = {
	Data: PlayerDataShape,
	LastSavedData: PlayerDataShape,
	IsActive: (self: Profile) -> boolean,
	Save: (self: Profile) -> (),
	OnAfterSave: Signal,
}
type GrantFn = (player: Player, profile: Profile, receipt: { [string]: any }) -> ()

local PlayerData = require(ServerScriptService.Data.PlayerData) :: {
	GetProfile: (player: Player) -> Profile?,
	WaitForProfile: (player: Player, timeout: number) -> Profile?,
}

local PURCHASE_ID_LOG_SIZE = 100 -- enough to cover any burst of re-deliveries
local PROFILE_WAIT_SECONDS = 15
local SAVE_RETRY_SECONDS = 10

-- Product handlers: must only MUTATE profile.Data (no yields, no external side effects).
-- Side effects that are not persisted (VFX, temporary buffs) go in AFTER_GRANT.
local GRANTS: { [number]: GrantFn } = {
	[0000001] = function(_player, profile, _receipt) -- 1,000 coins pack
		profile.Data.Coins += 1000
	end,
	[0000002] = function(_player, profile, _receipt) -- starter pack (one-time per player)
		profile.Data.StarterPackOwned = true
		profile.Data.Coins += 500
	end,
}
local AFTER_GRANT: { [number]: (player: Player) -> () } = {}

local inFlight: { [string]: boolean } = {} -- same-server duplicate guard

local function isRecorded(data: PlayerDataShape?, purchaseId: string): boolean
	return data ~= nil and data.PurchaseIds ~= nil and table.find(data.PurchaseIds, purchaseId) ~= nil
end

-- Blocks until purchaseId is present in the last SAVED snapshot, or the session is lost.
local function waitUntilSaved(profile: Profile, purchaseId: string): boolean
	while profile:IsActive() do
		if isRecorded(profile.LastSavedData, purchaseId) then
			return true
		end
		local before = profile.LastSavedData
		profile:Save()
		if profile.LastSavedData == before then
			profile.OnAfterSave:Wait()
		end
		if isRecorded(profile.LastSavedData, purchaseId) then
			return true
		end
		task.wait(SAVE_RETRY_SECONDS)
	end
	return false
end

local function processReceipt(receipt: { [string]: any }): Enum.ProductPurchaseDecision
	local purchaseId = receipt.PurchaseId :: string
	local productId = receipt.ProductId :: number
	local player = Players:GetPlayerByUserId(receipt.PlayerId :: number)
	if not player then
		return Enum.ProductPurchaseDecision.NotProcessedYet -- re-delivered on next join
	end

	local grant = GRANTS[productId]
	if not grant then
		warn(`[Receipt] Unknown product {productId}; leaving unresolved so a hotfix can grant it`)
		return Enum.ProductPurchaseDecision.NotProcessedYet
	end

	if inFlight[purchaseId] then
		return Enum.ProductPurchaseDecision.NotProcessedYet
	end
	inFlight[purchaseId] = true

	local ok, decision = pcall(function(): Enum.ProductPurchaseDecision
		local profile = PlayerData.WaitForProfile(player, PROFILE_WAIT_SECONDS)
		if not profile or not profile:IsActive() then
			return Enum.ProductPurchaseDecision.NotProcessedYet
		end

		local data = profile.Data
		data.PurchaseIds = data.PurchaseIds or {}
		local firstTime = not isRecorded(data, purchaseId)
		if firstTime then
			grant(player, profile, receipt) -- atomic with the log entry below (same table, same save)
			table.insert(data.PurchaseIds, purchaseId)
			while #data.PurchaseIds > PURCHASE_ID_LOG_SIZE do
				table.remove(data.PurchaseIds, 1)
			end
		end

		if not waitUntilSaved(profile, purchaseId) then
			return Enum.ProductPurchaseDecision.NotProcessedYet -- session moved; the other server will see the log
		end

		if firstTime then
			local after = AFTER_GRANT[productId]
			if after then task.spawn(after, player) end
			if receipt.ProductPurchaseChannel ~= Enum.ProductPurchaseChannel.AdReward then
				-- value = Robux actually paid (reflects regional/test/Plus pricing)
				AnalyticsService:LogCustomEvent(player, "RobuxSpent", receipt.CurrencySpent :: number, {
					[Enum.AnalyticsCustomFieldKeys.CustomField01.Name] = tostring(productId),
				})
			end
		end
		return Enum.ProductPurchaseDecision.PurchaseGranted
	end)

	inFlight[purchaseId] = nil
	if not ok then
		warn(`[Receipt] Handler error for {purchaseId}: {decision}`)
		return Enum.ProductPurchaseDecision.NotProcessedYet
	end
	return decision :: Enum.ProductPurchaseDecision
end

MarketplaceService.ProcessReceipt = processReceipt -- the ONLY assignment in the codebase
```

Why it is correct:
- Grant and log entry live in the same `profile.Data` table, so they are saved together. Either both persist or neither does.
- A crash before the save → nothing was persisted and Roblox re-delivers the receipt → it is granted once.
- A crash after the save but before Roblox records `PurchaseGranted` → on re-delivery the log hits, nothing is granted again, and the call returns Granted.
- Two servers at once: only the server holding the session lock has `IsActive() == true`. The other returns `NotProcessedYet`, and its later re-delivery hits the log.

### Variant: plain DataStore (no session locking)
If the player's data is not session-locked, do the grant inside **one `UpdateAsync`** on the player's key: check `PurchaseIds` inside the transform, mutate, append, and return the new value. Then return `PurchaseGranted` only if `UpdateAsync` succeeded. Do **not** do `GetAsync` → modify → `SetAsync`, because that pattern races. In-memory caches of the same key must then be refreshed from the `UpdateAsync` result, otherwise the next autosave overwrites the grant.

### Variant: BindReceiptHandler (2026 API)
```lua
--!strict
-- ServerScriptService/Monetisation/AdRewardReceipts.server.luau
local MarketplaceService = game:GetService("MarketplaceService")
local AD_REWARD_PRODUCT = 0000003
-- Filtered handler: only this product. Returns Enum.ReceiptDecision (not ProductPurchaseDecision).
MarketplaceService:BindReceiptHandler(Enum.ReceiptType.DeveloperProduct, function(receipt: { [string]: any }): Enum.ReceiptDecision
	-- same idempotent grant pattern as above, mapped to Processed / NotProcessedYet
	return Enum.ReceiptDecision.NotProcessedYet
end, { AD_REWARD_PRODUCT })
```
Rules: binding a second handler for the same product, or a second catch-all, **throws**. Robux-transfer receipts (`RobuxTransferSender/Receiver`) can only be handled via `BindReceiptHandler`, and they are delivered to whatever server the user is currently in.

## Offline players, gifting, retries
- **Buyer offline:** do nothing. Return `NotProcessedYet`, and the receipt replays when they join any server of the game.
- **Gifts** (buyer pays, someone else receives): the receipt carries no recipient. Store `pendingGiftTarget[buyerUserId] = recipientUserId` server-side **before** prompting. In the handler, write the gift to the **recipient's** data idempotently (UpdateAsync on the recipient key, or a MessagingService hand-off to the recipient's server), then log the PurchaseId on the buyer's side. If the server that held the target crashed, the replay has no target. In that case grant the buyer a redeemable "gift token" instead of guessing. Check regional price levels before allowing gifts (see [[Gamepasses-vs-Developer-Products]]).
- **Limited stock / time-limited products:** check eligibility **before** prompting. Once Roblox charged, you must grant. A "sold out" reply in the handler is not an option: return Granted with an equivalent or compensation item.

## Common bugs that lose or double-grant purchases

| Bug | Effect | Fix |
|---|---|---|
| Two scripts assign `ProcessReceipt` (e.g. a free-model shop) | The last assignment wins and the other products never grant | Grep for `ProcessReceipt =`, keep one router |
| Returning `PurchaseGranted` before the save completes | The server crashes, the Robux is taken, nothing is granted | Wait for the saved snapshot (above) |
| Granting via `PromptProductPurchaseFinished` | Exploitable, and grants on cancel | Grant only in the receipt handler |
| No PurchaseId log, or log saved in a different key than the goods | Double grants on re-delivery | Same document, same write |
| Handler errors (nil leaderstats, character not loaded) | Default code returns nil and the purchase is lost, or it stays stuck | pcall + `NotProcessedYet`. Never depend on the character for persistent goods |
| `WaitForChild` / infinite yield inside the handler | The receipt never resolves until the server dies | Bounded waits |
| Product handler for a deleted or renamed ID | Old receipts stuck forever | Keep legacy IDs in `GRANTS` permanently |
| Publishing with no callback for even a minute | All receipts in that window auto-acknowledged and lost | Handler in the first published build. Use test mode |
| Data wipe / schema reset that also clears `PurchaseIds` | Re-delivered receipts grant twice, and paid goods vanish | Migrate, never wipe, paid fields (see [[Monetisation-Mistakes]]) |
| Not logging PurchaseId, ProductId and CurrencySpent | Cannot handle support tickets | Log to a `Purchases` DataStore or your analytics backend |

## Checklist
- [ ] Exactly one `ProcessReceipt` assignment, or deliberate `BindReceiptHandler` routing
- [ ] Every product ID ever sold is present in `GRANTS` (legacy IDs kept)
- [ ] Grant + PurchaseId in one atomic write. `PurchaseGranted` returned only after the durable save
- [ ] All failure paths return `NotProcessedYet`
- [ ] Tested: buy → kick before save → rejoin → granted once. Buy → hop server → granted once
- [ ] Store-tab external purchase tested in test mode before enabling external sales
- [ ] AdReward and CommerceProduct channels handled and excluded from revenue metrics
- [ ] Support log of PurchaseId / UserId / ProductId / CurrencySpent / timestamp

## Pitfalls
- Roblox does **not** store per-user developer-product history for you. If you don't log it, you can't verify a refund claim.
- Price tests and regional pricing mean the same product sells at different `CurrencySpent` values. Never validate on price.
- Studio test purchases don't charge and still call the handler, so a broken save path can look fine in Studio. Test in a live private server too.

## Related
- [[Monetisation/_Index]] · [[Gamepasses-vs-Developer-Products]] · [[Monetisation-Mistakes]] · [[Monetisation-Design-Checklist]]
- [[Data-Persistence-DataStores-And-ProfileStore]] · [[Analytics-And-Instrumentation]]

## Sources
- Roblox creator-docs, `reference/engine/classes/MarketplaceService.yaml` (ProcessReceipt guarantees/limitations, BindReceiptHandler), `reference/engine/enums/ProductPurchaseChannel.yaml`, `production/monetization/developer-products.md`, `robux-transfers.md`, `shop.md`. Snapshot 2026-10-02 of https://github.com/Roblox/creator-docs. Mirrors https://create.roblox.com/docs/reference/engine/classes/MarketplaceService#ProcessReceipt (accessed 2026-10-04)
- ProfileStore by loleris (DevForum / GitHub `MadStudioRoblox/ProfileStore`). Receipt pattern adapted from its developer-product example. ⚠️ verify: member names for your version
