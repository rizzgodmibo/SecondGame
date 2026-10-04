---
title: Blender to Roblox Asset Pipeline
date: 2026-10-03
tags: [blender, roblox, pipeline, 3d]
---
# Blender to Roblox Asset Pipeline

Worked out in [[Fish a Monster]] and used throughout [[Paper Plane Toss]]. The full version lives in `Documents\GameDev\AssetLibrary\README.md`.

## Steps
1. Get or build the model in Blender, through the MCP connection or headless (`blender --background --factory-startup --python script.py`).
2. Export a GLB of **only the active scene**. Otherwise the default Cube from another scene sneaks in.
3. Upload with Open Cloud: `AssetLibrary/tools/upload_model.sh <glb> "<name>" "<desc>"`. It reads the key from a gitignored file. See [[Keeping API Keys Out of Git]].
4. Insert it in Studio with MCP `insert_asset`, remove the PackageLink, then anchor and place it.

## Gotchas
- **Imported GLBs arrive rotated 180°.** Apply `CFrame.Angles(0, π, 0)`, or set `PivotOffset` for nose-forward models.
- **Don't export vertex colours.** They multiply into the texture and turn the ground almost black. Use palette or atlas textures.
- Transparent leaf edges render black unless the leaf material has a transparency setting.
- glTF imports use quaternion rotation, so set `rotation_mode = "XYZ"` before changing Euler yaw.
- Faces can import pointing the wrong way: the lake faced down and the waterfall was half backwards. Flip them or make them double-sided.
- **Cartoon outlines:** bake an inverted hull into the mesh. It works because Roblox only draws front faces.
- Keep big meshes under the triangle cap by splitting them into chunks by area.
- Don't use Roblox's AI mesh generator. See [[Art Direction Feedback]].

## Fully scripted props as OBJ (Dragon's Hoard, 2026-10-03)
An alternative to the GLB + Open Cloud route, used for [[Dragons-Hoard-Set]]. One Python script builds every model from scratch, with no MCP and no Blender window. The template is `Assets/DragonsHoard/build_hoard.py`. These are local observations; the Studio import side is untested.
- **Build with bmesh helpers:**
  - `lathe()` for anything round (coins, goblet, egg body, grip, crown band). Trace the profile with the outside on the right and the faces wind outward without any normal fixing.
  - `hull()` (`bmesh.ops.convex_hull`) for gems, boxes, blade parts and chest planks.
  - Hand-built faces with an "interior hint" point for the odd shapes, such as egg scales.
- **Colour comes from an atlas, not materials.** Store a palette index per face in an int layer. Write the 8×8-cell atlas with numpy, then project each face into the middle 60% of its cell. One material, no vertex colours.
- **Export:** `bpy.ops.wm.obj_export(export_selected_objects=True, export_triangulated_mesh=True, path_mode="COPY", forward_axis="NEGATIVE_Z", up_axis="Y")`. Roblox then sees (x, z, −y), and Blender +Y becomes the model's front (−Z).
- **Pivots:** write `build_report.json` (tris, sizes, pivot and socket offsets from the bounding-box centre, in Roblox axes). A command-bar setup script then applies `PivotOffset` and the attachments, so the result doesn't depend on how the importer centres the mesh.
- **Preview before showing:** render each model with Workbench (`color_type="TEXTURE"`, Standard view) and critique it honestly. Two problems only showed up in renders: z-fighting and flat-looking egg scales.

Related: [[Blender MCP Setup]], [[Roblox Studio MCP Quirks]], [[Roblox Asset Pipeline Skill]] (preflight checks + previews before upload)
