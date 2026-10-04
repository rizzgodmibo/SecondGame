---
tags: [assets/3d, visuals/vfx]
status: draft
updated: 2026-10-03
confidence: medium
---

# Dragon's Hoard Set

A standalone prop set for learning and reference (not tied to a game): 11 separate low-poly models plus a client-side VFX module.
Files are in `Assets/DragonsHoard/`. The import steps are in `Assets/DragonsHoard/IMPORT.md`, and the deliverable is `DragonsHoard.zip` (≈5.7 MB).

## TL;DR
- **Build:** `build_hoard.py` (Blender 5.2, headless, `--factory-startup`) rebuilds everything. That covers 11 OBJ+MTL files, the 512px atlas `HoardAtlas.png` (8×8 flat colour cells, no vertex colours), 7 particle PNGs, previews and `build_report.json` (tris, sizes, pivots, sockets).
- **Scripts:**
  - `HoardVFX.luau` goes in ReplicatedStorage and runs on the client only.
  - `HoardSetup.luau` is pasted into the command bar once. It sets pivots, collision fidelity, attachments and the shared TextureID.
  - `DevHoardDemo.client.luau` is for Studio testing only.
- **Pivots:** PivotOffsets are set by HoardSetup from `build_report.json`. That makes them independent of where the 3D Importer puts the MeshPart centre.
- **Binaries:** `.blend`, `*.png` and the zip are gitignored. The source script, OBJ/MTL text, Luau and docs are tracked.
- **Status:** v1 is built and previewed in Blender only, then parked by Holden on 2026-10-03 with critiques to come. **Not imported into Studio yet; nothing has been tested in play.**
- **To change a model:** edit its `make_*` function in `build_hoard.py` and rerun it. Then rebuild the zip, and paste any changed pivot numbers from `build_report.json` into HoardSetup.

## Gallery (final v1 renders, 2026-10-03)
These are Blender Workbench previews with studio lighting. They come out darker and less saturated than the models will look in Roblox.
They are kept in `Assets/DragonsHoard/previews/` and tracked in git. The first-pass renders were overwritten by the rebuild, so the "before" state survives only as the text in *Pitfalls hit while building*.

**The whole set** (chest open on its hinge, sword standing in the large pile):

![[Assets/DragonsHoard/previews/_Showcase.png|640]]

**Dragon eggs** (Ember · Frost · Venom):

![[Assets/DragonsHoard/previews/Egg_Ember.png|260]] ![[Assets/DragonsHoard/previews/Egg_Frost.png|260]] ![[Assets/DragonsHoard/previews/Egg_Venom.png|260]]

**Gold** (coin · small pile · large pile with gems):

![[Assets/DragonsHoard/previews/Coin_Gold.png|260]] ![[Assets/DragonsHoard/previews/CoinPile_Small.png|260]] ![[Assets/DragonsHoard/previews/CoinPile_Large.png|260]]

**Treasure** (goblet · crown · sword):

![[Assets/DragonsHoard/previews/Goblet_Jewelled.png|260]] ![[Assets/DragonsHoard/previews/Crown_Gold.png|260]] ![[Assets/DragonsHoard/previews/Sword_Ornate.png|260]]

**Chest** (base · lid):

![[Assets/DragonsHoard/previews/Chest_Base.png|300]] ![[Assets/DragonsHoard/previews/Chest_Lid.png|300]]

**Shared colour atlas** (8×8 cells; grey cells are unused on purpose):

![[Assets/DragonsHoard/textures/HoardAtlas.png|256]]

## Critique status
- **Holden (2026-10-03):** "I definitely have some critiques, like the ones you mentioned, but let's leave it here for now." The set is **parked at v1**. Holden's own list hasn't been given yet, so ask for it before starting v2.
- Claude's self-critique of v1. This is the v2 backlog, not approved changes:
  - Coins are 8-sided and read as octagons up close. Try 12 sides on the single coin and 9–10 in the piles, and budget for it.
  - The chest lid's underside is plain dark wood. It could get inner planks and gold strap ends.
  - The small pile is flat and sparse. It needs more height and a few upright coins.
  - The crown points are thin spikes. Broader leaf or fleur shapes would read better at phone size.
  - The single coin's emblem is a plain diamond. A dragon-head or claw stamp would suit the theme better.
  - Nothing has been checked in Studio lighting yet, and colour has to be judged there.

## User-approved decisions (2026-10-03)
| Topic | Decision |
|---|---|
| Scale | Held-size (avatar ≈ 5 studs). Final sizes are in IMPORT.md: egg 1.6 tall, coin 0.5, goblet 1.0, crown 1.2 wide, sword 4.44, chest 3.06×1.35×2.13 |
| Source | Everything modelled in Blender by script (no Poly Pizza, no Roblox AI meshes, no part-built props) |
| Eggs | Overlapping raised scale plates, two-tone per egg. Ember has gold speckles; Venom blends green at the base to purple at the top |
| Chest | Two-tone wood planks, gold corner caps, straps, rims, lock and hasp, barrel lid; the base holds gold coins and gems |
| Sword | Silver blade with light edge bevels and a dark fuller, gold wing crossguard, red wrapped grip, ruby pommel and guard gems |
| Sword in pile | `SwordSocket` attachment + `HoardVFX.placeSword` (sinks 0.9, leans 8°) |
| VFX side | Client |
| Output | Inside the vault, binaries gitignored |

## Build facts (local observations, 2026-10-03)
- Triangles: each egg 1,476 · coin 92 · small pile 530 · large pile 1,900 · goblet 390 · crown 842 · chest base 746 · lid 206 · sword 342. All are under the 2,000 cap.
- OBJ export: `bpy.ops.wm.obj_export`, forward −Z, up Y, triangulated, flat normals, `path_mode="COPY"`. Every model folder gets its own copy of the atlas, and HoardSetup repoints them all to one TextureID.
- Front faces Blender +Y (Roblox −Z). The lid opens with `CFrame.Angles(+rad(105), 0, 0)` about the `LidHinge` attachment.
- The sword's pivot is its tip, so it is a "base centre" only when standing. If it's held, offset the grip in your Tool code.

## How the meshes are made (reusable technique)
- **Lathe for anything round.** If the profile traces the outline with the outside on the right, the faces wind outward automatically (`normal = (dz, −dr)`).
- **Convex hull for gems, boxes and blade parts.** Use `bmesh.ops.convex_hull`, then flip any face whose normal points toward the hull centre.
- **Atlas UVs per face.** Each face stores a colour index in an int layer. Its UVs are a planar projection squeezed into the middle 60% of that colour's cell, so the UVs aren't degenerate and mipmaps don't bleed between cells.
- **Previews.** Workbench renders `color_type=TEXTURE` with Standard view. Fit the camera with `dist = radius / sin(17°)`.

## Pitfalls hit while building
- **Coplanar overlapping faces z-fight.** It happened with the chest rims on the wall tops and the lid trims on the barrel underside. Offset by at least 0.015–0.03 studs.
- **First-pass egg plates looked flat.** Single kite plates in strict row colours read as "triangles" and "Christmas stripes". Rounded 7-point shingles with per-scale colour mixing fixed that.
- **Bare mound bands.** A coin pile needs coins biased toward the rim (`r ∝ rand^0.4`), or the bare mound shows as a turtle shell.
- **Pale gold reads grey** under studio lighting. Keep gold saturated: gold `242,180,36`, light `255,214,76`.
- **Bad preview framing.** Fitting the camera with `size × 1.25` cropped tall items like the sword. Fit the bounding sphere instead.
- **Platform limits from memory.** The first draft of HoardVFX said Roblox caps Highlights at 31 per client. The vault already had the verified figure (255, in [[VFX-Particles-Beams-Trails]]). Search the vault before stating a platform limit.
- **Command-bar-only property.** CollisionFidelity can't be set from game scripts, which is why HoardSetup is pasted into the command bar rather than shipped as a Script.
- **Rokit tools need a manifest.** Selene and StyLua only run from a folder with a `rokit.toml`. For files outside a project, run them from `C:\Users\holde\Downloads\Fish A Monster` and pass absolute paths.

## Open questions / to verify in Studio
- ⚠️ verify: the 3D Importer's OBJ unit handling. HoardSetup warns if `Size.Y` is more than 2% off and scales the offsets.
- ⚠️ verify: whether the importer assigns `TextureID` or creates a `SurfaceAppearance` for an OBJ with `map_Kd`.
- ⚠️ verify: `rbxasset://textures/particles/*.dds` fallback paths still ship with the client.
- ⚠️ verify: that the blade shine (FaceCamera Beam sweeping tip to guard) reads well. Also check the particle sizes on mobile.
- HoardVFX is written `--!strict`, but no analyzer was run on it. Selene showed 0 warnings and StyLua formatting is applied.

## Related
- [[VFX-Particles-Beams-Trails]] · [[Blender-To-Roblox-Pipeline]] · [[Blender to Roblox Asset Pipeline]] · [[Art Direction Feedback]] · [[Studio Only Dev Test Scripts]]
- [[Shaders-Materials-And-Surfaces]]
- [[Free-Icon-Pack-v3.1-Basic]]

## Sources
- Holden's brief and Q&A in the Claude session, 2026-10-03.
- Pipeline and art rules: `C:\Users\holde\Documents\GameDev\AssetLibrary\README.md`.
- Build output: `Assets/DragonsHoard/build_report.json`.
