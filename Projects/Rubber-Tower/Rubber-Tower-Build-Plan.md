---
tags: [project/rubber-tower, project/plan]
status: draft
updated: 2026-10-04
confidence: low
---
# Rubber Tower: Build Plan (phases 0 and 1 approved and built; later phases DRAFT)

## TL;DR
- 2026-10-04: Holden approved phases 0 and 1 and they are built (see [[Rubber-Tower-Build-Status]]). Phases 2 and later are still DRAFT and need his go-ahead. The game is built in Claude Code connected to this vault.
- Order follows [[Game-Building-Playbook]]: prove the riskiest thing first (avatar ragdoll on a phone), then graybox the tower, then the push move, then saving.
- Holden makes commits. The ongoing vault mandate does not cover game changes, publishing, purchases or messages.
- Before any 3D or map work, read `C:\Users\holde\Documents\GameDev\AssetLibrary\README.md` (read in the kickoff run on 2026-10-04; phase 1 uses only graybox parts).
- 2026-10-04 kickoff run: the detailed phase 0 and 1 proposal and questions are below. Status and gates are in [[Rubber-Tower-Build-Status]].

## Phases (DRAFT)
| # | Phase | Output | Gate to pass |
|---|---|---|---|
| 0 | Scaffold | Rojo project, strict Luau, lint and format config, empty bootstraps | `rojo build` and lint pass; Holden confirms folder and repo |
| 1 | Ragdoll prototype | Player's own avatar ragdolls on fall on a flat test place | Looks and feels right on PC **and a real phone**; ragdoll cost measured |
| 2 | Tower graybox | Fixed tall tower with 3 to 4 big checkpoints, a few soft platforms between (fall onto, never spawn at), respawn at latest | Holden plays it; segment length feels fair |
| 3 | Push move | Server-validated shove with cooldown and force cap | Funny but not grief-heavy in a 2 to 4 player test |
| 4 | Saving | Checkpoint progress and world unlock persisted; checkpoint menu with teleport to claimed checkpoints | Data survives rejoin; follows [[Data-Persistence-DataStores-And-ProfileStore]] |
| 4b | Currency, titles and friend boost | Currency earned at checkpoints, titles above heads, friend boost on the currency | Server-validated; once-per-reward earning; friend check uses Roblox friends API |
| 5 | Art and feel | Low-poly Blender assets, sound, wobble polish | Screenshots thumbnail-worthy ([[Art-Direction]]) |
| 6 | Cosmetics and monetisation | Cosmetic shop (currency), Robux currency packs, 3 free + emote pack, passes (Buddy Carry with accept prompt, banana peel, skip checkpoint with title), no eggs | [[Monetisation-Design-Checklist]] complete; receipts idempotent ([[ProcessReceipt-Handling]]) |
| 7 | Soft launch | Public, small | Funnel instrumented ([[KPI-Dashboard-Spec]]) |
| 8 | World 2 | Second tower and unlock flow | After launch data |

## Proposed files for phases 0 to 4 (DRAFT)
New project folder, location UNDECIDED (suggested: `C:\Users\holde\Documents\GameDev\RubberTower`):

| File | Purpose |
|---|---|
| `default.project.json`, `rokit.toml`, `wally.toml`, `selene.toml`, `stylua.toml`, `.gitignore`, `README.md` | Rojo and tooling scaffold via the roblox-dev setup skill |
| `src/shared/Config.luau` | Tunables (cooldowns, force cap, checkpoint list) |
| `src/shared/Types.luau` | Shared types |
| `src/shared/Remotes.luau` | Remote definitions |
| `src/server/Main.server.luau` | Server bootstrap |
| `src/server/RagdollService.luau` | Ragdoll state and caps (phase 1) |
| `src/server/CheckpointService.luau` | Latest checkpoint and respawn (phase 2) |
| `src/server/PushService.luau` | Push validation: range, cooldown, force cap (phase 3) |
| `src/server/DataService.luau` | Persistence (phase 4) |
| `src/client/Main.client.luau` | Client bootstrap |
| `src/client/RagdollController.luau` | Client-side ragdoll visuals and input |
| `src/client/PushController.luau` | Push input and effects |
| `tests/*.spec.luau` | Pure-logic tests for checkpoint choice and push validation |
| Place file (tower map) | Built in Studio. Must be saved, because the map lives only in the place file, not in git |

## Phase 0 and 1 detail (approved by Holden 2026-10-04; built the same day)
Written during the kickoff run. Gates and evidence are tracked in [[Rubber-Tower-Build-Status]].
**As built, the differences from the tables below are:**
- Live avatars turned out to use AnimationConstraint joints with built-in sockets, so for them the service reuses Roblox's sockets ([[Avatar-Ragdoll]]).
- `BounceController` requires `RagdollController` directly.
- `dev.project.json` was added, and `default.project.json` ignores `**/Dev*.luau` so dev tools can never be published.
- The test place also has 11- and 13-stud threshold ledges and an angled bounce pad.
- No GitHub repo or CI, since Holden chose local git only.

**Notes for phase 3 (shove):**
- The target's client must apply the knockback, or the server must briefly own the body.
- `RagdollService:RagdollPlayer(target, Config.Shove.RagdollSeconds)` already extends an existing ragdoll.
- Consider a server cooldown on fall ragdolls (reviewer finding M1). This refines the table above: services go under `src/server/Services/` as in [[Module-Architecture]], not flat in `src/server/`.

### Phase 0: scaffold
| File | Purpose |
|---|---|
| `rokit.toml` | rojo 7.7.0, selene, stylua, lune (the code-gate pins) |
| `default.project.json` | Shared → ReplicatedStorage, Server → ServerScriptService, Client → StarterPlayerScripts. No `Packages` until a dependency is needed (ProfileStore in phase 4) |
| `selene.toml`, `stylua.toml`, `.gitattributes` (`eol=lf`), `.gitignore` (`*.rbxl*`, `sourcemap.json`, `Packages/`, `.mcp.json`, `.secrets/`) | Lint, format, line endings ([[Rojo Workflow Gotchas]]) |
| `README.md`, `CLAUDE.md` | How to build and run, plus a pointer to the vault hub and traps |
| `.mcp.json` (gitignored) | Registers `Roblox_Studio` for this project |
| `src/server/Main.server.luau`, `src/client/Main.client.luau` | Init/Start loaders that print "ready" with module counts |
| `src/shared/Config.luau` | Tunables. Holden's shove values (about 10 studs, 30 s, 2 to 3 s ragdoll) are recorded here but unused until phase 3 |
| `src/shared/Types.luau`, `src/shared/Remotes.luau` | Shared types. One remotes registry, created by the server |
| `src/shared/Rules/Cooldown.luau` + `tests/Cooldown.spec.luau` | One pure rules module so `gate.sh --scaffold` can pass. Reused later by the shove, teleport and banana peel |
| `.github/workflows/ci.yml` | Only if Holden wants a GitHub remote |

**Gate:** `gate.sh --scaffold` prints `GATE PASS`. With `rojo serve` connected, Studio Output shows both bootstraps ready with no errors. Holden confirms the folder and repo and makes the first commit.

### Phase 1: avatar ragdoll prototype
| File | Purpose |
|---|---|
| `src/shared/Config.luau` (Ragdoll, Bounce sections) | Fall threshold, recovery time, simultaneous-ragdoll cap, bounce launch speed, ragdoll-on-bounce flag. All starting numbers are DRAFT, for tuning |
| `src/shared/Rules/Ragdoll.luau` + `tests/Ragdoll.spec.luau` | Pure logic: does this fall ragdoll, how long, is the cap hit, is this request allowed |
| `src/shared/Remotes.luau` | Adds one client→server intent, `RagdollRequest` ("I am falling"). The client sends no numbers the server trusts. Ragdoll state replicates as a character attribute, not a remote |
| `src/server/Net/Guard.luau`, `RateLimiter.luau` | Copied from Fish a Monster's reviewed versions |
| `src/server/Services/RagdollService.luau` | Builds the constraints at spawn and handles both Motor6D and AnimationConstraint rigs. Sets `RequiresNeck = false` and `BreakJointsOnDeath = false`. Validates fall requests against the server's view of the root part. Exposes `Ragdoll(player, reason, seconds)` for the phase 3 shove. Applies the cap, recovery and cleanup on death or leave |
| `src/client/Controllers/RagdollController.luau` | Detects falls locally and sends the intent. On the `Ragdolled` attribute it sets the Physics state, stops animations and handles the camera. Afterwards it gets the character up and turns it upright |
| `src/client/Controllers/BounceController.luau` | Parts tagged `BouncePad` launch your own character. The owning client applies the force, because it simulates its own character |
| Dev only, never committed: `src/client/DevRagdoll.client.luau`, `src/server/DevStress.server.luau` | A Studio-only self-ragdoll key with PASS/FAIL checks, and a tool that spawns N varied R15 dummies and ragdolls them for the cost table. DevStress needs a non-Studio gate for the phone test (Holden's userId plus the test place id): **needs Holden's OK** |
| Studio place (saved, not in git) | A flat graybox: spawn, drop towers at about 8, 16, 32 and 64 studs, 2 tagged bounce pads and a ledge. Placeholder parts only, no art |

**Gate (proposed):** (1) the code gate prints `GATE PASS`, and `roblox-dev:roblox-reviewer` finds no unresolved high issues. (2) In Studio with 2 clients: falls above the threshold ragdoll and falls below don't. The player recovers upright and never dies from a ragdoll. Resetting mid-ragdoll is clean. The other client sees the ragdoll. Bounce pads launch. It works on R15 with accessories. 50 ragdoll cycles leave connections and memory flat. (3) Holden plays the private test place on his phone and PC, and his verdict is quoted. (4) A cost table: phone model, FPS and client physics ms, server heartbeat and physics ms, at 0, 1, 8 and 16 simultaneous ragdolls, with the dummy caveat stated. (5) Holden says phase 1 passes.

### Technical risks found during the kickoff run
- ⚠️ verify: [[Join Cutscene and Tutorial]] (Paper Plane Toss) says catalog-outfit rigs came with **AnimationConstraint** joints, not Motor6D. The ragdoll research in [[Rubber-Tower-Reference-Obbies]] assumes swapping Motor6Ds. Before coding, inspect a live R15 player character in Studio.
- Each player's client simulates their own character ([[Physics-And-Network-Ownership]]). So the server decides and caps ragdolls, bounces and pushes, but the owning client applies the motion. An exploiter could ignore it. This is acceptable for the prototype. A movement guard follows later ([[Anti-Exploit-And-Server-Authority]]).
- A real-phone test means a published private test place. Publishing is Holden's action.

### Questions for Holden before phases 0 and 1
1. Project folder and repo: `C:\Users\holde\Documents\GameDev\RubberTower` (suggested)? Local git only, or also a private GitHub repo with CI?
2. Avatar type: R15 only (recommended: more joints means floppier ragdolls, and one rig to support) or allow R6?
3. Max players per server: undecided, and the cost test needs a target. Test at 16 and 20?
4. Which falls ragdoll: proposed, a drop of about 12 studs or more (about 1.7 jump heights), tunable in Config. Fall recovery time: proposed about 1.5 s after landing.
5. Bounce pads: launch only, or launch and ragdoll? This will be a Config flag so Holden can feel both.
6. Phone test: will Holden publish the test place privately, and is DevStress allowed in that live server, gated to his userId?
7. Optional: add `luau-lsp` type checking. This downloads Roblox type definitions from GitHub. The current gate does not check `--!strict` types.

## Phase 2 detail: tower greybox (PROPOSAL, 2026-10-04, awaiting Holden)
Goal from the table above: a fixed tall tower with 3 to 4 big checkpoints and a few soft platforms between them (you can fall onto them, never spawn at them), and respawn at the latest checkpoint. **Gate:** Holden plays it, and segment length feels fair. Saving, the teleport menu and Squishies stay in phases 4 and 4b, so checkpoint progress in phase 2 lasts for the session only.

### Proposed layout (DRAFT; every number to tune with timed runs)
- **Shape:** a spiral path around a central core, so most falls land on a lower turn of the same segment instead of at the bottom. Soft platforms are wide catch ledges under the hardest stretches.
- **Size:** 4 segments, at about 8 to 10 short stages of 30 to 50 s each, which fits Holden's 5 to 8 minute segment target. Each stage rises about 10 studs, so each segment is about 100 studs and the whole tower about 400 studs (guess ⚠️, tune after Holden's timed run).
- **Obstacles in the greybox:** standard jumps sized from the gap table in [[Difficulty-And-Mastery]] (easy at the bottom, harder going up, with an easy relief stage after each spike), ladders (trusses) and bounce pads (approved). Nothing beyond these unless Holden adds it.
- **Art:** placeholder parts only, with crisp zone colours per segment. Real low-poly Blender art comes in phase 5 (asset library README read 2026-10-04).
- **Conflict to manage:** [[Difficulty-And-Mastery]] says don't lose more than about 60 s of progress to one mistake. Long segments are Holden's choice, so the spiral and the soft platforms are how a single fall is kept short. The timed runs will show whether that works.

### Proposed files
| File | Purpose |
|---|---|
| `src/shared/Config.luau` (Checkpoints section) | Tag names, the respawn rule, the fall-zone tag, segment time targets (5 to 8 min, USER) for the dev timer |
| `src/shared/Rules/Checkpoint.luau` + `tests/Checkpoint.spec.luau` | Pure logic: does touching checkpoint N change your respawn, which checkpoint you respawn at, segment-time summary |
| `src/server/Services/CheckpointService.luau` | Checkpoint pads tagged `Checkpoint` (attribute `Index`). The server claims on touch, checking a living character within range. Stores progress per player in memory and shows it as a `Checkpoint` player attribute. On spawn, puts you on your checkpoint. Landing in a `FallZone` ends any ragdoll and teleports you to your checkpoint in under 1 s. Soft platforms (`SoftPlatform` tag) are never respawn points |
| `src/client/Controllers/CheckpointController.luau` | A placeholder "Checkpoint 2!" message when the attribute changes. Real UI and sounds come later |
| Dev only (gitignored): `src/server/DevSegmentTimer.server.luau`, plus `DevPanel` buttons "Go to checkpoint N" | Prints each run's time and falls per segment to Output and the panel, so segment length is measured, not guessed |
| Temporary: the `roblox-map-audit` runner | Checks every checkpoint is reachable from spawn, nothing is a dead end, and fall heights. Removed after the run |
| Studio place (saved, not in git) | `Workspace.Tower`: a start island, Segment1 to Segment4, checkpoint pads, soft platforms, the fall zone. Built by Claude through Studio MCP in chunks, then tuned |

### Proposed gate
1. The code gate prints `GATE PASS`, and the reviewer finds no high-severity issues.
2. Map audit: no FAIL. Every checkpoint is reachable, there are no pits without a way out, and short falls are listed.
3. Studio tests:
   - claiming checkpoints in order
   - resetting puts you back on your checkpoint
   - landing in the fall zone teleports you to your checkpoint in under 1 s, even while ragdolled
   - a soft platform never becomes your respawn
4. Holden plays it on phone and PC, and the dev timer records his segment times against the 5 to 8 minute target. This is one player's run, not a median.
5. Holden says the segment length feels fair.

### Questions for Holden before phase 2
1. **What sends you back to your checkpoint?** Recommended: a fall zone (for example a soft "rubber sea") below and around the tower; anywhere else you land, you carry on climbing from there.
2. **Checkpoints:** 3 checkpoints plus the summit, so 4 segments? Recommended: yes.
3. **Touching a lower checkpoint you already claimed** (after teleporting down, later): does your respawn move down? Recommended: no, you always respawn at your highest checkpoint.
4. **Tower shape:** a spiral around a core (recommended), a straight climb, or a zig-zag?
5. **Soft platforms:** how many? Recommended: about 2 per segment, wide and clearly coloured, under the hardest stretches.
6. **Obstacles:** plain jumps, ladders and bounce pads only for now (recommended), or greybox ice or wobble platforms already?
7. **Movement:** keep Roblox's defaults (walk speed 16, jump height 7.2)? Recommended: yes. Every gap is measured from these, so they need locking before building.

## Phase 2 as built: greybox v1 (2026-10-04)
- **Code:** `CheckpointService`, `SurfaceService` (ice), `WobbleController`, `CheckpointController` (placeholder message), `Rules/Checkpoint` + spec, and Config sections Ice/Wobble/Checkpoints. Dev only: `DevSegmentTimer`, plus panel buttons Start / Go to CP 1–3 / Go to top / Reset progress.
- **Map tool:** `tools/BuildTowerGreybox.luau`, synced only by `dev.project.json` into ServerStorage.DevTools. It builds a 60×60 hollow tower, 4 × 100 studs, with checkpoint floors you climb through a hatch.
- **Checks:**
  - code gate `GATE PASS` (23 specs);
  - map audit per segment at spacing 1: **4/4 PASS**;
  - every ladder, bounce pad and hatch walk-tested OK;
  - checkpoint tests 9/9 plus a ragdolled send-back;
  - ragdoll self-test 15/15.
  Details in [[Rubber-Tower-Build-Status]].
- **Holden's verdict:** too enclosed and too narrow, and it needs a fantasy world feel. The layout is rejected; the code stays.

## Phase 2 greybox v2: as built (2026-10-04)
- Holden answered: walled mystical valley, floating islands and crystals, 240×240 for now, use existing assets and make new models. Built as `tools/BuildValleyGreybox.luau`. Evidence in [[Rubber-Tower-Build-Status]], models in [[Rubber-Tower-Valley-Kit]].
- Next:
  1. Holden looks at it in Studio and reviews the kit art.
  2. With his OK, upload the kit.
  3. The builder swaps placeholders for the kit meshes.
  4. Re-audit, and run the timed segment runs (gate item 4).

## Phase 2 greybox v2 (PROPOSAL, 2026-10-04, awaiting Holden)
The code (checkpoints, ice, wobble, bounce, fall send-back, timer) doesn't change; only the map tool and the place do.
- **A walled world, not a shaft:** an inside area about 240 × 240 studs (4× v1's width), bounded by a square of tall fantasy border walls (castle ramparts or cliffs with towers and arches) far from the path. Open sky above, so you always see the world below and the summit above.
- **Ground level is a start area inside the walls** (meadow, village or courtyard), so it reads as a world from the first second.
- **A central landmark as the spine** (its kind is Holden's choice). The path spirals around it, hops out to floating islands, and visits balconies and ledges on the border walls.
- **Big checkpoints are wide open islands or plateaus** about 50–60 studs across, attached to the spine, not sealed floors. Falls land on lower islands, soft platforms or the checkpoint island below. The existing "fall below your checkpoint" rule still sends you back.
- **Each segment is its own themed fantasy world** (the chained-obby lesson). Platforms are themed objects instead of plain slabs. Special platforms fit the themes (for example bouncy mushrooms, ice crystals, jelly or cloud wobble platforms). All of this is a suggestion; the themes are Holden's call.
- **Size:** still 4 segments of about 80–100 studs (wider routes take longer per stud of height). Retime with the dev timer.
- **Greybox look:** simple shapes with the zone palettes. Optionally place Holden's existing low-poly trees and rocks (already uploaded, asset library) on the ground and islands to show the fantasy feel early; nothing new is uploaded. Real art stays phase 5 (Blender pipeline).
- **Risks:** more parts and a wide tall view cost phone performance, so re-measure FPS and check streaming. Wider gaps between path and walls also mean longer falls; the soft platforms and islands must catch them.
- **Gate:** the same as v1, plus Holden says it feels like an open fantasy world.

### Questions for Holden before v2
1. Border walls: full height (a walled valley with sky above; recommended), or lower walls around a ground kingdom with the climb rising above them into open sky?
2. What is the central spine? (A giant tree or beanstalk, a wizard tower, a crystal spire, a stack of floating islands with no spine, or your own idea.)
3. The theme of each of the 4 segments. Suggestions: 1 meadow/castle courtyard, 2 mushroom forest, 3 crystal/ice caves, 4 cloud kingdom. Pick these or name your own.
4. Size: about 240 × 240 inside and about 400 tall (recommended)?
5. Place your existing low-poly trees and rocks in the greybox now for the feel, or keep it pure blocks until the art phase?

## Decision points that need Holden
1. Go-ahead to start (no changes requested so far).
2. The project folder is created in the Claude Code session; no path needed here.
3. Ragdoll (USER): mostly on falls and pushes, plus wobble or bounce areas. Phase 1 should prototype both the fall ragdoll and a bounce/wobble area.
4. Push (USER): basic shove for everyone; numbers still to set in phase 3.
5. Passes (USER ideas): banana peel and carry/throw; rules to design before phase 6, nothing priced yet.

## Pitfalls
- Do not start phase 2 art before the ragdoll passes on a phone.
- Do not add the push move without server validation and a cooldown.

## Related
- [[Rubber-Tower]] · [[Rubber-Tower-Build-Status]] · [[Rubber-Tower-GDD]] · [[Rubber-Tower-Reference-Obbies]] · [[Project-Bootstrap-Checklist]] · [[Module-Architecture]]

## Sources
- Vault playbook and conversation with Holden, 2026-10-04. No external sources.
