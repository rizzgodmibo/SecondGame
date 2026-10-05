---
title: Atmosphere
date: 2026-10-05
type: research
status: done
area: world
game: none
source: claude
tags: [roblox, lighting, atmosphere, haze, reference]
---

# Atmosphere
Insert an `Atmosphere` object into the `Lighting` service. It scatters sunlight like real air: distant things fade into haze, the horizon glows, and the world gets depth. Back to [[Lighting Overview]].

![Sunset built with atmospheric effects (Roblox docs)](https://prod.docsiteassets.roblox.com/assets/lighting-and-effects/atmosphere/Sahara-Sunset.jpg)

## Properties
| Property | What it does | Tips |
|---|---|---|
| `Density` | How many particles are in the air. Higher = distant objects get hidden and light scatters | Docs example: 0 shows the background clearly, 0.391 conceals distant trees. The official campfire scene uses 0.272 |
| `Offset` | How light transmits between camera and sky. Raise it for a horizon silhouette against the sky | Too low can cause "ghosting" of the skybox; too high can reveal level-of-detail popping on far objects. Balance with Density |
| `Haze` | Haziness above the horizon and in the distance | Combine with Color for moods (smoky tint, foggy blue). Campfire scene uses 1 |
| `Color` | Hue of the atmosphere | Set it close to the average color of your environment. Campfire scene uses 85,78,54 |
| `Glare` | Glow around the sun | Only visible when Haze > 0 |
| `Decay` | Hue of the atmosphere **away from** the sun, fading from Color toward this value | Only visible when Haze and Glare are both > 0. Docs example: 255,90,80 gives a warm sunset falloff |

Important: Atmosphere takes most of its colors from the **skybox**, so choose the sky first ([[Sky and Clouds]]). Atmosphere replaces the old `Fog*` properties on Lighting.

## Visual references (official Roblox docs images)
Each image shows the property at the value in the caption. The paired comparison images (for example Offset 1, Decay 255/90/80) are on the [official page](https://create.roblox.com/docs/en-us/environment/atmosphere).

![Density = 0](https://prod.docsiteassets.roblox.com/assets/lighting-and-effects/atmosphere/Density-A.jpg)
![Offset = 0](https://prod.docsiteassets.roblox.com/assets/lighting-and-effects/atmosphere/Offset-A.jpg)
![Haze = 1](https://prod.docsiteassets.roblox.com/assets/lighting-and-effects/atmosphere/Haze-A.jpg)
![Color = 255,255,255](https://prod.docsiteassets.roblox.com/assets/lighting-and-effects/atmosphere/Color-A.jpg)
![Glare = 0](https://prod.docsiteassets.roblox.com/assets/lighting-and-effects/atmosphere/Glare-A.jpg)
![Decay = 255,255,255](https://prod.docsiteassets.roblox.com/assets/lighting-and-effects/atmosphere/Decay-A.jpg)

(These are hotlinked and show when you are online. Drop your own Studio screenshots into `Assets/` and embed them with `![[name.png]]` as you build your own looks.)

## Mood cheat sheet (directional, tune by eye)
- Smoky / polluted / alien: raise Haze, tint Color.
- Foggy and somber: raise Density and Haze, cool or gray Color.
- Clear and crisp: low Density, low Haze.
- Sunset: raise Haze and Glare, warm Decay.
