---
tags: [systems/tooling]
status: draft
updated: 2026-10-04
confidence: medium
---
# Tooling: Rojo, Wally, Selene, StyLua, luau-lsp and Studio MCP

## TL;DR
- Code lives in **git** as `.luau` files; **Rojo** (v7.7.1) syncs them into Studio; **Wally** (v0.3.x stable; 0.4 alpha exists) installs packages; **Rokit** (v1.2.0) pins tool versions per repo.
- Quality gates: **StyLua** (format), **Selene** (lint), **luau-lsp** (`luau-lsp analyze` type checking with a Rojo sourcemap) — all run in GitHub Actions on every push.
- The **Roblox Studio MCP server** is built into Studio (Assistant → … → Manage MCP Servers → *Enable Studio as MCP server*). Claude Code is a quick-connect client. It lets an AI read/edit scripts, explore the DataModel, run Luau, start/stop playtests, read output, capture screenshots and simulate input.
- Recommended AI loop: Claude edits files in the repo → Rojo live-syncs into Studio → Claude uses MCP `start_stop_play` + `get_console_output` + `screen_capture` to verify → fixes → commits. Never let MCP `multi_edit` and Rojo both own the same scripts (Rojo will overwrite).
- Publish only from a clean, CI-green commit (`rojo build` → place file → publish via Studio or Open Cloud Place Publishing API).

## Details

### Tool versions (latest git tags checked 2026-10-04)
| Tool | Purpose | Latest tag |
|---|---|---|
| Rojo | Filesystem ↔ Studio sync, place builds | v7.7.1 |
| Rokit | Toolchain manager (`rokit.toml`) — successor to Aftman/Foreman | v1.2.0 |
| Wally | Package manager | v0.3.2 stable (v0.4.0-alpha.0 pre-release exists) |
| Selene | Linter (roblox std) | 0.32.0 |
| StyLua | Formatter | v2.5.2 |
| luau-lsp | Language server + `analyze` CLI | 1.70.1 |
| Roblox/studio-rust-mcp-server | Standalone (older) MCP server repo | v0.2.365 — superseded for most uses by Studio's built-in server ⚠️ verify |

### `rokit.toml`
```toml
[tools]
rojo = "rojo-rbx/rojo@7.7.1"
wally = "UpliftGames/wally@0.3.2"
selene = "Kampfkarren/selene@0.32.0"
stylua = "JohnnyMorganz/StyLua@2.5.2"
luau-lsp = "JohnnyMorganz/luau-lsp@1.70.1"
wally-package-types = "JohnnyMorganz/wally-package-types@1.7.0"
```
`rokit install` then all tools are on PATH for this repo.

### `wally.toml`
```toml
[package]
name = "yourname/yourgame"
version = "0.1.0"
registry = "https://github.com/UpliftGames/wally-index"
realm = "shared"

[dependencies]
Trove = "sleitnick/trove@^1"          # 1.8.0 in RbxUtil, 2026-10-04
Signal = "sleitnick/signal@^2"        # 2.0.3
# Promise = "evaera/promise@^4"

[server-dependencies]
ProfileStore = "lm-loleris/profilestore@1.0.3"
```
`wally install` → `Packages/` (shared) and `ServerPackages/`. Gitignore both; CI runs `wally install`. Run `wally-package-types --sourcemap sourcemap.json Packages/` so luau-lsp sees package types.

### Selene / StyLua configs
`selene.toml`:
```toml
std = "roblox"
[rules]
global_usage = "deny"
unused_variable = "warn"
shadowing = "warn"
deprecated = "deny"     # catches wait/spawn/delay
```
`stylua.toml`:
```toml
column_width = 120
indent_type = "Tabs"
quote_style = "AutoPreferDouble"
call_parentheses = "Always"
```

### luau-lsp
- VS Code extension "Luau Language Server" + Rojo sourcemap (`rojo sourcemap --watch -o sourcemap.json`) gives typed `script.Parent.X` requires and instance trees.
- CI: `luau-lsp analyze --definitions:@roblox=globalTypes.d.luau --sourcemap=sourcemap.json src/`. Since recent versions, definitions files must be **named** (`--definitions:@roblox=…`); unnamed form is temporarily still accepted (luau-lsp CHANGELOG, 2026). Definitions file: `scripts/globalTypes.d.luau` in the luau-lsp repo.

### GitHub Actions CI
```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: CompeyDev/setup-rokit@v0.2.1   # tag checked 2026-10-04
      - run: rokit install --no-trust-check   # ⚠️ verify: setup-rokit may already install tools
      - run: wally install
      - run: rojo sourcemap default.project.json -o sourcemap.json
      - run: stylua --check src
      - run: selene src
      - run: |
          curl -sL -o globalTypes.d.luau https://raw.githubusercontent.com/JohnnyMorganz/luau-lsp/main/scripts/globalTypes.d.luau
          luau-lsp analyze --definitions:@roblox=globalTypes.d.luau --sourcemap=sourcemap.json --ignore="Packages/**" src
      - run: rojo build default.project.json -o build.rbxl
      - run: '! grep -rnE "^\s*(wait|spawn|delay)\(" src'
      - run: '! grep -rn "InvokeClient" src'
```
Tests: run unit tests outside Roblox with **Lune** for pure-Luau modules, or in-engine with **Jest-Lua** (Roblox's port) via Open Cloud **Luau Execution** API against a test place ⚠️ verify: Open Cloud Luau Execution API availability and quotas.

### Roblox Studio MCP server (built-in)
What it is: an MCP server that runs as a local `stdio` process connected to open Studio sessions. Enable: Studio → **Assistant** → **…** → **Manage MCP Servers** → **Enable Studio as MCP server** (green indicator shows connected clients).

Connect Claude Code: quick connect (Assistant Settings → MCP Servers → Quick connect → Claude Code), or manually:
- Windows: `claude mcp add Roblox_Studio -- cmd.exe /c %LOCALAPPDATA%\Roblox\mcp.bat`
- macOS: `claude mcp add Roblox_Studio -- /Applications/RobloxStudio.app/Contents/MacOS/StudioMCP`
(JSON config equivalents: `"command": "cmd.exe", "args": ["/c", "%LOCALAPPDATA%\\Roblox\\mcp.bat"]` on Windows; `"command": "/Applications/RobloxStudio.app/Contents/MacOS/StudioMCP"` on macOS.)

Tools exposed (docs, 2026-10-04) — every call takes a `studio_id` (get from `list_roblox_studios`):
| Group | Tools |
|---|---|
| Scripts | `script_read`, `multi_edit` (creates if missing; `datamodel_type` Edit), `script_search` (≤10), `script_grep` (≤50) |
| Assets/gen | `generate_mesh`, `generate_material`, `generate_procedural_model`, `wait_job_finished`, `search_asset`, `insert_asset`, `upload_image`, `store_image` |
| DataModel | `search_game_tree`, `inspect_instance`, `subagent` (`explore`, `playtest`) |
| Luau | `execute_luau` (`datamodel_type` Edit / Client / Server) |
| Playtest | `get_studio_state`, `start_stop_play`, `get_console_output`, `screen_capture` |
| Input sim | `character_navigation`, `user_keyboard_input`, `user_mouse_input` |
| Docs | `http_get` (Roblox docs only), `skill` |
| Session | `list_roblox_studios` |

How Claude should drive Studio:
1. `list_roblox_studios` → pick `studio_id`.
2. Inspect: `search_game_tree` / `inspect_instance` to learn the place structure (map, tags, attributes).
3. Code: edit files in the Rojo repo (source of truth). Use `multi_edit` only for places not managed by Rojo.
4. World building: `execute_luau` with `datamodel_type = Edit` to create/modify instances (batched, idempotent scripts; tag created objects).
5. Verify: `start_stop_play` → `character_navigation` / input tools → `get_console_output` + `screen_capture` → stop. Use `execute_luau` with `Server` datamodel during play to assert state (e.g. read a player's profile coins).
6. Report findings; commit code; save the place (Studio) for map changes.
Safety: MCP clients can modify any open place — connect only trusted clients; close production places you aren't working on; keep Studio API access to DataStores off (or use ProfileStore Mock) during AI playtests.

## Checklist
- [ ] `rokit.toml`, `default.project.json`, `wally.toml`, `selene.toml`, `stylua.toml`, `.github/workflows/ci.yml` committed.
- [ ] `Packages/`, `ServerPackages/`, `sourcemap.json`, `*.rbxl` gitignored.
- [ ] Rojo plugin installed in Studio; `rojo serve` connects.
- [ ] Studio MCP enabled and Claude Code connected; `list_roblox_studios` works.
- [ ] CI green before every publish.

## Pitfalls
- Editing scripts in Studio while Rojo syncs → edits lost on next sync. Studio is for the world, git for code.
- Two-way sync of the map via Rojo `.rbxm` is possible but merge conflicts on binary models are painful — keep the map in the place file, version via Studio's place history, or export key models as `.rbxm`.
- Forgetting `wally-package-types` → packages typed `any`.
- AI `execute_luau` in Edit mode makes permanent changes — use ChangeHistoryService-compatible edits or save a copy first ⚠️ verify: whether MCP edits are undoable.

## Related
- [[Module-Architecture]]
- [[Project-Bootstrap-Checklist]]
- [[Roblox Code Gate Skill]]
- [[Common-Libraries]]
- [[Luau-Strict-Typing]]

## Sources
- https://create.roblox.com/docs/studio/mcp (via github.com/Roblox/creator-docs, read 2026-10-04)
- https://devforum.roblox.com/t/assistant-updates-studio-built-in-mcp-server-and-playtest-automation/4474643 (announcement; not directly fetchable 2026-10-04)
- https://github.com/Roblox/studio-rust-mcp-server
- https://rojo.space, https://github.com/rojo-rbx/rokit, https://wally.run, https://github.com/Kampfkarren/selene, https://github.com/JohnnyMorganz/StyLua, https://github.com/JohnnyMorganz/luau-lsp (tags via `git ls-remote`, 2026-10-04)
