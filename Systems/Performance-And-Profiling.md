---
tags: [systems/performance]
status: draft
updated: 2026-10-06
confidence: medium
---
# Performance and Profiling

## TL;DR
- Frame budget at 60 FPS is **16.67 ms** (client and server Heartbeat). Measure on a **real low-end phone**, not Studio — Studio runs client+server and skews memory/FPS.
- Tools: **MicroProfiler** (Ctrl+Alt+F6 / ⌘⌥F6; Ctrl+P pause) for frame time, **Developer Console** (F9) for memory/network/server stats, **Script Profiler** (Dev Console → ScriptProfiler, or `ScriptProfilerService`) for Luau hot functions, `debug.profilebegin/profileend` for custom labels.
- Keep server memory < **50%** of `6.25 GiB + 100 MiB × peak players` (30 players ≈ 9.18 GiB). Client crash rate > 2–3% in the Performance dashboard = investigate.
- Mobile baseline targets (rule of thumb from Roblox's example): < **1,000 draw calls** and < **1,000,000 triangles** in view; enable StreamingEnabled; reuse meshes/textures; prefer built-in materials.
- Top killers: per-frame loops doing heavy work, leaked connections (`LuaHeap` growing), thousands of unanchored parts, high-collision-fidelity meshes, `Instance.new`/`Destroy` churn, chatty remotes, partial transparency overdraw.
- Pool frequently spawned objects (projectiles, VFX, damage numbers); move them with `workspace:BulkMoveTo` instead of setting CFrame per part.

## Details

### Tool map
| Question | Tool | How |
|---|---|---|
| Why is FPS low? | MicroProfiler | Ctrl+Alt+F6, Ctrl+P to freeze, find longest bars; `debug.profilebegin("Label")` around suspects |
| Which Luau function is hot? | Script Profiler | Dev Console (F9) → ScriptProfiler tab → Start on Client/Server; sort by total time |
| Memory leak? | Dev Console → Memory | Watch `LuaHeap` and `PlaceScriptMemory` over 30+ min with players joining/leaving; use `debug.setmemorycategory("ServiceName")` so script memory is attributed |
| Lua heap contents | Heap snapshot (`HeapProfilerService`) ⚠️ verify: UI location in Dev Console | Compare two snapshots |
| Client asset memory | Dev Console → Memory → PlaceMemory → `GraphicsMeshParts`, `GraphicsTexture`, `Sounds` | Reduce unique assets |
| Physics cost | Memory `PhysicsParts`; MicroProfiler `physicsStepped` | Lower collision fidelity, anchor, sleep |
| Network | Dev Console → Network / Server Stats (data ping); Shift+F3 network stats; MicroProfiler network | Find chatty remotes, replication queues |
| Render | Shift+F2 render stats (Draw (scene) calls/triangles) | Cut draw calls/tris |
| Join size | Studio Settings → Network → **Print Join Size Breakdown** | Shrink top instances |
| Load time | Stopwatch / `game.Loaded` timing in ReplicatedFirst | – |
| Device testing | Real devices + Studio Device Emulator (aspect/controls only, not memory) | – |

### Budgets (defaults to start from)
| Metric | Target | Source/confidence |
|---|---|---|
| Client frame | ≤ 16.67 ms on baseline phone | docs |
| Server Heartbeat | ≥ 55 Hz sustained at max players; server frame time < 10 ms average | ⚠️ verify: rule of thumb |
| Script time per frame (all scripts, client) | ≤ 3–4 ms | rule of thumb |
| Draw calls / triangles visible | < 1,000 / < 1,000,000 on baseline device | docs example |
| Total parts in workspace | ≤ 20–30k with streaming; unanchored parts ≤ a few hundred moving at once | ⚠️ verify: community rule of thumb |
| Server memory | < 50% of allocation | docs |
| Client memory on low-end mobile | keep under ~1–1.5 GB total ⚠️ verify: device-dependent | rule of thumb |
| Client crash rate | < 2–3% | docs |
| Instances replicated at join | as few as possible; stream the world | – |

### Common perf killers → fixes
| Killer | Fix |
|---|---|
| `RunService.Heartbeat/RenderStepped` doing work for every entity every frame | Event-driven code; tick at 10–20 Hz with an accumulator; spread work across frames (round-robin N entities per frame) |
| `while true do wait() end` polling | Signals (`GetPropertyChangedSignal`, `ChildAdded`), `task.wait(interval)` |
| Leaked connections (CharacterAdded per player never disconnected, per-instance connections on destroyed instances not in a destroyed tree) | Trove/Janitor per object; clean player-keyed tables on PlayerRemoving |
| Tables keyed by Player/Instance never cleared | `PlayerRemoving` cleanup or weak tables (`setmetatable(t, {__mode = "k"})`) |
| `GetDescendants()` / `FindFirstChild` chains every frame | Cache references; use CollectionService tags |
| Spawning/destroying hundreds of parts per second | Object pool + `BulkMoveTo` |
| Many unanchored parts / complex constraint mechanisms | Anchor scenery; `CollisionFidelity = Box/Hull`; `CanCollide/CanTouch/CanQuery = false` for decor |
| `Touched` on many parts | Spatial queries (`GetPartBoundsInBox`) at a fixed rate |
| `PhysicsSteppingMethod = Fixed` | Use Adaptive (Fixed forces 240 Hz) |
| Partial transparency, many lights with shadows, huge textures | 0/1 transparency, limit shadowed lights, 512–1024 px textures for most assets |
| Humanoids on NPCs (expensive) | Use AnimationController + custom movement for crowds |
| Big remotes every frame | Batch/delta/quantise ([[Remotes-And-Networking]]) |

### Object pool
```lua
--!strict
-- ReplicatedStorage/Shared/Util/PartPool.luau
-- Pools BaseParts; parks inactive ones far away instead of reparenting (reparenting is costly).
local PartPool = {}
PartPool.__index = PartPool

local PARK_CFRAME = CFrame.new(0, -10_000, 0)

type PoolData = { template: BasePart, free: { BasePart }, folder: Folder }
export type PartPool = typeof(setmetatable({} :: PoolData, PartPool))

function PartPool.new(template: BasePart, prewarm: number, parent: Instance): PartPool
	local folder = Instance.new("Folder")
	folder.Name = template.Name .. "Pool"
	folder.Parent = parent
	local self = setmetatable({ template = template, free = {}, folder = folder } :: PoolData, PartPool)
	local parts: { BasePart } = {}
	for i = 1, prewarm do
		local p = template:Clone()
		p.Anchored = true
		p.Parent = folder
		parts[i] = p
		table.insert(self.free, p)
	end
	workspace:BulkMoveTo(parts, table.create(#parts, PARK_CFRAME), Enum.BulkMoveMode.FireCFrameChanged)
	return self
end

function PartPool.acquire(self: PartPool, cf: CFrame): BasePart
	local p = table.remove(self.free)
	if p == nil then
		p = self.template:Clone()
		p.Anchored = true
		p.Parent = self.folder
	end
	p.CFrame = cf
	return p
end

function PartPool.release(self: PartPool, p: BasePart)
	p.CFrame = PARK_CFRAME
	table.insert(self.free, p)
end

return PartPool
```
For many moving pooled parts per frame, collect parts and CFrames into arrays and call `workspace:BulkMoveTo(parts, cframes, Enum.BulkMoveMode.FireCFrameChanged)` once.

### Profiling workflow (do this before every major release)
1. Join a live/private server with ≥ max players (or use Studio local server with N clients for scripts only).
2. Baseline device: record FPS (Shift+F5), memory (F9), crash rate on the Creator Hub Performance dashboard.
3. MicroProfiler dump of worst moment (heavy combat, round start); find top 3 labels.
4. Script Profiler on server for 60 s at peak; fix the top function.
5. Leave server running 1 h with churn; `LuaHeap` should plateau.
6. Log results in the project notes; re-test after fixes.

## Checklist
- [ ] Baseline low-end Android device chosen and tested each milestone.
- [ ] `debug.setmemorycategory` per service/controller.
- [ ] All per-entity loops run ≤ 20 Hz unless visual.
- [ ] Pools for projectiles/VFX/damage numbers.
- [ ] Decor parts: Anchored, CanCollide/CanTouch/CanQuery false, low collision fidelity.
- [ ] StreamingEnabled on; join size breakdown reviewed.
- [ ] Performance dashboard (Creator Hub) checked weekly after launch.

## Pitfalls
- **Distant parts and MeshParts are culled by graphics quality** (local test, Trap Your Friends Sky v3, 2026-10-06, Studio on a PC). Markers drew out to roughly 250 studs at quality 1, ~400 at 5, ~600 at 10, and 3,000+ at 21; culling looked like it goes by the distance to the nearest surface. Terrain `Clouds` and the skybox draw at every level. Decorative far objects (cloud rings, silhouettes) are a high-quality bonus, and map landmarks more than ~300 studs away can vanish on low phones. ⚠️ verify on a real phone. Details: [[Trap-Your-Friends-Sky-v3-Plan]].
- Optimising from Studio numbers.
- `--!native` as a perf fix for code that is actually API-bound (no gain; see [[Luau-Strict-Typing]]).
- Destroying pooled objects by accident (e.g. via Debris) and leaking pool slots.
- Assuming the server is fast: one 100 ms server spike every second stutters every player's physics/replication.
- Too many `task.spawn` per frame (thread churn) — batch work in one loop.

## Related
- [[Parallel-Luau]]
- [[Streaming-And-Instance-Streaming]]
- [[Physics-And-Network-Ownership]]
- [[Remotes-And-Networking]]
- [[Luau-Strict-Typing]]

## Sources
- https://create.roblox.com/docs/performance-optimization/identify (server memory formula, 50% guidance, crash 2–3%; via github.com/Roblox/creator-docs 2026-10-04)
- https://create.roblox.com/docs/performance-optimization/design (16.67 ms, 1,000 draw calls / 1M triangles example)
- https://create.roblox.com/docs/performance-optimization/improve (LuaHeap, PlaceScriptMemory, PhysicsParts, Fixed stepping 240 Hz)
- https://create.roblox.com/docs/performance-optimization/microprofiler/use-microprofiler (shortcuts)
- https://create.roblox.com/docs/reference/engine/classes/ScriptProfilerService
