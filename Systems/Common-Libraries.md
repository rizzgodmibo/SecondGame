---
tags: [systems/libraries]
status: draft
updated: 2026-10-04
confidence: medium
---
# Common Libraries

## TL;DR
- **Default stack for a new game (2026-10):** ProfileStore (data) + Trove (cleanup) + Signal (events) + plain RemoteEvents with guards, upgraded to **Blink** when bandwidth matters + **Vide** or **Fusion** for reactive UI (or plain Instances for small UIs) + TopbarPlus for topbar buttons.
- **Don't start new projects on Knit** — archived. Use the ~40-line Init/Start loader from [[Module-Architecture]].
- Install via **Wally**; pin versions; vendor (commit) any lib not on Wally.
- Every library is code you ship: read it, prefer small, typed, maintained ones; check last commit date before adopting.
- Avoid libraries for things Roblox now does natively (e.g. `UnreliableRemoteEvent`, `Players:BanAsync`, `TextChatService`, Input Action System).

## Details

### Catalogue (versions = latest git tags checked 2026-10-04)
| Library | Purpose | Version / status | Use when | Avoid when |
|---|---|---|---|---|
| **ProfileStore** (MadStudioRoblox / loleris) | Session-locked player data, auto-save, messages | v1.0.3 (Wally `lm-loleris/profilestore`) — active successor to ProfileService | Always for player data | Never for leaderboards/ephemeral data |
| ProfileService | Older loleris data lib | Superseded by ProfileStore | Existing games only | New projects |
| **Trove** (Sleitnick, RbxUtil) | Cleanup of connections/instances/threads | 1.8.0 (`sleitnick/trove`) | Per-object/per-round cleanup | – |
| Janitor (howmanysmall) | Same role as Trove | v1.17.0 | Team already uses it | Mixing both in one codebase |
| **Signal** (Sleitnick, RbxUtil) / GoodSignal (stravant) | Fast Luau signals | signal 2.0.3 / goodsignal v0.3.0 | Module-to-module events | Cross-VM (Actors) — use Actor messaging |
| **Promise** (evaera) | A+ promises, cancellation | v4.0.0-rc.3 | Complex async orchestration | Simple retry (use plain pcall + backoff) |
| **Fusion** (dphfox / Elttob) | Reactive UI (state objects, Computeds, scopes) | v0.3 (beta tags) | Medium–large UI, team likes declarative | Tiny UIs |
| **Vide** (centau) | Reactive UI inspired by Solid; fully Luau-typecheckable | 0.4.1 | Strict-typed declarative UI, smaller API than Fusion | – |
| **React-lua** (jsdotlua) | React 17 port used by Roblox itself | v17.2.1 | Team with React experience, very large UI | Small teams; heavier runtime |
| Roact | Legacy | Deprecated in favour of react-lua | – | New work |
| **Knit** (Sleitnick) | Service/controller framework + networking | v1.7.0, **archived** | Maintaining an existing Knit game | New projects |
| **Blink** (1Axen) | IDL → generated, buffer-packed networking with type validation | v0.18.9 (1.0.0-pre.10 pre-release) | Bandwidth-heavy games; strong typing | Very small games (extra build step) |
| **Zap** (red-blox) | IDL networking compiler, similar to Blink | v0.6.29 | Alternative to Blink | Using both |
| **ByteNet** (ffrostfall) | Runtime-defined buffer serialization | v0.4.3 | Want buffer packing without codegen | ⚠️ verify: maintenance status |
| **TopbarPlus** (1ForeverHD) | Topbar icons/menus matching Roblox UI | v3.4.0 | Buttons in the top bar | ⚠️ verify: compatibility with current Roblox topbar layout after UI updates |
| Lune | Standalone Luau runtime for scripts/tests outside Roblox | – | CI tests for pure modules, build scripts | In-game code |
| Jest-Lua (Roblox) | Jest-style test framework | – | In-engine unit tests | – |

### Usage snippets
```lua
--!strict
-- Trove: per-round cleanup (server)
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Trove = require(ReplicatedStorage.Packages.Trove)

local function startRound(arena: Model)
	local trove = Trove.new()
	trove:Connect(arena.ChildAdded, function(child: Instance)
		print("spawned", child.Name)
	end)
	trove:Add(task.delay(120, function() print("round over") end)) -- threads are task.cancel'd on cleanup
	return function()
		trove:Destroy() -- disconnects, cancels thread, destroys added instances
	end
end
```
```lua
--!strict
-- Signal: typed module events
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Signal = require(ReplicatedStorage.Packages.Signal)

local CurrencyEvents = {
	Changed = Signal.new() :: Signal.Signal<Player, number>, -- module exports `Signal<T...>` (2.0.3)
}
CurrencyEvents.Changed:Connect(function(player: Player, newValue: number)
	print(player.Name, newValue)
end)
CurrencyEvents.Changed:Fire(game:GetService("Players"):GetPlayers()[1], 100)
```

### Selection rules
1. Prefer Roblox-native features when they exist (UnreliableRemoteEvent, Input Action System, TextChatService, Ban API, MemoryStore).
2. One library per role (don't mix Trove and Janitor; Fusion and Vide).
3. Check: last commit < 12 months, issues answered, typed for `--!strict`, licence (MIT/MPL fine).
4. Wrap third-party APIs behind your own thin module where swapping is plausible (networking, UI).
5. Record the choice and version in the project's decision log (`Projects/<name>/`).

## Checklist
- [ ] `wally.toml` lists pinned versions; `wally install` reproducible.
- [ ] `wally-package-types` run so packages are typed.
- [ ] No Knit/Roact/ProfileService in new projects.
- [ ] Each library read once (skim source) before adopting.

## Pitfalls
- Requiring a server-realm package (ProfileStore) from a client → it isn't there (ServerPackages not replicated) — correct and intended.
- Copying libs from the Toolbox with hidden backdoors (`require(assetId)`, `getfenv`) — only install from Wally/GitHub, grep for `require(%d` before shipping.
- Mixing Signal libraries with `BindableEvent`s — Bindables deep-copy tables and drop metatables.
- Using pre-1.0 networking libs without pinning exact versions (breaking schema changes).

## Related
- [[Module-Architecture]]
- [[Remotes-And-Networking]]
- [[Data-Persistence-DataStores-And-ProfileStore]]
- [[Tooling-Rojo-Wally-And-Studio-MCP]]
- [[Error-Handling-And-Logging]]

## Sources
- https://github.com/MadStudioRoblox/ProfileStore (wally.toml 1.0.3, read 2026-10-04)
- https://github.com/Sleitnick/RbxUtil (trove 1.8.0, signal 2.0.3 wally.toml, read 2026-10-04)
- https://github.com/Sleitnick/Knit (README: archived, read 2026-10-04)
- Tags via `git ls-remote` 2026-10-04: github.com/howmanysmall/Janitor, stravant/goodsignal, evaera/roblox-lua-promise, dphfox/Fusion, centau/vide, jsdotlua/react-lua, 1Axen/blink, red-blox/zap, ffrostfall/ByteNet, 1ForeverHD/TopbarPlus
