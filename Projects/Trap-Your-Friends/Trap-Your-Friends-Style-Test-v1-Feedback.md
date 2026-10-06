---
tags: [project/trap-your-friends, visuals/art-direction, playtest/feedback]
status: draft
updated: 2026-10-06
confidence: medium
---
# Trap Your Friends: Style Test v1 Feedback → v2 Spec

## Holden's verdict on style test v1 (USER, 2026-10-06)
- "the traps or things like that, we need **TONS** of them, thats the whole game" → [[Trap-Your-Friends-Trap-Catalogue]].
- "they look kind of **uninteresting**".
- "games like **Steal an Egg** and games with that style have a kind of **outline around models**, we could do something like that".
- "the destruction, we want it **as close to Jujutsu Shenanigans as possible**".
- "the retro look of the builds is alright, but it looks **low quality / low effort**".
- Not decided: legacy vs MaterialVariant studs, shatter vs ragdoll, the spinner/wall-heal issue. The style guide stays NOT locked.

## 1. Outlines (Steal an Egg look)
| Method | How | Good for | Cost and limits |
|---|---|---|---|
| **Highlight per model** (recommended first try) | One `Highlight` on each trap **model**: `OutlineColor` near-black, `OutlineTransparency` 0, `FillTransparency` 1, `DepthMode = Occluded` | Traps, props, NPCs: outlines the whole silhouette | Limit raised **31 → 255** (Roblox, 2025-11-10). Each highlighted object is a separate draw call, plus a post-process pass if any is on screen. Budget: ~1 per trap model + key props, so ~80 max on screen; cull far ones on low-end devices |
| **Inverted hull** | Duplicate slightly larger mesh with flipped normals, black, made in Blender | Hero props and meshes; works at any count | Mesh work per model; doesn't work on plain Parts. Thickness is fixed in world space |
| **SelectionBox edges** | `SelectionBox` (black, LineThickness ~0.03) on bricks | Crisp edge lines on lane bricks (comic look) | Lots of instances; test cost; it's a box, so only good for block parts |
| **Edge-trim parts** | Thin dark parts along brick edges | Static scenery | Part count goes up |
- Test in v2: Highlight on all traps and NPCs; SelectionBox edges on one segment's bricks vs none; compare on a phone-size view. Thickness and colour must stay consistent across all traps.
- Source: devforum "Lights, Camera, More Highlights!" (2025-11-10); Highlight API docs.

## 2. Destruction as close to JJS as possible
**What JJS shows** (frames from FloatyZone, "13 Destruction Experiments in Jujutsu Shenanigans", 2026; stills only; `Assets/Reference-Captures/Retro-Stud/jjs-video-frames-*.jpg`):
- Obs: walls break into **irregular slabs and chunks of many sizes**, big pieces and small ones mixed. Not uniform little cubes.
- Obs: only **the part of the wall touched by the hit** breaks; the rest stays standing with a jagged hole (devforum description: "the part of the big wall which is touching my hitbox gets turned into voxels, but the rest of the part stays normal").
- Obs: debris **piles up and lingers on the ground**. One frame shows a whole field littered with fragments.
- Obs: heavy hit VFX: white speed/impact streaks, flashes, coloured burst, camera shake.
- Obs: JJS maps are smooth simple part-built cities (blocky buildings and trees), not studded. Studs remain our own choice.
- Reported: JJS used the **Vex 2.0** module, later heavily modified by its developer (devforum hearsay). It reportedly uses layered cutting and aggressive part-count reduction rather than full voxelisation.

**v2 destruction spec (DRAFT):**
- **Cut around the impact:** subdivide only the hit region of a part. Pieces are small near the impact centre and bigger further out (layered/octree split, a few levels). The surrounding wall stays, with a hole.
- **Fragment variety:** mixed sizes (0.5–3 studs), some long slabs, random small rotations at spawn. Keep the brick colour; fragments keep studs on their top faces if they're big enough.
- **Physics debris on clients:** fragments fly, bounce, collide with the ground and **settle and linger ~10–15 s**, then sink/fade. Cap and pool them (mobile cap stays, budget TBD by measurement).
- **Impact VFX stack:** a white flash frame, radial streak lines (Beams or Trails), dust burst, small debris particles, camera shake scaled by strength, a crunch sound + a bass thump.
- **Hit-stop:** a 50–80 ms freeze on big hits (the JJS-like punch).
- **Rebuild:** keep the lane fair. Broken pieces rebuild after a delay with a pop-back, but **wait until no player is near and not mid-hit** (fixes the spinner never letting the wall heal). Delay to tune (6–15 s).
- **Server stays authoritative** over what is solid; fragments stay client-side only.
- **Modules:** study VoxBreaker (free, reset timer, hitbox-based; its author recommends client-side debris) and VoxelDestruct. Installing a third-party module needs Holden's approval and an audit ([[Asset-Creation-Workflow-And-Marketplace]]). Our own implementation is also fine.

## 3. "Low quality / low effort" fixes (proposal)
| Problem in v1 | Fix for v2 |
|---|---|
| Lane floats over an empty template baseplate grid | **Themed environment**: island or arena around the lanes, a skybox with clouds, distant scenery silhouettes, ground with grass/terrain or stud-voxel terrain, a start area and finish arch |
| Flat colour blocks, no detail | **3-tone colour variation** per surface (base + slightly lighter/darker bricks mixed), trim/edge bricks on lane borders, plates as accents, small props (flags, signs, lamps, crates) |
| Traps are plain blocks | Trap design rules in [[Trap-Your-Friends-Trap-Catalogue]]: silhouette, faces/eyes, idle animation, tells, outlines |
| Busy wall pattern, glare speckle | Calmer patterns: 2 tones max per wall, no light-grey speckle on floors |
| Weak lighting | Direction A lighting pass: warmer sun, softer shadows, Atmosphere with light haze, ColorCorrection saturation +0.15, mild Bloom; check on a phone-size view |
| No juice | Every trap hit: VFX + sound + camera shake + text pop ("TRAPPED!") |
| Decals not allowed in v1 | Allow **our own** decal/texture uploads (signs, warning stripes, faces, crate "?") as private assets. Holden to approve |

## 4. Open questions for Holden
1. Outline: black, or dark version of each object's colour?
2. OK to upload our own decals/textures (faces, stripes, signs) as private images?
3. OK to evaluate (and possibly use) VoxBreaker after an audit, or build our own?
4. Debris linger time: JJS-like long (10–15 s), or shorter for phones?
5. Stud method: still undecided. Re-judge in v2 with outlines and better lighting.

### Answers (USER, Holden, 2026-10-06)
1. Outline colour: **black**.
2. **Yes:** make and upload our own decals/textures (faces, warning stripes, signs, "?" crate) as private images. Nothing downloaded, nothing published.
3. **Read and audit** VoxBreaker and VoxelDestruct as references; show the audit before installing any of them. Building our own is also fine.
4. Debris linger **about 10 s**: measure it, and lower it on low graphics quality if needed.
5. Stud method: still undecided; re-judge in v2 (Legacy + MaterialVariant copies kept).

## Related
[[Trap-Your-Friends]] · [[Trap-Your-Friends-Art-Style-Guide]] · [[Trap-Your-Friends-Trap-Catalogue]] · [[Trap-Your-Friends-Reference-Board]] · [[VFX-Particles-Beams-Trails]] · [[UI-Polish-And-Juice]]

## Sources
- Holden's message after style test v1, 2026-10-06.
- Highlight limit 255 (2025-11-10): https://devforum.roblox.com/t/lights-camera-more-highlights/4061534 ; API: https://create.roblox.com/docs/reference/engine/classes/Highlight
- JJS destruction thread (Vex 2.0 mention): https://devforum.roblox.com/t/how-could-i-make-destruction-like-jujutsu-shenanigans-or-realm-rampage/3127398
- VoxBreaker: https://devforum.roblox.com/t/voxbreaker-an-oop-voxel-destruction-module/2935099
- Wall-break technique thread: https://devforum.roblox.com/t/how-would-i-be-able-to-break-a-wall-into-a-bunch-of-smaller-parts-like-the-game-bulked-up-or-jujitsu-shenanigans/2912775
- Video frames: FloatyZone, "13 Destruction Experiments in Jujutsu Shenanigans..." https://www.youtube.com/watch?v=7F6IbI3BV8c (frames at 20–300 s, sampled via the Browser pane; stills only).
