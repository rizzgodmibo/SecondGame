---
tags: [project/trap-your-friends, design/core-loop]
status: draft
updated: 2026-10-06
confidence: low
---
# Trap Your Friends: Round Structure v2 (roles + map vote)

## TL;DR
- **(USER, 2026-10-06) The structure changed.** It is no longer two teams building lanes for each other. Each round, **some players are randomly chosen as Trappers** ("similar to old games like SharkBite"). Everyone else is a **Runner**.
- (USER) **3 medium-sized maps**; players **vote** on the map each round.
- (USER) Trappers **place traps during a short prep phase, then can also trigger them live** during the run (Deathrun-style buttons).
- (USER) About **1 Trapper per 4 players**. (USER, 2026-10-06) **A full server is 16: up to 4 Trappers and 12 Runners. Trapper zones are fixed, one per Trapper; they merge when there are fewer Trappers.**
- (USER) Runners win by **reaching the end** before time runs out; Trappers score for every runner they catch.
- Everything else below is DRAFT. This replaces the "two teams build lanes, proof run, swap" loop in [[Trap-Your-Friends-GDD]]; that GDD section needs rewriting (Claude Code task).

## Precedents (Roblox games API, 2026-10-06 snapshot)
| Game | Roles | Snapshot | Take |
|---|---|---|---|
| [Deathrun](https://www.roblox.com/games/206640076) (2015) | Killer presses buttons to fire traps; runners race the map | 371M visits, ~35 playing, 15-player servers | **Closest precedent.** A proven loop with no strong modern version, so the market has an opening (hypothesis) |
| [SharkBite Classic](https://www.roblox.com/games/734159876) (2017) / [SharkBite 2](https://www.roblox.com/games/8908228901) | 1 random shark vs everyone; teeth currency after each round | 1.66B / 499M visits, 15–18 servers | Random role each round; between-round shop |
| [Murder Mystery 2](https://www.roblox.com/games/142823291) | Random murderer/sheriff/innocents | ~209k playing, 12 servers | Random roles drive "one more round" |
| [Flee the Facility](https://www.roblox.com/games/893973440), [Survive the Killer](https://www.roblox.com/games/4580204640), [Piggy](https://www.roblox.com/games/4623386862) | 1 killer vs survivors; Piggy has placeable traps | 29k / 3.5k / 23k playing | Asymmetric rounds are still huge on Roblox |

## Roles (DRAFT numbers)
| Players in server | Trappers | Runners |
|---|---|---|
| 2–5 | 1 | 1–4 |
| 6–9 | 2 | 4–7 |
| 10–13 | 3 | 7–10 |
| 14–16 | 4 | 10–12 |
- Server cap **16** (USER, 2026-10-06; replaces the DRAFT cap of 12); minimum 2 to start (bots fill runners below 4? UNDECIDED).
- **Zones (USER 2026-10-06):** each map has 4 fixed Trapper zones. With 4 Trappers each owns one; with 3, zones 3+4 merge; with 2, zones 1+2 and 3+4 merge; with 1, the Trapper owns all 4 (DRAFT merge order).
- **Fair random:** weighted so players who haven't been a Trapper recently are more likely; nobody is Trapper twice in a row unless the server is tiny.
- UNDECIDED: sell a "Trapper chance" boost? Many asymmetric games do; it's a fairness and ethics call ([[Pay-To-Win-Boundaries]]). Default: no.

## Round flow (DRAFT timings, ~4–5 min)
| Phase | Time | Runners | Trappers |
|---|---|---|---|
| Lobby + map vote | 15 s | Vote on pads/UI (3 maps) | Same |
| Role reveal | 5 s | Big "RUNNER" card | Big "TRAPPER" card + their trap hand |
| Prep | 40 s | Wait in the start room. **(USER, 2026-10-06) Runners CAN see the course but NOT the traps:** traps stay invisible to Runners until the run starts. Start-room activities are DRAFT ([[Trap-Your-Friends-Map1-Layout]]) | Fly/walk the course and **place traps from their hand onto trap sockets**; budget per trapper |
| Run | **Timer 3:30 (USER, 2026-10-06, DRAFT)**; an average run takes 2:30–3:00 | Race to the finish; respawn at the last checkpoint; finish = win | **Trigger placed traps live** (each with a cooldown and a visible tell); passive traps run on their own |
| Results | 10 s | Finishers + "Most Trapped" + "Best Trap" replay | Catches scored |

## Trap placement (DRAFT)
- Each map has **trap sockets**: marked grid zones of different sizes (floor 2×2 / 4×4, wall, ceiling, lane-wide) along the route. Traps snap to a socket, which keeps it buildable on mobile and stops unwinnable blocking.
- Trap hand: each trapper draws ~6 cards from their unlocked collection (see [[Trap-Your-Friends-Trap-Catalogue]]); budget ~30 per trapper.
- Rule: a route must always exist (sockets are designed so no combination can fully block; Brick Walls are Bash-able).
- **Live triggers:** traps with a "triggered" mode show a button on the trapper's **HUD (USER, 2026-10-06: HUD buttons, not catwalk world buttons)**. Cooldown per trap; a 0.4 s tell before firing so runners can react.
- Trapper view: free camera over the map, or a catwalk above the course (UNDECIDED; the catwalk is more Deathrun-like and works with avatars). Claude's recommendation: a balcony per zone + HUD buttons ([[Trap-Your-Friends-Map1-Layout]]).

## Scoring (DRAFT)
- Runners: finish = coins (more for earlier places), +bonus for no deaths.
- Trappers: +1 per catch (cap per trap so one trap can't farm), +bonus if few runners finish.
- Currency name and spend: UNDECIDED.

## Maps (USER: 3 medium maps, voted)
- "Medium" = a 2–3 minute run for an average runner. (USER, 2026-10-06) Maps must be **bigger than the v2 slice**; DRAFT target ~800–1,200 studs of route, 4 zones × 10–12 sockets.
- Proposal: 3 themes, each with its own environment and trap-socket layout: **Castle Sky Island** (the v2 style test theme), plus two more (candidates: Candy Factory, Spooky Mansion, Space Station, Pirate Cove). UNDECIDED.
- Each map is a linear-ish route with branching shortcuts, checkpoints every ~30 s, and a finish tower.

## Open questions
1. ~~Trapper triggers: HUD or world buttons?~~ **HUD buttons (USER, 2026-10-06).** Trapper names shown on the zone banners (USER, 2026-10-06).
2. Can trappers also walk into the course to shove runners? (Probably not; keep them as "game masters".)
3. Bots: fill runners in small servers?
4. Themes for maps 2 and 3.
5. Currency name and the between-round shop (SharkBite-style).

## Related
[[Trap-Your-Friends]] · [[Trap-Your-Friends-GDD]] · [[Trap-Your-Friends-Trap-Catalogue]] · [[Trap-Your-Friends-Style-Test-v1-Feedback]] · [[Session-Length-And-Pacing]] · [[Friend-And-Group-Play]] · [[Genre-Playbooks]]

## Sources
- Holden's messages and answers, 2026-10-06 (Cowork chat).
- Roblox games API via the Browser pane, 2026-10-06 (visits, playing, max players; a single snapshot).
