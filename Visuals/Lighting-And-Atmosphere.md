---
tags: [visuals/lighting]
status: draft
updated: 2026-10-04
confidence: medium
---
# Lighting and Atmosphere

## TL;DR
- **`Lighting.Technology` is superseded** (as of the 2026 docs) by two properties: **`LightingStyle`** (`Realistic` = most advanced lighting/shadows; `Soft` = flat, retro-Roblox look) and **`PrioritizeLightingQuality`** (true = keep shadows/high-quality shaders at close range as quality drops; false = keep view distance). `Technology` remains Studio-only/non-scriptable; `Unified` and `Legacy` are deprecated.
- **Default choice**: `LightingStyle = Realistic`, `PrioritizeLightingQuality = true` for most games; `Soft` for cartoony simulators/obbies wanting the classic flat look.
- Build mood with **Atmosphere** (Density 0.25–0.4, Haze 0–2) + **Sky** + **ColorCorrection** (Saturation +0.1–0.3 for kids' genres, Contrast +0.05–0.15) + mild **Bloom**. Skip DepthOfField in gameplay (blurs, costs, hurts readability); use it only in menus/cutscenes.
- **Mobile cost** comes from shadow-casting local lights, many lights in view, post effects, and fill-rate. Engine disables shadows below graphics quality 4 — design scenes that still read without shadows.
- Light ranges are **capped at 120 studs**; disable `Shadows` on decorative lights and `CastShadow` on small/moving parts.
- Lighting sells thumbnails: set up a separate bright, saturated "photo" lighting preset for thumbnail/icon captures (see [[Thumbnails-And-Icons]]).

## Lighting technology (2026 model)

| Property | Values | Notes |
|---|---|---|
| `Lighting.LightingStyle` | `Realistic`, `Soft` | Artistic intent. `ShadowSoftness` (0 hard–1 soft) only applies with `Realistic`. |
| `Lighting.PrioritizeLightingQuality` | bool | As device quality drops: true keeps lighting quality near camera; false keeps draw distance. Per docs, `Soft` + true uses shadow maps rather than voxel lighting. |
| `Lighting.Technology` (legacy) | `Voxel` (4×4×4 voxel lighting), `ShadowMap` (crisp sun shadows), `Future` (most advanced, local light shadows), `Compatibility` (deprecated), `Legacy`/`Unified` (deprecated) | Non-scriptable; superseded. Older tutorials reference these — map "Future" ≈ Realistic + PrioritizeLightingQuality. ⚠️ verify: exact mapping of old Technology values to the new pair in Studio's property migration. |

Old "Compatibility" look: use Voxel-style/Soft lighting + `ColorGradingEffect` with `TonemapperPreset = Retro`.

## Core Lighting properties (cheat sheet)
- `Ambient` (indoor/occluded hue; keep dark, ~(70,70,80)), `OutdoorAmbient` (outdoor fill; ~(120,120,130) daytime), `Brightness` (sun; 2–3 typical), `ColorShift_Top` (sun-facing tint; warm in evenings), `ColorShift_Bottom`.
- `EnvironmentDiffuseScale` / `EnvironmentSpecularScale` (0–1): sky-driven ambient and reflections. Set ~1 / ~1 for Realistic PBR scenes and **lower Ambient/OutdoorAmbient** to compensate; 0.2–0.5 for stylised.
- `ExposureCompensation` (−5…5; +1 = 2× exposure). Use ±0.3 to tune overall brightness instead of over-driving Brightness.
- `ClockTime`/`TimeOfDay`, `GeographicLatitude` (sun path), `GlobalShadows`, `ShadowSoftness`, `FogStart`/`FogEnd`/`FogColor` (Fog properties are hidden/superseded when Lighting contains an Atmosphere — use Atmosphere instead).

## Atmosphere, Sky, Clouds
- `Atmosphere`: `Density` (0.3 default-ish haze, 0.5+ thick fog), `Offset` (horizon blend with sky), `Color` (haze colour), `Decay` (distant colour with haze), `Glare` and `Haze` (sun glow/haze strength). Atmosphere is the best cheap depth cue and hides streaming pop-in.
- `Sky`: `SkyboxBk/Dn/Ft/Lf/Rt/Up`, `SunTextureId`, `SunAngularSize`, `MoonTextureId`, `MoonAngularSize`, `StarCount`, `CelestialBodiesShown`, `SkyboxOrientation`. Also feeds reflections when Environment*Scale > 0.
- `Clouds` (under Terrain): `Cover` (0–1), `Density`, `Color`. Dynamic clouds cost GPU; turn off for low-end-focused games or indoor maps.

## Post-processing (in Lighting or Camera)
| Effect | Key props | Recommended |
|---|---|---|
| `ColorCorrectionEffect` | Brightness, Contrast, Saturation, TintColor | Saturation +0.15, Contrast +0.1 (stylised); also gameplay feedback (red tint on low HP) |
| `ColorGradingEffect` | `TonemapperPreset` (`Default`, `Retro`) | Default unless chasing retro |
| `BloomEffect` | Intensity, Size, Threshold | Intensity 0.6–1, Size 24, Threshold 1.0–1.5 (low threshold = everything glows) |
| `SunRaysEffect` | Intensity, Spread | Intensity 0.05–0.15, Spread 0.5–1 |
| `DepthOfFieldEffect` | FarIntensity, FocusDistance, InFocusRadius, NearIntensity | Menus/cutscenes only; disable during gameplay |
| `BlurEffect` | Size | 8–16 behind modal menus (see [[UI-Architecture]]) |

## Genre presets (starting points — tune by eye on phone)

| Genre | Style | Clock | Brightness | Ambient / OutdoorAmbient | Atmosphere (Density / Haze / Color) | ColorCorrection | Bloom |
|---|---|---|---|---|---|---|---|
| Simulator / tycoon (bright, kid-friendly) | Soft or Realistic | 13–14 | 3 | (110,110,120) / (150,150,160) | 0.25 / 0 / light blue | Sat +0.25, Con +0.1 | 0.7 / 24 / 1.2 |
| Obby | Soft | 14 | 2.5–3 | (100,100,110) / (140,140,150) | 0.2 / 0 / sky blue | Sat +0.2 | light |
| Horror | Realistic, PrioritizeLightingQuality true | 0–2 | 0–0.5 | (5,5,8) / (20,20,30) | 0.5–0.7 / 2–4 / grey-green | Sat −0.3, Con +0.15, TintColor cool | off/low; local SpotLight flashlight with Shadows |
| Fantasy RPG / adventure | Realistic | 16–17 (golden hour) | 2.5 | (70,60,80) / (130,120,140) | 0.35 / 1 / warm | Sat +0.1, Tint warm (255,245,230) | 0.8 / 30 / 1.0 + SunRays 0.1 |
| Shooter / competitive | Realistic | 12–14 | 2.5 | (90,90,100) / (130,130,140) | 0.25 / 0 | Con +0.05, Sat 0 | minimal (readability) |
| Night city / neon | Realistic | 22 | 1 | (20,20,35) / (40,40,70) | 0.4 / 1 / purple | Sat +0.2 | 1.2 / 32 / 0.9, Neon signage |

Store presets as Configuration/attribute tables and apply via a client module so day/night or zone transitions can tween between them.

## Lights & mobile cost
- `PointLight`, `SpotLight` (`Angle`, `Face`), `SurfaceLight`: `Range` ≤ 120 studs (hard clamp), `Brightness`, `Color`, `Shadows`.
- Shadow-casting local lights are expensive; give shadows only to a few key lights (horror flashlight, hero lamp). Decorative lamps: `Shadows = false`, Range 8–16.
- `BasePart.CastShadow = false` on small parts, foliage, moving objects, VFX parts.
- Engine auto-degrades shadows as graphics quality falls and disables them below quality level 4 → test at low graphics quality: lights and silhouettes must still read.
- Post effects each cost a full-screen pass; 3–4 is fine on mid phones; avoid DepthOfField + SunRays + heavy Bloom combo on mobile-majority games.

## Day/night (client-side for smoothness)

`Lighting.ClockTime` is tagged NotReplicated in the API (its string twin `TimeOfDay` is the replicated one). Rather than stepping time on the server, derive it on every client from synced server time — deterministic, smooth, zero network traffic:

```lua
--!strict
-- StarterPlayerScripts/DayNight.client.luau
local Lighting = game:GetService("Lighting")
local RunService = game:GetService("RunService")
local Workspace = game:GetService("Workspace")

local DAY_LENGTH_SECONDS = 20 * 60 -- one 24h cycle every 20 minutes
local START_HOUR = 8

RunService.Heartbeat:Connect(function()
	local t = Workspace:GetServerTimeNow()
	Lighting.ClockTime = (START_HOUR + t / DAY_LENGTH_SECONDS * 24) % 24
end)
```

Server logic that depends on time of day (night-only spawns) computes the same formula with `Workspace:GetServerTimeNow()`.

## Checklist
- [ ] LightingStyle + PrioritizeLightingQuality chosen deliberately
- [ ] Atmosphere present (depth + hides streaming)
- [ ] ≤ 4 post-processing effects; no gameplay DepthOfField
- [ ] Decorative lights shadowless; small/moving parts CastShadow off
- [ ] Scene tested at graphics quality 1–3 on a phone
- [ ] Thumbnail/photo lighting preset saved

## Pitfalls
- Following old tutorials that set `Lighting.Technology` from a script — it's non-scriptable and now superseded.
- Bloom Threshold too low → white, washed-out UI-like scenes; thumbnails lose contrast.
- High `EnvironmentDiffuseScale` with high Ambient → flat, grey, over-lit look.
- Pitch-black horror on mobile → players see nothing on dim phone screens; keep a minimum OutdoorAmbient and use local lights.
- Dozens of shadow-casting point lights in a tycoon → mobile FPS collapse.

## Related
- [[Visuals/_Index]] · [[Art-Direction]] · [[Shaders-Materials-And-Surfaces]] · [[VFX-Particles-Beams-Trails]] · [[Thumbnails-And-Icons]]

## Sources
- Global lighting (LightingStyle, PrioritizeLightingQuality, ShadowSoftness) — https://create.roblox.com/docs/environment/lighting
- Lighting API (Technology superseded, ExposureCompensation range, 120-stud light range clamp, EnvironmentDiffuseScale) — https://create.roblox.com/docs/reference/engine/classes/Lighting ; enum Technology — https://create.roblox.com/docs/reference/engine/enums/Technology
- Post-processing effects incl. ColorGradingEffect — https://create.roblox.com/docs/environment/post-processing-effects
- Atmosphere — https://create.roblox.com/docs/environment/atmosphere ; Sky — https://create.roblox.com/docs/environment/skybox ; Clouds — https://create.roblox.com/docs/environment/clouds
- Light sources — https://create.roblox.com/docs/effects/light-sources
- Performance (shadows disabled below quality 4, CastShadow advice) — https://create.roblox.com/docs/performance-optimization/improve
- All checked via Roblox/creator-docs GitHub source (2026-10-02 commit) on 2026-10-04. Genre preset numbers are author starting points, not Roblox guidance.
