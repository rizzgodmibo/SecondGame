---
tags: [monetisation/anti-patterns]
status: draft
updated: 2026-10-04
confidence: medium
---
# Monetisation Mistakes That Lose a Paying Playerbase

## TL;DR
- The paying base runs on **trust**. Whatever someone paid for must keep its value, keep working, and never vanish. Most Roblox monetisation disasters are **retroactive changes to things already sold**: nerfs, wipes, price cuts without compensation, exclusive items made obtainable again.
- **Broken receipts** are the most expensive bug: Robux charged and no item. See [[ProcessReceipt-Handling]]. Never ship products without an idempotent handler.
- **Aggressive pop-ups** (on join, chained, mid-combat) make reviews say "cash grab". Limit to one unsolicited prompt per session.
- **Too many currencies** (more than 2 premium-adjacent ones) hide prices, confuse kids and parents, and lead to refund requests. Use one soft currency, one premium currency at most, and event tokens that expire clearly.
- Before any change touching paid content, apply the **grandfather rule**: existing buyers keep the old value, or get compensation at least equal to what they lost.

## Mistake catalogue

| # | Mistake | Why it hurts | Do instead |
|---|---|---|---|
| 1 | **Nerfing a paid pass** (2× → 1.5×, auto-farm slowed) | Buyers feel robbed and ask for refunds. Roblox doesn't refund passes, so the anger goes to reviews and social media | Design pass perks you can honour forever. If balance demands it, grandfather owners or give compensation (a free exclusive item, currency ≥ pass price) and announce it beforehand |
| 2 | **Wiping data** (economy reset, new "season" that wipes paid items) | Paid items vanishing is the #1 trust killer. Also double-grant risk if `PurchaseIds` is wiped | Migrate, never wipe, paid fields. Seasonal resets touch only free progression, and paid cosmetics persist |
| 3 | **Broken / non-idempotent receipts** | Lost purchases or duplicated currency (economy inflation) | [[ProcessReceipt-Handling]] pattern. Test rejoin/server-hop cases |
| 4 | **"Rejoin to receive your item"** | Looks like a scam. Some players leave and never return | Apply pass perks live on `PromptGamePassPurchaseFinished`. Grant products in-session |
| 5 | **Aggressive pop-ups** (on join, every death, chained) | Early-session churn, which lowers D1 and therefore discovery | ≤1 unsolicited prompt per session, none in the first 3 min; contextual prompts only. See [[Conversion-Funnels]] |
| 6 | **Devaluing exclusives** (re-releasing a "limited" item, giving away a former paid item free) | Collectors' items lose value. Trading-game economies crash | Variants (shiny/v2) instead of re-release. Honour "limited" literally |
| 7 | **Price drops right after a launch sale** without protection | Early buyers feel punished | Launch-price guarantees, or partial credit for recent buyers |
| 8 | **Price hikes on established items** | Screenshots of the old price circulate. Fairness complaints | Raise via new items or bundles. Grandfather existing sales. Robux subscriptions require 30 days' notice for increases |
| 9 | **Too many currencies** (gems, crystals, tokens, stars, coins…) | Obscures real prices. Hard to disclose odds properly. Parents complain | 1 soft + ≤1 premium currency. Event currency auto-converts at event end. See [[Economy-Design-Sinks-And-Faucets]] |
| 10 | **Hard-coded prices** | With Managed Pricing / Plus discounts, the UI shows the wrong price | `GetProductInfoAsync` everywhere |
| 11 | **Odds not disclosed / silently changed** | Policy violation. Reveals were-worse odds later, so trust is lost twice | Live odds UI. Announce rate changes in patch notes. See [[Pay-To-Win-Boundaries]] |
| 12 | **Paid power in PvP** | "P2W" reviews, a falling like ratio, and free players leave, which removes the content whales pay to beat | Cosmetics/convenience in PvP. Separate ranked |
| 13 | **Changing private server price** | **Cancels all active PS subscriptions** (Roblox behaviour) | Set it once at launch |
| 14 | **Deleting a local-currency subscription** | Forces refunds to all subscribers | Take off sale + cancel renewals, then wait |
| 15 | **Converting a pass into a subscription for existing owners** | Taking away something already paid for | Keep the pass honoured forever. Sell the subscription to new users |
| 16 | **Selling items you can't deliver** (sold-out limited, ended event) | Roblox charged, so you must grant | Check eligibility before prompting |
| 17 | **Relying on platform features that can change** (cross-game passes, Premium Payouts) | Business model breaks overnight | Diversify revenue. Watch DevForum announcements. See [[Robux-Economy-DevEx-And-Platform-Cuts]] |
| 18 | **No support trail** | Can't verify or refund claims → angry Discord | Log PurchaseId/ProductId/CurrencySpent per user |
| 19 | **Dark patterns** (fake countdowns, fake "92% off", confirm-shaming) | Policy risk under deceptive-practice rules, plus trust loss with older players | Real deadlines and real reference prices. ⚠️ verify: Community Standards wording on misleading commerce |

## Real examples (dated, sourced)
- **Pet Simulator X NFTs (BIG Games, 2021-11-09):** BIG Games announced NFT-linked pets giving 12 players exclusive pets nobody else could get. Fans publicly said they'd quit and skip future events. Lesson: off-platform-exclusive or ultra-scarce items sold outside the game's normal economy anger the core collectors. (Pro Game Guides, 2021)
- **Pet Simulator 99 RNG egg odds nerf:** an update cut the chance of Huge/Titanic pets from the RNG egg drastically (reported 1 in 999M → 1 in 100B). It drew heavy backlash and calls to revert. Lesson: odds of a monetised random system are part of the deal, so changes need communication and compensation. ⚠️ verify: exact update date (Gamederp report)
- **Gamepass nerf → refund demands (DevForum, 2021):** a developer nerfed a gamepass and players asked for Robux refunds. Community advice converged on compensation and avoiding nerfs to paid perks. (DevForum thread 1156739)
- **Cross-game pass/product sales disabled (Roblox, effective 2026-05-30; announced ~2026-05):** donation games like PLS DONATE that relied on buying other players' passes faced an existential change. The replacement Transfers API requires Roblox Plus, and under-18 transfers need parental consent. Reports cite a 1,000 R$/month transfer cap. ⚠️ verify: cap figure. Lesson: don't build your whole revenue on a loophole in platform features. (PiunikaWeb 2026-05-05; Bloxy News on X)
- **Regional pricing on donation passes (2025):** creators of PLS DONATE, Starving Artists and similar games objected that discounted regional prices broke donation semantics. (DevForum regional pricing thread, p.6)

## Pre-change checklist (run before any patch touching paid content)
- [ ] Does this reduce the value of anything sold? If yes, apply grandfathering or compensation ≥ value lost
- [ ] Does this remove or re-release anything sold as exclusive or limited? If yes, don't
- [ ] Are `PurchaseIds` and paid entitlements untouched by migrations?
- [ ] Are odds changes reflected in the UI and patch notes?
- [ ] Have price changes been announced ahead? Do old buyers get protection?
- [ ] Community announcement drafted (Discord/group shout) with the compensation explained

## Pitfalls
- "It's only a small nerf." Players compare against what they paid for, not against game balance.
- Quiet changes get found by data miners within hours, so it is always better to announce.
- Compensating with soft currency that is worth less than the loss. Compensation must feel bigger than the loss.

## Related
- [[Monetisation/_Index]] · [[ProcessReceipt-Handling]] · [[Pay-To-Win-Boundaries]] · [[Pricing-Psychology]] · [[Monetisation-Design-Checklist]]
- [[Economy-Design-Sinks-And-Faucets]] · [[Data-Persistence-DataStores-And-ProfileStore]] · [[Moderation-And-Policy-Compliance]]

## Sources
- Pro Game Guides, "Pet Simulator X faces backlash from fans after NFT release" (2021-11): https://progameguides.com/roblox/pet-simulator-x-faces-backlash-from-fans-after-nft-release/
- Gamederp, "Roblox Pet Simulator 99 Faces Negative Backlash Over Massive Nerf to RNG Egg Drops" (date ⚠️ verify): https://gamederp.com/roblox-pet-simulator-99-faces-backlash-over-massive-nerf-to-rng-egg-drops/
- DevForum, "Players ask for refund after gamepass nerf" (2021): https://devforum.roblox.com/t/players-ask-for-refund-after-gamepass-nerf/1156739
- PiunikaWeb, "Roblox will disable cross-game Gamepass sales…" (2026-05-05): https://piunikaweb.com/2026/05/05/roblox-disable-gamepasses-sales-players-furious/
- Bloxy News on X, Roblox response re cross-game sales (2026-05): https://x.com/Bloxy_News/status/2051771169486131328
- DevForum, "Introducing Regional Pricing for Passes" p.6 (2025): https://devforum.roblox.com/t/introducing-regional-pricing-for-passes/3621382?page=6
- Roblox creator-docs (snapshot 2026-10-02): `passes.md` / `developer-products.md` (cross-game sales disabled 2026-05-30), `private-servers.md` (price change cancels subscriptions), `subscriptions.md`
