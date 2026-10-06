---
tags: [project/trap-your-friends, visuals/art-direction, playtest/feedback]
status: draft
updated: 2026-10-06
confidence: medium
---
# Trap Your Friends: Style Test v2 Feedback → v3 Spec

## Holden's verdict on style test v2 (USER, 2026-10-06)
- "it came out **decent**".
- **Sky:** "the sky is terrible, it's a still image, I want an actual good sky". Research other games and use the vault.
- **Traps:** "they seem to function fine, outline is decent, but they **look low quality / cheap**".
- **Map:** "it's small. Even though we're making 3, I want it **bigger** than the size it is now."
- **Server:** up to **4 Trappers and 12 Runners** when the server is full at **16/16**. This replaces the DRAFT server cap of 12 in [[Trap-Your-Friends-Round-Structure]].
- Still not locked: the style guide, the stud method, shatter vs ragdoll.

## 1. Sky: from a static painted box to a living sky (proposal)
**Why v2 looked bad:** one painted cube map with the clouds baked in. Nothing moves, the cloud sea is flat, and baked clouds never line up with the 3D world.

**What good Roblox skies do** (devforum + Roblox docs; stills/observations, not measured):
- **Layered**, not one image: a clean gradient skybox (sky colours only, no baked clouds) + the dynamic `Clouds` object (under Terrain; `Cover`, `Density`, `Color`; moves with `Workspace.GlobalWind`) + Atmosphere for the horizon blend + **3D cloud and island layers** in the world for depth.
- Custom sky domes: one devforum project used inverted sky-sphere meshes with an alpha gradient, recoloured live, so "the horizon colour smoothly differs from the sky colour, with colourable clouds" (devforum "Cool sky system", 2019).
- Moving elements: slow `SkyboxOrientation` rotation or drifting cloud meshes give motion cheaply.
- Skybox quality rules: seamless 360°, faraway-only content, a high enough resolution (Roblox downsamples large images).

**v3 sky spec (DRAFT):**
1. **Gradient skybox, no clouds painted in:** deep blue top → light cyan horizon → warm haze band; 6 faces generated from one equirectangular gradient so there are no seams.
2. **Dynamic `Clouds`:** Cover ~0.5–0.6, Density ~0.3, white with a slight warm tint; `GlobalWind` gentle so they drift.
3. **3D cloud sea below the island:** big puffy cartoon cloud meshes (Blender, soft toon shading, outlined like the traps), drifting slowly on the client, at 2–3 depth layers for parallax.
4. **Distant floating islands and castles** as silhouettes, with slow bobbing.
5. **Sun:** a stylised sun texture with `SunAngularSize` larger than default, plus light SunRays (0.05–0.1).
6. **Atmosphere** back on but tuned so it only tints the horizon (low Density, Offset set so it doesn't paint over the near cloud layer).
7. Optional later: a slow time-of-day drift per round (morning / noon / sunset) for variety.
8. Check the phone-size view, and low graphics quality (Clouds cost GPU, so test it without them).

## 2. Traps: from "cheap" to hero quality (proposal)
**Why they look cheap:** primitive parts with stuck-on googly eyes, flat colours, no bevels, no texture, and the faces don't match the bodies.

**Quality bar (from the vault):** the approved [[Rubber-Tower-Art-Style-Guide]] (v5 kit) standard: chunky forms, **hand-painted textures** with hard-edged detail, edge highlights and dark creases, `SurfaceAppearance` on MeshParts, built in Blender through [[Blender-To-Roblox-Pipeline]] and the `roblox-asset-pipeline` skill checks.

**v3 trap spec (DRAFT):**
- **Traps become Blender meshes** (the map stays part-built and studded). Chunky, **bevelled** cartoon shapes with a painted toon texture (light top, dark underside, edge highlight, a few hard-edged details) and **stud details** where they fit (studs on top faces, so they still belong in the retro world).
- **Faces are designed, not stuck on:** eyes and mouths are part of each model's shape language (angry brow on the hammer, big grin on the wrecking ball, actual teeth on the Chomper), modelled or painted in.
- **Outlines:** keep the black Highlight for now; compare against a Blender **inverted-hull** outline on 2 traps for quality and cost.
- **Shape language per family:** danger = spiky/angular, bounce = round and squashy, trick = wobbly, creature = blob plus teeth.
- **Animation quality:** squash-and-stretch on tells and hits, overshoot on recover, idle loops at different speeds so traps don't move in sync.
- **Fix v2's misreads:** the Boxing Glove must read as a glove (thumb, cuff, laces); no "ball with eyes".
- Start with **4 hero traps** (Swinging Hammer, Wrecking Ball, Chomper, Boxing Glove Wall). Get Holden's approval on those before redoing the rest.

## 3. Map size for 16 players (DRAFT targets)
| Target | Value (to tune) | Why |
|---|---|---|
| Players | 12 Runners + 4 Trappers (USER) | |
| Run time | 2:30–3:00 for an average runner incl. deaths | Matches the round structure |
| Route length | ~800–1,200 studs centreline | WalkSpeed 16; ~6–8 studs/s effective with obstacles and deaths |
| Path width | 20–32 studs main path; never under 12 | 12 runners must not jam |
| Branches | 2–3 alternative routes per section (short risky vs long safe) | Spreads runners; gives trappers choices |
| Trapper zones | 4 zones, one per Trapper (with fewer Trappers, zones merge) | No fighting over sockets; each Trapper "owns" a part of the map |
| Sockets | ~10–12 per zone (~40–48 per map) | Trappers fill ~6–8; empty ones keep it unpredictable |
| Checkpoints | Every ~30 s of running (5–6 per map) | Fair respawns |
| Footprint | Fold the route (switchbacks, a spiral up a tower, a loop around the castle) into roughly 400×400 studs | Keeps the island readable and streamable |
| Performance | Part budget and StreamingEnabled plan needed before building (16 players + debris) | roblox-performance skill |
- Map 1 (Castle Sky Island) outline idea: gatehouse start → moat causeway → courtyard (branches: wall-walk vs dungeon) → great hall → spiral tower climb → sky bridge to the finish keep.
- Plan first as a **top-down layout image** with zones, sockets, checkpoints and branches, for Holden to approve before building.

## Open questions
1. Trapper zones: fixed per Trapper, or free roam over the whole map?
2. OK to move traps to Blender meshes (the map stays parts)? This brings the vault's original art rule back for traps.
3. Time-of-day variety per round: yes or no?

## Related
[[Trap-Your-Friends]] · [[Trap-Your-Friends-Round-Structure]] · [[Trap-Your-Friends-Style-Test-v1-Feedback]] · [[Trap-Your-Friends-Trap-Catalogue]] · [[Lighting-And-Atmosphere]] · [[Rubber-Tower-Art-Style-Guide]] · [[Blender-To-Roblox-Pipeline]]

## Sources
- Holden's message after style test v2, 2026-10-06.
- Roblox docs, Clouds: https://create.roblox.com/docs/environment/clouds (Cover, Density, Color; must be under Terrain; moves with global wind).
- Devforum "Custom Skyboxes 101": https://devforum.roblox.com/t/custom-skyboxes-101/2849003 (seamless 360°, distant content only, cube-map conversion).
- Devforum "Cool sky system for our project": https://devforum.roblox.com/t/cool-sky-system-for-our-project/242166 (sliced inverted sky spheres, vertex-colour gradients, layered elements).
- Vault: [[Lighting-And-Atmosphere]] (Sky, Clouds and Atmosphere properties; Clouds cost GPU).
