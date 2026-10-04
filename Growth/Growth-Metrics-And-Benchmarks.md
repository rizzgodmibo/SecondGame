---
tags: [growth/metrics, operations/analytics]
status: draft
updated: 2026-10-04
confidence: medium
---
# Growth Metrics and Benchmarks

## TL;DR
- **Benchmark against Roblox's own "similar games" percentiles** in Creator Analytics (Home Recommendations tab, Overview, Retention). Absolute "good numbers" from the internet are rough guides only. Roblox publishes **no official absolute targets**.
- Top-of-funnel KPIs, in order: **RFY impressions → Play-through rate (PTR) → First-play bounce (<60 s, 61–180 s) → D1 playtime/play days → D2–7 → D8–28**. These are the official RFY signals since 2026-06-15.
- **The algorithm is picking you up when:** Home Recommendations impressions grow day-over-day for 3+ days, "Home recommendations" becomes your **#1 new-user source (>50% of new users)**, and PTR and bounce hold near benchmark while impressions scale. Falling impressions with stable signals usually means seasonality or competitors (official).
- Use **cohort-by-source** views (Acquisition: conversion rate, D7, 7D playtime, 30D payer conversion, 30D revenue/user per source). Never judge organic health from blended DAU that includes ads or influencer spikes.
- CCU milestones are vanity until retention backs them. A rough ladder: **25 → 100 → 1k → 10k → 100k CCU**. Each step up usually needs both an RFY expansion and a retained cohort ⚠️ verify (heuristic).

## Details

### Metric dictionary (official definitions)
| Metric | Definition | Where |
|---|---|---|
| **Impressions (Home Recs)** | Times your tile was shown in Recommended For You | Acquisition → Home Recommendations |
| **PTR** | Rate users play after seeing you in RFY; first session of RFY-acquired users only | Home Recs tab |
| **First-play bounce rate** | Share of RFY first sessions ending early; buckets <60 s and 61–180 s; negative signal | Home Recs tab |
| **QPTR** | Qualified plays ÷ impressions (qualified excludes accidental and quick bounces); still used in **thumbnail personalization**; **removed from RFY ranking 2026-06** | Thumbnails → Home Page tab |
| **Play days / user** | Avg unique days played: D1, D2–7 (out of 6 days), D8–28 | Home Recs tab |
| **Playtime / user** | Avg minutes, **capped at 60 min per user per day** for the signal | Home Recs tab |
| **Intentional co-play days, qualified sessions, spend days, Robux spent / user** | Secondary RFY signals | Home Recs tab |
| **Conversion rate (Acquisition)** | % of new users who played after an impression, per source | Acquisition |
| **D7 retention** | % of new players who played again on day 8 after their first session | Acquisition / Retention |
| **7D playtime/user, 30D payer conversion, 30D revenue/user** | Cumulative per new-user cohort, per source / share link | Acquisition |
| **CPP / ROAS** | Ad cost per play; earnings ÷ spend | Ads Manager |
| **Creator Rewards** | Daily rewarded active spenders (50th–90th pct benchmark shown), rewarded signups | Monetization → Creator Rewards |

### Rough absolute heuristics (community, NOT official; always prefer your benchmark percentiles) ⚠️ verify all
| Metric | Weak | OK | Strong | Notes |
|---|---|---|---|---|
| Icon/thumbnail CTR (Ads Manager clicks ÷ impressions) | <1.5% | 2–3% | >4% | Third-party guides cite "3%+ good" ⚠️ verify |
| First-play bounce <60 s | >40% | 25–40% | <20% | Genre-dependent; story/horror differ |
| D1 retention | <8% | 10–15% | >20% | Simulators/obbies lower; social RP and competitive higher |
| D7 retention | <3% | 4–7% | >10% | |
| Avg session length | <6 min | 8–15 min | >20 min | Signal capped at 60 min/day |
| Payer conversion (30D) | <1% | 2–4% | >5% | |
| 30D revenue / new user | — | — | > ad CPP in USD | The break-even rule for ads |

### Interpreting the curve
| Pattern | Meaning | Action |
|---|---|---|
| Impressions ↑ for 3–7 days after an update; PTR dips slightly, bounce stable | **Explore phase working** (official: a PTR dip on impression growth is normal) | Hold changes. Prepare the next patch |
| Impressions ↑ then ↓ to below the prior baseline within a week | New cohort didn't retain (D1/D2–7 ↓) | Check the update's first-session changes and bugs |
| Impressions ↓, signals stable | Seasonality (weekday/back-to-school) or competitors improved more | Compare with the same weekday last week; look at benchmarks |
| Impressions ↓ after an ad campaign | Ad users counted as "already acquired" (official, not a penalty) | Look at total new users, not RFY alone |
| PTR ↓, bounce ↑ after a thumbnail change | Thumbnail mis-sells | Include the old winner; revert |
| D1 fine, D8–28 ↓ | No long-term hooks | Collections, social goals, events. See [[Retention-Metrics-D1-D7-D30]] |
| Banner "reduced exposure" on dashboard | Quality or uniqueness flag | Fix metadata or uniqueness; it is re-evaluated daily |

### CCU milestone ladder (heuristic) ⚠️ verify
| CCU | What it usually means | Next lever |
|---|---|---|
| <25 | Not yet in meaningful RFY rotation; friends and testers only | Seed traffic (ads, shorts), fix the first 60 s |
| 25–100 | RFY testing you with small cohorts | Raise D1 and play days; ship a weekly update |
| 100–1k | Expanding cohorts; Up-and-Coming possible | Influencers plus update stacking; ≥100 DAU also unlocks Creator Rewards Audience Expansion (avg over 60 d) |
| 1k–10k | Charts presence (genre sorts, Top Trending) | Live-ops cadence, monetisation depth, Earnings ads |
| 10k–100k+ | Top-tier distribution; competing on relative signals | Events, collaborations, localisation |
Platform context: Roblox had 123M DAU in Q2 2026. Record single-game peaks are Steal a Brainrot 25.87M CCU (2025-10-11) and Grow a Garden 22.35M (2025-08-23).

### Weekly growth review (template)
1. New users by source (Home Recs / Search / Charts / Sponsored / Search ads / Other / share links), week over week.
2. Home Recs: impressions, PTR, bounce (both buckets), D1/D2–7/D8–28 days and playtime vs benchmark percentile.
3. Thumbnail table: QPTR and avg playtime per active thumbnail.
4. Paid: CPP, ad-cohort D1 vs organic, ROAS (closed windows only).
5. Decision: what single change ships next week, and which metric it targets.

## Checklist
- [ ] Custom analytics funnel for onboarding steps ([[Analytics-And-Instrumentation]]).
- [ ] Weekly review scheduled; snapshots saved in `Projects/<name>/`.
- [ ] Benchmarks recorded (percentile per signal) at launch, D30 and D90.
- [ ] Alerts on error rate and CCU drops (Analytics → Alerts).

## Pitfalls
- Optimising QPTR or CTR alone. Since 2026-06, bounce and play days dominate.
- Comparing against mega-hits rather than the similar-games benchmark.
- Treating one Saturday spike as an "algorithm pick-up". Use 7-day moving averages.
- Mixing ad cohorts into organic retention readings.

## Related
- [[Growth/_Index]] · [[Discovery-Algorithm]] · [[Thumbnails-And-Icons]] · [[Sponsored-Ads-And-Paid-Acquisition]] · [[Launch-Checklist]]
- [[Retention-Metrics-D1-D7-D30]] · [[Analytics-And-Instrumentation]] · [[AB-Testing]] · [[Onboarding-And-First-60-Seconds]]

## Sources
- Roblox Creator Docs, *Discovery* (signals, time segments, 60-min cap, explore/expand): https://create.roblox.com/docs/discovery (GitHub mirror 2026-10-02)
- Roblox Creator Docs, *Discovery FAQ*: https://create.roblox.com/docs/discovery-faq
- Roblox Creator Docs, *Acquisition*: https://create.roblox.com/docs/production/analytics/acquisition
- Roblox Creator Docs, *Thumbnails* (QPTR table): https://create.roblox.com/docs/production/publishing/thumbnails
- Roblox Creator Docs, *Creator Rewards* (benchmarks; 100 DAU rule): https://create.roblox.com/docs/creator-rewards
- Roblox Q2 2026 Shareholder Letter (123M DAU): https://s27.q4cdn.com/984876518/files/doc_financials/2026/q2/Roblox-Q2-2026-Earnings-Shareholder-Letter.pdf
- Guinness World Records (Steal a Brainrot CCU): https://www.guinnessworldrecords.com/world-records/503322-most-concurrent-players-for-a-videogame-made-in-roblox
- Third-party CTR heuristic (unverified): https://rowatcher.com/news/roblox-ads-in-2026-the-break-even-math-small-devs-ignore
