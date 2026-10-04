--!strict
--[[
	HoardVFX — client-side visuals for the Dragon's Hoard set.
	Location: ReplicatedStorage.HoardVFX (ModuleScript). Require it from LocalScripts only.
	Visual only: no pickup or interaction logic. Your server fires a RemoteEvent, clients call these.

	API
		HoardVFX.enable(target, preset)        preset: "Ember" | "Frost" | "Venom" | "Sparkle" | "Blade" | "Pickup"
		HoardVFX.disable(target, preset?)      one preset, or everything (incl. pickup idle) when preset is nil
		HoardVFX.enableDefault(target)         uses the "HoardVFXPreset" attribute HoardSetup put on the part
		HoardVFX.enableAllIn(container)        enableDefault on every tagged part under container
		HoardVFX.setPickupIdle(target, on, opts?)   slow bob + spin + shine (anchored items only)
		HoardVFX.openChest(chest, instant?) / HoardVFX.closeChest(chest, instant?) / HoardVFX.isChestOpen(chest)
		HoardVFX.placeSword(sword, pile, opts?)     stands the sword in CoinPile_Large's SwordSocket

	target = the item's Model (with PrimaryPart) or its MeshPart. Use one or the other per item, not both.
	Everything created is named "HoardVFX_*" and is removed by disable() or when the target is destroyed.
]]

local RunService = game:GetService("RunService")
local TweenService = game:GetService("TweenService")

export type Target = Model | BasePart
export type IdleOptions = {
	amplitude: number?, -- bob height in studs (default 0.2)
	period: number?, -- seconds per bob (default 2.4)
	spinSpeed: number?, -- radians per second (default 1.2)
	lift: number?, -- extra height above the resting pivot (default 0.35)
	shine: boolean?, -- sparkle + soft light (default true)
}
export type SwordOptions = {
	depth: number?, -- how far the tip sinks into the pile (default 0.9)
	tilt: number?, -- lean in degrees (default 8)
	yaw: number?, -- turn in degrees (default 0)
}

local HoardVFX = {}

-- Paste the Image asset ids after uploading the PNGs in vfx/ (e.g. "rbxassetid://1234567890").
-- Left empty, a built-in Roblox particle texture is used so everything still works while testing.
HoardVFX.Textures = {
	Sparkle = "",
	Ember = "",
	FrostFlake = "",
	Bubble = "",
	Glow = "",
	CoinGlint = "",
	Shine = "",
} :: { [string]: string }

-- Eggs pulse with a Highlight as well as a light. Roblox allows up to 255 Highlights per client, but each one
-- is an extra render pass, so turn this off if you place lots of eggs (aim for 10 or fewer on mobile).
HoardVFX.UseHighlightGlow = true

local FALLBACK: { [string]: string } = {
	Sparkle = "rbxasset://textures/particles/sparkles_main.dds",
	Ember = "rbxasset://textures/particles/fire_main.dds",
	FrostFlake = "rbxasset://textures/particles/sparkles_main.dds",
	Bubble = "rbxasset://textures/particles/smoke_main.dds",
	Glow = "rbxasset://textures/particles/smoke_main.dds",
	CoinGlint = "rbxasset://textures/particles/sparkles_main.dds",
	Shine = "rbxasset://textures/particles/sparkles_main.dds",
}

local EGG_COLOURS: { [string]: Color3 } = {
	Ember = Color3.fromRGB(255, 120, 40),
	Frost = Color3.fromRGB(130, 205, 255),
	Venom = Color3.fromRGB(130, 255, 90),
}
local GOLD = Color3.fromRGB(255, 214, 110)
local WARM_WHITE = Color3.fromRGB(255, 250, 225)
local PREFIX = "HoardVFX_"
local SWORD_LENGTH = 4.44 -- Sword_Ornate height in studs at import scale
local CHEST_OPEN_ANGLE = 105

type Entry = {
	instances: { Instance },
	tweens: { Tween },
	alive: boolean,
}

type IdleState = {
	base: CFrame,
	t: number,
	amplitude: number,
	period: number,
	spinSpeed: number,
	lift: number,
	moves: boolean,
	extras: Entry,
}

type TargetState = {
	presets: { [string]: Entry },
	idle: IdleState?,
	destroying: RBXScriptConnection?,
}

type ChestState = {
	closedOffset: CFrame,
	angle: NumberValue,
	open: boolean,
	extras: Entry?,
	angleConn: RBXScriptConnection,
}

local states: { [PVInstance]: TargetState } = {}
local chests: { [Model]: ChestState } = {}
local idleConn: RBXScriptConnection? = nil

-- ---------------------------------------------------------------- helpers

local function texture(name: string): string
	local id = HoardVFX.Textures[name]
	if id ~= nil and id ~= "" then
		return id
	end
	return FALLBACK[name]
end

local function asPart(inst: Instance?): BasePart?
	if inst == nil then
		return nil
	end
	if inst:IsA("BasePart") then
		return inst
	end
	if inst:IsA("Model") then
		return inst.PrimaryPart or inst:FindFirstChildWhichIsA("BasePart", true)
	end
	return nil
end

local function ns(points: { { number } }): NumberSequence
	local keys = {}
	for _, p in points do
		table.insert(keys, NumberSequenceKeypoint.new(p[1], p[2]))
	end
	return NumberSequence.new(keys)
end

local function maxDim(part: BasePart): number
	return math.max(part.Size.X, part.Size.Y, part.Size.Z)
end

local function newEntry(): Entry
	return { instances = {}, tweens = {}, alive = true }
end

local function stopEntry(entry: Entry)
	entry.alive = false
	for _, tween in entry.tweens do
		tween:Cancel()
	end
	for _, inst in entry.instances do
		inst:Destroy()
	end
	table.clear(entry.tweens)
	table.clear(entry.instances)
end

local function own(entry: Entry, inst: Instance, parent: Instance)
	inst.Parent = parent
	table.insert(entry.instances, inst)
end

local function loopTween(entry: Entry, inst: Instance, info: TweenInfo, goal: { [string]: any })
	local tween = TweenService:Create(inst, info, goal)
	table.insert(entry.tweens, tween)
	tween:Play()
end

local function newEmitter(name: string, tex: string): ParticleEmitter
	local e = Instance.new("ParticleEmitter")
	e.Name = PREFIX .. name
	e.Texture = texture(tex)
	e.LightEmission = 1
	e.Shape = Enum.ParticleEmitterShape.Sphere
	e.ShapeStyle = Enum.ParticleEmitterShapeStyle.Volume
	e.Transparency = NumberSequence.new(0)
	return e
end

local function newLight(name: string, colour: Color3, range: number, brightness: number): PointLight
	local light = Instance.new("PointLight")
	light.Name = PREFIX .. name
	light.Color = colour
	light.Range = range
	light.Brightness = brightness
	light.Shadows = false
	return light
end

local function getState(target: Target): TargetState
	local existing = states[target]
	if existing then
		return existing
	end
	local state: TargetState = { presets = {}, idle = nil, destroying = nil }
	state.destroying = target.Destroying:Connect(function()
		HoardVFX.disable(target)
	end)
	states[target] = state
	return state
end

local function releaseIfEmpty(target: PVInstance)
	local state = states[target]
	if state and next(state.presets) == nil and state.idle == nil then
		if state.destroying then
			state.destroying:Disconnect()
		end
		states[target] = nil
	end
end

-- ---------------------------------------------------------------- presets

local function sparkleEmitter(part: BasePart, rateScale: number): ParticleEmitter
	local size = math.clamp(maxDim(part) * 0.14, 0.12, 0.6)
	local e = newEmitter("Sparkle", "Sparkle")
	e.Color = ColorSequence.new(WARM_WHITE, GOLD)
	e.Size = ns({ { 0, 0 }, { 0.35, size }, { 1, 0 } })
	e.Lifetime = NumberRange.new(0.35, 0.6)
	e.Rate = math.clamp(part.Size.X * part.Size.Z * 0.6, 0.5, 4) * rateScale
	e.Speed = NumberRange.new(0)
	e.Rotation = NumberRange.new(0, 90)
	e.ZOffset = 0.4 -- pull twinkles in front of the surface they spawn under
	e.LockedToPart = true
	return e
end

local function buildEgg(entry: Entry, part: BasePart, target: Target, kind: string)
	local colour = EGG_COLOURS[kind]
	local k = part.Size.Y / 1.6
	local pulse = TweenInfo.new(1.6, Enum.EasingStyle.Sine, Enum.EasingDirection.InOut, -1, true)

	local light = newLight("Glow", colour, 6 * k, 0.4)
	own(entry, light, part)
	loopTween(entry, light, pulse, { Brightness = 1.8 })

	if HoardVFX.UseHighlightGlow then
		local hl = Instance.new("Highlight")
		hl.Name = PREFIX .. "Pulse"
		hl.Adornee = target
		hl.FillColor = colour
		hl.FillTransparency = 0.92
		hl.OutlineTransparency = 1
		hl.DepthMode = Enum.HighlightDepthMode.Occluded
		own(entry, hl, part)
		loopTween(entry, hl, pulse, { FillTransparency = 0.7 })
	end

	local e: ParticleEmitter
	if kind == "Ember" then
		e = newEmitter("Embers", "Ember")
		e.Color = ColorSequence.new(Color3.fromRGB(255, 210, 90), Color3.fromRGB(230, 60, 20))
		e.Size = ns({ { 0, 0.11 * k }, { 1, 0.02 * k } })
		e.Lifetime = NumberRange.new(1, 1.8)
		e.Rate = 5
		e.Speed = NumberRange.new(0.5 * k, 1.1 * k)
		e.Acceleration = Vector3.new(0, 1.2 * k, 0)
		e.Drag = 1
		e.SpreadAngle = Vector2.new(25, 25)
		e.Transparency = ns({ { 0, 0 }, { 0.7, 0.2 }, { 1, 1 } })
	elseif kind == "Frost" then
		e = newEmitter("FrostFlakes", "FrostFlake")
		e.Color = ColorSequence.new(Color3.fromRGB(255, 255, 255), Color3.fromRGB(160, 215, 255))
		e.Size = ns({ { 0, 0 }, { 0.2, 0.14 * k }, { 1, 0.08 * k } })
		e.Lifetime = NumberRange.new(2, 3)
		e.Rate = 3
		e.Speed = NumberRange.new(0.15 * k, 0.35 * k)
		e.Acceleration = Vector3.new(0, -0.3 * k, 0)
		e.Rotation = NumberRange.new(0, 360)
		e.RotSpeed = NumberRange.new(-60, 60)
		e.LightEmission = 0.6
		e.Transparency = ns({ { 0, 0.1 }, { 0.75, 0.3 }, { 1, 1 } })
	else
		e = newEmitter("Bubbles", "Bubble")
		e.Color = ColorSequence.new(Color3.fromRGB(190, 255, 120), Color3.fromRGB(110, 230, 80))
		e.Size = ns({ { 0, 0.05 * k }, { 0.85, 0.15 * k }, { 1, 0 } }) -- grow, then pop
		e.Lifetime = NumberRange.new(1.2, 2)
		e.Rate = 4
		e.Speed = NumberRange.new(0.3 * k, 0.6 * k)
		e.Acceleration = Vector3.new(0, 0.6 * k, 0)
		e.LightEmission = 0.4
		e.Transparency = ns({ { 0, 0.15 }, { 1, 0.35 } })
	end
	e.ShapeStyle = Enum.ParticleEmitterShapeStyle.Surface
	own(entry, e, part)
end

local function buildSparkle(entry: Entry, part: BasePart)
	own(entry, sparkleEmitter(part, 1), part)
end

local function buildBlade(entry: Entry, part: BasePart)
	local k = part.Size.Y / SWORD_LENGTH
	local pivot = part.PivotOffset.Position -- the tip, once HoardSetup has run
	local function bladePoint(x: number, h: number): Vector3
		return pivot + Vector3.new(x * k, h * k, 0)
	end

	own(entry, newLight("BladeGlow", Color3.fromRGB(200, 225, 255), 5 * k, 0.5), part)
	local twinkle = sparkleEmitter(part, 0.3)
	twinkle.Color = ColorSequence.new(Color3.fromRGB(235, 245, 255))
	own(entry, twinkle, part)

	local a0 = Instance.new("Attachment")
	a0.Name = PREFIX .. "Shine0"
	local a1 = Instance.new("Attachment")
	a1.Name = PREFIX .. "Shine1"
	own(entry, a0, part)
	own(entry, a1, part)
	local beam = Instance.new("Beam")
	beam.Name = PREFIX .. "Shine"
	beam.Attachment0 = a0
	beam.Attachment1 = a1
	beam.FaceCamera = true
	beam.Texture = texture("Shine")
	beam.TextureMode = Enum.TextureMode.Stretch
	beam.LightEmission = 1
	beam.Segments = 1
	beam.ZOffset = 0.05
	beam.Width0 = 0
	beam.Width1 = 0
	beam.Color = ColorSequence.new(Color3.fromRGB(240, 248, 255))
	own(entry, beam, part)

	local width = 0.3 * k
	task.spawn(function()
		while entry.alive do
			a0.Position = bladePoint(-0.24, 0.45)
			a1.Position = bladePoint(0.24, 0.45)
			local sweep = TweenInfo.new(0.8, Enum.EasingStyle.Quad, Enum.EasingDirection.InOut)
			local fade = TweenInfo.new(0.25)
			TweenService:Create(a0, sweep, { Position = bladePoint(-0.27, 3.0) }):Play()
			TweenService:Create(a1, sweep, { Position = bladePoint(0.27, 3.0) }):Play()
			TweenService:Create(beam, fade, { Width0 = width, Width1 = width }):Play()
			task.wait(0.55)
			if not entry.alive then
				break
			end
			TweenService:Create(beam, fade, { Width0 = 0, Width1 = 0 }):Play()
			task.wait(2.8)
		end
	end)
end

local BUILDERS: { [string]: (Entry, BasePart, Target) -> () } = {
	Ember = function(entry, part, target)
		buildEgg(entry, part, target, "Ember")
	end,
	Frost = function(entry, part, target)
		buildEgg(entry, part, target, "Frost")
	end,
	Venom = function(entry, part, target)
		buildEgg(entry, part, target, "Venom")
	end,
	Sparkle = function(entry, part)
		buildSparkle(entry, part)
	end,
	Blade = function(entry, part)
		buildBlade(entry, part)
	end,
}

-- ---------------------------------------------------------------- pickup idle

local function idleStep(dt: number)
	for target, state in states do
		local idle = state.idle
		if idle and idle.moves then
			idle.t += dt
			local bob = idle.lift + math.sin(idle.t * 2 * math.pi / idle.period) * idle.amplitude
			target:PivotTo(idle.base * CFrame.new(0, bob, 0) * CFrame.Angles(0, idle.t * idle.spinSpeed, 0))
		end
	end
end

local function refreshIdleLoop()
	local any = false
	for _, state in states do
		if state.idle then
			any = true
			break
		end
	end
	if any and idleConn == nil then
		idleConn = RunService.Heartbeat:Connect(idleStep)
	elseif not any and idleConn then
		idleConn:Disconnect()
		idleConn = nil
	end
end

function HoardVFX.setPickupIdle(target: Target, on: boolean, opts: IdleOptions?)
	local part = asPart(target)
	if part == nil then
		warn("[HoardVFX] setPickupIdle: no part in", target:GetFullName())
		return
	end
	local state = getState(target)
	local idle = state.idle
	if not on then
		if idle then
			stopEntry(idle.extras)
			if idle.moves then
				target:PivotTo(idle.base)
			end
			state.idle = nil
		end
		refreshIdleLoop()
		releaseIfEmpty(target)
		return
	end
	if idle then
		return
	end
	local o: IdleOptions = opts or {}
	local moves = part.Anchored
	if not moves then
		warn("[HoardVFX] pickup idle only bobs anchored items; adding shine only for", target:GetFullName())
	end
	local extras = newEntry()
	if o.shine ~= false then
		own(extras, sparkleEmitter(part, 1.5), part)
		own(extras, newLight("PickupGlow", WARM_WHITE, 4, 0.8), part)
	end
	state.idle = {
		base = target:GetPivot(),
		t = 0,
		amplitude = o.amplitude or 0.2,
		period = o.period or 2.4,
		spinSpeed = o.spinSpeed or 1.2,
		lift = o.lift or 0.35,
		moves = moves,
		extras = extras,
	}
	refreshIdleLoop()
end

-- ---------------------------------------------------------------- enable / disable

function HoardVFX.enable(target: Target, preset: string)
	if preset == "Pickup" then
		HoardVFX.setPickupIdle(target, true)
		return
	end
	local builder = BUILDERS[preset]
	if builder == nil then
		warn("[HoardVFX] unknown preset", preset)
		return
	end
	local part = asPart(target)
	if part == nil then
		warn("[HoardVFX] enable: no part in", target:GetFullName())
		return
	end
	local state = getState(target)
	if state.presets[preset] then
		return
	end
	local entry = newEntry()
	state.presets[preset] = entry
	builder(entry, part, target)
end

function HoardVFX.disable(target: Target, preset: string?)
	local state = states[target]
	if state == nil then
		return
	end
	if preset == "Pickup" then
		HoardVFX.setPickupIdle(target, false)
		return
	end
	for name, entry in state.presets do
		if preset == nil or name == preset then
			stopEntry(entry)
			state.presets[name] = nil
		end
	end
	if preset == nil and state.idle then
		HoardVFX.setPickupIdle(target, false)
	end
	releaseIfEmpty(target)
end

function HoardVFX.enableDefault(target: Target)
	local part = asPart(target)
	local preset = part and part:GetAttribute("HoardVFXPreset")
	if typeof(preset) == "string" and preset ~= "" then
		HoardVFX.enable(target, preset)
	end
end

function HoardVFX.enableAllIn(container: Instance)
	for _, inst in container:GetDescendants() do
		if inst:IsA("BasePart") and inst:GetAttribute("HoardVFXPreset") ~= nil then
			HoardVFX.enableDefault(inst)
		end
	end
end

-- ---------------------------------------------------------------- chest

local function chestParts(chest: Model): (BasePart?, PVInstance?, Attachment?)
	local base = asPart(chest:FindFirstChild("Chest_Base", true))
	local lidInst = chest:FindFirstChild("Chest_Lid", true)
	local lid: PVInstance? = if lidInst and lidInst:IsA("PVInstance") then lidInst else nil
	local hinge = base and base:FindFirstChild("LidHinge")
	return base, lid, if hinge and hinge:IsA("Attachment") then hinge else nil
end

local function chestState(chest: Model, lid: PVInstance, hinge: Attachment): ChestState
	local existing = chests[chest]
	if existing then
		return existing
	end
	local angle = Instance.new("NumberValue")
	local closedOffset = hinge.WorldCFrame:ToObjectSpace(lid:GetPivot())
	local state: ChestState
	state = {
		closedOffset = closedOffset,
		angle = angle,
		open = false,
		extras = nil,
		angleConn = angle.Changed:Connect(function(value: number)
			lid:PivotTo(hinge.WorldCFrame * CFrame.Angles(math.rad(value), 0, 0) * state.closedOffset)
		end),
	}
	chests[chest] = state
	chest.Destroying:Once(function()
		state.angleConn:Disconnect()
		if state.extras then
			stopEntry(state.extras)
		end
		angle:Destroy()
		chests[chest] = nil
	end)
	return state
end

local function chestBurst(base: BasePart): Entry
	local entry = newEntry()
	local k = base.Size.X / 3.06
	local mouth = Instance.new("Attachment")
	mouth.Name = PREFIX .. "ChestMouth"
	mouth.Position = Vector3.new(0, base.Size.Y * 0.24, 0)
	own(entry, mouth, base)

	local light = newLight("ChestLight", GOLD, 12 * k, 0)
	own(entry, light, mouth)
	local flash = TweenService:Create(light, TweenInfo.new(0.15, Enum.EasingStyle.Quad), { Brightness = 5 })
	local settle = TweenService:Create(light, TweenInfo.new(1.2, Enum.EasingStyle.Quad), { Brightness = 1.2 })
	table.insert(entry.tweens, flash)
	table.insert(entry.tweens, settle)
	flash.Completed:Once(function(state)
		if state == Enum.PlaybackState.Completed then
			settle:Play()
		end
	end)
	flash:Play()

	local glow = newEmitter("ChestFlash", "Glow")
	glow.Enabled = false
	glow.Color = ColorSequence.new(GOLD)
	glow.Size = ns({ { 0, 1.5 * k }, { 1, 6 * k } })
	glow.Lifetime = NumberRange.new(0.5)
	glow.Speed = NumberRange.new(0)
	glow.Transparency = ns({ { 0, 0.3 }, { 1, 1 } })
	own(entry, glow, mouth)

	local coins = newEmitter("CoinBurst", "CoinGlint")
	coins.Enabled = false
	coins.Color = ColorSequence.new(GOLD)
	coins.LightEmission = 0.5
	coins.Size = NumberSequence.new(0.22 * k)
	coins.Lifetime = NumberRange.new(1, 1.6)
	coins.Speed = NumberRange.new(6 * k, 10 * k)
	coins.SpreadAngle = Vector2.new(30, 30)
	coins.EmissionDirection = Enum.NormalId.Top
	coins.Acceleration = Vector3.new(0, -18 * k, 0)
	coins.Rotation = NumberRange.new(0, 360)
	coins.RotSpeed = NumberRange.new(-300, 300)
	coins.Transparency = ns({ { 0, 0 }, { 0.8, 0 }, { 1, 1 } })
	own(entry, coins, mouth)

	local sparks = newEmitter("SparkBurst", "Sparkle")
	sparks.Enabled = false
	sparks.Color = ColorSequence.new(WARM_WHITE, GOLD)
	sparks.Size = ns({ { 0, 0 }, { 0.2, 0.4 * k }, { 1, 0 } })
	sparks.Lifetime = NumberRange.new(0.6, 1)
	sparks.Speed = NumberRange.new(3 * k, 6 * k)
	sparks.SpreadAngle = Vector2.new(50, 50)
	sparks.EmissionDirection = Enum.NormalId.Top
	sparks.Drag = 2
	own(entry, sparks, mouth)

	local shimmer = newEmitter("OpenShimmer", "Sparkle")
	shimmer.Color = ColorSequence.new(WARM_WHITE, GOLD)
	shimmer.Size = ns({ { 0, 0 }, { 0.35, 0.3 * k }, { 1, 0 } })
	shimmer.Lifetime = NumberRange.new(0.5, 0.8)
	shimmer.Rate = 3
	shimmer.Speed = NumberRange.new(0.5, 1.2)
	shimmer.SpreadAngle = Vector2.new(70, 70)
	shimmer.EmissionDirection = Enum.NormalId.Top
	own(entry, shimmer, mouth)

	glow:Emit(1)
	coins:Emit(24)
	sparks:Emit(30)
	return entry
end

function HoardVFX.openChest(chest: Model, instant: boolean?)
	local base, lid, hinge = chestParts(chest)
	if base == nil or lid == nil or hinge == nil then
		warn(
			"[HoardVFX] openChest needs Chest_Base (with a LidHinge attachment) and Chest_Lid inside",
			chest:GetFullName()
		)
		return
	end
	local state = chestState(chest, lid, hinge)
	if state.open then
		return
	end
	state.open = true
	local attr = chest:GetAttribute("OpenAngle")
	local openAngle = if typeof(attr) == "number" then attr else CHEST_OPEN_ANGLE
	if instant then
		state.angle.Value = openAngle
	else
		TweenService:Create(state.angle, TweenInfo.new(0.6, Enum.EasingStyle.Back, Enum.EasingDirection.Out), {
			Value = openAngle,
		}):Play()
	end
	if state.extras then
		stopEntry(state.extras)
	end
	if instant then
		state.extras = chestBurst(base)
	else
		state.extras = nil
		task.delay(0.12, function() -- burst once the lid has cracked open
			if state.open and state.extras == nil then
				state.extras = chestBurst(base)
			end
		end)
	end
end

function HoardVFX.closeChest(chest: Model, instant: boolean?)
	local state = chests[chest]
	if state == nil or not state.open then
		return
	end
	state.open = false
	if instant then
		state.angle.Value = 0
	else
		TweenService:Create(state.angle, TweenInfo.new(0.45, Enum.EasingStyle.Quad, Enum.EasingDirection.In), {
			Value = 0,
		}):Play()
	end
	local extras = state.extras
	state.extras = nil
	if extras then
		for _, inst in extras.instances do
			if inst:IsA("PointLight") then
				TweenService:Create(inst, TweenInfo.new(0.4), { Brightness = 0 }):Play()
			elseif inst:IsA("ParticleEmitter") then
				inst.Enabled = false
			end
		end
		task.delay(1.2, stopEntry, extras)
	end
end

function HoardVFX.isChestOpen(chest: Model): boolean
	local state = chests[chest]
	return state ~= nil and state.open
end

-- ---------------------------------------------------------------- sword placement

-- Pure CFrame placement: works from server or client (only the server's call replicates).
function HoardVFX.placeSword(sword: Target, pile: Target, opts: SwordOptions?)
	local pilePart = asPart(pile)
	local socket = pilePart and pilePart:FindFirstChild("SwordSocket")
	if socket == nil or not socket:IsA("Attachment") then
		warn("[HoardVFX] placeSword: no SwordSocket attachment in", pile:GetFullName(), "(run HoardSetup)")
		return
	end
	local o: SwordOptions = opts or {}
	local depth = o.depth or 0.9
	sword:PivotTo(
		socket.WorldCFrame
			* CFrame.Angles(0, math.rad(o.yaw or 0), 0)
			* CFrame.Angles(math.rad(o.tilt or 8), 0, 0)
			* CFrame.new(0, -depth, 0)
	)
end

return HoardVFX
