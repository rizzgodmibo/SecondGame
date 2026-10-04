---
tags: [systems/streaming, systems/performance]
status: draft
updated: 2026-10-04
confidence: high
---
# Streaming and Instance Streaming

## TL;DR
- Keep `Workspace.StreamingEnabled = true` (default for new places; cannot be set from scripts). It cuts join time and memory and is required for the Server Authority model.
- Defaults to start with: `StreamingMinRadius = 64`, `StreamingTargetRadius = 1024`, `StreamOutBehavior = Opportunistic` on memory-heavy/mobile-first games (default `LowMemory`), `StreamingIntegrityMode = PauseOutsideLoadedArea`, `ModelStreamingBehavior = Improved`.
- Client code must assume **any Workspace instance may be absent or disappear**: use `WaitForChild` with timeouts, `CollectionService` tag signals (`GetInstanceAddedSignal`/`GetInstanceRemovedSignal`), and `Instance.Destroying`/ancestry handling.
- Use `ModelStreamingMode = Atomic` for models whose parts must arrive together (interactive machines, NPCs), `Persistent` only for a handful of always-needed models (wait for `Workspace.PersistentLoaded`), `PersistentPerPlayer` for per-player always-present things (their own plot/base).
- Before a server-side teleport/spawn far away, call `player:RequestStreamAroundAsync(position, timeout)` so the area is loaded when they land.

## Details

### Key properties (Workspace)
| Property | Default | Recommendation |
|---|---|---|
| `StreamingEnabled` | true (new places) | true |
| `StreamingMinRadius` | 64 | Keep 64; raise only for fast vehicles/large sightlines |
| `StreamingTargetRadius` | 1024 | 512–1024; lower for dense maps/mobile focus; must be > MinRadius |
| `StreamOutBehavior` | `LowMemory` | `Opportunistic` if memory/OOM crashes are an issue |
| `StreamingIntegrityMode` | (not scriptable; set in Studio) ⚠️ verify: default value | `PauseOutsideLoadedArea` (pauses player in unloaded areas; customise pause UI via `Player.GameplayPaused`) |
| `ModelStreamingBehavior` | `Legacy` | `Improved` (models with BaseParts stream efficiently; non-part children don't all replicate at join) |
| `Player.ReplicationFocus` / `Player:AddReplicationFocus()` | character root | Add foci for spectating, cameras, remote-controlled vehicles |
| Frustum streaming (`Player.FrustumStreaming`, `Enum.FrustumStreamingMode`) | Default (= Disabled) | Opt-in per player from a server Script, e.g. while a scoped weapon is equipped; additive to normal radius, costs memory |

Only descendants of **Workspace** stream; ReplicatedStorage contents replicate fully at join (don't dump the whole map there).

### Model streaming modes
| Mode | Behaviour | Use for |
|---|---|---|
| `Nonatomic` (default) | Parts stream individually | Scenery |
| `Atomic` | Whole model streams in/out together once any part is eligible | NPCs, doors with scripts, vehicles, anything client code indexes into |
| `Persistent` | Sent soon after join, never streamed out; wait for `Workspace.PersistentLoaded` | Tiny number of global landmarks client scripts need (lobby portals) |
| `PersistentPerPlayer` | Persistent for players added via `Model:AddPersistentPlayer(player)`, Atomic for others | Player's own tycoon/plot, their pet |
Overusing Persistent defeats streaming and costs memory.

### Client patterns
```lua
--!strict
-- StarterPlayerScripts/Client/Controllers/DoorController.luau
-- Tag-driven: works regardless of when doors stream in or out.
local CollectionService = game:GetService("CollectionService")

local DoorController = {}
local cleanups: { [Instance]: () -> () } = {}

local function onDoorAdded(inst: Instance)
	if not inst:IsA("Model") then return end
	local conn = inst:GetAttributeChangedSignal("Open"):Connect(function()
		-- play local tween/sound based on inst:GetAttribute("Open")
	end)
	cleanups[inst] = function() conn:Disconnect() end
end

local function onDoorRemoved(inst: Instance)
	local c = cleanups[inst]
	if c then c() cleanups[inst] = nil end
end

function DoorController.Start(self: typeof(DoorController))
	CollectionService:GetInstanceAddedSignal("Door"):Connect(onDoorAdded)
	CollectionService:GetInstanceRemovedSignal("Door"):Connect(onDoorRemoved)
	for _, d in CollectionService:GetTagged("Door") do onDoorAdded(d) end
end

return DoorController
```
Streamed-out instances fire the tag-removed signal; when they stream back they're re-added (often **new** Instance objects — don't cache references across stream-out).

`WaitForChild` rules:
- Inside a known-present container (Atomic model you already have, PlayerGui, ReplicatedStorage): `WaitForChild(name)` is fine.
- For Workspace content: `WaitForChild(name, timeout)` and handle `nil`, or prefer tags.
- Never chain `workspace.Map.Area.Part` on the client.

### Server patterns
```lua
--!strict
-- ServerScriptService/Server/Services/TeleportInPlace.luau
local TeleportInPlace = {}

function TeleportInPlace.To(self: typeof(TeleportInPlace), player: Player, cf: CFrame)
	local ok, err = pcall(function()
		player:RequestStreamAroundAsync(cf.Position, 5) -- yields up to timeout
	end)
	if not ok then warn("RequestStreamAroundAsync failed", err) end
	local char = player.Character
	if char then
		-- MovementGuard.Allow(player, 2) — see Anti-Exploit note
		char:PivotTo(cf)
	end
end

return TeleportInPlace
```
- The server always has the full world; server scripts don't need stream awareness — except that instances passed to a client in a remote may arrive as `nil` if not streamed in for that client.
- Client-side physics/prediction only runs in streamed areas; add a replication focus near far-away things the client must simulate.

## Checklist
- [ ] StreamingEnabled true; radii and StreamOutBehavior set deliberately.
- [ ] `ModelStreamingBehavior = Improved`.
- [ ] Interactive models set Atomic; Persistent count ≤ a handful.
- [ ] All client world interaction is tag-based or timeout-guarded.
- [ ] Server teleports call `RequestStreamAroundAsync` first.
- [ ] Tested by walking to world edges on a low-memory device with Opportunistic stream-out.

## Pitfalls
- Client `LocalScript`s inside streamed models: they may be destroyed/recreated with the model — keep client logic in controllers.
- Caching an Instance reference on the client and using it after stream-out (now detached).
- Huge `StreamingMinRadius` → nothing ever streams out, defeats purpose.
- Putting the map in ReplicatedStorage "to avoid streaming issues" — replicates everything at join.
- UI that shows nearby objects via `workspace:GetDescendants()` on the client misses unstreamed ones; drive it from server data.

## Related
- [[Performance-And-Profiling]]
- [[Client-Server-Boundary-And-Replication]]
- [[Physics-And-Network-Ownership]]
- [[Project-Bootstrap-Checklist]]

## Sources
- https://create.roblox.com/docs/workspace/streaming (via github.com/Roblox/creator-docs, read 2026-10-04: defaults 64/1024, stream-out behaviours, model modes, PersistentLoaded, GameplayPaused)
- https://create.roblox.com/docs/reference/engine/classes/Player#RequestStreamAroundAsync
