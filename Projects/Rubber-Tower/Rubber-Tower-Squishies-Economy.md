---
tags: [project/rubber-tower, design/economy, monetisation/pricing]
status: reviewed
updated: 2026-10-05
confidence: medium
---
# Rubber Tower: Squishies Economy (v1)

Holden locked these numbers on 2026-10-05 (USER). The model below checks them against player types. Numbers live in `RubberTower/src/shared/Config.luau` → `Squishies` (CheckpointReward, TitleReward, ReplaySummitReward, DailyStreak, DailyMissRule, Packs, HatPrice, Hats).

## TL;DR
- **Paid in code since 2026-10-05 (session-only, USER):**
  - title payouts (`TitleService`);
  - **checkpoints 50/75/100 and the 200 first summit, once each**;
  - **+20 replay summit once per UTC day** (`RewardService`).
  Each payout logs `[Squishies] name +N (reason) = total` to Output; the total shows in the dev panel. No HUD counter until the UI pass (USER).
  - **Clean runs only for the summit money** (USER, the Leap of Faith rule): a teleport up during the run means no 200, no +20 and no summit titles.
  - Studio-verified, see [[2026-10-05-Rubber-Tower-Studio-Test]]:
    - clean run: 75 → 225 → 400 → 1,050;
    - replay: +20, then "already paid today";
    - tainted summit: 0.
  - Not built yet: dailies, packs, hat purchases, real saving.
- **Faucets (all once per player, except dailies):**
  - Checkpoints: 50 / 75 / 100, Summit 200 (first clear = 425).
  - Titles (27, USER 2026-10-05): by rarity Common 25, Uncommon 75, Rare 75, Epic 150, Legendary 300, Mythic 300, once each. All 27 pay **2,975**.
  - Replay: **+20 for re-reaching the summit, once per day** (USER 2026-10-05).
  - Daily 7-day streak: 25, 30, 40, 50, 60, 75, 150 (430 per week). **A missed day restarts at day 1** (USER 2026-10-05).
- **Sinks:** 38 sold hats.
  - Prices by rarity: Common 30, Uncommon 75, Rare 175, Epic 400, Legendary 900, Mythic 2,250.
  - The whole collection costs **14,185**.
  - Summit_Crown is a reward, never sold.
- **Robux packs (developer products):** 99 → 400, 249 → 1,100, 499 → 2,500. That's 4.04 / 4.42 / 5.01 Squishies per R$, so the value ladder rises with every tier. 1 Squishy ≈ 0.20–0.25 R$.
- **Verdict (v2, with titles + replays):** a daily player now reaches a Mythic on about day 21 (was 39 on dailies alone) and the whole collection in about 5.7–6.4 months (was 7.6). One thing to watch: a first-clear player who saves gets a **Legendary on day 2** (was day 6). See "Model v2" below.
- Earlier risks, now decided by Holden (2026-10-05):
  1. Missing a day restarts the streak: **kept as Restart** (USER). Claude's grace-day proposal was declined.
  2. No repeat play faucet: **fixed with +20 per day for re-reaching the summit** (USER).
- One label fix, already applied in Config: the Bag's real bonus is **+9%**, not +10%.

## Faucets and sinks (USER, 2026-10-05)
| Source | Amount | Rule |
|---|---|---|
| CP1 / CP2 / CP3 / Summit | 50 / 75 / 100 / 200 | Once per player. New worlds pay more later |
| Titles (27) | By rarity: Common 25, Uncommon 75, Rare 75, Epic 150, Legendary 300, Mythic 300 (USER 2026-10-05; the old easy/medium/hard/very hard amounts mapped onto the hat rarities) | Once per title; all 27 = 2,975. List in Config `Titles` and [[Rubber-Tower]] |
| Replay summit | 20 | Once per day for re-reaching the summit (USER 2026-10-05) |
| Daily streak | 25, 30, 40, 50, 60, 75, **150** | Repeats every 7 days, 430 per week. Day 7 gets a bigger celebration (Daily_Chest_Day7). A missed day restarts at day 1 (USER) |
| Packs (dev products) | Handful 99 R$ → 400 · Bag 249 → 1,100 (+9%, Popular) · Bucket 499 → 2,500 (+24%, Best value) | Repeatable. Grant only via ProcessReceipt, idempotent, saved before granting ([[ProcessReceipt-Handling]], [[Gamepasses-vs-Developer-Products]]). Show the bonus ribbon and Squishies per R$ on each tile. Names are placeholders |

| Rarity | Price | Sold hats | Set cost | ≈ R$ |
|---|---|---|---|---|
| Common | 30 | 7 | 210 | 6–7 |
| Uncommon | 75 | 8 (incl. Snail_Shell_Helm, halfway) | 600 | 15–19 |
| Rare | 175 | 9 (incl. Spore_Puff_Cap, Firefly_Jar_Hat, halfway) | 1,575 | 35–43 |
| Epic | 400 | 7 (incl. Toadstool_Top_Hat, halfway) | 2,800 | 80–99 |
| Legendary | 900 | 5 | 4,500 | 180–223 |
| Mythic | 2,250 | 2 (Cosmic_Jellyfish, Duck_King) | 4,500 | 449–557 |
| **Total** | | **38** | **14,185** | |

## Player types, model v1 (2026-10-05, before the title list)
**How the model works:**
- Exact day-by-day wallet model (script in the session scratchpad, numbers above). "Can afford" = spending cheapest first; the first hat pays its Easy title (+25). Time to Legendary/Mythic = extra days of dailies if they save everything from that point.
- **The title list is not written yet, so this is an ASSUMPTION:**
  - Easy: CP1, CP2, first hat.
  - Medium: CP3, Summit, push 5 players.
  - Hard: friends title.
  - Very hard: excluded, since few players will get it.

| Player type | Checkpoints | Titles | Dailies | Wallet | Can afford (cheapest first) | Legendary | Mythic |
|---|---|---|---|---|---|---|---|
| Plays once, quits before the top (CP2) | 125 | 50 | 25 | **200** | all 7 Commons | +13 days | +35 days |
| Plays once and clears | 425 | 200 | 25 | **650** | 7 Commons + 6 Uncommons, *or* a Rare + an Uncommon + 2 Commons with 365 left | +6 days | +28 days |
| First clear + 1 week of dailies | 425 | 275 | 430 | **1,130** | all Commons + Uncommons + 1 Rare, *or* a Legendary now | now | +20 days |
| Daily for a month (30 days) | 425 | 425 | 1,775 | **2,625** | all Commons, Uncommons and Rares, *or* a Mythic now | now | now |
| Daily for 3 months (90 days) | 425 | 425 | 5,440 | **6,290** | every Common to Epic + 1 Legendary (44% of the collection) | now | now |

**Daily-only pace (no titles or checkpoints):**
- 1,775 per 30 days (~1,840/month on average).
- Legendary on day 16, Mythic on day 39, the whole collection on day 231 (~7.6 months).
- Holden's rough maths (~2 weeks / ~5 weeks / 7–8 months) checks out.

## Model v2: Holden's title list + the replay reward (2026-10-05)
**How it works:** the same day-by-day model (scratchpad `econ2.py`, run with Blender's Python), now using the real titles.

**Assumptions (which titles each player type gets):**
- Quitter: Wobbly Beginner, Meadow Hopper, Mushroom Muncher.
- Clear: those three + Frostbitten, Rubber Champion, Bonk Survivor (100 falls in a ragdoll climb).
- Week: + Loyal Squish.
- Month: + Daily Wobbler, Secret Finder, Helping Hand, Squishmaster; buying earns Hat Collector + Mushroom Fashion.
- 3 months: + Pro Faller, Disco Duck, Duck Whisperer, Pushy, Long Way Down.
- Fresh Fit is paid on the first hat.
- **Replays:** 3 of 7 days in the first week, 12 of 30 days for a month, 36 of 90 days for 3 months.

**Title payouts:**
| Rarity | Titles | Pays | Subtotal |
|---|---|---|---|
| Common | 5 | 25 | 125 |
| Uncommon | 7 | 75 | 525 |
| Rare | 7 | 75 | 525 |
| Epic | 4 | 150 | 600 |
| Legendary | 2 | 300 | 600 |
| Mythic | 2 | 300 | 600 |
| **All 27** | | | **2,975** (21% of the 14,185 collection) |

**Player types:**
| Player type | Titles (v1 → v2) | Replays | Wallet (v1 → v2) | Can afford, cheapest first (v2) |
|---|---|---|---|---|
| Plays once, quits at CP2 | 50 → 125 | 0 | 200 → **275** | all 7 Commons + 1 Uncommon |
| Plays once and clears | 200 → 425 | 0 | 650 → **875** | all Commons + all Uncommons (15 hats) |
| First clear + 1 week | 275 → 500 | 60 | 1,130 → **1,415** | 15 hats + 3 Rares |
| Daily for a month | 425 → 1,100 | 240 | 2,625 → **3,540** | every Common to Rare + 3 Epics (27 hats) |
| Daily for 3 months | 425 → 1,550 | 720 | 6,290 → **8,135** | every Common to Epic + 3 Legendaries (34 of 38) |

**How much faster the hats get (saving from the first clear; dailies + checkpoints + titles):**
| Pace | v1 (dailies only) | v1 + assumed titles | v2 (clear titles, no replays) | v2 + replays 3 days a week |
|---|---|---|---|---|
| Legendary (900) | day 16 | day 6 | day 2 | day 2 |
| Mythic (2,250) | day 39 | day 28 | day 25 | **day 21** |
| Whole collection | day 231 (7.6 months) | day 223 | day 218 | **day 192 (6.3 months)** |

- A dedicated player who also earns the 3-month titles finishes the collection around **day 174 (5.7 months)**. Adding Speedy Noodle, Party Starter and Checkpoint Who? brings it to about day 161.
- Mad Hatter (+300) only pays after the last hat, so it doesn't speed up the collection.

**Honest read on v2 (recommendations, not decisions):**
- **2,975 from titles is fine.** It's 21% of the collection, most of it comes from long-term or skill titles, and every title pays once. It makes titles feel worth chasing without replacing the daily streak.
- **Day one got richer:**
  - A first-clear player now has 875, enough for all 15 Commons and Uncommons.
  - That's generous, but those hats are cheap (810 in total) and it gives a great first session.
- **The one spot that's arguably too fast is Legendary on day 2** for a player who saves everything after the first clear (Rubber Champion's 150 does most of it).
  - If Legendaries should feel earned, a PROPOSAL was to raise Legendary to 1,200. **Declined: Holden keeps Legendary at 900 and the economy as it is (USER 2026-10-05).**
  - Leaving it is also defensible: most kids spend on cheap hats first, which delays a Legendary anyway.
- **Mythic at about 3 weeks of dailies + replays still feels like a goal**, and the 499 R$ Bucket stays a shortcut, not a requirement.
- **The replay reward does its job:** an active climber earns ~240 extra a month on top of 1,775 from dailies (about 14% more) for actually playing, without becoming the main faucet.

## Honest read: too slow, too fast? (recommendations, not decisions)
- **The day-1 goal is met.** A first-clear player has ~650. Holden's target (a Rare + an Uncommon + a couple of Commons) costs 310, so they also have room for the first-hat title. Even a quitter can buy every Common.
- **Legendary in ~2 weeks and Mythic in ~5–6 weeks of dailies** feels right for young teens:
  - long enough to be a goal;
  - not so long it feels impossible;
  - the 499 R$ Bucket is a clear shortcut to a Mythic without being required.
- **Full collection ~7.6 months on dailies alone is long but fine.** Collections are meant to outlast the first month, and future worlds and titles will add faucets.
- **Risk 1: missing a day resets the streak.** The vault rule ([[Daily-Rewards-And-Streaks]]) is "never make one miss fatal"; hard resets churn the best players, and young teens miss days for school and trips.
  - **PROPOSAL:** keep Holden's 7-day track, but give **1 free "grace" day per completed week (max 2 banked)**. A miss uses one automatically; with none banked, the streak restarts at day 1.
  - **Decided 2026-10-05: Restart** (USER). Config `DailyMissRule = "Restart"`.
- **Risk 2: no repeatable play faucet.**
  - After the first clear, Squishies only come from logging in. A player who climbs the tower five times a day earns the same as one who logs in for 10 seconds, which fights the core loop ("climb, fall, retry").
  - **PROPOSAL (keeps the structure):** a small capped repeat reward, e.g. **+20 for re-reaching the Summit, once per day**. That's about 600 per month for an active player, roughly a third faster to a Mythic.
  - Alternatively, leave it out and let future worlds plus events carry this.
- **Risk 3 (minor): the shop has no sink after the collection is done.** That's fine for v1. Future worlds and event hats keep Squishies meaningful. Watch the wallet balance of 3-month players in analytics.
- **Packs:** the value ladder is correct (never inverted). The 99 R$ Handful buys exactly one Epic, which is a good impulse anchor. The Bucket buys a Mythic with 250 left (a Rare + an Uncommon), so the leftover isn't wasted. The bonus labels must be computed against the Handful rate: Bag **+9%**, Bucket **+24%**.

## Platform checks (verified 2026-10-05, live creator docs)
- **Developer products:**
  - Repeatable; 1 to 1 billion R$.
  - Grant via the `ProcessReceipt` callback (return `PurchaseGranted` / `NotProcessedYet`; set once by one server script).
  - Cross-game product sales disabled since 2026-05-30.
- **Regional pricing for developer products is OPT-IN:**
  - Requires dynamic prices and `GetUsersPriceLevelsAsync`.
  - Regional prices sit at 30–100% of the default.
  - Unchanged from the vault's 2026-10-02 snapshot.
- Revenue share (70%) is not on the developer-products page itself; it comes from [[Gamepasses-vs-Developer-Products]].

## Checklist (before phase 4/4b code)
- [x] Holden: streak miss rule = Restart; repeat summit = +20 once per day (USER 2026-10-05)
- [x] Title list written with tiers (USER 2026-10-05; Config `Titles`). Final names by Claude on Holden's instruction, same counts per rarity, so the model and the 2,975 total are unchanged ([[Rubber-Tower]])
- [ ] Duck Whisperer goal = number of Hidden_Duck props placed (set when the map is built)
- [ ] Packs created as developer products; ProductIds in Config; UI prices from `GetProductInfoAsync`
- [ ] ProcessReceipt handler: idempotent, saved before granting, tested with repeated receipts
- [ ] Sim spec in `tests/` replays these player types against Config (phase-4 gate, [[Roblox Economy Modelling and Progression Tests]])

## Pitfalls
- Don't label pack bonuses by eye; compute them against the base pack rate.
- Hard-coded Robux prices in the UI go wrong as soon as regional pricing or price tests are on.

## Related
[[Rubber-Tower]] · [[Rubber-Tower-GDD]] · [[Economy-Design-Sinks-And-Faucets]] · [[Roblox Economy Modelling and Progression Tests]] · [[Pricing-Psychology]] · [[Daily-Rewards-And-Streaks]] · [[ProcessReceipt-Handling]] · [[Gamepasses-vs-Developer-Products]] · [[Rubber-Tower-Valley-Kit]]

## Sources
- Holden's decisions in chat, 2026-10-05.
- Roblox creator docs, accessed 2026-10-05: https://create.roblox.com/docs/production/monetization/developer-products and https://create.roblox.com/docs/production/monetization/regional-pricing
