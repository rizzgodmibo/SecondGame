---
title: Sky Island Hub and Throw Lane
date: 2026-10-03
tags: [roblox, map, lighting, art]
project: Paper Plane Toss
---
# Sky Island Hub and Throw Lane

## Hub (`Workspace.Island`)
- Built from Blender (`art/make_island.py`) and uploaded as about 20 GLBs. Holden asked for it **smaller**: 164 × 132 studs, down from 240 × 190.
- Checkered spawn plaza with a paper-plane statue, a checkered back wall, a post-and-rail fence and gold lamps: Stone Skipping and Steal an Egg touches.
- 12 plane pedestals in an arc, chunky library trees, vines under the rim.
- Gameplay anchors (TrainingPad, PlanePedestals, Coach, Leaderboards, LaunchPoint) **kept their names** and were moved, so no code changed.

![[Render Island Three Quarter.png|400]] ![[Render Island Top.png|300]]

## Throw lane (`Workspace.Lane.Art`)
- A 3,100-stud cloud road with distance posts every 100 m and rainbow arches every 500 m.
- 5 zones; the names are DRAFT: Cloud Meadow, Sunset Skies, Candy Clouds, Starry Heights, Golden Heavens.
- **The sky changes per zone during your own flight** (client `LaneSky`; time of day only moves forward). This was Holden's top priority.

![[Render Lane Zones.png|450]]
![[Render Lane Sunset.png|200]] ![[Render Lane Candy.png|200]] ![[Render Lane Starry.png|200]] ![[Render Lane Golden.png|200]]

## Problems solved
- **Spawning into the void:**
  - Made the island `ModelStreamingMode = Persistent` and the spawn pad solid.
  - Added a server no-ground check on spawn.
  - The likely real cause was **Play Here** spawning at an editor camera left off the island.
- Greybox floor parts caused floating and showed through the plank gaps. Parked in `ServerStorage.Greybox`, since MCP deletion is blocked.
- **Fall respawn** below y = −40 puts the player back on the plaza.
- **Hub lighting:** first default-ish, then a pastel skybox plus a cloud sea, then "way too bright". Fixed by lowering exposure, bloom and haze.
- Blender glTF imports use quaternion rotation, so set `rotation_mode = "XYZ"` before changing yaw.
- `Workspace.Lobby` was a plain folder and could stream out. It's now a Persistent model.

## Holden's bug screenshots
| Greybox floor | Spawn in void | Too bright |
|---|---|---|
| ![[Bug Greybox Floor Under Launch Deck.png\|250]] | ![[Bug Spawn in Void.png\|250]] | ![[Hub Too Bright.webp\|250]] |

Related: [[Paper Plane Toss]], [[Blender to Roblox Asset Pipeline]], [[Roblox Studio MCP Quirks]]
