---
tags: [operations/experimentation]
status: reviewed
updated: 2026-10-04
confidence: high
---
# AB Testing

## TL;DR
- **Use Roblox's native Experiments first** (Creator Hub → Experiments, built on **Configs** / `ConfigService`). Roblox handles randomisation and tracks D1, D7, playtime, ARPU, ARPPU, payer conversion and session time, with confidence intervals, early-harm alerts and sample-ratio-mismatch checks. Runs last 14–60 days, with ≤2 variants plus control.
- Below **~1,000 DAU** experiments rarely reach significance (Roblox's own guidance). Below that, ship the bold change and compare cohorts week over week, or use your own bucketing on a high-traffic, high-variance metric.
- Roll your own (deterministic `UserId` hash) only for things Configs can't express: multi-session persistence, server-level variants, or more than 2 variants.
- Size the test first. For a D1 retention of 10%, detecting a **+1 pp absolute** lift needs about **14.7k new users per arm**; +2 pp needs about **3.8k per arm** (α = 0.05, power 80%).
- Test order, by expected value: **onboarding (first 5 min) > first-purchase offer / starter pack price > core-loop pacing numbers > shop layout > cosmetics**.
- Don't peek and stop. Run whole weeks (at least 14 days on Roblox; weekends behave differently), and change nothing else in the tested area while it runs.

## Native Roblox Experiments (verified 2026-10-02 docs)
**Types:** In-game (varies a Config value) and Matchmaking (varies a matchmaking config; one at a time; 100% rollout recommended; up to 3 variants split equally).

**Setup:** Create a Config key, then Experiments → Create → name, **goal metric**, duration of **14–60 days**, **rollout %**, variants (≤2 + control), optional **targeting** (country, language, new vs returning, source, tenure, payer status, activity, engagement, platform spender), then schedule. Once scheduled, the configuration is locked (you can only reschedule). The Config key is also locked while the experiment runs.

**Metrics tracked:** D1 retention, D7 retention, Playtime*, ARPU*, ARPPU, Payer conversion*, Session time. Results update daily. The starred metrics update **every 5 min during the first 24 h** for early-harm detection.

**Early-harm thresholds** (only evaluated once ≥10,000 players are enrolled across variant and control): Playtime −10%, ARPU −20%, Payer conversion −20%. Alerts arrive by email, the Creator Hub tray and an optional webhook. Use them **only** to stop early, never to ship.

**Significance:** the result counts when the CI of the % change excludes 0. On SRM (sample ratio mismatch), stop and restart.

**Make decision:** promotes the winner into permanent configs automatically.

### Code (ServerScriptService)
```lua
--!strict
-- ServerScriptService/Experiments.server.lua
-- Enrol lazily: GetValue() on a per-player snapshot is what enrols the player.
local ConfigService = game:GetService("ConfigService")
local Players = game:GetService("Players")
local Analytics = require(script.Parent.Analytics) -- see [[Analytics-And-Instrumentation]]

local DEFAULT_STARTER_PRICE = 99

local snapshots: { [Player]: ConfigSnapshot } = {}

local function getSnapshot(player: Player): ConfigSnapshot?
	local snap = snapshots[player]
	if snap then return snap end
	local ok, result = pcall(function()
		return ConfigService:GetConfigForPlayerAsync(player)
	end)
	if ok then
		snapshots[player] = result
		return result
	end
	warn("[Experiments] config load failed", result)
	return nil
end

-- Call ONLY when the player is about to see the offer, so non-viewers aren't enrolled.
local function starterPackPrice(player: Player): number
	local snap = getSnapshot(player)
	local v = snap and snap:GetValue("starterPackPrice")
	local price = if typeof(v) == "number" then v else DEFAULT_STARTER_PRICE
	Analytics.setVariantTag(player, `Exp - starterPackPrice={price}`)
	return price
end

Players.PlayerRemoving:Connect(function(p) snapshots[p] = nil end)

return nil
```
Notes:
- `GetConfigAsync()` (global) does **not** apply experiments or targeting. You must use `GetConfigForPlayerAsync(player)`.
- Targeting attributes are evaluated **per session**. For multi-session flows (an onboarding that spans days), persist the assigned value in the player's DataStore profile the first time.
- Configs: up to 1,000 active, 100 conditions per game, 20 per key; string and JSON values up to 100,000 characters. Publishing takes about 15 s–1 min, or can be spread over 15 min.

## Rolling your own: deterministic bucketing
Use this when you need more than 2 variants, server-level variants, or tests on a game without Configs access. Hash `salt .. userId` so that each experiment gets an independent split, a player always gets the same arm, and nothing needs storing.

```lua
--!strict
-- ReplicatedStorage/Shared/Bucket.lua (ModuleScript) — pure, safe on client and server.
local Bucket = {}

-- FNV-1a 32-bit. 16777619 = 2^24 + 403, split to stay inside double precision.
local function fnv1a(s: string): number
	local h = 2166136261
	for i = 1, #s do
		h = bit32.bxor(h, string.byte(s, i))
		h = (bit32.lshift(h, 24) + h * 403) % 4294967296
	end
	return h
end

-- Returns 0..9999
function Bucket.slot(experiment: string, userId: number): number
	return fnv1a(experiment .. ":" .. tostring(userId)) % 10000
end

-- weights e.g. {control = 50, fast = 25, slow = 25}; rollout 0..100 (% of users in the test)
function Bucket.assign(experiment: string, userId: number, weights: { [string]: number }, rollout: number): string?
	local slot = Bucket.slot(experiment, userId)
	if slot >= rollout * 100 then return nil end -- not enrolled: serve default
	-- second, independent hash so rollout changes don't reshuffle arms
	local s2 = Bucket.slot(experiment .. "#arm", userId)
	local total = 0
	for _, w in weights do total += w end
	local names = {}
	for name in weights do table.insert(names, name) end
	table.sort(names) -- deterministic iteration order
	local cursor = 0
	for _, name in names do
		cursor += weights[name] / total * 10000
		if s2 < cursor then return name end
	end
	return names[#names]
end

return Bucket
```
Server usage: `local arm = Bucket.assign("onb_v3", player.UserId, {control=50, short=50}, 100)`. Then call `Analytics.setVariantTag(player, "Exp - onb_v3=" .. (arm or "none"))` so every funnel, economy and custom event is broken down by arm on CF03. On the dashboard you compare **funnel completion, economy and custom events by CF03**. Retention by arm is **not** available natively for home-grown buckets: log a `ReturnedDay` custom event (value = days since first join) with CF03 = arm, or export via your own backend.

Hygiene:
- Run an **A/A test** once (two identical arms). If it shows a "significant" difference, your pipeline is broken.
- New experiment = new salt. Never reuse a salt across tests.
- Check the observed split each day: expected 50/50 but seeing 47/53 with thousands of users means SRM. Find the bug.

## Sample size math
Two-proportion test, per arm: `n = (z₁₋α/₂ + z₁₋β)² · [p₁(1−p₁) + p₂(1−p₂)] / (p₁ − p₂)²`, with z = 1.96 (α = .05 two-sided) and 0.84 (80% power), so `(z+z)² ≈ 7.85`.

| Baseline | Detect (absolute) | n per arm |
|---|---|---|
| D1 10% | +1 pp (→11%) | ≈14,750 |
| D1 10% | +2 pp | ≈3,840 |
| D1 20% | +2 pp | ≈6,500 |
| Payer conv 2% | +0.5 pp (→2.5%) | ≈13,800 |
| Payer conv 2% | +1 pp | ≈3,800 |
| Tutorial completion 60% | +5 pp | ≈1,470 |

For means (playtime, ARPU): `n ≈ 15.7 · σ² / δ²` per arm. ARPU is heavy-tailed (σ is often 5–20× the mean), so revenue tests need far more users than conversion tests. **Test payer conversion and ARPPU separately.**

Duration rule: `days = n_per_arm × arms / (daily new users × rollout)`, rounded **up to whole weeks**, minimum 14 days on native Experiments.

## What to test first (decision rules)
1. **Onboarding funnel step with the biggest drop** (from the Funnel dashboard). One change per test: remove a step, add an arrow, give an earlier reward. It's high-volume and every new user sees it.
2. **First purchase**: starter pack price (e.g. 49 vs 99 vs 149 R$), timing (after first loop vs at 10 min), contents. Goal: payer conversion; guard metric: D1.
3. **Core pacing numbers**: currency multiplier, early upgrade cost curve, egg/hatch speed. Goal: D1, D7; guard: session time.
4. **Daily reward / streak structure**: goal D7.
5. **Shop UI**: tabs and default tab, highlighted offer. Goal: shop funnel completion.

Don't A/B test: whether to fix bugs, tiny cosmetic copy changes on a <10k DAU game, or anything that splits the social graph (trading rules, server size). For server-level changes, use matchmaking experiments or whole-week before/after comparisons.

## Checklist
- [ ] Hypothesis written: "Changing X will move metric Y by Z because W"
- [ ] Goal metric plus 1–2 guard metrics (D1, payer conversion)
- [ ] MDE / sample size computed; duration in whole weeks
- [ ] Enrol at point of exposure, not on join
- [ ] Variant tagged on CF03
- [ ] No other changes to the tested surface during the run
- [ ] Decision logged in `Projects/<game>/` with the CI, not just the point estimate

## Pitfalls
- Peeking daily and stopping on the first green result multiplies the false-positive rate. Novelty effects swing early results.
- Enrolling everyone on `PlayerAdded` dilutes the effect with players who never see the feature.
- Influencer spikes skew cohorts (different source mix). Check the acquisition source mix is similar across arms.
- Testing price on a trading game creates arbitrage between arms.
- Paid random items: the variant must still respect `ArePaidRandomItemsRestricted` ([[Moderation-And-Policy-Compliance]]).
- Experiments on the same key can't overlap. Two experiments on different keys can interact, so avoid tests on the same surface at once.

## Related
- [[Operations/_Index]] · [[Analytics-And-Instrumentation]] · [[Live-Ops-Playbook]] · [[KPI-Dashboard-Spec]]
- [[Conversion-Funnels]] · [[Retention-Metrics-D1-D7-D30]] · [[Pay-To-Win-Boundaries]] · [[Growth-Metrics-And-Benchmarks]]

## Sources
- Roblox creator-docs (mirror), commit 9f840b1, 2026-10-02: `production/experiments.md`, `production/configs.md`; https://create.roblox.com/docs/production/experiments and https://create.roblox.com/docs/production/configs. Checked 2026-10-04.
- `ConfigService`, `ConfigSnapshot` API YAML (same commit).
- Sample-size formula: standard two-proportion z-test (e.g. Kohavi, Tang & Xu, *Trustworthy Online Controlled Experiments*, 2020, ch. 17).
