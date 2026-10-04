---
title: Fish a Monster Island v3 Design
date: 2026-10-02
tags: [roblox, game-design, map]
project: Fish a Monster
---
# Fish a Monster Island v3 Design

Holden drew the starter island from an aerial view (`docs/starter-island-sketch.png`). His decisions are tagged `[YOU, Oct 2]` in the project's CLAUDE.md.

![[Starter Island Sketch.png|600]]

- **Story hook:** the player shipwrecks on a fishing island. This is a starter cinematic for later.
- **Size:** about 1000 × 650 studs. Spawn on Dock 1 (east), hub on Beach 1.
- **Areas:** Dock 1, Beach 1, Forest 1, Lake, Rivers, Mountain with waterfall, Cave, Northeast forest (in-between, maybe a quest NPC), Ravine, Forest 2, Beach 2. Each area has its own catches.
- **Difficulty:** no locked areas. Higher areas have a much harder reel and need better gear. Forests have tame beasts; deeper areas like the cave have wilder fantasy monsters.
- **Shops:** the main three on Beach 1, a secret blacksmith in the cave, and a late-game shop on Beach 2.
- **Later:** player levels, quests across the island, more islands, bridges over the ravine.
- **Look:** parts and meshes, not Terrain. That changed in v4 to Terrain water for swimming and waves. Holden liked the flat low-poly palm style best.

First Blender layout, built from the sketch:

![[Render v3 Layout Top.png|450]]

**Open code work when it was parked:** a server-side area lookup for per-area catch tables, which also closes review item #9.

Related: [[Fish a Monster Map Iterations]], [[Fish a Monster Catch and Reel Design]]
