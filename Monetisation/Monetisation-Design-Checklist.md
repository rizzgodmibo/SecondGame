---
tags: [monetisation/checklist]
status: draft
updated: 2026-10-04
confidence: high
---
# Monetisation Design Checklist (Pre-Launch)

## TL;DR
- Run this list top to bottom before the first public release, and again before any major update that touches the shop.
- Hard blockers (ship nothing until done): **idempotent receipt handler**, **no hard-coded prices**, **odds disclosure + PolicyService gating**, **paid entitlements survive migrations**.
- Revenue levers to have at launch: a 2–4 pass core set, one currency ladder, a starter pack, a contextual wall offer, a rewarded-ad button (if eligible), a Plus prompt, and Share Links.
- Instrumentation must be live on day 1, because you can't recover funnel data after the fact.

## 1. Accounts and eligibility (week −4)
- [ ] ID-verified owner account + 2FA (needed for ads, Audience Expansion rewards, local-currency subscriptions)
- [ ] DevEx portal set up and tax form (W-9/W-8) filed. 13+ ([[Robux-Economy-DevEx-And-Platform-Cuts]])
- [ ] Group game: the revenue-permission member meets the same requirements
- [ ] Maturity & Compliance Questionnaire submitted and approved (ads eligibility; paid random items declared). See [[Moderation-And-Policy-Compliance]]
- [ ] Decided R15-only vs R6 with the **U.S. 18+ DevEx rate ($0.0054)** in mind

## 2. Catalogue design
- [ ] Each perk mapped to pass / product / subscription ([[Gamepasses-vs-Developer-Products]])
- [ ] 2–4 core passes (e.g. 2× currency, VIP, auto-collect, extra slots) whose perks you can honour **forever**
- [ ] Currency ladder 4–6 rungs with monotonic value per R$ ([[Pricing-Psychology]])
- [ ] Starter pack (one-time, 49–149 R$, ≥5× value) + second-purchase + wall-breaker offers ([[Bundles-And-Starter-Packs]])
- [ ] Optional subscription with daily-felt benefits; local currency where available ([[Subscriptions-And-Premium-Payouts]])
- [ ] Private server price decided and **fixed** (changing it cancels subscriptions)
- [ ] One pass designed for Buy Robux page promotion (50–800 R$, no random items)
- [ ] Avatar items / UGC shop considered (40% affiliate commission)
- [ ] P2W review per mode ([[Pay-To-Win-Boundaries]]); no tactical subscriber/Plus perks
- [ ] Max 1 soft + 1 premium currency ([[Economy-Design-Sinks-And-Faucets]])

## 3. Engineering (blockers)
- [ ] Exactly one `ProcessReceipt` (or deliberate `BindReceiptHandler` routing); PurchaseId log saved atomically with goods; `PurchaseGranted` only after a durable save ([[ProcessReceipt-Handling]])
- [ ] Legacy product IDs kept in the grant table forever
- [ ] Tests passed: buy → kick → rejoin; buy → server hop; buy while data is still loading; Store-tab purchase in **test mode** (real Robux)
- [ ] Pass ownership checked server-side at join (batched, retried); perks apply mid-session without a rejoin
- [ ] All prices come from `GetProductInfoAsync` on the client; **Dynamic Price Check** passed (Price pinned + Location pinned)
- [ ] Managed Pricing enabled. If items are tradeable or giftable: `GetUsersPriceLevelsAsync` gating + `IsPaidItemTradingAllowed`
- [ ] Paid random items: full odds list with % before purchase, live boosted odds, `ArePaidRandomItemsRestricted` treatment, fail closed
- [ ] Rewarded video ads: dev-product reward, `GetAdAvailabilityNowAsync` checked at shop open, damage paused during ads, non-random reward
- [ ] Immersive ad units hidden for `AreAdsAllowed == false` users if fallbacks look bad
- [ ] Plus prompt (`PromptRobloxSubscriptionPurchase`) rewards only after `HasRobloxSubscription` changes
- [ ] Data migrations never touch `PurchaseIds` or paid entitlements; a backup/versioning plan exists ([[Data-Persistence-DataStores-And-ProfileStore]])
- [ ] Purchase support log (UserId, PurchaseId, ProductId, CurrencySpent, time)

## 4. UX and placement
- [ ] Persistent shop button; Roblox Shop (`ExperienceShop`) left enabled unless you have a reason
- [ ] ≤1 unsolicited prompt per session; none in the first 3 min, during combat, or while trading
- [ ] Contextual prompts at walls, inventory-full and locked areas
- [ ] Every item shows its contents clearly; bundle "Worth X" values computed from live prices
- [ ] Countdowns are server-authoritative and real
- [ ] Gifting flow (if any) is rate-limited and announced socially

## 5. Analytics ([[Analytics-And-Instrumentation]], [[Conversion-Funnels]])
- [ ] Shop funnel: Opened → Viewed → Prompted → Purchased (custom fields: source, itemId)
- [ ] `LogEconomyEvent` for all currency sources and sinks; Robux-bought currency tagged `IAP` with SKU
- [ ] `RobuxSpent` custom event with `CurrencySpent`; `FirstPurchase` event; AdReward excluded
- [ ] Offer impressions logged with `offerId`; wall hits logged with `gateId`
- [ ] Target KPIs written down: daily conversion ≥2%, ARPDAU, D1/D7 not harmed by monetisation tests
- [ ] [[AB-Testing]] plan for the first 3 monetisation experiments (starter pack price, prompt timing, ladder bonuses)

## 6. Growth-linked revenue
- [ ] Share Links created for every off-platform channel (Audience Expansion: 35% of new/reactivated users' first $100)
- [ ] A daily "first game of the day" hook (Daily Engagement reward: 5 R$ per Active Spender) — see [[Genre-Playbooks]]

## 7. Live-ops guardrails
- [ ] Pre-change checklist from [[Monetisation-Mistakes]] adopted (no nerfs or wipes of paid content without grandfathering)
- [ ] Patch notes template includes odds changes and compensation
- [ ] DevForum Announcements watched weekly (monetisation rules changed many times in 2025–2026)

## Pitfalls
- Launching "monetisation later": products added after launch without funnels give you no baseline.
- Testing only in Studio: test purchases don't exercise real failure modes. Use a live private server with low-price products.
- Over-scoping the catalogue: 30 products at launch spread attention thin. Start with about 10 SKUs.

## Related
- [[Monetisation/_Index]] · all notes in this folder
- [[Analytics-And-Instrumentation]] · [[AB-Testing]] · [[Moderation-And-Policy-Compliance]] · [[Data-Persistence-DataStores-And-ProfileStore]] · [[Economy-Design-Sinks-And-Faucets]] · [[Genre-Playbooks]]

## Sources
- Compiled from the notes in this folder. Primary source is Roblox creator-docs (snapshot 2026-10-02, https://create.roblox.com/docs/production/monetization, accessed 2026-10-04). See each linked note for item-level citations.
