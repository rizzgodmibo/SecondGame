---
tags: [prompting/monetisation, monetisation/design]
status: draft
updated: 2026-10-04
confidence: medium
---
# Prompting: Monetisation (Passes, Products, Shop, Receipts, Policy)

How to ask Claude for a monetisation plan and the code behind it so purchases are safe, compliant and honest. General rules: [[Prompting-Principles]].

## TL;DR
- **Separate the decisions from the code.** Claude proposes the catalogue (passes, products, starter pack, prices) using the vault's rules; Holden decides; then Claude builds. Paper Plane Toss's strategy ("copy the reference games") was Holden's call, recorded as such ([[Paper Plane Toss Monetization]]).
- **Name the hard blockers in every monetisation prompt:** an idempotent receipt handler keyed on `PurchaseId`, no hard-coded prices (`GetProductInfoAsync`), odds shown before any paid random item plus `PolicyService` gating, and paid entitlements that survive migrations ([[Monetisation-Design-Checklist]]).
- **Ask for the failure scenarios as tests,** not just "add a receipt handler": duplicate delivery, crash before/after save, two servers, profile not loaded, unknown product ([[Roblox Purchase Receipt Handling]]).
- **Make every number on screen computed** from live prices and config (savings %, per-egg price, "worth" values), never typed in. The shop trial did this for every tag ([[Shop Gauntlet Workbench]]).
- **Nothing is published or put on sale by Claude.** Creating passes or products and changing prices are Holden's actions.

## What Claude needs from you
- The genre and whether it's PvE or PvP (it decides what paid power is acceptable).
- Existing passes/products and their prices (from Creator Hub or Config), and which are already sold (the grandfather rule applies).
- Your stance on paid random items, trading and the starter pack, and any reference game's shop you want to match.

## Vault notes to point Claude at
| Note | Gives Claude |
|---|---|
| [[Monetisation-Design-Checklist]] · [[Monetisation-Mistakes]] | Hard blockers, launch levers, the trust rules (grandfathering, one unsolicited prompt per session) |
| [[Gamepasses-vs-Developer-Products]] · [[Pricing-Psychology]] · [[Bundles-And-Starter-Packs]] | Pass vs product, price ladders, charm prices, starter pack 49–149 R$ with ≥ 5× value |
| [[ProcessReceipt-Handling]] · [[Roblox Purchase Receipt Handling]] | Idempotency, `NotProcessedYet` rules, test scenarios |
| [[Pay-To-Win-Boundaries]] · [[Reward-Schedules]] · [[Moderation-And-Policy-Compliance]] | Speed vs power, odds disclosure, `ArePaidRandomItemsRestricted`, `IsPaidItemTradingAllowed` |
| [[Robux-Economy-DevEx-And-Platform-Cuts]] · [[Subscriptions-And-Premium-Payouts]] · [[Conversion-Funnels]] | 70% share, DevEx $0.0038, Plus, funnels and benchmarks (all dated) |
| [[Roblox Monetisation Policy Pricing and Revenue]] | Policy and pricing reuse guidance with review gaps |

## Prompts

### 1. Propose the monetisation plan
```text
Propose a monetisation plan for [Game]. Don't write code or create anything on Roblox.
READ FIRST: the GDD; Monetisation/Monetisation-Design-Checklist.md; Gamepasses-vs-Developer-Products.md; Pricing-Psychology.md; Bundles-And-Starter-Packs.md; Pay-To-Win-Boundaries.md; Reward-Schedules.md.
CONTEXT: [PvE simulator / PvP …], young teens, solo dev, about 10 SKUs at launch.
Give me a table: item, pass or product, what it does, proposed price, why (cite the note), and P2W risk. Include a 2–4 pass core set, one currency ladder with bonus % rising per tier, a starter pack (one-time, shown after the core loop clicks, never on join), and where each prompt appears (moment of need, after a win, the shop button).
Flag anything that needs PolicyService handling or odds disclosure. Tag everything PROPOSAL; I'll decide.
```

### 2. Build the receipt handler (after approval)
```text
Implement developer product handling for [products] following Monetisation/ProcessReceipt-Handling.md and Resources/Roblox Purchase Receipt Handling.md.
- Exactly one handler. Idempotency key = receiptInfo.PurchaseId, stored in the same profile as the granted goods, granted and recorded in one mutation on a copy, then committed.
- Return PurchaseGranted only after the save is confirmed; NotProcessedYet if the player left, the profile isn't loaded or owned, the save failed, the product is unknown, or anything errors. Never grant from PromptProductPurchaseFinished.
- Prices displayed from GetProductInfoAsync; product ids in Config.
Write a DevTest script that runs these scenarios and prints PASS/FAIL: duplicate delivery before and after save; receipt arriving before the profile loads; grant error halfway (no partial reward); unknown product id; two receipts overlapping. Quote the results and the code gate. Note that Studio test purchases don't exercise real failures: list what still needs a live private-server test.
```
Why: broken receipts are "the most expensive bug" ([[Monetisation-Mistakes]]); the scenario list is from the Paper Plane Toss audit.

### 3. Paid random items (eggs, spins, crates)
```text
Add paid [eggs] to [Game]. Rules (Monetisation/Pay-To-Win-Boundaries.md, Design/Reward-Schedules.md):
- Show every outcome with numerical odds summing to 100% before purchase, generated from the same table the server rolls with (one shared odds module).
- Roll on the server only; the hatch animation must show the server's real result (no fake near-misses).
- If PolicyService says ArePaidRandomItemsRestricted for the player, hide the paid option and show a clean alternative (free path or message), not a broken button. Check it on the server too.
- Robux-bought currency spent on eggs still counts as a paid random item.
- Add pity if the top item is under 1%.
Prove the odds with a 100,000-roll simulation in a spec and show the measured vs stated table.
```
Why: Fish a Monster checked its catch roll with 100k simulated rolls and shared the odds module between the server and the shop ([[Fish a Monster Catch and Reel Design]]).

### 4. Compliance and trust audit before release
```text
Audit [Game]'s monetisation before release, read-only. Check against Monetisation/Monetisation-Design-Checklist.md and Operations/Moderation-And-Policy-Compliance.md:
hard-coded prices anywhere; receipt handler idempotency and return paths; odds displayed vs odds in code; PolicyService checks (server side) for paid random items and paid-item trading; one-time products saved with a flag (starter pack never re-offered); pop-ups on join or chained; guilt or pressure copy; anything sold that a future change would nerf.
List findings by severity with file:line. Mark anything policy-dependent "⚠️ verify:" with what to check on the current Roblox docs.
```

## More examples (added 2026-10-04)
Shorter prompts for other common jobs. Same rules: fill every bracket, keep the check. Sourced patterns are credited in [[Community-Prompt-Examples]].

### Pass perk review (honour forever)
```text
Review [Game]'s passes as a buyer would. For each: is the perk easy to understand in one line, can we honour it forever without nerfing it, does it give paid power over other players (Monetisation/Pay-To-Win-Boundaries.md), and does it still work if data is wiped (passes are tracked by Roblox)? Suggest wording fixes; don't change prices or create anything.
```

### Currency pack ladder
```text
Design the [currency] pack ladder for [Game] from Monetisation/Pricing-Psychology.md: 4–5 tiers with prices ending in 9, bonus % rising per tier, "Best value" on the second-highest, pack sizes that scale with player progress if the economy needs it, and every number on screen computed from GetProductInfoAsync and Config. Show a table and check that no bigger pack is worse per Robux.
```

### Gifting
```text
Add gifting to [Game]: a player can buy [pass/product] for another player in the same server. Use developer products with the recipient stored before the prompt, granted in the receipt handler to the recipient's profile (or held until they're online), logged on both sides. List the abuse cases (gifting to alts, refunds) and how the receipt rules handle each.
```

### Limited-time offer (real deadline)
```text
Add a limited-time offer to [Game]: shown once per player after [condition], with a server-authoritative expiry saved in the profile, a visible countdown, and no re-run right after it ends. Players who already own its contents get excluded or a pro-rated version. Track offer_shown → opened → prompt → purchased with the analytics module.
```

### Roblox Plus perks
```text
Add perks for Roblox Plus members to [Game]: convenience or cosmetic only, never tactical power (Monetisation/Subscriptions-And-Premium-Payouts.md). Check player.HasRobloxSubscription on the server, and only reward the in-game Plus prompt after the subscription flag actually flips. Show the perk list for my approval first.
```

## How to check the result
- DevTest receipt scenarios all PASS; then a live private-server purchase on a non-owner account.
- The odds simulation matches the stated odds; restricted-policy players see a clean alternative.
- No literal prices in code (search for `R$` and digits in UI strings).
- Holden creates passes and products and sets prices himself.

## Pitfalls
- **"Permanent" items sold as products without a saved flag** are lost on a data wipe; passes are safer for permanence ([[Gamepasses-vs-Developer-Products]]).
- **Nerfing or re-pricing what players already bought** without grandfathering ([[Monetisation-Mistakes]]).
- **Price claims from old guides:** DevEx, Premium Payouts and cross-game sales all changed in 2025–26. Ask Claude to cite the vault note and its date ([[Robux-Economy-DevEx-And-Platform-Cuts]]).
- **Testing the creator account's ownership** is not proof for other players; use a separate account ([[Paper Plane Toss Monetization]]).
- **Wagers on outcomes** where currency can be bought with Robux count as gambling ([[Challenges Instead of Wagers]]).

## Related
[[Prompting/_Index|Prompting]] · [[Prompting-Principles]] · [[Prompting-UI]] · [[Prompting-Gameplay-Systems]] · [[Monetisation/_Index|Monetisation index]]

## Sources
- Local: [[Paper Plane Toss Monetization]], [[Roblox Purchase Receipt Handling]], [[Fish a Monster Catch and Reel Design]], [[Shop Gauntlet Workbench]].
- Platform rules and numbers: see the dated sources inside each linked Monetisation note.
