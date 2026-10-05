---
tags: [prompting/game-feel, visuals/vfx, visuals/animation, visuals/audio, visuals/lighting]
status: draft
updated: 2026-10-04
confidence: medium
---
# Prompting: Game Feel (VFX, Animation, Sound, Lighting)

How to ask Claude for effects, animation, audio and lighting, which are the areas where it can't directly see motion or hear sound and so needs the most scaffolding. General rules: [[Prompting-Principles]].

## TL;DR
- **VFX: compose from building blocks and review with a phase freeze.** Fire the effect, wait an exact time, freeze (`TimeScale = 0`), screenshot start/middle/end. The budget lint passed an effect that the freeze showed was nearly empty mid-way, so ask for both ([[Roblox VFX Review Skill]]).
- **Animation is Claude's weakest area.** Give it a real R6/R15 rig with labelled limbs, have it render every frame onto one contact sheet and check that, and let it copy real Roblox animations first ([[AI-Assisted-Workflow]] §6; SyphoDev: "Claude isn't good at this").
- **Claude can't listen.** It shortlists 3 sounds per need with lengths and tags, Holden picks by ear, and the soundcheck measures silence, clipping and loudness before approval ([[Roblox Audio Pipeline]], [[Roblox Sound Library Skill]]).
- **Lighting: name a preset and the failure to avoid.** Paper Plane Toss's hub went from default to "way too bright"; the fix was lower exposure, bloom and haze ([[Sky Island Hub and Throw Lane]]).
- **Every action gets motion + particles + sound, scaled to the reward size.** Say so in the prompt, with the vault's numbers ([[UI-Polish-And-Juice]], [[VFX-Particles-Beams-Trails]]).

## What Claude needs from you
- The moment and its importance (small hit, big reward, ambient loop), where it plays (client only for bursts), and a reference clip or frames.
- The texture library it may use ([[VFX-Texture-Pack]], built-in textures until uploads are approved).
- For animation: the rig type, the character's personality, which animations (idle, walk, attack) and priority.
- For sound: the mood, any banned sources (Holden avoids AI-generated tracks), and the quota situation.

## Vault notes to point Claude at
| Note | Gives Claude |
|---|---|
| [[VFX-Particles-Beams-Trails]] · [[Roblox VFX Review Skill]] · [[VFX-Texture-Pack]] · [[X-VFX-Reference]] | Caps (400/s, 100/s mobile, 20 s lifetime), burst budgets (hit ≤ 30, ability ≤ 150), client-side bursts, 17 building blocks, references |
| [[Animation-Rigging-And-IK]] · [[X-Animation-Reference]] | Animator rules, priorities, ownership, IK; reference clips |
| [[Sound-Design]] · [[Roblox Audio Pipeline]] · [[Roblox Sound Library Skill]] | Buses and levels, calibrated targets (SFX −19.7 dB, music −30.3 dB), quota (100/month verified), PPT's late-starting SFX finding |
| [[Lighting-And-Atmosphere]] · [[Shaders-Materials-And-Surfaces]] | LightingStyle + PrioritizeLightingQuality, Atmosphere/ColorCorrection ranges, mobile costs |
| [[UI-Polish-And-Juice]] · [[X-Game-Feel-And-Showcases]] | Reward recipe, FOV kick and shake numbers; real game-feel examples |

## Prompts

### 1. A VFX effect
```text
Make a [EFFECT, e.g. "level-up burst"] for [Game]. It's a [small / big / ambient] moment.
READ FIRST: Visuals/VFX-Particles-Beams-Trails.md and the roblox-vfx-review skill's library and budgets.
- Compose it from the skill's building blocks (e.g. glow + sparks + ring); use built-in textures or the VFX Texture Pack. Don't harvest Toolbox packs without telling me the creator and licence.
- Bursts use Emit(n) on the client, fired by a RemoteEvent with position and type; nothing spawned by the server.
- Stay in budget: [hit ≤ 30 / ability ≤ 150 / ambient ≤ 20/s], lifetime ≤ 20 s, LightEmission ≤ 0.5 on bright skies.
- Expose it as [Module].play(position, "[Name]") so gameplay code can call it.
DONE WHEN: the skill's lint passes AND the phase freeze screenshots at start, middle and end each show something readable from [N] studs. Show me the three frames with your honest look review.
```
Why: the fireball impact passed the lint but looked like a white puff, then nothing; the freeze is the only way Claude "sees" a sub-second effect ([[Roblox VFX Review Skill]]).

### 2. Retune an effect from a look review
```text
The [EFFECT] phase freeze showed: start = [what], middle = [what], end = [what]. I want: [e.g. "orange/red flame lasting 0.8–1.2 s, embers readable at 18 studs, lighter smoke"]. Change only that effect, re-run the lint and the freeze at the same times, and show old vs new frames side by side.
```

### 3. Animation
```text
Make [ANIMATIONS: idle, walk, attack] for [CHARACTER] on an [R15 / R6 / custom] rig. Expect several rounds; this is hard for you.
- First recreate [a reference Roblox animation or clip] on the same rig, so you learn how it moves.
- Use a rig with a labelled texture (FRONT/BACK/L/R on each limb) so you don't confuse sides.
- Write poses as data (joint, angle, time); build it in Blender; render every frame onto one contact sheet and check it before showing me. Look for foot sliding, limbs through the body, and the attack reading clearly at phone size.
- In game: play it through the Animator, load each track once, priority Action for attacks (upper body only so walking legs still play), assets owned by the group that owns the game.
Show me the contact sheet and a short honest critique.
```
Why: contact sheets let Claude see the whole motion in one image; ownership and priority mistakes make animations silently fail ([[AI-Assisted-Workflow]] §6, [[Animation-Rigging-And-IK]]).

### 4. Sounds
```text
I need sounds for [list of moments]. You can't listen, so:
1. For each moment, shortlist 3 options from [Pixabay / my catalogue] with length, tags and the file URL. Check the catalogue (AssetLibrary/audio/catalogue.json) first and reuse an approved id if one fits.
2. I'll pick by ear. Then run the soundcheck on my picks: lead silence (trim or use PlaybackRegion if over 50 ms), clipping, loudness, and suggest a Sound.Volume that hits the targets (SFX about −19.7 dB, music about −30.3 dB).
3. Don't upload until I say so; log every upload in the catalogue (the quota is about 100 a month for a verified account).
Avoid AI-generated tracks. Repeated sounds get ±5–10% pitch variation and a minimum gap so they can't stack.
```
Why: this is the flow that shipped Paper Plane Toss's 17 sounds; the soundcheck later found 9 SFX starting 59–216 ms late ([[Roblox Sound Library Skill]]).

### 5. Lighting pass
```text
Do a lighting pass on [AREA] for [Game] (genre: [simulator/obby/…], audience young teens on phones).
Start from the preset in Visuals/Lighting-And-Atmosphere.md for this genre: LightingStyle, Atmosphere density and colour, ColorCorrection saturation and contrast, mild Bloom, sun angle for readable shadows. Walkable and interactive things must be the brightest, most saturated things on screen; background lower saturation.
Avoid: washed-out white (too much exposure or bloom), pitch-dark areas on a dim phone, dozens of shadow-casting lights.
Show me screenshots at player-eye and overview, before and after, and say what you'd tweak next.
```

## More examples (added 2026-10-04)
Shorter prompts for other common jobs. Same rules: fill every bracket, keep the check. Sourced patterns are credited in [[Community-Prompt-Examples]].

### Big reward moment
```text
Make the [big reward] moment in [Game] feel great using Visuals/UI-Polish-And-Juice.md: popup scales 0 → 1.15 → 1, count-up on the number, a particle burst on the client, a rising-pitch coin sound, a camera FOV kick (+6–10°, 0.08 s in, 0.35 s out) and a small shake, with fades instead when ReducedMotion is on. Scale it down for small rewards so the big one stays special.
```

### Hit feedback for melee
```text
Add impact feel to [Game]'s melee hits: a 0.05–0.08 s hit-stop on the attacker's client, a hit spark from the VFX library at the contact point, a short target flash (Highlight), a hit sound with ±8% pitch, and knockback applied by the owning client. Show phase-freeze frames of the spark and tell me how it feels at 30 FPS on a phone.
```

### Footsteps by material
```text
Add footsteps for [Game]: sounds per floor material ([grass, wood, stone, cloud]) from my catalogue, timed to the walk animation, pitch varied ±5–10%, quieter for other players, none while airborne. Throttle so fast movement can't stack them.
```

### Ambient life
```text
Make [area] feel alive without hurting phones: [2–3] ambient emitters (rate ≤ 20 each, e.g. drifting leaves, fireflies at night), a quiet ambience loop that doesn't sound like an engine, and one moving detail (birds, swaying banners). Check the live particle count stays within budget and show me before/after screenshots.
```

### Cutscene camera
```text
Build the [intro] cutscene camera for [Game]: waypoints I'll approve from a top-down sketch, eased tweens, and a Skip button. Before showing me, check every camera path segment against the real map geometry with raycasts (nothing passes through statues or walls) and record it at phone aspect.
```
Paper Plane Toss's arrival flew through a statue for 4.5 s of white screen ([[2026-10-03 Paper Plane Toss Phone Playtest]]).

## How to check the result
- VFX: lint PASS + three phase-freeze frames that read clearly; live particles within budget.
- Animation: a contact sheet with no foot sliding or clipping; plays for other players in a live test (ownership).
- Sound: soundcheck numbers within targets; Holden's ears; quota logged.
- Lighting: before/after screenshots that Holden approves on his phone.

## Pitfalls
- **Server-spawned particles** for every hit cost bandwidth and arrive late ([[VFX-Particles-Beams-Trails]]).
- **Studio accepts invalid values** (Rate 450, Lifetime 25) without clamping; the lint must catch them ([[Roblox VFX Review Skill]]).
- **`require` caches across MCP calls**, so after a Rojo sync Claude may test an old module; require a fresh clone ([[Roblox Studio MCP Quirks]]).
- **Animations uploaded to a personal account** don't play in a group game's live servers ([[Animation-Rigging-And-IK]]).
- **Constant ambience loops** can sound wrong (Paper Plane Toss's wind loop sounded like an engine) and music mixes judged on PC are too loud on phones ([[Roblox Audio Pipeline]]).
- **Lighting judged on a bright monitor** looks black on a phone at half brightness ([[Art-Direction]]).

## Related
[[Prompting/_Index|Prompting]] · [[Prompting-Principles]] · [[Prompting-3D-Assets-And-Maps]] · [[Prompting-UI]] · [[Roblox VFX Review Skill]] · [[Roblox Sound Library Skill]]

## Sources
- SyphoDev video (VFX harvest + phase freeze 18:08–20:12; sound 20:12–20:58; animation 20:58–22:08): <https://www.youtube.com/watch?v=afuKhenJldY>
- Local: [[Roblox VFX Review Skill]], [[Roblox Audio Pipeline]], [[Roblox Sound Library Skill]], [[Sky Island Hub and Throw Lane]], [[Join Cutscene and Tutorial]] (2026-10-02 to 2026-10-04).
- Roblox Open Cloud asset usage guide (audio quotas): <https://create.roblox.com/docs/cloud/guides/usage-assets>
