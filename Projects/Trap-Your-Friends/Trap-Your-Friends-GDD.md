---
tags: [project/trap-your-friends, design/gdd]
status: draft
updated: 2026-10-06
confidence: low
---
# Trap Your Friends: Game Design Doc (draft)

**Tags on every line:** (USER) = Holden approved it. (DRAFT) = a proposal, not approved. UNDECIDED = open question. SUPERSEDED = replaced by a later USER decision (kept for history). Only (USER) lines and the hub's "Decisions from Holden" are approved ([[Trap-Your-Friends]]). Numbers are starting guesses to playtest.

**2026-10-06: the core loop changed** (USER) to random Trappers vs Runners on 3 voted maps. Details in [[Trap-Your-Friends-Round-Structure]]. The old "two teams build lanes, proof run, swap" loop is kept in the **Superseded** section at the end.

## TL;DR
- (USER) Each round, some players are **randomly picked as Trappers** (like SharkBite), **about 1 per 4 players**. Everyone else is a **Runner**.
- (USER) Trappers **place traps from their hand during a short prep phase**, then can **trigger them live during the run** (Deathrun-style).
- (USER) Runners win by **reaching the end before time runs out**. Trappers **score for each runner they catch**.
- (USER) **3 medium-sized maps**; players **vote** on the map each round. Map 1 = **Castle Sky Island** (USER, 2026-10-06).
- (USER) Retro stud style with JJS-style destruction: **cut around the hit**, smallest piece 1 stud (replaces the v1 "1-stud cells", USER 2026-10-06).
- (DRAFT) Monetisation is cosmetic only. Trap cards unlock by playing, never by paying.

## 1. Core fantasy
- (DRAFT) Trapper: "I'm the game master. I set the course and pressed the button at exactly the right moment." Runner: "I dodged everything my friend threw at me and made it." The roles swap between rounds, so everyone gets both.

## 2. Players, roles and server
- (USER) About 1 Trapper per 4 players, picked randomly each round.
- (DRAFT) Server cap 12; minimum 2 to start. Trappers by server size: 2–5 → 1, 6–9 → 2, 10–12 → 3.
- (DRAFT) Fair random: weighted towards players who haven't been a Trapper recently; nobody is Trapper twice in a row unless the server is tiny.
- UNDECIDED: bots fill Runners in small servers? A paid "Trapper chance" boost (default: **no**, [[Pay-To-Win-Boundaries]])?

## 3. Maps and trap sockets
- (USER) 3 medium maps, voted each round. "Medium" (DRAFT) = a 2–3 minute run for an average runner.
- (USER, 2026-10-06) Map 1 = **Castle Sky Island**. Maps 2 and 3: proposals in [[Trap-Your-Friends-Map-Plan]] (UNDECIDED).
- (DRAFT) Each map is a linear-ish route with branching shortcuts, checkpoints about every 30 s and a finish tower.
- (DRAFT) **Trap sockets:** marked grid zones along the route (floor 2×2 / 4×4, wall, ceiling, lane-wide). Traps snap to sockets: easy to place on mobile, and no unwinnable blocking. 8–12 sockets per Trapper per map.
- (DRAFT) Rule: a route must always exist (no socket combination can fully block; Brick Walls are Bash-able).
- (DRAFT) Built from classic studded bricks ([[Trap-Your-Friends-Art-Style-Guide]]); everything breakable rebuilds (see 8).

## 4. Round flow (DRAFT timings, ~4–5 min)
| Phase | Time | Runners | Trappers |
|---|---|---|---|
| Lobby + map vote | 15 s | (USER) vote on 3 maps | Same |
| Role reveal | 5 s | "RUNNER" card | "TRAPPER" card + trap hand |
| Prep | 40 s | Wait in the start room and can't see the course | (USER) place traps from their hand onto sockets; budget per Trapper |
| Run | 2:30–3:00 | (USER) race to the finish; respawn at the last checkpoint | (USER) trigger placed traps live (cooldown + visible 0.4 s tell); passive traps run on their own |
| Results | 10 s | Finishers, "Most Trapped", "Best Trap" replay | Catches scored |
- (DRAFT, carried over from the old loop) Traps are a **surprise for Runners**: they can't see the course during prep. (The old USER decision was "hidden from the other team during the build phase". Holden to confirm this is the new form of it.)

## 5. Traps
- Pool of ~100 ideas, the design rules and a suggested launch 30: [[Trap-Your-Friends-Trap-Catalogue]] (DRAFT).
- (USER, 2026-10-06) "We need TONS of them". Every trap follows the design rules: chunky silhouette, face/eyes, idle animation, tell → wind-up → hit → recover, big funny hit, **black outline**.
- (DRAFT) Trap hand: each Trapper draws ~6 cards from their unlocked collection; budget ~30 per Trapper.
- (USER) Live triggering: traps with a "triggered" mode can be fired by the Trapper during the run. (DRAFT) Per-trap cooldown; 0.4 s tell. UNDECIDED: HUD buttons or world buttons on a Trapper catwalk.
- UNDECIDED: can Trappers walk into the course to shove runners? (Proposal: no, they're game masters.)

## 6. Runner abilities
- (DRAFT) Default movement (WalkSpeed 16, JumpHeight 7.2 as in [[Rubber-Tower]]).
- (DRAFT) **Bash** (stretch): a short shoulder dash (8 s cooldown) that breaks Brick Walls and knocks nothing else.
- UNDECIDED: can runners bump each other?

## 7. Scoring
- (USER) Runners win by reaching the end before time runs out. Trappers score for each runner they catch.
- (DRAFT) Runners: finish = coins (more for earlier places), a bonus for no deaths.
- (DRAFT) Trappers: +1 per catch (capped per trap so one trap can't farm), a bonus if few runners finish.
- UNDECIDED: currency name and the between-round shop (SharkBite-style).

## 8. Destruction system
- (USER, 2026-10-06) **As close to Jujutsu Shenanigans as possible:**
  - Cut only around the hit (the wall keeps standing with a jagged hole).
  - Mixed-size slabs and chunks.
  - Debris lands and lingers about 10 s (lower on low graphics quality if needed).
  - Heavy impact VFX: flash, streaks, dust, camera shake, a short hit-stop.
  - Rebuild only when nobody is nearby.
- (USER, 2026-10-06) Cut-around-the-hit **replaces the v1 "1-stud destruction cells"**. The smallest piece stays 1 stud.
- (DRAFT) Tech: the server splits the hit part along whole-stud lines and keeps anchored remainder pieces (authoritative collision). Clients get the removed boxes and spawn pooled, client-only physics debris. No unanchored server parts. Spec: [[Trap-Your-Friends-Style-Test-v2-Plan]].
- UNDECIDED: does a caught runner shatter into cubes (JJS-like comedy) or ragdoll? The style tests show a noob shatter **as a demo only**.

## 9. Controls
- (DRAFT) Trapper prep: free camera or catwalk over the map (UNDECIDED). Mobile: tap a card → sockets light up → tap a socket → Rotate / Confirm. PC: click, R.
- (DRAFT) Trapper run: a trigger button per triggerable trap, with its cooldown ring.
- (DRAFT) Runner: standard controls; a Bash button on mobile.

## 10. Modes
- (DRAFT) v1: the classic Trappers vs Runners round on 3 voted maps.
- (DRAFT) Later: private-server rules, events (one map remix), a hard mode with more Trappers.

## 11. First session
- (DRAFT) First round as a Runner, with on-screen trap tells explained. A short Trapper tutorial (place 2 traps, trigger one on a noob bot) the first time someone is picked as Trapper.

## 12. Progression and monetisation
- (DRAFT) XP unlocks trap cards and cosmetics (play only). Trap mastery stats, titles.
- (DRAFT) Cosmetic shop: trap skins, **debris skins** (confetti, candy cubes), runner trails, emotes, private servers. No pay-to-win ([[Pay-To-Win-Boundaries]]).

## 13. Without chat
- (DRAFT) Trapper/Runner role cards, pings, vote pads. Voice is a bonus.

## 14. Safety
- (DRAFT) Traps snap to fixed sockets, and placements live only for the round, so nobody can build anything offensive. Report button on the results screen.

## 15. Risks
- Trapper UX on mobile (placing and triggering). Destruction cost on low-end phones. Fun for Runners when a Trapper is AFK (fallback: passive traps still run; auto-trigger UNDECIDED). Role fairness.
- Competitors and precedents: Deathrun, SharkBite, MM2, Flee the Facility, Piggy ([[Trap-Your-Friends-Round-Structure]]); Build and Kill Verity (~3.3k playing on 2026-10-05).

## Superseded (kept for history, do not build)
**SUPERSEDED 2026-10-06** by the Trappers vs Runners structure above (USER). The old draft loop was:
- ~~(USER 2026-10-05) Two teams each build a hidden trap lane from classic studded bricks, then swap and run each other's lane.~~
- ~~(DRAFT) A match is best of 3 rounds (~12 min): theme vote 10 s → draft 15 s (5 cards, keep 3) → build 90 s (brick budget ~40 per player, hidden from the other team) → proof run 30 s → swap run 75 s → fail cam 10 s.~~
- ~~(DRAFT) Proof run rule: your team must clear its own lane, or your kill bricks go harmless and the other team gets +2.~~
- ~~(DRAFT) 2 teams × 2–4 players, server cap 8, each player owns one 35-stud segment of a 12 × 140 lane.~~
- ~~(DRAFT) Scoring: runners +1 per segment, +3 finish, +1 first; builders +1 per trap kill (cap 3); team score + MVP.~~
- ~~(DRAFT) Build camera over your own segment; modes Classic 2v2/4v4, King of Traps, Daily Gauntlet; tutorial segment with 3 kill bricks.~~
- ~~(USER 2026-10-05) 1-stud destruction cells~~ → replaced by cut-around-the-hit (USER 2026-10-06).
- The old 16-trap table (costs 1–5 per trap) moved to the larger pool in [[Trap-Your-Friends-Trap-Catalogue]].

## Related
[[Trap-Your-Friends]] · [[Trap-Your-Friends-Round-Structure]] · [[Trap-Your-Friends-Map-Plan]] · [[Trap-Your-Friends-Trap-Catalogue]] · [[Trap-Your-Friends-Art-Style-Guide]] · [[Trap-Your-Friends-Style-Test-v2-Plan]] · [[Friend-And-Group-Play]] · [[Anti-Exploit-And-Server-Authority]]

## Sources
- Holden's decisions 2026-10-05 and 2026-10-06; [[Trap-Your-Friends-Round-Structure]]; destruction references in [[Trap-Your-Friends-Reference-Board]] and [[Trap-Your-Friends-Style-Test-v1-Feedback]].
