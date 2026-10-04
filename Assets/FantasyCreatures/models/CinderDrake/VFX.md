# Cinder Drake: VFX setup in Roblox Studio (spec v3, 2026-10-04)

This is a data-only spec that matches the VFX key on the v3 sheet. No scripts yet ("Roblox scripts + zip: Not yet"). It has **not been built or tested in Studio**; every number is a starting point to tune.

The machine-readable copy is `vfx_spec.json`. Do [IMPORT.md](IMPORT.md) first.

**v3 change:**
- the fire breath uses **our own flame flipbook** (`CinderDrake_FlameFlip4x4.png`) plus a glow core;
- the smoke flipbook plays OneShot;
- the **jaw is a separate hinged part**, so the mouth can open for the breath;
- the attachment positions are updated for the v3.1 export (thicker legs moved the Body's centre slightly).

[Why the textures changed](#texture-notes).

## What's on the drake

| Sheet key | How it's made | Runs |
|---|---|---|
| Nostril smoke | `NostrilSmoke` emitter on NostrilL and NostrilR | always (ambient) |
| Ember drift | `EmberDrift` emitter on ThroatFX | always |
| Throat furnace | Body emissive seams (already in the export) + `ThroatLight` on ThroatFX | always |
| Ember eyes | `CinderDrake_Glow` Neon + Bloom (IMPORT.md steps 6 and 8) | always, no emitter |
| Fire breath | Jaw opens (see [The jaw](#the-jaw)), then `BreathFlame`, `BreathCore`, `BreathSparks`, `BreathSmoke` + `BreathLight` on BreathFX | **trigger**: Enabled = false until the drake breathes |

**Budget:**
- **Ambient:** 9 particles/s, about 19 live particles, 1 light.
- **Breath:** 124 particles/s across 4 emitters (the largest is 60/s; the mobile cap is 100/s per emitter), about 66 live particles, 1 light.
- **Lights:** both have Shadows off.
- **Textures:** 5 unique; only one of them is 1024².

These are inside the vault targets in [[VFX-Particles-Beams-Trails]]: ambient Rate ≤ 20, a big ability ≤ 150 live particles.

## 1. Textures
Upload these as **Images**, then copy each Image id. Asset Manager bulk import gives Image ids directly; a Creator Hub Decal upload gives a Decal id, which won't work in `Texture`. Uploading publishes to your account, so do it when you're ready.

Until a texture is uploaded you can build and review with its built-in placeholder. Placeholders are single images, so `BreathFlame` and `BreathSmoke` use FlipbookLayout **None** until the real sheets are in.

| Key | File | Size | Placeholder (`rbxasset://textures/particles/…`) |
|---|---|---|---|
| flame_flip | `Assets/FantasyCreatures/models/CinderDrake/CinderDrake_FlameFlip4x4.png` (ours) | 512², 4×4 flipbook | `fire_main.dds` |
| smoke_puff | `Assets/VFX/TexturePack/VFX_smoke_puff.png` | 256² | `explosion01_smoke_main.dds` |
| spark_dot | `Assets/VFX/TexturePack/VFX_spark_dot.png` | 128² | `sparkles_main.dds` |
| glow | `Assets/DragonsHoard/vfx/Glow.png` | 128² | `explosion01_core_main.dds` |
| smoke_flip | `Assets/VFX/TexturePack/VFX_smoke_flip4x4.png` | 1024², 4×4 flipbook | `smoke_main.dds` |

Write the ids into [[VFX-Texture-Pack]] (and the roblox-vfx-review library) so other effects reuse them.

**Low-end fallback:** give `BreathSmoke` (and if needed `BreathFlame`) smoke_puff and no flipbook. That drops the only 1024² texture.

## 2. Add four Attachments to `CinderDrake_Body`
Insert Object → Attachment, then rename it and type in its Position and Orientation.

| Name | Position (from the Body part's centre) | Orientation | Where it is |
|---|---|---|---|
| NostrilL | 0.12, -1.113, -7.2 | 0, 0, 0 | on the left nostril |
| NostrilR | -0.126, -1.113, -7.2 | 0, 0, 0 | on the right nostril |
| ThroatFX | -0.003, -1.241, -4.145 | 0, 0, 0 | 0.11 studs under the throat, outside the mesh |
| BreathFX | -0.003, -1.491, -7.295 | **-12**, 0, 0 | 0.1 studs in front of the lips, tilted 12° down. It's on the Body (upper jaw), so it stays put when the Jaw opens |

**Check the markers.** Turn on `Visible` on each attachment and look at the green markers. A MeshPart's centre is the centre of its bounding box, which here sits (0.003, 3.641, 1.795) from the imported pivot. If the markers are off, the importer centred the part differently: use the `pivot_position` values in `vfx_spec.json` with the model's pivot instead. Turn `Visible` off afterwards.

**Why the breath points 12° down:** the breath leaves along BreathFX's Front face. The head is pitched down about 25°, so aiming the jet that low would bury it in the ground about 4.6 studs out. At -12° the flames (about 6 studs long) stay just above flat ground.

## 3. Add the emitters and lights
Properties that aren't listed keep their defaults.

**How to read the tables:**
- **Size, Transparency and Color** are keypoints, written as `time: value`.
- **Lifetime, Speed, Rotation and RotSpeed** are min–max ranges.
- **Emitters on an Attachment** spawn from that single point, and EmissionDirection is a face of the attachment.

### NostrilSmoke: copy it onto both NostrilL and NostrilR
| Property | Value |
|---|---|
| Texture | smoke_puff |
| Enabled / Rate | true / 2 |
| Lifetime / Speed | 1.4–2.0 / 0.3–0.6 |
| EmissionDirection / SpreadAngle | Front / 20, 20 |
| Drag / Acceleration | 2 / 0, 1, 0 |
| Size | 0: 0.18 · 0.5: 0.5 · 1: 0.85 |
| Transparency | 0: 0.45 · 0.4: 0.65 · 1: 1 |
| Color | 0: #C9C0BD · 1: #8A817E |
| LightEmission / LightInfluence | 0 / 1 |
| Rotation / RotSpeed / ZOffset | 0–360 / -25–25 / 0.1 |

### EmberDrift on ThroatFX
| Property | Value |
|---|---|
| Texture | spark_dot |
| Enabled / Rate | true / 5 |
| Lifetime / Speed | 2.0–3.0 / 0.6–1.4 |
| EmissionDirection / SpreadAngle | **Bottom** / 70, 70 |
| Drag / Acceleration | 1 / 0, 1.5, 0 |
| Size | 0: 0.12 · 0.75: 0.09 · 1: 0 |
| Transparency | 0: 0 · 0.7: 0.15 · 1: 1 |
| Color | 0: #FFD27A · 0.5: #FF8A1E · 1: #B5260A |
| LightEmission / LightInfluence / Brightness | 1 / 0 / 2 |
| ZOffset / WindAffectsDrag | 0.2 / true |

The sparks leave the throat downward and sideways, then curl up past the sides of the neck. Straight up would hide them inside the neck.

### ThroatLight (PointLight) on ThroatFX
Enabled true · Color 255, 106, 26 · Brightness 1.2 · Range 6 · Shadows false.

Later, a client script can pulse its Brightness between 0.8 and 1.6 (sine, about 2.4 s per cycle). It looks fine without the pulse.

### Fire breath on BreathFX: all of these start with Enabled = false

| Property | BreathFlame | BreathCore | BreathSparks | BreathSmoke |
|---|---|---|---|---|
| Texture | flame_flip | glow | spark_dot | smoke_flip |
| Rate | 60 | 30 | 24 | 10 |
| Lifetime | 0.45–0.6 | 0.12–0.2 | 0.5–0.9 | 1.0–1.5 |
| Speed | 11–14 | 5–7 | 12–18 | 9–12 |
| EmissionDirection / SpreadAngle | Front / 8, 8 | Front / 5, 5 | Front / 16, 16 | Front / 12, 12 |
| Drag | 1.5 | 0 | 1 | 2 |
| Acceleration | 0, 3, 0 | 0, 0, 0 | 0, 2.5, 0 | 0, 2.5, 0 |
| Size | 0: 0.55 · 0.35: 1.5 · 1: 2.6 | 0: 0.5 · 1: 1.2 | 0: 0.14 · 1: 0 | 0: 1.0 · 1: 3.2 |
| Transparency | 0: 0.15 · 0.6: 0.3 · 1: 1 | 0: 0 · 0.7: 0.2 · 1: 1 | 0: 0 · 0.8: 0.1 · 1: 1 | 0: 1 · 0.2: 0.45 · 1: 0.6 |
| Color | 0: #FFE7A0 · 0.35: #FF9A2A · 1: #C2300C | 0: #FFF4CC · 1: #FFC860 | 0: #FFE2A0 · 0.5: #FFB347 · 1: #FF6A1A | 0: #4A4240 · 1: #2B2726 |
| LightEmission / LightInfluence | 1 / 0 | 1 / 0 | 1 / 0 | 0 / 1 |
| Brightness | 2.5 | 4 | 3 | (default) |
| Rotation / RotSpeed | 0–360 / -90–90 | (default) | (default) | 0–360 / -40–40 |
| ZOffset | 0.4 | 0.8 | 0.4 | 0 |
| Flipbook | Grid4x4, **OneShot**, StartRandom off | none | none | Grid4x4, **OneShot**, StartRandom off |

With the placeholder textures, use FlipbookLayout None on both flipbook emitters.

### BreathLight (PointLight) on BreathFX
Enabled **false** · Color 255, 138, 48 · Brightness 3 · Range 12 · Shadows false.

## 4. Preview the breath without a script
1. Open the mouth: select `CinderDrake_Jaw` and rotate it -28° about X with the Rotate tool. It turns around its pivot once the pivot is set (IMPORT.md step 9). Undo afterwards.
2. Press Run (F8).
3. Select BreathFlame, BreathCore, BreathSparks, BreathSmoke and BreathLight.
4. Tick `Enabled`, then untick it.

Particles already in the air finish their lifetime.

The real trigger is the same jaw turn and toggle, done by a client script when the server says the drake breathes. How long the breath lasts and when it fires belong to the attack design, which isn't decided yet.

## Texture notes
- **`VFX_fire_flip4x4.png` isn't used here.** Its 16 frames are torch flames whose base is cut flat (three frames also have tips cut flat at the top).
  - Flying, rotating particles show those straight edges. In the first preview they stacked into a hard-edged slab at the end of the jet.
  - Keep that sheet for anchored flames: torches and burning ground, with low Speed, upward Acceleration and Rotation 0.
- **`VFX_smoke_flip4x4.png` fades by itself.** Each frame's centre alpha drops from 0.95 in frame 1 to about 0 by frames 14–16 (measured from the PNG). So it needs **OneShot** with no random start; Loop would pop back to full opacity.
- **`CinderDrake_FlameFlip4x4.png` is ours**, made procedurally by `build_creatures.py -- flameflip` (`make_flame_flipbook`).
  - It has 16 turbulent flame puffs: frames start compact and white-hot, then lick upward, then break into wisps.
  - Alpha is zero on every cell edge, so flying, rotating particles show no straight edges.
  - It's greyscale, so the tint comes from `Color`. Play it OneShot; 512² keeps it light for phones.
- **Soft puffs (smoke_puff) are the low-end fallback.** Tinted hot-to-cool with additive blending, they still read as fire, but without the licking shapes.

## Lint (roblox-vfx-review rules, checked by hand on 2026-10-04)
The skill's Studio lint (`VFXCheck`) and phase freeze were **not run**, because nothing has been built in Studio.

| Check | Result |
|---|---|
| no-texture | pass once the Image ids are filled in (placeholders listed until then) |
| rate-cap | pass: largest is 60/s |
| lifetime-cap | pass: longest is 3 s |
| ambient-rate | pass: largest ambient emitter is 5/s |
| stream-in-burst | **WARN, expected.** The breath is channelled (Enabled while breathing), not an `Emit()` burst |
| invisible | pass |
| flipbook | pass, as long as BreathFlame and BreathSmoke use Grid4x4 only with their uploaded sheets |
| brightness | pass: highest is 4 |
| live-estimate | pass: about 85 live with ambient and breath together |

## The jaw
- **What it is.** Since v3.1 the lower jaw, lower teeth, lower fangs and jaw spines are their own MeshPart, `CinderDrake_Jaw`. It's still a static mesh with no rig: a script just turns the part.
- **Pivot.** Its hinge is at (0, 2.669, -3.52) from the model pivot. Set `PivotOffset` to **(0, 0.333, 0.755)** from the part's centre (IMPORT.md step 9).
- **Opening it.** Turn it about its own X axis:
  - **-28°** for the breath (the sheet's FIRE BREATH pose);
  - **-40°** for a roar (the ROAR pose);
  - negative opens; around 0.12 s each way feels snappy.
- **Textures.** The Body texture set was baked with the jaw 40° open, so the palate, tongue and teeth are textured at any opening (see `preview_game_jaw_open.png`). It shares the Body's SurfaceAppearance images.
- **Limits.**
  - Neck, head and tail still can't move.
  - BreathFX stays on the Body (upper jaw) at the lips, so the fire starts between the open jaws.
  - LockedToPart and VelocityInheritance stay at their defaults.

## ⚠️ Verify in Studio
- [ ] Attachment markers sit at the nostrils, under the throat and in front of the lips.
- [ ] **Jaw.** With PivotOffset (0, 0.333, 0.755), a -28° turn about X opens the mouth around the hinge. The sign was worked out from Blender axes, not tested in Studio.
- [ ] **Jet length.** Drag is documented as "the rate in seconds at which individual particles will lose half their speed via exponential decay". Check that the jet reaches about 6 studs and the smoke rolls off its end; tune Speed or Drag if not.
- [ ] **Breath against different lighting.** Check a bright sky and a dark cave. If the additive fire turns white, lower Brightness or set LightEmission to 0.5.
- [ ] **Embers.** They should rise beside the neck, not vanish inside it. If they do vanish, raise SpreadAngle or Speed a little.
- [ ] **Phase freeze** (roblox-vfx-review) of the breath at start / middle / end once it's built.
- [ ] **Frame time** on a low-end phone with the breath running (MicroProfiler / Shift+F2).

## Sources
- ParticleEmitter API, from the creator-docs GitHub source `ParticleEmitter.yaml`, fetched 2026-10-04:
  - an emitter on an Attachment spawns from the attachment's position, so rotate the attachment to aim it;
  - Acceleration is global-axis;
  - FlipbookFramerate max 30;
  - OneShot ignores FlipbookFramerate.
- Vault notes:
  - [[VFX-Particles-Beams-Trails]]: 400/s per emitter, 100/s on mobile, 20 s Lifetime cap, effect budgets.
  - [[VFX-Texture-Pack]]: texture sizes and the Image-vs-Decal id pitfall.
- Texture alpha measured from the PNGs (2026-10-04).
- roblox-vfx-review skill: lint rules, library blocks and placeholders.
