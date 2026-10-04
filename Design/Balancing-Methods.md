---
tags: [design/balancing]
status: draft
updated: 2026-10-04
confidence: medium
---
# Balancing Methods

## TL;DR
- Balance against **time-to-X targets**, not prices: write down when the median player should hit each milestone (first upgrade, zone 2, first rebirth, max level), then solve for the numbers.
- Run a **simulation** before shipping: a spreadsheet for the first hour, and a scripted greedy-buyer sim (code below) for long-tail pacing. Re-run it on every number change.
- Keep a **power budget**: total player power at each stage = Σ sources (levels, gear, pets, passes, boosts). Paid power ≤ ~1 zone ahead of free power at equal playtime.
- After launch, tune with **telemetry + A/B tests**: Roblox Experiments for causal tests, Configs for live value changes without a server restart. Change one variable per test.
- Tuning order: **onboarding funnel → D1 → session length → D7 → monetisation**. Never tune monetisation on a leaky funnel.

## 1. Time-to-X targets (write these first)
| Milestone | Simulator target (median) | Tycoon | Obby | TD / RPG |
|---|---|---|---|---|
| First reward | ≤ 15 s | ≤ 15 s | stage 1 cleared ≤ 20 s | first kill/wave ≤ 30 s |
| First purchase/upgrade | ≤ 60 s | ≤ 60 s | — | ≤ 3 min (post-match) |
| First "big moment" (zone, egg tier, floor) | 3–5 min | 5 min | stage 10 ≤ 5 min | first unlock ≤ 10 min |
| Session-1 goal reached | 15–25 min | 20–30 min | stage 30–50 | 2–3 matches |
| First rebirth / prestige | 30–60 min | 45–90 min | — | — |
| "Endgame" visible | day 3–7 | day 2–4 | — | week 2+ |
| Max level / completion | weeks (raised each update) | 3–10 h | hours | months |

These are vault heuristics consistent with [[Progression-Curves]] and [[Session-Length-And-Pacing]]. ⚠️ verify against your genre's top games by timing them yourself (play a fresh account and log the timestamps).

## 2. Spreadsheet simulation (first hour)
One row per purchase event, with these columns:
`t (s) | income/s | wallet | next item | cost | TTN = (cost − wallet)/income | t_after = t + TTN | new income/s`

Procedure:
1. Seed with starting currency (Roblox docs suggest A/B-testing starter amounts) and base income.
2. Greedy rule: buy the item with the best `Δincome / cost` (or the designer-intended path).
3. Read off when each milestone happens and compare with the targets above.
4. Adjust **base costs** first (shifts timing), then **growth rates** (shapes pacing), then **multiplier sources** (structure).

## 3. Scripted sim (long tail, many upgrade lines)
Run it in a Studio test script or with Lune ([[Analytics-And-Instrumentation]] for tooling). The output is milestone times for a greedy median player.
```lua
--!strict
-- ServerScriptService/Dev/EconomySim.server.lua (Studio-only; disable in production)
type Upgrade = { name: string, base: number, r: number, incomeAdd: number, owned: number }

local upgrades: { Upgrade } = {
	{ name = "Shovel", base = 10, r = 1.15, incomeAdd = 1, owned = 0 },
	{ name = "Worker", base = 120, r = 1.14, incomeAdd = 8, owned = 0 },
	{ name = "Drill", base = 1_500, r = 1.13, incomeAdd = 60, owned = 0 },
	{ name = "Factory", base = 20_000, r = 1.12, incomeAdd = 450, owned = 0 },
}
local milestones: { { label: string, income: number } } = {
	{ label = "income 10/s", income = 10 },
	{ label = "income 100/s", income = 100 },
	{ label = "income 1K/s", income = 1_000 },
	{ label = "income 10K/s", income = 10_000 },
}

local function cost(u: Upgrade): number
	return u.base * u.r ^ u.owned
end

local t, wallet, income = 0, 0, 1 -- base click income 1/s
local nextMilestone = 1
local DT_CAP = 3600 * 48
while t < DT_CAP and nextMilestone <= #milestones do
	-- greedy: best income per coin
	local best: Upgrade? = nil
	local bestScore = -1
	for _, u in upgrades do
		local score = u.incomeAdd / cost(u)
		if score > bestScore then
			best, bestScore = u, score
		end
	end
	assert(best, "no upgrades")
	local c = cost(best)
	local dt = math.max(0, (c - wallet) / income)
	t += dt
	wallet += dt * income - c
	best.owned += 1
	income += best.incomeAdd
	while nextMilestone <= #milestones and income >= milestones[nextMilestone].income do
		print(string.format("%-14s at %6.1f min (TTN last: %.0fs)", milestones[nextMilestone].label, t / 60, dt))
		nextMilestone += 1
	end
end
```
Extend it with rebirth (reset + multiplier), offline gains and egg EV. Run variants for "casual" (40% efficiency, 20-min sessions) and "grinder" (100%, 3-h sessions) players. The gap between them is your whale/no-life spread.

## 4. Power budget
`Power(stage) = base(level) × gear × pets × rebirthMult × passMult × boostMult`

| Source | Share of power at mid-game (guideline) |
|---|---|
| Free progression (levels, gear, pets) | 70–85% |
| Rebirth/prestige | 10–25% (grows late) |
| Paid permanent (e.g. 2× gamepass) | ≤ 2× flat; never stacks multiplicatively with >2 other paid sources |
| Temporary boosts (potions) | short spikes, ≤ 3× |

Decision rules:
- Enemy HP / zone gate / boss requirement = power budget at the *free* median × target TTK or TTN. Paying then means **faster**, not **only way** ([[Gamepasses-vs-Developer-Products]]).
- If a new item exceeds its slot's budget by > 20%, it is power creep. Either nerf it or raise the content bar in the same update ([[Content-Cadence]]).
- In PvP keep paid power ≤ ~10% advantage, or make it cosmetic or sidegrade.

## 5. Playtesting metrics (pre-launch, 5–20 testers)
| Metric | How | Red flag |
|---|---|---|
| Time to first reward / first loop | stopwatch or event log | > 15 s / > 60 s |
| "What are you trying to do?" answer | ask at 2 min and 10 min | wrong or "I don't know" |
| Deaths/fails per stage | event log | spike > 2× neighbours |
| Points of confusion | think-aloud, screen record | same spot for ≥ 3 testers |
| Would play again tomorrow (1–5) | post-session survey | median < 4 |
| Mobile usability | test on a phone | buttons < 44 px, text unreadable ⚠️ verify: Roblox mobile UI guidance |

## 6. Telemetry-driven tuning (post-launch)
1. **Instrument**: onboarding funnel (`LogOnboardingFunnelStepEvent`), progression funnels (`LogFunnelStepEvent`), economy events (source/sink with amounts), custom events. Events are server-only and published-game only ([[Analytics-And-Instrumentation]]).
2. **Read the leak**: find the funnel step with the biggest drop relative to the previous step.
3. **Hypothesis → Experiment**: A/B one change (shorter dialogue vs. arrow, 5 s vs. 10 s hint, 100 vs. 250 starting coins).
4. **Ship the winner via Configs**. Log the change in the project decisions file.
5. **Re-check the recommendation signals** a week later: first-play bounce, playtime, play days ([[Discovery-Algorithm]], [[Retention-Metrics-D1-D7-D30]]).

Sample sizes: to detect a 2-percentage-point change in a ~30% completion rate at 95% confidence and 80% power you need roughly 8,000 players per arm. Use `n ≈ 16·p(1−p)/Δ²` per arm → 16·0.3·0.7/0.02² = 8,400. Below ~1,000 DAU, test only big changes (Δ ≥ 5–10 pts).

## Checklist
- [ ] Time-to-X target table filled in the GDD before any numbers are set
- [ ] First-hour spreadsheet and greedy sim agree within ±20%
- [ ] Power budget table per zone; paid power checked against it
- [ ] Playtest with ≥ 5 fresh players (≥ 2 on mobile) before launch
- [ ] Funnels + economy events live at launch; tunables exposed as Configs
- [ ] A/B test log: hypothesis, metric, result, decision

## Pitfalls
- Balancing from a developer account with god-mode knowledge. Always test on a fresh account.
- Tuning to the top 1% (Discord regulars) instead of the median.
- Changing five values at once, so you can't tell which one moved D1.
- Nerfing paid items after sale, which burns trust and invites refund demands. Buff the alternatives instead.
- Ignoring seasonality: Saturdays peak, and school holidays shift baselines ([[Discovery-Algorithm]]). Compare same-weekday cohorts.

## Related
- [[Progression-Curves]] · [[Economy-Design-Sinks-And-Faucets]] · [[Prestige-And-Rebirth]] · [[Difficulty-And-Mastery]] · [[Onboarding-And-First-60-Seconds]] · [[Session-Length-And-Pacing]]
- [[Analytics-And-Instrumentation]] · [[Retention-Metrics-D1-D7-D30]] · [[Discovery-Algorithm]] · [[Gamepasses-vs-Developer-Products]] · [[Live-Ops-Playbook]]

## Sources
- Roblox Creator Docs, Funnel events (server-only, published only, up to 10 funnels): https://create.roblox.com/docs/production/analytics/funnel-events (read 2026-10-04)
- Roblox Creator Docs, Onboarding / Onboarding techniques (Experiments and Configs for FTUE tuning): https://create.roblox.com/docs/production/game-design/onboarding (read 2026-10-04)
- Roblox Creator Docs, Discovery (seasonality: weekly peak Saturday): https://create.roblox.com/docs/discovery (read 2026-10-04)
- Pecorella, Idle game worksheets: https://archive.org/details/idlegameworksheets
- Sample-size rule of thumb n ≈ 16·σ²/Δ² (Lehr's formula), standard A/B testing practice
