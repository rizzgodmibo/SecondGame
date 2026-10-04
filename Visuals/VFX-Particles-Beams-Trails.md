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
- **Hard limits**: one emitter tops out at **400 particles/s (100/s on mobile)**; particle **Lifetime is capped at 20 s**. Studio *accepts* Rate 450 and Lifetime 25 when set (observed 2026-10-04), so lint for them with [[Roblox VFX Review Skill]]. Fill-rate (screen pixels covered × overlap) is the real GPU cost — big, overlapping, transparent particles kill mobile.
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
- **Emitters inside an Attachment spawn from one point** (docs: "particles spawn from the attachment's position"). `Shape` doesn't spread them; aim the emitter by rotating the Attachment.
  - A ParticleEmitter's `EmissionDirection` face is read in the attachment's frame. With Orientation (−12, 0, 0), `Front` points 12° below the part's forward.
  - For an emission *area*, parent the emitter to an invisible, sized part instead. Verified from the creator-docs source, 2026-10-04.
- **Attachment.Position is relative to the parent part's CFrame.** For an imported MeshPart that is the centre of its bounding box, not the imported pivot. Convert Blender/file coordinates with `position = filePoint − bboxCentre`. ⚠️ verify on the first import with `Visible = true`.

### More verified ParticleEmitter facts (creator-docs `ParticleEmitter.yaml`, fetched 2026-10-04)
- `Acceleration` is in **global axes** (studs/s²), whatever the emitter's orientation.
- `FlipbookFramerate` maxes out at **30 fps**. `OneShot` ignores it and spreads the frames over each particle's lifetime.
- `Drag` is documented as "the rate in seconds at which individual particles will lose half their speed via exponential decay". Don't hand-calculate reach from that wording; tune `Speed`/`Drag` in Studio.
- `Brightness` only scales emitted light when `LightInfluence` is 0.

## Worked example: Cinder Drake VFX spec (2026-10-04)
`Assets/FantasyCreatures/models/CinderDrake/VFX.md` + `vfx_spec.json` describe a static boss creature's VFX as data, with no scripts. **Not built in Studio yet**, so treat it as a recommendation. See [[Fantasy-Creatures-Set]].
- **Ambient, always on:** nostril smoke (smoke_puff, Rate 2 per nostril), ember drift (spark_dot, Rate 5) and a throat PointLight (Range 6, no shadows).
- **Triggered:** fire breath, four emitters toggled together (`Enabled` true for the length of the breath):
  - BreathFlame: **smoke_puff tinted fire colours**, LightEmission 1, Rate 60, life 0.45–0.6 s, size 0.55 → 2.6;
  - BreathCore: Hoard `Glow.png`, white-hot, ZOffset 0.8, hides the static closed jaw;
  - BreathSparks;
  - BreathSmoke: smoke flipbook in **OneShot**, starts at Transparency 1 so it first shows past the flames;
  - plus a PointLight (Range 12).
  - Total 124 particles/s, about 66 live.
- **Why spec v2 dropped the pack's fire flipbook:** its frames are torch flames cut flat at the base, so a jet of flying, rotating flame particles shows straight edges. The smoke flipbook fades over its 16 frames, so Loop would pop. See [[VFX-Texture-Pack]] → Pitfalls.
- **A JSON layout that works for any creature:**
  - `textures` (key → file, image_id);
  - `attachments` (Position in part space, a pivot-space fallback, Orientation);
  - `emitters` (props with NumberSequence = `[[t, v], …]` and ColorSequence = `[[t, "#hex"], …]`);
  - `lights`, `triggers`, `budget` and `verify`.
  - A future setup script can build every instance from it.

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

## Worked example: HoardVFX (Dragon's Hoard set, 2026-10-03)
`Assets/DragonsHoard/scripts/HoardVFX.luau` is a reusable client ModuleScript. It has been written but **not yet run in Studio**, so treat the patterns below as recommendations. See [[Dragons-Hoard-Set]].
- **API:** `enable(target, preset)`, `disable(target, preset?)`, `enableDefault`/`enableAllIn` (reading a `HoardVFXPreset` attribute), `setPickupIdle`, `openChest`/`closeChest`, `placeSword`.
- **Cleanup:** every created instance is tracked per target and prefixed `HoardVFX_`. `disable()` or `target.Destroying` removes them, so nothing leaks.
- **Pulse glow:** a looping tween (`RepeatCount = -1`, `Reverses = true`, Sine) on `PointLight.Brightness`, plus an optional `Highlight.FillTransparency` (OutlineTransparency 1, DepthMode Occluded). The Highlight can be switched off because each one is an extra render pass.
- **Item twinkle:** an emitter parented to the part with Shape Sphere + Volume (it hugs round props better than Box) and `ZOffset 0.4` so twinkles sit on the near surface. Rate scales with footprint (0.5–4/s).
- **Egg particles:** Shape Sphere + **Surface**, so particles spawn on the egg's skin.
- **Chest burst:** emitters in an Attachment at the chest mouth, `Enabled = false`, then `Emit(1)` glow flash + `Emit(24)` coin glints (gravity −18) + `Emit(30)` sparks. A PointLight flashes to 5, settles to 1.2, and fades on close.
- **Blade shine sweep:** a `Beam` with `FaceCamera = true` between two attachments across the blade, tweened tip→guard. The appearance fades by tweening `Width0`/`Width1`, because NumberSequence transparency can't be tweened.
- **Pickup idle:** one shared `Heartbeat` connection for all idling items, disconnected when none remain. It runs `PivotTo(base * bob * spin)`, works on anchored items only, and restores the stored pivot when switched off.
- **Fallback textures:** `rbxasset://textures/particles/sparkles_main.dds`, `fire_main.dds` and `smoke_main.dds` are used until real Image ids are pasted in. ⚠️ verify that these still ship with the client.

## Related
- [[Visuals/_Index]] · [[UI-Polish-And-Juice]] · [[Dragons-Hoard-Set]] · [[VFX-Texture-Pack]] · [[Shaders-Materials-And-Surfaces]] · [[Lighting-And-Atmosphere]] · [[Animation-Rigging-And-IK]] · [[Remotes-And-Networking]]

## Sources
- Particle emitters (400/s, 100/s mobile, 20 s lifetime cap, flipbooks, fill-rate) — https://create.roblox.com/docs/effects/particle-emitters
- Beams — https://create.roblox.com/docs/effects/beams ; Trails — https://create.roblox.com/docs/effects/trails
- Highlighting (255 simultaneous limit) — https://create.roblox.com/docs/effects/highlighting
- Meshes / Importer `_Att` naming — https://create.roblox.com/docs/parts/meshes
- API: ParticleEmitter, Beam, Trail, enums ParticleOrientation/ParticleFlipbookLayout/ParticleFlipbookMode — https://create.roblox.com/docs/reference/engine/classes/ParticleEmitter (all checked via Roblox/creator-docs GitHub source, 2026-10-02 commit)
