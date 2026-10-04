---
tags: [visuals/animation]
status: draft
updated: 2026-10-04
confidence: medium
---
# Animation, Rigging and IK

## TL;DR
- **Use R15** for new games (15 parts, IK-friendly, layered clothing, dynamic heads, emotes). Use **R6** only for a deliberate retro/combat-game feel (6 parts, simpler hitboxes, huge library of combat animations). Set in Game Settings → Avatar.
- **Always play through `Animator`** (`Humanoid.Animator` or `AnimationController.Animator`). Load each animation **once** and cache the `AnimationTrack`; `LoadAnimation` always creates a new track.
- **Replication**: player-character animations started on the owning client replicate automatically; NPC animations must be played on the server. The `Animator` must be created by the server (a client-created Animator never replicates).
- **Priority**: `Core` (lowest) < `Idle` < `Movement` < `Action` < `Action2` < `Action3` < `Action4` (highest). Default character anims are Core/Idle/Movement; set attacks/emotes to `Action`+.
- **Ownership**: animation assets must be owned by the experience owner (user, or the **group** for group games) or explicitly shared via asset permissions — otherwise they silently fail to load in live servers.
- **Procedural polish** (head look, foot planting, weapon aim, springs) via `IKControl` and `Motor6D.Transform`/CFrame springs on the **client**.

## R15 vs R6 decision

| Factor | R15 | R6 |
|---|---|---|
| Parts / joints | 15 parts, Motor6Ds per limb segment | 6 parts |
| IKControl, layered clothing, dynamic heads | Yes | IK limited; no layered clothing deformation |
| Animation library | Catalog + Creator Store | Large legacy combat library |
| Feel | Modern, smoother | Snappy, retro; popular in battlegrounds/combat |
| Hitboxes | More parts, more complex | Simple |
| Recommended | Default for all new genres | Only if genre expects it (classic combat, retro obby) |

Avatar scaling: if your game needs consistent hitboxes, lock body proportions/scale in Game Settings → Avatar (or `StarterPlayer` character settings). ⚠️ verify: current Avatar settings UI names (Studio "Avatar Settings" window replaced the older Game Settings tab).

## Animator, tracks, weights

`AnimationTrack:Play(fadeTime = 0.1, weight = 1, speed = 1)`, `:Stop(fadeTime = 0.1)`, `:AdjustWeight(weight, fadeTime = 0.1)`, `:AdjustSpeed(speed)`, `.Looped`, `.Priority`, `.TimePosition`, `.Length` (0 until loaded), `:GetMarkerReachedSignal(name)`, `.Ended`, `.Stopped`.

Blending: higher priority wins per joint; **same priority → weights blend**. Use same-priority weight blending for locomotion blends (walk ↔ run by speed); different priorities for layering (upper-body attack over legs-running — key only the upper-body joints in the attack so legs fall through to Movement).

```lua
--!strict
-- ReplicatedStorage/Shared/Animation/AnimationCache.luau
-- Loads each animation once per Animator; use from client for local character, server for NPCs.
local AnimationCache = {}

local cache: { [Animator]: { [string]: AnimationTrack } } = setmetatable({}, { __mode = "k" }) :: any

function AnimationCache.get(animator: Animator, animationId: string, priority: Enum.AnimationPriority?): AnimationTrack
	local tracks = cache[animator]
	if not tracks then
		tracks = {}
		cache[animator] = tracks
	end
	local existing = tracks[animationId]
	if existing then
		return existing
	end
	local animation = Instance.new("Animation")
	animation.AnimationId = animationId
	local track = animator:LoadAnimation(animation) -- Animator must already be in Workspace
	if priority then
		track.Priority = priority
	end
	tracks[animationId] = track
	return track
end

function AnimationCache.play(animator: Animator, animationId: string, priority: Enum.AnimationPriority?, fade: number?): AnimationTrack
	local track = AnimationCache.get(animator, animationId, priority)
	track:Play(fade or 0.1)
	return track
end

return AnimationCache
```

## Animation events (markers)
- In the Animation Editor add **Animation Events** (KeyframeMarkers) e.g. `Hit`, `FootStep`, `TrailOn`, `TrailOff`, with an optional string **Parameter**.
- Listen: `track:GetMarkerReachedSignal("Hit"):Connect(function(param: string) ... end)`.
- Use markers for: hitbox windows (server-side validation still required — see [[Anti-Exploit-And-Server-Authority]]), footstep sounds, VFX/trail toggles, camera shake timing.
- Server hit detection should **not** depend on client marker timing alone; server uses its own timer (`GetTimeOfKeyframe` or known offsets) to validate.

## Tools
- **Animation Editor** (built in): 30 fps timeline by default, keyframes, easing per keyframe, **Curve Editor** for per-channel tangents, IK mode for posing, animation events, **Animation Capture** (create from video/webcam) — see docs. Publish → choose the **group** as Creator if the game is group-owned.
- **Animation Graph Editor** (Avatar tab → Graph Editor): node-based blend trees/state machines published as an `AnimationGraphDefinition` asset; load like an animation and drive with `AnimationTrack:SetParameter(name, value)`. Replication follows `Workspace.AuthorityMode`: in `Automatic`, the owning client drives player graphs (parameters auto-replicate, last-writer-wins per frame) and the server drives NPCs; in `Server`, the server simulates and clients predict. Good replacement for hand-written locomotion blend code.
- **Moon Animator 2** (third-party plugin): preferred by many animators for cutscenes, camera animation and multi-rig scenes; exports KeyframeSequences. ⚠️ verify: current price/licensing on the plugin page.
- **Blender** for complex rigs: export FBX with animation baked, import as Animation via the Importer/Animation Editor import. See [[Blender-To-Roblox-Pipeline]].

## IKControl (procedural IK)

Required properties: `Type` (`Transform`, `Position`, `Rotation`, `LookAt`), `EndEffector` (part/bone/attachment that moves), `Target` (anything with a world position), `ChainRoot` (start of chain). Optional: `Pole` (bend direction for elbows/knees), `Weight` (0–1), `SmoothTime` (seconds), `Priority` (solve order), `Offset`, `EndEffectorOffset`, `Enabled`. Parent under the `Humanoid` or `AnimationController`. IK solves on top of the playing animation.

Common uses:
| Use | Type | ChainRoot → EndEffector |
|---|---|---|
| Head looks at target / camera | `LookAt` | UpperTorso → Head (Weight 0.5–0.8, SmoothTime 0.1) |
| Hand to door handle / weapon grip | `Transform` | UpperArm → Hand (+ Pole behind elbow) |
| Foot planting on slopes/stairs | `Position` | UpperLeg → Foot, target from downward raycast |
| Turret/gun aim | `LookAt` | base → barrel |

Constrain joints with `HingeConstraint` (elbow/knee) and `BallSocketConstraint` with `LimitsEnabled`, `UpperAngle ≈ 80` (wrist), using attachments at the same positions as the Motor6D C0/C1; constraints and IKControl must share the same parent Model.

```lua
--!strict
-- StarterCharacterScripts/HeadLook.client.luau
-- Local player's head follows the camera look direction (cosmetic; runs on client).
local RunService = game:GetService("RunService")
local Workspace = game:GetService("Workspace")

local character = script.Parent :: Model
local humanoid = character:WaitForChild("Humanoid") :: Humanoid
local head = character:WaitForChild("Head") :: BasePart
local upperTorso = character:WaitForChild("UpperTorso") :: BasePart

local target = Instance.new("Attachment")
target.Name = "LookTarget"
target.Parent = Workspace.Terrain -- world-space attachment

local ik = Instance.new("IKControl")
ik.Type = Enum.IKControlType.LookAt
ik.ChainRoot = upperTorso
ik.EndEffector = head
ik.Target = target
ik.Weight = 0.6
ik.SmoothTime = 0.1
ik.Parent = humanoid

RunService.RenderStepped:Connect(function()
	local camera = Workspace.CurrentCamera
	if camera then
		target.WorldPosition = head.Position + camera.CFrame.LookVector * 20
	end
end)

humanoid.Died:Once(function()
	ik:Destroy()
	target:Destroy()
end)
```

⚠️ verify: whether an IKControl created on the client is visible to other players (IK is solved locally per client; for others to see head-look, create the IKControl on the server and replicate a target position/attribute at a low rate, e.g. 10 Hz).

## Procedural animation (springs)

```lua
--!strict
-- ReplicatedStorage/Shared/Animation/Spring.luau
-- Critically-damped-ish spring for numbers/Vector3 (viewmodel sway, UI bobbing, camera lag).
export type Spring = {
	position: Vector3,
	velocity: Vector3,
	target: Vector3,
	speed: number, -- angular frequency (rad/s), 10-20 snappy, 4-8 floaty
	damping: number, -- 1 = critical, <1 bouncy
}

local Spring = {}

function Spring.new(initial: Vector3, speed: number?, damping: number?): Spring
	return { position = initial, velocity = Vector3.zero, target = initial, speed = speed or 12, damping = damping or 1 }
end

function Spring.step(s: Spring, dt: number): Vector3
	-- semi-implicit Euler, sub-stepped for stability at low FPS
	local steps = math.max(1, math.ceil(dt / (1 / 120)))
	local h = dt / steps
	for _ = 1, steps do
		local accel = (s.target - s.position) * (s.speed * s.speed) - s.velocity * (2 * s.damping * s.speed)
		s.velocity += accel * h
		s.position += s.velocity * h
	end
	return s.position
end

return Spring
```

Use cases: first-person viewmodel sway (spring on camera rotation delta), pet follow (spring position toward an offset behind the player — far cheaper than pathfinding), hover/bob on pickups (`math.sin(os.clock()*2)*0.5`), squash-and-stretch on landing (tween `Size` of a mesh or bone scale). Write to `Motor6D.Transform` in `RunService.Stepped`/`PreSimulation` to layer on top of animations without fighting the Animator, or use `CFrame:Lerp(goal, 1 - math.exp(-k*dt))` for frame-rate-independent smoothing.

## Custom rigs (non-humanoid)
- **Motor6D rigs** (part-based): model parts, connect with `Motor6D` (Part0 = parent, Part1 = child, C0/C1 offsets), a root part (anchored or welded), `AnimationController` + `Animator`. Build/rig with Studio's **Rig Builder** or a plugin, animate in the Animation Editor.
- **Skinned meshes (Bones)**: rig + skin in Blender, import FBX; Bones appear under the MeshPart; animate in the Animation Editor; ≤ 4 bone influences per vertex, no influence on the root bone, bones at rest with scale 1 / rotation 0. Cheaper visually for organic creatures (one mesh) — see [[Blender-To-Roblox-Pipeline]].
- NPC crowds: animate with `AnimationController` (no Humanoid) on the server, or play animations purely client-side on client-spawned visual models for 50+ NPCs. `Animator.EvaluationThrottled` indicates engine LOD throttling of distant animations.

## Checklist
- [ ] Rig type chosen and locked in avatar settings
- [ ] All animations owned by the game owner (group!) or permission-granted
- [ ] One cached track per animation per Animator
- [ ] Priorities set (attacks ≥ Action) and only relevant joints keyed
- [ ] Markers drive SFX/VFX; server validates hits independently
- [ ] IK/springs run on client; NPC animations on server

## Pitfalls
- Publishing an animation to your personal account for a group game → animation doesn't play for anyone in live servers.
- Calling `LoadAnimation` every time an attack plays → track buildup and memory growth (Roblox warns at high track counts).
- Animation keyed on every joint at Action priority → overrides walking legs; keep attack anims upper-body only.
- Creating the `Animator` on the client for an NPC → nobody else sees it.
- Animations exported with leaf bones/scaled armatures from Blender → twisted limbs.
- Using `Humanoid:LoadAnimation` (deprecated) — use `Animator:LoadAnimation`.

## Related
- [[Visuals/_Index]] · [[Blender-To-Roblox-Pipeline]] · [[VFX-Particles-Beams-Trails]] · [[UI-Polish-And-Juice]] · [[Sound-Design]] · [[Anti-Exploit-And-Server-Authority]] · [[Remotes-And-Networking]]

## Sources
- Animator API (replication rules, LoadAnimation warning) — https://create.roblox.com/docs/reference/engine/classes/Animator
- AnimationTrack API (Play/Stop/AdjustWeight defaults, Priority order, SetParameter) — https://create.roblox.com/docs/reference/engine/classes/AnimationTrack
- Inverse kinematics / IKControl (required properties, constraints) — https://create.roblox.com/docs/animation/inverse-kinematics ; https://create.roblox.com/docs/reference/engine/classes/IKControl
- Animation Editor (30 fps, publish to group) — https://create.roblox.com/docs/animation/editor ; Animation events — https://create.roblox.com/docs/animation/events
- Animation Graph Editor (AnimationGraphDefinition, SetParameter, AuthorityMode replication) — https://create.roblox.com/docs/animation/graph-editor
- Rigging specs (4 influences, root) — https://create.roblox.com/docs/art/modeling/specifications
- Asset permissions for animations — https://create.roblox.com/docs/projects/assets/privacy
- All checked via Roblox/creator-docs GitHub source (2026-10-02 commit) on 2026-10-04.
