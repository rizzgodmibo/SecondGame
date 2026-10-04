---
tags: [design/index]
status: draft
updated: 2026-10-04
confidence: high
---
# Design — Index

## TL;DR
- Start a new game at [[Genre-Playbooks]] → [[Core-Loops]] → [[Game-Design-Doc-Template]].
- Before building content, set numbers with [[Progression-Curves]] and [[Economy-Design-Sinks-And-Faucets]] and validate them with [[Balancing-Methods]].
- The first session is owned by [[Onboarding-And-First-60-Seconds]]. Every other note links there instead of repeating it.

## Notes
| Note | One-line summary |
|---|---|
| [[Core-Loops]] | Core/session/meta/social loops, text loop diagrams, genre loop table, and the loop validation test (first loop ≤ 60 s). |
| [[Progression-Curves]] | Linear/polynomial/exponential/geometric/logistic curves with formulas and worked tables, TTN targets, and a `--!strict` big-number formatter (K…Vg). |
| [[Reward-Schedules]] | FR/VR/FI/VI schedules, loot-table math, pity systems, near-miss ethics, Roblox paid-random-item rules, and weighted loot code with luck and pity. |
| [[Difficulty-And-Mastery]] | Flow and sawtooth difficulty, skill floor/ceiling, obby gap tiers, combat knobs, consented adaptive difficulty, and an assist-offer script. |
| [[Roblox Map Audit Skill]] | Claude Code skill: raycast audit of a map with real movement numbers (reachability, pits, floating parts, sight lines, overlaps, rings) |
| [[Prestige-And-Rebirth]] | When to unlock rebirth, multiplier models, the run-length law (g/m), optimal reset point, and the reset-vs-persist table. |
| [[Idle-And-Offline-Earning]] | Server-time offline gains (cap/efficiency/min), timestamp-based growth, exploit table, and return-incentive design, with code. |
| [[Economy-Design-Sinks-And-Faucets]] | Currency architecture, faucet/sink catalogues, spreadsheet model with sink ratio, inflation signals, and safe trading (GUIDs, atomic commits, PolicyService). |
| [[Balancing-Methods]] | Time-to-X targets, spreadsheet and greedy-sim balancing (code), power budgets, playtest metrics, and telemetry and A/B tuning with sample sizes. |
| [[Onboarding-And-First-60-Seconds]] | **Single home for FTUE**: first-play bounce signal, second-by-second first minute, loading rules, funnel logging code, and tutorial patterns. |
| [[Session-Length-And-Pacing]] | Playtime signal (60 min/day cap), session targets by genre, beat structure, session-end hooks, and server events. |
| [[Content-Cadence]] | Weekly update model, explore/expand, update tiers vs. effort, a 4-week pipeline, and release/announcement mechanics. |
| [[Genre-Playbooks]] | 12 genre skeletons (loop, meta, social, monetisation, pitfalls, reference games) plus a comparison table. |
| [[Game-Design-Doc-Template]] | Fill-in Roblox GDD, with each section linked to the rule note. |

## Cross-folder dependencies
- Monetisation: [[Gamepasses-vs-Developer-Products]]
- Retention: [[Retention-Metrics-D1-D7-D30]] · [[Daily-Rewards-And-Streaks]]
- Growth: [[Discovery-Algorithm]]
- Operations: [[Analytics-And-Instrumentation]] · [[Live-Ops-Playbook]]
- Systems: [[Data-Persistence-DataStores-And-ProfileStore]] · [[Anti-Exploit-And-Server-Authority]]

## Related
- [[Home]]

## Sources
- See each note's Sources section. Primary platform source: Roblox Creator Docs (github.com/Roblox/creator-docs), read 2026-10-04.
