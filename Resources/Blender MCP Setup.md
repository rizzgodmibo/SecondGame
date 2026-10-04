---
title: Blender MCP Setup
date: 2026-10-02
tags: [blender, mcp, setup, windows]
---
# Blender MCP Setup

Set up on 2026-10-02 for [[Fish a Monster]] and reused for [[Paper Plane Toss]].

- **Project:** "MCP for Blender" (github.com/ahujasid/mcp-for-blender, PyPI `mcp-for-blender`, MIT). It's not the older `blender-mcp` package name.
- **Runner:** `uvx` from winget. **uv's own Python is broken on this PC** ("Missing expected target directory for Python minor version link"), so the server runs on **Blender's bundled Python** with `--no-python-downloads`.
- **Settings:** `DISABLE_TELEMETRY=true` and `BLENDER_MCP_SAFE_MODE=1`. Safe mode only allows bpy, bmesh and mathutils, with no lambdas or functions passed around, so scripts use plain mode names.
- **In Blender:** enable "Interface: MCP for Blender", then **Start MCP Server** in the N panel (port 9876). Poly Haven, Poly Pizza and Sketchfab sources are toggled there.
- **Registration:** per project, in a gitignored `.mcp.json`. New servers only load in a **new** Claude session.
- The add-on's Poly Pizza download command didn't work, so models are downloaded directly and imported.
- **No MCP loaded?** Headless `blender --background --python` works fine.
- **Vault registration (2026-10-04).** It is now also in `C:\Vault\.mcp.json` (gitignored) alongside `Roblox_Studio`. Checked live: add-on 1.8, protocol 13 (up to date), Blender 5.2.2 LTS, telemetry off.
  - The first call after a restart can fail with `WinError 10053` (connection aborted). Just retry.
  - **Safe mode limits (verified):**
    - Allowed: `bpy`, `bmesh`, `mathutils`, pure-Python stdlib, and render/save/import/export operators.
    - Blocked: numpy, `open`/`os`, and loading external `.blend` datablocks.
  - Numpy-heavy builds such as `Assets/FantasyCreatures/build_creatures.py` therefore stay headless. Use the MCP to view or tweak the live scene, e.g. importing the exported OBJs. See [[Fantasy-Creatures-Set]].

Related: [[Blender to Roblox Asset Pipeline]], [[Third Party Claude Tools Evaluated]]
