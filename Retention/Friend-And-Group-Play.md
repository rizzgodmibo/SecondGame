---
tags: [retention/social]
status: draft
updated: 2026-10-04
confidence: medium
---
# Friend and Group Play

## TL;DR
- **Co-play is a ranking signal.** Roblox's Home recommender uses "intentional co-play days per user": unique days users come back to play *with friends* via join, invite or private server ([[Discovery-Algorithm]]). Players with friends in-session also retain better. Design at least one reason to play together in every core loop ([[Core-Loops]]).
- **Friend boost:** +10% earnings per friend in the server, capped at +30–50%, shown on the HUD. Check friendship server-side with `Player:IsFriendsWithAsync(userId)` (cached) and recompute on join/leave.
- **Group (Community) rewards:** check with `Player:IsInGroupAsync(groupId)`. `IsInGroup` is **deprecated**. Prompt joining in-game with `GroupService:PromptJoinAsync(groupId)` (client). The server's membership cache does **not** refresh after an in-game join, so re-check on rejoin or verify via the client result with a server-side cap.
- **Roblox Parties:** `Player.PartyId` + `SocialService:GetPlayersByPartyId(partyId)` / `GetPartyAsync(partyId)`. Keep party members on the same team and teleport them together via a reserved server (`TeleportService:ReserveServerAsync` + `TeleportOptions.ReservedServerAccessCode`).
- **Private servers:** enable them (free or a monthly Robux price). Give owners perks (server-wide settings, `/kick` in *their* server only) via `game.PrivateServerOwnerId`. Changing the price **cancels all active subscriptions**. Pick it once.
- **Invites:** `SocialService:PromptGameInvite` + referral rewards. See [[Sharing-And-Referral-Loops]].

## Mechanics menu (pick 2–3 for launch)
| Mechanic | Retention effect | Implementation |
|---|---|---|
| Friend boost (% per friend in server) | Pulls friends into the same server, raises co-play days | Server multiplier, code below |
| Co-op objectives (boss needs 2+ players, team obby buttons) | Session length, invites | Scale HP by players, require 2 pads |
| Trading | D30 and economy depth | Secure two-sided confirm, server-side escrow |
| Gifting (send a pet/item) | Social obligation loop | Server transfer, rate-limited, logged |
| Show-off (plots, displays, emotes, titles) | Status | Plots visible to all, leaderboards |
| Party/squad queue | Keeps groups together across places | Party APIs + reserved servers |
| Guilds/clans | D30+ | Custom data (MemoryStore + DataStore), weekly guild leaderboard |
| Group membership perk | Builds an owned channel (group shouts, events, announcements) | `IsInGroupAsync` |
| Private-server perks | Monetisation + co-play | `PrivateServerOwnerId` |

Decision rules:
- Single-player-feeling genre (tycoon, simulator) → friend boost + gifting + visible plots.
- Session-based (round PvP, horror) → party APIs + squad queue + "play again with same squad".
- Social hangout/RP → private servers (cheap, ~100 R$/month ⚠️ verify typical pricing) + owner tools.

## Code

### Friend boost (ServerScriptService/FriendBoost, Script)
```lua
--!strict
-- ServerScriptService/FriendBoost (Script)
-- Sets player attribute "FriendBoost" (e.g. 1.2 = +20%). Economy code multiplies earnings by it.
local Players = game:GetService("Players")

local PER_FRIEND = 0.10
local MAX_BONUS = 0.30

-- Symmetric pair cache: key "minId:maxId" -> boolean
local friendCache: { [string]: boolean } = {}

local function pairKey(a: number, b: number): string
	return if a < b then `{a}:{b}` else `{b}:{a}`
end

local function areFriends(a: Player, b: Player): boolean
	local key = pairKey(a.UserId, b.UserId)
	local cached = friendCache[key]
	if cached ~= nil then
		return cached
	end
	local ok, result = pcall(function()
		return a:IsFriendsWithAsync(b.UserId)
	end)
	local value = ok and result == true
	if ok then
		friendCache[key] = value
	end
	return value
end

local function recompute(player: Player)
	if not player.Parent then
		return
	end
	local count = 0
	for _, other in Players:GetPlayers() do
		if other ~= player and areFriends(player, other) then
			count += 1
		end
	end
	local bonus = math.min(MAX_BONUS, count * PER_FRIEND)
	player:SetAttribute("FriendBoost", 1 + bonus)
	player:SetAttribute("FriendsInServer", count)
end

local function recomputeAll()
	for _, p in Players:GetPlayers() do
		task.spawn(recompute, p)
	end
end

Players.PlayerAdded:Connect(recomputeAll)
Players.PlayerRemoving:Connect(function(leaving)
	for key in friendCache do
		local a, b = string.match(key, "^(%d+):(%d+)$")
		if tonumber(a) == leaving.UserId or tonumber(b) == leaving.UserId then
			friendCache[key] = nil
		end
	end
	task.defer(recomputeAll)
end)
recomputeAll()
```

### Group membership reward (ServerScriptService/GroupReward, Script) + client prompt
```lua
--!strict
-- ServerScriptService/GroupReward (Script)
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local GROUP_ID = 0 -- your community/group ID

local remotes = ReplicatedStorage:FindFirstChild("Remotes") or Instance.new("Folder")
remotes.Name = "Remotes"
remotes.Parent = ReplicatedStorage
local claimRemote = Instance.new("RemoteFunction")
claimRemote.Name = "ClaimGroupReward"
claimRemote.Parent = remotes

local function isMember(player: Player): boolean
	local ok, inGroup = pcall(function()
		return player:IsInGroupAsync(GROUP_ID)
	end)
	return ok and inGroup == true
end

Players.PlayerAdded:Connect(function(player)
	player:SetAttribute("GroupMember", isMember(player))
end)

-- Called by the client after PromptJoinAsync returns Member. The server cache may still say
-- false until rejoin, so we only grant when the server sees membership. Otherwise tell the
-- client to rejoin (or grant on next join automatically).
claimRemote.OnServerInvoke = function(player: Player)
	if player:GetAttribute("GroupMember") ~= true then
		-- Server-side cache: re-check is cheap but returns cached value for this player/group.
		if not isMember(player) then
			return { ok = false, reason = "RejoinToClaim" }
		end
		player:SetAttribute("GroupMember", true)
	end
	-- Grant once: set profile.Data.GroupRewardClaimed = true in your data layer, give chest / 2x daily, chat tag.
	return { ok = true }
end
```
```lua
--!strict
-- StarterPlayer/StarterPlayerScripts/GroupPrompt (LocalScript)
local GroupService = game:GetService("GroupService")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local GROUP_ID = 0

local function promptJoin()
	local ok, status = pcall(function()
		return GroupService:PromptJoinAsync(GROUP_ID)
	end)
	if ok and status == Enum.GroupMembershipStatus.Member then
		local remote = ReplicatedStorage:WaitForChild("Remotes"):WaitForChild("ClaimGroupReward") :: RemoteFunction
		local result = remote:InvokeServer()
		print("Group reward:", result)
	end
end
-- Wire promptJoin to a "Join group for a free chest" button.
local _ = promptJoin
```
⚠️ verify: whether the server-side `IsInGroupAsync` cache refreshes after a client-side `PromptJoinAsync` join. The docs say only the client cache is cleared, so expect "rejoin to claim" on the server.

### Party teleport (ServerScriptService/PartyTeleport, ModuleScript)
```lua
--!strict
-- ServerScriptService/PartyTeleport (ModuleScript) — require from matchmaking code
local SocialService = game:GetService("SocialService")
local TeleportService = game:GetService("TeleportService")

local MATCH_PLACE_ID = 0 -- your match place

-- Teleport a player's whole in-server party together into a fresh reserved server.
local function teleportParty(leader: Player)
	local members: { Player } = { leader }
	if leader.PartyId ~= "" then
		members = SocialService:GetPlayersByPartyId(leader.PartyId)
	end
	local ok, code = pcall(function()
		return TeleportService:ReserveServerAsync(MATCH_PLACE_ID)
	end)
	if not ok then
		warn("ReserveServerAsync failed:", code)
		return
	end
	local options = Instance.new("TeleportOptions")
	options.ReservedServerAccessCode = code :: string
	local tpOk, err = pcall(function()
		return TeleportService:TeleportAsync(MATCH_PLACE_ID, members, options)
	end)
	if not tpOk then
		warn("TeleportAsync failed:", err)
	end
end

return teleportParty
```
For team games, assign by `PartyId` before filling teams (all members of a party → same team). Test with Studio's **Party Simulator**.

### Private-server owner perks
```lua
--!strict
-- ServerScriptService/PrivateServerPerks (Script)
local Players = game:GetService("Players")

local isPrivate = game.PrivateServerId ~= "" and game.PrivateServerOwnerId ~= 0 -- reserved servers have OwnerId 0
Players.PlayerAdded:Connect(function(player)
	player:SetAttribute("IsServerOwner", isPrivate and player.UserId == game.PrivateServerOwnerId)
end)
-- Gate owner-only commands (/kick, /weather, /reset-map) on the IsServerOwner attribute, server-side.
```

## Social presence
- Roblox shows friends' current game on Home (Friends list) with **Join**. Make sure "joinable" isn't blocked by full servers: set `Players.MaxPlayers` with headroom, or reserve friend slots (Game Settings → Places → server fill "leave slots for friends" ⚠️ verify: current setting name).
- In-game: list online friends (`player:GetFriendsOnlineAsync(200)`, 30 s cache, fields `VisitorId`, `DisplayName`, `PlaceId`, `GameId`, `LocationType`). Highlight friends playing *this* game and offer "Join them" via `TeleportService:TeleportAsync` with `TeleportOptions.ServerInstanceId = GameId`.
- Show friend names over plots/nameplates and a "friends in server" badge to make co-play visible.

## Checklist
- [ ] At least one co-op or social interaction in the core loop
- [ ] Friend boost implemented and visible in HUD
- [ ] Group/community created, linked on game page. Group reward via `IsInGroupAsync`.
- [ ] Private servers enabled (decide price once). Owner perks shipped.
- [ ] Party APIs tested in Party Simulator if the game has teams or matchmaking
- [ ] Analytics: log `FriendsInServer` at session end. Compare retention of players with ≥1 friend vs 0.

## Pitfalls
- Using deprecated `IsInGroup`, `IsFriendsWith`, `GetFriendsOnline` or `ReserveServer` in new code. Use the `…Async` versions.
- Trusting a client "I joined the group" message to grant valuable rewards.
- Friend boosts with no cap. Big friend groups farm 2–3× income.
- Changing private-server price after launch (cancels every subscription).
- Under-13 players may be unable to join private servers due to parental controls. Never gate core content behind them.
- Trading without server-side escrow and logs leads to dupes and scams.

## Related
- [[Retention/_Index]] · [[Sharing-And-Referral-Loops]] · [[Leaderboards]] · [[Discovery-Algorithm]] · [[Core-Loops]] · [[Community-Management]] · [[Data-Persistence-DataStores-And-ProfileStore]] · [[Retention-Metrics-D1-D7-D30]]

## Sources
- Roblox Creator Docs, "Discovery" (intentional co-play days per user), https://create.roblox.com/docs/discovery (accessed 2026-10-04)
- Roblox Engine API: `Player` (`IsInGroupAsync`, `IsInGroup` deprecated, `IsFriendsWithAsync`, `GetFriendsOnlineAsync`, `PartyId`), `GroupService:PromptJoinAsync`, `SocialService` (party APIs), `TeleportService:ReserveServerAsync`, `TeleportOptions`, `DataModel.PrivateServerId/OwnerId` (creator-docs mirror commit 2026-10-02; accessed 2026-10-04)
- Roblox Creator Docs, "Private servers", https://create.roblox.com/docs/production/monetization/private-servers (accessed 2026-10-04)
- DevForum, "Introducing Roblox Communities" (Groups renamed Communities, 2024-11), https://devforum.roblox.com/t/introducing-roblox-communities/3268307
