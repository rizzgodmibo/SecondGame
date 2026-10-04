---
tags: [design/idle, design/economy]
status: draft
updated: 2026-10-04
confidence: medium
---
# Idle and Offline Earning

## TL;DR
- Compute offline gains **on the server at profile load**: `elapsed = clamp(os.time() − lastSeen, 0, cap)`, `gain = elapsed × incomePerSec × efficiency`. Never trust a client timestamp. The "change your PC clock" exploit only works if the client supplies the time.
- Defaults:
  - **Cap** 4 h at launch (2–8 h range), raisable via upgrades or a gamepass to 12–24 h.
  - **Efficiency** 25–50% of online income, so playing always beats leaving.
  - **Minimum elapsed** 60 s before anything is granted.
- Model real-time growth (plants, eggs, buildings) as **timestamps** (`readyAt = plantedAt + duration`), not ticking loops. Offline progress then comes for free and can't drift.
- Make the return a **moment**: a "Welcome back! You earned 1.2M while away" panel with a claim animation. Optional boosts on top (2× claim, cap extension) are monetisation hooks.
- The real exploit risk is **data races**: two servers loading the same profile, or a failed save leaving `lastSeen` stale. Use session locking (ProfileStore) and stamp `lastSeen` on load as well as on save.

## Why offline earning matters
- It creates a **fixed-interval reason to return** ("my cap fills in 4 h"), which supports D1/D7 ([[Retention-Metrics-D1-D7-D30]], [[Daily-Rewards-And-Streaks]]).
- It makes short sessions feel worthwhile for players who can only play 5–10 min.
- Trade-off: it **doesn't** add playtime, a key recommendation signal capped at 60 min per user per game per day ([[Discovery-Algorithm]]). Offline gains must therefore pull players *back into* active play (spend the windfall), not replace it.

## Design parameters
| Parameter | Launch default | Range | Monetisation / upgrade lever |
|---|---|---|---|
| Offline cap | 4 h | 2–8 h base | upgrade tree to 8 h; gamepass to 12–24 h |
| Efficiency vs. online | 35% | 25–50% | upgrades +5% steps; gamepass ×2 |
| Minimum elapsed | 60 s | 30–300 s | — |
| Income basis | income/s **at logout** | or average of last N min | — |
| Claim UI | auto-shown on join | — | "Claim ×2" developer product or a rewarded-ad option ⚠️ verify: availability of rewarded video ads to your game |
| Long absence (> 3 days) | grant cap + a "comeback" gift | — | re-engagement ([[Live-Ops-Playbook]]) |

Worked example: income at logout 2,500/s, away 9 h, cap 4 h, efficiency 35%.
`elapsed = min(32,400, 14,400) = 14,400 s` → `gain = 14,400 × 2,500 × 0.35 = 12.6M`.
At 2,500/s online, that's 84 min of active income, enough for 1–2 upgrades (TTN 1–5 min, see [[Progression-Curves]]), so the player has something to spend on immediately. **Rule: the offline payout at cap should equal 30–90 min of active income.** Above that, active play stops mattering. Below it, nobody notices.

## Server time on Roblox
- `os.time()` on a **server** returns Unix seconds (UTC) from Roblox's server clock. `DateTime.now().UnixTimestamp` is equivalent. Both are fine for minute- and hour-scale logic.
- The DevForum "os.time can be changed by changing the computer's clock" issue applies to **client** scripts only. Keep all reward timing server-side.
- Different servers can disagree by a few seconds, so clamp negative elapsed to 0. ⚠️ verify: there is no published bound on server clock skew; assume ≤ a few seconds.
- For daily resets use UTC day boundaries: `math.floor(os.time() / 86400)`. See [[Daily-Rewards-And-Streaks]].

## Exploits and mitigations
| Exploit | How it works | Mitigation |
|---|---|---|
| Client clock change | client sends its time | server-only `os.time()`; the client never sends timestamps |
| Double-load race | join server B while A still holds data; B reads old `lastSeen` → double offline + online | session-locked profiles (ProfileStore) ([[Data-Persistence-DataStores-And-ProfileStore]]) |
| Failed save | `lastSeen` stays old → inflated payout next time | clamp to cap; write `lastSeen = now` on **load** too (autosaves keep it fresh) |
| Rejoin spam | leave/rejoin every 10 s to farm | minimum elapsed 60 s; payout uses efficiency < 1 |
| Rebirth before claim | reset then claim with the new multiplier | settle offline gains *before* any reset ([[Prestige-And-Rebirth]]) |
| Income stat inflation | buy temporary 10× boost, log out | base offline on **permanent** income only; exclude timed boosts |
| Alt-account feeding | many alts idle, trade to main | trade restrictions/cooldowns ([[Economy-Design-Sinks-And-Faucets]]) |

## Code: offline earnings module
```lua
--!strict
-- ServerScriptService/Economy/OfflineEarnings.lua (ModuleScript, server-only)
local OfflineEarnings = {}

export type Config = {
	capSeconds: number, -- e.g. 4 * 3600
	efficiency: number, -- 0..1, e.g. 0.35
	minSeconds: number, -- e.g. 60
}

export type SaveData = {
	lastSeen: number, -- os.time() stamp written on load, autosave and leave
	baseIncomePerSec: number, -- permanent income only (no timed boosts)
	offlineCapBonus: number, -- seconds added by upgrades/passes
	offlineEffBonus: number, -- additive efficiency from upgrades/passes
}

export type Result = { elapsed: number, credited: number, gain: number }

function OfflineEarnings.compute(data: SaveData, cfg: Config, now: number): Result
	local elapsed = math.max(0, now - data.lastSeen)
	if elapsed < cfg.minSeconds then
		return { elapsed = elapsed, credited = 0, gain = 0 }
	end
	local cap = cfg.capSeconds + data.offlineCapBonus
	local credited = math.min(elapsed, cap)
	local eff = math.clamp(cfg.efficiency + data.offlineEffBonus, 0, 1)
	local gain = math.floor(credited * data.baseIncomePerSec * eff)
	return { elapsed = elapsed, credited = credited, gain = gain }
end

-- Call once per session right after the profile is loaded and session-locked.
-- Returns the gain so the caller can add currency and fire the "Welcome back" UI.
function OfflineEarnings.settleOnLoad(data: SaveData, cfg: Config): Result
	local now = os.time()
	local result = OfflineEarnings.compute(data, cfg, now)
	data.lastSeen = now -- stamp immediately so a crash can't re-grant
	return result
end

-- Call on autosave and PlayerRemoving
function OfflineEarnings.touch(data: SaveData)
	data.lastSeen = os.time()
end

return OfflineEarnings
```
Usage: in the profile-loaded handler, `local r = OfflineEarnings.settleOnLoad(profile.Data, CONFIG)`. Then `profile.Data.coins += r.gain` and `WelcomeBackRemote:FireClient(player, r.gain, r.elapsed, r.credited)`. The UI shows "Away 9h · Earned 4h (cap) · Upgrade cap?".

### Timestamp-based growth (Grow a Garden–style)
```lua
--!strict
-- ReplicatedStorage/Shared/GrowTimer.lua (pure; server decides, client previews)
local GrowTimer = {}

export type Plot = { plantedAt: number, growSeconds: number }

function GrowTimer.progress(plot: Plot, now: number): number
	if plot.growSeconds <= 0 then
		return 1
	end
	return math.clamp((now - plot.plantedAt) / plot.growSeconds, 0, 1)
end

function GrowTimer.isReady(plot: Plot, now: number): boolean
	return now >= plot.plantedAt + plot.growSeconds
end

return GrowTimer
```
Growth speed-ups (sprinklers, paid boosts) **subtract from `growSeconds` or move `plantedAt` back** on the server. Don't run per-plant loops.

## Return-incentive design
1. **Visible accumulator**: show "Offline vault: 2h 13m / 4h" in-game, so players learn the cap and plan returns around it.
2. **Cap ≈ natural break length**: 4 h ≈ the gap between school and evening sessions. A 12–24 h cap pass suits once-a-day players.
3. **Spend on return**: tune so the payout buys ≥ 1 meaningful upgrade, which pulls players straight into the core loop ([[Core-Loops]]).
4. **Stack with dailies**: the offline claim, daily reward and streak share one "welcome back" flow. Use one modal, not three ([[Daily-Rewards-And-Streaks]]).
5. **Notify**: send an experience notification when the cap is full (for opted-in users). ⚠️ verify: current Experience Notifications API rules and rate limits ([[Live-Ops-Playbook]]).

## Checklist
- [ ] Offline gains computed server-side at load, with cap, efficiency and minimum elapsed
- [ ] `lastSeen` written on load, autosave and leave; profile session-locked
- [ ] Only permanent income counts; offline gains settle before rebirth
- [ ] Payout at cap ≈ 30–90 min of active income (check in the balance sheet)
- [ ] Welcome-back UI with a claim animation; log `offline_claim` with elapsed and gain ([[Analytics-And-Instrumentation]])
- [ ] Cap-extension upgrade/pass designed ([[Gamepasses-vs-Developer-Products]])

## Pitfalls
- Using `tick()` or client time, which can be manipulated or is timezone-dependent.
- No cap. A player returning after 3 months gets an economy-breaking windfall.
- 100% efficiency, which makes offline better than online (players stop playing, playtime signals drop).
- Popups on join stacking (offline + daily + update news + shop offer). Players bounce in the first 60 s ([[Onboarding-And-First-60-Seconds]]).
- Simulating growth with `while true do wait(1)` per plant. That costs server CPU and pauses when servers shut down.

## Related
- [[Progression-Curves]] · [[Prestige-And-Rebirth]] · [[Economy-Design-Sinks-And-Faucets]] · [[Core-Loops]] · [[Session-Length-And-Pacing]]
- [[Daily-Rewards-And-Streaks]] · [[Retention-Metrics-D1-D7-D30]] · [[Data-Persistence-DataStores-And-ProfileStore]] · [[Anti-Exploit-And-Server-Authority]] · [[Live-Ops-Playbook]] · [[Discovery-Algorithm]]

## Sources
- DevForum, Offline Earnings System: https://devforum.roblox.com/t/offline-earnings-system/1038335
- DevForum, How do "Steal a" games calculate offline cash?: https://devforum.roblox.com/t/how-do-steal-a-games-calculate-offline-cash/3854950
- DevForum, os.time() can be changed by changing computer's date (client-side): https://devforum.roblox.com/t/ostime-can-be-changed-by-changing-computers-date-and-time/1769666
- DevForum, os.time(), tick() or time()?: https://devforum.roblox.com/t/ostime-tick-or-time/1190886
- Roblox Creator Docs, Discovery (playtime capped at 60 min/user/game/day): https://create.roblox.com/docs/discovery (read 2026-10-04)
- Pecorella, Math of Idle Games: https://www.gamedeveloper.com/design/the-math-of-idle-games-part-i
