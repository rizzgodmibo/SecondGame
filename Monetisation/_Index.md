---
tags: [monetisation/index]
status: draft
updated: 2026-10-04
confidence: high
---
# Monetisation — Index

## TL;DR
- Start with [[Monetisation-Design-Checklist]] before launch, and [[Monetisation-Mistakes]] before any change to paid content.
- The receipt handler is the highest-risk code in the game: [[ProcessReceipt-Handling]].
- 2025–2026 platform changes that make older guides wrong:
  - **DevEx is $0.0038/R$** (since 2025-09-05), with **$0.0054** for U.S. 18+ eligible purchases (since 2026-06-08).
  - **Premium Payouts became Creator Rewards** (2025-07-24).
  - **Premium became Roblox Plus** (2026-04-30).
  - **Managed Pricing** (regional pricing + price optimization) is the default.
  - **Cross-game pass/product sales were disabled on 2026-05-30.**
  - `BindReceiptHandler` was added as an alternative to `ProcessReceipt`.
- Revenue formula: DAU × payer conversion × ARPPU × 0.7 × $0.0038. Fix conversion first.

## Notes

| Note | Use it when |
|---|---|
| [[Gamepasses-vs-Developer-Products]] | Choosing item types; MarketplaceService APIs, ownership caching, prompting, gifting |
| [[ProcessReceipt-Handling]] | Writing or reviewing receipt code (idempotent, ProfileStore-safe) |
| [[Pricing-Psychology]] | Setting prices, ladders, anchors; Managed Pricing |
| [[Bundles-And-Starter-Packs]] | Designing first-purchase and limited-time offers |
| [[Robux-Economy-DevEx-And-Platform-Cuts]] | Revenue shares, DevEx, Creator Rewards, ads, Robux→USD math |
| [[Subscriptions-And-Premium-Payouts]] | Experience subscriptions, Roblox Plus/Premium perks, what replaced Premium Payouts |
| [[Conversion-Funnels]] | KPIs, benchmarks, prompt placement, analytics events |
| [[Pay-To-Win-Boundaries]] | Power vs cosmetics by genre; paid random items and odds disclosure |
| [[Monetisation-Mistakes]] | Anti-patterns and real backlash cases |
| [[Monetisation-Design-Checklist]] | Pre-launch go/no-go |

## Cross-folder dependencies
- [[Economy-Design-Sinks-And-Faucets]]: currency design that the shop sells into
- [[Data-Persistence-DataStores-And-ProfileStore]]: session locking that receipt idempotency depends on
- [[Analytics-And-Instrumentation]] · [[AB-Testing]]: measuring and testing offers
- [[Moderation-And-Policy-Compliance]]: odds disclosure, the Maturity questionnaire, ads policy
- [[Genre-Playbooks]]: what monetises in each genre

## Open verification items
See `⚠️ verify:` markers in each note. Key ones:
- Optional Plus Robux bundles
- The current Robux pack table per platform
- The fate of legacy Premium after 2026
- Third-party conversion and ARPDAU benchmarks
- ProfileStore member names

## Related
- [[Home]]

## Sources
- Roblox creator-docs snapshot 2026-10-02 (https://github.com/Roblox/creator-docs), mirrored at https://create.roblox.com/docs/production/monetization (accessed 2026-10-04)
