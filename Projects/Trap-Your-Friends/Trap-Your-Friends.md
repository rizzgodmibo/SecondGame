---
tags: [project/trap-your-friends, project-hub]
status: draft
updated: 2026-10-05
confidence: low
---
# Trap Your Friends (project hub)

## TL;DR
- Holden chose this game on 2026-10-05 from the retro party brainstorm ([[Retro-Party-Game-Concepts-2026-10-05]] → [[Retro-Party-Deep-Dive-2026-10-05]], where it was called "Trap Builders").
- **Pitch (USER, 2026-10-06):** each round some players are randomly picked as **Trappers** (about 1 per 4). They place traps on sockets during a short prep, then trigger them live, Deathrun-style, while the **Runners** race to the finish of one of 3 voted maps. Built in the retro / classic-Roblox stud style with JJS-style brick destruction. *(Superseded pitch, 2026-10-05: two teams build trap lanes, prove them, then swap.)*
- **Status (2026-10-06):** v3 plan approved. **Step 0 done** (18 sounds wired, a/b toggle). **Step 1 done:** Sky v3 uploaded and applied in Studio, measured; open: the draw-distance option. Holden saved the place after Sky v3 (2026-10-06). **Step 2 done: Hammer grey forms in both routes, STOPPED for the route pick** ([[Trap-Your-Friends-Hero-Traps-Plan]]) ([[Trap-Your-Friends-Sky-v3-Plan]]). Plans: [[Trap-Your-Friends-v3-Plan]], [[Trap-Your-Friends-Map1-Layout]], [[Trap-Your-Friends-Hero-Traps-Plan]], [[Trap-Your-Friends-Map-Plan]]. Style still **not locked**.
- Design draft: [[Trap-Your-Friends-GDD]]. Kickoff prompt for Claude Code: [[Trap-Your-Friends-Claude-Code-Prompt]].
- Target: young teens, mobile and PC first, small scope. Separate from [[Rubber-Tower]]; don't share code or the place file without Holden's OK.

## Decisions from Holden (2026-10-05, user-approved)
- **Game:** the trap-building versus game ("Trap Builders" in the deep dive).
- **Name:** "Trap Your Friends".
- **Style:** retro / classic stud style is "very very important". Reference games he named: **Jujutsu Shenanigans** ("a very popular game with that kind of retro style") and "many others with similar retro-type styles".
- **Destruction:** wants a destruction system like the one in Jujutsu Shenanigans ("very helpful").
- **Art rule exception:** building from parts is acceptable in principle (overrides the vault's "no final part-built props" rule for this project), **but Holden wants to approve the style and the way it is built first.** Nothing is locked until he does.
- **Trap visibility:** traps are **hidden** from the other team during the build phase (surprise when running).
- **Next step requested:** a project folder in the vault + a prompt to paste into Claude Code.

## Decisions from Holden (2026-10-05, Claude Code kickoff answers)
- **Vault:** `E:\Vault` is the source of truth (the copy he opens in Obsidian). `C:\Vault` is an old copy: don't edit it and don't copy anything into it. Gap-Tracker and Verification-Log are updated in `E:\Vault` only. Notes or files that still say `C:\Vault` get flagged to Holden, not fixed.
- **Style test direction:** A "Modern Retro" is chosen. The style test is built in A only (no B, no B lighting preset, no R6 session). **The style guide stays NOT locked until Holden approves the test.**
- **Avatars in the style test:** Holden's own R15 avatar. The noob NPC is a blocky character in classic colours built from a `HumanoidDescription` (body colours only, no catalog items).
- **Stud MaterialVariant:** approved. Claude may make its own stud tile (colour map + normal map, procedural or Blender, nothing downloaded) and upload it as a **private image**. That upload only, nothing else. Apply it **part by part by name**, not as a Plastic override. Compare it with legacy `SurfaceType` studs on two copies of the segment.
- **Noob shatter:** OK **as a demo only**, so Holden can judge shatter vs ragdoll. It stays UNDECIDED in the GDD.
- **Git:** `git init` in the project folder with the agreed `.gitignore`. No commits (Holden commits).
- **Test place:** Holden opens a new Baseplate and saves it as `TrapYourFriends\places\StyleTest.rbxl`, then tells Claude. He publishes privately himself if he wants a phone test.
- **TNT Brick:** Bright red with white bands, **not** Really red. The screenshots must say whether it gets confused with the Kill Brick.
- **Trap markings from parts only:** cracks, chevrons, stripes and the "?" crate. No decals.
- **Destruction cells:** 1 stud. Report part counts. Keep the 35-stud segments for now.
- **Style guides:** the project style guide wins over the general [[Retro-Stud-Style-Guide]] where they disagree (R15, Realistic lighting).
- **Tooling:** no Wally, no GitHub Actions. Copy Rubber Tower's local code gate (copy only, change nothing in RubberTower).
- **Screenshots:** go in `Projects/Trap-Your-Friends/attachments/`.
- **Plan:** phase 0 and phase 1 approved with these changes (A only, two stud methods, the noob shatter demo). Stop after Gate 0 and report.

## Decisions from Holden (2026-10-06, verdict on style test v1)
Full note: [[Trap-Your-Friends-Style-Test-v1-Feedback]]. **The style is still NOT locked.**
- **Traps are the whole game:** "we need TONS of them". The v1 traps look uninteresting. Every trap follows the design rules in [[Trap-Your-Friends-Trap-Catalogue]]: chunky silhouettes, faces/eyes, idle animation, clear tells, big funny hits.
- **Outlines like Steal an Egg:** black cartoon outlines around trap models, props and NPCs. Try a Highlight per model first; also test SelectionBox edges on one segment's bricks.
- **Destruction as close to Jujutsu Shenanigans as possible:**
  - Cut only around the hit, so the wall keeps standing with a jagged hole.
  - Mixed-size slabs and chunks instead of uniform cubes.
  - Debris lands and lingers about 10 s.
  - Heavy impact VFX: flash, streaks, dust, camera shake and a short hit-stop.
  - Rebuild still happens, but only when nobody is nearby (this also fixes the spinner/wall issue).
- **Build quality:** the retro builds are alright but look low quality/low effort. Fix with:
  - a themed environment instead of floating over the template baseplate, and a skybox;
  - 3-tone colour variation, trim and props;
  - calmer wall patterns, no glare speckle;
  - a better lighting pass.
- **Answers:**
  1. Outline colour: **black**.
  2. Claude **may make and upload our own decals/textures** (faces, warning stripes, signs, "?" crate) as **private images**. Nothing downloaded, nothing published.
  3. Claude may **read and audit VoxBreaker and VoxelDestruct** as references, but must show Holden the audit **before installing** either. Building our own is also fine.
  4. Debris linger about **10 s**: measure it and lower it on low graphics quality if needed.
- **Next task:** style test v2 in the same place (StyleTest.rbxl) with the following, plan and file list first:
  - one themed segment (Legacy + MaterialVariant copies);
  - 12 launch-list traps from at least 8 families, including Swinging Hammer, Wrecking Ball, Trapdoor, Boxing Glove Wall, Chomper and Glass Floor;
  - the JJS destruction demoed with the Wrecking Ball, TNT and a Brick Wall;
  - the same honest report as v1.
- Holden saved the v1 place with File → Save to File (2026-10-06).

## Decisions from Holden (2026-10-06, new game structure + v2 answers)
- **New structure** ([[Trap-Your-Friends-Round-Structure]]; the GDD core loop is rewritten, the old loop is marked SUPERSEDED):
  - Each round, some players are **randomly picked as Trappers** (like SharkBite), **about 1 Trapper per 4 players**. Everyone else is a Runner.
  - Trappers **place traps from their hand during a short prep phase**, then can **trigger them live** during the run (Deathrun-style).
  - Runners win by **reaching the end before time runs out**. Trappers **score for each runner they catch**.
  - **3 medium-sized maps**; players **vote on the map** each round.
  - All numbers in the Round Structure note are DRAFT.
- **Superseded by this:** "Two teams each build a hidden trap lane… swap" (2026-10-05) and "Trap visibility: hidden from the other team during the build phase". The surprise now comes from Runners not seeing the course during prep (DRAFT, Holden to confirm).
- **Map 1 = Castle Sky Island.** Style test v2 = a **vertical slice of Map 1's route** (one stretch from the castle gatehouse toward the finish tower), not two team lanes. Marked **trap sockets** on the route (floor 2×2 and 4×4, wall, one lane-wide); the 12 traps sit in sockets. Legacy-stud vs MaterialVariant stays as **two halves of the island**.
- **Sound:** make **new, original SFX** (bonk, crunch, glass, spring, chomp, whoosh, explosion, trap tell, catch sting). Sources allowed:
  - our own synthesis or procedural audio;
  - **free licensed** sounds from the Roblox Creator Store audio library.
  - Nothing ripped, no commercial audio.
  - Use the [[Sound-Design]] and roblox-sound-library checks (lead silence, clipping, loudness).
  - Upload privately within the monthly quota, and keep a list of every sound and its source in the vault.
- **Sky:** our own **painted 6-face skybox** (bright, stylised, puffy clouds, fits Castle Sky Island and the retro look), uploaded privately; Clouds on top if it helps.
- **Destruction:** cut-around-the-hit **replaces the v1 "1-stud cells"** decision. The smallest piece stays 1 stud.
- **Git:** one commit of the v1 code, message "Style test v1" (done: `411d4d4`, 2026-10-06). That is the only commit Claude may make.
- **Extra for v2 (prototype only, no round system yet):**
  - a Studio-only Dev **trapper panel** that live-triggers the Swinging Hammer, Boxing Glove Wall and TNT, with a cooldown and the 0.4 s tell;
  - a **Map Plan** note for Maps 2 and 3 (3 options each + a recommendation + trap-socket counts). Plan only: [[Trap-Your-Friends-Map-Plan]].
- **Colour:** the 3-tone floor rules are fine; the ±5–8% colour variation goes in the style guide as a **DRAFT exception**.

## Decisions from Holden (2026-10-06, v2 plan rev 2 approved)
- **Plan rev 2 approved:** build style test v2 now ([[Trap-Your-Friends-Style-Test-v2-Plan]]). Claude shows the **skybox preview sheet before uploading** it, then stops after v2 with the same honest report as v1.
- **Audio upload:** Holden imports the sound files himself through Studio's Asset Manager. Claude puts the final candidates in `TrapYourFriends\art\sfx\export\` with clear names (`sfx_bonk_a.ogg`, `sfx_bonk_b.ogg`, …), tells him when they're ready with a short step list, then reads the new asset ids from Studio and wires them in. Creator Store sounds are fine where they're better. No Open Cloud key for now.
- **Ceiling gantry sockets:** yes, a socket type (for the Swinging Hammer and Wrecking Ball).
- **Stud halves:** left/right down the route, with a trim stripe on the seam.
- **Maps 2 and 3:** the [[Trap-Your-Friends-Map-Plan]] stays a proposal; Holden chooses the themes after seeing v2.

## Style test v2: built (2026-10-06), awaiting Holden
- Full report: [[2026-10-06-Trap-Your-Friends-Style-Test-v2]].
- **Code** (uncommitted after `411d4d4`):
  - shared Rules: Fracture, Pendulum, TrapCycle, RateLimit, Sockets, DebrisPlan, RebuildTimers, Projectile (44 specs);
  - Traps/TrapDefs + Motion, Audio/Sfx, Lighting v2/V1/CastleSky;
  - server: DestructionService v2, TrapService v2 with the validated TriggerTrap remote, 11 trap modules;
  - client: Debris, ImpactFx, TrapAnim, TrapLocal, Outline, Sfx controllers;
  - dev: DevStyleTest, DevHud, DevTrapperPanel;
  - builder: `tools/StyleTestV2/`.
  - The v1-only files are deleted, and the deletions are **staged** with `git rm`.
- **Code gate:** PASS (44 specs; the builder lints clean).
- **Audit:** [[Destruction-Modules-Audit]] (VoxBreaker clean, VoxelDestruct not auditable without inserting it). Nothing was installed.
- **Sound:** [[Trap-Your-Friends-Sound-List]]. 18 original SFX ready, **not imported yet** (Holden's call: finish v2 without them).
- **For Holden:**
  - File → Save to File (Team Create session);
  - delete the parked `ServerStorage.StyleTestV1`, `ServerStorage.Baseplate_Template` and `ServerStorage.SpawnLocation` if unwanted;
  - import the SFX when convenient.

## Asset ids (private images, uploaded 2026-10-06 by Claude via Studio MCP `upload_image`; Holden approved)
| Asset | Id | Source |
|---|---|---|
| Stud tile colour / normal (v1) | 139618384581445 / 134190443469137 | `art/stud_tile/make_stud_tile.py` |
| Skybox +X / −X / +Y / −Y / +Z / −Z (v2; replaced in the place by Sky v3 on 2026-10-06) | 76994714944751 / 115349247794704 / 118614402728814 / 100936115845181 / 89842195628964 / 105773014101917 | `art/sky/make_skybox.py`. Preview approved "upload as is"; the 4 side faces were re-uploaded the same day after Studio showed jagged cloud shading |
| Skybox side faces, first upload (unused) | +X 123458292510031, −X 95804443930647, +Z 128251707417106, −Z 116160975627280 | superseded |
| Hazard stripes | 135689902982132 | `art/textures/make_textures.py` |
| Glass crack light / heavy | 94868522540997 / 89640669383911 | same |
| Impact streak / dust puff | 75678476037008 / 78710906836534 | same |
| Banner emblem / socket marker | 110287690236676 / 116490770980613 | same |
| Mouth grin / angry brows | 78463374317986 / 117978560769270 | same |
| **Sky v3 (2026-10-06, Open Cloud, Holden OK'd the batch)** skybox px / nx / py / ny / pz / nz | images 88765616773493 / 122249454156335 / 125422986741860 / 138319131569499 / 83645873033204 / 80615567184267 | decals 90542545374345 / 98492631693634 / 78053083040851 / 128696035902269 / 84564611907027 / 113863209514746 |
| Sky v3 sun alpha (in use) / sun additive / palette | images 134296067233008 / 82270087666425 / 104342276533306 | decals 89355138842894 / 114590037386872 / 122968418981149 |
| Sky v3 meshes (Model ids) TYF_Cloud_A..E / TYF_Far_CastleIsle, Spires, Windmill | 74351483587299, 95956809710590, 77880205838711, 103557953952630, 125386728712999 / 76853356933175, 88749002732964, 73374733878840 | MeshParts in `ReplicatedStorage.SkyAssets`; shared embedded texture 124720179755312 |
- **SFX:** 18 files (9 sounds × a/b), soundcheck PASS. Uploaded by Holden via Creator Hub; **wired 2026-10-06** in `Audio/Sfx.luau` (a by default, key 4 in Studio switches to b). Ids: [[Trap-Your-Friends-Sound-List]].

## Decisions from Holden (2026-10-06, verdict on style test v2)
Notes: [[Trap-Your-Friends-Style-Test-v2-Feedback]] · plans: [[Trap-Your-Friends-v3-Plan]]. **The style is still NOT locked.**
- **v2 came out decent.** The destruction, the Trapper panel and the socket idea work.
- **The sky is terrible:** a still painted image. He wants an actual good, living sky.
- **Traps:** they function fine and the outline is decent, but the models look **low quality and cheap**.
- **Map:** too small. **All 3 maps must be bigger** than the v2 slice suggests.
- **Server:** a full server is **16 players: up to 4 Trappers and 12 Runners** (Config, Round Structure and Map Plan updated 2026-10-06).
- **Trapper zones are FIXED, one per Trapper**; they merge when there are fewer Trappers.
- **Traps move to Blender meshes; the map stays part-built and studded.**
- **Time-of-day variety per round:** later.
- **Git:** one commit "Style test v2" allowed (done: `7e22b51`).
- **Holden saved the place** with File → Save to File (2026-10-06).
- **Next:** planning only (Map 1 full layout, Sky v3, hero traps in 2 routes, updated Map Plan, file list, build order). No building or uploads until he says go.

## Decisions from Holden (2026-10-06, answers on the v3 plan; v3 plan approved)
Plan: [[Trap-Your-Friends-v3-Plan]].
- **Uploads:**
  - Holden made an Open Cloud API key and saves it himself in `TrapYourFriends\.secrets\roblox_open_cloud_key.txt`. Claude must **never print, log, copy or commit the key**, and must check `.secrets/` is gitignored before using it.
  - Tools: `AssetLibrary/tools/upload_model.sh` for GLBs and the image script for textures.
  - **Every upload batch needs Holden's OK first** (renders + file list, then upload).
- **Prep:** Runners **can see the course but not the traps.** Traps stay invisible to Runners until the run starts.
- **Boxing Glove colour: blue** (never confused with the red Kill Brick or the TNT).
- **Hero traps:** a **grey-form stop for Wrecking Ball, Chomper and Boxing Glove** before texturing. Holden approves the shapes, then Claude textures.
- **Run timer: 3:30 (DRAFT).**
- **Checkpoints:** 4 + the finish is OK for now, as long as no leg is over **~40 s** for an average runner (flag any that is).
- **Zone 3:** a **3rd route (dungeon tunnel)** goes into the layout as DRAFT.
- **Trigger buttons: HUD buttons.** **Trapper names on the zone banners: yes.**
- **16-player debris work:** done with the full Map 1 greybox (step 4), not before.
- **Build order:** (1) Sky v3 → screenshots incl. a phone-width view and the low-graphics fallback; (2) Swinging Hammer grey forms in both routes (front/side/¾) → **STOP** for the pick.

## Draft (not approved; see the GDD)
Everything else in [[Trap-Your-Friends-GDD]]: team sizes, timers, the brick budget, the proof run rule, the trap list, scoring, modes, progression, monetisation and how destruction fits.

## Open questions for Holden
1. **Style lock:** direction A was chosen for the style test (2026-10-05). The final lock comes after Holden reviews the test.
2. **Avatars for the game:** the style test uses Holden's own R15 avatar. The game-wide choice (own R15 vs forced classic R6) is not recorded as final. Note: games that allow R6 reportedly lose MeshPart heads/accessories (⚠️ verify).
3. **Destruction scope:** destruction as **juice** (traps and runners smash bricks, lane rebuilds after a few seconds) or also as **gameplay** (runners can bash through Brick Wall traps)? Recommendation: both, with runner Bash as a v1 stretch.
4. Team sizes: 2v2 and 4v4 at launch? Server size 8?
5. Bots: allowed in public servers to fill empty teams, or only in tiny servers?
6. ~~Project folder location~~ **Resolved (Holden, 2026-10-05):** `C:\Users\holde\Documents\GameDev\TrapYourFriends` Holden approved `git init` there (no commits).

## Phase 0 status (2026-10-05)
- **Done:** `git init` (branch `master`, **no commits**). Scaffold copied from Rubber Tower's layout and local gate (RubberTower unchanged): `rokit.toml` (rojo 7.7.0, selene 0.32.0, stylua 2.5.2, lune 0.10.5), `selene.toml`, `stylua.toml`, `.luaurc` (strict), `.gitignore`, `.gitattributes`, `default.project.json` (leaves out `**/Dev*.luau`), `dev.project.json` (adds `tools/` → `ServerStorage.DevTools`), `.mcp.json` (gitignored), project `CLAUDE.md`, README, `src/server/Main.server.luau` + empty `Services/`, `src/client/Main.client.luau` + empty `Controllers/`, `src/shared/Config.luau` (every GDD number, tagged USER/DRAFT, none wired up), `src/shared/Types.luau`, `tests/Config.spec.luau`.
- **Gate 0, code part: PASS.** `gate.sh --scaffold .` → build, tests (6 specs), lint and format PASS (local run, 2026-10-05). `rojo build dev.project.json` also builds.
- **Gate 0, Studio part: PASS (2026-10-05).** In `places\StyleTest.rbxl` (Team Create, placeId 79250742543087; Holden clicked Rojo Connect), `rojo serve dev.project.json` synced, and a playtest printed exactly `[Boot] server ready: 0 services` and `[Boot] client ready: 0 controllers` with no errors.
- No Luau type checker is installed, so `--!strict` isn't machine-checked yet (known gate gap, [[Roblox Code Gate Skill]]).

## Phase 1 status: style test v1 (2026-10-05, awaiting Holden)
- Full log, counts, screenshots and Claude's honest read: [[2026-10-05-Trap-Your-Friends-Style-Test]].
- **Built:** direction A, Legacy vs Variant segment copies, six traps (markings from parts), the destruction prototype, the noob shatter demo (demo only), lighting preset module. Code gate PASS (24 specs).
- **Asset ids (private images, uploaded 2026-10-05 via Studio MCP `upload_image`, the only upload Holden approved):** stud colour map `rbxassetid://139618384581445`, stud normal map `rbxassetid://134190443469137`. Source: `TrapYourFriends/art/stud_tile/make_stud_tile.py` (procedural, nothing downloaded). Used by `MaterialService.TYF_Studs` (StudsPerTile 1).
- **New code** (uncommitted): `src/shared/{Remotes,Tags}.luau`, `src/shared/Rules/{CellTimers,DebrisPlan,Spinner}.luau` + specs, `src/shared/Lighting/{ModernRetro,Apply}.luau`, `src/server/Services/{DestructionService,TrapService}.luau`, `src/server/Util/Characters.luau`, `src/client/Controllers/{DebrisController,SpinnerController,TrapFxController}.luau`, `tools/BuildStyleTest.luau`. Dev-only (gitignored): `src/server/DevStyleTest.server.luau`, `src/client/DevHud.client.luau`.
- **Place file:** Claude can't save to file from the MCP. Holden saves with File → Save to File (overwrite `places\StyleTest.rbxl`). Studio edits are in the Team Create session meanwhile.
- **Open design points from the test (Holden's call):** the Spinner re-carves the Brick Wall forever, the stud method choice, and TNT vs Kill Brick readability from a distance.

## Kickoff review (Claude Code, 2026-10-05)
Claude Code read the notes and presented a plan and file list for phases 0 (Rojo scaffold) and 1 (style test). Conflicts it raised (all answered in the second "Decisions from Holden" block above):
- **Two diverged vault copies.** These notes live only in `E:\Vault`. That clone is at commit 519b154 (2026-10-04) with ~55 uncommitted changes. `C:\Vault` (canonical according to [[CLAUDE]]) is at 52c1c15 (2026-10-05) and has no Trap-Your-Friends folder. Holden needs to say which copy is the source of truth.
- "Really red is the only red in the game" ([[Trap-Your-Friends-Art-Style-Guide]]) vs the TNT Brick spec "red-and-white striped".
- Cracks, chevrons, stripes and "?" trap tells need decals/textures, and so does a home-made stud MaterialVariant. All of these need image uploads, which aren't authorised yet.
- [[Retro-Stud-Style-Guide]] says R6 + `Soft` lighting as a general rule. Direction A here says R15 + `Realistic`. Once the project guide is locked, it wins.
- The units of the TNT "3×3 hole" (studs or cells) and the destruction cell size are undefined. The segment is 35 long, so it can't be split into 2-stud cells.
- In the JJS2 still the debris cubes look plain/smooth at contact-sheet resolution. Studded debris is our design choice, not a confirmed JJS detail.
- Lighting is global in Roblox, so A and B can only be **toggled**, not shown side by side. Avatar rig type (R6/R15) is also game-wide.

## Related
[[Trap-Your-Friends-GDD]] · [[Trap-Your-Friends-Art-Style-Guide]] · [[Trap-Your-Friends-Reference-Board]] · [[Trap-Your-Friends-Claude-Code-Prompt]] · [[Retro-Stud-Style-Guide]] · [[Retro-Party-Deep-Dive-2026-10-05]] · [[Trap-Your-Friends-v3-Plan]] · [[Trap-Your-Friends-Map1-Layout]] · [[Trap-Your-Friends-Sky-v3-Plan]] · [[Trap-Your-Friends-Hero-Traps-Plan]] · [[Trap-Your-Friends-Map-Plan]] · [[Trap-Your-Friends-Round-Structure]]

## Sources
- Planning conversation with Holden, 2026-10-05 (Cowork chat).
