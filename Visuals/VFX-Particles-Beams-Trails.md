---
tags: [visuals/vfx]
status: draft
updated: 2026-10-04
confidence: medium
---
# VFX: Particles, Beams, Trails

Roblox VFX are built from `ParticleEmitter`, `Beam`, `Trail`, `Attachment`s, plus meshes with Neon/transparent materials, `Highlight`, lights and tweens. No custom shaders — see [[Shaders-Materials-And-Surfaces]].

## TL;DR
- **Bursts, not streams**: for hits/pickups/level-ups, keep emitters `Enabled = false` and call `emitter:Emit(n)` on the **client**. Stream emitters (`Rate`) only for ambient loops (fire, aura, portal).
- **Hard limits**: one emitter tops out at **400 particles/s (100/s on mobile)**; particle **Lifetime is capped at 20 s**. Fill-rate (screen pixels covered × overlap) is the real GPU cost — big, overlapping, transparent particles kill mobile.
- **Budget per effect**: small hit ≤ 30 particles total; big ability ≤ 150; ambient emitter Rate ≤ 20. Aim ≤ ~1,500 live particles on screen at once for mid phones (⚠️ verify on your low-end test device with MicroProfiler).
- **Play VFX on clients** (server sends a RemoteEvent with position/type) — server-created particles replicate as instances, cost bandwidth, and lag.
- Use **flipbooks** (2×2/4×4/8×8 or Custom, up to 1024×1024 sheet) for animated smoke/explosions; clients auto-disable flipbooks when low on memory.
- Beams: two Attachments + texture; `TextureSpeed` scrolls (lasers, waterfalls, conveyor glow). Trails: two Attachments on a moving part; `Lifetime` 0.15–0.4 s for weapon swings.

## ParticleEmitter key properties (verified names)

| Property | What it does | Good starting value |
|---|---|---|
| `Texture` | Image per particle (white/greyscale textures tint best via `Color`) | soft circle / spark / smoke sheet |
| `Rate` | Particles per second (stream) | 0 for burst emitters |
| `Lifetime` (NumberRange) | Seconds, max 20 | 0.3–0.8 hits, 1–3 ambient |
| `Speed` (NumberRange) | Studs/s along EmissionDirection | 8–20 bursts |
| `SpreadAngle` (Vector2) | Random cone in degrees | (180,180) for omni burst, (15,15) jets |
| `Size` / `Transparency` (NumberSequence) | Over lifetime | Size 0.5→2→0; Transparency 0→0→1 |
| `Color` (ColorSequence) | Over lifetime | hot core → cooler edge |
| `LightEmission` | 0 normal blend, 1 additive | 1 for fire/magic/sparkles, 0 for smoke/dust |
| `LightInfluence` | 0 unlit (glows at night), 1 lit | 0 for magic, 1 for smoke/dust |
| `Brightness` | Scales emitted light | 1–3 for glow with Bloom |
| `Drag` | Seconds to lose half speed | 2–6 for explosive bursts that "hang" |
| `Acceleration` (Vector3) | World-space force | (0,-30,0) debris; (0,4,0) smoke rise |
| `Rotation`/`RotSpeed` | Random start angle / spin | (0,360) / (-90,90) |
| `Squash` (NumberSequence) | Non-uniform stretch | stretch sparks |
| `Orientation` | `FacingCamera`, `FacingCameraWorldUp`, `VelocityParallel`, `VelocityPerpendicular` | `VelocityParallel` for sparks/rain streaks |
| `Shape` / `ShapeStyle` / `ShapeInOut` / `ShapePartial` | Box/Sphere/Cylinder/Disc; Volume or Surface; out/in/both; partial arc | Disc + Surface + Outward = shockwave ring |
| `EmissionDirection` | NormalId face of parent | Top |
| `LockedToPart` | Particles move rigidly with parent | true for auras on moving characters |
| `VelocityInheritance` | Inherit parent velocity 0–1 | 0.3–0.5 for thrusters |
| `ZOffset` | Render nudge toward camera | 0.5–2 to draw over the character |
| `TimeScale` | 0–1 slow-mo | hit-stop effects |
| `WindAffectsDrag` | Follows `Workspace.GlobalWind` | true for leaves/snow |
| `Flipbook*` | `FlipbookLayout`, `FlipbookMode` (Loop/OneShot/PingPong/Random), `FlipbookFramerate`, `FlipbookStartRandom`, `FlipbookSizeX/Y` (Custom) | OneShot for explosions |

Methods: `Emit(count)`, `Clear()`.

## Recipes

| Effect | Setup |
|---|---|
| **Hit spark** | 2 emitters: (a) sparks: Texture streak, Orientation VelocityParallel, Speed 20–35, Lifetime 0.15–0.3, Drag 6, LightEmission 1, Emit(12); (b) flash: soft circle, Size 0→3, Lifetime 0.08, Emit(1) |
| **Coin pickup** | Star texture, Emit(15), Speed 6–10, SpreadAngle (180,180), Acceleration (0,-10,0), Size 0.6→0, gold ColorSequence, LightEmission 1 + a 0.2 s `PointLight` flash |
| **Level-up** | Disc ring (Shape Disc, ShapeStyle Surface, Speed 0, Size 0→8 ring texture, Lifetime 0.5) + upward column (Cylinder, Speed 8–14, Acceleration (0,10,0)) + Beam spiral optional; FOV kick ([[UI-Polish-And-Juice]]) |
| **Smoke puff** | 4×4 flipbook smoke, LightEmission 0, LightInfluence 1, Transparency 0.3→1, Size 2→6, Speed 2–4, Drag 2, RotSpeed ±30 |
| **Fire (ambient)** | Rate 15–25, Lifetime 0.6–1, Acceleration (0,6,0), Color yellow→orange→dark red, LightEmission 1, LightInfluence 0, Size 1.5→0.2 + PointLight (Range 10–14, flicker via script) |
| **Aura (character)** | LockedToPart true, Rate 8–12, Shape Cylinder around HumanoidRootPart, ZOffset 1, LightEmission 1 |
| **Rain near camera** | Emitter on a part following the camera (client), Box shape 60×1×60 above, Orientation VelocityParallel, Speed 60, Rate ≤100 — never world-wide emitters |

## Beams
- Render a texture between `Attachment0` and `Attachment1`; disabled if either attachment missing.
- `Width0`/`Width1`, `CurveSize0`/`CurveSize1` (Bezier curve using attachment orientation), `Segments` (default 10; raise only for curved beams), `FaceCamera` (true for lasers/light shafts), `TextureMode` (`Stretch`/`Wrap`/`Static`), `TextureLength`, `TextureSpeed` (scroll), `LightEmission`, `LightInfluence`, `ZOffset`, `Brightness`.
- Uses: lasers & tethers, light shafts (FaceCamera, LightEmission 1, Transparency 0.8→1 at ends), waterfalls (Wrap + TextureSpeed), electricity (randomise attachment positions each 0.05 s), path guide arrows for onboarding (Wrap arrows + TextureSpeed 1–2 — very effective FTUE pointer; see [[Onboarding-And-First-60-Seconds]]).

## Trails
- Two Attachments on a moving part define width; trail drawn where they travel. Props: `Lifetime`, `MinLength`, `MaxLength`, `WidthScale` (NumberSequence, taper 1→0), `Color`, `Transparency`, `FaceCamera`, `TextureMode`, `TextureLength`, `LightEmission`.
- Sword swing: attachments at hilt/tip, Lifetime 0.2, WidthScale 1→0, Transparency 0.2→1, LightEmission 1; enable only during the swing (via animation markers — see [[Animation-Rigging-And-IK]]).
- Cosmetic trails are a proven monetisation item (speed trails in simulators/obbies) — cheap to make, reads clearly at small size.

## Attachments
- Effects reference Attachments, not parts → one invisible anchor part (or character part) can host many effects. Name them (`HitPoint`, `TrailTop`) and import from Blender with the `_Att` suffix (Importer converts objects named `*_Att` to Attachments).
- `Attachment.WorldCFrame` for spawning effects at runtime positions.

## Burst helper (client)

```lua
--!strict
-- ReplicatedStorage/Shared/VFX/Burst.luau
-- Template: a Part/Attachment in ReplicatedStorage.VFX containing ParticleEmitters.
-- Each emitter may carry an "EmitCount" number attribute (default 10) and "EmitDelay" (seconds).
local Debris = game:GetService("Debris")
local Workspace = game:GetService("Workspace")

local Burst = {}

function Burst.play(template: Attachment, at: CFrame)
	local holder = Instance.new("Part")
	holder.Anchored = true
	holder.CanCollide = false
	holder.CanQuery = false
	holder.CanTouch = false
	holder.Transparency = 1
	holder.Size = Vector3.one
	holder.CFrame = at
	local attachment = template:Clone()
	attachment.Parent = holder
	holder.Parent = Workspace

	local maxLifetime = 0
	for _, child in attachment:GetDescendants() do
		if child:IsA("ParticleEmitter") then
			local count = (child:GetAttribute("EmitCount") :: number?) or 10
			local delay = (child:GetAttribute("EmitDelay") :: number?) or 0
			maxLifetime = math.max(maxLifetime, delay + child.Lifetime.Max)
			if delay > 0 then
				task.delay(delay, function()
					child:Emit(count)
				end)
			else
				child:Emit(count)
			end
		end
	end
	Debris:AddItem(holder, maxLifetime + 0.5)
end

return Burst
```

Server side only fires `RemoteEvent:FireAllClients("CoinBurst", position)`; clients within ~150 studs play it (distance-cull before playing).

## Performance rules
- Particles are rendered per-client; cost = count × screen coverage × overdraw. Big, slow, overlapping smoke is the worst case.
- Prefer **fewer, larger-texture** particles with flipbooks over many tiny ones — but keep flipbook sheets ≤ 1024² and the number of *unique* flipbook textures low (memory).
- Reuse textures across effects (one spark, one soft glow, one smoke sheet) — texture memory dominates on mobile.
- Disable ambient emitters outside the player's area (StreamingEnabled helps; or toggle by zone).
- `Highlight`: max **255** simultaneous on a client (extras silently ignored); each is a full-screen-ish pass — use ≤ 5–10 for gameplay outlines.
- Lights: `PointLight`/`SpotLight` with Shadows are expensive; VFX flash lights → `Shadows = false`, Range ≤ 16, destroy after 0.2 s.
- Profile with MicroProfiler (Ctrl+F6) and the Render stats (Shift+F2) on a low-end Android.

## Checklist
- [ ] All burst emitters `Enabled = false`, triggered with `Emit()` on client
- [ ] No emitter Rate > 100 (mobile cap) for anything players see often
- [ ] Shared texture set (≤ ~10 VFX textures for the whole game)
- [ ] Effects distance-culled on clients
- [ ] Tested on low-end mobile with 10+ players spamming abilities

## Pitfalls
- Spawning particles from the server for every hit → network spam and delayed visuals.
- `Lifetime` 30 expecting long trails — capped at 20 s.
- Additive (`LightEmission 1`) particles on bright skies wash out to white; use darker colours or `LightEmission 0.5`.
- Flipbook frames without padding bleed into neighbours at low mip levels.
- Forgetting `LockedToPart` on character auras → particles left behind when running.
- Trail attachments too far apart → giant ribbons; keep width ≤ object size.

## Related
- [[Visuals/_Index]] · [[UI-Polish-And-Juice]] · [[Shaders-Materials-And-Surfaces]] · [[Lighting-And-Atmosphere]] · [[Animation-Rigging-And-IK]] · [[Remotes-And-Networking]]

## Sources
- Particle emitters (400/s, 100/s mobile, 20 s lifetime cap, flipbooks, fill-rate) — https://create.roblox.com/docs/effects/particle-emitters
- Beams — https://create.roblox.com/docs/effects/beams ; Trails — https://create.roblox.com/docs/effects/trails
- Highlighting (255 simultaneous limit) — https://create.roblox.com/docs/effects/highlighting
- Meshes / Importer `_Att` naming — https://create.roblox.com/docs/parts/meshes
- API: ParticleEmitter, Beam, Trail, enums ParticleOrientation/ParticleFlipbookLayout/ParticleFlipbookMode — https://create.roblox.com/docs/reference/engine/classes/ParticleEmitter (all checked via Roblox/creator-docs GitHub source, 2026-10-02 commit)
