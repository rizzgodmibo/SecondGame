# Cinder Drake: import into Roblox Studio (v3, 2026-10-04)

The model is static (no rig, as in the brief). It is built by `build_creatures.py -- export3`. Sizes and triangle counts are in `build_report.json`.

## Files in this folder

| File | What it is | Where it goes |
|---|---|---|
| `CinderDrake.obj` + `CinderDrake.mtl` | One OBJ with three objects: Body (16,490 tris), Wings (3,648), Glow (160) | Studio 3D Importer → a Model in **Workspace**. Move it to ReplicatedStorage later if a script will spawn it |
| `CinderDrake_Body_Color.png` | 1024² albedo. AO is baked in, and the ember seams are painted orange | Body SurfaceAppearance → `ColorMap` |
| `CinderDrake_Body_Normal.png` | 1024² normal map, OpenGL tangent space | Body SurfaceAppearance → `NormalMap` |
| `CinderDrake_Body_Roughness.png` | 1024² greyscale | Body SurfaceAppearance → `RoughnessMap` |
| `CinderDrake_Body_Emissive.png` | 1024² greyscale mask (throat/chest scute seams, mouth seam) | Body SurfaceAppearance → `EmissiveMaskContent` |
| `CinderDrake_Wings_Color.png` / `_Normal.png` / `_Roughness.png` | 1024² maps for the membranes and finger bones | Wings SurfaceAppearance → `ColorMap` / `NormalMap` / `RoughnessMap` |
| `build_report.json` | Size, triangle counts, SurfaceAppearance values, attachment points (Roblox axes) | Reference only |
| `preview_game_*.png` | Blender renders of this exact game mesh with these maps | Reference only (Roblox's lighting will differ) |
| `VFX.md` + `vfx_spec.json` | Attachments, particle emitters and lights for the sheet's VFX (nostril smoke, ember drift, throat light, fire breath) | Step 9 |
| `_v2/` | The previous v2 export | Not used |

## Steps
1. **Import the mesh.** File → Import 3D → `CinderDrake.obj`.
   - **File Geometry:** Scale Unit = **Stud**, **Merge Meshes = off** (Body, Wings and Glow must stay separate MeshParts), Invert Negative Faces = off.
   - **Orientation:** World Forward = Front, World Up = Top (the defaults).
   - **Object:** Anchored = **on**, Use Imported Pivot = on.
   - Keep Upload to Roblox off while you test; turn it on for the real import.
2. **Check the result.** You should get Model `CinderDrake` with MeshParts `CinderDrake_Body`, `CinderDrake_Wings` and `CinderDrake_Glow`, about 8 × 7.6 × 14.5 studs (W × H × L).
3. **Upload the 7 PNGs.** Use View → Asset Manager → Bulk Import, or the Creator Dashboard, and copy each image ID.
4. **Body SurfaceAppearance.** Select `CinderDrake_Body` → Insert Object → **SurfaceAppearance** and set:
   - `ColorMap` = Body_Color, `NormalMap` = Body_Normal, `RoughnessMap` = Body_Roughness, `EmissiveMaskContent` = Body_Emissive;
   - `EmissiveStrength` = **6** (tune 3–8 in your scene lighting), `EmissiveTint` = white, `AlphaMode` = Overlay;
   - leave `MetalnessMap` empty (nothing on the drake is metal).
5. **Wings SurfaceAppearance.** Select `CinderDrake_Wings` → Insert Object → **SurfaceAppearance**: `ColorMap` / `NormalMap` / `RoughnessMap` = the Wings maps, `AlphaMode` = Overlay.
6. **Glow part.** On `CinderDrake_Glow` (the eyes): Material = **Neon**, Color = 255, 122, 30, CastShadow = off.
7. **Collision and rendering.**
   - Body: CollisionFidelity = **Hull** (or Box).
   - Wings and Glow: CanCollide = off, CanQuery = off, CollisionFidelity = Box.
   - RenderFidelity = Automatic on all parts.
   - DoubleSided is not needed, because the membranes have thickness.
8. **Bloom.** A `BloomEffect` in Lighting (Intensity ≈ 0.6, Size ≈ 24, Threshold ≈ 1.2) makes the eyes and throat embers read.
9. **VFX.** Follow [VFX.md](VFX.md): 4 attachments on the Body, 7 emitters and 2 lights. The fire breath stays off until something triggers it.

## Notes
- **Why the SurfaceAppearance is manual:** the importer builds it automatically only for FBX "Import as model" uploads. Nothing is documented for OBJ + MTL, so steps 3–5 do it by hand. The MTL only names the colour map.
- **Emissive colour:** Roblox takes the emissive colour from the **ColorMap**, roughly `(mask × strength × tint + light) × ColorMap`. That is why the glowing seams are painted ember orange in `Body_Color`.
  - ⚠️ verify: check the glow in Studio and on a phone at low graphics quality.
- ⚠️ verify: the normal maps were baked in Blender's MikkTSpace on the triangulated mesh. If the scales or plates look lit from the wrong side in Studio, report it.
- **Memory:** seven 1024² maps for one creature is fine for a hero or boss. Don't spawn dozens of copies.
- **Inside the closed mouth:** the palate vault, the tongue and the lower tooth row are modelled (added in the 2026-10-04 re-export for the open-jaw sheet poses). With the jaw shut, the edges of the roof and floor of the mouth sit close together and bake each other's surface. This is invisible while the mouth is closed. An open-mouth pose would need a rig plus a re-bake with the jaw opened.
