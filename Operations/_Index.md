---
tags: [operations/index]
status: reviewed
updated: 2026-10-04
confidence: high
---
# Operations Index

## TL;DR
- Operations covers running the game after code is written: **measure → decide → ship → protect**.
- Before launch, read [[Analytics-And-Instrumentation]] (instrument everything), [[Moderation-And-Policy-Compliance]] (questionnaire, filtering, PolicyService, Kids/Select gate) and [[Server-Scaling-And-Matchmaking]] (server size, teleports).
- At launch and after, use [[KPI-Dashboard-Spec]] daily, [[Bad-Launch-Response]] when numbers are off, and [[Live-Ops-Playbook]] weekly.
- For improvement, run [[AB-Testing]] using native Experiments and Configs. Learn from [[Post-Mortems-Real-Games]].
- For people and money, see [[Team-And-Budget]].

## Notes
| Note | Use when |
|---|---|
| [[Analytics-And-Instrumentation]] | Setting up AnalyticsService funnels, economy, progression and custom events; limits; taxonomy; external analytics |
| [[KPI-Dashboard-Spec]] | Daily and weekly metric review; target bands; the action each metric triggers |
| [[AB-Testing]] | Roblox Experiments/Configs, DIY deterministic bucketing, sample size, what to test first |
| [[Live-Ops-Playbook]] | Weekly rhythm, update day, server restarts, versioning, feature flags, hotfixes, admin commands |
| [[Bad-Launch-Response]] | Triaging CTR, onboarding, retention and monetisation problems; data-loss incidents; rollbacks; pivot or relaunch |
| [[Server-Scaling-And-Matchmaking]] | MaxPlayers, server fill, places, reserved servers, MessagingService and MemoryStore limits, queue matchmaking |
| [[Moderation-And-Policy-Compliance]] | Community Standards, maturity labels, age checks, text filtering, PolicyService, bans, UGC, links, DMCA |
| [[Post-Mortems-Real-Games]] | Lessons from Grow a Garden, Steal a Brainrot, Adopt Me, Doors, PS99, DTI, Blox Fruits, Frontlines, data incidents |
| [[Team-And-Budget]] | Solo vs team, contractor rates, revenue splits and group payouts, DevEx value, IP protection |

## Launch-week reading order
1. [[Moderation-And-Policy-Compliance]]: complete the questionnaire and decide the Kids/Select path
2. [[Analytics-And-Instrumentation]]: confirm events arrive in View Events
3. [[Live-Ops-Playbook]]: set up the staging place, flags and restart procedure
4. [[KPI-Dashboard-Spec]]: record baseline benchmarks
5. [[Bad-Launch-Response]]: keep it open for the first 72 hours

## Cross-folder links
- [[Launch-Checklist]] · [[Content-Cadence]] · [[Discovery-Algorithm]] · [[Growth-Metrics-And-Benchmarks]]
- [[Retention-Metrics-D1-D7-D30]] · [[Conversion-Funnels]] · [[Pay-To-Win-Boundaries]] · [[Data-Persistence-DataStores-And-ProfileStore]]

## Verification status
Most API limits and policies here were checked on 2026-10-04 against the official Roblox `creator-docs` GitHub repo (commit 9f840b1, 2026-10-02), which is the source for create.roblox.com/docs. Claims about rates, case-study numbers and third-party benchmarks are marked `⚠️ verify`.

## Related
- [[Home]]

## Sources
- https://github.com/Roblox/creator-docs (commit 9f840b1, 2026-10-02)
