---
tags: [design/pacing]
status: draft
updated: 2026-10-04
confidence: medium
---
# Session Length and Pacing

## TL;DR
- Roblox counts **playtime per user** as a top-tier recommendation signal, **capped at 60 min per user per game per day**. Engagement past 60 min/day earns nothing in ranking. Spend design effort on getting more players *to* 30–60 min and on **more play days** (D1, D2–7, D8–28 are separate signals) ([[Discovery-Algorithm]]).
- Build sessions from **beats** of 3–8 min. Each beat has a goal, an escalation and a payoff. A session is 3–6 beats, then a **session-end hook**.
- End every session with an **open loop**: a timer running (plants, offline cap, egg incubating), a goal at 70–90%, a streak to protect, or a scheduled event to return for.
- Target median session lengths by genre (table below). If you're below range, fix the beat gap (TTN, round downtime) before adding content.
- Use real-time **scheduled server events** (weather, admin events, boss spawns) every 15–60 min to extend sessions and gather players. Grow a Garden and Adopt Me both build on recurring timed content.

## How playtime is scored
| Fact | Implication |
|---|---|
| Playtime signal capped at 60 min/user/game/day | design for 20–60 min daily; marathon sessions don't pay off algorithmically |
| Signals use **organic Recommended-for-You users only** | ad-acquired or friend-joined users don't count toward ranking |
| Signals are per-user **averages** | small games with deeply engaged users are not disadvantaged |
| First-play bounce measured 61–180 s | session 1's first 3 min are the most important minutes ([[Onboarding-And-First-60-Seconds]]) |
| Weekly seasonality peaks on **Saturday** | ship updates Fri/Sat ([[Content-Cadence]]) |
| AFK time counts as playtime | AFK-friendly mechanics (idle income, AFK zones) raise playtime but not fun; balance with active rewards ⚠️ verify: how Roblox treats idle-kicked/AFK sessions in the playtime signal |

## Target session lengths by genre
⚠️ verify: these ranges are vault estimates from genre structure plus third-party reports, not Roblox-published benchmarks. Compare with the benchmark games on your Creator Analytics Engagement page.

| Genre | Median session target | Natural session unit | Main extender |
|---|---|---|---|
| Simulator / pet | 15–30 min | zone or rebirth run | eggs, events, rebirth |
| Tycoon | 20–40 min | build the next floor | next unlock always visible |
| Obby | 10–25 min | 10-stage section | stage count, skips, checkpoints persisted |
| Tower defense | 20–40 min | 1–3 matches (8–20 min each) | "one more match", daily quests |
| Horror (Doors-like) | 15–30 min | one run | squad runs, revives |
| Roleplay / hangout | 25–60 min | self-directed | friends, house, pets |
| Battlegrounds / fighting | 15–30 min | streaks | kill streaks, characters |
| Anime grinder / RPG | 30–60 min | level band, boss | quests, raids |
| Round-based social (DTI, MM2) | 20–40 min | 3–6 rounds (~6–10 min each) | ranks, cosmetics |
| Trend / brainrot (steal-a) | 15–40 min | base cycle | steal/defend tension, rare spawns |
| Survival (99 Nights) | 20–45 min | one run/night count | best-night record, squad |

Third-party aggregate (2024): average session for the top 25% of games ≈ 8–9 min, median ≈ 5–6 min across all games ⚠️ verify: rolearn.dev-style aggregates are unofficial. Treat "> 15 min median" as top-tier.

## Pacing beats
**Beat structure (3–8 min):**
1. **Goal reveal** (a gate, wave, round theme): 5–10 s.
2. **Escalation**: grind or challenge with rising reward: 2–6 min.
3. **Payoff**: unlock, hatch, win, with juice: 10–20 s.
4. **Breather / choice**: spend, equip, trade: 30–60 s.

**Session shape (example simulator session, 25 min):**
```
0-3   Welcome-back modal (1 screen) -> spend offline earnings -> immediate upgrade
3-9   Beat 1: push zone 7 gate (TTN ~60s per upgrade)
9-10  Payoff: zone 8 opens + new egg
10-16 Beat 2: hatch toward new egg's rare (variable reward)
16-17 Server event: "Golden Rain" (every 30 min) -> social gathering
17-23 Beat 3: rebirth push (bar 60% -> 85%)
23-25 Session-end hook: "Rebirth at 85%! Egg incubating: 2h. Daily streak: Day 4 tomorrow"
```

**Downtime budget**: in round-based games, keep non-play time (intermission, voting, loading between rounds) ≤ 20% of session time. In DTI-like rounds that is about ≤ 60–90 s of lobby per ~8-min cycle. Fill lobbies with mini-activities.

## Session-end hooks (pick 2–3)
| Hook | Mechanism | Strength | Ethics |
|---|---|---|---|
| Running timer (growth, incubation, offline cap) | FI schedule, return when ready | strong for D1 | fine |
| Near-complete goal (bar at 70–90%) | Zeigarnik effect | strong | fine |
| Streak protection | loss aversion | strong for D2–7 | cap the punishment; allow 1 grace day ([[Daily-Rewards-And-Streaks]]) |
| Scheduled event ("Boss at 6 PM", weekend admin event) | appointment | strong; social | fine |
| Cliffhanger content ("Door 50 is locked… next update") | curiosity | medium | fine |
| Friend activity (gifts, trade requests waiting) | social obligation | medium | no fake friend activity |
| Leaderboard reset countdown | competition | medium | fine |

Show a **session summary** on leave intent (menu open, idle) or at natural ends: earned, progress %, what's waiting tomorrow.

## Server events as session extenders
- **Random-interval** (VI schedule) events every 15–60 min: weather/mutation events, golden spawns, meteor showers. These keep players in-server and create shared moments ([[Reward-Schedules]]).
- **Fixed scheduled** events (top of each hour, weekend admin events): appointment play and social spikes. Grow a Garden and Steal a Brainrot used high-profile "admin abuse" events to spike concurrency ([[Live-Ops-Playbook]]).
- Show a countdown on the HUD ("Next event: 12:30"). The visible timer is the hook.

## Checklist
- [ ] Target median session and D1/D7 written in the GDD ([[Retention-Metrics-D1-D7-D30]])
- [ ] Session mapped into 3–6 beats with goals and payoffs
- [ ] ≥ 2 session-end hooks implemented; session summary screen
- [ ] At least one recurring in-server event with a HUD countdown
- [ ] Round games: downtime ≤ 20% of session
- [ ] Track session length distribution (not just mean) and quit-points ([[Analytics-And-Instrumentation]])

## Pitfalls
- Padding sessions with waits or walking. Playtime rises, satisfaction and D7 fall, and the algorithm follows retention long-term.
- Designing for 3-hour sessions. Past 60 min/day there is no ranking gain, and young players' play windows are short.
- Popups at session end that block leaving. That is a dark pattern and generates reports.
- Events so frequent they become noise (< 10 min apart).
- Ignoring mobile battery/heat. Long sessions on low-end phones need a performance budget.

## Related
- [[Core-Loops]] · [[Onboarding-And-First-60-Seconds]] · [[Progression-Curves]] · [[Reward-Schedules]] · [[Idle-And-Offline-Earning]] · [[Content-Cadence]] · [[Genre-Playbooks]]
- [[Discovery-Algorithm]] · [[Retention-Metrics-D1-D7-D30]] · [[Daily-Rewards-And-Streaks]] · [[Live-Ops-Playbook]] · [[Analytics-And-Instrumentation]]

## Sources
- Roblox Creator Docs, Discovery (playtime cap 60 min/user/game/day; play days D1/D2–7/D8–28; Saturday seasonality; organic-only signals): https://create.roblox.com/docs/discovery (via github.com/Roblox/creator-docs, read 2026-10-04)
- Dress to Impress round timing (360 s dressing): https://dti-dress-to-impress.fandom.com/wiki/Dress_To_Impress/Game_Mode
- Tubefilter (2025-08-25), Grow a Garden vs Steal a Brainrot admin events → 47M combined record: https://www.tubefilter.com/2025/08/25/roblox-grow-garden-steal-brainrot-admin-war-record/
- Unofficial aggregate session benchmarks: https://rolearn.dev/guidance/first-week-retention-optimization/ ⚠️ verify
