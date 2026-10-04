---
tags: [retention/dailies]
status: draft
updated: 2026-10-04
confidence: medium
---
# Daily Rewards and Streaks

## TL;DR
- **The server decides everything.** The day index is `math.floor((os.time() - resetOffset) / 86400)` computed on the server. Store `LastClaimDay` (an integer day index, never a timestamp from the client), `Streak`, `CalendarIndex` and `Freezes` in the player profile. The client only asks "claim" and renders what comes back.
- **Use one global UTC day boundary**, optionally shifted (e.g. reset 00:00 UTC = 8 pm US-East / 5 pm US-West, which is after-school prime time). A single boundary makes the countdown, events and leaderboards line up and cannot be exploited with device clocks.
- **Run a hybrid: a forgiving 7-day calendar that advances one slot per claim no matter the gap, plus a separate streak counter that multiplies or unlocks bonuses.** Calendars protect casual and young players. Streaks build habit in engaged players.
- **Never make one miss fatal.** Give 1 streak freeze per completed 7-day cycle (cap 2), consumed automatically. With no freezes left, apply a *soft reset* (halve the streak) instead of dropping to 0. Hard resets churn your best players.
- **Size rewards at roughly 10–25% of a typical session's earnings, with day 7 worth 3–5× day 1.** The reward should pull players back into the core loop, not replace it. (Vault heuristic, not a platform number.)
- **Show the claim popup only after onboarding is complete** (never in a new player's first 60 s, see [[Onboarding-And-First-60-Seconds]]). Pair it with a "come back in HH:MM" countdown and an opt-in notification prompt ([[Notifications-And-Re-Engagement]]).

## Design options
| Model | How it works | Best for | Risk |
|---|---|---|---|
| **Calendar (login track)** | Slot N on the Nth claim. A missed day pauses the track and never resets it. | Young/casual audiences, simulators | Weak habit pressure |
| **Streak** | Consecutive UTC days. A miss resets. | Competitive, older audiences | Rage-quit after a lost streak |
| **Hybrid (recommended)** | Calendar slot gives the base reward. Streak tiers (3/7/14/30) add multipliers or cosmetics. Freezes + soft reset. | Most games | More UI to explain |
| **Rolling cooldown** | Claim every 20 h, streak breaks after 48 h | Players with irregular schedules | Countdown drifts and is hard to align with events. Pick one model per game. |
| **Playtime gifts** | In-session gifts at e.g. 5/10/15/25/40/60 min | Raising average session time | Players idle AFK. Require an activity check. |

Decision rules:
- Audience mostly under 13 or casual → calendar + playtime gifts, with no hard streak.
- PvP/competitive or 13+ → hybrid with streak tiers and visible "best streak" bragging (badge at 7/30/100).
- If you sell a streak restore (Robux), put it behind free freezes first. It drives negative sentiment if it is the *only* recovery path. ⚠️ verify: current Roblox monetisation/dark-pattern guidance before selling streak repair (see Monetisation notes).
- Daily *quests* (3 tasks/day that run through the core loop) beat pure login rewards for playtime and qualified sessions. Ship both: login reward (D1/D7 lift) + dailies (playtime).

## Data model (profile fields)
```text
Daily = {
  LastClaimDay  : number  -- UTC day index of last claim; -1 = never
  Streak        : number  -- current consecutive-day streak
  BestStreak    : number
  CalendarIndex : number  -- 0..CYCLE-1, next calendar slot to award
  Freezes       : number  -- streak freezes banked (cap MAX_FREEZES)
  TotalClaims   : number
}
```
Add this as a nested table in the profile template so ProfileStore's `Reconcile()` fills it for existing players ([[Data-Persistence-DataStores-And-ProfileStore]]).

## Code

### Pure logic (ReplicatedStorage/Shared/DailyRewardLogic, ModuleScript)
Has no services, so it can be unit-tested in Studio's command bar or TestEZ/Jest-Lua.
```lua
--!strict
-- ReplicatedStorage/Shared/DailyRewardLogic (ModuleScript)
local DailyRewardLogic = {}

export type DailyState = {
	LastClaimDay: number,
	Streak: number,
	BestStreak: number,
	CalendarIndex: number,
	Freezes: number,
	TotalClaims: number,
}

export type Reward = { Coins: number, Gems: number }

export type ClaimResult = {
	ok: boolean,
	reason: string?, -- "AlreadyClaimed" | "ClockSkew"
	slot: number, -- calendar slot awarded (1-based for UI)
	streak: number,
	usedFreezes: number,
	streakBroken: boolean,
	reward: Reward?,
}

DailyRewardLogic.SECONDS_PER_DAY = 86400
DailyRewardLogic.RESET_HOUR_UTC = 0 -- shift the day boundary, e.g. 4 = 04:00 UTC
DailyRewardLogic.CYCLE = 7
DailyRewardLogic.MAX_FREEZES = 2
DailyRewardLogic.SOFT_RESET = true -- halve streak instead of zeroing when no freezes

-- 7-slot calendar; day 7 ~4x day 1. Tune against session earnings.
DailyRewardLogic.CALENDAR = {
	{ Coins = 100, Gems = 0 },
	{ Coins = 150, Gems = 0 },
	{ Coins = 200, Gems = 5 },
	{ Coins = 250, Gems = 0 },
	{ Coins = 300, Gems = 10 },
	{ Coins = 350, Gems = 0 },
	{ Coins = 400, Gems = 25 },
} :: { Reward }

function DailyRewardLogic.default(): DailyState
	return {
		LastClaimDay = -1,
		Streak = 0,
		BestStreak = 0,
		CalendarIndex = 0,
		Freezes = 0,
		TotalClaims = 0,
	}
end

function DailyRewardLogic.dayIndex(unixSeconds: number): number
	local offset = DailyRewardLogic.RESET_HOUR_UTC * 3600
	return math.floor((unixSeconds - offset) / DailyRewardLogic.SECONDS_PER_DAY)
end

function DailyRewardLogic.secondsUntilNextDay(unixSeconds: number): number
	local offset = DailyRewardLogic.RESET_HOUR_UTC * 3600
	local nextStart = (DailyRewardLogic.dayIndex(unixSeconds) + 1) * DailyRewardLogic.SECONDS_PER_DAY + offset
	return nextStart - unixSeconds
end

function DailyRewardLogic.canClaim(state: DailyState, today: number): boolean
	return state.LastClaimDay < today
end

-- Streak multiplier tiers: +10% at 3 days, +25% at 7, +50% at 14, +100% at 30.
function DailyRewardLogic.streakMultiplier(streak: number): number
	if streak >= 30 then
		return 2
	elseif streak >= 14 then
		return 1.5
	elseif streak >= 7 then
		return 1.25
	elseif streak >= 3 then
		return 1.1
	end
	return 1
end

-- Mutates `state` in place (call inside your profile's data table). Returns result.
function DailyRewardLogic.claim(state: DailyState, today: number): ClaimResult
	if state.LastClaimDay == today then
		return { ok = false, reason = "AlreadyClaimed", slot = 0, streak = state.Streak, usedFreezes = 0, streakBroken = false }
	end
	if state.LastClaimDay > today then
		-- Server clock went backwards or data came from the future: refuse, do not reset.
		return { ok = false, reason = "ClockSkew", slot = 0, streak = state.Streak, usedFreezes = 0, streakBroken = false }
	end

	local usedFreezes = 0
	local streakBroken = false

	if state.LastClaimDay < 0 then
		state.Streak = 1
	else
		local missed = today - state.LastClaimDay - 1
		if missed <= 0 then
			state.Streak += 1
		elseif missed <= state.Freezes then
			state.Freezes -= missed
			usedFreezes = missed
			state.Streak += 1
		else
			streakBroken = true
			usedFreezes = state.Freezes
			state.Freezes = 0
			if DailyRewardLogic.SOFT_RESET then
				state.Streak = math.max(1, math.floor(state.Streak / 2))
			else
				state.Streak = 1
			end
		end
	end

	local slotIndex = state.CalendarIndex + 1 -- 1-based
	local base = DailyRewardLogic.CALENDAR[slotIndex]
	local mult = DailyRewardLogic.streakMultiplier(state.Streak)
	local reward: Reward = {
		Coins = math.floor(base.Coins * mult),
		Gems = base.Gems,
	}

	state.CalendarIndex = (state.CalendarIndex + 1) % DailyRewardLogic.CYCLE
	if state.CalendarIndex == 0 then
		-- Completed a full cycle: bank a freeze.
		state.Freezes = math.min(DailyRewardLogic.MAX_FREEZES, state.Freezes + 1)
	end
	state.LastClaimDay = today
	state.BestStreak = math.max(state.BestStreak, state.Streak)
	state.TotalClaims += 1

	return {
		ok = true,
		slot = slotIndex,
		streak = state.Streak,
		usedFreezes = usedFreezes,
		streakBroken = streakBroken,
		reward = reward,
	}
end

return DailyRewardLogic
```

### Server (ServerScriptService/DailyRewards.server.luau, Script)
Assumes the project's data layer exposes the loaded ProfileStore profile (see [[Data-Persistence-DataStores-And-ProfileStore]]). The `PlayerData` module interface below (`GetProfile(player)` returning `{Data: {...}}?`) is the vault convention. Adapt the require path to your project.
```lua
--!strict
-- ServerScriptService/DailyRewards (Script)
local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local ServerScriptService = game:GetService("ServerScriptService")

local DailyRewardLogic = require(ReplicatedStorage.Shared.DailyRewardLogic)
-- Expected API: PlayerData.GetProfile(player): { Data: { Daily: DailyState, Coins: number, Gems: number } }?
local PlayerData = require(ServerScriptService.Data.PlayerData) :: any

local remotes = ReplicatedStorage:FindFirstChild("Remotes") or Instance.new("Folder")
remotes.Name = "Remotes"
remotes.Parent = ReplicatedStorage

local claimRemote = Instance.new("RemoteFunction")
claimRemote.Name = "ClaimDaily"
claimRemote.Parent = remotes

local statusRemote = Instance.new("RemoteFunction")
statusRemote.Name = "GetDailyStatus"
statusRemote.Parent = remotes

local lastCall: { [Player]: number } = {}
local COOLDOWN = 1.0 -- seconds between remote calls per player

local function throttled(player: Player): boolean
	local now = os.clock()
	local last = lastCall[player]
	if last and now - last < COOLDOWN then
		return true
	end
	lastCall[player] = now
	return false
end

local function getDaily(player: Player): (any?, DailyRewardLogic.DailyState?)
	local profile = PlayerData.GetProfile(player)
	if not profile then
		return nil, nil -- data not loaded yet: never grant
	end
	if typeof(profile.Data.Daily) ~= "table" then
		profile.Data.Daily = DailyRewardLogic.default()
	end
	return profile, profile.Data.Daily :: DailyRewardLogic.DailyState
end

statusRemote.OnServerInvoke = function(player: Player)
	local _, daily = getDaily(player)
	if not daily then
		return nil
	end
	local now = os.time()
	local today = DailyRewardLogic.dayIndex(now)
	return {
		canClaim = DailyRewardLogic.canClaim(daily, today),
		secondsUntilReset = DailyRewardLogic.secondsUntilNextDay(now),
		streak = daily.Streak,
		nextSlot = daily.CalendarIndex + 1,
		freezes = daily.Freezes,
		-- Would the streak break if claimed now? Lets UI warn/celebrate.
		atRisk = daily.LastClaimDay >= 0 and (today - daily.LastClaimDay - 1) > daily.Freezes,
	}
end

claimRemote.OnServerInvoke = function(player: Player)
	if throttled(player) then
		return { ok = false, reason = "Throttled" }
	end
	local profile, daily = getDaily(player)
	if not profile or not daily then
		return { ok = false, reason = "DataNotLoaded" }
	end

	local today = DailyRewardLogic.dayIndex(os.time())
	local result = DailyRewardLogic.claim(daily, today)
	if result.ok and result.reward then
		-- Mutating profile.Data is enough: ProfileStore autosaves and saves on session end.
		profile.Data.Coins += result.reward.Coins
		profile.Data.Gems += result.reward.Gems
	end
	return result
end

Players.PlayerRemoving:Connect(function(player)
	lastCall[player] = nil
end)
```

### Client (StarterPlayerScripts/DailyRewardClient.client.luau, LocalScript)
```lua
--!strict
-- StarterPlayer/StarterPlayerScripts/DailyRewardClient (LocalScript)
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local remotes = ReplicatedStorage:WaitForChild("Remotes")
local statusRemote = remotes:WaitForChild("GetDailyStatus") :: RemoteFunction
local claimRemote = remotes:WaitForChild("ClaimDaily") :: RemoteFunction

local function refresh()
	local ok, status = pcall(statusRemote.InvokeServer, statusRemote)
	if not ok or status == nil then
		return
	end
	-- Render: status.canClaim, status.streak, status.nextSlot, status.secondsUntilReset, status.atRisk
	print("Daily status", status)
end

local function onClaimButton()
	local ok, result = pcall(claimRemote.InvokeServer, claimRemote)
	if ok and result and result.ok then
		print(("Claimed slot %d, streak %d"):format(result.slot, result.streak))
	end
	refresh()
end

refresh()
-- Hook to your UI, e.g.:
-- (playerGui.DailyGui.ClaimButton :: TextButton).Activated:Connect(onClaimButton)
local _ = onClaimButton
```

## UX rules
- Show all 7 slots, the current one highlighted, and the day-7 jackpot visible from day 1 (goal gradient).
- After a lost streak, show "Streak saved by freeze" or "Streak halved, back to X" as a positive message. Never show only a red "Streak lost".
- Show a countdown to the next reset in the UI and offer the notification opt-in prompt right after a claim. That is a context that warrants a future notification ([[Notifications-And-Re-Engagement]]).
- Playtime gifts need an AFK check (input in the last 2–5 min or a core-loop action) or they become AFK-farm rewards.
- Grant badges at 7/30/100-day streaks (BadgeService). Badges show on profiles and work as social proof.

## Checklist
- [ ] Day index computed only on server with `os.time()`. Reset hour constant documented.
- [ ] `Daily` table in profile template and reconciled for existing players
- [ ] Claim remote rate-limited and refuses when data isn't loaded
- [ ] Clock-skew guard (`LastClaimDay > today` → refuse, don't reset)
- [ ] Freezes + soft reset implemented. Copy reviewed for positive framing.
- [ ] Popup suppressed until onboarding complete
- [ ] Analytics: log claim slot/streak via `AnalyticsService:LogCustomEvent` and compare D1/D7 for claimers vs non-claimers ([[Analytics-And-Instrumentation]])

## Pitfalls
- Using `tick()` or a client-sent timestamp. `tick()` depends on the server's local timezone, and client time is trivially spoofed. Use `os.time()` (UTC epoch seconds) or `DateTime.now().UnixTimestamp`.
- Storing `LastClaimTime` and comparing `now - last >= 86400`. This forces a rolling window that drifts later every day. Store the **day index**.
- Granting before the profile loads, or granting on the client and "syncing". That is a duplication exploit.
- Rewards so large that players log in, claim and leave. D1 rises while playtime per user falls, and discovery weighs both.
- Changing `RESET_HOUR_UTC` after launch shifts everyone's day index. Migrate by recomputing `LastClaimDay` or give a grace day.
- Hard-reset 100-day streaks. Your most loyal players churn the moment they lose one.

## Related
- [[Retention/_Index]] · [[Retention-Metrics-D1-D7-D30]] · [[Data-Persistence-DataStores-And-ProfileStore]] · [[Core-Loops]] · [[Onboarding-And-First-60-Seconds]] · [[Events-And-Seasons]] · [[Notifications-And-Re-Engagement]] · [[Analytics-And-Instrumentation]]

## Sources
- Roblox `os` library docs: `os.time()` returns seconds since the Unix epoch in UTC, read from the device's local clock. It is trustworthy on Roblox servers and spoofable on clients. https://create.roblox.com/docs/reference/engine/libraries/os (accessed 2026-10-04)
- Roblox Creator Docs, "Retention" (D7 levers: progression, goals), https://create.roblox.com/docs/production/analytics/retention (accessed 2026-10-04)
- Roblox Creator Docs, AnalyticsService reference, https://create.roblox.com/docs/reference/engine/classes/AnalyticsService (accessed 2026-10-04)
- ProfileStore (loleris), https://github.com/MadStudioRoblox/ProfileStore. ⚠️ verify: method names (`StartSessionAsync`, `Reconcile`, `EndSession`) against the current release
