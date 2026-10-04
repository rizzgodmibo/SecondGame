---
tags: [operations/servers, systems/networking]
status: reviewed
updated: 2026-10-04
confidence: medium
---
# Server Scaling And Matchmaking

## TL;DR
- **Server size sets how full the game looks and how social it feels.** Defaults: simulators/tycoons/obbies **12–20**, social/roleplay **20–40**, round-based PvP **10–24**, horror co-op **4–8** per match (lobby 20–30). Small servers fill faster, so a new game looks active. Larger servers let one influencer pack hundreds of players into a single place.
- Leave server fill on **"Roblox optimizes server fill"**, which reserves social slots so friends can follow each other. Choose "fill as full as possible" only for games where a packed server is the point (e.g. a big social hub).
- Use one **universe** with multiple **places** (lobby + match places), joined via `TeleportService:TeleportAsync` from the **server** only. Set "Access Control for Places" to **Secure within universe** if non-start places must only be reached through your teleports.
- **Reserved servers** (`TeleportOptions.ShouldReserveServer` or `ReserveServerAsync`) are for matches and parties. Pair them with a **MemoryStore queue** for cross-server matchmaking. Roblox's **custom matchmaking** (scoring signals, `MatchmakingService` server attributes) tunes which *public* server a player joins, with no code.
- Cross-server state: **MessagingService** for broadcast (≤1 KB, about 1–2 s, best-effort), **MemoryStore** for shared ephemeral state (queues, global leaderboards, locks), **DataStores** for durable data. Know the quotas (table below) and pick the cheapest primitive.

## Choosing MaxPlayers (Place → Settings)
| Genre | Max players | Why |
|---|---|---|
| Simulator / clicker / tycoon | 12–16 (plots ≤ max) | One plot per player; fills fast; low server cost per player |
| Obby / tower | 15–30 | Social proof; low sync cost |
| Social hangout / roleplay | 25–50 | Density is the content. ⚠️ Social hangouts are **16+ only** (see [[Moderation-And-Policy-Compliance]]) |
| Round PvP (arena) | 10–24 | Match length × kill density |
| Battle royale / big shooter | 50–100 | Needs streaming-enabled maps and performance work |
| Co-op horror (Doors-style) | Lobby 20–40, match reserved 1–4/6 | Lobby → elevator → reserved server |

Rules:
- **Pre-launch / < 500 CCU:** prefer the *smaller* end so the first servers fill. A 50-slot server with 3 people looks dead.
- **Spike capacity:** an influencer stream sends thousands of joins in minutes. Roblox spins up servers automatically, so your limits are the per-universe quotas (DataStore, MemoryStore, MessagingService), not server count. Load-test those code paths.
- **Max server size:** Roblox has supported up to 700 players per server since 2023 ⚠️ verify (DevForum "Experience Join Improvements" 2023). Social-slot reservations can be customised up to 20% of max players.
- Performance budget scales with player count. Profile server heartbeat ≥ 55 Hz at max players on a full map before raising the cap.

## Server fill options (Place → Access/Settings)
- **Roblox optimizes server fill**: leaves slots for friends. This is the default and the recommended choice.
- **Fill each server as full as possible**: maximises density, but friends can't follow.
- **Customize reserved slots**: up to 20% of max (rounded down). Some devs report it behaves unexpectedly (DevForum 2023), so check after changing it.

## Places and universes
- Start place = lobby/hub (fast load, under about 5 s on mobile; shop + social). Extra places = worlds, match maps, private events.
- Each place has its own MaxPlayers. Places in a universe **share DataStores, MemoryStores, MessagingService topics, Configs and Analytics**.
- Teleports keep players in the universe, so analytics count them as one session. Inbound cross-game teleports show as the "Teleport" acquisition source.
- Teleport data set with `TeleportOptions:SetTeleportData()` is **client-visible and unencrypted**. Pass a match ID and look up authority data server-side (MemoryStore HashMap).

## Limits that matter (creator-docs 2026-10-02)
| Service | Limit |
|---|---|
| MessagingService | Message ≤ **1 KB**; send **600 + 240 × players/min per server**; receive per topic **40 + 80 × servers/min**; whole game **400 + 200 × servers/min**; subscriptions per server **20 + 8 × players**; subscribe requests **240/min per server**; topic names 1–80 chars |
| MemoryStore memory | **64 KB + 1.2 KB × users** per universe (shrinks only after an 8-day lag) |
| MemoryStore requests | **1,000 + 120 × CCU** request units/min per universe; ranged reads cost 1 unit per item returned |
| MemoryStore structure | Sorted map/queue: ≤ **1M items**, ≤ **100 MB**, ~**100k RU/min per structure**; single partition throttles at ~**30k RU/min**; hash-map key ~5k writes / 15k reads per min; item value ≤ **32 KB**; default expiration **45 days** (max) |
| TeleportService | Server-only `TeleportAsync`; retry on failure; handle `TeleportInitFailed` |
| `PolicyService:GetPolicyInfoForPlayerAsync` | ≤100 in flight before a response |

Shard queues and sorted maps (`Queue_1v1_0..N`, keyed by `userId % N`) once you have more than a few thousand CCU writing to them.

## Pattern: lobby → MemoryStore queue → reserved match
Flow: player presses Play in the lobby → the lobby server adds `{u = userId, s = jobId, t = os.time()}` to a queue → **one elected matchmaker** (a lock in a hash map) reads N entries → reserves a server → writes the assignment to a hash map per userId → publishes `MatchFound` via MessagingService → each lobby server teleports its own players. Lobby servers also poll the hash map every 2 s in case the message was dropped.

```lua
--!strict
-- ServerScriptService/Matchmaker.server.lua  (runs in LOBBY place servers)
local MemoryStoreService = game:GetService("MemoryStoreService")
local MessagingService = game:GetService("MessagingService")
local TeleportService = game:GetService("TeleportService")
local HttpService = game:GetService("HttpService")
local Players = game:GetService("Players")

local MATCH_PLACE_ID = 0          -- your match place
local MATCH_SIZE = 4
local QUEUE_TTL = 120             -- seconds an entry may wait
local ASSIGN_TTL = 60

local queue = MemoryStoreService:GetQueue("MM_Queue_Duo", 20) -- 20 s invisibility while matchmaker works
local assignments = MemoryStoreService:GetHashMap("MM_Assign")
local locks = MemoryStoreService:GetHashMap("MM_Lock")

type Entry = { u: number, s: string, t: number }
type Assignment = { code: string, matchId: string }

local queued: { [number]: boolean } = {}

local function enqueue(player: Player)
	if queued[player.UserId] then return end
	local ok, err = pcall(function()
		queue:AddAsync({ u = player.UserId, s = game.JobId, t = os.time() } :: Entry, QUEUE_TTL)
	end)
	if ok then queued[player.UserId] = true else warn("enqueue", err) end
end

local function teleportAssigned(userId: number, a: Assignment)
	local player = Players:GetPlayerByUserId(userId)
	if not player then return end
	queued[userId] = nil
	local opts = Instance.new("TeleportOptions")
	opts.ReservedServerAccessCode = a.code
	opts:SetTeleportData({ matchId = a.matchId }) -- non-secret only
	for attempt = 1, 3 do
		local ok = pcall(function()
			TeleportService:TeleportAsync(MATCH_PLACE_ID, { player }, opts)
		end)
		if ok then return end
		task.wait(attempt)
	end
end

-- Leader election: whoever holds the lock key runs matchmaking for ~10 s.
local function tryLead(): boolean
	local ok, got = pcall(function()
		return locks:UpdateAsync("leader", function(current: string?)
			if current == nil or current == game.JobId then return game.JobId end
			return nil -- someone else leads; abort update
		end, 10)
	end)
	return ok and got == game.JobId
end

local function runMatchmakerTick()
	local ok, items, readId = pcall(function()
		return queue:ReadAsync(MATCH_SIZE, true, 0) -- all-or-nothing
	end)
	if not ok or not items or #items < MATCH_SIZE then return end
	local entries = items :: { Entry }
	local okR, code = pcall(function()
		return TeleportService:ReserveServerAsync(MATCH_PLACE_ID)
	end)
	if not okR then return end -- items become visible again after invisibility timeout
	local matchId = HttpService:GenerateGUID(false)
	local userIds = {}
	for _, e in entries do
		table.insert(userIds, e.u)
		pcall(function()
			assignments:SetAsync(tostring(e.u), { code = code, matchId = matchId } :: Assignment, ASSIGN_TTL)
		end)
	end
	pcall(function() queue:RemoveAsync(readId) end)
	pcall(function()
		MessagingService:PublishAsync("MM_Found", { ids = userIds }) -- small payload (<1 KB)
	end)
end

-- Receive: check assignments for players on THIS server.
local function checkLocalAssignments()
	for userId in queued do
		local ok, a = pcall(function() return assignments:GetAsync(tostring(userId)) end)
		if ok and a then teleportAssigned(userId, a :: Assignment) end
	end
end

pcall(function()
	MessagingService:SubscribeAsync("MM_Found", function(_msg)
		task.spawn(checkLocalAssignments)
	end)
end)

task.spawn(function()
	while true do
		if tryLead() then runMatchmakerTick() end
		checkLocalAssignments() -- backstop for dropped messages
		task.wait(2)
	end
end)

Players.PlayerRemoving:Connect(function(p) queued[p.UserId] = nil end)

-- Hook enqueue(player) to your Play button RemoteEvent (validate + debounce server-side).
return nil
```
Notes:
- The queue, hash-map and lock calls cost about 3–6 request units per tick per server. At 200 lobby servers polling every 2 s that is about 30k RU/min, which hits the per-partition limit on a single hash-map key. **Scale by:** polling only while `queued` is non-empty (already done in `checkLocalAssignments`), increasing the interval to 3–5 s, and sharding queues by mode or region.
- For skill-based matching, use a **MemoryStoreSortedMap** keyed by `rating_paddedUserId`, read a range around the player, and widen the window over time.
- The match server reads `matchId` from `player:GetJoinData().TeleportData`, then fetches authoritative info from MemoryStore.

## Parties and friends
- To teleport a party together, pass all of them in one `TeleportAsync` call with the same options. The first player in the list is used for matchmaking into public servers.
- "Join friend": `TeleportService:GetPlayerPlaceInstanceAsync(userId)` returns the place and JobId, then teleport with `ServerInstanceId`.
- Private servers (paid VIP servers) are monetisation. See `production/monetization/private-servers.md`. Reserved servers are free and script-created.

## Roblox custom matchmaking (no code)
Creator Hub → Matchmaking lets you reweight scoring signals (latency, friends, language, age group, custom attributes from DataStores) that decide which **public** server a joining player lands in. Use it for language-coherent servers or skill-coherent public lobbies. You can A/B test it with a **matchmaking experiment** ([[AB-Testing]]). Server-side values go in through `MatchmakingService:SetServerAttribute(name, value)`.

## Global state cheat-sheet
| Need | Use |
|---|---|
| "Server X just got a rare drop!" broadcast | MessagingService topic (fan-out; best-effort) |
| Global live leaderboard (top 100, minutes-fresh) | MemoryStoreSortedMap (TTL) plus an hourly OrderedDataStore snapshot |
| All-time leaderboard | OrderedDataStore |
| Cross-server auction/trading house | MemoryStore HashMap with `UpdateAsync` (atomic), with the durable result in DataStores |
| Global event countdown/state | Config value (`ConfigService`) or a DataStore key read on boot plus a MessagingService nudge |
| Server list / browser | MemoryStore SortedMap of `jobId → {players, region}` with a 30 s TTL heartbeat |

## Checklist
- [ ] MaxPlayers chosen per place for the genre; server fill = Roblox optimized
- [ ] All teleports server-side with retry plus a `TeleportInitFailed` handler
- [ ] Access Control for Places set (Secure if progression-gated)
- [ ] MemoryStore keys have short TTLs; queues sharded at scale
- [ ] MessagingService payloads < 1 KB with a polling backstop
- [ ] Load test: 50 bots or several team members joining a lobby; watch the MemoryStore observability dashboard

## Pitfalls
- Big servers at launch make the game look empty and spread players thin.
- Client-side `TeleportService:Teleport` is deprecated and exploitable.
- Trusting `TeleportData`: it can be spoofed by the client.
- Forgetting `RemoveAsync(readId)` lets matched players re-enter the queue after the invisibility timeout.
- Long MemoryStore TTLs (45-day default) fill the memory quota, after which **all writes fail**, breaking every MemoryStore feature at once.
- Reserved servers have no social discovery. Friends can't "join" a match unless you build that flow.

## Related
- [[Operations/_Index]] · [[Live-Ops-Playbook]] · [[Analytics-And-Instrumentation]] · [[AB-Testing]]
- [[Data-Persistence-DataStores-And-ProfileStore]] · [[Discovery-Algorithm]] · [[Launch-Checklist]]

## Sources
- Roblox creator-docs (mirror), commit 9f840b1, 2026-10-02: `reference/engine/classes/MessagingService.yaml` (limits table), `cloud-services/memory-stores/index.md` (quotas, per-partition limits), `MemoryStoreQueue.yaml`, `TeleportService.yaml`, `projects/teleport.md`, `matchmaking/index.md`, `MatchmakingService.yaml`, `Players.yaml` (MaxPlayers). Live: https://create.roblox.com/docs/cloud-services/memory-stores. Checked 2026-10-04.
- Server size / social slots: https://devforum.roblox.com/t/experience-join-improvements-server-size-join-queues-and-social-slots-reservations/2294621 (2023; ⚠️ verify current max)
- Reserved slots behaviour: https://devforum.roblox.com/t/customize-reserved-server-slots-is-either-broken-or-named-incorrectly/2654016
