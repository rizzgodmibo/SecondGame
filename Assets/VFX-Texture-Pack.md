---
title: VFX Texture Pack
date: 2026-10-03
type: asset
area: other
game: none
source: me
tags: [assets/vfx, visuals/vfx, textures, particles, impact-frames]
status: draft
updated: 2026-10-03
confidence: high
---

# VFX Texture Pack

Holden's own reusable VFX texture set, added to the vault on 2026-10-03 from `vfx-vault-drop.zip`. Not tied to one game.
Image files are in `Assets/VFX/TexturePack/`. All sizes below were checked against the files when they were added.

## TL;DR
- **Contents:** 25 PNGs (all RGBA) plus 2 MP4 previews:
  - 13 particle sprites, including three 4×4 flipbooks (fire, smoke, electric)
  - 4 Beam/Trail strips
  - 2 cloud sheets
  - an anime-style "impact frame" set (backgrounds, ink overlay, word atlas)
- **Tint them in Roblox.** The sprites are greyscale or white on transparent, so set the colour with `ParticleEmitter.Color`, `Beam.Color` and so on.
- **Flipbooks:** set `FlipbookLayout = Grid4x4` and `FlipbookMode = OneShot` or `Loop`. See [[VFX-Particles-Beams-Trails]].
- **Upload before use.** Upload a PNG as an Image (Asset Manager bulk import or Creator Hub), then write its id in the tables below. Nothing is uploaded yet.
- **The MP4s are reference only.** Roblox can't play them, so use the stills in-game.

## Particle sprites
| Texture | Size | Layout | Good for | Asset ID |
|---|---|---|---|---|
| VFX_fire_flip4x4.png | 1024x1024 | 4x4 flipbook | fire, torches, burning | |
| VFX_smoke_flip4x4.png | 1024x1024 | 4x4 flipbook | smoke, dust trails | |
| VFX_electric_flip4x4.png | 1024x1024 | 4x4 flipbook | electricity, shocks | |
| VFX_smoke_puff.png | 256x256 | single | soft puffs, steam | |
| VFX_spark_dot.png | 128x128 | single | sparks, embers | |
| VFX_spark_streak.png | 64x256 | single | streaking sparks | |
| VFX_flare.png | 512x512 | single | glows, lens flare | |
| VFX_impact_burst.png | 512x512 | single | hit sparks | |
| VFX_shockwave_ring.png | 512x512 | single | shockwave rings | |
| VFX_slash_arc.png | 512x512 | single | sword slashes | |
| VFX_ground_cracks.png | 512x512 | single | ground slam decals | |
| VFX_magic_circle.png | 1024x1024 | single | spell circles | |
| VFX_noise_tile.png | 256x256 | tile | noise/distortion | |

## Strips and trails
| Texture | Size | Good for | Asset ID |
|---|---|---|---|
| VFX_energy_strip.png | 512x128 | energy beams | |
| VFX_lightning_strip.png | 512x128 | lightning beams | |
| VFX_wind_strip.png | 512x128 | wind trails | |
| VFX_trail_soft.png | 256x64 | soft Trail objects | |

## Clouds
- cloud_puff_1024.png (1024x512)
- cloud_puffs_2x2.png (1024x512), several puffs in one image

## Impact frames (`ImpactFrames/`)
- HA_bg_black_on_white.png / HA_bg_white_on_black.png (1920x1080)
- HA_bg_black_on_white_1024.png / HA_bg_white_on_black_1024.png (1024x576)
- HA_bg_ink_1024.png (1024x576, transparent ink overlay)
- HA_words_atlas.png (1024x1024, word/text atlas, white on transparent)
- HA_anim_black_on_white.mp4 / HA_anim_white_on_black.mp4 (960x540, 3 s previews)

Roblox can't play MP4 files, so those are reference previews only. Use the stills in-game, for example as a full-screen ImageLabel flash for the impact-frame thumbnail style noted in [[Icon-And-Thumbnail-Gallery]].

## Previews
![[VFX_fire_flip4x4.png]]
![[VFX_magic_circle.png]]
![[VFX_shockwave_ring.png]]

## Usage notes
- **Flipbooks:** set ParticleEmitter `FlipbookLayout` to Grid4x4 and `FlipbookMode` to OneShot or Loop.
- **Strips** suit `Beam.Texture` with `TextureMode = Wrap` or `Stretch`, and soft trails suit `Trail.Texture`.
- Link game-specific VFX systems here with [[wikilinks]] once they exist.

## Pitfalls
- **Use the Image id, not the Decal id.** Uploading as a Decal in Creator Hub gives a Decal id. `ParticleEmitter.Texture` needs the underlying Image id; Asset Manager bulk import gives that directly. ⚠️ verify the current Creator Hub upload flow.
- **The 1920x1080 impact backgrounds are larger than needed.** On mobile, prefer the 1024x576 versions.
- **The 1024² flipbooks cost the most texture memory in the pack.** Don't run all three on screen at once on low-end phones.

## Related
- [[VFX-Particles-Beams-Trails]] · [[Dragons-Hoard-Set]] (its own particle PNGs: sparkle, ember, frost flake, bubble, glow, coin glint, shine) · [[Free-Icon-Pack-v3.1-Basic]] · [[Icon-And-Thumbnail-Gallery]]

## Sources
- Holden's `vfx-vault-drop.zip` (Downloads), 2026-10-03. Original note text by Holden. Sizes were checked file by file on import.
