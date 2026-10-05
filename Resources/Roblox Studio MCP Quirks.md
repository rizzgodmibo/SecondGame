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

**Update 2026-10-04 (Rubber Tower, Studio play mode):**
- `screen_capture` with a camera position **worked in play mode**: it captured the ragdolled avatar and the dev panel. This counts against the dispute below for this Studio build.
- `execute_luau` calls time out at about 60 s, including calls that only wait. Start long tests with `task.spawn`, write progress to a workspace attribute, and read it in a later call.
- `execute_luau` can't fire remotes, but setting a workspace attribute that a Studio-only server script listens to (`DevCommand`) drives dev tools well.
- Rojo-synced script changes only take effect after a play restart.
- Humanoid `MoveTo` called from the server **does** walk a player's own character (useful for walk-off-ledge tests). Calling it repeatedly also walks a character into a truss so it climbs, which makes it good for ladder, bounce and hatch tests.
- **Blank white `screen_capture` (Rubber Tower, 2026-10-04):** Studio was maximised but covered by other windows, so it didn't draw 3D (client FPS showed 15). Fix: bring Studio to the front first, from PowerShell with user32 `keybd_event(Alt)` + `SetForegroundWindow`. Then captures work in both edit and play mode. Calls can still time out while Studio is busy; retry.
- After `rojo serve` restarts (including after a crash), the Studio plugin reconnects **by itself in about 20–25 s**. Poll for a freshly synced instance instead of asking Holden to click Connect.
- In play mode, `require(module:Clone())` on the Server datamodel works for stateless modules (used to run MapAudit directly). Modules that hold state give a separate copy.

**Play-mode screenshots disputed (2026-10-04):** a SyphoDev tutorial claims Studio MCP screenshots only work in edit mode, so the output log is the only thing that comes out of a running game. That creator falls back to an unnamed third-party Roblox MCP when the built-in one breaks. This conflicts with the play-mode observation above. ⚠️ Re-test on the current Studio build. See [[Video-SyphoDev-Claude-Code-Roblox-Workflow]].
**Don't use the Blender MCP's Hunyuan3D tools for Holden's games:** the Hunyuan3D licence excludes the UK (verified 2026-10-04).

**Update 2026-10-04 (Edit mode):** `require` via `execute_luau` **worked** in Edit mode (the "blocked require" above may be play-mode-only or fixed since). But `require` **caches across MCP calls**: after Rojo syncs a change you still get the old module. Require a fresh clone instead (`mod:Clone()`, parent it, `require` the clone). Particles also simulate in Edit mode, and `TimeScale = 0` freezes them for `screen_capture` ([[Roblox VFX Review Skill]]).
