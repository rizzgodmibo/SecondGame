---
title: Lighting Service Properties
date: 2026-10-05
type: research
status: done
area: world
game: none
source: claude
tags: [roblox, lighting, properties, reference]
---

# Lighting Service Properties
Source: Roblox Creator Docs, `Lighting` class (checked 2026-10-05). Back to [[Lighting Overview]].

## The look: LightingStyle (replaces Technology)
| Property | What it does | Notes |
|---|---|---|
| `LightingStyle` | `Soft` = stylized, flatter look with softer lights/shadows. `Realistic` = naturalistic, crisp shadows, local lights cast real shadows | New experiences start on **Soft**. Switch to Realistic for the campfire/outdoor style in [[Lighting Recipes]] |
| `PrioritizeLightingQuality` | When quality drops, `true` keeps shadows/shaders at close range, `false` keeps view distance | Soft + this enabled uses shadow maps instead of voxel lighting |
| `Technology` | Old system: Voxel, ShadowMap, Future (Compatibility is deprecated) | Studio-only, not scriptable. Voxel = 4x4x4 stud light grid. ShadowMap = crisp sun shadows. Future = most advanced |

## Light color and brightness
| Property | Default | Plain-English meaning |
|---|---|---|
| `Brightness` | | Strength of the sun/moon light on the world |
| `Ambient` | 0,0,0 | Fill color for areas **blocked from the sky** (indoors, under trees) |
| `OutdoorAmbient` | 127,127,127 | Fill color for areas **open to the sky**. Effective value is clamped to be at least `Ambient` per channel |
| `ColorShift_Top` | | Tint on surfaces facing the sun/moon |
| `ColorShift_Bottom` | | Tint on the opposite surfaces (hard to notice with GlobalShadows on) |
| `ExposureCompensation` | 0 | Range -5 to 5. +1 = twice the exposure, -1 = half. Applied before tonemapping, so it is a quick global brightness knob |
| `EnvironmentDiffuseScale` | 0 | Ambient light derived from the sky; changes with sky and time of day. If you raise it, lower Ambient/OutdoorAmbient |
| `EnvironmentSpecularScale` | 0 | Makes smooth/metal surfaces reflect the environment. Needed for convincing metal |

**Gotcha:** if `GlobalShadows` is false, there is no indoor/outdoor split, `OutdoorAmbient` is ignored, and `Ambient` applies everywhere.

## Time and sun
| Property | Meaning |
|---|---|
| `ClockTime` | Hours as a number (17 = 5 pm, 17.5 = 5:30 pm). Does not change by itself in game |
| `TimeOfDay` | Same thing as a "HH:MM:SS" string. Changing one updates the other |
| `GeographicLatitude` | Shifts where the sun sits for every time of day |
| `GetSunDirection()` / `GetMoonDirection()` | Vector3 direction, useful for scripts. Still points below the horizon when the sun has set |
| `SetMinutesAfterMidnight(n)` | Sets time numerically, allows values past 24h. Handy for [[Lighting Recipes#Day night cycle]] |
| Moon phase | Fixed. `GetMoonPhase()` always returns 0.75 |

## Shadows
| Property | Meaning |
|---|---|
| `GlobalShadows` | Voxel-based shadows in sheltered areas. Voxels are 4x4x4 studs, so objects need to be bigger than that for a realistic shadow |
| `ShadowSoftness` | Default 0.2. Blurriness of shadows. Only works in ShadowMap/Future-capable setups on capable devices |

## Fog (old way)
`FogColor`, `FogStart`, `FogEnd` still exist but are **hidden when an Atmosphere object is present**. Use [[Atmosphere]] instead.

## Deprecated / do nothing
`Outlines`, `ShadowColor`, and the lowercase method variants are deprecated.

## Event worth knowing
`Lighting.LightingChanged` fires on most Lighting changes or when a Sky is added/removed. It does **not** fire for GlobalShadows or fog changes.
