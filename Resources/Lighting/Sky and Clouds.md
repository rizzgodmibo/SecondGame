---
title: Sky and Clouds
date: 2026-10-05
type: research
status: done
area: world
game: none
source: claude
tags: [roblox, lighting, sky, skybox, clouds, reference]
---

# Sky and Clouds
Back to [[Lighting Overview]]. Atmosphere colors come from the sky, see [[Atmosphere]].

## Sky object (inside Lighting)
A skybox is a cube of six images that forms the background. The Sky object also draws the sun, moon, and stars, which rise and set with `ClockTime`.

| Property | Meaning |
|---|---|
| `SkyboxBk / Dn / Ft / Lf / Rt / Up` | Back, down, front, left, right, up images. Import your images to Roblox first, then use their asset IDs |
| `SunAngularSize` | Sun size in degrees (default 21) |
| `MoonAngularSize` | Moon size in degrees |
| `StarCount` | Number of stars (default 3000) |
| `CelestialBodiesShown` | Turn off to remove sun, moon, and stars together |
| `SkyboxOrientation` | Rotates only the six skybox faces, not the sun/moon. Cheap and works on all platforms, tween it for a slowly turning sky |

To hide only the sun or moon but keep stars, set `SunAngularSize` or `MoonAngularSize` to 0.
The Sky can also act as a reflection cubemap in ViewportFrames (only the six face properties are used there).

## Choosing or making a skybox (official guidance)
- The **lower half** should be close to your terrain color so reflections off objects roughly match the ground.
- The lower half should be **darker** than the upper half. This mimics light being blocked from below and makes reflections on metal look natural. An evenly bright skybox makes a chrome sphere look like it is not reflecting the world.
- A skybox does not need clouds. Use dynamic clouds instead and let them supplement the sky.
- Older Roblox docs mentioned 256x256 as a recommended face size. Current docs do not state a size, so test what looks sharp enough for you.

## Clouds object (must be under Terrain)
`Clouds` only render when parented under **Terrain** (Explorer: hover Terrain, click +, insert Clouds). They are realistic clouds that drift slowly, and global wind sets their motion. Turning off `CelestialBodiesShown` does not remove them.

| Property | Range / meaning |
|---|---|
| `Cover` | 0 = sparse, 1 = full cover |
| `Density` | Thickness/transparency of the cloud particles. Low = light and translucent, high = heavy, dark, stormy |
| `Color` | Material color of the cloud particles |
| `Enabled` | Toggle, useful if you keep several Clouds objects and swap them |

Clouds are also tinted by Lighting and Atmosphere settings, so `Color` alone will not give you a perfect sunset. Adjust the Atmosphere and ambient colors too.

## Visual references (official Roblox docs images)
![Cover = 0.65](https://prod.docsiteassets.roblox.com/assets/lighting-and-effects/clouds/Cover-A.jpg)
![Density = 0.05](https://prod.docsiteassets.roblox.com/assets/lighting-and-effects/clouds/Density-A.jpg)
![Color = 255,255,255](https://prod.docsiteassets.roblox.com/assets/lighting-and-effects/clouds/Color-A.jpg)

Comparison values from the docs: Cover 0.8, Density 0.4, and Color 75,50,255 (a purple, alien-looking sky). See the [official clouds page](https://create.roblox.com/docs/en-us/environment/clouds) for the paired images.

## Ideas
- Stormy: Cover 0.8 or higher, Density 0.4 or higher, plus grayer Atmosphere and lower Brightness.
- Fair weather: Cover around 0.4 to 0.65 with low Density (starting points, tune by eye).
- Animate Cover/Density with TweenService for weather changes (see [[Lighting Recipes]]).
- Community caption seen on TikTok: a "dynamic skybox" built from giant models that follow the camera, plus a pre-rendered skybox kept for reflections. Interesting but unverified, see [[Lighting Sources and Videos]].
