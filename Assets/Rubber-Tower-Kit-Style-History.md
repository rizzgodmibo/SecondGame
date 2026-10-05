---
tags: [assets/models, project/rubber-tower, visuals/art-direction]
status: reviewed
updated: 2026-10-04
confidence: high
---
# Rubber Tower Kit: Style History (v1 to v5)

Split out of [[Rubber-Tower-Valley-Kit]] on 2026-10-04. How the kit style evolved through Holden's reviews. **v5 is the locked style** ([[Rubber-Tower-Art-Style-Guide]]).

## v5 style test (2026-10-04): painted textures, climbable
**How it's built:**
- `RubberTower/art/build_styletest_v5.py` with the helpers in `art/kitlib5.py`, run as headless Blender 5.2 plus Cycles bake.
- Output goes to `art/kit_v5_styletest/` (models, textures, previews, `build_report.json`).

**Texture method (new):**
- Every face has a surface type (rock, grass_top, grass_drape, blade, dirt, wood_x/y/z, rope, stone, gold, banner, crystal, leaf, flowers…).
- Each type is a procedural "paint" shader, emission-baked into **one 1024² texture per mesh** (512² for the ground apron). The bake takes about 6 s per model.
- Every pattern uses a hard threshold, so nothing is blurry:
  - rock: cracks (Voronoi edges, patchy), strata lines, facet patches;
  - grass: two-tone zones, stipple, clover;
  - wood: grain and nails;
  - stone: triplanar bricks with moss in AO creases.
- The bake adds **AO in creases** (AO node) and a **light rim on exposed edges** (Bevel node normal vs face normal, masked by AO).
- Tones run darker at the bottom and lighter at the top over the model height.
- Glow parts stay untextured `_Glow` MeshParts that become Neon.

**Geometry:** chipped bevelled rock masses, an irregular double-sided grass-blade fringe, tufts, oversized bent flowers, pebbles, a wooden scaffold ledge with rope bindings, and a crooked signpost.

| Model | Parts (tris) | Notes |
|---|---|---|
| Obby_Wall_A | Body 3,164 · Ledges 3,070 · Props 1,132 · Ground 498 · Glow 176 (**8,040 total**) | 68 wide × 64.5 tall. 12 ledges with walk heights every 5 studs (+2 for the apron) and 2–4 stud gaps; ledge 5 is a wooden scaffold. Collider boxes are in the build report, and Studio colliders come from `tools/DevStyleTestStage.luau` |
| Checkpoint_Islet | 1,630 + 66 | Radius 11. The walk surface is 10.9 above the bottom. The beacon sits on it |
| Meadow_Islet_M | 1,380 + 44 | Radius 7, a puffy 4-puff bush, goofy flowers, hanging roots |
| Crystal_Cyan | 502 + 132 | Painted crystals with white edge highlights, plus Neon shards |
| Checkpoint_Beacon | 1,194 + 286 | Brick pillars with crooked blocks, a leaning arch (3°), a gold keystone and caps, banners, a rune ring, a crystal crown |

- **Preflight:** PASS for all 5 models, 0 FAILs.
- **Preflight warnings (all intentional):**
  - **normals:** the reversed twins of double-sided blades and cloth.
  - **colour-variation:** the single-colour Neon glow parts.
  - **origin:** offset parts in multi-part models.
- **Budget note:** the wall section is 8k tris, over the v4 guide's 3k backdrop budget. A climbable hero section with painted detail needs more. ⚠️ verify phone performance in Studio's device emulator and on Holden's phone once several sections are placed.

**Self-check of the Blender previews** (not the real test: Holden wants it judged in Studio):
- The wall reads as a solid cliff with the steps visible.
- The islet and beacon look much less like plastic.
- The rock masses are still a little boulder-like.

**Upload blocked (2026-10-04):**
- Claude Code's permission system blocked using the Open Cloud key, because the only key file is in the Fish a Monster project's `.secrets`.
- Holden can upload himself, put a key in `RubberTower/.secrets/`, or import the GLBs with Studio's 3D Importer into `workspace.StyleTest_v5`.

## v4 style test (2026-10-04)
- **Built by** `RubberTower/art/build_styletest_v4.py`, using the shared helper library `art/kitlib.py`, both scripted in headless Blender 5.2.
- **Output:**
  - Models in `art/kit_v4_styletest/` (GLBs plus `RT_ValleyKit_v4_styletest.blend`).
  - One 256² atlas.
  - Glow parts are separate `<name>_Glow` children, to become Neon in Studio.
- **Renders:** Eevee, a sun, and a cyan sky (#11E3FE) for camera rays. Lighting uses a neutral sky, because the saturated sky tinted the shadows teal.
- **Sheets:** v3 | v4 | reference(s), in `Assets/Rubber-Tower-Valley-Kit/v4-styletest/`.

![[Sheet_Diorama.png|700]]
![[Sheet_Cliff.png|700]]
![[Sheet_Islet.png|700]]
![[Sheet_Beacon.png|700]]
![[Sheet_Crystals.png|700]]
![[Sheet_Obelisk.png|600]]
![[Sheet_Portal.png|700]]

| Model | Tris (body + glow) | References → what was taken | How close (honest) |
|---|---|---|---|
| Cliff_Rock_A | 2,418 + 324 (budget 3,000), 71 × 35 × 111 | **OmniKoi2 img-1:** warm tan masses of very different sizes, lime caps on every top, stepped ledges. **img-2:** caps spilling over. **Mossy Rocks:** rounded faceted masses | **Close in colour and caps.** Weak: the masses are tall vertical columns, while OmniKoi2's are wider and lumpier. Still a little "stacked", but no back slab or grey. Crystals are small at backdrop distance |
| Meadow_Islet_M | 600 + 68 | **OmniKoi2 img-1:** two-tone lime top, darker drape, tan underside. **Mossy Rocks:** chunky rock body under a grass cap | **Good silhouette and colours.** Weak: the bush is a yellow-lime lump, not a puffy OmniKoi2 canopy. The under-crystal is tiny. (The PPT v6 wide image was the wrong ref: it is a snow and sled thumbnail, so it was swapped out) |
| Checkpoint_Beacon | 824 + 316 | **haooffiso:** white/lavender stone, gold trim, glowing portal goal. **DKEaterrr ruin portal:** rune plates on pillars | **Good.** It reads as magic at a glance: a glowing rune ring, gold keystone, blue banners and a floating crystal crown. Weak: no vines or moss tying it to S1 |
| Crystal_Magic_Cyan / Magenta / Gold | 144 + 226 | **haooffiso:** glowing accents. **OmniKoi2:** lime cap base | **Good after the fix:** saturated 3-tone crystals (they rendered almost white at emission 0.55; now 0.3 with more saturated light tones). There's no dedicated crystal reference yet; find one in batch S3 |
| Rune_Obelisk_Floating | 770 + 124 | **haooffiso:** white stone and gold. **OmniKoi2:** capped floating rock | **Weakest.** Thin and small: the chains read as dotted lines and the orbiting rune stones are tiny at 150 px. Needs a fatter obelisk, bigger runes and a glowing band |
| Magic_Portal | 1,052 + 224 | **haooffiso:** glowing portal gate. **DKEaterrr ruin portal:** ring with vines | **Readable.** Weak: the vines are thin green sticks. The swirl is flat bands, not a spiral |
| Diorama | n/a | Framed like OmniKoi2 img-1 | **Closest to the target:** canyon walls, checker ground, sand path with an outline, glow accents. Missing trees (next batch), a waterfall and depth layers |

**Fixes made during the test (pipeline lessons):**
- 8-bit image pixels are already sRGB. An extra conversion washed out the sampled palette.
- `bmesh.ops.bevel` rebuilds faces, so recolour every face not in the "before" set, or only the bevel strips get coloured.
- Library-append the v3 models and call `view_layer.update()` before framing. A moved glTF import without a depsgraph update gave a blank panel.
- A saturated sky as world light tints shadows. Use LightPath "Is Camera Ray" to split the visible sky from the lighting.
- The cliff's triangle count depends on the random layout as much as on `n`. The cuts that actually worked were: no caps on hidden core tiers, fewer top-ring points, and wider minimum masses.

**Preflight:**
- `PREFLIGHT RESULT PASS objects=16 fails=0 warns=9`.
- 8 WARNs are `_Glow` origins. They are intentional: a glow part shares its parent's origin so it lines up when placed.
- 1 WARN is the obelisk body, whose lowest point sits above the origin because its glowing pendants hang lower.

## Kit v3 contents (2–3 sizes per platform type)
| Group | Models | Tris | Use |
|---|---|---|---|
| Backdrop | Cliff_Wall_A / _B, Cliff_Peak_A / _B, Cliff_Arch, Cliff_Waterfall, Corner_Spire | 506–1,586 | Mountain walls of chunky faceted rock masses. Modules are 64 wide × 96 tall, with peaks on top. The arch window (30 × 48, starting 26 up) shows the world outside. The waterfall has a splash pool. Fronts face Blender −Y |
| Far background | Distant_Mountain_A / _B, Cloud_Puff_S / _L | 130 / 2,240 | Snow-capped ranges outside the walls (low saturation), smooth-shaded clouds |
| Ground | Meadow_Ground (240×240 crisp zones, sand path, plaza), Pond, Start_Gate, Boulder_S / M / L, Flower_Patch_S / L | 76–956 | The valley floor |
| Segment 1 (meadow) | Meadow_Islet_S / M / L, Mossy_Ledge_S / M, Flower_Bounce, Checkpoint_Island | 104–1,466 | Path platforms, wall-terrace ledges, bounce pad, checkpoint island |
| Landmarks | Checkpoint_Beacon (stone arch, crystal crown, banners), Summit_Crystal (45 tall, gold) | 234–580 | Studio adds light beams |

## Renders
![[_Diorama_ground.png|600]]
![[_Diorama_overview.png|600]]
![[Cliff_Wall_A_front.png|260]] ![[Cliff_Arch_front.png|260]] ![[Cliff_Waterfall.png|260]]
![[Start_Gate_front.png|240]] ![[Checkpoint_Beacon.png|240]] ![[Summit_Crystal.png|200]]
![[Meadow_Islet_M.png|240]] ![[Flower_Bounce.png|240]] ![[Distant_Mountain_A.png|240]]
(The images are in `Assets/Rubber-Tower-Valley-Kit/v3/`.)

## Honest critique (my own, before Holden's review)
- **Cliffs:**
  - v3a was weak: random triangles read as crumpled paper, the waterfall was a checkerboard, and the arch was cardboard pillars.
  - v3b rebuilt them from overlapping faceted rock masses. They now read as a rock face, and the waterfall has vertical streaks.
  - Remaining: the masses are still fairly rectangular and similar in size. Up close they can look like stacked blocks. The top edge needs grass and trees, to be added in Studio from Holden's library.
- **Checkpoint beacon:** v3a had stick pillars and loose banners. v3b uses stacked-stone pillars like the gate, a semicircular arch and a crystal crown. Good.
- **Start gate:** clean and readable.
- **Islets:** good shape, now with bigger flowers and hanging vines. Their undersides render dark in Workbench light.
- **Flower bounce pad:** readable, but the pinks are muted.
- **Ground:** crisp curved zones, the olive tone fixed. Still sparse until trees, boulders and flower patches are placed in Studio.
- **Clouds and distant mountains:** fine as background. The clouds render grey in Workbench; check them under Roblox light.
- **Not yet checked in Roblox lighting.** Colours in Workbench are darker than in game.

## Pipeline lessons (v3)
- **Blender MCP safe mode** blocks lambdas, `os`, `exec` and `bpy.app.driver_namespace` (nothing persists between calls). Model headless with a full script, and use the MCP to import the GLBs into a separate scene for Holden to inspect. glTF import is allowed; use forward-slash paths with no `os`.
- **Single-sided pieces must be truly double-sided** (`face2`: a duplicate of the face with its own reversed verts). `recalc_face_normals` must skip them, or it flips one copy.
- **Check orientation in a diorama render.** A rotation mistake put the cliff backs (the dark slab) towards the valley; it was only visible with the pieces together.
- **A window in a module needs the same hole in the hidden back slab.**

## v1 (superseded)
Nine models (3 islands, 2 crystal clusters, a mushroom, a cloud, 2 rampart walls), preflight PASS, never uploaded. Holden asked for mountain-wall terrain instead of ramparts, and for a per-segment kit.


## Related
[[Rubber-Tower-Valley-Kit]] · [[Rubber-Tower-Kit-Batch-Results]] · [[Rubber-Tower-Art-Style-Guide]] · [[Rubber-Tower-Kit-v4-Style-Prompt]] · [[Rubber-Tower-Kit-v5-Prompt]]
