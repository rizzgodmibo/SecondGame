---
tags: [systems/architecture]
status: draft
updated: 2026-10-04
confidence: high
---
# Module Architecture

## TL;DR
- Use **single-script architecture**: one `Script` (server) and one `LocalScript` (client) bootstrap that require ModuleScripts. Everything else is a ModuleScript.
- Server logic = **Services** (`ServerScriptService/Server/Services`), client logic = **Controllers** (`StarterPlayerScripts/Client/Controllers`), shared code in `ReplicatedStorage/Shared`.
- Two-phase lifecycle: **`Init()`** (synchronous, no yielding, wire references) for all modules, then **`Start()`** (may yield/spawn loops) for all modules. This removes almost all circular-require needs.
- Secrets (economy tables with server-only data, admin lists, loot weights you don't want datamined) go in **ServerScriptService/ServerStorage**, never ReplicatedStorage.
- Remotes are created **by the server in code** (or declared by a networking lib like Blink/Zap), never hand-placed scattered instances.
- Manage the project with **Rojo** so code lives in git; Studio holds only the map/assets.

## Details

### Recommended layout (Rojo `src/` → DataModel)
```
src/
  server/                     -> ServerScriptService.Server
    Main.server.luau          (bootstrap Script)
    Services/
      DataService.luau
      CurrencyService.luau
      CombatService.luau
  client/                     -> StarterPlayer.StarterPlayerScripts.Client
    Main.client.luau          (bootstrap LocalScript)
    Controllers/
      UIController.luau
      InputController.luau
  shared/                     -> ReplicatedStorage.Shared
    Types.luau
    Config/                   (tuning tables safe for clients to see)
    Net.luau                  (remote definitions / generated networking)
    Util/
  first/                      -> ReplicatedFirst.First  (loading screen only)
Packages/                     -> ReplicatedStorage.Packages (Wally shared)
ServerPackages/               -> ServerScriptService.ServerPackages (Wally server realm)
```
Assets that the server clones (maps, NPC templates) → `ServerStorage`. Assets the client needs (VFX, UI templates, sounds) → `ReplicatedStorage/Assets`.

### `default.project.json`
```json
{
  "name": "MyGame",
  "tree": {
    "$className": "DataModel",
    "ReplicatedStorage": {
      "Shared": { "$path": "src/shared" },
      "Packages": { "$path": "Packages" }
    },
    "ServerScriptService": {
      "Server": { "$path": "src/server" },
      "ServerPackages": { "$path": "ServerPackages" }
    },
    "StarterPlayer": {
      "StarterPlayerScripts": { "Client": { "$path": "src/client" } }
    },
    "ReplicatedFirst": { "First": { "$path": "src/first" } },
    "Workspace": { "$properties": { "StreamingEnabled": true } }
  }
}
```
File naming under Rojo: `*.server.luau` → Script, `*.client.luau` → LocalScript, `*.luau` → ModuleScript, `init.luau` inside a folder → the folder becomes that ModuleScript.

### Service contract
```lua
--!strict
-- ReplicatedStorage/Shared/Types.luau (excerpt)
export type Module = {
	Init: ((self: any) -> ())?,
	Start: ((self: any) -> ())?,
}
```

### Bootstrap (server)
```lua
--!strict
-- ServerScriptService/Server/Main.server.luau
local ServerScriptService = game:GetService("ServerScriptService")

type Module = { Init: ((any) -> ())?, Start: ((any) -> ())?, [any]: any }

local servicesFolder = ServerScriptService:WaitForChild("Server"):WaitForChild("Services")
local modules: { [string]: Module } = {}

-- 1. Require everything (module top-level must not yield or touch other services)
for _, child in servicesFolder:GetChildren() do
	if child:IsA("ModuleScript") then
		modules[child.Name] = require(child) :: any
	end
end

-- 2. Init: synchronous wiring, no yields. Errors here are fatal by design.
for name, mod in modules do
	if mod.Init then
		local t = os.clock()
		mod:Init()
		if os.clock() - t > 0.05 then warn(`[Boot] {name}.Init took {os.clock() - t}s — must not yield`) end
	end
end

-- 3. Start: may yield; spawned so one slow service doesn't block others.
for name, mod in modules do
	if mod.Start then
		task.spawn(function()
			debug.setmemorycategory(name)
			mod:Start()
		end)
	end
end

print(`[Boot] server ready: {#servicesFolder:GetChildren()} services`)
```
The client bootstrap is identical, pointed at `Client/Controllers`, and should first wait for anything critical (e.g. `Players.LocalPlayer:GetAttribute("DataLoaded")`).

### A service
```lua
--!strict
-- ServerScriptService/Server/Services/CurrencyService.luau
local CurrencyService = {}

-- typeof(require(...)) is evaluated by the type checker only; nothing is required here.
local DataService: typeof(require(script.Parent.DataService))

function CurrencyService.Init(self: typeof(CurrencyService))
	DataService = require(script.Parent.DataService) -- resolved in Init: no require-order coupling
end

function CurrencyService.Start(self: typeof(CurrencyService))
	-- connect remotes, start loops
end

function CurrencyService.Add(self: typeof(CurrencyService), player: Player, amount: number): boolean
	assert(amount == amount and amount >= 0, "bad amount")
	local profile = DataService:GetProfile(player)
	if not profile then return false end
	profile.Data.Coins += amount
	return true
end

return CurrencyService
```

### Avoiding circular requires
`require` of a module that is still loading errors ("Requested module was required recursively"). Rules:
1. **Never** call another service at module top-level. Resolve dependencies in `Init`, use them in `Start`/methods.
2. Requiring inside `Init` (as above) is safe because by then every module has finished its top-level execution.
3. If A and B genuinely need each other, extract the shared part into a third module or communicate through a Signal.
4. Shared modules (`ReplicatedStorage/Shared`) must not require server or client modules.
5. Static require paths (`script.Parent.X`) are typed by luau-lsp through the Rojo sourcemap. Studio also supports string requires (`require("./X")`) ⚠️ verify: require-by-string availability/behaviour in live servers before adopting.

### Framework choice
| Option | Status | When |
|---|---|---|
| Hand-rolled Init/Start loader (above) | ~40 lines, no deps | **Default** — fully typed, nothing to maintain |
| Knit | **Archived** (no longer updated) | Don't start new projects on it |
| Networking via Blink/Zap + loader above | Active | Competitive/bandwidth-heavy games |
See [[Common-Libraries]].

### Where code runs
| Container | Server sees | Client sees | Scripts run |
|---|---|---|---|
| ServerScriptService | yes | **no** | Server `Script`s |
| ServerStorage | yes | **no** | none (storage) |
| ReplicatedStorage | yes | yes | none by default (modules required from either side) |
| ReplicatedFirst | yes | yes (first) | `LocalScript`s, loading screen |
| StarterPlayerScripts | copied to `Player.PlayerScripts` | yes | `LocalScript`s, once per session |
| StarterCharacterScripts | copied to character | yes | re-run every respawn |
| StarterGui | copied to `PlayerGui` | yes | Prefer `ResetOnSpawn = false` ScreenGuis |
| Workspace | yes | yes (streamed) | Server scripts with `RunContext` |
Note: `Script.RunContext` (`Legacy`/`Server`/`Client`) lets a `Script` run anywhere; with single-script architecture you shouldn't need it.

## Checklist
- [ ] Exactly one server bootstrap Script and one client bootstrap LocalScript.
- [ ] Every service/controller exposes `Init`/`Start`; no top-level cross-requires.
- [ ] No ModuleScript under ServerScriptService is required by client code.
- [ ] Rojo project file committed; `Packages/` gitignored and restored by Wally.
- [ ] `debug.setmemorycategory` per service so Developer Console memory is attributable.

## Pitfalls
- Putting server-only modules in ReplicatedStorage leaks logic (exploiters can decompile anything replicated).
- Yielding in `Init` (DataStore calls, `WaitForChild`) stalls the whole boot.
- `StarterCharacterScripts` code re-runs each respawn — leaking connections unless cleaned with Trove/Janitor.
- `ResetOnSpawn = true` (default) on ScreenGuis destroys UI state on every death.
- Requiring modules by string paths built at runtime defeats type checking and luau-lsp.

## Related
- [[Luau-Strict-Typing]]
- [[Client-Server-Boundary-And-Replication]]
- [[Remotes-And-Networking]]
- [[Tooling-Rojo-Wally-And-Studio-MCP]]
- [[Project-Bootstrap-Checklist]]
- [[Common-Libraries]]

## Sources
- https://create.roblox.com/docs/scripting/locations (via github.com/Roblox/creator-docs, 2026-10-04)
- https://create.roblox.com/docs/scripting/module
- https://rojo.space/docs/v7/ (Rojo v7.7.1 latest tag, checked 2026-10-04)
- https://github.com/Sleitnick/Knit (README: "Knit has been archived", checked 2026-10-04)
