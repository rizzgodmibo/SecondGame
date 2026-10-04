---
title: Roblox Vault Coverage and Maintenance
date: 2026-10-03
updated: 2026-10-04
tags: [roblox, vault, maintenance, research]
source: Holden ongoing vault mandate
project: null
status: reviewed
confidence: high
---
# Roblox Vault Coverage and Maintenance

## Purpose and current state

Help Claude make evidence-backed design, production, launch and growth decisions with minimal correction. This goal never completes. Navigation: [[Roblox Development Playbook]]. Conventions: [[CLAUDE]].

Initial inventory found strong project histories and art workflows, but little dedicated reusable coverage of acquisition, analytics, economy modelling, social retention or operations. This is a coverage audit, not a claim that every existing note was read or verified.

## Rotation state

**Current authority (2026-10-04):** [[Gap-Tracker]] holds the active rotation, detailed gaps and session log after the vault reorganisation. Visuals/assets is next after the Engineering boundary-validation pass. Follow its seven-domain queue and cover all seven before repeating. The coverage table and older change-log entries below preserve the earlier cycle as history; their next-step labels are not the active queue.

Track the exact subtopic and canonical note after each pass. Select the oldest or highest-impact gap within the next domain. Urgent data-loss, security, payment or policy corrections can interrupt, but resume the displaced domain next. Never repeatedly expand a favourite subject while others wait.

A six-hour thread automation was created: maintain-roblox-development-vault. Scheduled execution depends on app availability and permissions; creation is not evidence of successful future runs.

## Coverage and backlog

| Domain | Existing starting points | Required subtopics / next gaps | Latest focused pass |
|---|---|---|---|
| Engineering | [[Fish a Monster Saving and Offline Income]], [[Roblox Purchase Receipt Handling]], [[Roblox Studio MCP Quirks]], [[Rojo Workflow Gotchas]] | Luau/strict typing; module lifecycle; server/client boundaries; replication/remotes; validation/rate limiting/anti-exploit; DataStores/ProfileStore/session locking/migrations; error handling; physics/network ownership; performance/profiling; streaming; Parallel Luau; Studio MCP. Next: remote validation and mutation contracts; persistence guidance now in [[Roblox Persistence and Session Failure Runbook]]. | Persistence/session-loss runbook and local source inspection, 2026-10-03 |
| Visuals/assets | [[Blender to Roblox Asset Pipeline]], [[Art Direction Feedback]], [[Roblox Mobile UI Layout]], [[Roblox Audio Pipeline]] | UI architecture/layout/device/input scaling/accessibility/polish; icons/thumbnails; VFX/particles/beams/trails/shader capability boundaries; animation/rigging/IK/procedural motion; Blender/topology/UV/texturing/LODs/import/collision; lighting/sound/art direction. Next: BillboardGui semantics, accessibility and UI lifecycle ownership. | Mobile UI reuse audit and device acceptance matrix, 2026-10-03 |
| Game design | [[Paper Plane Toss References and Core Loop]], [[Paper Plane Toss Progression Numbers]], [[Paper Plane Toss Rebirth]] | Core loops; first 60 seconds/onboarding; progression/pacing/rewards; difficulty/mastery; prestige/rebirth; idle/offline earning; economy sinks/faucets/balance; session length/content cadence. Next: first-sixty-second onboarding, mastery and pacing. Model specification: [[Roblox Economy Modelling and Progression Tests]]. | Economy model specification, arithmetic and historical-claim audit, 2026-10-03 |
| Monetisation | [[Paper Plane Toss Monetization]], [[Roblox Purchase Receipt Handling]] | Passes/products; offers/pricing/bundles/starter packs; regional/dynamic display; platform cuts/Robux/DevEx; funnels; paid randomness/policy; pay-to-win boundaries; buyer trust; receipt recovery. Next: transaction-specific fee schedules, offer experiments and payer trust. See [[Roblox Monetisation Policy Pricing and Revenue]]. | Policy, pricing, DevEx and local purchase-path inspection, 2026-10-03 |
| Acquisition/discovery | [[Roblox Discovery and Retention Measurement]], [[Paper Plane Toss Thumbnails and Game Icon]] | Discovery signals/uncertainty; icons/thumbnails/title/description/tags; genre/positioning; sponsored ads/targeting/cost/return; organic growth/launch timing/influencer outreach. Next: metadata/search, genre positioning, share links and evidenced creator campaigns. Protocol: [[Roblox Acquisition Experiments and Ad Measurement]]. | Creative allocation, attribution and metric-definition audit, 2026-10-03 |
| Retention/social | [[Roblox Discovery and Retention Measurement]], [[Join Cutscene and Tutorial]] | First session; D1/D7/D30; daily rewards/streaks/events/seasons; friends/co-play/leaderboards; sharing/referrals; community and moderation. Next: diagnosis tree separating broken onboarding from weak return motivation. | Bootstrap basics, 2026-10-03 |
| Operations | [[Paper Plane Toss Release Prep]], [[Fish a Monster Pre-Publish Review]] | Analytics/event contracts; A/B tests; live-ops; bad launches; incident response/rollback; server scaling; moderation/policy; real-game post-mortems. Next: launch observability and rollback runbook. | Not yet |

## Evidence and freshness policy (maintenance choices)

- Recheck payments, policy, DevEx/fees, ads and discovery within 30 days, and immediately before decisions using them.
- Recheck engine APIs, libraries and pipelines within 90 days or on a version/API change. Record dependency version when inspected.
- Revisit design hypotheses after relevant playtests or experiments; otherwise inspect within 90 days. Never give universal retention or conversion targets without comparable evidence.
- Project observations are dated history; don't rewrite them as current production state. Append changed status with evidence.
- Sources failing to load remain unverified; record the gap and seek a primary alternative.
- Score readiness by evidence: missing → sourced → actionable procedure → locally tested → production observed. Note count is not a readiness score.

## Required output per pass

Read existing coverage; verify one useful gap; edit canonical notes; include decision rules, failure modes and acceptance checks; validate frontmatter, wikilinks and source claims; update this log and next domain. Save unanswered questions explicitly.

## Open corrections to investigate

- [[Roblox Mobile UI Layout]] now separates historical touch-control lookup, input heuristics and half-safe-inset tuning from verified reuse guidance. Remaining: execute the device matrix and verify BillboardGui semantics.
- [[Paper Plane Toss Monetization]] now qualifies creator ownership and per-user randomness claims. [[Roblox Monetisation Policy Pricing and Revenue]] records policy validation/enforcement and price-fallback review gaps; full purchase-path testing is pending.
- [[Paper Plane Toss Release Prep]] records a historical audit as clean. That is not a present-day guarantee; obtain build identity and test evidence before relying on it.
- Current MarketplaceService reference exposes BindReceiptHandler as well as ProcessReceipt. Investigate availability/migration separately; do not mix callback enums or silently migrate project code.
- No local Studio tests, live analytics, paid campaigns or production receipt tests were performed in the bootstrap pass.

## Change log

2026-10-04 — Engineering: updated [[Remotes-And-Networking]] and [[Anti-Exploit-And-Server-Authority]] with primary-source validation, mutation contract procedure and pending adversarial checks. No game code or runtime tests. Next: Visuals/assets; active queue in [[Gap-Tracker]].

2026-10-04 — Reconciled this legacy entry point with [[Gap-Tracker]]. Updated canonical [[Thumbnails-And-Icons]] and [[Verification-Log]]; no duplicate retention note created. Next: Engineering per the active rotation.

2026-10-03 — Acquisition/discovery: added [[Roblox Acquisition Experiments and Ad Measurement]]; separated personalisation from campaign delivery and attributed from incremental return; flagged revenue/D7 definition differences across reports. No campaign or account access. Next: retention/social diagnosis and return motivation.

2026-10-03 — Monetisation: added [[Roblox Monetisation Policy Pricing and Revenue]], verified indirect paid-randomness scope, runtime prices and multiple DevEx rates; scoped local policy/price findings without claiming compliance. Updated historical project assertions. Next: acquisition/discovery creative experiments and ad measurement.

2026-10-03 — Game design: created [[Roblox Economy Modelling and Progression Tests]]; checked illustrative calculations; corrected rebirth arithmetic and clarified cumulative XP; qualified historical simulator times. No new game simulation or code changes. Next: monetisation policy and net-revenue definitions.

2026-10-03 — Visuals/assets: updated [[Roblox Mobile UI Layout]] in place with PreferredInput guidance, interactive safe-area guidance, scoped historical assumptions, source inspection and ten-case device matrix. No code changes or new runtime tests. Next: game design economy worksheet specification.

2026-10-03 — Engineering: added [[Roblox Persistence and Session Failure Runbook]], verified ProfileStore 1.0.3 in the local project, identified custom-cancellation timeout gap and post-migration setup failure boundary for review. Documentation/source inspection only; no game changes or runtime tests. Next: visuals/assets mobile UI assumptions and device test matrix.

2026-10-03 — Created missing conventions entry point and playbook; inventoried seven domains; corrected receipt-cache guarantee and load-wait wording; added sourced discovery/retention basics; created six-hour maintenance automation. Next: engineering persistence/session-loss runbook.

## Sources

- Holden's instructions and ongoing mandate in this chat, 2026-10-03.
- Local vault inventory and linked notes, read or indexed 2026-10-03; topic-specific verification is recorded in each researched note.





