---
tags: [project/rubber-tower, design/economy]
status: final
updated: 2026-10-05
---
# Rubber Tower: hat prices + Squishies earning + batch (h) prompt

Next session prompt (2026-10-05). The numbers are proposals; Holden can edit them before pasting.

```
Next session. Two parts: lock the Squishies economy for the hats, then start batch (h).

PART 1: SQUISHIES ECONOMY (my decisions; record them in [[Rubber-Tower]] and [[Rubber-Tower-GDD]] as USER)
How players earn Squishies (all payouts are once per player unless it says otherwise):
- Checkpoints: CP1 = 50, CP2 = 75, CP3 = 100, Summit = 200 (first clear = 425 total). New worlds later pay more.
- Titles: every title pays once. Easy titles 25, medium 75, hard 150, very hard ("reach the top without claiming checkpoints") 300. Put the amount next to each title when the title list is made.
- Daily reward, a 7-day streak that repeats: day 1 = 25, day 2 = 30, day 3 = 40, day 4 = 50, day 5 = 60, day 6 = 75, day 7 = 150 (the milestone, with a bigger celebration). 430 per full week. Missing a day restarts the streak at day 1 (PROPOSAL, tell me if you think a softer rule is better for young teens).
- Squishies packs for Robux: exactly 3, increasing in size. These are DEVELOPER PRODUCTS (repeatable), not gamepasses ([[Gamepasses-vs-Developer-Products]]), so receipts must follow [[ProcessReceipt-Handling]] (idempotent, saved before granting).
| Pack | Robux | Squishies | Squishies per R$ | Bonus | Tag |
|---|---|---|---|---|---|
| Handful | 99 | 400 | 4.04 | — | — |
| Bag | 249 | 1,100 | 4.42 | +10% | Popular |
| Bucket | 499 | 2,500 | 5.01 | +24% | Best value |
  Why these numbers (from [[Pricing-Psychology]]): charm prices from the vault ladder (99/249/499), the cheapest pack is an impulse buy under 399 R$, value per Robux goes up with every tier (never an inverted ladder), and the bonus grows with the tier. Show the bonus ribbon and the Squishies-per-Robux on each tile. Pack names are placeholders; I may rename them. Check that Roblox's current developer product rules and regional pricing (opt-in for products) haven't changed (⚠️ verify).

Hat prices by rarity (Squishies):
| Rarity | Price | Hats | About the same as |
|---|---|---|---|
| Common | 50 | 7 | 12 R$ |
| Uncommon | 125 | 8 (incl. Snail_Shell_Helm, halfway only) | 30 R$ |
| Rare | 300 | 9 (incl. Spore_Puff_Cap + Firefly_Jar_Hat, halfway only) | 75 R$ |
| Epic | 700 | 7 (incl. Toadstool_Top_Hat, halfway only) | 175 R$ |
| Legendary | 1,500 | 5 | 300 R$ |
| Mythic | 4,000 | 2 sold (Cosmic_Jellyfish, Duck_King) | 800 R$ |
- Summit_Crown is NOT sold. It's the reward for reaching the summit.
- Halfway-only hats cost the same as their rarity; the reason to stop there is that they're exclusive.
- Buying your first hat unlocks its title (already decided), so the first purchase should be easy: a first-clear player (425 + early titles) can afford a Rare plus a Common, or an Uncommon and a few Commons, on day 1. The smallest pack (400) also buys a Rare, so a first Robux purchase gets a real hat.

Check the numbers before locking them:
- Use [[Roblox Economy Modelling and Progression Tests]] and [[Economy-Design-Sinks-And-Faucets]]. Make a small table (a sheet or markdown) with player types: "plays once", "first clear + 1 week of dailies", "daily player for a month", "daily player for 3 months". For each, show which hats they can afford and how long a Legendary and a Mythic take.
- My rough maths: the whole collection is 24,450 Squishies (about 13 months of dailies alone); a daily-only player gets about 1,840 a month, so a Legendary takes about 3–4 weeks and a Mythic about 2 months. The Robux value of hats sits inside the vault's 299–1,499 R$ range for exclusive cosmetics at the top end. Tell me honestly if that feels too slow or too fast for young teens and suggest changes, but keep my structure (milestones, titles, 7-day daily).
- Put every number in Config so we can tune it later. No economy code beyond that yet unless it's already in the plan.

PART 2: START BATCH (h) (extra and misc models)
- Follow the batch (h) checklist in [[Rubber-Tower-Valley-Kit]]: hub/village pieces, segment entry gates, height markers, the fantasy extras, the secrets, the misc list and the seasonal set.
- Skip anything batches (a)–(g) already made (reuse it or make a colour variant).
- Make sure these gameplay items look great since they show up in UI too: the banana peel, the Squishies pickup (use the chosen Duck/Grape coin style), the trophies and the checkpoint flags.
- Add the daily reward pieces if they're missing: the gift chest/mailbox from (f) with a "day 7" big chest version.
- Same rules as before: v5 style locked ([[Rubber-Tower-Art-Style-Guide]]), references next to every model, preflight PASS, phone-friendly, a diorama render, self-critique first, then stop for my review.
- Still no uploads. When (h) is done, the next step is uploading the kit to the test place to check the hats on real avatars and in ragdoll.
```
