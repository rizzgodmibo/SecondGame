---
tags: [project/trap-your-friends, visuals/lighting, visuals/sky]
status: draft
updated: 2026-10-06
confidence: low
---
# Trap Your Friends: Sky v3, a living sky (plan + Step 1a mockup)

## TL;DR
- **Why:** (USER, 2026-10-06) "the sky is terrible": v2 was one still painted cube map with the clouds baked in.
- **v3 is layered.** All layers are client-side or Lighting, nothing gameplay:
  1. a **clean gradient skybox** (no clouds painted in), made from one equirectangular gradient;
  2. **dynamic `Clouds`** under Terrain, drifting with `Workspace.GlobalWind`;
  3. **3 depth layers of outlined toon cloud meshes** that drift on the client;
  4. **distant floating-island and castle silhouettes**;
  5. a **stylised sun** (our texture, bigger `SunAngularSize`, SunRays 0.05–0.1);
  6. **Atmosphere back on**, tuned to tint only the horizon.
- **Look target:** saturated and clear like Steal a Brainrot / Grow a Garden (deep blue, white clouds), not washed out. **Each map gets its own sky mood**, like Super Doomspire.
- **Before any upload:** a Blender mockup render (normal and phone aspect) for Holden. In Studio: 4 fixed shots at high and low graphics quality.
- **Cost:**
  - ~9 private images + ~8 meshes (no Robux; Holden approves each upload batch);
  - runtime ≈ 70 cloud meshes (~45k triangles), few draw calls if Roblox batches the identical meshes (⚠️ verify in render stats), plus the GPU cost of `Clouds` (unknown, measure).


## Status: Step 1a mockup built (2026-10-06), waiting for Holden's upload OK
Nothing uploaded and nothing changed in the place yet. Art: `TrapYourFriends/art/sky_v3/`.

**What was built:**
- **Skybox:** 6 gradient faces (1024²) sampled from one equirectangular master. Worst seam step is 0.31 of an 8-bit level (invisible), with dither against banding. The gradient depends on elevation only, so face orientation can't misplace anything.
- **Sun:** a toon disc, a crisp ring and soft rays, in **two versions** (additive and alpha). Roblox's blending for `SunTextureId` is unknown, so both get tested in Studio and one is kept (⚠️ verify).
- **Palette:** one shared texture (512×256: flat swatches on the left, the cloud toon ramp on the right). It replaces the planned 1024² atlases, so all meshes can share one TextureID.
- **5 cloud meshes** (`TYF_Cloud_A..E`), **640 triangles each including the outline shell:**
  - puff spheres merged (voxel remesh), flat bottom, decimated, **smooth shading**;
  - toon bands come from the ramp texture: crisp curved band lines, no blurry gradient;
  - a black **inverted-hull outline** (2.4% of the width).
  - An earlier flat-shaded version looked crumpled and noisy, so it was dropped.
- **3 silhouettes** (`TYF_Far_CastleIsle` 244 tris, `TYF_Far_Spires` 256, `TYF_Far_Windmill` 156): flat-shaded, saturated pastel blues with pink roofs, no outline.
- **8 GLBs** in `export/` (`use_selection`, `use_active_scene`, no vertex colours).
- **Asset preflight** (`roblox-asset-pipeline`): **PASS, 0 FAIL, 13 WARN.** All WARNs are deliberate:
  - "inward normals" = the outline shell;
  - "origin" = clouds pivot at their base, silhouettes at the grass top.
- **Code** (gate PASS, 52 specs):
  - `Rules/CloudDrift` + spec;
  - `Lighting/SkyMoods` (CastleNoon; ids empty until upload);
  - `Lighting/Apply.applyMood`;
  - `Controllers/SkyLayersController` (client: 3 rings turning, silhouettes bobbing, low tier);
  - `tools/SkyV3/ApplyMood`.
- **Studio playtest:** clean boot (7 controllers); the only message is the expected "SkyAssets missing".

**Verified in Studio (2026-10-06, Edit mode via MCP):**
- `Clouds.Enabled` exists (default true). Defaults: Cover 0.5, Density 0.7.
- `Sky.SunAngularSize` defaults to 21 and clamps at 60. The mood uses 38.
- `MeshPart.DoubleSided` exists, default false, so the inverted hull should cull as in the mockup (⚠️ verify the look in Studio after upload).
- `UserGameSettings.SavedQualityLevel` reads `Automatic` in Studio, so the controller treats Automatic as high. A Studio attribute `TYF_SkyLow` forces the low tier for testing.

**Changes from the plan (Claude's, for Holden to judge):**
- **Low tier = 8 near + 10 mid clouds, no far ring, no silhouettes**, plus Terrain Clouds, SunRays and Bloom off. "Near ring only" left the sky nearly empty, because the near ring hides under the plateau edge from most spots (seen in the mockup).
- **Ring heights went down** (mid −150 to −80, far −450 to −330). At the planned heights the mid ring stood up like a wall at eye level.
- **Map 1 mood = ClockTime 10.5** (late morning) instead of v2's 15.2.

**Mockup renders** (Blender EEVEE, grey stand-in island, not the real map). Blender can't show Roblox's Terrain `Clouds`, so the overhead layer is missing here; only Studio can show it.

![[tyf-v3-sky-01-start-to-beacon.png]]
![[tyf-v3-sky-03-tower-cloud-sea.png]]
![[tyf-v3-sky-04-low-graphics.png]]
![[tyf-v3-sky-05-mesh-sheet.png]]
Also: `tyf-v3-sky-02-phone-width.png` (1266×585, phone aspect 2.16:1), `tyf-v3-sky-06-textures.png` (faces, equirect strip, sun, palette).

**Claude's honest read:**
- The sky gradient is clearly saturated and not washed out.
- The clouds read as cartoon puffs with outlines.
- **Weak:**
  - Cloud B and D undersides show crumpled facets from the decimation;
  - Cloud C looks thin from the side;
  - from the start room the rings mostly hide behind the plateau, so the sky above looks empty until Terrain Clouds are on;
  - the outline on far clouds may read heavy on phones.
- All of that gets judged in Studio, not here.

**Upload batch for Holden's OK** (all private, Holden's account, Open Cloud scripts):

| # | File | What | Size |
|---|---|---|---|
| 1–6 | `out/sky_v3_{px,nx,py,ny,pz,nz}.png` | Skybox faces (image/decal) | 1024², 235–311 KB each |
| 7–8 | `out/sky_v3_sun_additive.png`, `out/sky_v3_sun_alpha.png` | Sun, 2 versions to test (keep one) | 256², 18–30 KB |
| 9 | `out/sky_v3_palette.png` | Shared mesh texture | 512×256, 1.5 KB |
| 10–14 | `export/TYF_Cloud_{A..E}.glb` | Cloud meshes (model) | 640 tris, ~17 KB each |
| 15–17 | `export/TYF_Far_{CastleIsle,Spires,Windmill}.glb` | Silhouettes (model) | 156–256 tris, 13–19 KB |

- 17 uploads, no Robux (⚠️ verify the current upload quotas before the batch).
- After upload, Claude inserts the models, puts the MeshParts in `ReplicatedStorage.SkyAssets`, points them all at the palette id, applies the mood with `tools/SkyV3/ApplyMood`, and takes the Studio shots: 4 views × high/low + phone width + frame time and render stats.


## Status: Step 1b in Studio (2026-10-06): uploaded, applied, measured; one design question open
**Upload:** Holden OK'd the 17-file batch. It went up through Open Cloud (`upload_image.sh` / `upload_model.sh`; the key never printed). Ids are in the hub asset table and the AssetLibrary README; decal ids are also in `art/sky_v3/upload_ids.txt`.

**In the place (Edit mode):**
- `ReplicatedStorage.SkyAssets` holds 8 MeshParts (imported upright; all share one embedded palette texture).
- The CastleNoon mood is applied, with nothing skipped: skybox faces, the alpha sun at size 38, Clouds (0.55 / 0.3), GlobalWind, Atmosphere, SunRays, ClockTime 10.5.
- Workspace attributes: `TYF_SkyMood = CastleNoon`, `TYF_SkyCentre = (6, 10, 123)` (the v2 slice centre, meadow y 10).
- **Holden must save the place** (File → Save to File).

**Tuning after the first shots** (code; gate PASS):
- Atmosphere density 0.2 → **0.12**;
- near 16 → 20 clouds (radius 180–320, y −110 to −50);
- mid 20 → 24 (y −170 to −100);
- far 30 → 40, radius 1,400–2,200, raised to y −260 to −160 so the cloud tops reach the horizon.

**Measured in Studio** (Holden's PC, Studio in front; not a phone):
- Frame time 16.7 ms average, 18.2 ms worst over 180 frames at quality 21 with every layer on: Studio's 60 fps cap, so no visible cost on this PC.
- Console clean.
- Draw calls and triangles were **not** measured: render stats aren't readable from scripts.

**Finding: Roblox culls distant objects by graphics quality.** Test: red marker clouds at set distances, Studio rendering quality set with `settings().Rendering.QualityLevel` from a Client `execute_luau`.

| Quality level | Markers that drew (distance from camera) | Not drawn |
|---|---|---|
| 1 | 150, 250 | 350+ |
| 5 | 400 | 600+ |
| 10 | 400, 600 | 900+ |
| 21 | 600 … 3,000 (all) | none |

- A 600-wide cloud at 600 studs **did** draw at level 1, while a 1,200-wide cloud at 1,200 did not. So culling goes by the distance to the object's nearest surface, not its centre (one test, ⚠️ verify on a phone).
- At level 1, parts of the castle 400 studs away vanished too: this is engine-wide, not just the sky.
- **Terrain `Clouds` draw at every level** (they're part of the sky, not parts). So the overhead layer always works.
- Effect: the **far ring and silhouettes only show at high quality.** On most phones (low/mid quality) the player sees the near ring plus Terrain Clouds. Studio's own "Automatic" level culled the mid and far rings too, which is why the first shots looked sparse.

**Shots** (`attachments/`):
- `tyf-v3-sky-s01-overview-q21.jpg` (everything: a full cloud sea, the castle-isle silhouette);
- `tyf-v3-sky-s02-overview-q10.jpg`;
- `tyf-v3-sky-s03-overview-q01.jpg` (only nearby clouds; the castle partly culled);
- `tyf-v3-sky-s04-runner-q10.jpg` and `tyf-v3-sky-s06-runner-q10-phone-width-844.png` (a downscale, not a phone);
- `tyf-v3-sky-s05-cloudsea-automatic.jpg`;
- draw-distance tests `tyf-v3-sky-t1..t4-*.jpg`.

![[tyf-v3-sky-s01-overview-q21.jpg]]
![[tyf-v3-sky-s04-runner-q10.jpg]]
![[tyf-v3-sky-s03-overview-q01.jpg]]

**Claude's honest read:**
- **High quality:** looks like a real living cloud sea; the outlines and toon bands work in Roblox; the sky stays saturated.
- **Overcrowding:** around the small v2 slice it's too busy, because the rings are sized for Map 1's 400×400 island.
- **Up close:** facets on cloud undersides and a few black hull slivers in concave spots.
- **Low quality:** the sky is mostly the gradient + Terrain Clouds + a few nearby puffs. Clean and saturated, but not a cloud sea.

**Options for the draw-distance problem (Holden decides):**
1. **Camera-following horizon ring** (recommended): one cloud ring that follows the camera (x, z) at ~250–350 studs, scaled down so it reads as far away, sitting below eye level. It draws even at level 1. Far clouds barely show parallax anyway. Risk: it can clip into the island underside when viewed from outside the island.
2. **Bring all rings inside ~350 studs of the island edge.** Works at every level, but loses depth and crowds the near view.
3. **Accept it:** the far ring and silhouettes are a high-quality bonus; low quality relies on Terrain Clouds.

Not recommended: a soft cloud band baked into the skybox horizon. It works at every level, but it breaks Holden's "no baked clouds" rule.

## Layers (top to bottom, DRAFT values to tune by screenshot)
| # | Layer | How | Starting values |
|---|---|---|---|
| 1 | Gradient skybox | 6 faces, 1024², generated by a numpy script from **one equirectangular gradient**, so there are no seams. **No clouds and no sea painted in** | Zenith `#1F6FE5` → upper sky `#3E9BFF` → horizon `#A8E2FF` → a thin warm band `#FFE7B8` right at the horizon → below the horizon `#8FD3FF` (matches the cloud-sea tops, so no hard line) |
| 2 | Dynamic `Clouds` | `Clouds` instance parented to `Workspace.Terrain` (required for it to render, Roblox docs) | `Cover` 0.55, `Density` 0.3, `Color` `#FFF9F2`. `Workspace.GlobalWind` ≈ (6, 0, 2), gentle drift. GlobalWind also moves particles that use `WindAffectsDrag` |
| 3a | Near cloud sea | 12–16 big puff meshes (60–120 studs) under and around the island at y −60 to −15 | Drift 1–2 studs/s; the whole layer wraps around the island |
| 3b | Mid ring | ~20 meshes (150–300 studs) in a ring 600–900 studs out, a bit below the horizon | Rotates around the island centre ~0.3°/s (one `PivotTo` per layer per frame) |
| 3c | Far ring | ~30 meshes (400–800 studs) 1,500–2,500 studs out, on the horizon | ~0.1°/s. ⚠️ verify: low graphics quality cuts view distance, so the far ring may vanish; the skybox horizon then still reads |
| 4 | Silhouettes | 3 meshes: a floating island with a castle, rock spires, a windmill islet. 900–2,000 studs away, away from the sun direction | Slow bob ±4 studs over ~20 s. Colours lighter and bluer with distance but **still saturated** |
| 5 | Sun | `Sky.SunTextureId` = our painted sun (256², alpha, a soft toon disc + short rays); `Sky.SunAngularSize` about 2× the default (⚠️ verify the property range in Studio) | `SunRays` Intensity 0.07, Spread 0.6. Bloom stays at threshold 1.6 (v2) |
| 6 | Atmosphere | Back on, but thin: tints the horizon, not the near cloud sea | Density ~0.2, Offset ~0.1, Haze 0, Glare 0.3, Color `#CFEFFF`, Decay `#9FD0FF` (v2 lesson: haze painted over the below-horizon art; with no painted sea that risk is lower) |

- **Toon cloud meshes:**
  - 4–5 variants (puff clusters made from the superellipsoid/puffy helpers in `kitlib6.py`), 400–800 triangles each.
  - **One shared 1024² toon atlas:** white top, a hard-edged soft-lilac shadow band underneath, a slightly warm rim. Crisp bands, no blurry gradient (art rule).
  - Outline: a **baked inverted-hull shell** in the mesh. Using `Highlight` on ~70 clouds is too costly: each Highlight is its own draw call plus a post pass.
  - MeshParts: Anchored, `CanCollide`/`CanTouch`/`CanQuery` false, `CastShadow` false.
- **Motion:** pure wrap/rotate maths in a tested `Rules` module. The controller moves whole layers (3 `PivotTo` calls per frame), not 70 parts.

## Per-map sky moods (DRAFT, Holden picks the map themes later)
| Map | Mood | Notes |
|---|---|---|
| 1 Castle Sky Island | Bright late morning, saturated blue, white puffy clouds, warm horizon band | Built first |
| 2 (Candy Factory if chosen) | Peach-pink sunset, candy-floss pink clouds, lilac shadows | Seen through big factory windows and a skylight |
| 3 (Toy Room if chosen) | Golden late afternoon through a giant window | Indoor: sky only through the window. `Clouds` off indoors (Lighting note) |
- One `SkyMoods.luau` data table per mood: gradient stops, sun, Clouds, Atmosphere, ColorCorrection, cloud-mesh tint, silhouette set. **Lighting is applied by the server at map load** (it replicates). **Cloud layers are spawned by each client.**
- **Each mood needs its own 6 skybox faces** (a skybox can't be tinted by a property), so 6 images per map. Only Map 1 now.
- Time-of-day variety per round: **later** (USER). The mood table leaves room for it.

## Low-graphics fallback (test both)
- The client reads the quality level (⚠️ verify the right API: `UserSettings().GameSettings.SavedQualityLevel` reports "Automatic" for many players).
- **Low quality:**
  - `Clouds.Enabled = false` locally (property exists, verified in Studio 2026-10-06);
  - fewer clouds: 8 near + 10 mid, no far ring, no silhouettes (changed 2026-10-06 after the mockup; see Status);
  - SunRays and Bloom off.
- **Test plan:** the same 4 shots at Studio quality level 10 and level 1 (⚠️ verify the Studio menu path for the edit quality level), and frame time with Studio as the front window.

## Mockup and screenshot plan (what Holden sees, in order)
1. **Blender mockup:**
   - world background = the gradient (equirectangular);
   - the 3 cloud layers and silhouettes in place;
   - a grey stand-in island and keep;
   - camera at Runner eye height in the start room looking at the beacon;
   - renders: 1920×1080 and a phone frame (2532×1170 crop), plus a contact sheet of the cloud variants (front, side, three-quarter) and the sun texture.
2. **Holden approves** → upload the images and meshes (private).
3. **Studio shots:**
   1. start room → beacon;
   2. mid-map over the cloud sea;
   3. tower-top panorama;
   4. phone-width downscale of shot 1.

   Each at high and low quality: 8 images, plus frame time and render stats (draw calls, triangles).

## Asset list and cost
| Asset | Count | Size | Upload |
|---|---|---|---|
| Skybox faces (gradient, Map 1) | 6 | 1024² PNG | Private image (the approved category: our own sky textures) |
| Sun texture | 1 | 256² PNG with alpha | Private image |
| Cloud toon atlas | 1 | 1024² PNG | Private image |
| Silhouette atlas | 1 | 1024² PNG | Private image |
| Cloud meshes | 4–5 | 400–800 tris | Model upload via Open Cloud (`upload_model.sh`; USER 2026-10-06), after Holden OKs the batch |
| Silhouette meshes | 3 | 1–3k tris | Same |
- **Images** go up with `upload_image.sh` (Open Cloud key, USER 2026-10-06), after Holden OKs the batch.
- **Money:** no Robux; uploads are free (⚠️ verify the current upload quotas before the batch).
- **Runtime estimates (⚠️ verify by measuring):** ~70 cloud instances × ~600 tris ≈ 42k tris; silhouettes ≈ 6k. With identical MeshId + TextureID, the clouds should batch into a handful of draw calls. `Clouds` GPU cost is unknown on phones; the fallback covers it.
- The v2 skybox ids stay uploaded (asset table in [[Trap-Your-Friends]]). v3 replaces them in `CastleSky.luau`; nothing gets deleted.

## Files (planned)
- **Art scripts:**
  - `art/sky_v3/make_gradient_sky.py`: equirect gradient → 6 cube faces + preview;
  - `art/sky_v3/make_sun.py`;
  - `art/sky_v3/clouds_blender.py`: cloud variants, toon bake, inverted hull, GLB export;
  - `art/sky_v3/silhouettes_blender.py`;
  - `art/sky_v3/render_mockup.py`.
- **Code:**
  - `src/shared/Lighting/SkyMoods.luau`: data;
  - `src/shared/Lighting/Apply.luau`: extended to apply a mood;
  - `src/shared/Lighting/CastleSky.luau`: new ids;
  - `src/shared/Rules/CloudDrift.luau` + `tests/CloudDrift.spec.luau`: wrap and rotate maths;
  - `src/client/Controllers/SkyLayersController.luau`: spawns and drifts the layers, low-quality fallback;
  - the templates live in `ReplicatedStorage.SkyAssets` (MeshParts, after upload).

## Pitfalls
- **No clouds baked into the skybox.** They never line up with the 3D world (v2 lesson).
- **Atmosphere:** keep it thin. Density above ~0.3 washes the saturated look out.
- **Far meshes:** check that they don't pop on streaming. Client-created parts aren't streamed, but render distance still applies at low quality.
- **Inverted hull:** the shell must be a separate flipped-normal part of the same mesh, and the MeshPart must not be double-sided (⚠️ verify how Roblox renders a flipped shell).

## Related
[[Trap-Your-Friends]] · [[Trap-Your-Friends-v3-Plan]] · [[Trap-Your-Friends-Style-Test-v2-Feedback]] · [[Trap-Your-Friends-Map1-Layout]] · [[Trap-Your-Friends-Map-Plan]] · [[Lighting-And-Atmosphere]] · [[Trap-Your-Friends-Art-Style-Guide]] · [[Blender-To-Roblox-Pipeline]]

## Sources
- Roblox docs, Clouds (checked 2026-10-06): https://create.roblox.com/docs/environment/clouds (Cover 0–1, Density, Color; must be parented under Terrain; moves with global wind; no quality-level notes on that page).
- Roblox docs, Sky class: https://create.roblox.com/docs/reference/engine/classes/Sky (that page didn't state the SunAngularSize range: verify in Studio).
- Reference stills: `Assets/Reference-Captures/Retro-Stud/sky-model-study-a-gag-sab-fisch.jpg`, `sky-model-study-b-babft-bss-doomspire.jpg` (observations, not measurements).
- Devforum sky threads listed in [[Trap-Your-Friends-Style-Test-v2-Feedback]].
