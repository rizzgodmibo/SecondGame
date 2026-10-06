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

**Update 2026-10-05 (Trap Your Friends style test, Team Create place):**
- **`screen_capture` writes every image to disk** under `~/.claude/projects/<project>/<session>/tool-results/mcp-Roblox_Studio-blob-*.jpg` (the path is printed under the image). Copy those files into the vault instead of re-capturing.
- **Play mode: the camera parameters lose to the follow camera.** The first capture used the requested view; later ones snapped back behind the avatar. Fix: run Client `execute_luau` with `CurrentCamera.CameraType = Scriptable` and set `CFrame`, then call `screen_capture` **with no camera parameters**.
- **Freezing effects for screenshots:** a Studio-only client listener on a workspace attribute (e.g. `TYF_FreezeDebris`) anchors live client debris and pauses its tweens. A Server `execute_luau` can set the attribute a measured time after triggering the effect.
- `upload_image` takes **http URLs**, not file paths. Serving the folder with a local `python -m http.server` on 127.0.0.1 worked. Results map URL → `rbxassetid://`.
- `MaterialVariant.Pattern` is not a valid member in this Studio build (set `MaterialPattern` inside a pcall instead).
- Rojo + Team Create: syncing worked once Holden clicked Connect (the plugin needs a click for a new place; the MCP can't click it).

**Update 2026-10-06 (Trap Your Friends style test v2):**
- **`execute_luau` on the Client datamodel CAN `FireServer` now** (it worked with plain and junk arguments). That made a real remote security test possible from the MCP. The older "it can't FireServer" note is out of date for this Studio build.
- **`screen_capture` resets a Scriptable camera to Custom before it grabs the frame**, so setting the camera once isn't enough. Fix: `RunService:BindToRenderStep("ShotCam", Enum.RenderPriority.Camera.Value + 10, ...)`, which re-applies `CameraType = Scriptable` + `CFrame` from a workspace attribute every frame; then capture with no camera parameters. Unbind afterwards.
- **Studio throttles to 15 fps (66.7 ms) when it isn't the foreground window.** Frame numbers taken then are worthless. Bring Studio forward (`SetForegroundWindow`, with the Add-Type and the call in **one** PowerShell call, because types don't persist between calls) and drop throttled samples.
- Studio session ids change when Holden reopens the place (call `list_roblox_studios` again). An old `rojo serve` from an earlier Claude session can still be running and holding port 34872. Check before starting another.
- Cloned-module requires: clone the **whole folder** of a builder (sibling `require(script.Parent.X)` would otherwise hit cached originals).
- **Test graphics quality from the MCP (2026-10-06):** a Client `execute_luau` can set `settings().Rendering.QualityLevel = Enum.QualityLevel.Level01` … `Level21` (and back to `Automatic`) during a play test. Combine it with red marker parts at set distances to see the draw distance per level. Studio's own "Automatic" level culled objects past ~600 studs on Holden's PC. Remember to set it back to `Automatic`.
