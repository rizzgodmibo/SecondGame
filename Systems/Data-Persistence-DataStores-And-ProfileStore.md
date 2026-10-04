---
tags: [systems/data, systems/datastore]
status: draft
updated: 2026-10-04
confidence: high
---
# Data Persistence: DataStores and ProfileStore

## TL;DR
- Use **ProfileStore** (loleris / MAD STUDIO, v1.0.3) for player data: session locking, auto-save every 300 s, `EndSession` on leave, BindToClose handled for you. Don't hand-roll session locking.
- One profile per player, key `Player_<UserId>`, data ≤ ~100 KB in practice (hard limit **4,194,304 chars per key**). Keep a `Version` field and run migrations on load.
- If you write raw DataStore code: **`UpdateAsync`** for anything read-modify-write; `SetAsync` only for blind overwrites of keys nothing else writes. Always `pcall` + retry with backoff.
- Budgets (default per **server**, per minute, 2026-10-04): standard Get/Set/Remove **60 + 40 × players**, List **5 + 2 × players**; ordered Write/Remove **30 + 5 × players**. Per-key throughput: **25 MB/min read, 4 MB/min write**. `GetRequestBudgetForRequestType` before bulk work.
- Developer-product purchases: grant in `ProcessReceipt` **into the profile** and return `PurchaseGranted` only after the grant is in the session-locked data (ProfileStore pattern below); call `profile:Save()` for big purchases.
- GDPR/RTBF: call `profile:AddUserId(userId)` and configure **RTBF deletion templates** in Creator Hub → Data Stores Manager so Roblox deletes `Player_{UserId}` keys automatically.

## Details

### Limits (from Roblox docs, read 2026-10-04)
| Limit | Value |
|---|---|
| DataStore name / key name / scope | 50 chars each |
| Value size | 4,194,304 chars (serialized JSON) per key |
| Metadata | key name 50, value 250 chars, 300 total key-value pairs |
| Per-key throughput (rolling 60 s, rounded up to 1 KB per request) | Read 25 MB/min, Write 4 MB/min |
| Server default budget — standard Read/Write/Remove | 60 + numPlayers × 40 /min each (`UpdateAsync` consumes Read **and** Write) |
| Server default — standard List | 5 + numPlayers × 2 /min |
| Server default — ordered Read | 60 + numPlayers × 40; ordered Write/Remove 30 + numPlayers × 5; GetSorted 5 + numPlayers × 2 |
| Experience-wide (shared with Open Cloud) | Read 300 + CCU × 40, Write 300 + CCU × 20, List 300 + CCU × 2, Remove 300 + CCU × 40 /min |
| Throttle queue | 30 requests per queue; beyond that requests fail with 301–306 |
| Storage | 500 MB + 1 MB × lifetime users (compressed latest versions only); don't pre-compress |
| `GetAsync` cache | 4 s local cache; use `DataStoreGetOptions.UseCache = false` for verification reads |
| OrderedDataStore page size | 1–100 |
| BindToClose | server waits max **30 s** for all bound functions |
Server limits are configurable with `DataStoreService:SetRateLimitForRequestType()` — use it to stop one server (or Open Cloud tooling) eating the experience budget. Old "6-second write cooldown per key" is **not** in current docs; per-key limits are now throughput-based. ⚠️ verify: whether a per-key write cooldown still applies in practice.

### Decision rules
| Data | Store |
|---|---|
| Player progress, inventory, currency | ProfileStore (DataStore) |
| Global leaderboards (top 100) | OrderedDataStore, written on session end / every ≥ 60 s, read every ≥ 60 s and cached |
| Cross-server, ephemeral (matchmaking queues, live auctions, server lists, rate counters) | MemoryStore (sorted map / queue / hash map) |
| Cross-server notifications (announcements, "friend joined") | MessagingService |
| Gifts/trades to possibly-offline players that must not be lost | `ProfileStore:MessageAsync()` |
| Config you want to change without publishing | ⚠️ verify: Roblox "Configs" service availability; otherwise a DataStore key read on server start + MessagingService refresh |

### ProfileStore — complete DataService
```lua
--!strict
-- ServerScriptService/Server/Services/DataService.luau
-- Requires ServerScriptService/ServerPackages/ProfileStore (Wally: lm-loleris/profilestore@1.0.3)
local Players = game:GetService("Players")
local RunService = game:GetService("RunService")
local ServerScriptService = game:GetService("ServerScriptService")

local ProfileStore = require(ServerScriptService.ServerPackages.ProfileStore)

local DATA_VERSION = 2
local TEMPLATE = {
	Version = DATA_VERSION,
	Coins = 0,
	Gems = 0,
	Level = 1,
	Inventory = {} :: { [string]: number },
	PurchaseIds = {} :: { string }, -- last N processed receipt ids
	Settings = { Music = true },
}
export type PlayerData = typeof(TEMPLATE)
type Profile = ProfileStore.Profile<PlayerData>

-- Migrations: index n upgrades from version n to n+1. Never edit old ones.
local MIGRATIONS: { [number]: (data: any) -> () } = {
	[1] = function(data)
		-- v1 stored Coins as "Money"
		data.Coins = (data.Money or 0)
		data.Money = nil
	end,
}

local store = ProfileStore.New("PlayerData_v1", TEMPLATE)
if RunService:IsStudio() then
	store = store.Mock :: any -- don't touch live data from Studio playtests
end

local profiles: { [Player]: Profile } = {}
local DataService = {}

local function migrate(data: any)
	local v = data.Version or 1
	while v < DATA_VERSION do
		local step = MIGRATIONS[v]
		if step then step(data) end
		v += 1
	end
	data.Version = DATA_VERSION
end

local function onPlayerAdded(player: Player)
	local profile = store:StartSessionAsync(`Player_{player.UserId}`, {
		Cancel = function()
			return player.Parent ~= Players
		end,
	})
	if profile == nil then
		player:Kick("Data failed to load - please rejoin")
		return
	end
	profile:AddUserId(player.UserId) -- GDPR association
	migrate(profile.Data)
	profile:Reconcile() -- fill new template fields

	profile.OnSessionEnd:Connect(function()
		profiles[player] = nil
		player:Kick("Your data was loaded on another server - please rejoin")
	end)

	if player.Parent ~= Players then
		profile:EndSession()
		return
	end
	profiles[player] = profile
	player:SetAttribute("Coins", profile.Data.Coins)
	player:SetAttribute("DataLoaded", true)
end

function DataService.Init(self: typeof(DataService))
	for _, p in Players:GetPlayers() do task.spawn(onPlayerAdded, p) end
	Players.PlayerAdded:Connect(onPlayerAdded)
	Players.PlayerRemoving:Connect(function(player)
		local profile = profiles[player]
		if profile then profile:EndSession() end
	end)
	-- ProfileStore ends sessions itself on server shutdown (OnLastSave reason "Shutdown").
end

function DataService.GetProfile(self: typeof(DataService), player: Player): Profile?
	local profile = profiles[player]
	if profile and profile:IsActive() then return profile end
	return nil
end

function DataService.AddCoins(self: typeof(DataService), player: Player, amount: number): boolean
	local profile = self:GetProfile(player)
	if not profile then return false end
	profile.Data.Coins += amount
	player:SetAttribute("Coins", profile.Data.Coins)
	return true
end

return DataService
```

### Developer products with ProfileStore (idempotent)
```lua
--!strict
-- ServerScriptService/Server/Services/ReceiptService.luau
local MarketplaceService = game:GetService("MarketplaceService")
local Players = game:GetService("Players")
local DataService = require(script.Parent.DataService)

local PRODUCTS: { [number]: (data: any) -> () } = {
	[0000001] = function(data) data.Gems += 100 end, -- replace with real product ids
}
local MAX_STORED_IDS = 50

MarketplaceService.ProcessReceipt = function(info): Enum.ProductPurchaseDecision
	local player = Players:GetPlayerByUserId(info.PlayerId)
	if not player then return Enum.ProductPurchaseDecision.NotProcessedYet end
	-- Wait briefly for data to load (player may have just joined)
	local profile = DataService:GetProfile(player)
	local t = os.clock()
	while profile == nil and player.Parent == Players and os.clock() - t < 10 do
		task.wait(0.5)
		profile = DataService:GetProfile(player)
	end
	if profile == nil then return Enum.ProductPurchaseDecision.NotProcessedYet end

	local ids = profile.Data.PurchaseIds
	if table.find(ids, info.PurchaseId) then
		return Enum.ProductPurchaseDecision.PurchaseGranted -- already granted
	end
	local grant = PRODUCTS[info.ProductId]
	if not grant then return Enum.ProductPurchaseDecision.NotProcessedYet end
	if not profile:IsActive() then return Enum.ProductPurchaseDecision.NotProcessedYet end

	grant(profile.Data)
	table.insert(ids, info.PurchaseId)
	while #ids > MAX_STORED_IDS do table.remove(ids, 1) end
	profile:Save() -- 1 UpdateAsync; protects against crash before next auto-save
	return Enum.ProductPurchaseDecision.PurchaseGranted
end

return {}
```
⚠️ verify: Roblox's current recommended receipt pattern (docs page "player-data-purchasing" uses session-locked UpdateAsync with 180 s periodic save) — ProfileStore's `docs/devproducts` page is the reference for this library.

### Raw DataStore: UpdateAsync vs SetAsync
- `UpdateAsync(key, fn)` reads the latest value and writes atomically; `fn` may run **multiple times** — keep it pure (no side effects, no yields). Return `nil` to cancel the write.
- `SetAsync` overwrites blindly — data loss if another server wrote in between. Acceptable only for single-writer keys (e.g. a config blob you own).
- A failed write call doesn't guarantee the write didn't happen; verify with an uncached read if it matters.
- `IncrementAsync` for simple global counters (consumes Write budget).

### Session locking (why ProfileStore)
Without a lock, server A (player leaving, saving) and server B (player joined) race: B loads stale data → item duplication when trading. ProfileStore stores a session tag in the key; another server requesting the profile asks the owner to release, waits (`SESSION_STEAL` 40 s), and treats sessions with no updates for `ASSUME_DEAD` 630 s as crashed. Never use `{Steal = true}` in production.

### OrderedDataStore leaderboards
```lua
--!strict
-- ServerScriptService/Server/Services/LeaderboardService.luau
local DataStoreService = game:GetService("DataStoreService")
local ods = DataStoreService:GetOrderedDataStore("TopCoins_v1")

local cache: { { userId: number, value: number } } = {}

local function refresh()
	local ok, pages = pcall(function()
		return ods:GetSortedAsync(false, 100)
	end)
	if not ok then warn("leaderboard read failed", pages) return end
	local entries = (pages :: DataStorePages):GetCurrentPage()
	table.clear(cache)
	for _, e in entries do
		local userId = tonumber(string.match(e.key, "%d+"))
		if userId then table.insert(cache, { userId = userId, value = e.value }) end
	end
end

local function submit(userId: number, value: number)
	pcall(function()
		ods:SetAsync(`Player_{userId}`, math.floor(value)) -- integers only
	end)
end

task.spawn(function()
	while true do
		refresh()
		task.wait(120)
	end
end)

return { submit = submit, get = function() return cache end }
```
Submit on session end and at most every ≥ 60 s per player; ordered write budget is only 30 + 5 × players/min per server.

### MemoryStore quick facts (2026-10-04)
- Memory quota: **64 KB + 1.2 KB × users** (experience-wide); request units **1,000 + 120 × CCU per minute**.
- Single sorted map/queue: ≤ 1,000,000 items, ≤ 100 MB; ~30,000 request units/min per partition before throttling; hash map per-key ~5,000 writes / 15,000 reads per min.
- Default/maximum expiration 45 days. Always set the shortest TTL that works.
- Uses: matchmaking queues, cross-server party/trade state, global "recently active" lists, rate limits across servers. **Never** the only copy of anything a player paid for.

### Data versioning rules
1. Store `Version` in every profile; migrations are append-only and idempotent.
2. Never rename/remove a field without a migration; add new fields to TEMPLATE (Reconcile fills them).
3. Changing store name (`PlayerData_v1` → `_v2`) = fresh data for everyone; only do it with an explicit copy-on-load migration from the old store.
4. Use `ProfileStore:VersionQuery()` / DataStore versioning to roll back an individual player after a bug.

### GDPR / right to erasure
- Roblox emails creators RTBF requests; you must delete that user's data.
- Configure **automated RTBF**: Creator Hub → game → Configure → **Data Stores Manager → RTBF Deletion → Create Template**, e.g. Standard Key, store `PlayerData_v1`, key `Player_{UserId}`; also Ordered Key `TopCoins_v1` / `Player_{UserId}`. Up to 100 templates. Can also be set via Open Cloud Configs API (`user_data_templates`).
- Using a static prefix (`Player_`) is why the key format matters — templates need a matchable pattern. ⚠️ verify: whether a bare `{UserId}` key pattern (ProfileStore tutorial default) is accepted.
- Keep any user data in other stores (MemoryStore, analytics) keyed so it can be deleted too.

## Checklist
- [ ] ProfileStore installed server-side; Mock in Studio.
- [ ] Key `Player_<UserId>`, `AddUserId` called, RTBF templates configured.
- [ ] `Version` + migrations table; `Reconcile` after migrate.
- [ ] Kick on load failure; kick on `OnSessionEnd`.
- [ ] ProcessReceipt idempotent with stored `PurchaseId`s and `profile:Save()`.
- [ ] Studio "Enable Studio Access to API Services" only when deliberately testing live data.
- [ ] Data size logged (`#HttpService:JSONEncode(profile.Data)`) and alerted above ~500 KB.

## Pitfalls
- Saving on every change → throttling and queue drops (errors 301–306).
- Writing `profile.Data` after `OnSessionEnd` — silently not saved.
- Yielding between `IsActive()` check and mutation in trades — check, mutate both profiles, no yields.
- Storing Instances, Vector3/CFrame or mixed tables directly — not JSON-serialisable; convert to plain tables.
- Leaderstats as the source of truth (it's display; exploiters can't change server values but devs often read from it and drift).
- Pre-compressing JSON yourself — wastes CPU; DataStores compress already.
- Using OrderedDataStore with non-integer values (error 106).

## Related
- [[Error-Handling-And-Logging]]
- [[Module-Architecture]]
- [[Anti-Exploit-And-Server-Authority]]
- [[Common-Libraries]]
- [[Project-Bootstrap-Checklist]]

## Sources
- https://create.roblox.com/docs/cloud-services/data-stores/error-codes-and-limits (via github.com/Roblox/creator-docs commit of 2026-10-02, read 2026-10-04)
- https://create.roblox.com/docs/cloud-services/data-stores/versioning-listing-and-caching (4 s cache)
- https://create.roblox.com/docs/cloud-services/data-stores/right-to-be-forgotten (RTBF templates)
- https://create.roblox.com/docs/cloud-services/data-stores/best-practices
- https://create.roblox.com/docs/cloud-services/memory-stores
- https://create.roblox.com/docs/reference/engine/classes/DataModel#BindToClose (30 s)
- https://github.com/MadStudioRoblox/ProfileStore (docs/api.md, ProfileStore.luau constants; wally.toml v1.0.3; read 2026-10-04)
