---
tags: [systems/physics, systems/networking]
status: draft
updated: 2026-10-04
confidence: high
---
# Physics and Network Ownership

## TL;DR
- Physics is simulated per **assembly** (parts rigidly joined by welds/Motor6Ds). Each unanchored assembly has one **network owner** (server or one client) whose simulation is authoritative and replicated.
- Default: the engine **auto-assigns** ownership of unanchored parts near a player to that player's client; anchored parts are always server-owned.
- A client that owns a part can move it anywhere — so **gameplay-critical** unanchored objects (balls in a sports game scored by server, loot, enemy NPCs) must be `SetNetworkOwner(nil)` (server) or validated.
- Give vehicles to the driver (`vehicleSeat:SetNetworkOwner(player)` on sit, `SetNetworkOwnershipAuto()` on exit) for responsive control, then sanity-check speed/position on the server.
- Use **mover constraints** (`LinearVelocity`, `AngularVelocity`, `AlignPosition`, `AlignOrientation`, `VectorForce`, `Torque`) — legacy BodyMovers (`BodyVelocity`, `BodyPosition`, `BodyGyro`…) are deprecated.
- Use **collision groups** via **`workspace:RegisterCollisionGroup` / `workspace:CollisionGroupSetCollidable`** (per-world WorldRoot API) and `BasePart.CollisionGroup` to stop players colliding with each other, pets, projectiles. The `PhysicsService` collision-group methods are **deprecated** (superseded by WorldRoot, checked 2026-10-04).

## Details

### Ownership rules (docs, 2026-10-04)
- Server owns all parts by default; anchored parts are always server-owned and can't be reassigned.
- Automatic ownership: engine gives parts close to a player's character to that client, based on proximity and client hardware.
- Setting ownership on one assembly in a mechanism with no anchored parts applies to **every** assembly in that mechanism.
- Anchoring then unanchoring a lone assembly resets ownership to automatic.
- `SetNetworkOwner` is **server-only**. `GetNetworkOwner()` returns the owning Player or `nil` (server). `CanSetNetworkOwnership()` tells you if it's allowed (fails for anchored/welded-to-anchored).
- Setting server ownership on things players physically interact with causes visible latency/jitter for them — use it conservatively.

### Decision table
| Object | Owner | Why |
|---|---|---|
| Player character | That client (forced) | Responsiveness; validate movement server-side |
| Driven vehicle | Driver | Responsiveness; validate speed/teleports |
| Unoccupied vehicle | Auto or server | Prevent nearby exploiters flinging it |
| NPCs/enemies | Server (`SetNetworkOwner(nil)` on root) | Exploiters could otherwise teleport/kill/fling them |
| Scoring ball / objective item | Server | Integrity of win conditions |
| Physics debris / cosmetic props | Auto | Cheap; outcome irrelevant |
| Projectiles | Usually not physics at all: server raycast + client visual | Precision and security |
| Carried item (player picks up) | Holder (weld to character) | Responsiveness; server validates drop/use |

```lua
--!strict
-- ServerScriptService/Server/Services/NpcService.luau (excerpt)
local function claimForServer(model: Model)
	for _, d in model:GetDescendants() do
		if d:IsA("BasePart") and not d.Anchored and d:CanSetNetworkOwnership() then
			d:SetNetworkOwner(nil)
		end
	end
end
```
```lua
--!strict
-- Vehicle driver ownership (server Script inside the vehicle model or a VehicleService)
local function bindSeat(seat: VehicleSeat)
	seat:GetPropertyChangedSignal("Occupant"):Connect(function()
		local hum = seat.Occupant
		if hum then
			local player = game:GetService("Players"):GetPlayerFromCharacter(hum.Parent)
			if player and seat:CanSetNetworkOwnership() then
				seat:SetNetworkOwner(player)
			end
		elseif seat:CanSetNetworkOwnership() then
			seat:SetNetworkOwnershipAuto()
		end
	end)
end
```

### Constraints vs BodyMovers
| Need | Use |
|---|---|
| Set velocity (conveyor, dash) | `LinearVelocity` (attachment-based; `VelocityConstraintMode` Vector/Line/Plane) |
| Hold position (hover, pick-up) | `AlignPosition` (+ `AlignOrientation`) |
| Constant force (thrusters, wind) | `VectorForce` / `Torque` |
| Spin | `AngularVelocity` / `HingeConstraint` with Motor actuator |
| One-off impulse | `BasePart:ApplyImpulse()` (on owner side; on server only affects server-owned parts) |
| Character-like controllers without Humanoid | `ControllerManager` + `GroundController`/`AirController` (not deprecated as of 2026-10-04) |
| Joints | `WeldConstraint` for static welds, `Motor6D` for animated rigs, `RigidConstraint` for attachment-based rigid joints |

### Collision groups
```lua
--!strict
-- ServerScriptService/Server/Services/CollisionService.luau
local Players = game:GetService("Players")

local CollisionService = {}

function CollisionService.Init(self: typeof(CollisionService))
	-- WorldRoot API (workspace); PhysicsService equivalents are deprecated.
	workspace:RegisterCollisionGroup("Players")
	workspace:RegisterCollisionGroup("Pets")
	workspace:CollisionGroupSetCollidable("Players", "Players", false)
	workspace:CollisionGroupSetCollidable("Pets", "Players", false)
	workspace:CollisionGroupSetCollidable("Pets", "Pets", false)
end

local function setGroup(model: Model, group: string)
	for _, d in model:GetDescendants() do
		if d:IsA("BasePart") then d.CollisionGroup = group end
	end
	model.DescendantAdded:Connect(function(d)
		if d:IsA("BasePart") then d.CollisionGroup = group end
	end)
end

function CollisionService.Start(self: typeof(CollisionService))
	Players.PlayerAdded:Connect(function(player)
		player.CharacterAdded:Connect(function(char) setGroup(char, "Players") end)
	end)
end

return CollisionService
```
Max collision groups: **32** (`workspace:GetMaxCollisionGroups()`, docs 2026-10-04). Register groups at edit-time (Collision Groups editor) for static content.

### Physics performance
- Anchor everything that doesn't need to move. Sleeping assemblies cost little; awake ones with many contacts cost a lot.
- `CollisionFidelity`: `Box` or `Hull` for most meshes; `PreciseConvexDecomposition` only where it matters. High fidelity shows in `PhysicsParts` memory.
- `CanTouch = false` and `CanQuery = false` on decor removes them from Touched and raycasts.
- `Workspace.PhysicsSteppingMethod = Adaptive` (Fixed forces 240 Hz for all).
- Massless (`Massless = true`) for accessories/welded visuals on vehicles to avoid handling changes.

### Physics exploit risks
- Client-owned parts can be flung at other players (fling exploits) → keep other players' collisions off or server-own shared objects; cap `AssemblyLinearVelocity` server-side on server-owned things players touch.
- Client can make its character fly/noclip — see [[Anti-Exploit-And-Server-Authority]].
- `Touched` events fire on the owner's simulation: a client can generate Touched with your coin by moving its parts there — verify distance server-side.

## Checklist
- [ ] NPCs and objective items server-owned.
- [ ] Vehicles: driver ownership on sit, auto on exit, server speed sanity check.
- [ ] No legacy BodyMovers in new code.
- [ ] Collision groups for players/pets/projectiles.
- [ ] Decor anchored, low fidelity, CanTouch/CanQuery off.

## Pitfalls
- Calling `SetNetworkOwner` on a part welded to an anchored part → error; check `CanSetNetworkOwnership()`.
- Server-owning a ball players dribble → laggy feel; consider client-owner with server validation, or Server Authority mode.
- Applying forces from the server to a client-owned part does nothing visible (the owner's sim wins).
- Re-anchoring/unanchoring resets ownership to automatic.

## Related
- [[Anti-Exploit-And-Server-Authority]]
- [[Client-Server-Boundary-And-Replication]]
- [[Performance-And-Profiling]]
- [[Streaming-And-Instance-Streaming]]

## Sources
- https://create.roblox.com/docs/physics/network-ownership (via github.com/Roblox/creator-docs, read 2026-10-04)
- https://create.roblox.com/docs/physics/assemblies
- https://create.roblox.com/docs/physics/mover-constraints
- https://create.roblox.com/docs/workspace/collisions
- https://create.roblox.com/docs/reference/engine/classes/WorldRoot (collision group methods; PhysicsService versions deprecated)
- https://create.roblox.com/docs/scripting/security/network-ownership
