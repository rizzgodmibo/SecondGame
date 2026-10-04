# Cinder Drake: import into Roblox Studio (v3.1, 2026-10-04)

The model is static: no rig, as in the brief. Since v3.1 the **jaw is its own hinged MeshPart**, so a script can open the mouth without a rig.

It is built by `build_creatures.py -- export3`. Sizes and triangle counts are in `build_report.json`.

## Files in this folder

| File | What it is | Where it goes |
|---|---|---|
| `CinderDrake.obj` + `CinderDrake.mtl` | One OBJ with four objects: Body (14,759 tris), Jaw (1,640), Wings (3,648), Glow (160) | Studio 3D Importer → a Model in **Workspace**. Move it to ReplicatedStorage later if a script will spawn it |
| `CinderDrake_Body_Color.png` | 1024² albedo. AO is baked in, and the ember seams are painted orange | Body **and Jaw** SurfaceAppearance → `ColorMap` |
| `CinderDrake_Body_Normal.png` | 1024² normal map, OpenGL tangent space | Body and Jaw SurfaceAppearance → `NormalMap` |
| `CinderDrake_Body_Roughness.png` | 1024² greyscale | Body and Jaw SurfaceAppearance → `RoughnessMap` |
| `CinderDrake_Body_Emissive.png` | 1024² greyscale mask (throat/chest scute seams, mouth seam, hot throat inside the mouth) | Body and Jaw SurfaceAppearance → `EmissiveMaskContent` |
| `CinderDrake_Wings_Color.png` / `_Normal.png` / `_Roughness.png` | 1024² maps for the membranes and finger bones | Wings SurfaceAppearance → `ColorMap` / `NormalMap` / `RoughnessMap` |
| `CinderDrake_FlameFlip4x4.png` | 512² flame flipbook for the fire breath (our own, procedural) | A VFX texture: see VFX.md |
| `build_report.json` | Size, triangle counts, part centres, SurfaceAppearance values, jaw hinge, attachment points (Roblox axes) | Reference only |
| `preview_game_*.png` | Blender renders of this exact game mesh with these maps. `preview_game_jaw_open.png` shows the Jaw part turned -28° | Reference only (Roblox's lighting will differ) |
| `VFX.md` + `vfx_spec.json` | Attachments, particle emitters and lights for the sheet's VFX (nostril smoke, ember drift, throat light, fire breath) and how the jaw opens | Step 10 |
| `_v2/` | The previous v2 export | Not used |

## Steps
1. **Import the mesh.** File → Import 3D → `CinderDrake.obj`.
   - **File Geometry:** Scale Unit = **Stud**, **Merge Meshes = off** (Body, Jaw, Wings and Glow must stay separate MeshParts), Invert Negative Faces = off.
   - **Orientation:** World Forward = Front, World Up = Top (the defaults).
   - **Object:** Anchored = **on**, Use Imported Pivot = on.
   - Keep Upload to Roblox off while you test; turn it on for the real import.
2. **Check the result.** You should get Model `CinderDrake` with MeshParts `CinderDrake_Body`, `CinderDrake_Jaw`, `CinderDrake_Wings` and `CinderDrake_Glow`, about 8 × 7.6 × 14.5 studs (W × H × L).
3. **Upload the 7 map PNGs.** Use View → Asset Manager → Bulk Import, or the Creator Dashboard, and copy each image ID. The VFX textures are listed in VFX.md.
4. **Body SurfaceAppearance.** Select `CinderDrake_Body` → Insert Object → **SurfaceAppearance** and set:
   - `ColorMap` = Body_Color, `NormalMap` = Body_Normal, `RoughnessMap` = Body_Roughness, `EmissiveMaskContent` = Body_Emissive;
   - `EmissiveStrength` = **6** (tune 3–8 in your scene lighting), `EmissiveTint` = white, `AlphaMode` = Overlay;
   - leave `MetalnessMap` empty (nothing on the drake is metal).
5. **Jaw SurfaceAppearance.** Copy the Body's SurfaceAppearance and paste it into `CinderDrake_Jaw`. It uses the same four images, because the jaw is in the Body's texture layout, so it costs no extra texture memory.
6. **Wings SurfaceAppearance.** Select `CinderDrake_Wings` → Insert Object → **SurfaceAppearance**: `ColorMap` / `NormalMap` / `RoughnessMap` = the Wings maps, `AlphaMode` = Overlay.
7. **Glow part.** On `CinderDrake_Glow` (the eyes): Material = **Neon**, Color = 255, 122, 30, CastShadow = off.
8. **Collision and rendering.**
   - Body: CollisionFidelity = **Hull** (or Box).
   - Jaw, Wings and Glow: CanCollide = off, CanQuery = off, CollisionFidelity = Box.
   - RenderFidelity = Automatic on all parts.
   - DoubleSided is not needed, because the membranes have thickness.
9. **Jaw hinge.** Select `CinderDrake_Jaw` and set its **PivotOffset** position to **(0, 0.333, 0.755)**. That puts the pivot on the hinge, which is at (0, 2.669, -3.52) from the model pivot.
   - Turning the part -28° about its X axis then opens the mouth for the breath; -40° gives a roar. Negative opens.
   - It stays closed until a script turns it (scripts: not yet).
10. **Bloom.** A `BloomEffect` in Lighting (Intensity ≈ 0.6, Size ≈ 24, Threshold ≈ 1.2) makes the eyes and throat embers read.
11. **VFX.** Follow [VFX.md](VFX.md): 4 attachments on the Body, 7 emitters and 2 lights. The fire breath stays off until something triggers it.

## Notes
- **Why the SurfaceAppearance is manual:** the importer builds it automatically only for FBX "Import as model" uploads. Nothing is documented for OBJ + MTL, so steps 3–6 do it by hand. The MTL only names the colour map.
- **Emissive colour:** Roblox takes the emissive colour from the **ColorMap**, roughly `(mask × strength × tint + light) × ColorMap`. That is why the glowing seams are painted ember orange in `Body_Color`.
  - ⚠️ verify: check the glow in Studio and on a phone at low graphics quality.
- ⚠️ verify: the normal maps were baked in Blender's MikkTSpace on the triangulated mesh. If the scales or plates look lit from the wrong side in Studio, report it.
- ⚠️ verify: the jaw's turn direction (worked out from Blender axes, not yet tried in Studio).
- **Memory:** seven 1024² maps for one creature is fine for a hero or boss. Don't spawn dozens of copies.
- **Inside the mouth:** the palate vault, the tongue and the lower tooth row are modelled. The Body texture set is baked with the jaw 40° open, so the inside of the mouth is textured properly at any opening. At the open angles you can see the hot throat glow.
