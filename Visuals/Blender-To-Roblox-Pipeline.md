---
tags: [visuals/3d, visuals/pipeline]
status: draft
updated: 2026-10-04
confidence: high
---
# Blender → Roblox Pipeline

## TL;DR
- **Blender scene setup**: Scene → Units → Unit System **None**, Rotation Degrees. 1 Blender unit = 1 stud. Character ≈ 5–6 studs tall (R15 default ~5.5).
- **Export FBX**: Path Mode **Copy** + **Embed Textures**, Transform → **Apply Scalings = FBX Unit Scale** (all other scales 1.0), Armature → **Add Leaf Bones off**, **Bake Animation off** unless exporting an animation. Or export **glTF**, which needs no scale fixes.
- **Studio Importer**: File → Import; File Geometry → **Scale Unit = Stud**; World Forward = Front, World Up = Top (defaults); disable **Upload to Roblox** while iterating; enable **Anchored** for static props.
- **Hard limits**: ≤ **20,000 triangles per mesh**; ≤ 4 bone influences per vertex; one material/texture set per MeshPart; single UV set in 0–1 space. Rigid & layered accessories ≤ 4k tris.
- **Textures**: uploads up to 4096² are accepted, but use **256² (5-stud objects) / 512² (10-stud) / 1024² (20-stud, characters)**; PBR maps 1024² max per guideline. Normal maps **OpenGL** tangent space.
- Set **CollisionFidelity = Box/Hull** for decor (Default/PreciseConvexDecomposition only where players interact with concave shapes) and **RenderFidelity = Automatic** (Performance for crowds of small props).

## Scale and axis
| Setting | Value | Why |
|---|---|---|
| Blender Unit System | None | Values read as studs |
| FBX Apply Scalings | FBX Unit Scale | Recommended by Roblox; imports at same size, round-trips to Blender |
| Alternative | Export Scale 0.01, or Scene Unit Scale 0.01 | Works, but breaks round-tripping / causes Blender camera/modifier issues |
| glTF | defaults | No scaling configuration required |
| Axis | Blender Z-up → Studio Y-up; FBX exporter converts (Forward −Z, Up Y default) | If rotated on import, fix with Importer World Forward/World Up, not by rotating in Studio |
| Transforms | **Apply All Transforms** (Ctrl+A) before export; bones scale 1, rotation 0 | Unapplied scale = wrong collision and skinning |
| Origin | Set origin where you want the pivot; Importer "Set Pivot to Scene Origin" default on, per-object "Use Imported Pivot" | Predictable placement & rotation |

## Topology & triangle budgets
- Hard cap 20k tris per mesh (split larger assets into several MeshParts). Practical budgets for mobile-first games:

| Asset | Target tris |
|---|---|
| Small prop (coin, crate, tool) | 50–500 |
| Medium prop (tree, furniture, pet) | 500–3,000 |
| Hero prop / vehicle | 3,000–10,000 |
| Building module | 500–5,000 |
| Custom NPC / creature | 2,000–8,000 |
| Avatar body (per Roblox spec) | Head 4,000; Torso 1,750; each limb group 1,248 |
| Rigid / layered accessory | ≤ 4,000 (hard) |

- Whole-scene guideline: keep visible triangles on low-end mobile in the low hundreds of thousands and **draw calls low** — draw calls (unique mesh+material combinations) matter more than tris. ⚠️ verify: a specific scene budget with MicroProfiler on your lowest target device.
- Requirements: watertight (no holes/backfaces), no zero-thickness geometry, quads where possible (no n-gons), normals facing out (Importer "Invert Negative Faces" can fix flipped ones), **no double-sided** unless needed (Importer "Make Double Sided" is more expensive).
- Reuse: one mesh asset instanced 500× is cheap (same MeshId shares memory and batches); 500 unique meshes are not.

## UVs and textures
- Single UV set, all UVs within 0–1, overlaps allowed (mirror/stack to save texel space).
- Texel density guideline from Roblox: parts show 1024² per 8×8 studs; terrain 512² per 8×8 studs. Match that so imported props sit with built-in materials.
- Upload formats: `.png`, `.jpg`, `.tga`, `.bmp` (images also `.gif` via Importer). Roblox streams lower mips first and may downsample under memory pressure.
- **Atlas** small props into shared 1024² sheets (one texture for 20 props → far fewer texture loads). Stylised trick: a **palette/gradient atlas** (e.g. 64×64 or 256×256 swatch texture) with UVs collapsed onto colour cells — near-zero texture memory, very consistent art style.
- Vertex colours are imported (FBX/glTF) — another zero-texture colouring option; Importer "Ignore Vertex Colors" toggles it.

## PBR maps (SurfaceAppearance)
| Map | Format | Notes |
|---|---|---|
| Color/Albedo | RGB 24-bit (+ alpha if using AlphaMode) | No baked lighting for realistic; baked AO is fine for stylised |
| Normal | RGB 24-bit, **OpenGL (Y+)** tangent space | Blender bakes OpenGL by default; Substance: choose OpenGL |
| Roughness | 8-bit greyscale | |
| Metalness | 8-bit greyscale | Mostly 0 or 1 |
| Emissive mask | 8-bit greyscale | With `EmissiveStrength`/`EmissiveTint` |

Budget: 64–128² (1×1×1 stud items), 256² (2×2×2), 512² (4×4×4), **1024² max** (8×8×8 / characters); non-albedo maps for rigid accessories ≤ 256². Name textures with affixes and connect them in Blender's Principled BSDF so the Importer auto-creates the SurfaceAppearance. See [[Shaders-Materials-And-Surfaces]].

## Export formats
| Format | Use | Notes |
|---|---|---|
| **FBX** | Default for everything, required for rigs/skinning/animation import | Settings above; one animation take per export |
| **glTF (.gltf/.glb)** | Static & rigged meshes, PBR, vertex colours, cages | No scale fiddling; Studio also has a **glTF export (beta)** for round-tripping — no animation data in export |
| **OBJ** | Simple static meshes only | No rig, no hierarchy niceties |

## Studio Importer settings (File → Import)
- **File General**: Name; **Import Only As Model** (default on; off = each child becomes its own asset); **Upload to Roblox** (default on — turn off while iterating to avoid inventory spam); Import as Package; Creator (pick the **group** for group games!); Add to Workspace; Insert Using Scene Position; Keep Zero Influence Bones (off); Set Pivot to Scene Origin (on); **Anchored**; Uses Cage.
- **Rig General**: Rig Type (`R15` / `Custom` / `No Rig`), Validate UGC Body, Rig Scale (Default/Rthro/Rthro Narrow).
- **File Transform**: World Forward (Front), World Up (Top).
- **File Geometry**: **Scale Unit** (Studs), **Merge Meshes** (one MeshPart — good for static decor, bad if parts need separate collision/colour), Invert Negative Faces.
- **Object**: Anchored, Use Imported Pivot, Make Double Sided, Ignore Vertex Colors.
- Naming conventions auto-convert: `*_Att` → Attachment, `*_OuterCage` → WrapTarget, `*_InnerCage` + `*_OuterCage` → WrapLayer, FACS heads → FaceControls.
- Save **presets** (e.g. "Static prop", "Rigged NPC").
- Bulk imports of images/audio/simple meshes: Asset Manager (doesn't support rigged/skinned/animated meshes). See [[Asset-Creation-Workflow-And-Marketplace]].

## Collision and render fidelity
| CollisionFidelity | Use |
|---|---|
| `Box` | Small/decor/non-interactive props; cheapest |
| `Hull` | Convex-ish props (rocks, barrels, vehicles) |
| `Default` | Concave shapes players walk on/into, semi-detailed |
| `PreciseConvexDecomposition` | Only when exact concave collision is essential (e.g. a tunnel you walk through); most expensive |
| `Tunable` | Exposes `CollisionPrecision` slider for a cost/precision trade-off |

Also: `CanCollide = false` + `CanQuery = false` + `CanTouch = false` for pure decor (biggest physics win). Use invisible simple Parts as collision proxies for complex meshes.

`RenderFidelity`: `Automatic` (default; full detail < 250 studs, medium 250–500, lowest > 500), `Precise` (always full — hero assets only), `Performance` (always reduced). Model-level LOD with StreamingEnabled: `Model.LevelOfDetail` = `StreamingMesh` (coarse untextured imposter) or **`SLIM`** (cloud-generated composite LODs, much better quality; requires StreamingEnabled, a place saved to Roblox, and Team Create).

## Skinned meshes
- Armature with root bone at 0,0,0; bones at rest scale 1 / rotation 0; **max 4 influences per vertex**; no weights on root bone; disable Add Leaf Bones.
- Import with Rig Type `Custom` (or `R15` for humanoids following R15 bone names). Bones appear as `Bone` instances; animate with Animation Editor or import FBX animation (one take per file).
- See [[Animation-Rigging-And-IK]].

## Layered clothing caging
- Accessory mesh + `_InnerCage` + `_OuterCage` meshes (names = accessory name + suffix). Start from Roblox's template cages in the layered accessory project files; **never delete cage vertices or edit cage UVs** (they map coordinates between cages). Only the outer cage is reshaped to wrap the accessory; inner cage matches the body template.
- ≤ 4k tris, ≤ 4 influences, skinned to the R15 armature (or use automatic skinning transfer). Validate with the Accessory Fitting Tool / validation tool before UGC upload.

## Checklist
- [ ] Units None, transforms applied, origin set
- [ ] Tris within budget; no n-gons/holes; normals outward
- [ ] One UV set 0–1; texture ≤ 1024² (prefer 256–512²); OpenGL normals
- [ ] FBX: Copy+Embed, FBX Unit Scale, no leaf bones, bake anim off
- [ ] Importer: Scale Unit Stud, Creator = correct group, Anchored for statics, Upload off while iterating
- [ ] CollisionFidelity Box/Hull for decor; CanCollide/CanQuery/CanTouch off for pure decor
- [ ] Repeated props share one MeshId

## Pitfalls
- Default Blender FBX export → model imports ~100× too large.
- Uploading under your personal account for a group game → assets restricted; must grant permission or re-upload to the group.
- Merge Meshes on a building → one giant collision hull, can't recolour parts.
- PreciseConvexDecomposition on hundreds of props → physics stalls on join.
- DirectX normal maps (Y−) from Substance defaults → lighting looks inverted.
- Many unique 1024² textures on small props → mobile memory crashes, long loads.

## Related
- [[Visuals/_Index]] · [[Shaders-Materials-And-Surfaces]] · [[Animation-Rigging-And-IK]] · [[Asset-Creation-Workflow-And-Marketplace]] · [[Art-Direction]]

## Sources
- General mesh specifications (20k tris, 4 influences, watertight, rig rules) — https://create.roblox.com/docs/art/modeling/specifications
- Texture specifications (4096 max upload, size guidance, PBR budget table, UV rules, 1024 UV-space max) — https://create.roblox.com/docs/art/modeling/texture-specifications
- Export settings (Blender FBX) — https://create.roblox.com/docs/art/modeling/export-requirements
- Blender guide (units, axis, FBX scaling options, glTF needs no scaling) — https://create.roblox.com/docs/art/blender
- Importer settings — https://create.roblox.com/docs/studio/importer
- Meshes (RenderFidelity distances, CollisionFidelity options, naming conventions) — https://create.roblox.com/docs/parts/meshes
- SLIM — https://create.roblox.com/docs/workspace/streaming/slim
- glTF export (beta) — https://create.roblox.com/docs/art/modeling/gltf-export
- Avatar specs (body tri budgets) — https://create.roblox.com/docs/avatar/character-bodies/specifications ; layered accessories — https://create.roblox.com/docs/avatar/layered-accessories/specifications
- All checked via Roblox/creator-docs GitHub source (2026-10-02 commit) on 2026-10-04. Note: the brief for this note assumed a 1024 max texture; current docs say uploads support up to 4096², while UV/PBR guidance still caps at 1024².
