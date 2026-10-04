---
tags: [systems/performance, systems/parallel]
status: draft
updated: 2026-10-04
confidence: medium
---
# Parallel Luau

## TL;DR
- Only reach for Parallel Luau when the **Script Profiler shows a CPU-bound Luau hotspot** (> ~2 ms/frame) made of many **independent** units of work: raycasts for many NPCs, pathfinding grids, procedural generation, visibility checks, custom physics/math.
- Scripts must live under an **Actor**; code runs serially until `task.desynchronize()` (or `:ConnectParallel`). Write to instances only after `task.synchronize()`.
- One Actor = one thread lane. Scripts in the same Actor run serially, so split work into **several Actors** (≈ number of cores, 4–8), not one per entity when entities number in the thousands.
- Communicate with `Actor:SendMessage` / `BindToMessageParallel` and **`SharedTable`** for large shared state; don't share Luau tables between Actors (each Actor has its own VM).
- Most simulators/tycoons/obbies never need it — fix algorithmic waste first.

## Details

### Model
- Each Actor's scripts run in a separate Luau VM. Module requires are **per VM** (a module required in two Actors has two copies/states).
- Frame phases: serial → parallel (desynchronized code from all Actors runs across cores) → serial again.
- Thread safety tags on API members: **Unsafe** (default if unlabeled; cannot use in parallel), **Read Parallel** (read only), **Local Safe** (usable within the same Actor), **Safe**. Engine blocks unsafe access in parallel with an error.
- Raycasts/spatial queries (`workspace:Raycast`, `GetPartBoundsInBox`) are usable in parallel — the main reason to parallelise NPC sensing. ⚠️ verify: current thread-safety tags for specific APIs in the API reference.

### Pattern: N worker Actors processing a shared work list
```lua
--!strict
-- ServerScriptService/Server/Parallel/Dispatcher.server.luau
-- Clones a worker Actor template N times and sends each a slice of NPC ids every tick.
local RunService = game:GetService("RunService")
local ServerScriptService = game:GetService("ServerScriptService")
local ServerStorage = game:GetService("ServerStorage")

local WORKERS = 4
-- Template lives in ServerStorage so its script doesn't run until cloned into ServerScriptService.
local template = ServerStorage:WaitForChild("WorkerTemplate") :: Actor
local parallelFolder = Instance.new("Folder")
parallelFolder.Name = "ParallelWorkers"
parallelFolder.Parent = ServerScriptService

local actors: { Actor } = {}
for i = 1, WORKERS do
	local a = template:Clone()
	a.Name = `Worker{i}`
	a.Parent = parallelFolder
	table.insert(actors, a)
end

-- Shared state readable from all Actors without copying per message.
local npcPositions = SharedTable.new()

local acc = 0
RunService.Heartbeat:Connect(function(dt)
	acc += dt
	if acc < 0.1 then return end -- 10 Hz sensing
	acc = 0
	-- (populate npcPositions[id] = Vector3 from your NPC registry here, serially)
	for i, actor in actors do
		actor:SendMessage("Sense", npcPositions, i, WORKERS)
	end
end)
```
```lua
--!strict
-- ServerStorage/WorkerTemplate (Actor) / Worker (Script, RunContext = Legacy so it only runs once cloned into ServerScriptService)
local actor = script:GetActor()
assert(actor, "Worker must be under an Actor")

local params = RaycastParams.new()
params.FilterType = Enum.RaycastFilterType.Exclude

actor:BindToMessageParallel("Sense", function(positions: SharedTable, index: number, total: number)
	local results: { [any]: boolean } = {}
	local n = 0
	for id, pos in positions do
		n += 1
		if n % total == index - 1 then -- this worker's slice
			local hit = workspace:Raycast(pos :: Vector3, Vector3.new(0, -50, 0), params)
			results[id] = hit ~= nil
		end
	end
	task.synchronize() -- back to serial before touching instances / firing events
	-- apply results: set attributes, move NPCs, etc.
end)
```
SharedTables support element access and generalized `for` iteration (official code sample "SharedTable-ElementIteration"). Keys must be strings or non-negative integers < 2^32 — use numeric/string NPC ids, never Instances as keys.

### SharedTable notes
- `SharedTable.new()`; values: boolean, number, vector, string, nested SharedTable, or a serializable data type (no functions; ⚠️ verify: whether Instance references count as "serializable" — assume not). Keys: string or integer 0..2^32-1.
- Share by sending in `Actor:SendMessage` or registering by name in `SharedTableRegistry` (`SharedTableRegistry:GetSharedTable(name)` / `SetSharedTable`).
- Concurrent writes from multiple Actors are allowed but racy — prefer **one writer** (serial phase) and many parallel readers, or `SharedTable.update(st, key, fn)` for atomic per-key updates.
- `SharedTable.cloneAndFreeze` for cheap read-only snapshots.

### When it is worth it — decision rule
1. Profile. Is the cost Luau CPU (not rendering/physics/network)? If no → stop.
2. Can the work be split into independent chunks with read-only world access? If no → optimise algorithm or spread over frames.
3. Is the hotspot ≥ 2 ms/frame on server or target client? If no → messaging overhead may exceed gains.
4. Implement with 4 Actors, measure with MicroProfiler (parallel lanes visible), tune count.

### Alternatives first
- Spread work over frames (time-slicing: process 50 NPCs per Heartbeat).
- Lower update rate (10 Hz sensing instead of 60 Hz).
- `@native` on numeric hot functions ([[Luau-Strict-Typing]]).
- Spatial partitioning (grid buckets) to cut O(n²) checks.

## Checklist
- [ ] Hotspot measured and documented before parallelising.
- [ ] Workers under Actors; instance writes only after `task.synchronize()`.
- [ ] Actor count ~4–8, not per-entity for large counts.
- [ ] MicroProfiler confirms parallel lanes and frame-time drop.

## Pitfalls
- Expecting module state to be shared across Actors (it's not; separate VMs).
- Writing instance properties in parallel → error "not safe to call in parallel" / blocked writes.
- One Actor per tiny entity → overhead dominates; scripts in an Actor still run serially.
- `ConnectParallel` on high-frequency events with trivial work → slower than serial.
- Forgetting the client has fewer cores on mobile; client parallelism yields less there.

## Related
- [[Performance-And-Profiling]]
- [[Luau-Strict-Typing]]
- [[Module-Architecture]]

## Sources
- https://create.roblox.com/docs/scripting/multithreading (via github.com/Roblox/creator-docs, read 2026-10-04)
- https://create.roblox.com/docs/reference/engine/datatypes/SharedTable (read 2026-10-04)
- https://create.roblox.com/docs/reference/engine/classes/Actor
