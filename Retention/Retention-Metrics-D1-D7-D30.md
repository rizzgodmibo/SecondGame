---
tags: [retention/metrics]
status: draft
updated: 2026-10-04
confidence: medium
---
# Retention Metrics: D1, D7, D30

## TL;DR
- **D1, D7 and D30 are cohort metrics keyed to the first play date.** D1 is the share of new users who first played on date X and came back the next day. D7 is the share who came back on day 8 (Day 7), and D30 the share who came back on day 31 (Day 30). They measure **new-user** retention only. Returning-player health needs other metrics (play days per user, DAU/MAU).
- **Benchmark against your "similar games" band, not against folklore.** The dashboard shows the 50th–90th percentile of games with similar players (needs 100+ DAU). Roblox's own docs example is D1 p50 12.11% / p90 18.73%. GameAnalytics' 2026 Roblox report gives a platform median of **D1 10.3%, D7 1.6%, D30 0.5%** and a p99 of **D1 22.2%, D7 9.1%, D30 4.7%**. ⚠️ verify: GameAnalytics figures come from a search snippet; the page could not be fetched.
- **Working targets for a scale-ready game:** D1 ≥ 15%, D7 ≥ 4%, D30 ≥ 1.5%. Hitting your similar-games p90 counts as "great". Do not buy ads or run influencer pushes until D1 and average session time are at least at your p50 (Roblox's own guidance).
- **Each metric has its own lever.** D1 depends on the core loop, the FTUE and performance ([[Onboarding-And-First-60-Seconds]], [[Core-Loops]]). D7 depends on progression and short/mid-term goals. D30 depends on endgame, social systems and update cadence ([[Content-Cadence]], [[Live-Ops-Playbook]]).
- **A dip in all three curves on one cohort date means an acquisition-mix shift**, such as a traffic spike, an ad burst or a front-page feature. It is not a regression. A dip that starts on a date and persists across later cohorts means you shipped a regression.
- Recommended-for-You ranks on the **retention of users who arrived via Recommended**. Ad, friend and search users are excluded from that stage ([[Discovery-Algorithm]]). Always segment retention by acquisition source.

## Definitions (as in the Creator Dashboard)
| Metric | Dashboard definition | Matures after | Primary lever |
|---|---|---|---|
| D1 retention | % of new users who first played on date X and **returned the next day** | 1 day | Core loop clarity, FTUE ≤ 5 min to fun, performance/crashes |
| D7 retention | % of new users who return on the **8th day (Day 7)** | 7 days | Progression system, short + long goals, content variety, difficulty balance |
| D30 retention | % of new users who return on the **31st day (Day 30)** | 30 days | "Ending system": endgame, social mechanics (trading, parties, guilds, PvP, leaderboards), regular updates |
| New-user first-session retention | % of new users still in game X minutes after first join (Engagement page) | same session | First 60 s / 5 min ([[Onboarding-And-First-60-Seconds]]) |
| Average session time | Total time / number of sessions | — | Session loop length ([[Core-Loops]]) |
| Play days per user (D1, D2–D7, D8–D28) | Discovery signal charts | — | Habit loops: dailies, streaks, notifications |
| Intentional co-play days per user | Unique days users return to play **with friends** (join, invite, private server) | — | [[Friend-And-Group-Play]] |

Notes:
- The x-axis of each retention chart is the **cohort's first play date**. The most recent 7 days of D7 and the most recent 30 days of D30 are empty by design.
- The cohort table shows **daily cohorts** (first 10 days) and **weekly cohorts** (Mon–Sun, 10 weeks). Each cohort carries 7D playtime/user, 7D payer conversion, and 7D and 30D revenue/user. Use these to judge whether event-acquired cohorts are worth more.
- Day boundary: the docs do not state the timezone. ⚠️ verify: assume UTC calendar days, so "returned next day" means any session on the next UTC date. A player who first plays at 23:50 UTC and returns at 00:10 UTC counts toward D1.
- Analytics access requires the game to have had 10+ DAU over the past 7 days. Benchmarks require 100+ DAU.

## Benchmarks
| Source (date) | D1 | D7 | D30 | Notes |
|---|---|---|---|---|
| Roblox docs example, similar-games band (2026-10) | p50 12.11% / p90 18.73% | — | — | Illustrative example in the docs. Your own band is on the dashboard. |
| Roblox DevForum example (2023 benchmark launch) | p50 12.4% / p90 24.1% | — | — | ⚠️ verify: example from the "Similar Experience Benchmarks" announcement |
| GameAnalytics 2026 Roblox report | median 10.3%, p25 8.4%, p99 22.2% | median 1.6%, p25 1.0%, p99 9.1% | median 0.5%, p25 0.3%, p99 4.7% | GameAnalytics SDK games only, skewed toward smaller studios. ⚠️ verify |
| GameAnalytics 2025 Roblox report | D1 median rises with session length: ~4.3% (1–3 min sessions) → ~10.2% (13–24 min sessions) | — | — | Short sessions predict low D1. ⚠️ verify |

**Decision rules**
- D1 < your p50 → do not scale traffic. Fix FTUE, performance and core-loop payoff first.
- D1 ≥ p50 but D7/D1 < 0.2 → the progression runs out or stalls by day 3–5. Add mid-term goals, dailies and a collection/index ([[Daily-Rewards-And-Streaks]]).
- D7 healthy but D30/D7 < 0.25 → there is no endgame. Add social systems, leaderboards, events and a weekly update rhythm ([[Events-And-Seasons]], [[Leaderboards]]).
- Treat community blog targets such as "good D1 = 20%, great = 30–40%" as aspirational. They are top-chart numbers and unsourced. Use the dashboard band.

## Diagnosing drop-off
1. **Segment first:** acquisition source (Recommended vs ads vs friends vs search), platform (phone/PC/console/tablet), new vs returning, country. The Acquisition page shows D7 retention by source and platform.
2. **Check performance:** crash rate, client memory, FPS, error report after every release (Analytics → Performance/Crashes). Low-end-phone crashes show up as a D1 drop concentrated on phones.
3. **Funnel the first session:** instrument each FTUE step with `AnalyticsService:LogOnboardingFunnelStepEvent` and find the biggest step-over-step loss ([[Analytics-And-Instrumentation]]).
4. **Progression distribution:** log level/zone reached (`LogProgressionEvent` / custom events) and look for a cliff, i.e. a level where many players stop.
5. **Cohort compare:** compare the cohort before and after the update date in the cohort table. If only the post-update cohort dropped, roll back or hotfix.
6. **Recommendation signals:** impressions usually fall after play-through rate, play days per user or playtime per user drops, or after first-play bounce rate rises. Check D1, D2–D7 and D8–D28 windows separately.

| Symptom | Likely cause | First fix |
|---|---|---|
| All 3 curves dip on one date, then recover | Traffic spike with a lower-intent mix | None. Annotate it. |
| D1 drops after an update and stays low | FTUE or perf regression | Roll back, then diff the funnel |
| D1 fine, D7 poor | Content runs out / no reason to return | Dailies, streaks, quests, an egg/zone ladder |
| D7 fine, D30 poor | No endgame / social | Leaderboards, trading, guilds, events, updates every 2–4 weeks |
| Phone-only drop | Memory/perf/UI scaling | Mobile perf pass |
| Ads cohort much worse | Wrong audience/creative | Retarget. Organic ranking ignores ads users. |

## Checklist
- [ ] Dashboard benchmark band noted in project doc (D1/D7/D30 p50 and p90, date)
- [ ] Onboarding funnel + progression events instrumented before launch
- [ ] Retention reviewed weekly by acquisition source and platform
- [ ] Each update annotated (date) to read cohort impact
- [ ] Scaling gate: D1 ≥ p50 and session time ≥ p50 before paid traffic

## Pitfalls
- Reading D7/D30 for the last 7/30 days. Those cohorts are immature or empty.
- Optimising blended retention when ranking uses Recommended-sourced users only.
- Comparing yourself to front-page games. Compare against your similar-games set.
- Inflating D1 with login-only rewards. Players who come back just to claim and leave raise D1 but not playtime, and the algorithm also weighs playtime and qualified sessions.
- Changing several systems in one update, which leaves no way to attribute the cohort change.

## Related
- [[Retention/_Index]] · [[Onboarding-And-First-60-Seconds]] · [[Core-Loops]] · [[Discovery-Algorithm]] · [[Analytics-And-Instrumentation]] · [[Live-Ops-Playbook]] · [[Content-Cadence]] · [[Retention-Checklist]]

## Sources
- Roblox Creator Docs, "Retention", https://create.roblox.com/docs/production/analytics/retention (read via github.com/Roblox/creator-docs mirror, commit 2026-10-02; accessed 2026-10-04)
- Roblox Creator Docs, "Analytics dashboard → Benchmarking", https://create.roblox.com/docs/production/analytics/analytics-dashboard (accessed 2026-10-04)
- Roblox Creator Docs, "Analytics" overview and "Acquisition", https://create.roblox.com/docs/production/analytics (accessed 2026-10-04)
- Roblox Creator Docs, "Discovery", https://create.roblox.com/docs/discovery (accessed 2026-10-04)
- GameAnalytics, "2026 Roblox Benchmark Report", https://www.gameanalytics.com/reports/2026-roblox-report (search snippet only, 2026-10-04)
- GameAnalytics, "2025 Roblox Benchmark Report", https://www.gameanalytics.com/reports/2025-roblox-report (search snippet only, 2026-10-04)
- DevForum, "Analytics [Similar Experience Benchmarks & Broader Access]", https://devforum.roblox.com/t/analytics-similar-experience-benchmarks-broader-access/2210285
