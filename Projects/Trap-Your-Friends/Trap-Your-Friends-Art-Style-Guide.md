---
tags: [project/trap-your-friends, visuals/art-direction, visuals/retro]
status: draft
updated: 2026-10-05
confidence: medium
---
# Trap Your Friends: Art Style Guide (AWAITING HOLDEN'S APPROVAL)

**Not locked.** Holden said parts are OK in principle but wants to approve the style and the way it's built. The approval step is a Studio **style test** (phase 1 of [[Trap-Your-Friends-Claude-Code-Prompt]]). Until then, everything below is a proposal. General rules: [[Retro-Stud-Style-Guide]]. Pictures: [[Trap-Your-Friends-Reference-Board]].

**Update 2026-10-05 (Holden):** direction **A was chosen for the style test**; B is not being built. Still **NOT locked** until Holden approves the test. Approved for the test: TNT is **Bright red with white bands** (not Really red; the screenshots must say whether it gets confused with the Kill Brick), every trap marking is **made from parts only** (cracks, chevrons, stripes, the "?" crate; no decals), destruction cells are **1 stud**, and the stud MaterialVariant is home-made and applied **part by part by name** (not as a Plastic override), compared with legacy `SurfaceType` studs on two copies of the segment.

**(USER, 2026-10-06) Verdict on v2:** decent overall, but:
- **the painted sky is terrible** (needs a living, layered sky);
- **trap models look cheap**: traps move to **Blender meshes**, while the map stays **part-built and studded**.
Still **NOT locked**. Plans: [[Trap-Your-Friends-v3-Plan]].

**Style test v2 built (2026-10-06), reviewed:** [[2026-10-06-Trap-Your-Friends-Style-Test-v2]]. Lighting v2: Atmosphere is off, because its haze covered the skybox's sea of clouds. Still **NOT locked**.

**(USER, 2026-10-06) Holden's verdict on v1** ([[Trap-Your-Friends-Style-Test-v1-Feedback]]); still **NOT locked**:
- Traps look uninteresting; every trap follows the catalogue design rules (silhouette, face/eyes, idle animation, tells, big funny hits).
- **Black** cartoon outlines (Steal an Egg style) on trap models, props and NPCs.
- JJS-style destruction (cut around the hit, mixed slabs, ~10 s lingering debris, heavy impact VFX + hit-stop, rebuild only when nobody is near).
- Builds look low effort. Needed: a themed environment + skybox, 3-tone colour variation, trim and props, calmer walls, no glare speckle, a better lighting pass.
- Our own decals/textures may be uploaded as private images.

**Style test v1 built (2026-10-05), reviewed 2026-10-06:** [[2026-10-05-Trap-Your-Friends-Style-Test]] (screenshots, counts, Legacy vs MaterialVariant studs). Still **NOT locked**.

## TL;DR
- **Two directions to choose between.** A "Modern Retro" (recommended) and B "Authentic 2008". Both use classic studded bricks; they differ in lighting, VFX and characters.
- **What Holden's reference games actually do** (Jujutsu Shenanigans, Forsaken, Die of Death, untitled tag game, Doomspire Brickbattle):
  - Obs: blocky classic Roblox characters and classic faces are the identity.
  - Obs: classic studded bricks and primary colours, especially in Doomspire and in JJS destruction debris.
  - Obs: modern lighting, shadows, bloom and punchy VFX on top. They are not 2008-accurate.
  - Obs: hand-drawn comic thumbnails of blocky characters (Forsaken, UTG, Die of Death).
  - Principle: "retro" in 2026 hits = **classic shapes, faces and studs + modern feel**. That's direction A.
- **Destruction is part of the look:** bricks shatter into small studded cubes, bounce, shrink and fade, then the lane rebuilds (JJS-style).
- **Every trap has its own colour and shape**, so a runner knows what it does before touching it. Really red is reserved for kill bricks.

## Direction A: Modern Retro (recommended)
| Element | Spec (starting values to tune in the style test) |
|---|---|
| Geometry | Classic primitives only (Block, Wedge, Cylinder, Ball, Truss) on a **1-stud grid**; Brick 1.2 / Plate 0.4 heights; 90° rotations; chunky (walls ≥ 1 stud) |
| Surfaces | **Studs on top, inlets underneath.** Test both: legacy `SurfaceType.Studs/Inlet` on Parts vs a stud `MaterialVariant`. Pick the one that reads better on a phone |
| Materials | Plastic / SmoothPlastic + studs. Neon only for trap "tells" (a glow strip on dangerous moving parts) |
| Palette | Bright classic BrickColors. Each lane theme gets 3–4 colours + the reserved trap colours below. Nothing off-palette. **DRAFT exception (Holden OK'd the idea, 2026-10-06):** floors and ground use **3 tones** per surface (the palette colour ±5–8% lightness as Color3); walls use 2 tones max; no light speckle. Reserved trap colours never get the variation |
| Lighting | `LightingStyle = Realistic` with soft shadows (studs read better with shadows), bright midday sky, Bloom low (Intensity ~0.5), ColorCorrection Saturation +0.1–0.2. No DepthOfField |
| Characters | Players' own avatars (R15). Tutorial bots and NPC runners are **classic blocky noobs** (yellow head/arms, blue torso, green legs is the iconic combo; ⚠️ verify there are no brand issues with using the classic noob colours) |
| VFX | Modern and punchy: dust puffs, white impact flashes, small screen shake, stud-cube debris, confetti on trap kills |
| Sound | Plastic clacks, brick crumble, a goofy "bonk" and an original cartoon death sound. No old "oof" |
| UI | Modern-classic chunky buttons (vault `X/ui-stud` refs): thick strokes, bright fills, stud pattern on panel backs |
| Thumbnail (later) | Hand-drawn comic style of blocky characters falling into traps (Forsaken / UTG approach) |

## Direction B: Authentic 2008
| Element | Spec |
|---|---|
| Geometry / surfaces / palette | Same as A, palette even stricter (~16 colours) |
| Lighting | `LightingStyle = Soft`, flat ambient, no visible shadows, `ColorGradingEffect` Retro tonemapper, ClockTime 14 |
| Characters | Forced classic R6 blocky characters |
| VFX / UI | Minimal; grey translucent 2008-style panels |
| Risk | Reads as "old" rather than "fun-retro" to 12–15-year-olds; R6 reportedly blocks MeshPart heads/accessories (⚠️ verify) |

## Trap colour language (proposal)
| Trap | Colour / shape tell |
|---|---|
| Kill Brick | **Really red**, the only red in the game; slight pulse |
| Disappearing Plate | Pale yellow, dashed outline, flickers before vanishing |
| Conveyor | Dark grey with scrolling yellow chevrons |
| Bounce Pad | Hot pink dome with a spring |
| Spinner Bar | Orange bar with a glowing Neon strip on the tip |
| Ice Plate | Pale cyan, shiny |
| Glue Plate | Lime green, dripping blobs |
| Push Wall | Navy block with a hazard-stripe face |
| Fake Floor | Same colour as the floor + **faint shimmer** (fairness) |
| Brick Wall (breakable) | Brown/tan brick pattern, visible cracks; shatters |
| TNT Brick | Red-and-white striped brick with a fuse spark. **Style test (Holden, 2026-10-05): Bright red + white bands, never Really red** |
| Mystery Crate | Classic question-mark crate, gold |

## Destruction look (JJS-inspired)
- Hit → the brick **splits into 1×1 studded cubes** (or 2×2 for big pieces) in the brick's own colour; cubes fly from the impact, bounce, shrink and fade over ~1.5 s.
- Large hits (Wrecking Ball, TNT) add a dust puff, flash and small screen shake.
- **The lane rebuilds**: broken cells pop back with a quick "un-break" tween after ~6 s (tunable), so destruction never makes a lane unwinnable.
- Debris is **cosmetic and client-side** (see the GDD tech notes). That's what keeps it cheap and safe.

## Approval checklist (for Holden, after the style test)
- [ ] Direction A or B (or a mix)
- [ ] Stud method: legacy surfaces or MaterialVariant (judge on a phone)
- [ ] Lane theme palette for theme 1 (Classic Baseplate)
- [ ] Trap colours readable at a glance on a phone
- [ ] Destruction feel: debris size, amount, rebuild time
- [ ] Avatar choice: own avatars (R15) or forced classic
- [ ] → then set this note to **LOCKED** with Holden's quote, as was done for Rubber Tower

## Pitfalls
- Matching a thumbnail instead of gameplay. JJS/Forsaken marketing art is hand-drawn; judge the game in Studio and on a phone.
- Too many debris parts on mobile; cap and pool them.
- Copying recognisable characters from Forsaken/JJS (their cast is their IP). Use original blocky characters.

## Related
[[Trap-Your-Friends]] · [[Trap-Your-Friends-Reference-Board]] · [[Retro-Stud-Style-Guide]] · [[Lighting-And-Atmosphere]] · [[VFX-Particles-Beams-Trails]] · [[Art-Direction]]

## Sources
- Observations from the reference board (Roblox game thumbnails and devforum screenshots captured 2026-10-05; stills only, not gameplay).
- R6 / MeshPart heads restriction: creation.dev (Apr 2026), third-party — https://www.creation.dev/learn/r6-avatar-meshpart-heads-accessories-compatibility-issue-2026 ⚠️ verify against Roblox docs.
- Holden's messages, 2026-10-05.
