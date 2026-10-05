---
title: Lighting Sources and Videos
date: 2026-10-05
type: research
status: done
area: world
game: none
source: claude
tags: [roblox, lighting, sources, tiktok, youtube, devforum]
---

# Lighting Sources and Videos
Researched 2026-10-05. Back to [[Lighting Overview]].

## Official Roblox docs (most reliable, checked directly)
- [Lighting and effects overview](https://create.roblox.com/docs/en-us/environment)
- [Lighting class reference](https://create.roblox.com/docs/en-us/reference/engine/classes/Lighting.md)
- [Technology enum](https://create.roblox.com/docs/en-us/reference/engine/enums/Technology.md)
- [Atmospheric effects](https://create.roblox.com/docs/en-us/environment/atmosphere)
- [Dynamic clouds](https://create.roblox.com/docs/en-us/environment/clouds)
- [Skybox](https://create.roblox.com/docs/en-us/environment/skybox)
- [Post-processing effects](https://create.roblox.com/docs/en-us/environment/post-processing-effects)
- [Tutorial: Enhance outdoor environments with realistic lighting](https://create.roblox.com/docs/en-us/tutorials/use-case-tutorials/lighting/enhance-outdoor-environments)
- Practice places: [Lighting Outdoors - Start](https://www.roblox.com/games/17835285085/Lighting-Outdoors-Start) and [Complete](https://www.roblox.com/games/17835194683/Lighting-Outdoors-Complete)

## DevForum (community, mixed age)
- [Guide to Lighting](https://devforum.roblox.com/t/guide-to-lighting/2764787): plain-English property rundown
- [Tips on realistic lighting](https://devforum.roblox.com/t/tips-on-realistic-lighting/1261456): contrast/saturation tweaks, warm ColorShift_Top, warning about overusing bloom/DoF/saturation
- [How to make realistic lighting](https://devforum.roblox.com/t/how-to-make-realistic-lighting/1593494): Future, skybox importance, water/reflection tips
- [Realistic Roblox Lighting](https://devforum.roblox.com/t/realistic-roblox-lighting/3144291): includes a downloadable `.rbxm`. **Do not insert downloaded models blindly**; inspect scripts first (I did not scan it)
- [Future is Bright Phase 3](https://devforum.roblox.com/t/future-is-bright-phase-3-released/878634): Roblox staff on light shadow cost
- [Mobile performance article](https://devforum.roblox.com/t/3127146): what lower quality levels remove

## Secondary write-ups
- [creation.dev: realistic lighting guide](https://www.creation.dev/learn/how-to-make-realistic-lighting-roblox-studio): summarizes a **ToastDevRBLX** YouTube tutorial (fake volumetric light with semi-transparent parts, warm indoor lights, bloom values). I did not watch the video and the page is a summary, so treat numbers as hints.

## Video platforms: what I could and could not get
- **YouTube:** the search tool could not return video pages or transcripts. Useful search terms to try yourself: `Roblox Studio realistic lighting Atmosphere ColorCorrection tutorial`, `Roblox Studio skybox clouds tutorial`, `Roblox LightingStyle Realistic`, and the creator name ToastDevRBLX. DevForum posts mention these videos but I did not watch them: [volumetric clouds demo](https://www.youtube.com/watch?v=C_k3Awr6w9E) (2016-era, per a DevForum comment) and [old Future is Bright builds demo](https://www.youtube.com/watch?v=vLHh3d2x6Gc).
- **TikTok:** only captions and titles were visible, not the video content. Captions found (verify before trusting):
  - @nobel.courses: [changing the sky using Toolbox skies or a custom Sky](https://www.tiktok.com/@nobel.courses/video/7581944681462762774)
  - @punto_code: automatic day/night cycle using Lighting and ClockTime ([topic page](https://www.tiktok.com/discover/how-to-change-the-time-the-sky-changes-in-roblox-studio))
  - @_pizzalemon_: horror ambience using lighting, skybox, and sound ([topic page](https://www.tiktok.com/discover/how-to-set-the-lighting-in-a-room-in-roblox-studios))
  - @mysticdevex: lighting setup for a simulator game (same topic page)
  - @martin.tutoriales: a step-by-step light setup for a popular "Volviiiiii"-style look ([topic page](https://www.tiktok.com/discover/what-to-make-in-the-roblox-game-studio-light))
  - @ntoahlcrei12: dynamic skybox from giant models that follow the camera, vertex-colored dome, plus a pre-rendered skybox for reflections ([topic page](https://www.tiktok.com/discover/tutorial-how-to-make-a-skybox-roblox))
- **X (Twitter):** searches returned nothing useful. Follow Roblox developers' showcase threads manually and save screenshots into `Assets/`.

## Things to ignore or double-check
- Any advice saying "set Technology to Future" or "set ShadowMap to Voxel" is **older** than the current LightingStyle system. Check [[Lighting Service Properties]].
- A guide I found claimed Atmosphere `Decay` should be between 0.8 and 1.0. That is wrong: `Decay` is a color, not a number. Official docs in [[Atmosphere]] are correct.
- Several SEO-style pages (random domains repeating "roblox lighting" text) had no real info. I skipped them.
- Moon phase cannot be changed (always 0.75), despite some pages implying otherwise.

## Keep your own references here
When you find a lighting look you like, save a screenshot to `Assets/` and add a note with the settings. Suggested frontmatter for those notes: `type: design`, `area: world`, and the game name.
