---
tags: [archive, assets/kit, project/rubber-tower]
status: stale
updated: 2026-10-06
confidence: high
---
# Rubber Tower Valley Kit: E:\Vault copy before the restructure (archived)

> **Archived 2026-10-06 during the C:\Vault → E:\Vault sync.** This is the version of [[Rubber-Tower-Valley-Kit]] that existed only in E:\Vault, from before the note was restructured (batches marked BUILT; older sections moved to [[Rubber-Tower-Kit-Batch-Results]] and [[Rubber-Tower-Kit-Style-History]]).
> 143 of its 178 unique lines exist elsewhere in the vault. The other 35 are mostly superseded status lines, but a few are unique details (the v4 archive location, the Blender inspection scene, triangle counts), so the whole copy is kept here. **Statuses below are out of date**; the live note is the source of truth.

---

# Rubber Tower Valley Kit

## TL;DR
- **v5 is the LOCKED style** (Holden 2026-10-04: "Lock it in"), defined in [[Rubber-Tower-Art-Style-Guide]]. The v5 models are saved and uploaded: `AssetLibrary/models/rubber-tower-kit-v5/`.
- **Batch (a), the obby mechanic models, is built and waiting for Holden's review** (2026-10-04): 46 types, 54 meshes, 12 colour variants, preflight PASS (see "Batch (a) results").
  - Code: `RubberTower/art/batch_a.py` on `kitlib6.py`.
  - Output: `art/kit_batch_a/` (GLBs, shared-atlas textures + colour variants, `manifest.json` with tags, colliders and pivots, tiles and sheets).
  - **Not uploaded and not placed** (Holden: don't upload or build the map yet).
- **v5 style test (2026-10-04, done, approved):**
  - Holden rejected the v4 look ("cheap plastic", and the terrain has to go UP). His prompt is in [[Rubber-Tower-Kit-v5-Prompt]].
  - v5 adds hand-painted baked textures and a climbable 60-stud wall.
  - **Built, and preflight PASS, but not yet in Studio:** the Open Cloud upload was blocked (see the v5 section).
- **v4 style test (2026-10-04): rejected as a style, models archived** in `AssetLibrary/models/rubber-tower-kit-v4/` (Holden: "save these models in case I want to use them later").
  - What it is: 3 v3 models restyled (cliff, islet, checkpoint beacon) plus 3 new magic models (crystal cluster in 3 colours, floating rune obelisk, magic portal) and a diorama, all in the "Roblox style" from [[Rubber-Tower-Art-Style-Guide]].
  - Preflight: `PREFLIGHT RESULT PASS objects=16 fails=0 warns=9`.
  - **Not uploaded.** Nothing more gets built until Holden approves.
  - Holden's critique of v3 is logged in [[Rubber-Tower]] (Decisions).
- **v3 (kept, per Holden 2026-10-04):** a reusable kit of 28 models for the ground floor, segment 1 (meadow), the backdrop and the landmarks. Built by `RubberTower/art/build_kit_v3.py` (one function per model; `--only` rebuilds single models). It's made from scratch: no AI meshes, no downloads, so no licence or credit is needed.
- **Preflight: `PREFLIGHT RESULT PASS objects=28 fails=0 warns=3`.** The 3 WARNs are intentional double-sided faces (the waterfall sheet and two banners), which the normals check flags by design.
- Triangles per model: 76 to 2,240. No vertex colours. One 256² atlas (`RT_ValleyAtlas.png`).
- **Not uploaded.** Holden asked to see the renders before uploading (2026-10-04).
- v1 (9 models, above-the-island style) is superseded. Holden's verdict on the map that used parts instead: "you can do better".
- Holden can inspect every model in his live Blender, in the scene `RT_ValleyKit` (collections Backdrop / Ground / Segment1 / Sky), imported from the GLBs through the Blender MCP.

## Full kit list (v5 style, ordered by Holden 2026-10-04)
**How to read the list:**
- **Columns:** name — sizes in studs (S/M/L) — tri budget per mesh — references — segment — notes.
- **Variant colours** reuse the same mesh with a re-baked texture.
- **Reference keys:**
  - **V5:** v5 kit (`AssetLibrary/models/rubber-tower-kit-v5/`);
  - **OK1–4:** OmniKoi2 img-1–4;
  - **HAO:** haooffiso Sky_Island;
  - **MR:** Mossy Rocks;
  - **ORCA:** Orca_Environ;
  - **M0TO:** M0TOPRINCESS variants;
  - **PPS:** Parkour Spiral;
  - **TOS:** Tower of Sky;
  - **FIS:** Fisch;
  - **VFX:** `Assets/VFX/TexturePack`;
  - **HP:** Holden-Picks (empty so far).
- **Segments:** S1 meadow, S2 mushroom grove, S3 crystal-ice, S4 cloud kingdom, All = any.
- **Tags:** B = `BouncePad`, I = `IcePlatform`, W = `WobblePlatform` (a single MeshPart, about 12×12, 4+ studs clear underneath).
- **Status:** ticked = built, rendered and preflight-passed; Holden's review is a separate gate.

### Batch (a): obby mechanic models (built first)
**Fixes to v5 pieces**
- [x] Obby_Wall_A v5.1: varied mass sizes and depths, no grid (68×64) — 9k — V5, OK1, PPS — S1
- [x] Checkpoint_Beacon v5.1: chunky stones, fewer bigger bricks (15×15×21) — 2k — V5, HAO — S1
- [x] Meadow_Islet_M v5.1 and Checkpoint_Islet v5.1: puffy canopy bush (r7 / r11) — 1.5k / 2k — V5, OK1 — S1

**Bounce (hot pink and magenta; tag B on an invisible top collider)**
- [x] Bounce_Mushroom S/M/L (cap ⌀8/12/16): fat cap with spots and a goofy face on the stem — 1.2k — OK3, V5 — S1/S2 — variants red, pink, purple, orange
- [x] Bounce_FlowerPad S/M (⌀10/14): giant flat flower — 900 — OK1 — S1
- [x] Bounce_Jelly S/M (8/10): slime dome with a face and bubbles — 800 — ORCA — All — variants pink, green, blue
- [x] Bounce_SpringPad (⌀8): cushion on a metal coil — 1k — V5 — All
- [x] Bounce_Leaf (14×7): giant curved leaf ledge — 600 — OK1 — S1/S2

**Ice (pale cyan and white; tag I)**
- [x] Ice_Slab S/M/L (8×8 / 12×12 / 16×10): frost cracks, snow lumps, icicles — 800 — HAO, V5 — S3
- [x] Ice_PuddleIslet (r7): snowy islet with a frozen puddle top — 1.4k — V5 — S3
- [x] Ice_CrystalLedge (10×7): snowy rock ledge with icicles and shards — 1.2k — V5 — S3
- [x] Ice_Slide (6×20, 8 drop): ramp with snowy rails — 1k — TOS — S3

**Wobble (lime and yellow jelly; tag W; one MeshPart, no glow)**
- [x] Wobble_JellyCube (12×12×4): wobbly outline, bubbles — 600 — ORCA — All — variants lime, orange, purple
- [x] Wobble_LilyPad (⌀12): notch and veins — 400 — OK1 — S1/S2
- [x] Wobble_SeesawLog (14×4) + Seesaw_Base (stump fulcrum) — 800 + 400 — V5 — S1
- [x] Wobble_Raft (12×12): logs with rope bindings and corner rings — 1.2k — FIS — S1
- [x] Wobble_StoneDisc (⌀12) + Spring_Base (metal coil decor) — 800 + 600 — HAO — S3/S4

**Soft rest (cream, white and pastel; no tag; never a spawn)**
- [x] Soft_Cloud S/M (10/14): puffy cloud pad — 900 — HAO, PPT — S4/All
- [x] Soft_Pillow (10×7×2.5): seams, buttons, tassels — 600 — M0TO — All — variants pink, blue, cream
- [x] Soft_Marshmallow (⌀6 stack): 2–3 stacked marshmallows — 500 — OK3 — S4/All
- [x] Soft_HayBale (8×5×4): straw and twine — 400 — FIS — S1
- [x] Soft_MossCushion (⌀8): moss mound on rock with flowers — 900 — MR — S1/S2

**Movement (future mechanics; moving parts are separate MeshParts)**
- [x] Move_RopeBridge (24 long): sagging planks, posts — 1.5k — V5 — All
- [x] Move_Tightrope (20): two posts and a rope — 400 — V5 — All
- [x] Move_SwingPaddle: pivot hub + arm with a red rubber paddle — 800 — PPS — All
- [x] Move_SwingHammer: pivot + rubber mallet — 800 — PPS — All
- [x] Move_Windmill: crooked tower + Blades part — 2.5k — OK1 — S1
- [x] Move_FanVent (⌀8): stone ring, grate, Fan part, glow — 1k — HAO — S3/S4
- [x] Move_Slingshot: Y-frame, rubber band, pouch — 700 — V5 — S1
- [x] Move_VineConveyor (4×20): braided vine belt with leaves and rollers — 1.2k — MR — S2

**Climbing**
- [x] Climb_Ladder (12 tall): crooked rungs, rope bindings — 500 — V5 — All
- [x] Climb_VineWall (10×16): vine net on rock — 1.5k — MR — S1/S2
- [x] Climb_MushroomSteps: 4 stair-step shelf mushrooms on a rock strip — 2k — OK3 — S2
- [x] Climb_ShelfFungus S/M (6/9 wide): wall ledge — 500 — MR — S2 — variants orange, teal
- [x] Climb_Scaffold (10×10×16): 2 decks + ladder — 2.5k — V5 — S1
- [x] Climb_SpiralSteps (pillar ⌀8, 30 tall, 12 steps): stone steps round a pillar — 4k — PPS — All

**Checkpoint**
- [x] Checkpoint_Island S1/S2/S3/S4 (r11, themed tops and undersides) — 2k — V5, HAO — per segment
- [x] Checkpoint_Beacon S1/S2/S3/S4 (stone / mushroom-wood / ice-crystal / gold temple arch) — 2k — V5, HAO — per segment
- [x] Soft_FallNet (14×14): rope net on 4 posts — 1k — V5 — All

### Batch (b): S1 meadow + fantasy props
- [ ] Meadow islets S/M/L (r5/7/10), Log_Platform S/M, Stump_Platform S/M/L, Plank_Platform S/M, Picket_Fence (straight, corner, broken), Haystack, Windmill (big landmark)
- [ ] Props: Lantern (post and hanging), Signpost ×4 silly signs, Treasure_Chest (open/closed), Barrel, Crate S/M, Banner, Flag, Bench, Fountain, Wood_Bridge S/M, Well, Cart
- [ ] Trees: Puffy_Tree S/M/L (3 tints), Blossom_Tree (pink), GlowFruit_Tree, Twisted_Magic_Tree, Crystal_Tree; Bush S/M ×3 tints; Giant_Flower ×4 colours; Vines (hanging, wall); Lily_Pad; Glow_Grass patch
- [ ] Creatures (decor): Slime ×4 colours, Frog_On_LilyPad, Bird ×2, Butterfly ×3 colours

### Batch (c): S2 mushroom grove
- [ ] Mushroom_Cap platforms S/M/L × 4 colours, Shelf_Fungus wall ledges (shared with (a)), Spore_Mushroom (glowing) ×3, Toadstool_House (door and windows, glow), Mushroom_House S/M, Roots (arches, strands), Vine curtains, Glow_Moss, Fairy_Treehouse, S2 cliff wall variant (teal grass, purple rock)

### Batch (d): S3 crystal-ice
- [ ] Crystal_Shard platforms S/M/L, Ice_Slab (from (a)), Frozen_Arch, Snowy_Islet S/M/L, Frozen_Waterfall, Icicle clusters, Crystal clusters in 5+ colours, Snow_Pine trees ×3, Ice cliff wall variant, Igloo/ice hut

### Batch (e): S4 cloud kingdom + backdrop + magic and landmarks
- [ ] Cloud platforms S/M/L, Sky_Temple pieces (floor tile, column, broken column, stairs, arch), Rainbow_Bridge, Floating_Pillar, Sky_Castle_Gate, Floating_Castle, Airship
- [ ] Magic: Rune_Stone ×3, Obelisk (v5 fix: thicker, chunky chains, big runes), Floating_Chained_Rock S/M, Portal (real spiral), Spell_Circle (decal + glow ring), Potion_Bottles ×5, Cauldron, Spell_Books (floating), Wizard_Hat_Post, Orb_Pedestal ×3, Rune_Door
- [ ] Buildings: Wizard_Tower, Crooked_Lighthouse, Ruined_Arch, Ruined_Pillars, Giant_Rubber_Duck statue, Wobbly_Knight statue, Sleeping_Dragon (far peak)
- [ ] Backdrop: cliff and wall variants per segment, Waterfall S/M, Distant_Floating_Islands ×3, Distant_Mountains ×2, Cloud puffs ×3

## Batch (a) results (2026-10-04): waiting for Holden's review
**Output and checks:**
- **Built:** 46 model types, 54 meshes with sizes, **55 textures** (43 base atlases + 12 colour variants), **55,366 tris in total**. The biggest is Obby_Wall_A at 10,292 across 4 parts.
- **Code:** `RubberTower/art/batch_a.py` (models) on `kitlib6.py` (framework).
- **Output:** `art/kit_batch_a/`: `models/*.glb`, `textures/`, `tiles/`, `sheets/`, and `manifest.json`. The manifest holds per-model tags, collider boxes (Blender coords; `rx`/`rz` in degrees), pivots for moving parts, stand points, refs, segment and tris.
- **Preflight:** `PREFLIGHT RESULT PASS objects=74 fails=0 warns=51`.
  - Glow parts: single colour and shared origin.
  - Moving parts (Blades, Arm, Fan): pivot origins.
  - Normals: the twins of double-sided blades, straw and leaves.
  - ⚠️ verify: 2 inward faces on Wobble_LilyPad, to check in Studio.
- **Not uploaded** (USER: not yet).

**Sheets (model | reference) and the diorama:**

![[BatchA_Diorama.png|700]]
![[BatchA_Bounce.png|700]]
![[BatchA_Ice.png|700]]
![[BatchA_Wobble.png|700]]
![[BatchA_Soft.png|700]]
![[BatchA_Movement.png|700]]
![[BatchA_Climbing.png|700]]
![[BatchA_Checkpoint.png|700]]
![[BatchA_Fixes.png|700]]

**Studio setup rules (from the code, for placement later):**
- **Wobble pieces** are single MeshParts tagged `WobblePlatform` directly (Box collision), with 4+ studs clear below.
- **Bounce and ice** carry the tag on the invisible top collider listed in the manifest.
- **Moving parts** rotate about their manifest pivot.
- **Glow parts** become Neon.
- **Every textured part** gets a SurfaceAppearance (ColorMap = its texture).

**Self-critique, first pass (all fixed before showing):**
- **Obby_Wall_A v5.1:** random placement exposed a flat core slab. It's now jittered rows that always cover the face, with masses varying ×2.5 and 30% jutting out 2–4 studs.
- **Stone:** the bricks were still too busy, which was Holden's beacon complaint. Now scale 0.14–0.15 (bricks about 3.5×1.6 studs) with 3 tone steps per stone.
- **Sky stone:** no more moss on S4 sky stone.
- **Ice and snow:** read as plain white. The ice palette is now bluer and the snow has blue shading and sparkles.
- **Smaller fixes:** the moss cushion drape is thinner, the mushroom spots are bigger, the lily pad is darker, and the cloud refs are corrected (the PPT image is a snow thumbnail).

**Honest weak points still open:**
- **Checkpoint_Island_S3:** the top is plain white snow and needs a frozen pond or more crystals. Will fix in batch (d).
- **Climb_MushroomSteps:** the rock backing reads as stacked boulders, not a wall.
- **Mushroom caps:** smoother than the v5 rock standard.
- **Ice slabs:** the S size is small next to the dummy.
- **Wall:** 10.3k tris, over the 9k budget, so the next pass reduces masses.
- **Variety:** many pieces share the same lavender-white stone. Segment palettes should diverge more in batches (c)–(e).

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
- [[Rubber-Tower]] · [[Rubber-Tower-Build-Status]] · [[Roblox Asset Pipeline Skill]] · [[Blender to Roblox Asset Pipeline]] · [[Art Direction Feedback]] · [[Rubber-Tower-Reference-Obbies]]
