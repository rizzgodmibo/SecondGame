---
title: Rojo Workflow Gotchas
date: 2026-10-03
tags: [roblox, rojo, tooling]
---
# Rojo Workflow Gotchas

- **Tools** come from Rokit in `~/.rokit/bin` (Rojo 7.7.0, Wally, Selene, StyLua). Run Rojo **from the project folder**, because Rokit needs the manifest.
- **Studio needs** the Rojo plugin's Script Injection permission turned on.
- **Scripts:** edit them only in `src/`, because Rojo overwrites synced scripts. Maps, models and UI built in Studio live only in the place file, so **save the place**.
- **Changes to `default.project.json`** (for example adding `ServerPackages`) need a `rojo serve` restart, and the plugin then needs Connect again.
- **A background `rojo serve`** started by Claude dies at the background task limit (30 min to 2 h) and when the session ends.
- **A server left running for another project** will offer to sync the wrong game into Studio. Dismiss it.
- **Fallback when nobody can click Connect:**
  1. `rojo build` to an `.rbxm`
  2. Copy it into Studio's `Versions/<ver>/content`
  3. Load it with `game:GetObjects("rbxasset://...")`
- **Line endings:** add a `.gitattributes` with `* text=auto eol=lf`, or StyLua's check fails after git converts files to CRLF.
- **Python and Node aren't in Git Bash** on this PC, so edit JSON with the Edit tool.

Related: [[Roblox Studio MCP Quirks]], [[MyGame]]
