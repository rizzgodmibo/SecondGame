---
tags: [monetisation/ethics, monetisation/policy]
status: draft
updated: 2026-10-04
confidence: medium
---
# Pay-to-Win Boundaries and Paid Random Items

## TL;DR
- Players accept paid **speed** (progress faster, automate, more slots) in **PvE/simulator/idle** games. They reject paid **power over other players** in **competitive PvP**. Draw the line at "can money beat a skilled free player head-to-head?"
- In PvP, sell **cosmetics, convenience and sidegrades**. Gate paid power behind matchmaking separation, or cap it (paid weapons equal to earnable ones, just obtained earlier).
- **Paid random items** (eggs, spins, crates, and anything bought with Robux-purchasable currency) **must show all outcomes and numerical odds before purchase**. That includes luck boosts and pity systems, whose effect must be shown numerically and updated live.
- Check `PolicyService:GetPolicyInfoForPlayerAsync(player).ArePaidRandomItemsRestricted` per player. Restricted users must get one of Roblox's approved treatments: free path, deterministic order, direct purchase at expected-value price, removal, error message, or teleport away. Also check `IsPaidItemTradingAllowed` before allowing trades of paid items.
- Premium/Plus/subscriber perks: **no tactical advantage**. Roblox guidance says so explicitly for Premium.

## Acceptance matrix (where power purchases work)

| Genre / mode | Paid speed (2×, auto) | Paid power (stats, weapons) | Paid cosmetics | Paid random (eggs/spins) | Notes |
|---|---|---|---|---|---|
| Simulator / idle / tycoon | ✅ Expected | ✅ Mostly accepted (PvE) | ✅ | ✅ Core loop, with odds disclosure | The leaderboard is the only "PvP". Consider a separate free-to-play leaderboard |
| PvE RPG / dungeon co-op | ✅ | ⚠️ OK if it doesn't trivialise content for the party | ✅ | ⚠️ Gear gacha = backlash risk | Paid revives are fine with a cap per run |
| Social / roleplay / hangout | n/a | n/a | ✅ Primary model | ⚠️ Low fit | Houses, vehicles, outfits |
| Obby / platformer | ✅ Skips accepted | n/a | ✅ Trails, effects | ❌ | "Skip stage" is the classic product |
| Competitive PvP (shooter, fighting) | ⚠️ XP boosts only | ❌ Backlash | ✅ Skins, emotes, kill effects | ⚠️ Cosmetic-only crates | Battle pass with cosmetic rewards |
| Asymmetric / party PvP | ⚠️ | ⚠️ Paid "roles" OK if balanced and rotated | ✅ | ⚠️ | Paid "choose your role" products are common. Cap per round |
| Trading-economy games | ✅ | ⚠️ | ✅ | ✅ Drives trading | Regional price arbitrage. `IsPaidItemTradingAllowed` |

Decision rules:
1. If a paid item changes **PvP outcome odds by >10%** for equal skill (assumption, test it), make it earnable at a reasonable free pace, or remove it from ranked/competitive modes.
2. **Never sell the only best item.** A free path to equivalent power must exist, and paying should buy time, not exclusivity of power.
3. Paid power in PvP is more tolerable when the matchmaking pool separates it (casual servers vs. ranked with normalised stats).
4. Visibility amplifies resentment. If paid players one-shot free players in public servers, expect "P2W" reviews and ratings drops, even if the revenue looks good short-term.

## Paid random items: compliance spec (Roblox policy, 2026-10)

**Scope:** any random outcome paid for **directly with Robux or indirectly with currency purchasable with Robux**: capsules (eggs, chests, wheels), enhancement items (random-duration potions, upgrade chances), combination/fusion, and probability modifiers (luck boosts, pity, rate-ups, enhanced drops). Free random rewards (a found key opens a chest) need no disclosure.

**Display rules:**
- List **all possible outcomes** with **numerical odds as percentages** that sum to exactly 100%. Rounding is allowed to ≥4 decimal places past the first non-zero digit, with a rounding disclaimer.
- If outcomes don't fit in the 3D view, use a clickable pop-up with a visible **word** ("Info"/"Details") **before purchase**. A bare (i) icon is not sufficient.
- Shared odds can be stated once ("Odds for each item below: X%").
- If outcomes are unique per user (can only be obtained once), **update the remaining odds for that user**.
- Luck/odds modifiers: explain the effect numerically before purchase, and show the **live modified odds** while active.
- External sales (Store tab) and promoted passes **may not** include paid random items. Rewarded-ad rewards **may not** be random.

**Restricted users** (`ArePaidRandomItemsRestricted == true`), pick one treatment:

| Treatment | Example |
|---|---|
| Free, earnable path | Eggs granted at gameplay milestones |
| Deterministic, disclosed order | Spin 1 = 5 gems, spin 2 = 10 gems, … |
| Direct purchase at expected-value price | 10 R$ crate with 5% sword → sell sword for 200 R$ |
| Remove/hide | Replace the wheel with a direct shop |
| Block with a message | "Unavailable in your region" |
| Remove the user from that area | Teleport them away |

```lua
--!strict
-- ServerScriptService/Monetisation/PolicyGate.luau (ModuleScript)
local PolicyService = game:GetService("PolicyService")
local Players = game:GetService("Players")

export type Policy = { randomRestricted: boolean, tradingAllowed: boolean }
local cache: { [Player]: Policy } = {}
local PolicyGate = {}

local SAFE_DEFAULT: Policy = { randomRestricted = true, tradingAllowed = false } -- fail closed

function PolicyGate.Get(player: Player): Policy
	local hit = cache[player]
	if hit then return hit end
	for attempt = 1, 3 do
		local ok, info = pcall(PolicyService.GetPolicyInfoForPlayerAsync, PolicyService, player)
		if ok and type(info) == "table" then
			local p: Policy = {
				randomRestricted = (info :: any).ArePaidRandomItemsRestricted == true,
				tradingAllowed = (info :: any).IsPaidItemTradingAllowed == true,
			}
			cache[player] = p
			return p
		end
		task.wait(attempt)
	end
	return SAFE_DEFAULT -- not cached, so it retries next call
end

Players.PlayerRemoving:Connect(function(p) cache[p] = nil end)
return PolicyGate
```
Use it server-side **before** every paid-random prompt or spend of Robux-bought currency on a random outcome, and before every trade of paid items. The client only hides UI. A fail-closed default prevents a compliance breach when the API is down.

## Community backlash patterns (documented and observed)
- **Regional-pricing arbitrage in donation/trading games:** creators of PLS DONATE-style games objected when regional pricing hit passes used as donations (DevForum regional pricing thread, 2025). Lesson: anything transferable needs `GetUsersPriceLevelsAsync` gating.
- **Cross-game pass sales disabled 2026-05-30:** donation and "support me" mechanics built on buying another game's pass broke. Use Robux transfers (Plus) instead.
- **Common pattern: paid exclusive power pets or weapons outclassing all free content in PvP servers** leads to "P2W" reviews, a rating drop, and a falling like ratio, which affects discovery. ⚠️ verify: collect named, dated examples in [[Monetisation-Mistakes]] once sourced.
- **Odds non-disclosure:** policy violation that can lead to removal or moderation. Fixing it after launch also exposes how low the odds were, which hurts trust twice.

## Checklist
- [ ] Every paid item classified: speed / power / cosmetic / random
- [ ] PvP: no paid item gives a head-to-head edge not obtainable free at a reasonable pace
- [ ] All paid random sources show the full outcome list with % odds before purchase, plus live boosted odds
- [ ] `ArePaidRandomItemsRestricted` treatment implemented and tested. Fail closed
- [ ] `IsPaidItemTradingAllowed` and price-level gating on trades and gifts
- [ ] Maturity & Compliance Questionnaire answered accurately for paid random items (see [[Moderation-And-Policy-Compliance]])
- [ ] Subscriber/Plus perks are non-tactical

## Pitfalls
- Odds that change silently (event rate-ups) without updating the display.
- Treating "gems bought with Robux" as exempt. Indirect purchases are in scope.
- Luck boosts sold as "much luckier!" without numbers. Non-compliant.
- Selling paid random items externally or in promoted passes: prohibited.
- Restricted-region users seeing a broken wheel instead of a clean treatment. That counts as a policy failure, not just bad UX.

## Related
- [[Monetisation/_Index]] · [[Monetisation-Mistakes]] · [[Subscriptions-And-Premium-Payouts]] · [[Gamepasses-vs-Developer-Products]]
- [[Moderation-And-Policy-Compliance]] · [[Genre-Playbooks]] · [[Economy-Design-Sinks-And-Faucets]]

## Sources
- Roblox creator-docs, "Paid random items policy guidelines" `production/monetization/paid-random-items.md` (snapshot 2026-10-02): https://create.roblox.com/docs/production/monetization/paid-random-items (accessed 2026-10-04)
- Roblox Community Standards, Roblox economy / paid random items: https://about.roblox.com/community-standards#roblox-economy-paid-random-items
- Roblox creator-docs `engagement-based-payouts.md` (Premium: "do not give them a tactical gameplay advantage"), `passes.md`, `developer-products.md`, `promotion/rewarded-video-ads.md`
- DevForum, "Introducing Regional Pricing for Passes" p.6 (2025): https://devforum.roblox.com/t/introducing-regional-pricing-for-passes/3621382?page=6
- DevForum, "Best way to monetize a game without being too Pay2Win or greedy?" (2025): https://devforum.roblox.com/t/best-way-to-monetize-a-game-without-being-too-pay2win-or-greedy/3428955
- Acceptance matrix: author synthesis. ⚠️ verify per genre via [[Genre-Playbooks]]
