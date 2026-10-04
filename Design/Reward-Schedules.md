---
tags: [design/rewards]
status: draft
updated: 2026-10-04
confidence: medium
---
# Reward Schedules

## TL;DR
- Pair a **fixed** schedule, which gives a predictable goal ("10 more kills to level"), with a **variable** schedule layered on top (random drop, hatch, mutation). The fixed part sets direction. The variable part drives activity rate.
- Variable-ratio rewards produce the highest, steadiest activity, and that is why they are the most ethically loaded. Put them on **free** actions (drops, hatches bought with earned currency) by default. Paid random items carry legal disclosure duties.
- **Paid random items on Roblox**:
  - Show every outcome with numerical odds summing to 100% *before* purchase.
  - Explain luck boosts and **pity systems** numerically, with odds updated live.
  - Check `PolicyService:GetPolicyInfoForPlayerAsync().ArePaidRandomItemsRestricted` per player.
- Add pity on any table where the chase item is < 1%. Hard pity at ≈ 1.5–2× the expected number of rolls caps the worst case without changing the median much.
- Never fake a near-miss on a paid roll. The animation must reflect the outcome actually rolled on the server.

## The four schedules (operant conditioning, applied)
| Schedule | Rule | Player behaviour | Roblox examples | Use it for |
|---|---|---|---|---|
| Fixed ratio (FR) | reward every N actions | burst, then pause after the reward | "defeat 20 enemies", XP bar, quest counters | clear goals, onboarding steps |
| Variable ratio (VR) | reward after a random number of actions, mean N | high, steady rate; slow to stop | egg hatches, drops, crits, fishing catches, mutations | the core-loop "juice" |
| Fixed interval (FI) | first action after time T is rewarded | activity spikes as T approaches ("scalloping") | daily rewards, playtime gifts, timed shop restocks | return visits ([[Daily-Rewards-And-Streaks]]) |
| Variable interval (VI) | first action after a random time is rewarded | moderate, steady checking | random weather/events, server luck boosts, wandering merchants | keeping players in-server, social gathering |

Hopson (Bungie, 2001): "variable ratio schedules produce the highest overall rates of activity of all the schedules", because activity tracks how soon the player *expects* the next reward.

**Compound pattern (recommended default):**
FR progress bar (e.g. 100 coins = 1 egg) + VR result (rarity roll) + FI daily bonus + VI server events. Each covers a different gap: goal, excitement, return and stay.

## Loot table design
1. Define rarity tiers by **tier weight first**, then split items inside each tier. Designers can then add items without changing tier odds.
2. Common tier sizing: Common 60–75%, Uncommon 20–30%, Rare 4–10%, Epic 0.5–2%, Legendary 0.05–0.5%, Secret/Huge ≤ 0.01%. ⚠️ verify: these are vault heuristics; benchmark against odds displayed in top games (Pet Simulator 99, Grow a Garden).
3. A chase item worth chasing for a week needs `p ≈ 1 / (rolls per week of an engaged player)`.

### Roll math
- P(at least one hit in n rolls) = `1 − (1 − p)^n`
- Rolls for a 50% chance = `ln 0.5 / ln(1 − p)`. Rolls for 90% = `ln 0.1 / ln(1 − p)`.
- Expected rolls with hard pity at H = `(1 − (1 − p)^H) / p`

| p | 50% chance after | 90% after | 99% after | Expected rolls with hard pity H = 100 |
|---|---|---|---|---|
| 10% | 7 | 22 | 44 | 10.0 |
| 1% | 69 | 230 | 459 | 63.4 |
| 0.1% | 693 | 2,302 | 4,603 | 95.2 |

Worked example: a 1% legendary at 4 hatches/min. The median player gets one in ~17 min and 10% of players are still dry after ~57 min. That 10% is your churn risk. Hard pity at 100 rolls (25 min) caps it.

### Pity systems
| Type | Mechanic | Effect |
|---|---|---|
| Hard pity | guaranteed hit at roll H since last hit | caps the worst case; players plan around it |
| Soft pity | from roll S, p rises by +Δ per roll | smooths the tail with no visible "cliff" |
| Bad-luck protection token | each miss grants a token; X tokens buy the item | turns VR into FR at the tail; ethical, transparent |
| Duplicate protection | an owned item is rerolled or converted to shards | prevents the "dupe streak" feeling |

Industry reference: Genshin Impact runs a 5★ base 0.6%, soft pity from about roll 74 and hard pity at 90. ⚠️ verify: public HoYoverse disclosure figures.

Roblox policy classes **pity systems and luck boosts as "probability modifier" paid random items**. If the rolls are paid (Robux, or currency bought with Robux), you must explain the effect numerically and show the player's current odds dynamically.

## Code: weighted tiers with luck and pity (server-only rolls)
```lua
--!strict
-- ReplicatedStorage/Shared/LootTable.lua
-- Pure logic module. Call roll() ONLY on the server; client uses currentOdds() for the odds UI.
local LootTable = {}

export type Item = { id: string, weight: number }
export type Tier = { name: string, weight: number, items: { Item } }
export type Pity = {
	tier: string, -- tier protected by pity
	softStart: number, -- roll number (since last hit) where soft pity begins
	softStep: number, -- added probability per roll after softStart (e.g. 0.02)
	hardAt: number, -- guaranteed on this roll number
}
export type RollResult = { tier: string, itemId: string, newPityCount: number }

local function pickWeighted<T>(list: { T }, weightOf: (T) -> number, rng: Random): T
	local total = 0
	for _, v in list do
		total += weightOf(v)
	end
	local r = rng:NextNumber() * total
	local acc = 0
	for _, v in list do
		acc += weightOf(v)
		if r < acc then
			return v
		end
	end
	return list[#list]
end

-- Returns tier probabilities (0..1) for the player's NEXT roll, after luck and pity.
function LootTable.currentOdds(tiers: { Tier }, pity: Pity?, pityCount: number, luck: number): { [string]: number }
	local weights: { [string]: number } = {}
	local total = 0
	for _, t in tiers do
		local w = t.weight
		total += w
		weights[t.name] = w
	end
	-- luck multiplies the weight of rare tiers (< 1% base)
	local luckedTotal = 0
	for _, t in tiers do
		local w = weights[t.name]
		if w / total < 0.01 then
			w *= luck
		end
		weights[t.name] = w
		luckedTotal += w
	end
	local odds: { [string]: number } = {}
	for name, w in weights do
		odds[name] = w / luckedTotal
	end
	if pity then
		local nextRoll = pityCount + 1
		local p = odds[pity.tier] or 0
		local forced: number? = nil
		if nextRoll >= pity.hardAt then
			forced = 1
		elseif nextRoll >= pity.softStart then
			forced = math.min(1, p + (nextRoll - pity.softStart + 1) * pity.softStep)
		end
		if forced then
			local rest = 1 - p
			for name, q in odds do
				if name == pity.tier then
					odds[name] = forced
				elseif rest > 0 then
					odds[name] = q / rest * (1 - forced)
				end
			end
		end
	end
	return odds
end

function LootTable.roll(tiers: { Tier }, pity: Pity?, pityCount: number, luck: number, rng: Random): RollResult
	local odds = LootTable.currentOdds(tiers, pity, pityCount, luck)
	local tier = pickWeighted(tiers, function(t: Tier): number
		return odds[t.name] or 0
	end, rng)
	local item = pickWeighted(tier.items, function(i: Item): number
		return i.weight
	end, rng)
	local newCount = pityCount + 1
	if pity and tier.name == pity.tier then
		newCount = 0
	end
	return { tier = tier.name, itemId = item.id, newPityCount = newCount }
end

-- Disclosure helper: percent strings rounded to 4 decimals (policy allows rounding + disclaimer)
function LootTable.formatOdds(odds: { [string]: number }): { [string]: string }
	local out: { [string]: string } = {}
	for name, p in odds do
		out[name] = string.format("%.4f%%", p * 100)
	end
	return out
end

return LootTable
```
Server usage (ServerScriptService/HatchService.server.lua):
- Use one `Random.new()` per server.
- Read `pityCount` from the player's profile ([[Data-Persistence-DataStores-And-ProfileStore]]). Deduct currency, roll and save the new count all in the same server step.
- Then tell the client which result to animate. The client never chooses or predicts the result ([[Anti-Exploit-And-Server-Authority]]).

## Near-miss
- A near-miss is a loss that looks almost like a win (the wheel stops one slot past the jackpot). Research on gambling shows near-misses raise the urge to continue even though they carry no information.
- **Allowed**: a near-miss that happened naturally. The visual is a true reflection of a fairly rolled outcome on free rolls.
- **Not allowed (vault rule)**:
  - Picking the "lose" animation that lands next to the jackpot more often than its true probability on paid spins.
  - Showing rare items "almost" dropping.
  - Fake "x players just won" tickers.
- Where to use near-miss legitimately: skill contexts (an obby fall one jump from the checkpoint, a boss left at 3% HP), where it feeds mastery ([[Difficulty-And-Mastery]]).

## Ethical boundaries (audience skews young)
1. **Free first**: every rarity tier must be reachable without Robux, even if slowly.
2. **Disclose everything** for paid random items:
   - Odds percentages summing to 100%, in a pop-up labelled with a word ("Details"/"Odds"). A bare (i) icon does not count.
   - Remaining odds updated when an outcome is unique-per-user.
3. **Respect `ArePaidRandomItemsRestricted`**. When it is true, choose one:
   - an earnable free path,
   - a disclosed deterministic order,
   - direct purchase priced at expected value (Roblox's example: a 5% sword in a 10-Robux box → sell it for 200 Robux),
   - hide or block the purchase.
4. **Respect `IsPaidItemTradingAllowed`**. Players without trading rights must not be able to trade paid-random outcomes.
5. No limited-time pressure on *paid* random items shorter than 24 h. No stacking "luck" purchases without showing the final odds. ⚠️ verify: vault ethics rule, not platform policy.
6. Monetise the convenience around the randomness (auto-hatch, triple hatch, faster hatch) more than the odds themselves. See [[Gamepasses-vs-Developer-Products]].

## Checklist
- [ ] Each random table has tier weights, item weights, a computed p, and a "rolls to 50%/90%" row in the balance sheet
- [ ] Pity configured for any chase tier < 1%, stored in DataStore, and reset on hit
- [ ] Odds UI built from `currentOdds()` so displayed odds always equal real odds, luck and pity included
- [ ] `PolicyService` checked on join; restricted players routed to the fallback treatment
- [ ] Rolls server-only; client receives the result to animate
- [ ] Hatch/drop events logged with tier for telemetry ([[Analytics-And-Instrumentation]])

## Pitfalls
- Odds shown on the UI that differ from the weights in code (an easy policy violation after a tuning patch). Generate the UI from the same table.
- Luck boosts that multiply *all* tiers do nothing. Luck must reweight the rare tiers only.
- Rolling on the client "for responsiveness". Exploiters can pick their results.
- Too many tiers (8+) with near-zero odds leave players feeling the game is rigged. Keep ≤ 6 visible tiers and make the top one obtainable.
- Pity counters that reset on rebirth or server hop without the player knowing.

## Related
- [[Core-Loops]] · [[Economy-Design-Sinks-And-Faucets]] · [[Prestige-And-Rebirth]] · [[Difficulty-And-Mastery]] · [[Balancing-Methods]]
- [[Gamepasses-vs-Developer-Products]] · [[Daily-Rewards-And-Streaks]] · [[Anti-Exploit-And-Server-Authority]] · [[Data-Persistence-DataStores-And-ProfileStore]] · [[Analytics-And-Instrumentation]]

## Sources
- Roblox Creator Docs, Paid random items policy guidelines: https://create.roblox.com/docs/production/monetization/paid-random-items (via github.com/Roblox/creator-docs, read 2026-10-04)
- DevForum, Clarifying Requirements for Paid Random Items: https://devforum.roblox.com/t/clarifying-requirements-for-paid-random-items/4654622
- Tech Times (2026-06-26), Korea's loot-box rules push Roblox to disclose odds worldwide: https://www.techtimes.com/articles/319148/20260626/koreas-loot-box-rules-push-roblox-disclose-item-odds-worldwide.htm
- John Hopson, Behavioral Game Design (Gamasutra, 2001): https://www.gamedeveloper.com/design/behavioral-game-design
- The Compulsion Loop Explained: https://www.gamedeveloper.com/business/the-compulsion-loop-explained
