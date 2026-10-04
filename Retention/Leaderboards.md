---
tags: [retention/leaderboards]
status: draft
updated: 2026-10-04
confidence: medium
---
# Leaderboards

## TL;DR
- **Three tiers:** `leaderstats` (in-server, the built-in player list), **OrderedDataStore** (persistent global: all-time, weekly), and **MemoryStore SortedMap** (real-time, short-lived: hourly/daily/event, ≤ 45 days).
- **Weekly beats all-time for retention.** An all-time board is frozen by the top 0.1%. A weekly board resets Monday 00:00 UTC and gives everyone a fresh shot. Use the key/store suffix `weekIndex = floor((os.time() - 345600) / 604800)`. 345600 s offsets the Thursday epoch to a Monday.
- **Write throttled, read cached.** Push a player's score every ~120 s only if it changed, plus on leave. Each server refreshes the top 100 every 60–120 s. Per-server limits are `OrderedWrite 30 + 5×players/min` and `OrderedList 5 + 2×players/min`. `GetSortedAsync` page size is 1–100.
- **Only server-owned values reach a board.** Write from the profile data (never from a client-sent number), sanity-cap the delta per interval, exclude banned users, and keep a `RemoveAsync` path for cleanup.
- **Show the player's own rank context** ("You: #4,213, 1,200 to #4,000"). Only the top 0.01% ever see themselves on a top-100. Pair with friend leaderboards for everyone else.
- OrderedDataStore values must be **integers**. Store scaled ints for decimals, e.g. time in ms (ascending for speedruns).

## Which tier for what
| Need | Use | Why |
|---|---|---|
| Show stats in player list | `leaderstats` Folder with `IntValue`/`NumberValue` under the Player | Built-in UI. Server-set only. |
| All-time / weekly global top 100 | `OrderedDataStore` | Persistent, integer-sorted |
| Hourly/daily/event top, near-real-time | `MemoryStoreSortedMap` | Fast, `sortKey` numeric or string, TTL ≤ 3,888,000 s (45 days) |
| Friend leaderboard | `GetFriendsOnlineAsync` / friends' UserIds → batch `GetAsync` on the OrderedDataStore | Relevant to everyone |
| Guild/clan board | OrderedDataStore keyed by guildId | Same pattern |

## Limits (Roblox docs, accessed 2026-10-04)
| API | Per-server limit (req/min) | Experience-wide (shared with Open Cloud) |
|---|---|---|
| OrderedDataStore `GetAsync`/`UpdateAsync` read | 60 + 40×players | 300 + 40×CCU |
| `SetAsync`/`IncrementAsync`/`UpdateAsync` write | 30 + 5×players | 300 + 20×CCU |
| `GetSortedAsync` | 5 + 2×players | 300 + 2×CCU |
| `RemoveAsync` | 30 + 5×players | 300 + 40×CCU |
| MemoryStore (all calls) | — | 1000 + 120×CCU request units/min. ~30,000 units/min throttle per partition (a sorted map lives on one partition). 100,000 units/min per structure. |
| SortedMap sizes | key ≤ 128 chars, value ≤ 32 KB, sortKey ≤ 128 chars, ≤ 1,000,000 items, `GetRangeAsync` count ≤ 200 | memory quota 64 KB + 1.2 KB×users |

## Code

### Shared time helpers (ReplicatedStorage/Shared/TimeKeys, ModuleScript)
```lua
--!strict
-- ReplicatedStorage/Shared/TimeKeys (ModuleScript)
local TimeKeys = {}
local DAY = 86400
local WEEK = 604800
local MONDAY_OFFSET = 345600 -- 1970-01-05 00:00 UTC was a Monday

function TimeKeys.dayIndex(t: number): number
	return math.floor(t / DAY)
end

function TimeKeys.weekIndex(t: number): number
	return math.floor((t - MONDAY_OFFSET) / WEEK)
end

function TimeKeys.secondsUntilWeekReset(t: number): number
	local nextStart = (TimeKeys.weekIndex(t) + 1) * WEEK + MONDAY_OFFSET
	return nextStart - t
end

return TimeKeys
```

### Global + weekly board (ServerScriptService/Leaderboards, Script)
```lua
--!strict
-- ServerScriptService/Leaderboards (Script)
-- Assumes your data layer keeps authoritative totals in profile.Data:
--   Coins (all-time earned, integer) and WeeklyCoins + WeeklyIndex (reset lazily).
local DataStoreService = game:GetService("DataStoreService")
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local ServerScriptService = game:GetService("ServerScriptService")
local UserService = game:GetService("UserService")

local TimeKeys = require(ReplicatedStorage.Shared.TimeKeys)
local PlayerData = require(ServerScriptService.Data.PlayerData) :: any -- GetProfile(player)

local WRITE_INTERVAL = 120
local READ_INTERVAL = 90
local TOP_N = 100
local MAX_WEEKLY_GAIN_PER_INTERVAL = 50_000 -- tune: > max legit earn rate * WRITE_INTERVAL

local allTimeStore = DataStoreService:GetOrderedDataStore("Coins_AllTime")
local function weeklyStore(week: number): OrderedDataStore
	return DataStoreService:GetOrderedDataStore(`Coins_Week_{week}`)
end

local banned: { [number]: boolean } = {} -- load from your ban list / Players:GetBanHistoryAsync tooling
local lastWritten: { [number]: { allTime: number, weekly: number } } = {}

-- leaderstats (in-server display)
local function setupLeaderstats(player: Player)
	local folder = Instance.new("Folder")
	folder.Name = "leaderstats"
	local coins = Instance.new("IntValue")
	coins.Name = "Coins"
	coins.Parent = folder
	folder.Parent = player
end
Players.PlayerAdded:Connect(setupLeaderstats)

local function flagSuspicious(player: Player, delta: number)
	warn(`[Leaderboard] Suspicious gain {delta} by {player.UserId}`)
	-- Log via AnalyticsService:LogCustomEvent / webhook; don't auto-ban on one signal.
end

local function writePlayer(player: Player)
	if banned[player.UserId] then
		return
	end
	local profile = PlayerData.GetProfile(player)
	if not profile then
		return
	end
	local data = profile.Data
	local week = TimeKeys.weekIndex(os.time())
	if data.WeeklyIndex ~= week then
		data.WeeklyIndex = week
		data.WeeklyCoins = 0
	end
	local allTime = math.floor(data.Coins)
	local weekly = math.floor(data.WeeklyCoins)
	local prev = lastWritten[player.UserId]
	if prev and prev.allTime == allTime and prev.weekly == weekly then
		return -- unchanged: save budget
	end
	if prev and weekly - prev.weekly > MAX_WEEKLY_GAIN_PER_INTERVAL then
		flagSuspicious(player, weekly - prev.weekly)
		return -- hold the write until reviewed
	end
	local key = tostring(player.UserId)
	local ok1 = pcall(function()
		-- Monotonic all-time: never lower a score because of a stale server.
		allTimeStore:UpdateAsync(key, function(old: number?)
			if old and old >= allTime then
				return nil -- cancel write
			end
			return allTime
		end)
	end)
	local ok2 = pcall(function()
		weeklyStore(week):SetAsync(key, weekly)
	end)
	if ok1 and ok2 then
		lastWritten[player.UserId] = { allTime = allTime, weekly = weekly }
	end
	local ls = player:FindFirstChild("leaderstats")
	local coinsValue = ls and ls:FindFirstChild("Coins")
	if coinsValue and coinsValue:IsA("IntValue") then
		coinsValue.Value = allTime
	end
end

export type Entry = { rank: number, userId: number, name: string, value: number }

local function readTop(store: OrderedDataStore): { Entry }
	local ok, pages = pcall(function()
		return store:GetSortedAsync(false, TOP_N)
	end)
	if not ok then
		return {}
	end
	local page = (pages :: DataStorePages):GetCurrentPage()
	local ids: { number } = {}
	for _, item in page do
		table.insert(ids, tonumber(item.key) :: number)
	end
	local names: { [number]: string } = {}
	local infoOk, infos = pcall(function()
		return UserService:GetUserInfosByUserIdsAsync(ids)
	end)
	if infoOk then
		for _, info in infos do
			names[info.Id] = info.DisplayName
		end
	end
	local out: { Entry } = {}
	for i, item in page do
		local uid = tonumber(item.key) :: number
		if not banned[uid] then
			table.insert(out, { rank = i, userId = uid, name = names[uid] or "?", value = item.value })
		end
	end
	return out
end

-- Publish to clients through a replicated StringValue (JSON) or RemoteEvent; here: attribute JSON.
local HttpService = game:GetService("HttpService")
local boardFolder = Instance.new("Folder")
boardFolder.Name = "Leaderboards"
boardFolder.Parent = ReplicatedStorage

task.spawn(function()
	while true do
		local week = TimeKeys.weekIndex(os.time())
		boardFolder:SetAttribute("AllTime", HttpService:JSONEncode(readTop(allTimeStore)))
		boardFolder:SetAttribute("Weekly", HttpService:JSONEncode(readTop(weeklyStore(week))))
		boardFolder:SetAttribute("WeeklyResetIn", TimeKeys.secondsUntilWeekReset(os.time()))
		task.wait(READ_INTERVAL)
	end
end)

task.spawn(function()
	while true do
		task.wait(WRITE_INTERVAL)
		for _, p in Players:GetPlayers() do
			task.spawn(writePlayer, p)
		end
	end
end)

Players.PlayerRemoving:Connect(function(p)
	writePlayer(p)
	lastWritten[p.UserId] = nil
end)

game:BindToClose(function()
	for _, p in Players:GetPlayers() do
		task.spawn(writePlayer, p)
	end
	task.wait(3)
end)
```
Notes:
- Attribute strings are fine for 100 rows (~5 KB). For bigger payloads use a RemoteEvent.
- `PlayerRemoving` → `writePlayer` must run **before** your data layer ends the profile session. Order it explicitly in your data module.
- Weekly board stores accumulate (one per week). They cost nothing while idle. Never iterate old ones.

### Real-time event board with MemoryStore SortedMap (ServerScriptService/EventBoard, ModuleScript)
```lua
--!strict
-- ServerScriptService/EventBoard (ModuleScript)
local MemoryStoreService = game:GetService("MemoryStoreService")

local EventBoard = {}
local TTL = 7 * 86400 -- keep for the event + buffer (max 3,888,000)

function EventBoard.map(eventId: string): MemoryStoreSortedMap
	return MemoryStoreService:GetSortedMap(`EventBoard_{eventId}`)
end

-- Add to a player's score atomically; sortKey = score so the map sorts by score.
function EventBoard.addScore(eventId: string, userId: number, delta: number): boolean
	local ok = pcall(function()
		EventBoard.map(eventId):UpdateAsync(tostring(userId), function(old: any, oldSortKey: any)
			local score = (if typeof(oldSortKey) == "number" then oldSortKey else 0) + delta
			return score, score -- value, sortKey
		end, TTL)
	end)
	return ok
end

function EventBoard.top(eventId: string, count: number): { { userId: number, score: number } }
	local ok, items = pcall(function()
		return EventBoard.map(eventId):GetRangeAsync(Enum.SortDirection.Descending, math.min(count, 200))
	end)
	local out = {}
	if ok then
		for _, item in items do
			table.insert(out, { userId = tonumber(item.key) :: number, score = item.sortKey :: number })
		end
	end
	return out
end

return EventBoard
```
Batch `addScore` per player (accumulate locally, flush every 10–30 s). Every call costs request units on the single partition. Above ~5k CCU, shard into N maps by `userId % N` and merge the top lists. When the event ends, copy the final top 100 into an OrderedDataStore or DataStore for the permanent record (MemoryStore is not durable).

### Weekly rewards (pattern)
1. On server start and hourly, if `weekIndex(now) > lastProcessedWeek`, try to take a lock: `DataStore:UpdateAsync("WeekProcessed_" .. (week-1), …)` returns true only for the first server.
2. The lock winner reads the previous week's top 100 and writes `PendingRewards_<userId>` entries (title, badge, crate) to a DataStore.
3. On join, each player's server checks pending rewards, grants them into the profile and deletes the key.
4. Announce the winners in-game, in Discord and via the community announcement ([[Community-Management]]).

## Anti-cheat on leaderboard values
- **Authority:** scores come only from server-side game logic. Remotes request *actions* ("swing", "sell"), never amounts.
- **Rate sanity:** compute max legit gain per interval (best gear × max multipliers × interval) and hold writes above it for review. Log flagged users.
- **Monotonic all-time** via `UpdateAsync` (above) so a stale server or rollback cannot lower or overwrite a score.
- **Exclusion:** maintain a banned/excluded set. Skip them on read and `RemoveAsync` their key. Use `Players:BanAsync` (verified to exist, 2026-10) for confirmed cheaters. Parameter details belong in the moderation notes.
- **Display-side filtering:** names come from `UserService` (already moderated). Never display user-entered text on boards without `TextService` filtering.
- **Studio/test data:** use a different store name (`Coins_AllTime_DEV`) when `RunService:IsStudio()`, or test in a separate place/universe.

## Checklist
- [ ] leaderstats shows 1–3 stats max (player list is cramped on mobile)
- [ ] Weekly board with visible reset countdown + rewards for top 1/10/100 and participation tiers
- [ ] Own-rank / next-target display. Friend board.
- [ ] Writes throttled and change-only. Reads cached and shared per server.
- [ ] Monotonic all-time writes. Suspicious-gain hold. Ban exclusion.
- [ ] Physical in-world leaderboard near spawn (social proof) + UI version
- [ ] Separate dev/test store names

## Pitfalls
- Writing every coin change (instant throttling, `OrderedWriteExperienceThrottled`).
- Non-integer values in OrderedDataStore (error). Floats need scaling.
- Reading top-100 per player instead of per server.
- An all-time board as the only board. New players see an unreachable wall.
- Forgetting `GetSortedAsync` returns `DataStorePages`. Rank = index within page + (pageNumber−1)×pageSize.
- MemoryStore boards with no persistence step. Data expires or evicts.

## Related
- [[Retention/_Index]] · [[Events-And-Seasons]] · [[Friend-And-Group-Play]] · [[Data-Persistence-DataStores-And-ProfileStore]] · [[Live-Ops-Playbook]] · [[Analytics-And-Instrumentation]] · [[Core-Loops]]

## Sources
- Roblox Creator Docs, "Data store error codes and limits", https://create.roblox.com/docs/cloud-services/data-stores/error-codes-and-limits (creator-docs mirror commit 2026-10-02; accessed 2026-10-04)
- Roblox Engine API, `OrderedDataStore` (integers only, `GetSortedAsync(ascending, pagesize, minValue, maxValue)`), https://create.roblox.com/docs/reference/engine/classes/OrderedDataStore (accessed 2026-10-04)
- Roblox Creator Docs, "Memory stores" (quotas, partition limits) and "Sorted map", https://create.roblox.com/docs/cloud-services/memory-stores (accessed 2026-10-04)
- Roblox Engine API, `MemoryStoreSortedMap` (`GetRangeAsync` count ≤ 200, `UpdateAsync` transform returns value + sortKey), `UserService:GetUserInfosByUserIdsAsync` (accessed 2026-10-04)
