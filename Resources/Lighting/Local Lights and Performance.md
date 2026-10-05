---
title: Local Lights and Performance
date: 2026-10-05
type: research
status: done
area: world
game: none
source: claude
tags: [roblox, lighting, pointlight, spotlight, performance, mobile, reference]
---

# Local Lights and Performance
Back to [[Lighting Overview]].

## Light objects
| Light | Shape | Use for |
|---|---|---|
| `PointLight` | Omnidirectional, spreads in all directions | Campfires, lamps, candles, glowing orbs |
| `SpotLight` | One direction, cone with an Angle | Flashlights, stage lights, car headlights |
| `SurfaceLight` | Projects from one face of a part | Panels, windows, screens |

Range is capped at **120 studs** for all three.

## Official example: campfire PointLight
From Roblox's outdoor lighting tutorial (needs `LightingStyle = Realistic` for good local shadows):
- Range 48 (the default was not enough to light nearby trees, rocks, and brush)
- Shadows enabled (so surrounding objects cast shadows from the fire)
- Brightness 2
- Color 255,179,73 (a warm orange instead of white)

Rule of thumb: warm local lights for cozy and fire, cool for sci-fi and night. Use `Shadows` only where they add a lot, since they cost performance on weak devices.

## What costs performance (and what to do)
| Fact | Source |
|---|---|
| Shadow cost, cheapest to most expensive: narrow **SpotLight** (under about 120 degrees), then narrow **SurfaceLight**, then **PointLight** (most expensive by a margin). A wide spot angle becomes almost as expensive as a point light | Roblox staff post, Future is Bright phase 3 (2020, still a good rule) |
| Realistic/Future lighting falls back to ShadowMap, or Voxel if unsupported, on devices that cannot do per-pixel lighting | same post |
| Lower graphics quality levels turn shadows off, shorten draw distance, simplify particles and beams, and drop shader effects such as water and glass | DevForum mobile optimization article |
| Big "fill" lights with Shadows on, placed close to floors or ceilings, can make Voxel and Future look very different in brightness | Roblox staff post |
| Community claim: voxel lighting cost grows roughly with the cube of a light's radius, so avoid huge ranges | DevForum thread, community member |

Practical rules:
1. Keep the number of **shadow-casting** lights small. One community guide suggests staying around 20 to 30 visible lights in a Future scene (secondhand, a rough guide).
2. Prefer narrow SpotLights over PointLights when you need shadows.
3. Only enable shadows on a light when the player is close or the light is inside a building (a trick devs use: toggle `Shadows` by distance with a script).
4. Test on the lowest quality level and on a phone before shipping a look.
5. Roblox Studio Lite and mobile Studio do not show the full lighting results, so check on desktop.

## Materials matter
In Future/Realistic lighting, local lights produce proper specular highlights, so the material (roughness, metalness) changes how a light looks. Built-in materials already use PBR. Set `EnvironmentDiffuseScale` and `EnvironmentSpecularScale` to 1 so metal reflects both the sky and your lights, see [[Lighting Service Properties]].
