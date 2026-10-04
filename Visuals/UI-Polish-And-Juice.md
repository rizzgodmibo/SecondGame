---
tags: [visuals/ui, visuals/feel]
status: draft
updated: 2026-10-04
confidence: medium
---
# UI Polish and Juice

"Juice" = immediate, exaggerated, multi-sensory feedback (motion + sound + particles + camera) for every player action. It is the cheapest way to make a simulator/tycoon/obby feel premium and directly drives session length and purchase confidence.

## TL;DR
- **Every button**: hover scale 1.05–1.08 (0.12 s, Quad Out), press scale 0.90–0.94 (0.06 s), release overshoot back to 1 (0.25 s, Back Out), click sound. Use a `UIScale` child — never tween `Size` (breaks layouts).
- **Easing defaults**: UI enter = `Back`/`Out` 0.25–0.35 s; UI exit = `Quad`/`In` 0.15–0.2 s; colour/transparency = `Sine`/`Out` 0.2 s; numbers = `Quart`/`Out` 0.6–1.2 s. Exits faster than entrances.
- **Rewards**: count-up numbers + popup scaling from 0 → 1.15 → 1 + particle burst + rising pitch "coin" sound. Big rewards add camera FOV kick (+6–10°, 0.08 s in, 0.35 s out) and small screen shake.
- **Pair every visual with a sound**, and vary pitch ±5–10% on repeated sounds to avoid fatigue.
- Respect `GuiService.ReducedMotionEnabled`: replace movement/scale/shake with fades.
- Style: `UICorner` (8–16 px or `UDim.new(0.25,0)`), `UIStroke` (2–3 px, darker shade of fill), `UIGradient` (top-light to bottom-dark, 15–25% value difference) — the "Roblox simulator" look in 3 instances.

## TweenService defaults

```lua
--!strict
-- ReplicatedStorage/Shared/UI/Motion.luau — shared TweenInfo presets so the whole game feels consistent
local GuiService = game:GetService("GuiService")

local Motion = {}

local function info(time: number, style: Enum.EasingStyle, direction: Enum.EasingDirection): TweenInfo
	if GuiService.ReducedMotionEnabled then
		time = 0
	end
	return TweenInfo.new(time, style, direction)
end

function Motion.hover(): TweenInfo return info(0.12, Enum.EasingStyle.Quad, Enum.EasingDirection.Out) end
function Motion.press(): TweenInfo return info(0.06, Enum.EasingStyle.Quad, Enum.EasingDirection.Out) end
function Motion.release(): TweenInfo return info(0.25, Enum.EasingStyle.Back, Enum.EasingDirection.Out) end
function Motion.enter(): TweenInfo return info(0.3, Enum.EasingStyle.Back, Enum.EasingDirection.Out) end
function Motion.exit(): TweenInfo return info(0.18, Enum.EasingStyle.Quad, Enum.EasingDirection.In) end
function Motion.fade(): TweenInfo return info(0.2, Enum.EasingStyle.Sine, Enum.EasingDirection.Out) end
function Motion.countUp(): TweenInfo return info(0.9, Enum.EasingStyle.Quart, Enum.EasingDirection.Out) end

return Motion
```

Easing cheat sheet: `Back` = overshoot (playful, buttons/popups); `Elastic` = wobbly (use sparingly, big rewards only); `Bounce` = landing (drop-in banners); `Quad/Cubic/Quart/Quint` = increasingly snappy; `Sine` = gentle (pulses, idle bobbing); `Linear` = only for rotation loops and progress bars driven by time.

## Reusable button-juice module

```lua
--!strict
-- ReplicatedStorage/Shared/UI/ButtonJuice.luau
-- Usage (LocalScript): local cleanup = ButtonJuice.attach(myButton, { clickSound = sounds.Click })
local SoundService = game:GetService("SoundService")
local TweenService = game:GetService("TweenService")

local Motion = require(script.Parent.Motion)

export type Options = {
	hoverScale: number?, -- default 1.06
	pressScale: number?, -- default 0.92
	hoverSound: Sound?,
	clickSound: Sound?,
	pitchJitter: number?, -- default 0.06 (±6%)
}

local ButtonJuice = {}
local rng = Random.new()

local function playSound(template: Sound?, jitter: number)
	if not template then
		return
	end
	local sound = template:Clone()
	sound.PlaybackSpeed = template.PlaybackSpeed * (1 + rng:NextNumber(-jitter, jitter))
	sound.Parent = SoundService
	sound:Play()
	sound.Ended:Once(function()
		sound:Destroy()
	end)
end

function ButtonJuice.attach(button: GuiButton, options: Options?): () -> ()
	local opts: Options = options or {}
	local hoverScale = opts.hoverScale or 1.06
	local pressScale = opts.pressScale or 0.92
	local jitter = opts.pitchJitter or 0.06

	local scale = button:FindFirstChildOfClass("UIScale")
	if not scale then
		local created = Instance.new("UIScale")
		created.Name = "JuiceScale"
		created.Parent = button
		scale = created
	end
	local uiScale = scale :: UIScale

	local hovered = false
	local pressed = false
	local current: Tween? = nil

	local function to(target: number, tweenInfo: TweenInfo)
		if current then
			current:Cancel()
		end
		local tween = TweenService:Create(uiScale, tweenInfo, { Scale = target })
		current = tween
		tween:Play()
	end

	local function restingScale(): number
		return if hovered then hoverScale else 1
	end

	local connections: { RBXScriptConnection } = {}
	local function on(signal: RBXScriptSignal, fn: (...any) -> ())
		table.insert(connections, signal:Connect(fn))
	end

	on(button.MouseEnter, function()
		hovered = true
		if not pressed then
			to(hoverScale, Motion.hover())
			playSound(opts.hoverSound, jitter)
		end
	end)
	on(button.MouseLeave, function()
		hovered = false
		pressed = false
		to(1, Motion.hover())
	end)
	-- Gamepad selection behaves like hover
	on(button.SelectionGained, function()
		hovered = true
		to(hoverScale, Motion.hover())
	end)
	on(button.SelectionLost, function()
		hovered = false
		to(1, Motion.hover())
	end)
	on(button.InputBegan, function(input: InputObject)
		local t = input.UserInputType
		if t == Enum.UserInputType.MouseButton1 or t == Enum.UserInputType.Touch then
			pressed = true
			to(pressScale, Motion.press())
		end
	end)
	on(button.InputEnded, function(input: InputObject)
		local t = input.UserInputType
		if t == Enum.UserInputType.MouseButton1 or t == Enum.UserInputType.Touch then
			pressed = false
			to(restingScale(), Motion.release())
		end
	end)
	on(button.Activated, function()
		playSound(opts.clickSound, jitter)
		if not pressed then
			-- gamepad / keyboard activation: quick punch
			uiScale.Scale = pressScale
			to(restingScale(), Motion.release())
		end
	end)

	return function()
		for _, connection in connections do
			connection:Disconnect()
		end
		table.clear(connections)
		if current then
			current:Cancel()
		end
		uiScale.Scale = 1
	end
end

return ButtonJuice
```

Notes: keep `AutoButtonColor = false` on juiced buttons (the default darkening fights your styling); add a darker `UIGradient`/colour swap on press if you want colour feedback. Disable a button during a server request (`button.Interactable = false`) and show a spinner — prevents double purchases.

## Number count-up

```lua
--!strict
-- ReplicatedStorage/Shared/UI/CountUp.luau
local TweenService = game:GetService("TweenService")
local Motion = require(script.Parent.Motion)

local function abbreviate(n: number): string
	local suffixes = { "", "K", "M", "B", "T", "Qa", "Qi" }
	local i = 1
	while math.abs(n) >= 1000 and i < #suffixes do
		n /= 1000
		i += 1
	end
	return if i == 1 then string.format("%d", n) else string.format("%.1f%s", n, suffixes[i])
end

-- Tweens label text from `from` to `to`. Returns the Tween so callers can :Cancel().
return function(label: TextLabel, from: number, to: number): Tween
	local holder = Instance.new("NumberValue")
	holder.Value = from
	local conn = holder.Changed:Connect(function(v: number)
		label.Text = abbreviate(math.floor(v + 0.5))
	end)
	local tween = TweenService:Create(holder, Motion.countUp(), { Value = to })
	tween.Completed:Once(function()
		conn:Disconnect()
		label.Text = abbreviate(to)
		holder:Destroy()
	end)
	tween:Play()
	return tween
end
```

Pair with: label `UIScale` punch to 1.2 on start, tick sound every ~0.05 s with rising pitch (cap 1.5×), final "ding".

## Reward popup recipe (in order, total ≤ 1.2 s)
1. Dim background (Frame, transparency 1 → 0.5, `Motion.fade`).
2. Card `UIScale` 0 → 1 with `Back Out` 0.3 s; rotate −8° → 0° simultaneously.
3. At 0.15 s: burst of 20–40 UI "sparkle" ImageLabels or a 3D `ParticleEmitter:Emit(30)` at the character (see [[VFX-Particles-Beams-Trails]]).
4. Count-up the amount (0.6–0.9 s); currency icon flies to the HUD counter (tween Position to the counter's `AbsolutePosition`) and the HUD counter punches 1 → 1.2 → 1.
5. Sound stack: whoosh (open) → sparkle (burst) → ticks → ding (end). Auto-dismiss after 2 s or on tap.

## Screen shake and FOV kick

```lua
--!strict
-- StarterPlayerScripts/CameraJuice.luau (ModuleScript required by client code)
local RunService = game:GetService("RunService")
local TweenService = game:GetService("TweenService")
local GuiService = game:GetService("GuiService")
local Workspace = game:GetService("Workspace")

local CameraJuice = {}
local trauma = 0 -- 0..1, shake magnitude = trauma^2
local MAX_ANGLE = math.rad(2.5)
local MAX_OFFSET = 0.35 -- studs
local DECAY = 1.6 -- trauma per second
local seed = math.random() * 1000

RunService:BindToRenderStep("CameraJuiceShake", Enum.RenderPriority.Camera.Value + 1, function(dt: number)
	if trauma <= 0 then
		return
	end
	trauma = math.max(0, trauma - DECAY * dt)
	local camera = Workspace.CurrentCamera
	if not camera then
		return
	end
	local shake = trauma * trauma
	local t = os.clock() * 25
	local function n(o: number): number
		return math.noise(seed + o, t)
	end
	camera.CFrame *= CFrame.new(n(1) * MAX_OFFSET * shake, n(2) * MAX_OFFSET * shake, 0)
		* CFrame.Angles(n(3) * MAX_ANGLE * shake, n(4) * MAX_ANGLE * shake, n(5) * MAX_ANGLE * shake)
end)

function CameraJuice.shake(amount: number) -- 0.2 hit, 0.4 explosion, 0.7 boss slam
	if GuiService.ReducedMotionEnabled then
		return
	end
	trauma = math.clamp(trauma + amount, 0, 1)
end

function CameraJuice.fovKick(extra: number?) -- default +8 degrees
	local camera = Workspace.CurrentCamera
	if not camera or GuiService.ReducedMotionEnabled then
		return
	end
	local base = 70 -- keep in sync with your camera's default FOV
	local up = TweenService:Create(camera, TweenInfo.new(0.08, Enum.EasingStyle.Quad, Enum.EasingDirection.Out), { FieldOfView = base + (extra or 8) })
	up.Completed:Once(function()
		TweenService:Create(camera, TweenInfo.new(0.35, Enum.EasingStyle.Quad, Enum.EasingDirection.Out), { FieldOfView = base }):Play()
	end)
	up:Play()
end

return CameraJuice
```

Shake is applied after the default camera (priority Camera+1) and re-derived each frame, so it never accumulates drift. Keep shake < 0.3 trauma for frequent events; players on mobile get motion-sick faster.

## Styling recipe (simulator-style button)
- Frame/ImageButton fill: saturated mid-tone (e.g. `#3BD16F`).
- `UICorner.CornerRadius = UDim.new(0, 12)` (or `UDim.new(0.3, 0)` for pills).
- `UIStroke`: Thickness 3, Color = fill darkened ~40%, `ApplyStrokeMode = Border` for the frame; separate `UIStroke` on the text label (Thickness 2, black, Transparency 0.2) for legibility. `StrokeSizingMode`: `FixedSize` = Thickness in pixels (then scaled by UIScale); `ScaledSize` = Thickness relative to the parent's min width/height (or font size for text) — use ScaledSize for strokes that must stay proportional on Scale-sized elements.
- `UIGradient`: `Rotation = 90`, Color top white → bottom light grey (the gradient multiplies the fill), gives a bevel. Animate `Offset` for a shine sweep on premium buttons.
- `UIShadow` (BlurRadius, Offset, Spread) exists for drop shadows; otherwise a 9-slice shadow ImageLabel behind.
- Idle attention pulse on "Free reward" buttons: UIScale 1 ↔ 1.05, `Sine InOut`, 0.8 s, `RepeatCount = -1`, `Reverses = true`. Max one pulsing element per screen.

## Checklist
- [ ] All buttons use `ButtonJuice.attach` (or equivalent) with click sound
- [ ] Shared `Motion` presets; no ad-hoc TweenInfo numbers in screens
- [ ] Currency changes animate (count-up + HUD punch)
- [ ] Big moments: particles + sound + FOV kick + light shake
- [ ] ReducedMotion path tested (no movement, fades only)
- [ ] Buttons disabled while awaiting server response

## Pitfalls
- Tweening `Size`/`Position` of items inside `UIListLayout` → layout fights the tween; tween `UIScale` or an inner frame instead.
- Creating a new Tween every frame / not cancelling the previous one → jitter.
- Shake on every hit in a combat game → nausea; scale trauma by damage and cap.
- Loud click sounds: UI SFX should sit ~6–10 dB below music peak (see [[Sound-Design]]).
- Too much juice on low-value actions dilutes big moments — scale feedback to reward size (small/medium/large tiers).

## Related
- [[Visuals/_Index]] · [[UI-Architecture]] · [[UI-Layout-And-Device-Scaling]] · [[VFX-Particles-Beams-Trails]] · [[Sound-Design]] · [[Animation-Rigging-And-IK]] · [[X-Animated-UI-Lessons-And-Tools]] (real designer examples of spring press, shine sweep, odometer counters and reveals) · [[X-Reference-Library]]

## Sources
- UI animation / tweening — https://create.roblox.com/docs/ui/animation
- Appearance modifiers (UIGradient, UIStroke, UICorner, UIShadow) — https://create.roblox.com/docs/ui/appearance-modifiers
- Reduced motion guidance — https://create.roblox.com/docs/production/publishing/accessibility#reduced-motion
- API: TweenService, EasingStyle, UIStroke (StrokeSizingMode, ApplyStrokeMode), UIShadow, GuiButton — https://create.roblox.com/docs/reference/engine/classes/UIStroke (checked via Roblox/creator-docs GitHub source, 2026-10-02 commit)
- Trauma-based shake technique: Squirrel Eiserloh, "Math for Game Programmers: Juicing Your Cameras With Math", GDC 2016 — https://www.youtube.com/watch?v=tu-Qe66AvtY
