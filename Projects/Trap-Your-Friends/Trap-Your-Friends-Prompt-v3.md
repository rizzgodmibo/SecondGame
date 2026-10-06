---
tags: [project/trap-your-friends, project/prompt]
status: draft
updated: 2026-10-06
confidence: medium
---
# Trap Your Friends: Claude Code Prompt for v3 Planning

## TL;DR
- Paste the block below into the Trap Your Friends Claude Code session after style test v2.
- It records Holden's v2 verdict, points Claude Code at every vault note that applies, and asks for **plans only** (Map 1 full layout, Sky v3, hero traps in two model routes, performance), then a stop.
- Built from [[Trap-Your-Friends-Style-Test-v2-Feedback]], [[Art Direction Feedback]], the AssetLibrary README, [[Roblox Asset Pipeline Skill]], [[Roblox Map Audit Skill]], [[Roblox Studio MCP Quirks]], [[Streaming-And-Instance-Streaming]], [[Performance-And-Profiling]], [[Destruction-Modules-Audit]], [[Trap-Your-Friends-Map-Plan]] and [[Trap-Your-Friends-Round-Structure]].

## The prompt

```text
Feedback on style test v2 and the next step. This is a PLANNING step: no building, no uploads, until I approve.

STEP 0: HOUSEKEEPING
- You may make ONE git commit now of the current v2 work, message "Style test v2" (the staged v1 deletions included). No other commits.
- I've saved the place with File → Save to File. Tell me the exact instances you still want me to delete; don't delete them yourself.

STEP 1: READ (in this order, all in E:\Vault unless noted)
1. Projects/Trap-Your-Friends/Trap-Your-Friends-Style-Test-v2-Feedback.md: my verdict, the sky research, the reference study of hit games, the two trap-model routes, the map-size targets, and the vault rules that apply.
2. Assets/Reference-Captures/Retro-Stud/sky-model-study-a-gag-sab-fisch.jpg and sky-model-study-b-babft-bss-doomspire.jpg (look at them).
3. Resources/Art Direction Feedback.md: my standing art rules. Grey form review before textures; renders before uploads; colour variation; crisp zones, no blurry noise; no part-built props (this is why the traps failed); no washed-out sky-island lighting.
4. C:\Users\holde\Documents\GameDev\AssetLibrary\README.md, plus the kitlib5 bake pipeline in AssetLibrary/models/rubber-tower-kit-v5/ and the generator scripts in rubber-tower-kit-v6-map/ (reuse them; don't reinvent).
5. Resources/Blender to Roblox Asset Pipeline.md, Visuals/Blender-To-Roblox-Pipeline.md, Resources/Roblox Asset Pipeline Skill.md (preflight: FAIL >20k tris or vertex colours; WARN >10k tris or textures >1024), Resources/Roblox Texture Upload Failures.md.
6. Resources/Roblox Map Audit Skill.md (real movement: WalkSpeed 16, JumpHeight 7.2, running-jump reach about 7.4 studs with margin) and Resources/Roblox Studio MCP Quirks.md (screenshots, camera, the 15 fps background throttle).
7. Systems/Streaming-And-Instance-Streaming.md, Systems/Performance-And-Profiling.md (mobile: under 1,000 draw calls and 1M triangles in view; 16.67 ms frame), Systems/Destruction-Modules-Audit.md.
8. Projects/Trap-Your-Friends/Trap-Your-Friends-Round-Structure.md, Trap-Your-Friends-Map-Plan.md, Trap-Your-Friends-Trap-Catalogue.md, Visuals/Lighting-And-Atmosphere.md.

STEP 2: RECORD MY VERDICT (USER, 2026-10-06) in the hub, the v2 playtest log and the style guide (still NOT locked)
- v2 came out decent. The destruction, trapper panel and socket idea work.
- The sky is terrible: a still painted image. I want an actual good, living sky.
- The traps function fine and the outline is decent, but the models look low quality and cheap.
- The map is too small. All 3 maps must be bigger than the v2 slice suggests.
- A full server is 16 players: up to 4 Trappers and 12 Runners. Update Round Structure, Map Plan (socket counts were sized for 3 Trappers) and Config.
- My answers: Trapper zones are FIXED, one per Trapper (they merge when there are fewer Trappers). Traps move to Blender meshes; the map stays part-built and studded. Time-of-day variety per round: later.

STEP 3: PLANS (write each as a vault note, link it from the hub, then report)

A) Map 1 full layout: Castle Sky Island for 12 Runners + 4 Trappers
- Targets (DRAFT, from the feedback note): 2:30–3:00 run for an average runner incl. deaths; about 800–1,200 studs of route centreline; main paths 20–32 studs wide, never under 12; 2–3 alternative routes per section (short and risky vs long and safe); 4 Trapper zones with 10–12 sockets each (about 40–48 total, mixed floor 2x2/4x4, wall, ceiling gantry, lane-wide); a checkpoint about every 30 s (5–6); the route folded into about 400x400 studs (switchbacks, a spiral tower climb, a loop around the keep).
- Start: a Runner start room with something to do during prep (Runners can't see the course; flag it if you think that rule is wrong). Finish: the keep/finish tower, visible from early in the route ("path to a glowing goal", Reference/X-Low-Poly-Builds-And-Maps.md).
- Trapper side: say where Trappers stand or fly during prep and the run, and how each zone is readable for them (outline colour or banner per zone). Recommend HUD buttons vs world buttons on a catwalk, with reasons.
- Every jump and gap within the measured reach; tag MapMustReach/MapNoReach so the roblox-map-audit skill can check the greybox later.
- Deliver: a top-down layout image (zones coloured, routes, branches, sockets with type icons, checkpoints, start/finish, scale bar in studs) saved in Projects/Trap-Your-Friends/attachments/, plus a section table (name, length, width, branches, sockets, checkpoint, expected time).
- Budgets: target part count for the full map, a draw-call/triangle estimate, and a StreamingEnabled plan (which models are Atomic, radius values) for 16 players plus destruction debris. Say how the debris cap scales with 16 players on phones.

B) Sky v3: a living sky
- Keep nothing from the v2 painted box except what you justify.
- Layers: a clean saturated gradient skybox with NO baked clouds (made from one equirectangular gradient so seams can't show); dynamic Clouds under Terrain (Cover about 0.5–0.6, Density about 0.3, drifting with Workspace.GlobalWind); 2–3 depth layers of 3D cartoon cloud meshes below and around the island (Blender, toon-shaded, outlined like the traps, drifting slowly on the client); distant floating-island and castle silhouettes; a stylised sun (bigger SunAngularSize, light SunRays 0.05–0.1); Atmosphere back on but tuned only for the horizon.
- Must not look washed out (my standing rule). Saturated like Steal a Brainrot's sky, and give each future map its own sky mood like Super Doomspire does.
- Include a low-graphics fallback (Clouds cost GPU) and test both.
- Deliver a mockup render or a Studio screenshot plan, the asset list (meshes and images to make), and the cost.

C) Hero traps: fix "cheap"
- Two model routes (details in the feedback note):
  Route A, voxel detail like Grow a Garden / Steal a Brainrot: many 0.25–0.5-stud cubes, each with a bevel/inset tile texture, merged into one mesh with an atlas.
  Route B, smooth chunky toon mesh at the Rubber Tower v5 quality bar: bevelled forms plus a painted texture bake.
- Make the Swinging Hammer in BOTH routes first, as grey forms (front, side, three-quarter renders), for me to pick a route BEFORE any texturing. Then the other 3 hero traps (Wrecking Ball, Chomper, Boxing Glove Wall; the glove must read as a glove with thumb, cuff and laces) in the chosen route.
- For each trap: shape language (danger = angular/spiky, bounce = round/squashy, creature = blob + teeth), a face designed into the form (not stuck-on spheres), colour zones with variation, stud details on top faces so it belongs in the stud world, triangle budget (under 10k), texture size (1024 max), outline method (Highlight vs a baked inverted hull: compare on 2 traps for look and cost), and an animation list (squash and stretch on the tell and hit, overshoot on recover, idles out of sync).
- Pipeline: dedicated Blender export scene, one GLB per trap (use_selection, use_active_scene), no vertex colours, atlas textures, preflight with the roblox-asset-pipeline skill, renders shown to me BEFORE any upload. No Roblox AI meshes, no Hunyuan3D.
- Uploads: no Open Cloud key is set up for this project. Say whether you want me to create one (I'd store it in a gitignored .secrets file myself) or whether I import through Creator Hub/Studio.

D) Also include
- An updated Map Plan (Maps 2 and 3) at the new size and socket count. I still choose the themes later.
- The full file list and the build order. My proposed order: (1) Sky v3, (2) hammer grey forms in both routes, then stop for my pick, (3) the other 3 hero traps, then stop for review, (4) the full Map 1 greybox with zones and sockets, audited with the map-audit skill, then stop.
- Gates for each step, and what you'll show me at each stop (renders, screenshots incl. a phone-width view, counts, frame time measured with Studio in front, an honest critique).

STEP 4: STOP
Show me the plans, the layout image and the file list, and ask anything that blocks you. Don't build until I say go.
```

## Related
[[Trap-Your-Friends]] · [[Trap-Your-Friends-Style-Test-v2-Feedback]] · [[Trap-Your-Friends-Claude-Code-Prompt]]

## Sources
- Holden's message after style test v2 and his request for a more detailed prompt pulled from the vault, 2026-10-06.
