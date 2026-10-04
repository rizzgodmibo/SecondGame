---
tags: [monetisation/products, systems/marketplace]
status: draft
updated: 2026-10-04
confidence: high
---
# Passes vs Developer Products

## TL;DR
- **Pass** = bought once, owned forever, and Roblox tracks ownership (`UserOwnsGamePassAsync`). Use it for permanent perks: VIP, 2× currency, extra slots, auto-collect, a radio, a permanent cosmetic.
- **Developer product** = can be bought repeatedly, and **you** track ownership. Use it for currency packs, consumables, boosts, revives, skips, limited-time bundles, gifts, and anything one-time that you want to be able to **reset or gift**.
- Prices: 1 – 1,000,000,000 R$ for both. You keep 70%. Since 2026-05-30 **cross-game pass and product sales are disabled**. Since 2025-04 **regional pricing is on by default for passes** (Managed Pricing). Products need opt-in.
- **Always fetch prices at runtime with `GetProductInfoAsync`** on the client, never hard-code them. Price tests, regional pricing and Roblox Plus discounts all change the real price.
- Check pass ownership on the server at join (batched with `task.spawn`) and cache it in a player attribute or your data module. Update the cache on `PromptGamePassPurchaseFinished`. Grant products **only** in the receipt handler ([[ProcessReceipt-Handling]]).
- Note `GetProductInfo` is deprecated in favour of `GetProductInfoAsync`, and `InfoType.GamePass` vs `InfoType.Product` must match the ID type.

## Decision table

| Need | Use | Why |
|---|---|---|
| Permanent perk, single purchase | Pass | Roblox persists ownership. It survives your data loss. It shows on the game page Store tab and in Shop |
| Repeatable purchase (currency, potion, revive) | Product | Passes can't be re-bought |
| One-time offer that should be reset per season, or one-per-account but giftable | Product + your own flag | You control the flag and can re-offer |
| Gifting to another player | Product ("Gift: VIP") | No native pass gifting API exists ⚠️ verify: no 2026 gifting API |
| Reward for watching a rewarded video ad | Product (required) | `AdService:CreateAdRewardFromDevProductId` only takes products |
| Recurring monthly benefit | Subscription | See [[Subscriptions-And-Premium-Payouts]] |
| Featured on the Buy Robux page (free promo) | Pass priced 50–800 R$, no random items | Only passes can be promoted |
| Tiered upgrade (Tier 1 → 2 → 3) | Products with server-side tier gating, or one pass per tier | Products give more pricing flexibility. Passes are more trusted |

## API cheat sheet (MarketplaceService, 2026-10)

| Task | API | Side | Notes |
|---|---|---|---|
| Price/name for UI | `GetProductInfoAsync(id, Enum.InfoType.Product / .GamePass)` | Client (for personalised price) | Fields `PriceInRobux`, `UserBasePriceInRobux`, `PriceDiscountDetails` (Plus), `IsForSale` |
| All products | `GetDeveloperProductsAsync()` → Pages | Either | Build shop lists |
| Personalised order | `RankProductsAsync({ {InfoType, Id} })` | Server/client | Strict rate limit: call **once at join** |
| "Top picks" | `RecommendTopProductsAsync({InfoType...})` | Either | Up to 50. Empty if no sales in 28 days. Excludes owned passes. Wrap in `task.spawn` |
| Pass ownership | `UserOwnsGamePassAsync(userId, passId)` | Either (trust the server) | Cached. Always true on first join after purchase. Transparent batching |
| Prompt pass | `PromptGamePassPurchase(player, passId)` | Client or server | |
| Pass prompt closed | `PromptGamePassPurchaseFinished(player, passId, wasPurchased)` | Server | OK to grant **pass** perks here, as ownership is authoritative |
| Prompt product | `PromptProductPurchase(player, productId)` | Client or server | |
| Grant product | `ProcessReceipt` / `BindReceiptHandler` | Server | Never `PromptProductPurchaseFinished` |
| Regional price level | `GetUsersPriceLevelsAsync({userIds})` → 1–1000 | Server | Gate trades and gifts. Don't cache across sessions |
| Plus status | `Player.HasRobloxSubscription`, `GetRobloxSubscriptionDetailsAsync` | | |
| Paid random items allowed? | `PolicyService:GetPolicyInfoForPlayerAsync(p).ArePaidRandomItemsRestricted` | Server | Also `IsPaidItemTradingAllowed` |
| Built-in Shop | `MarketplaceService:OpenShop(player)`. Hide the menu entry with `StarterGui:SetCoreGuiEnabled(Enum.CoreGuiType.ExperienceShop, false)` | Either | Roblox-ranked overlay of all passes + listed products. Can also surface Robux packs that bundle your items |

## Pass ownership cache (server)

```lua
--!strict
-- ServerScriptService/Monetisation/PassService.luau  (ModuleScript)
local MarketplaceService = game:GetService("MarketplaceService")
local Players = game:GetService("Players")

local PassService = {}

export type PassName = "VIP" | "DoubleCoins" | "ExtraSlots"
local PASS_IDS: { [PassName]: number } = {
	VIP = 0000001,
	DoubleCoins = 0000002,
	ExtraSlots = 0000003,
}

local owned: { [Player]: { [number]: boolean } } = {}
local onGranted = Instance.new("BindableEvent") -- (player, passName)
PassService.Granted = onGranted.Event

local function nameFor(passId: number): PassName?
	for name, id in PASS_IDS do
		if id == passId then return name end
	end
	return nil
end

local function setOwned(player: Player, passId: number)
	local t = owned[player]
	if not t or t[passId] then return end
	t[passId] = true
	local name = nameFor(passId)
	if name then
		player:SetAttribute("Pass_" .. name, true) -- replicated read-only hint for client UI
		onGranted:Fire(player, name)
	end
end

local function loadOwnership(player: Player)
	owned[player] = {}
	for _, passId in PASS_IDS do
		task.spawn(function() -- concurrent calls are transparently batched
			for attempt = 1, 3 do
				local ok, has = pcall(MarketplaceService.UserOwnsGamePassAsync, MarketplaceService, player.UserId, passId)
				if ok then
					if has then setOwned(player, passId) end
					return
				end
				task.wait(2 ^ attempt)
			end
		end)
	end
end

function PassService.Owns(player: Player, pass: PassName): boolean
	local t = owned[player]
	return t ~= nil and t[PASS_IDS[pass]] == true
end

function PassService.Id(pass: PassName): number
	return PASS_IDS[pass]
end

MarketplaceService.PromptGamePassPurchaseFinished:Connect(function(player: Player, passId: number, purchased: boolean)
	if purchased then setOwned(player, passId) end
end)
Players.PlayerAdded:Connect(loadOwnership)
Players.PlayerRemoving:Connect(function(p) owned[p] = nil end)
for _, p in Players:GetPlayers() do task.spawn(loadOwnership, p) end

return PassService
```

Rules for consumers:
- Read `PassService.Owns` on the **server** for every gameplay effect.
- Subscribe to `PassService.Granted` so a purchase mid-session applies **instantly**, without a rejoin. "Rejoin to receive your item" is a top cause of refund complaints.
- If you also mirror ownership into saved data (e.g. for offline leaderboards), treat `UserOwnsGamePassAsync` as the source of truth.

## Client price display (dynamic, required for Managed Pricing / Plus)

```lua
--!strict
-- StarterPlayerScripts/Shop/PriceLabel.client.luau
local MarketplaceService = game:GetService("MarketplaceService")

local cache: { [string]: { price: number, base: number, at: number } } = {}
local TTL = 300

local function getPrice(id: number, infoType: Enum.InfoType): (number?, number?)
	local key = `{infoType.Name}:{id}`
	local hit = cache[key]
	if hit and os.clock() - hit.at < TTL then return hit.price, hit.base end
	local ok, info = pcall(MarketplaceService.GetProductInfoAsync, MarketplaceService, id, infoType)
	if not ok or type(info) ~= "table" then return nil, nil end
	local price = (info :: any).PriceInRobux :: number?
	local base = ((info :: any).UserBasePriceInRobux or price) :: number?
	if price then cache[key] = { price = price, base = base or price, at = os.clock() } end
	return price, base
end

-- Usage: show strike-through base price when a Plus/regional discount applies.
local function bind(label: TextLabel, id: number, infoType: Enum.InfoType)
	task.spawn(function()
		local price, base = getPrice(id, infoType)
		if not price then label.Text = "…"; return end
		label.Text = if base and base > price then `<s>{base}</s> R$ {price}` else `R$ {price}`
		label.RichText = true
	end)
end

return bind
```

## Gifting pattern (products)
1. The gifter selects a recipient in the server. The server validates that the recipient is in the same server (or exists), that the gift isn't already owned, and that **price levels allow it**: allow gifting only if `senderLevel >= recipientLevel` via `GetUsersPriceLevelsAsync`. This blocks regional-price arbitrage.
2. The server stores `pendingGift[gifterId] = {recipient, sku, expires = now + 120}`, then calls `PromptProductPurchase(gifter, GIFT_PRODUCT[sku])`.
3. The receipt handler grants to the recipient idempotently, and falls back to a "gift token" for the buyer if the context is lost. See [[ProcessReceipt-Handling]].
4. Gifting is a strong social conversion driver. Announce it server-wide ("X gifted Y VIP!"). Rate-limit it to stop spam.

## Checklist
- [ ] Every perk mapped to pass / product / subscription using the table above
- [ ] No hard-coded prices (run **Dynamic Price Check** in Creator Hub → Monetization → Managed Pricing)
- [ ] Pass perks apply mid-session on purchase, without a rejoin
- [ ] Ownership checked server-side, with retries and batching
- [ ] Every product has a thumbnail (required for external/Store sales and Shop surfaces)
- [ ] Products listed in Shop (Monetization → Shop) where appropriate. Passes are always listed
- [ ] One pass created specifically for Buy Robux page promotion (50–800 R$)
- [ ] Gifting gated by price level, and rate-limited

## Pitfalls
- **Selling one-time "permanent" items as products without saving a flag** → the item is lost on a data wipe, and the player paid. Prefer passes for permanence: Roblox remembers them even if your data breaks.
- **Passes can't be revoked or reset.** If you plan to rebalance a perk (e.g. 2× → 1.5×), you will face backlash. Design pass perks you can honour forever. See [[Monetisation-Mistakes]].
- Calling `UserOwnsGamePassAsync` in a loop or every frame: it is cached, but still yields and rate-limits.
- Using the client's word for ownership: exploiters can set attributes locally. The server decides.
- Cross-game passes (donation games, "buy my pass in another game") stopped working on 2026-05-30. Use `PromptRobuxTransferAsync` (Plus users only) instead.

## Related
- [[Monetisation/_Index]] · [[ProcessReceipt-Handling]] · [[Pricing-Psychology]] · [[Subscriptions-And-Premium-Payouts]] · [[Pay-To-Win-Boundaries]]
- [[Data-Persistence-DataStores-And-ProfileStore]] · [[Economy-Design-Sinks-And-Faucets]]

## Sources
- Roblox creator-docs (snapshot 2026-10-02): `production/monetization/passes.md`, `developer-products.md`, `regional-pricing.md`, `managed-pricing.md`, `shop.md`, `roblox-plus.md`; `reference/engine/classes/MarketplaceService.yaml` (UserOwnsGamePassAsync caching, GetProductInfo deprecation). Mirrors https://create.roblox.com/docs/production/monetization/passes and /developer-products (accessed 2026-10-04)
- DevForum, "Introducing Regional Pricing for Passes" (2025-04): https://devforum.roblox.com/t/introducing-regional-pricing-for-passes/3621382
- DevForum, "Introducing Regional Pricing for Developer Products" (2025): https://devforum.roblox.com/t/introducing-regional-pricing-for-developer-products/3971235
