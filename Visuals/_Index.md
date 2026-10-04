---
tags: [visuals/index]
status: draft
updated: 2026-10-04
confidence: high
---
# Visuals — Index

UI, VFX, animation, 3D pipeline, lighting, audio and art direction. Facts verified on 2026-10-04 against the Roblox creator-docs source (2026-10-02 commit); open questions carry `⚠️ verify:` markers inside each note.

## TL;DR
- Start with [[Art-Direction]] (style the team can sustain, readable at thumbnail size), then [[UI-Architecture]] + [[UI-Layout-And-Device-Scaling]] (mobile-first).
- Polish pass = [[UI-Polish-And-Juice]] + [[VFX-Particles-Beams-Trails]] + [[Sound-Design]] — every action gets motion + particles + sound.
- 3D content goes through [[Blender-To-Roblox-Pipeline]] and [[Asset-Creation-Workflow-And-Marketplace]] (group ownership, audits, budgets).
- There are no custom shaders: see [[Shaders-Materials-And-Surfaces]]; lighting moved to `LightingStyle` + `PrioritizeLightingQuality` — see [[Lighting-And-Atmosphere]].

## Notes

| Note | One-line summary |
|---|---|
| [[UI-Architecture]] | ScreenGui layering (DisplayOrder, ResetOnSpawn=false, ZIndexBehavior=Sibling, ScreenInsets), state-driven UI (React-lua / Fusion / Vide / minimal Value helper), router & component patterns, UI Styling tokens |
| [[UI-Layout-And-Device-Scaling]] | Scale vs Offset, aspect constraints, UIScale controller, list/flex/grid layouts, safe areas & thumb zones, touch target sizes, gamepad selection, text scaling & accessibility |
| [[Roblox UI Checker Skill]] | Claude Code skill: automated UI checks at 4 screen sizes (touch size, overlap, off-screen, centring, text size, stray boxes, outline mix) |
| [[Roblox VFX Review Skill]] | Claude Code skill: VFX budget lint + phase-freeze screenshots (start/middle/end), building blocks from Holden's pack, recipes |
| [[Roblox Asset Pipeline Skill]] | Claude Code skill: Blender preflight (tri limits, vertex colours, transforms, origin, normals, textures, UVs, colour variation) + previews before Open Cloud upload |
| [[Roblox Sound Library Skill]] | Claude Code skill: soundcheck (lead silence, clipping, limits), tagged catalogue of approved ids, upload quota, calibrated volumes, layered SoundPlayer |
| [[UI-Polish-And-Juice]] | Tween easing presets, reusable ButtonJuice module, count-up numbers, reward popup recipe, trauma screen shake, FOV kick, UIStroke/UIGradient/UICorner styling |
| [[VFX-Particles-Beams-Trails]] | ParticleEmitter properties & recipes, Emit() bursts on the client, flipbooks, Beams, Trails, Attachments, limits (400/s, 100/s mobile, 20 s lifetime, 255 Highlights) |
| [[Shaders-Materials-And-Surfaces]] | Substitutes for shaders: MaterialVariant, SurfaceAppearance PBR + emissive, Highlight, Neon/Glass/ForceField, scrolling textures, ViewportFrames, EditableImage/EditableMesh |
| [[Animation-Rigging-And-IK]] | R15 vs R6, Animator & track caching, priorities/weights, replication & ownership, markers, Animation Graph Editor, IKControl, springs, custom Motor6D/Bone rigs |
| [[Blender-To-Roblox-Pipeline]] | Units/axis/FBX/glTF export settings, 20k-tri mesh cap & budgets, UVs, texture sizes, PBR maps, Importer settings, Collision/RenderFidelity, SLIM LOD, skinning, cages |
| [[Lighting-And-Atmosphere]] | LightingStyle/PrioritizeLightingQuality (replacing Technology), Atmosphere/Sky/Clouds, post-processing, genre presets, mobile cost, day/night |
| [[Sound-Design]] | Legacy Sound/SoundGroup vs audio API (AudioPlayer/Wire/AudioFader/Emitter/Listener), bus mixer code, rolloff, UI sound map, licensing & upload limits, loudness normalisation |
| [[Art-Direction]] | Choosing a sustainable style, readability at small sizes, palettes & rarity colours, style guide template, genre expectations, art → thumbnails |
| [[Asset-Creation-Workflow-And-Marketplace]] | Creator Store use & limits, licensing/IP, Importer vs Asset Manager vs Open Cloud, asset privacy, packages, moderation, free-model backdoor auditing |

## Suggested order for a new game
1. [[Art-Direction]] → 2. [[UI-Architecture]] → 3. [[UI-Layout-And-Device-Scaling]] → 4. [[Blender-To-Roblox-Pipeline]] / [[Asset-Creation-Workflow-And-Marketplace]] → 5. [[Lighting-And-Atmosphere]] → 6. [[Animation-Rigging-And-IK]] → 7. [[VFX-Particles-Beams-Trails]] + [[Shaders-Materials-And-Surfaces]] → 8. [[UI-Polish-And-Juice]] + [[Sound-Design]].

## Related
- [[Home]] · [[Game-Building-Playbook]] · [[Thumbnails-And-Icons]] · [[Systems/_Index|Systems]] · [[Growth/_Index|Growth]]

## Sources
- Roblox Creator Documentation — https://create.roblox.com/docs (source: https://github.com/Roblox/creator-docs)
