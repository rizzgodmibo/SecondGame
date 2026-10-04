---
title: Roblox Game Development Research
date: 2026-10-03
tags: [roblox, game-development, maps, models, vfx, ui, audio]
source: codex
project: null
---
# Roblox Game Development Research

## Summary

Prove the playable layout first, establish a consistent asset style, then combine readable UI, restrained VFX, and purposeful sound. Test on mobile throughout development. Holden's existing Blender pipeline and clean low-poly direction provide the starting point. Recommendations here are research synthesis, not approval to add mechanics or change project plans.

## Key findings

- **Map building:** Recommended workflow: greybox routes, sightlines, camera clearance, and interaction spacing before final art. Roblox Terrain uses 4-stud voxels and supports sculpting and heightmap imports. For Holden's preferred crisp zone borders and stylized silhouettes, use Blender-built environments and reusable props, with Terrain where useful, such as water. This is a style recommendation, not an engine requirement. See [[Art Direction Feedback]] and [[Fish a Monster Map Iterations]]. [Terrain](https://create.roblox.com/docs/building-and-visuals/studio-modeling/terrain)

- **Streaming:** Instance streaming loads and unloads world content to reduce memory pressure and improve joining. Client scripts must tolerate objects disappearing; test distant cameras and fast movement. Avoid making every model persistent just to hide streaming bugs. [Streaming](https://create.roblox.com/docs/workspace/streaming)

- **Models:** Build a reusable kit in Blender and inspect scale, pivot, forward axis, normals, textures, and collision after import. The current Importer exposes transform, pivot, double-sided, and Ignore Vertex Colors settings. Existing notes about 180-degree rotation and dark vertex colors describe this project's pipeline experience, not unavoidable behavior for every import. Follow [[Blender to Roblox Asset Pipeline]] and preview assets before upload. See [[Game Dev Resource Sites]] for sourcing. [Importer](https://create.roblox.com/docs/studio/importer)

- **Lighting:** Establish lighting with the first finished environment sample so colors are judged in-game. Roblox provides global lighting, atmosphere, and post-processing controls. Suggested art target: readable silhouettes and interaction areas, with restrained bloom; avoid the washed-out lighting rejected in [[Art Direction Feedback]]. [Lighting](https://create.roblox.com/docs/environment/lighting)

- **VFX:** Use ParticleEmitter for bursts and sparks, Trails for moving objects, and Beams for effects spanning attachments. Use `Emit()` for discrete bursts. GPU cost depends on screen coverage and overlapping transparency as well as particle count. Reduce oversized overlapping sprites and long lifetimes before adding more particles. Test several simultaneous effects on mobile. [Effects](https://create.roblox.com/docs/effects), [Particles](https://create.roblox.com/docs/effects/particle-emitters)

- **UI:** Design for phone readability and touch reach while preserving PC interaction. Keep important controls clear of Roblox's mobile control zones. Use automatic sizing and size, text, and aspect constraints for different screens and longer labels. Holden's illustrated UI direction can use these layout tools underneath; keep text live and readable. Test narrow screens rather than relying only on scaling a desktop canvas. See [[Paper Plane Toss UI Redesign]]. [Positioning](https://create.roblox.com/docs/ui/position-and-size), [Sizing](https://create.roblox.com/docs/ui/size-modifiers)

- **SFX and music:** Use positional audio for world sounds and non-positional audio for UI and background music. Current guidance covers AudioPlayer, AudioEmitter, and connected audio objects; the older Sound workflow also remains documented. Use Creator Store sounds or properly licensed files, and grant the experience permission to private uploads. Suggested mix: separate music and effects controls, short action cues, restrained repetition, and visual equivalents for essential audio feedback. See [[Game Dev Resource Sites]]. [Audio](https://create.roblox.com/docs/audio), [Audio assets](https://create.roblox.com/docs/audio/assets)

- **Performance:** Reuse mesh and texture assets, limit unnecessary shadows, and inspect texture memory, collision complexity, and transparent effects. Profile representative gameplay on an actual target phone; desktop Studio performance alone does not establish mobile performance. Avoid arbitrary universal triangle budgets: the whole scene and device matter. [Performance](https://create.roblox.com/docs/performance-optimization/improve)

- **Testing and gameplay integration:** Studio supports device and multi-client simulation. Test UI, crowded scenes, and effects together. Keep cosmetic presentation separate from authoritative rewards: validate and rate-limit client requests on the server, including requests that broadcast effects. An animation finishing is not proof a reward was earned. See [[Studio Only Dev Test Scripts]], [[Roblox Studio MCP Quirks]], and [[Deterministic Flight Sim and Ghosts]]. [Testing](https://create.roblox.com/docs/studio/testing-modes), [Security](https://create.roblox.com/docs/scripting/security/client-server-boundary)

## Suggested production order

Greybox and playtest → finish one small area with representative models and lighting → build reusable assets → add UI, VFX, and sound → test the combined scene on mobile and multiple clients → expand content. This is a recommendation, not a change to any project's roadmap.

## Sources

Official Roblox documentation, checked 2026-10-03:

- [Environmental terrain](https://create.roblox.com/docs/building-and-visuals/studio-modeling/terrain)
- [Instance streaming](https://create.roblox.com/docs/workspace/streaming)
- [Importer](https://create.roblox.com/docs/studio/importer)
- [Global lighting](https://create.roblox.com/docs/environment/lighting)
- [Effects overview](https://create.roblox.com/docs/effects)
- [Particle emitters](https://create.roblox.com/docs/effects/particle-emitters)
- [Position and size UI objects](https://create.roblox.com/docs/ui/position-and-size)
- [Size modifiers and constraints](https://create.roblox.com/docs/ui/size-modifiers)
- [Audio overview](https://create.roblox.com/docs/audio)
- [Audio assets and permissions](https://create.roblox.com/docs/audio/assets)
- [Improve performance](https://create.roblox.com/docs/performance-optimization/improve)
- [Studio testing modes](https://create.roblox.com/docs/studio/testing-modes)
- [Securing the client-server boundary](https://create.roblox.com/docs/scripting/security/client-server-boundary)

Local context: [[Art Direction Feedback]], [[Blender to Roblox Asset Pipeline]], [[Fish a Monster Map Iterations]], [[Paper Plane Toss UI Redesign]], and `C:\Users\holde\Documents\GameDev\AssetLibrary\README.md`. Local preferences are distinguished above from platform guidance.
