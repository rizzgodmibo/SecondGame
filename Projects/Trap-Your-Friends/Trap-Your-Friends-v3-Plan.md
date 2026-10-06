---
tags: [project/trap-your-friends, meta/plan]
status: draft
updated: 2026-10-06
confidence: medium
---
# Trap Your Friends: v3 plan (build order, files, gates). APPROVED by Holden 2026-10-06

## TL;DR
- **v3 fixes Holden's v2 verdict** (USER, 2026-10-06): the sky is terrible, the traps look cheap, the map is too small. 16 players = 4 Trappers + 12 Runners, fixed zones.
- **The plans:**
  - [[Trap-Your-Friends-Map1-Layout]]: the full Map 1 layout + image;
  - [[Trap-Your-Friends-Sky-v3-Plan]]: the living sky;
  - [[Trap-Your-Friends-Hero-Traps-Plan]]: Route A voxel vs Route B smooth toon;
  - [[Trap-Your-Friends-Map-Plan]]: Maps 2/3 at the new size.
- **Build order:** Holden's, plus a small Step 0 (wire the 18 uploaded sounds) and one extra stop:
  - **0** sounds;
  - **1** Sky v3: **stop at the mockup before uploads**, then stop with Studio shots;
  - **2** Hammer grey forms in both routes → **stop for the pick**;
  - **3** the other 3 hero traps: grey forms → **stop**, then textured + outline test → **stop**;
  - **4** the full Map 1 greybox, audited → **stop**.
- **Approved by Holden (2026-10-06)** with the answers below. Uploads still need his OK per batch. Holden makes the commits.
- **Progress (2026-10-06):** Step 0 done (sounds wired, gate PASS, all 18 load in Studio). Step 1a done (Sky v3 mockup + meshes + code; preflight PASS) → **stopped for the upload OK**. Step 2 (Hammer grey forms) comes after the Sky v3 Studio shots.

## Build order with gates
| Step | What | Gate (must pass before the stop) | What Holden sees at the stop |
|---|---|---|---|
| **0. Sounds** (small) | Put the 18 uploaded ids into `Audio/Sfx.luau`; candidate "a" plays by default. A Studio-only A/B toggle in the dev Trapper panel | Code gate PASS; playtest console clean | A short list of which sound plays on which trap; he picks a/b by ear (no separate stop, reported with Step 1) |
| **1a. Sky mockup** | Gradient faces + sun + 4–5 cloud variants (grey → toon) + 3 silhouettes in Blender; a mockup render | Faces seamless (preview sheet); clouds < 800 tris; textures PNG ≤ 1024²; asset-pipeline preflight | **STOP:** mockup at 1920×1080 + a phone frame, the cloud contact sheet (front/side/¾), the sun, the face preview. **Approve before upload** |
| **1b. Sky in Studio** | Upload (9 images, ~8 meshes); `SkyMoods` + `SkyLayersController` + `CloudDrift` (+ spec); Map 1 mood | Code gate PASS; frame time measured with Studio in front; render stats | **STOP:** 4 shots × high/low quality (8), phone-width view, draw calls/tris/frame time, honest critique |
| **2. Hammer grey forms** | Route A (voxel) and Route B (smooth toon) Hammer in Blender, grey only | Each < 10k tris; clean pivots; silhouettes read | **STOP:** front / side / ¾ / silhouette / scale vs R15 for **both routes** on one sheet, Claude's honest read. **Holden picks the route** |
| **3a. Hero grey forms** | Wrecking Ball, Chomper, Boxing Glove Wall in the chosen route, grey | Same; the glove silhouette must read as a glove | **STOP:** the same sheet for the 3 traps |
| **3b. Hero traps finished** | Textures (1024² atlas each), colour zones, faces, studs; animation (squash/stretch, overshoot, random-phase idles); the outline test (Highlight vs inverted hull) on Hammer + Wrecking Ball; upload; swap into the trap modules | Code gate PASS (new `Rules/Squash` spec); asset preflight; frame time in Studio; no server errors in a playtest | **STOP:** colour renders before upload, then Studio close-ups of all 4, a tell/hit/recover frame strip, the outline comparison (3 distances + phone width, draw calls), honest critique |
| **4. Map 1 greybox** | The full layout from `map1_layout.json` in studded parts with zone colours (no final art), 44 sockets tagged, 4 checkpoints + finish, start room, 4 lookouts, beacon; StreamingEnabled settings; 12 Studio-only noob runners for timing | `roblox-map-audit` PASS (`MapMustReach`/`MapNoReach`); counts within budget (parts ≤ 12k, draw calls < 1,000, tris < 1M in view); frame time with Studio in front; noob run times logged | **STOP:** top-down Studio shot next to the plan image, per-zone shots, phone-width view, counts, noob run times vs the 2:30–3:00 target, honest critique |

- **Proposed later (not in Holden's order; ask first):** the 16-player debris work, i.e. quality tiers, distance LOD and a distance-filtered `Fractured` ([[Trap-Your-Friends-Map1-Layout]] § Debris). Needed before any 16-player test. Checkpoint/respawn, zone ownership, the Trapper HUD and the round loop are game systems for after the style lock.

## File list (planned; `TrapYourFriends/` repo unless noted)
| Step | New | Changed |
|---|---|---|
| Planning (done now, uncommitted) | `design/map1/make_layout.py`, `design/map1/map1_layout.json`, `design/map1/map1_sections.md`, `design/map1/render_layout.ps1` | `src/shared/Config.luau` + `tests/Config.spec.luau` (16 players, 4 zones; gate PASS) |
| 0 | none | `src/shared/Audio/Sfx.luau`, `src/client/DevTrapperPanel.client.luau` (Dev, gitignored) |
| 1 | `art/sky_v3/make_gradient_sky.py`, `make_sun.py`, `clouds_blender.py`, `silhouettes_blender.py`, `render_mockup.py`; `src/shared/Lighting/SkyMoods.luau`; `src/shared/Rules/CloudDrift.luau` + `tests/CloudDrift.spec.luau`; `src/client/Controllers/SkyLayersController.luau` | `src/shared/Lighting/Apply.luau`, `CastleSky.luau`, `ModernRetro.luau` (Atmosphere back on) |
| 2 | `art/traps/common.py` (export scene, render sheet), `art/traps/voxelise.py` (Route A), `art/traps/hammer/build_hammer_a.py`, `build_hammer_b.py` | none |
| 3 | `art/traps/wrecking_ball/build.py`, `chomper/build.py`, `boxing_glove/build.py`, `art/traps/export/*.glb`; `src/shared/Rules/Squash.luau` + `tests/Squash.spec.luau`; `tools/StyleTestV3/HeroTraps.luau` (places the test models) | `src/client/Controllers/TrapAnimController.luau` (squash/stretch, overshoot, random phase), `OutlineController.luau` (distance culling, hull test toggle), `src/server/Traps/{SwingingHammer,WreckingBall,Chomper,BoxingGlove}.luau` (mesh models, same attribute/Rig contract) |
| 4 | `design/map1/to_luau.py` → `tools/Map1/LayoutData.luau`; `tools/Map1/{Build,Kit,Route,Zones,Sockets,Checkpoints,StartRoom,Lookouts,Landmarks}.luau`; `src/server/DevMap1Noobs.server.luau` (Dev, gitignored) | `src/shared/Rules/Sockets.luau` (+ zone id), `src/shared/Tags.luau` (Checkpoint, Lookout, Zone tags) |
| Vault | `attachments/tyf-v3-*` renders and shots; playtest logs `Playtests/2026-10-xx-Trap-Your-Friends-v3-*.md` | hub, the Sound List (ids → wired), the style guide (verdicts), Gap-Tracker, Verification-Log |
| AssetLibrary | `audio/catalogue.json` (done: 18 sounds logged) | `README.md` lessons, and an asset-ids entry per upload |

## Studio instances for Holden to delete (Step 0 of the planning prompt)
- `ServerStorage.StyleTestV1`: the v1 build (1,038 descendants); its code is gone.
- `ServerStorage.Baseplate_Template`.
- `ServerStorage.SpawnLocation`: the v1 template spawn.
- Optional: `Lighting.DepthOfField` (disabled, unused).
- **Keep:** `ServerStorage.DevTools`, `ServerStorage.__Rojo_SessionLock`, `Workspace.StyleTestV2`, `MaterialService.TYF_Studs`, Lighting `Sky`/`SunRays`/`Atmosphere`/`Bloom`/`ColorCorrection`.
- Vault file: `attachments/tyf-v2-10-phone-844x390.png` (superseded crop).


## Flags (disagreements between notes and code)
- ~~Prep visibility~~: resolved (USER, 2026-10-06). Runners see the course, not the traps.
- ~~Run timer~~: resolved (USER, DRAFT 3:30). `Config.Round.RunSeconds = 210`; gate PASS (45 specs).
- **`Config.Round.TrapBudget = 30` per Trapper** (DRAFT) was set for 30 sockets per map. With 44 sockets and merged zones, it may need to scale with the number of zones a Trapper owns. Still open.
- **v2 feedback note:** Holden says section 4 (Route A/B + reference study) is now in [[Trap-Your-Friends-Style-Test-v2-Feedback]], but the E:\Vault copy still has only sections 1–3 (checked 2026-10-06). The Hero Traps plan follows [[Trap-Your-Friends-Prompt-v3]] until the section shows up.
- **Checkpoints:** 4 + finish is OK (USER) if no leg is over ~40 s. **Market Rooftops leg = 41 s (flagged)**; two Zone 3 legs are 38 s (borderline). Leg table in [[Trap-Your-Friends-Map1-Layout]].

## Holden's answers (USER, 2026-10-06), also in the hub
1. **Uploads:**
   - Open Cloud key in `TrapYourFriends/.secrets/roblox_open_cloud_key.txt` (Claude made only the empty file; gitignore confirmed). Never print, log, copy or commit the key.
   - `upload_model.sh` for GLBs, `upload_image.sh` for images.
   - **Every batch needs his OK** on renders + file list.
2. **Prep:** Runners see the course but not the traps.
3. **Boxing Glove:** blue.
4. **Grey-form stop** for the other 3 hero traps: yes (Step 3a).
5. **Run timer:** 3:30 (DRAFT).
6. **Zone 3:** the 3rd route (dungeon tunnel) goes in as DRAFT.
7. **Triggers:** HUD buttons.
8. **Zone banners:** show Trapper names.
9. **16-player debris work:** with the Step 4 greybox.
10. **Build now:** (1) Sky v3 → screenshots incl. phone width + the low-graphics fallback; (2) Hammer grey forms in both routes → STOP for the pick.

## Related
[[Trap-Your-Friends]] · [[Trap-Your-Friends-Map1-Layout]] · [[Trap-Your-Friends-Sky-v3-Plan]] · [[Trap-Your-Friends-Hero-Traps-Plan]] · [[Trap-Your-Friends-Map-Plan]] · [[Trap-Your-Friends-Round-Structure]] · [[Trap-Your-Friends-Style-Test-v2-Feedback]] · [[2026-10-06-Trap-Your-Friends-Style-Test-v2]] · [[Trap-Your-Friends-Sound-List]]

## Sources
- Holden's v3 planning prompt and verdict, 2026-10-06.
- Studio instance list read via the Studio MCP, 2026-10-06; repo state at commit `7e22b51 Style test v2` + the uncommitted Config/planning files above.
