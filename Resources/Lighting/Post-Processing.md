---
title: Post-Processing
date: 2026-10-05
type: research
status: done
area: world
game: none
source: claude
tags: [roblox, lighting, bloom, colorcorrection, postprocessing, reference]
---

# Post-Processing
Screen filters applied after the scene is rendered. Back to [[Lighting Overview]].

## Where to put them
- Inside **Lighting**: everyone in the experience sees it. Use for the global look (sun rays, color grade).
- Inside **Camera**: only that one player sees it. Use for reactive effects, such as blur behind a menu or a red tint at low health.
- If an effect does not show in Studio, set File > Studio Settings > Rendering > Editor Quality Level to the highest level.

## The effects
| Effect | What it does | Key properties |
|---|---|---|
| `BloomEffect` | Bright things glow, like a camera looking at a bright light | Intensity, Size, Threshold |
| `BlurEffect` | Gaussian blur over the whole 3D view | Size |
| `ColorCorrectionEffect` | Overall mood and feedback | Brightness, Contrast, Saturation, TintColor |
| `DepthOfFieldEffect` | Blurs what is out of focus, for distance blur or focusing on an item | focus distance and blur settings |
| `SunRaysEffect` | Halo and rays around the sun, shaped by objects in front of it | Intensity, Spread |
| `ColorGradingEffect` | Changes how the renderer maps colors to the screen. `TonemapperPreset`: Default (vivid, high contrast) or Retro (pre-2019 look: less saturated, less contrast) | TonemapperPreset |

For a full pre-2019 look, the docs suggest the Retro preset plus all light brightness at a maximum of 1.

## Practical advice
- Official: use ColorCorrection to set mood and for player feedback.
- Community (DevForum): raise contrast and saturation only a little (about 0.1 to 0.2); the most common mistake is overusing depth of field, saturation, and bloom.
- Community (DevForum): ambient colors should be similar to the sky color.
- A creation.dev write-up of a ToastDevRBLX video suggests bloom size around 20 to 30 with a threshold of about 1.5 to 2 for realistic scenes. This is secondhand and unverified, treat it as a starting point.
- Sun rays look best when something (a tree line, a building) sits between the camera and the sun.

## Apply order
Do this last in the [[Lighting Overview]] workflow. If a scene looks bad, fix light and atmosphere first; filters cannot rescue bad lighting.
