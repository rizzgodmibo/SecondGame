---
title: Roblox Studio MCP Quirks
date: 2026-10-03
tags: [roblox, mcp, studio, debugging]
---
# Roblox Studio MCP Quirks

Collected across [[Fish a Monster]] and [[Paper Plane Toss]]. The connection uses Studio's built-in server: `cmd.exe /c %LOCALAPPDATA%\Roblox\mcp.bat`, registered as `Roblox_Studio` in `.mcp.json`.

- **Deletions are blocked** by Claude Code's safety check even when Holden gives permission. List the exact instances for him to delete in Explorer, or park them in `ServerStorage`.
- **`execute_luau` is sandboxed:** `_G` is nil, it can't FireServer or reparent into PlayerGui, and it later blocked `require` too. Test through [[Studio Only Dev Test Scripts]] instead.
- It **caches required modules** separately from the running game, so require a `Shared:Clone()` to see fresh code. Command-bar requires load a *separate copy* of a module.
- Calls time out after about 60 s, so split long tests.
- **Screenshots** sometimes come back pure white when the window is minimized or covered. The UI still captures in play mode. When they fail, verify with raycasts and ask Holden to look.
- It resets a Scriptable camera, so the in-game follow camera never shows in screenshots.
- **Studio ids change every launch;** call `list_roblox_studios`.
- If Claude stops a playtest, Holden's own testing is interrupted (and the reverse). Ask before touching Studio when he might be in it.
- **Play Here** spawns at the editor camera. A camera left off the map looks like a spawn bug.
- After restoring a test save, wait about 8 s before stopping play, or ProfileStore never writes it.

Related: [[Rojo Workflow Gotchas]], [[Blender to Roblox Asset Pipeline]]

**Play-mode screenshots disputed (2026-10-04):** a SyphoDev tutorial claims Studio MCP screenshots only work in edit mode, so the output log is the only thing that comes out of a running game. That creator falls back to an unnamed third-party Roblox MCP when the built-in one breaks. This conflicts with the play-mode observation above. ⚠️ Re-test on the current Studio build. See [[Video-SyphoDev-Claude-Code-Roblox-Workflow]].
**Don't use the Blender MCP's Hunyuan3D tools for Holden's games:** the Hunyuan3D licence excludes the UK (verified 2026-10-04).

**Update 2026-10-04 (Edit mode):** `require` via `execute_luau` **worked** in Edit mode (the "blocked require" above may be play-mode-only or fixed since). But `require` **caches across MCP calls**: after Rojo syncs a change you still get the old module. Require a fresh clone instead (`mod:Clone()`, parent it, `require` the clone). Particles also simulate in Edit mode, and `TimeScale = 0` freezes them for `screen_capture` ([[Roblox VFX Review Skill]]).
