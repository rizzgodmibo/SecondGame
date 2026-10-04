---
tags: [visuals/rendering, visuals/materials]
status: draft
updated: 2026-10-04
confidence: medium
---
# Shaders, Materials and Surfaces (what to use instead of custom shaders)

**Roblox has no custom shader/HLSL/shader-graph support.** Everything "shader-like" is built from engine materials, PBR textures, emissive masks, post-processing, Highlights, transparency/blend tricks, animated textures, and runtime-editable images/meshes.

## TL;DR
- **Default stack**: built-in `Enum.Material`s for most surfaces → **`MaterialVariant`** (custom tiling PBR material, applied by name or as a global override) for a consistent stylised world → **`SurfaceAppearance`** (per-mesh PBR + emissive) for hero props and characters.
- **Glow** = `Neon` material or `SurfaceAppearance` emissive mask + `BloomEffect`. **Outlines/x-ray** = `Highlight` (≤ 255 per client). **Scrolling/animated** = `Texture.OffsetStudsU/V` tweened, `Beam.TextureSpeed`, flipbook particles.
- **Glass refraction doesn't render on mobile**; design glass to look fine as tinted transparency.
- `EditableImage` / `EditableMesh` give runtime pixel/vertex control but require the owner to be 13+ ID-verified and to toggle **Enable Mesh / Image APIs** in the Creator Dashboard for published games; strict client memory budgets; only one displayed EditableImage updates per frame.
- Stylised low-poly + flat colours + good lighting beats realistic PBR on mobile for both performance and thumbnail readability — see [[Art-Direction]].

## Substitutes map

| Want (other engines) | Roblox approach |
|---|---|
| Custom surface shader / PBR | `SurfaceAppearance` on a MeshPart: `ColorMap`, `NormalMap` (OpenGL tangent-space), `RoughnessMap`, `MetalnessMap`, `EmissiveMaskContent` + `EmissiveStrength` + `EmissiveTint`; `Color` tint; `AlphaMode` |
| Tiling world material | `MaterialVariant` under `MaterialService`: `BaseMaterial`, PBR maps, `StudsPerTile`, `MaterialPattern` (`Regular`/`Organic` — Organic breaks visible tiling), `CustomPhysicalProperties`; set as **material override** to replace a base material everywhere (also the only way to restyle terrain) |
| Emissive / glow | `Neon` material (fixed glow, cheap) or emissive mask (per-pixel); amplify with `BloomEffect` (Threshold ~0.9–1.5, Intensity 0.5–1, Size 24–40) |
| Rim light / outline / x-ray | `Highlight`: `FillColor`, `FillTransparency`, `OutlineColor`, `OutlineTransparency`, `DepthMode` (`AlwaysOnTop` = see through walls, `Occluded`). Cap ~5–10 in gameplay; engine ignores beyond 255 |
| Hologram / force field | `ForceField` material (animated) or transparent Neon + scrolling `Texture` + `Highlight` |
| Scrolling texture (lava, conveyors, water) | `Texture` instance on a face: tween `OffsetStudsU`/`OffsetStudsV` on the client (RenderStepped or looped Tween); `StudsPerTileU/V` for scale |
| UV-animated beams/lasers | `Beam` with `TextureMode = Wrap`, `TextureSpeed` |
| Dissolve | Swap `Transparency` + particle burst; or `EditableImage` writing alpha into a texture (expensive) |
| Vertex animation (flags, grass) | Skinned mesh + bones animated by an `AnimationController` (cheap on GPU), or `EditableMesh` per-frame (CPU-heavy, avoid for many objects). Terrain grass has built-in wind (`Workspace.GlobalWind`) |
| Toon shading | `Lighting.LightingStyle = Soft`, flat colours, `Highlight` outline on key characters, painted shadows in albedo, low `EnvironmentSpecularScale` |
| Colour grading / LUT | `ColorCorrectionEffect` (Brightness, Contrast, Saturation, TintColor) + `ColorGradingEffect.TonemapperPreset` (`Default`/`Retro`) — see [[Lighting-And-Atmosphere]] |
| Render-to-texture / 3D in UI | `ViewportFrame` (own `CurrentCamera`, `Ambient`, `LightColor`, `LightDirection`, optional `Sky` child as reflection cubemap. Caveats per API: no shadows or post-processing, Neon/Glass render at lowest quality, environment diffuse/specular treated as 0 (metalness looks different), nested GuiObjects unsupported; particles don't render ⚠️ verify: particle support in ViewportFrames). Use for shop item previews and pet cards |
| Decals / grunge | `Decal` (stretch) or `Texture` (tile); for meshes use `AlphaMode = Overlay`/`TintMask` on SurfaceAppearance |
| Procedural texture | `EditableImage` (`DrawRectangle`, `DrawCircle`, `DrawLine`, `DrawImage`, `WritePixelsBuffer`) → `Content.fromObject(img)` into `ImageLabel.ImageContent` / `MeshPart.TextureContent` |
| Procedural mesh | `EditableMesh` (`AddVertex`, `AddTriangle`, `SetUV`, `SetPosition`…) → `AssetService:CreateMeshPartAsync(Content.fromObject(mesh))` |

## SurfaceAppearance details
- Only on `MeshPart`s (not Parts). Overrides `MeshPart.TextureID`. Per the API reference, **most SurfaceAppearance properties cannot be modified by scripts** (pre-processing too expensive) — swap/clone pre-made SurfaceAppearance instances instead (or `AssetService:CreateSurfaceAppearanceAsync`). Look varies by device graphics quality — preview at low quality.
- `AlphaMode`: `Overlay` (default; transparent areas show `MeshPart.Color` — use for one mesh in many colours), `Transparency` (real cut-out/blend: leaves, hair cards, lace), `TintMask` (alpha marks where `SurfaceAppearance.Color` tints — recolourable cosmetics), `Opaque` (ignore alpha).
- PBR map budgets (Roblox guideline): 256² per 2×2×2-stud object, 512² for 4×4×4, **1024² max** for 8×8×8 (characters). See [[Blender-To-Roblox-Pipeline]].
- Image formats for maps: Albedo RGB 24-bit; Normal RGB 24-bit **OpenGL (Y+)**; Roughness/Metalness/Emissive single-channel 8-bit greyscale.
- **Emissive masks** went live for published experiences on **2026-02-12**. They use the Neon pipeline, so they work on all devices, and the red channel of an RGB mask is read.
  - The glow colour comes from the **ColorMap**: final ≈ `(EmissiveMask × EmissiveStrength × EmissiveTint + light) × ColorMap`. The Studio inspector slider for EmissiveStrength runs 0–40.
  - **Practical rule:** glowing texels must be painted in the glow colour *in the ColorMap*. A dark albedo under a white mask does not glow. Leave EmissiveTint white and drive the brightness with EmissiveStrength.
  - Used this way for [[Fantasy-Creatures-Set]] (Cinder Drake throat embers).
  - ⚠️ verify: the formula is quoted from the Studio Beta thread, not from the docs page. Check it in Studio on a test mesh.

## Built-in material notes
- `Neon`: unlit, glows with Bloom; cheap; overuse makes scenes noisy and thumbnails blown-out.
- `Glass`: refraction **not supported on mobile**; on PC it depends on graphics quality. Set Transparency 0.3–0.6 and a tint so mobile still reads.
- `ForceField`: animated, unlit; good for shields/zones.
- `SmoothPlastic` + good lighting is the cheapest clean stylised look; `Plastic` has subtle noise.
- Material/texture memory is per unique texture: 10 MaterialVariants × 4 maps × 1024² is substantial on mobile — keep custom materials ≤ ~8–12 per place and reuse.

## Scrolling texture (client)

```lua
--!strict
-- StarterPlayerScripts/ScrollingTextures.client.luau
-- Tag any Texture instance "Scroll" and give it attributes SpeedU / SpeedV (studs per second).
local CollectionService = game:GetService("CollectionService")
local RunService = game:GetService("RunService")

local active: { [Texture]: Vector2 } = {}

local function add(inst: Instance)
	if inst:IsA("Texture") then
		local u = (inst:GetAttribute("SpeedU") :: number?) or 0
		local v = (inst:GetAttribute("SpeedV") :: number?) or 1
		active[inst] = Vector2.new(u, v)
	end
end

local function remove(inst: Instance)
	if inst:IsA("Texture") then
		active[inst] = nil
	end
end

for _, inst in CollectionService:GetTagged("Scroll") do
	add(inst)
end
CollectionService:GetInstanceAddedSignal("Scroll"):Connect(add)
CollectionService:GetInstanceRemovedSignal("Scroll"):Connect(remove)

RunService.RenderStepped:Connect(function(dt: number)
	for texture, speed in active do
		-- wrap to avoid float precision loss over long sessions
		texture.OffsetStudsU = (texture.OffsetStudsU + speed.X * dt) % texture.StudsPerTileU
		texture.OffsetStudsV = (texture.OffsetStudsV + speed.Y * dt) % texture.StudsPerTileV
	end
end)
```

## EditableImage example (procedural badge)

```lua
--!strict
-- LocalScript example: draws a progress ring background into an ImageLabel.
-- Published games: owner must enable "Enable Mesh / Image APIs" in Creator Dashboard (13+ & ID verified).
local AssetService = game:GetService("AssetService")

local function makeBadge(label: ImageLabel, fill: Color3)
	local ok, image = pcall(function()
		return AssetService:CreateEditableImage({ Size = Vector2.new(128, 128) })
	end)
	if not ok or image == nil then
		return -- memory budget exhausted or API disabled: keep the static fallback image
	end
	image:DrawRectangle(Vector2.zero, Vector2.new(128, 128), Color3.new(0, 0, 0), 1, Enum.ImageCombineType.Overwrite)
	image:DrawCircle(Vector2.new(64, 64), 56, fill, 0, Enum.ImageCombineType.BlendSourceOver)
	label.ImageContent = Content.fromObject(image)
end

return makeBadge
```

Verified 2026-10-04: `DrawRectangle(position, size, color, transparency, combineType)`, `DrawCircle(center, radius, color, transparency, combineType, antiAliasing?)`; default size 512×512, **max 1024×1024**, cannot be resized. ⚠️ verify: the options-table key name `Size` for `CreateEditableImage` (docs say "option table" without naming the key in the summary).

## Checklist
- [ ] ≤ ~10 custom MaterialVariants; material overrides set for terrain if stylised
- [ ] Hero props use SurfaceAppearance with ≤ 1024² maps; background props use built-in materials
- [ ] Glass looks acceptable with refraction off (test on phone)
- [ ] Highlights capped and cleaned up
- [ ] Editable APIs have a static fallback path

## Pitfalls
- DirectX-style (Y−) normal maps → inverted bumps; Roblox needs OpenGL tangent-space.
- Expecting `SurfaceAppearance` on a basic Part — only MeshParts.
- 4K textures everywhere "because supported" — mobile downsamples them anyway and memory spikes cause crashes.
- Relying on EditableImage/EditableMesh without the Dashboard toggle → works in Studio, fails in production.
- Bloom + Neon everywhere → white thumbnails/screenshots that don't read at icon size.

## Related
- [[Visuals/_Index]] · [[Lighting-And-Atmosphere]] · [[Blender-To-Roblox-Pipeline]] · [[VFX-Particles-Beams-Trails]] · [[Art-Direction]]

## Sources
- Materials, custom materials, overrides, Glass-on-mobile note — https://create.roblox.com/docs/parts/materials
- PBR textures / SurfaceAppearance (5 maps, alpha modes, emissive) — https://create.roblox.com/docs/art/modeling/surface-appearance
- Texture specifications (formats, OpenGL normals, PBR budgets) — https://create.roblox.com/docs/art/modeling/texture-specifications
- Highlighting — https://create.roblox.com/docs/effects/highlighting
- ViewportFrames — https://create.roblox.com/docs/ui/viewport-frames
- EditableImage (verification toggle, memory, one-update-per-frame) — https://create.roblox.com/docs/reference/engine/classes/EditableImage ; EditableMesh — https://create.roblox.com/docs/reference/engine/classes/EditableMesh ; AssetService — https://create.roblox.com/docs/reference/engine/classes/AssetService
- All checked via Roblox/creator-docs GitHub source (2026-10-02 commit) on 2026-10-04.
