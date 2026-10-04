---
tags: [meta/playbook]
status: reviewed
updated: 2026-10-04
confidence: medium
---
# Game-Building Playbook (end-to-end order of work)

## TL;DR
- Validate the **idea and thumbnail** before building systems: discovery is gated by click-through and early retention, not code quality.
- Build the **core loop vertical slice in ≤2 weeks**, playtest, then add meta progression and monetisation.
- Ship with **data safety, receipt idempotency and analytics** in place on day one — these cannot be retrofitted after a wipe.
- Launch small, read the funnel (CTR → play-through → D1 → payer conversion), fix the weakest stage first, then spend on ads.

## Phases and gates
| # | Phase | Output | Gate to pass before next phase | Notes |
|---|---|---|---|---|
| 0 | Concept | 1-line pitch, genre gap, 3 mock thumbnails | Pitch fits a proven genre with a twist; thumbnail readable at 150px | [[Genre-Positioning]], [[Thumbnails-And-Icons]] |
| 1 | GDD | Filled [[Game-Design-Doc-Template]] | Core loop explainable in one sentence; first reward < 60s | [[Core-Loops]], [[Onboarding-And-First-60-Seconds]] |
| 2 | Bootstrap | Repo + Rojo + data/remotes/analytics layers | [[Project-Bootstrap-Checklist]] complete | [[Module-Architecture]] |
| 3 | Vertical slice | Playable core loop, placeholder art | Testers voluntarily play ≥10 min | [[Balancing-Methods]] |
| 4 | Meta + economy | Progression, currencies, rebirth | Spreadsheet sim gives target time-to-X | [[Progression-Curves]], [[Economy-Design-Sinks-And-Faucets]] |
| 5 | Polish + art | Art pass, UI juice, VFX, audio | Screenshots are thumbnail-worthy | [[Art-Direction]], [[UI-Polish-And-Juice]] |
| 6 | Monetisation | Passes, products, starter pack | [[Monetisation-Design-Checklist]] complete | [[ProcessReceipt-Handling]] |
| 7 | Soft launch | Public, small ad spend / friends | Funnel metrics meet [[KPI-Dashboard-Spec]] floors | [[Launch-Checklist]] |
| 8 | Launch | Ads, influencer push, update cadence | D1 and play-through above floors before scaling ads | [[Sponsored-Ads-And-Paid-Acquisition]] |
| 9 | Live-ops | Weekly updates, events | Retention steady or rising | [[Live-Ops-Playbook]], [[Events-And-Seasons]] |

## Diagnose-first rule
When numbers are bad, fix in funnel order: **impressions → CTR → play-through → session length → D1 → D7 → payer conversion → ARPPU**. See [[Bad-Launch-Response]].

## Related
- [[Home]] · [[Gap-Tracker]] · [[Roblox Game Manager Skill]] (Claude Code skill that runs this playbook phase by phase, with gates and evidence)
