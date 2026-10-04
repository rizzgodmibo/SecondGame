---
tags: [resources/tooling, visuals/pipeline, meta/ai-workflow]
status: verified
updated: 2026-10-04
confidence: high
---
# Roblox Asset Pipeline Skill

A Claude Code skill (`roblox-asset-pipeline`): Holden's Blender → Open Cloud → Studio pipeline as a checked procedure, with a headless **preflight** and preview renders before anything uploads.
Built 2026-10-04 as the fifth skill from [[Video-SyphoDev-Claude-Code-Roblox-Workflow]] (its "check every model before import" rule, §7.3/§7.7), **without** the video's AI image-to-3D route.

## TL;DR
- **Where:** `C:\Users\holde\.claude\skills\roblox-asset-pipeline\`. It points at the AssetLibrary README and [[Blender to Roblox Asset Pipeline]] instead of copying them.
- **Preflight** (`scripts/preflight.py`, Blender 5.2 headless, read-only). Per mesh in the export scene, it checks:
  - FAIL: > 20k triangles, vertex colours, textures > 4096
  - WARN: > 10k triangles (prop budget, Holden's choice), textures > 1024, unapplied transforms, origin not at base, inward normals, **missing UVs on a textured mesh**, single flat colour
  - It also reports shading (flat/smooth/mixed) and renders an orthographic **preview PNG per object** for art review.
- **Uploads** still need Holden's explicit OK per batch, because they publish to his account.
- **Status: self-test PASSED 2026-10-04** (10 fixture objects, exact expected findings, 10 previews). **Not yet run on a real asset.**

## What the first run taught
- `bmesh.ops.create_cube(calc_uvs=True)` only fills an existing UV layer. The fixture cube had no UVs, and the colour check silently fell back to the material colour.
  That led to a new `uv-missing` check, because a textured mesh without UVs is broken in Roblox anyway.
- Holden's Blender MCP runs in safe mode (no lambdas, only bpy/bmesh/mathutils), so the preflight runs headless on the saved .blend.

## Related
- [[Blender to Roblox Asset Pipeline]] · [[Blender-To-Roblox-Pipeline]] · [[Art-Direction]] · [[Art Direction Feedback]] · [[Blender MCP Setup]]
- [[Roblox Map Audit Skill]] · [[Roblox VFX Review Skill]] · [[Video-SyphoDev-Claude-Code-Roblox-Workflow]]

## Sources
- SyphoDev video, 7:20–8:00 and 17:48–18:08: https://www.youtube.com/watch?v=afuKhenJldY
- Roblox mesh and texture specifications (limits verified 2026-10-04; see [[Verification-Log]]).
- Self-test output, 2026-10-04 (Blender 5.2.2 LTS).
