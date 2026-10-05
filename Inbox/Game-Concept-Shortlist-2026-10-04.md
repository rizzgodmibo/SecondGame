---
tags: [design/concepts, inbox]
status: draft
updated: 2026-10-04
confidence: low
---
# Game Concept Shortlist (2026-10-04 brainstorm)

## TL;DR
- Brainstorm from Holden's third-game session: 12 pitches (3 per genre: simulator, obby, survival, weird), each tagged with one hook (progress, chaos, competition, exploration), 3 per hook.
- Holden picked **[[Rubber-Tower]]** to build. The other five fleshed-out concepts and six un-fleshed pitches are parked here for later.
- These are **recommendations / hypotheses**, not approvals. None has a plan, spec or code. Evidence type: brainstorm only, nothing tested or verified.
- Scope assumed: small game (core loop, progression, a few zones), young teens, mobile and PC first.
- Existing games to avoid overlapping: [[Paper Plane Toss]], Fish a Monster.

## Parked concepts (fleshed out)

### Scrap Yard Rebuild (simulator, hook: satisfying progress)
- **Loop:** grab scrap, sort into bins, snap parts onto a vehicle frame, sell or drive it, spend coins on bigger bins, a magnet tool and the next frame.
- **First 60s:** pile next to spawn, three parts, highlighted frame, snap clunk + particle burst, tiny cart done in about 40 s.
- **Progression:** 3 zones (backyard, junkyard, industrial dump), about 6 vehicle tiers, about 4 tools. Rebirth left out of v1.
- **Risks:** sorting becomes a chore (needs early auto-sort); part variety must read at a glance (Blender kit matters).
- **Open questions:** solo or shared yard? Do vehicles have a purpose (races, delivery) or just reward?

### Cloud Climb Atlas (obby, hook: exploration)
- **Loop:** climb a main path section by section; side routes hide collectibles; found shortcuts stay unlocked.
- **First 60s:** small cloud, clear first jump, visible glowing collectible just off path fills a map page.
- **Progression:** atlas menu of sections cleared and secrets found; cosmetics or titles. 5 biomes, 3 secrets each.
- **Risks:** secrets need visual hints; players who skip secrets finish fast.
- **Open questions:** are secrets cosmetic only, or do they affect the climb (shortcuts, double jump)?

### Raft Frenzy (survival/co-op, hook: funny chaos)
- **Loop:** raft moves down a river; hazards approach; team splits jobs (steer, patch, gather scrap, fend off); scrap becomes parts; run ends at sinking or river's end.
- **First 60s:** rock ahead, hole opens, water rises, plank patch, tutorial prompt shows roles, first crisis solved in about 30 s.
- **Progression:** permanent raft upgrades (hull, engine, storage); 3 river stages, about 8 hazards, about 6 parts.
- **Risks:** networked physics raft is technically demanding and exploit-prone; solo players need an AI or reduced-difficulty option.
- **Open questions:** player cap (2 to 4 or more)? Hazards as enemies or purely environmental?

### Base Camp Blitz (survival, hook: satisfying progress)
- **Loop:** about 10-minute rounds: gather, build defences, survive a wave; permanent upgrades in a hub between rounds.
- **First 60s:** small island, glowing tree and rock, first defence placed, countdown to first wave.
- **Progression:** permanent upgrade tree (tools, building types, starting resources); difficulty tiers; 3 maps, about 6 defences, about 3 enemy types.
- **Risks:** wave and combat balance needs heavy playtesting; permanent upgrades can trivialise early rounds, so tiers must scale.
- **Open questions:** AI enemies or player attackers? Any PvP?

### Gravity Garden (weird, hook: satisfying progress)
- **Loop:** plant seeds that grow into platforms and hazards, arrange a course, publish it, others run and rate it, ratings earn seeds for new plant types.
- **First 60s:** plant first seed, bouncy platform sprouts, build a five-jump course, test-run it immediately.
- **Progression:** about 8 plant types (bouncy, sticky, moving, disappearing), 3 garden themes, browse and rate screen.
- **Risks:** user-generated content needs moderation and a creator-must-complete-it rule before publishing (⚠️ verify: current Roblox policy for UGC and young audiences); mobile building UI is fiddly.
- **Open questions:** shared list or friends only? How would moderation work?

## Parked pitches (not fleshed out)
- **Moving Day Mayhem** (simulator, funny chaos): carry furniture into a truck with wobbly physics; co-op couch carrying; earnings buy bigger trucks and straps.
- **Lemonade Wars** (simulator, competition): shared street of stands, undercutting, harmless pranks, daily leaderboard.
- **Relay Obby** (obby, competition): teams of 2 to 4 each take a section and hand off a baton; team vs team race.
- **Last Lantern** (survival, exploration): keep one lantern lit through the night; explore for fuel and secrets; zones get more dangerous further out.
- **Inside the Vending Machine** (weird, exploration): world is the inside of a giant machine; conveyor zones, snack-themed areas, mechanical-puzzle secrets.
- **Ghost Delivery Race** (weird, competition): couriers race to deliver to ghosts; haunted shortcuts open and close each round.

## Comparison (judgement, not tested)
| Concept | Scope risk | Main technical risk |
|---|---|---|
| Rubber Tower (chosen) | Low | Mobile ragdoll physics |
| Scrap Yard Rebuild | Low | Part-snapping system |
| Cloud Climb Atlas | Low to medium | Level design volume |
| Raft Frenzy | High | Networked physics |
| Base Camp Blitz | Medium to high | Combat balance |
| Gravity Garden | High | UGC tools and moderation |

## Pitfalls
- No checklist guarantees commercial success; the ranking above is judgement.
- Check [[Genre-Playbooks]] and [[Thumbnails-And-Icons]] before committing to any parked concept.

## Related
- [[Home]] · [[Game-Building-Playbook]] · [[Core-Loops]] · [[Rubber-Tower]]

## Sources
- Brainstorm conversation with Holden, 2026-10-04 (chat). No external sources.
