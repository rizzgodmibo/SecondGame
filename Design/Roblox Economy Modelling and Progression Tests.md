---
title: Roblox Economy Modelling and Progression Tests
date: 2026-10-03
updated: 2026-10-03
verified: 2026-10-03
review_after: 2027-01-01
tags: [roblox, design, economy, progression, balancing]
source: Roblox documentation, mathematical derivation and local source inspection
project: null
status: actionable-model-specification
---
# Roblox Economy Modelling and Progression Tests

Related: [[Paper Plane Toss Progression Numbers]], [[Paper Plane Toss Rebirth]], [[Fish a Monster Saving and Offline Income]], [[Roblox Discovery and Retention Measurement]], [[Roblox Vault Coverage and Maintenance]].

## Use and evidence limits

Use this specification to evaluate an approved economy before changing game code. It defines model inputs, calculations and acceptance evidence; no workbook or game simulation was built in this pass. Arithmetic examples were evaluated directly. Suggested tests and design choices are recommendations, not new approved mechanics.

Roblox recommends tracking earned/purchased resources, spending and usage, estimating reward expected value, and planning sinks before events. [S1] That is useful direction, but source examples also need checking: S1 lists a 10% chance for a 30-unit reward, then later prints 30% alongside a result of 3. The consistent calculation uses 10% and yields total expected reward 14. Do not copy the inconsistent line.

## Model inputs: minimum table specification

| Table | Fields and units | Why it matters |
|---|---|---|
| Assumptions | Value, unit, source/date, confidence, range, approval status | Separates measured behaviour from guesses |
| Actions | Duration seconds, travel/wait seconds, success chance, reward distribution, resource cost | Converts per-action rewards into realistic rates |
| Catalog | Item ID, currency, price, prerequisites, benefit, stack rule, rounding, ownership cap | Prevents accidental double stacking |
| Progression | Cumulative threshold, marginal requirement, resulting unlocks/rate changes | Distinguishes total XP from XP for next level |
| Player scenarios | Starting state, session pattern, purchase strategy, skill, spending entitlement | Avoids modelling everyone as an optimal player |
| Resets and offline | Fields reset/kept, cap, eligible rate snapshot, timestamp rule | Captures state transitions |
| Outputs | Time to milestones, wallet, source/sink totals, stalls, loop count, content exhaustion | Connects numbers to player experience |

Keep different currencies separate. State whether time means active play, session time or elapsed calendar time. Include travel, menus, loading and failure instead of assuming uninterrupted productive clicks. Copy rounding order from the authoritative implementation.

## Calculation rules (derived)

**Wallet conservation:** end balance = start balance + all sources − all sinks. Record refunds, compensation and resets explicitly. A balance clamp must not hide an accounting error.

**Fixed-rate time to affordability:** max(0, price − current balance) / (source rate − unavoidable spend rate), when net rate is positive and constant. With balance 80, price 500, source 30/min and mandatory spend 5/min, time is 16.8 minutes. A zero or negative net rate with an unmet goal means unreachable under those assumptions, not zero minutes. Optional upgrades change the path; simulate their purchase decisions.

**Geometric progression:** if the first level-up costs a and marginal cost grows by g, cumulative XP to reach level L from level 1 is a × (g^(L−1) − 1)/(g−1), for g ≠ 1. At g=1 use a×(L−1). Marginal XP from L to L+1 is a×g^(L−1). For a=10, g=1.25, total to level 6 is 82.0703125; level 6→7 alone costs 30.517578125. They are different quantities.

**Random reward:** expected reward per attempt = sum(probability × reward). Convert to a rate using the full cycle time. Expected value alone hides unlucky players. For independent fixed-probability attempts with success p, probability of at least one success in n attempts is 1−(1−p)^n. With p=1%, reaching at least 90% success probability requires 230 attempts, while mean waiting time is 100. Pity, changing odds and dependent rolls invalidate that simple formula.

**Upgrade payback:** cost / incremental net earning rate is a first screen for a constant-rate upgrade; it is not a complete purchase policy when unlocks, thresholds or alternative purchases intervene.

## Simulate state changes rather than one permanent multiplier

Track time, balance, XP/level, inventory, boosts, cooldowns and unlocked actions. Advance through actions; apply rewards and exact rounding; update level/unlocks; then apply the player's defined buying/reset decision. Record every milestone and money movement.

Run at least: casual free player, engaged free player, efficient optimiser, returning player near the offline cap, and each relevant paid entitlement combination. These are scenario categories, not assertions about real player proportions.

Test multiplier interactions individually and together. Additive bonuses and multiplicative categories are not interchangeable. Include temporary boost expiry and level changes during a session. Record distribution percentiles only when they come from actual sampled trials with stated seeds and sample count.

For rebirth, explicitly list kept/reset state and compare time to regain pre-reset capability, time to the next meaningful unlock, and the alternative of delaying rebirth. A faster second run is a hypothesis to evaluate; endlessly accelerating into content exhaustion is not automatically good pacing.

For offline earning, define the eligible rate and timestamp source. A suggested calculation is eligible seconds = clamp(now − valid lastSeen, 0, cap). Unknown/zero/future timestamps need an explicit policy; the Fish a Monster note records treating them as now. Test whether repeated joins can claim the same interval and whether paid boosts pause or expire. Do not silently import one game's policy into another.

## Balance diagnosis and measurement

Roblox economy events distinguish sources and sinks, report transaction amount and resulting balance, and must be emitted by the server in published games. Sink amounts are positive in the API. The dashboard exposes sources, sinks and wallet balances. [S2]

S2 suggests keeping aggregate sources minus sinks near zero. Treat that as a diagnostic heuristic, not a universal design invariant: players legitimately save for goals and a growing population changes totals. Inspect cohorts, progression tiers, payers/non-payers and time windows before adding sinks. A transfer moves ownership; it is not a net global sink unless a fee destroys currency.

If wallets rise, check for obsolete items, hoarding for an upcoming unlock, exploitable faucets, missing telemetry and stalled content before imposing higher prices. If balances are low, inspect affordability and loop friction rather than assuming engagement is healthy. Match model expectations to observed milestone times and interviews; optimise both comprehensibility and pacing.

## Acceptance checks and experiment record

- Probabilities normalise; units match; all currency movements reconcile.
- Initial, threshold, threshold-minus-one and extreme values behave as intended.
- No affordable upgrade is accidentally counted twice; no unavailable purchase is assumed.
- Free and paid paths retain stated choices and reachable milestones.
- Rebirth preserves exactly approved fields; replay does not duplicate grants.
- Offline cap and missing/future timestamps behave correctly across repeated joins.
- Stalls are surfaced explicitly; numerical overflow/NaN never becomes a valid reward.
- Sensitivity runs vary action time, participation, multipliers and spending choices; report which uncertainty changes the decision most.
- Historical simulation claims include model version, configuration, player policy and timing definition before reuse.

For each balance change save: problem evidence, hypothesis, approved parameter difference, expected milestone movement, affected cohorts, primary metric, guardrails (retention, early exit, fulfilment, complaints), observation window and rollback plan. Do not claim a growth or retention improvement from a spreadsheet alone.

## Local context and remaining work

Paper Plane Toss Levels.luau confirms that glideForLevel returns a cumulative threshold. Boosts.luau adds equipped pet bonuses within one category, then multiplies categories; pets affect Glide directly, not the Tokens multiplier function. Indirect progression effects still matter. No full server award path was audited here.

Next design passes: first-sixty-second onboarding and mastery/pacing; create a reproducible progression simulation only under the normal code-approval process. No genre-wide target session length or pay-to-win policy is invented here.

## Sources

Checked 2026-10-03:
- [S1: Balance virtual economies](https://create.roblox.com/docs/production/game-design/balance-virtual-economies) — principles and example inconsistency described above.
- [S2: Economy events](https://create.roblox.com/docs/production/analytics/economy-events) — telemetry contract and dashboard guidance.
- Local: C:\Users\holde\Downloads\SecondGame\src\shared\Levels.luau and C:\Users\holde\Downloads\SecondGame\src\shared\Boosts.luau, inspected 2026-10-03.
- Related project notes preserve historical decisions; new maths examples above are illustrative, not project tuning.
