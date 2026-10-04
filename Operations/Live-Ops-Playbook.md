---
tags: [operations/live-ops]
status: reviewed
updated: 2026-10-04
confidence: medium
---
# Live Ops Playbook

## TL;DR
- **Ship on a fixed weekly rhythm** at a fixed, publicly announced time. The default is **Saturday 10:00 ET (14:00/15:00 UTC)**, which is what Grow a Garden used at 20M+ CCU. A countdown in game and on the Discord/game page turns the update into an event. A minor update or event every week, a major one every 2–4 weeks ([[Content-Cadence]]).
- **Deploy dark, release with a Config flip.** Publish the place early with new content behind a `ConfigService` key, then switch it on at the announced minute (about 15–60 s to propagate). This avoids restarting servers and lets you roll back without republishing.
- Use **Server Management → Restart Servers** with **"Restart only servers with outdated versions"** and **"Delay server restart" (1–60 min)**. Roblox teleports each old server's players together into a new-version server. Listen to `game.ServerRestartScheduled` to show a countdown and save data.
- A **version string** on every server (`workspace:SetAttribute("BuildVersion")`) plus `game.PlaceVersion` in analytics and error logs lets you link any regression to a build.
- Hotfix path: kill-switch Config first (seconds), then fix → test in staging place → publish → restart outdated servers. Target **< 30 min** from detection to mitigation.
- Admin commands are server-validated with a UserId allow-list or group rank. **Never** trust the client, and log every admin action to a DataStore audit trail.

## Weekly rhythm (solo / small team)
| Day | Work |
|---|---|
| Sat (update day) | 1 h before: "admin abuse" / live event to pack servers. T-0: flip config, announce. T+15 min: watch the error report, crash rate and CCU. T+2 h: hotfix window. |
| Sun | Read D0 data: funnel changes, economy of the new item, Discord feedback. Write a 5-line retro. |
| Mon | Decide next week's content (from the backlog and the data). Prepare the thumbnail/icon refresh ([[Discovery-Algorithm]]). |
| Tue–Wed | Build. |
| Thu | Feature freeze. Publish to the **staging place** (a separate private universe), QA on mobile plus a low-end device. Push the thumbnail/teaser. |
| Fri | Publish to production **dark** (behind configs). Restart outdated servers off-peak (morning UTC) with a 10–15 min delay. Draft the patch notes. |

Why Saturday: under-16 players peak on weekend daytime in the US and EU. ⚠️ verify against your own CCU-by-hour chart after 2 weeks and move the slot to just before your weekly peak. Friday 4–6 pm ET is the common alternative.

Cadence benchmarks (public examples, not guarantees): Grow a Garden shipped weekly Saturday updates at 10:00 ET, preceded by an approximately 1 h "admin abuse" event (fan sites, 2025–26). Blox Fruits ships big numbered updates months apart, with smaller patches in between. See [[Post-Mortems-Real-Games]].

## Versioning
- Semantic-ish: `MAJOR.MINOR.PATCH`. MAJOR = data schema change (needs migration), MINOR = weekly content, PATCH = hotfix.
- Store `BuildVersion` in a ModuleScript constant. On server start: `workspace:SetAttribute("BuildVersion", Build.Version)`. Send it as a custom field on error and analytics events, and show it in a tiny corner label (players screenshot it in bug reports).
- `game.PlaceVersion` (the integer Roblox assigns on publish) goes in logs as well. Analytics filters support place version for alerts.
- Player data carries a `schemaVersion`. Migrations run on load and only forward ([[Data-Persistence-DataStores-And-ProfileStore]]).

## Release mechanics
### Configs as feature flags (preferred)
```lua
--!strict
-- ServerScriptService/Flags.lua (ModuleScript)
-- Wraps ConfigService with code defaults so a config outage never breaks the game.
local ConfigService = game:GetService("ConfigService")

local Flags = {}

local DEFAULTS: { [string]: any } = {
	event_halloween_enabled = false,
	shop_rotation_seed = 1,
	coin_multiplier = 1,
	kill_trading = false, -- emergency kill switch
	maintenance_message = "",
}

local snapshot: ConfigSnapshot? = nil
local listeners: { [string]: { (any) -> () } } = {}

local function load()
	local ok, result = pcall(function() return ConfigService:GetConfigAsync() end)
	if not ok then
		warn("[Flags] using defaults:", result)
		return
	end
	snapshot = result
	result.UpdateAvailable:Connect(function()
		result:Refresh()
	end)
	for key in DEFAULTS do
		result:GetValueChangedSignal(key):Connect(function(v)
			for _, fn in listeners[key] or {} do task.spawn(fn, v) end
		end)
	end
end

function Flags.get(key: string): any
	local d = DEFAULTS[key]
	assert(d ~= nil, "unknown flag " .. key)
	local snap = snapshot
	if snap then
		local v = snap:GetValue(key)
		if v ~= nil and typeof(v) == typeof(d) then return v end
	end
	return d
end

function Flags.onChanged(key: string, fn: (any) -> ())
	listeners[key] = listeners[key] or {}
	table.insert(listeners[key], fn)
end

task.spawn(load)
return Flags
```
For mid-match stability (competitive modes), don't auto-refresh. Call `snapshot:Refresh()` between rounds. Test values on one live server with `ConfigService:SetTestingValue(key, v)` from the Developer Console; this affects that server only.

### Fallback: DataStore + MessagingService flags
If Configs are unavailable (e.g. you need flags that game logic writes), keep a `LiveConfig` DataStore key (versioned, so rollback is free). On change, publish `MessagingService:PublishAsync("LiveConfig", version)` and have servers re-read. Poll every 60 s as a backstop (messages can be dropped). MessagingService limits: 1 KB per message, 600 + 240 × players sends/min per server.

### Restarting servers
Creator Hub → game → Configure → Server Management → select places → Restart Servers.
- ✅ **Restart only servers with outdated versions** (always, unless your flow is version-independent)
- ✅ **Delay server restart** of 1–60 min ("bleed-off"). Use 5–10 min for content updates and 0 for critical exploit or data-corruption fixes.
- Roblox stops matchmaking into old servers, waits, then teleports each old server's players **together** to a new-version server.
- To keep players out entirely (maintenance), make the game **private**. A restart alone lets them back in.
- Open Cloud has a restart endpoint (`Cloud_RestartUniverseServers`) for CI-driven releases.

```lua
--!strict
-- ServerScriptService/RestartNotice.server.lua
-- Shows a countdown and flushes saves when Roblox schedules a restart (developer update or maintenance).
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Players = game:GetService("Players")

local notice = Instance.new("RemoteEvent")
notice.Name = "ServerRestartNotice"
notice.Parent = ReplicatedStorage

game.ServerRestartScheduled:Connect(function(restartTime: DateTime, source: Enum.CloseReason, attributes: { [string]: any }?)
	local secondsLeft = math.max(0, restartTime.UnixTimestamp - DateTime.now().UnixTimestamp)
	local reason = if source == Enum.CloseReason.DeveloperUpdate then "update" else "maintenance"
	notice:FireAllClients(secondsLeft, reason)
	-- Save early instead of only in BindToClose (30 s budget): stagger saves to respect DataStore limits.
	for i, player in Players:GetPlayers() do
		task.delay(i * 0.2, function()
			-- PlayerData.save(player) -- your profile/session module
		end)
	end
end)
```
The event's parameters (`restartTime: DateTime`, `source: CloseReason`, `attributes: Dictionary`) were checked against DataModel.yaml on 2026-10-02.

### Old-style "soft shutdown"
Before the built-in delayed restart, devs teleported everyone to a reserved server and back in `BindToClose`. **Don't build this any more.** The built-in restart does the same job, and `BindToClose` has about 30 s before the server is forced down.

## Hotfix process
1. **Detect**: alert (crash rate > 5% for 5 min, DataStore errors), an error-report spike, or a Discord report flood.
2. **Mitigate (≤ 5 min)**: flip the kill-switch config (`kill_trading = true`, disable the event, set `maintenance_message`). If it's an economy exploit, also pause the affected remote server-side.
3. **Communicate (≤ 15 min)**: Discord announcement and an in-game banner from `maintenance_message`. Be honest ("trading paused while we fix a dupe").
4. **Fix**: branch from the live tag → fix → publish to the **staging place** → smoke test (join, load data, buy, save, rejoin).
5. **Ship**: publish to prod → Restart outdated servers (delay 0–2 min for exploits).
6. **Clean up**: data repair if needed ([[Bad-Launch-Response]]), compensation, a post-mortem note in `Projects/<game>/`.

## Environments
- **Staging universe**: a separate, private game with the same places. Publish there first. Configs can be pushed between experiences with Studio → File → Open Configs → **Publish As**.
- Use separate DataStore names by environment (`PlayerData_v3` vs `PlayerData_v3_STAGING`) or rely on the separate universe, which isolates DataStores automatically.
- Use Rojo plus git for code (tag every production publish with `vMAJOR.MINOR.PATCH`).

## Admin commands (TextChatService)
```lua
--!strict
-- ServerScriptService/AdminCommands.server.lua
-- Requires a TextChatCommand named "AdminCmd" (PrimaryAlias "/admin") under TextChatService.
local TextChatService = game:GetService("TextChatService")
local Players = game:GetService("Players")
local DataStoreService = game:GetService("DataStoreService")

local GROUP_ID = 0           -- your group
local MIN_RANK = 250         -- admin rank in group
local ALLOW: { [number]: true } = { [1] = true } -- explicit UserIds (owner)
local audit = DataStoreService:GetDataStore("AdminAudit_v1")

local function isAdmin(player: Player): boolean
	if ALLOW[player.UserId] then return true end
	if GROUP_ID == 0 then return false end
	local ok, rank = pcall(function() return player:GetRankInGroup(GROUP_ID) end)
	return ok and rank >= MIN_RANK
end

local handlers: { [string]: (Player, { string }) -> string } = {
	announce = function(_, args)
		-- Server-originated text shown to all must still be filtered if it came from a user:
		return "announced: " .. table.concat(args, " ")
	end,
	kick = function(_, args)
		local target = Players:FindFirstChild(args[1] or "")
		if target and target:IsA("Player") then
			target:Kick("Removed by moderator")
			return "kicked " .. target.Name
		end
		return "not found"
	end,
	ban = function(_, args)
		local userId = tonumber(args[1])
		local days = tonumber(args[2]) or 1
		if not userId then return "usage: /admin ban <userId> <days|-1>" end
		local ok, err = pcall(function()
			Players:BanAsync({
				UserIds = { userId },
				Duration = if days < 0 then -1 else math.floor(days * 86400),
				DisplayReason = "You broke the game rules. Appeal in our community server.",
				PrivateReason = "admin cmd: " .. table.concat(args, " ", 3),
				ExcludeAltAccounts = false,
				ApplyToUniverse = true,
			})
		end)
		return if ok then "banned " .. userId else "ban failed: " .. tostring(err)
	end,
}

local cmd = TextChatService:WaitForChild("AdminCmd") :: TextChatCommand
cmd.Triggered:Connect(function(source: TextSource, message: string)
	local player = Players:GetPlayerByUserId(source.UserId)
	if not player or not isAdmin(player) then return end
	local parts = string.split(message, " ")
	table.remove(parts, 1) -- "/admin"
	local name = table.remove(parts, 1) or ""
	local handler = handlers[name]
	if not handler then return end
	local result = handler(player, parts)
	pcall(function()
		audit:SetAsync(`{os.time()}_{player.UserId}`, { cmd = message, result = result })
	end)
	print("[Admin]", player.Name, message, "->", result)
end)
```
Note: `TextChatCommand.Triggered` also fires for non-admins, so the `isAdmin` check is the security boundary. Keep the command list short (kick, ban, announce, give-for-compensation, toggle-event). "Admin abuse" events should be **scripted server-side events** you trigger, not free-form give commands.

## Checklist
- [ ] Fixed public update day/time; countdown UI in game
- [ ] Staging universe exists; publish there first
- [ ] All new content behind Config flags; kill switches for trading, events, shop
- [ ] `BuildVersion` attribute plus logged `PlaceVersion`
- [ ] `ServerRestartScheduled` handler (countdown plus early save)
- [ ] Restart outdated servers with a 5–10 min delay
- [ ] Alerts configured (crash rate, DataStore errors) with a Discord webhook
- [ ] Admin commands: allow-list, audit log, no client authority

## Pitfalls
- Restarting **all** servers (not only outdated ones) disconnects players needlessly.
- A Config value of the wrong type makes `GetValue` return something your code doesn't expect. Validate it against the default type, as above.
- Flags that are never cleaned up turn into permanent branches. Delete them 2 weeks after full rollout.
- Publishing a schema migration while old servers still run means old servers can overwrite new-format data. Restart outdated servers immediately, and make the loader refuse to save data with a **newer** `schemaVersion` than it understands.
- Updates that land outside the announced slot get less of a spike, because the announcement is what concentrates players into the window.

## Related
- [[Operations/_Index]] · [[Bad-Launch-Response]] · [[AB-Testing]] · [[KPI-Dashboard-Spec]] · [[Server-Scaling-And-Matchmaking]]
- [[Content-Cadence]] · [[Launch-Checklist]] · [[Data-Persistence-DataStores-And-ProfileStore]] · [[Moderation-And-Policy-Compliance]]

## Sources
- Roblox creator-docs (mirror), commit 9f840b1, 2026-10-02: `projects/update-games.md` (Restart Servers, `ServerRestartScheduled`), `production/configs.md`, `chat/examples/custom-text-chat-commands.md`, `production/analytics/alerts.md`, `reference/engine/classes/MessagingService.yaml`, `Players.yaml` (BanAsync). Live: https://create.roblox.com/docs/projects/update-games. Checked 2026-10-04.
- Grow a Garden Saturday 10:00 ET schedule: https://www.pcgamesn.com/grow-a-garden/update-schedule ; https://mygagcalculator.com/grow-a-garden-saturday-admin-abuse/ (fan site; ⚠️ verify)
