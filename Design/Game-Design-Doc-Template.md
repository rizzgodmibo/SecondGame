---
tags: [design/gdd, template]
status: draft
updated: 2026-10-04
confidence: high
---
# Game Design Doc Template (Roblox)

## TL;DR
- Copy everything below the line into `Projects/<GameName>/GDD.md` and fill every `<…>`. Leave nothing blank: write "N/A + why" instead.
- Fill sections **in order**: 1–4 lock the concept, 5–9 make it buildable, 10–14 make it launchable. Do not build content until sections 1–6 pass review.
- Each section links to the vault note with the rules for it. Read that note before filling the section.
- Keep the GDD **≤ 8 pages**. Detail goes in linked spec notes in `Projects/<GameName>/`.

## How to use
- One GDD per game. Version it with an "Updated" date and a changelog at the bottom.
- Numbers go in tables with their target and source ("sim", "telemetry", "guess ⚠️").
- After launch, the GDD becomes the decision log. Every change records a reason and a metric.

---

```markdown
---
tags: [project/<game-slug>, design/gdd]
status: draft
updated: YYYY-MM-DD
confidence: low
---
# <Game Name> — GDD

## 0. One-liner
"<Verb> <things> to <goal>, with <twist>." (≤ 20 words)
Elevator pitch for a 10-year-old: <one sentence>

## 1. Pillars (max 3)
| Pillar | Means we do | Means we don't |
|---|---|---|
| <e.g. Satisfying collection> | <juicy hatch, visible pets> | <text-heavy menus> |

## 2. Audience & market  → [[Genre-Playbooks]] [[Discovery-Algorithm]]
- Genre / sub-genre: <…>   Reference games (3): <…>   Our twist (why we're not a copy): <…>
- Target age band / devices: <e.g. 9–14, 70% mobile> ⚠️ verify with analytics after launch
- Trend timing: <rising / peaked / evergreen> + evidence (CCU trend links)

## 3. Core loops  → [[Core-Loops]]
- Core (10–60 s): Action <…> → Reward <…> → Upgrade <…> (stat changed: <…>)
- Session (5–30 min) goal: <…>
- Meta (days–weeks): <…>
- Social loop: <trade / co-op / steal / show-off / rate>
- Text diagram:
  [<action>] -> [<reward>] -> [<upgrade>] -> back to [<action>]

## 4. First session  → [[Onboarding-And-First-60-Seconds]]
| Time | Player sees/does | Funnel step # |
|---|---|---|
| 0–5 s | <spawn view, one button> | 1–3 |
| ≤15 s | <first reward> | 4 |
| ≤60 s | <first purchase> | 5 |
| 3–10 min | <first big moment> | 6–7 |
| session end | <joy moment + hooks> | 8 |
Deferred until later: <shop, dailies, trading…>

## 5. Progression  → [[Progression-Curves]] [[Prestige-And-Rebirth]]
| Line | Curve | Params | Time-to-X target |
|---|---|---|---|
| <Upgrade A> | exponential | base <…>, r <…> | TTN ≤ <…> |
| Levels | polynomial | XP = <a>·L^<k> | L10 at <…> min |
| Zones | geometric | g0 <…>, m <…> | <…> min/zone |
| Rebirth | cost ×<g>, mult ×<m> | g/m = <…> | 1st at <…> min |
Reset vs. persist table: <…>

## 6. Economy  → [[Economy-Design-Sinks-And-Faucets]]
| Currency | Purpose | Faucets | Sinks | Resets? | Sold? |
|---|---|---|---|---|---|
Sink ratio target per stage: <0.7–0.95>   Trading: <yes/no; gating; PolicyService checks>

## 7. Rewards & randomness  → [[Reward-Schedules]]
| Table | Tiers & odds | Pity | Paid? (odds UI + PolicyService) |
|---|---|---|---|

## 8. Difficulty  → [[Difficulty-And-Mastery]]
Movement constants: WalkSpeed <…>, JumpPower <…>, Gravity <…>. Difficulty tiers & checkpoints: <…>. Assist offers: <…>

## 9. Idle/offline (if any)  → [[Idle-And-Offline-Earning]]
Cap <…> h · efficiency <…>% · min <…> s · payout at cap ≈ <…> min of active income

## 10. Monetisation  → [[Gamepasses-vs-Developer-Products]]
| Item | Type (pass/product/sub/private server) | Price (R$) | Value prop | When first shown |
|---|---|---|---|---|
Ethics check: free path to every tier ✅ · paid power ≤ <…> · odds disclosed ✅

## 11. Retention systems  → [[Retention-Metrics-D1-D7-D30]] [[Daily-Rewards-And-Streaks]] [[Session-Length-And-Pacing]]
Targets: D1 <…>% · D7 <…>% · median session <…> min · play days/wk <…>
Hooks: <dailies, streaks, timers, events, quests>

## 12. Live ops & content plan  → [[Content-Cadence]] [[Live-Ops-Playbook]]
Cadence: <weekly Sat 10:00 ET> · Update 1–4 contents: <…> · First event: <…>

## 13. Tech & data  → [[Data-Persistence-DataStores-And-ProfileStore]] [[Anti-Exploit-And-Server-Authority]]
Data schema v1 (keys, types, defaults): <…> · Server-authoritative actions: <…> · Remote list + validation: <…>

## 14. Analytics  → [[Analytics-And-Instrumentation]] [[Balancing-Methods]]
Onboarding funnel steps: <1..8> · Progression funnels: <…> · Economy events: <…> · Experiments planned: <…> · Configs exposed: <…>

## 15. Risks & open questions
| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|

## 16. Milestones
| Milestone | Date | Exit criteria |
|---|---|---|
| Graybox core loop | <…> | loop validation table passes ([[Core-Loops]]) |
| Vertical slice (first 30 min) | <…> | 5 fresh playtesters hit TTN targets |
| Soft launch | <…> | funnel instrumented, 4 updates ready |
| Launch | <…> | ads/influencer plan ready |

## Changelog
- YYYY-MM-DD — <change> — <reason/metric>
```

## Checklist
- [ ] Template copied to `Projects/<GameName>/GDD.md` and linked from the project index
- [ ] Sections 1–6 reviewed before content production starts
- [ ] Every number has a target and a source tag (sim / telemetry / guess ⚠️)
- [ ] Changelog kept up to date after launch

## Pitfalls
- A 40-page GDD nobody reads. Keep detail in linked spec notes.
- Writing features before loops: sections 3–4 must be solid first.
- Not updating the GDD after launch, so it no longer matches what's live.

## Related
- [[Core-Loops]] · [[Onboarding-And-First-60-Seconds]] · [[Progression-Curves]] · [[Economy-Design-Sinks-And-Faucets]] · [[Reward-Schedules]] · [[Genre-Playbooks]] · [[Balancing-Methods]]
- [[Gamepasses-vs-Developer-Products]] · [[Retention-Metrics-D1-D7-D30]] · [[Live-Ops-Playbook]] · [[Analytics-And-Instrumentation]]

## Sources
- Roblox Creator Docs, Design games on Roblox (core loops, onboarding, season pass design): https://create.roblox.com/docs/production/game-design (read 2026-10-04)
- Structure adapted from vault notes in `Design/`; no external template copied.
