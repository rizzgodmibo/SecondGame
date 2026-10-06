---
tags: [project/trap-your-friends, visuals/3d, visuals/art-direction]
status: draft
updated: 2026-10-06
confidence: low
---
# Trap Your Friends: hero traps, fixing "cheap" (PLAN ONLY)

## TL;DR
- **Why:** (USER, 2026-10-06) v2 traps "function fine, outline is decent, but they look low quality / cheap". **Traps move to Blender meshes; the map stays part-built and studded.**
- **Step 1: Swinging Hammer as grey forms in BOTH routes.** Holden picks a route before any texturing.
  - **Route A, voxel detail:** 0.25–0.5-stud cubes with bevel/inset tiles, merged into one mesh with an atlas (the Grow a Garden / Steal a Brainrot look).
  - **Route B, smooth chunky toon:** bevelled forms + a painted texture bake, at Rubber Tower v5 quality.
  - Renders: front, side and three-quarter for each route, plus a silhouette check and a scale check next to an R15 stand-in.
- **Step 2:** the other 3 hero traps (**Wrecking Ball, Chomper, Boxing Glove Wall**) in the chosen route → grey forms → **Holden approves the shapes (USER, 2026-10-06: a grey-form stop)** → textures → review → upload.
- **Answers (USER, 2026-10-06):**
  - **Boxing Glove = blue.**
  - **Uploads:** Open Cloud key in `TrapYourFriends\.secrets\roblox_open_cloud_key.txt`. Never print, log, copy or commit it; check the gitignore first. Every upload batch needs Holden's OK on renders + file list.
- **Rules for every trap:**
  - shape language per family; the face designed into the form; colour zones with variation; studs on top faces;
  - **< 10k triangles**, **texture ≤ 1024²**, no vertex colours, one GLB per trap;
  - squash/stretch on tell and hit, overshoot on recover, idles out of sync.
- **Outline:** compare **Highlight vs a baked inverted hull** on the Hammer and the Wrecking Ball (look and cost) before deciding.
- **Banned:** Roblox AI meshes and Hunyuan3D. **No uploads** until Holden approves the renders. Uploads go through the Open Cloud key (USER).


## Status: Step 2 Hammer grey forms built (2026-10-06), STOP for Holden's route pick
- **Built** with `TrapYourFriends/art/traps/hammer/build_hammer_grey.py` (Blender 5.2, headless, from scratch; no AI meshes). One design with the v2 gameplay sizes: pivot 10 studs above the floor, arm 7.5, head about 4.4 × 2.8 × 2.8.
- **Pieces:** `Mount` (static) + `Arm` (swings). Studs only on the head top and the mount top.
- **Triangles:**
  - Route A (voxel) **5,200** (mount 960 + arm 4,240);
  - Route B (smooth toon) **6,162** (mount 980 + arm 5,182): over the 6k target, under the 10k limit, trimmable later.
- **Route A details:**
  - 0.25-stud cubes, one grey bevel/inset tile per cube face (`grey/voxel_tile_grey.png`);
  - a **hand-placed pixel-art face** (stepped angry brow, recessed eyes, checker gritted teeth). Sampling the smooth face onto the grid read as noise, so voxel faces must be designed for the grid;
  - square-section handle and bands.
- **Route B details:** bevelled forms, sculpted V brow, eyeballs deep in boolean-cut sockets, two staggered rows of teeth, steel strike caps, bands next to the caps, a wrapped handle and collar.
- **Sheet:** `attachments/tyf-v3-hammer-grey-sheet.png`: front / side / three-quarter / scale with an R15-size stand-in / silhouettes front and side, both routes. Single shots: `tyf-v3-hammer-grey-{A,B}-{front,threequarter,scale}.png`.

![[tyf-v3-hammer-grey-sheet.png]]

**Claude's honest read** (grey only; colour, pupils and texture come after the pick):
- **Same silhouette:** both routes share one design, so the pick is about **surface language**, not shape.
- **Route A:**
  - **for:** clearly "built from blocks", so it belongs in the studded brick world and matches the debris;
  - **against:** the face reads in front and three-quarter, but at phone size the cube grid turns into texture noise, and curves (the caps) step.
- **Route B:**
  - **for:** the face reads at a glance (brow, eyes, teeth) and the forms look finished;
  - **against:** closest to the Rubber Tower kit, so it risks looking like a generic toon prop unless colour and studs tie it to the world.
- **Weak in both:**
  - the mount reads like a box or lantern from the side;
  - the handle is long and thin next to the chunky head (fine for the swing read, plain on its own).
- **Lean:** Route B for phone readability, maybe with voxel-style stud details. Holden decides; nothing gets textured before his pick.

## The two routes (Hammer first)
| | Route A: voxel detail | Route B: smooth chunky toon |
|---|---|---|
| Look | Built from small cubes (0.5 studs on big forms, 0.25 on the face and details). Each cube face carries a bevel highlight and an inset dark line from a tile atlas. Merged into one mesh | Bevelled superellipsoid/box forms, chunky proportions, a painted bake (light top, dark underside, edge highlight, hard-edged details), like the approved Rubber Tower v5 kit |
| Fits the world | Strong: cubes match the studded brick map and the destruction debris | Good: the Rubber Tower look players already like; contrasts with the blocky map (traps pop out) |
| Faces | Pixel-art eyes and mouth from 0.25 cubes (crisp, but expression is limited by the grid) | Sculpted brow ridges, recessed eye sockets, painted pupils (more expressive) |
| Squash/stretch | Works (whole-mesh scale), but stretched cubes show the distortion more | Natural |
| Triangles (Hammer est.) | ~4–9k after merging coplanar faces and dropping hidden ones (0.25 everywhere would go over 10k, so 0.25 only for details) | ~2–5k |
| Pipeline | New: a voxeliser script (shape → occupancy grid → surface quads → atlas UVs) on top of `kitlib6` | Proven: `kitlib5.bake_object` (1024 bake), `kitlib6` superellipsoid/face/cap helpers, `export_glb` |
| Risk | Curves alias into stair steps; looks noisy at phone size if the cubes are too small | Can look like any generic toon asset if the studs and bricks don't tie it to the world |
- **Claude's lean:** Route B for creatures (Chomper) and Route A for mechanical traps (Hammer, Glove wall) could also work as a mix. Holden picks after seeing the grey forms; nothing is decided.

## Per-trap specs (DRAFT; colour zones stay within the style guide palette, ±5–8% variation per DRAFT exception)
| Trap | Family / shape language | Face (built into the form) | Colour zones | Stud details | Moving parts (separate MeshParts) | Tris / texture |
|---|---|---|---|---|---|---|
| **Swinging Hammer** | Danger: angular, chamfered wedge head, metal bands, a thick handle | Angry brow ridge across the head front, recessed eye sockets, gritted teeth on the strike face | Iron head (two greys), lighter steel strike faces, brass bands, wood handle with a wrap, yellow gantry | On the head top and the gantry beam | Gantry (static) · arm + head (one swinging piece) | < 6k · 1024² atlas |
| **Wrecking Ball** | Danger and heavy: a round mass with angular riveted plates and blunt spikes | A huge toothy grin carved into the ball, small fierce eyes above | Dark iron ball, lighter plates, brass rivets, steel chain | On the gantry top and a cap plate on the ball | Gantry · chain (one link mesh reused ×8) · ball | < 8k · 1024² |
| **Chomper** | Creature: blob + teeth, squat on a 2×2 socket | Oversized jaw with angular cream teeth, tongue, eyes on top of the head | Teal/green body with a lighter belly, pink mouth, cream teeth, dark gums | Row of studs down its back | Body · upper jaw · lower jaw | < 7k · 1024² |
| **Boxing Glove Wall** | Bounce/punch: round and squashy glove on an angular wall mount | Cheeky face on the glove back (eyes + grin), or none if the glove silhouette reads better without | **Blue glove (USER, 2026-10-06)** with ±5–8% variation, white cuff band, laces, a brick wall plate, dark spring arm | On the wall plate top | Wall plate (static) · accordion arm · glove | < 7k · 1024² |
- **Boxing glove must read as a glove** (v2 read as "a pink ball"):
  - a clear **thumb lobe**;
  - a **knuckle ridge**;
  - a separate **cuff** with a trim band;
  - **criss-cross laces** on the palm side.
  - Check: a black silhouette render must still read as a glove from the side and three-quarter.
- **Glove colour: blue (USER, 2026-10-06),** so it is never confused with the red Kill Brick (Really red) or the TNT (Bright red + white bands).

## Animation list (client-side visuals; server hitboxes unchanged)
| Trap | Idle | Tell (0.4 s) | Hit | Recover |
|---|---|---|---|---|
| Hammer | Sway ±6° (existing), blink | Pull back 70° with anticipation squash (head −10% along the swing), brow drops | Stretch +15% along the motion at peak speed, impact squash on contact | Overshoot ~8° past rest, settle |
| Wrecking Ball | Grin "breathing" (±3% scale), eyes dart | Eyes widen, chain tension wobble | Squash 12% on wall contact (existing wall-smash) | Natural pendulum overshoot |
| Chomper | Breathing squash, eyes look around | Jaw opens wide, body stretches up 15% | Snap shut with a 20% squash down | Wobble overshoot, chew loop |
| Boxing Glove | Bob and flex | Pulls back + wiggle | Stretch 20% along the punch, arm extends, squash on contact | Retract with overshoot |
- **Every idle starts at a random phase and runs at ±10% speed,** so traps never move in sync. Squash/stretch = client-side `MeshPart.Size` scaling around a pivot; motion stays deterministic from `GetServerTimeNow()` (existing `Motion` module).

## Outline comparison (Hammer + Wrecking Ball)
| | Highlight (current) | Baked inverted hull |
|---|---|---|
| How | One `Highlight` per trap model, black, `DepthMode = Occluded` | A flipped-normal shell, ~0.05–0.08 studs out, in the same mesh, black in the atlas |
| Look | Even pixel-width outline at any distance; outlines the silhouette only | Outlines inner edges too (jaw, thumb); gets thinner with distance; can show gaps on sharp corners |
| Cost | +1 draw call per model + a post pass when any is on screen; limit 255 (2025-11-10) | ~2× triangles, no extra pass; batches with the mesh |
- **Test:** the same 3 distances (5, 20, 60 studs) + a phone-width downscale; draw calls and frame time from render stats. Decide per family: a hull on near-only traps is possible.

## Pipeline (per trap)
1. **Dedicated Blender export scene** `TYF_Export_<Trap>`, built by a script (`art/traps/<trap>/build_<trap>.py` on `kitlib5`/`kitlib6`; Route A adds `art/traps/voxelise.py`).
2. **Grey form renders** (front, side, three-quarter, silhouette, scale next to an R15 stand-in) → **Holden reviews.**
3. **Texture:**
   - painted bake (Route B) or tile atlas (Route A), 1024² **PNG** (AssetLibrary lessons: PNG not JPEG; avoid the `image.save` black-PNG bug);
   - **no vertex colours** in the export.
4. **Colour renders + animation preview** (a turntable and the tell/hit/recover poses) → **Holden reviews.**
5. **Export:**
   - one GLB per trap, `export_glb(use_selection=True, use_active_scene=True)`;
   - moving pieces as separate objects with clean pivots;
   - names like `TYF_Hammer_Arm`.
6. **Preflight** with the `roblox-asset-pipeline` skill: scale in studs, triangle count, pivots, names, texture size, no vertex colours.
7. **Upload** with the Open Cloud scripts (below, after Holden's OK) → insert into Studio → MeshParts + `SurfaceAppearance`/`TextureID`. `CollisionFidelity` Box/Hull: traps hit with server spheres; only static bases collide.
8. **Wire** into the existing trap modules: swap the part models for mesh models and keep the attribute and Rig contract.

## Upload route (USER, 2026-10-06: Open Cloud key)
- **Key file:** Holden saves the key himself in `TrapYourFriends/.secrets/roblox_open_cloud_key.txt`.
  - Claude created only the **empty** file (2026-10-06) and confirmed `git check-ignore` matches `.gitignore: .secrets/`.
  - Claude **never prints, logs, copies or commits the key**, and re-checks the gitignore before each batch.
- **Tools:**
  - GLBs: `AssetLibrary/tools/upload_model.sh` (creator MiboRBX; never prints the key);
  - textures and skybox images: `AssetLibrary/tools/upload_image.sh`.
- **Every batch:** renders + file list to Holden → his OK → upload → ids logged in the hub asset table and the AssetLibrary README.

## Pitfalls
- **The face must belong to the form.** No stuck-on googly eyes (the v2 "cheap" cause).
- **Silhouette first:** if the black silhouette doesn't read, texture won't save it.
- **Studs:** keep them to top faces. Studs all over turned the v2 walls into giant LEGO.
- **Squash/stretch** must not change server hitboxes. It's purely visual.

## Related
[[Trap-Your-Friends]] · [[Trap-Your-Friends-v3-Plan]] · [[Trap-Your-Friends-Trap-Catalogue]] · [[Trap-Your-Friends-Art-Style-Guide]] · [[Trap-Your-Friends-Style-Test-v2-Feedback]] · [[Rubber-Tower-Art-Style-Guide]] · [[Blender-To-Roblox-Pipeline]] · [[2026-10-06-Trap-Your-Friends-Style-Test-v2]]

## Sources
- Holden's v3 planning prompt, 2026-10-06 (Route A/B, the hero trap list, the rules above).
- ⚠️ **Flag (2026-10-06):** Holden says section 4 of [[Trap-Your-Friends-Style-Test-v2-Feedback]] now holds the Route A/B and reference-study text. The E:Vault copy has only sections 1–3 (checked twice; last modified before his message). C:Vault has no Trap-Your-Friends folder. This plan follows the Route A/B wording in [[Trap-Your-Friends-Prompt-v3]] until the section shows up; then re-check that they match.
- Reference stills: `Assets/Reference-Captures/Retro-Stud/sky-model-study-a-gag-sab-fisch.jpg` (voxel models of small inset-tile cubes), `sky-model-study-b-babft-bss-doomspire.jpg` (observations).
- AssetLibrary README and `models/rubber-tower-kit-v5`, `rubber-tower-kit-v6-map` scripts (kitlib5/kitlib6 helpers, PNG lessons), read 2026-10-06.
- Highlight limit 255 (Roblox, 2025-11-10) via [[Trap-Your-Friends-Style-Test-v1-Feedback]].
