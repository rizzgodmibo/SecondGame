---
tags: [playtest, project/trap-your-friends, visuals/retro, systems/destruction]
status: draft
updated: 2026-10-06
confidence: medium
---
# Trap Your Friends: style test v2, Map 1 slice (Studio, 2026-10-06)

## Holden's verdict (USER, 2026-10-06)
- "Decent". The destruction, the Trapper panel and the sockets work.
- **The sky is terrible** (a still painted image; he wants a living sky).
- **The trap models look low quality / cheap** (they function fine; the outline is decent).
- **The map is too small**; all 3 maps must be bigger.
- 16-player servers (4 Trappers + 12 Runners). Fixed Trapper zones. Traps become Blender meshes, the map stays studded parts. Time of day: later.
- Next: [[Trap-Your-Friends-v3-Plan]].

## TL;DR
- Built style test v2 in `places\StyleTest.rbxl` (Team Create) as planned ([[Trap-Your-Friends-Style-Test-v2-Plan]]): a **vertical slice of Map 1, Castle Sky Island** (gatehouse → causeway over the moat → courtyard → wall-walk → finish tower), **15 marked sockets with 12 traps** (8 families), the **JJS-style destruction rework**, black **Highlight outlines**, a **SelectionBox edge test**, our **painted skybox**, a new lighting pass, and a Studio-only **Trapper panel**. Legacy studs on the west half, our MaterialVariant on the east half, with a dark seam stripe. **Awaiting Holden's review; nothing is locked.**
- **Counts:**
  - ~935 parts in the build (860 visible in play), v1 had 988.
  - **30 Highlights** live (27 built + 2 noobs + 1 client-side dodgeball).
  - 138 SelectionBoxes when the edge test is on.
  - Client debris **peak 201 of the 250 cap**, 0 recycled, linger 10 s.
  - In ~50 s with both noobs looping: 36 cut hits, 209 boxes cut out, 9 catches.
- **Frame time (Studio on Holden's PC only):** 16.6–16.7 ms average (Studio's 60 fps cap), 18–20.9 ms worst frame with 119–170 debris alive. Server heartbeat 0.11 ms average, 0.32 ms max; physics max 0.32 ms; 2.4 kbps sent. **Not measured on a phone.** Samples while Studio wasn't the front window ran at a flat 66.7 ms (Studio's 15 fps throttle) and are left out.
- **Security (first client → server remote):** junk arguments, a non-triggerable trap, spam past the rate limit, presses during cooldown and a non-Trapper (even with a client-set attribute) were **all refused**; valid presses worked. No server errors all session.
- **Biggest weak spots:**
  - most debris still looks like uniform 1-stud cubes (not JJS slabs);
  - MaterialVariant studs make the east castle walls look like giant LEGO up close;
  - the boxing glove reads as a pink ball, not a glove;
  - the island is a flat green rectangle;
  - no sound yet (files ready, not imported).

## What was built
- **Environment:**
  - Grass in 16×16 chunks with 3 tones, layered dirt underside and hanging rocks, a moat with stone arches.
  - Gatehouse towers with banners (our emblem decal), courtyard keep walls with crenellations, wall-walk parapets, a finish tower with a flag.
  - 7 varied block trees (oak / pine / fruit, 0.9–1.35 scale), lamps, crates, barrels, tower flags, 3 distant floating islands.
- **Sky and light:**
  - Our painted 6-face skybox (puffy cartoon cumulus + a sea of clouds below), uploaded privately.
  - **Atmosphere off**: even light haze painted over the cloud sea below the horizon (seen in Studio). Lighting values are in `src/shared/Lighting/ModernRetro.luau` (v1 kept as `ModernRetroV1.luau`).
- **Traps (socket):**

  | Trap | Socket |
  |---|---|
  | Swinging Hammer | ceiling gantry |
  | Wrecking Ball | ceiling gantry |
  | Trapdoor | 4×4 |
  | Boxing Glove Wall | wall |
  | Bounce Pad | 2×2 |
  | Chomper | 2×2 |
  | Glass Floor | lane-wide |
  | TNT Brick | 2×2 |
  | Brick Wall | 4×4 |
  | Spike Pop | 2×2 |
  | Glue Plate | 4×4 |
  | Dodgeball Turret | wall |

  Empty sockets: one 2×2, one 4×4 and one wall socket. Every trap has googly eyes or a face, an idle animation, a tell → hit → recover cycle and a black outline.
- **Destruction:**
  - The server cuts each breakable part around the hit on whole-stud lines (pure `Rules/Fracture`, unit-tested) and keeps anchored remainder pieces, so the wall stands with a jagged hole.
  - Clients throw the removed boxes as slabs + chips that land and lie about 10 s, then sink.
  - Impact VFX: flash, streaks, dust (our texture), shake, FOV punch; a 60 ms local hit-stop.
  - A part rebuilds 10 s after its last hit and only with nobody within 10 studs.
- **Trapper panel (Studio-only):** HAMMER / GLOVE / TNT buttons (keys 1–3) with a cooldown shade, firing the validated `TriggerTrap` remote. Studio players are marked Trappers by the dev script.

## Observed in the playtests
- Both noobs loop their routes; the bounce launches them; the glass cracks over loops and then shatters; the chomper, spikes, trapdoor and moat catch them (noob shatter = demo only, still UNDECIDED).
- **The wall-smash works as Holden asked:** the Wrecking Ball punches a hole through the Brick Wall; the top course stays standing as a jagged arch; rubble lies on the courtyard floor for about 10 s; the wall rebuilds once things are quiet and nobody is near, then gets smashed again on a later swing.
- The TNT blows a crater in the wall-walk floor and the TNT body splits into big red slabs (the most JJS-like debris in the test).
- **Fixed during the test:**
  - the wrecking-ball gantry post blocked the east side (moved into the wall);
  - a noob stuck on the tower door corner (waypoint moved);
  - the Spike Pop face sank with the spikes (face marked Static);
  - the impact flash whited out the screen (now 0.4 transparent, smaller, a weaker light);
  - destruction stats now publish as workspace attributes.

## Screenshots (`Projects/Trap-Your-Friends/attachments/`)
- `tyf-v2-01-overview.jpg`: the island and castle over the sea of clouds.
- `tyf-v2-02-courtyard.jpg`: courtyard traps, the smashed wall arch and lingering rubble.
- `tyf-v2-03-causeway.jpg`: Bounce Pad, cracked Glass Floor, Swinging Hammer; both stud methods (round = variant on the left, square = legacy on the right).
- `tyf-v2-04-wallwalk-tower.jpg`: TNT Brick, Dodgeball Turret, finish.
- `tyf-v2-05-legacy-edges-off.jpg` / `tyf-v2-06-legacy-edges-on.jpg`: the SelectionBox edge test on the legacy half.
- `tyf-v2-07-wrecking-ball-frozen.jpg`: frozen 0.08 s after the ball hits the wall.
- `tyf-v2-08-tnt-frozen.jpg`: frozen 0.1 s after the TNT blast (flash, streaks, dust).
- `tyf-v2-09-trapper-panel-followcam.jpg`: follow camera with the dev HUD and Trapper panel (HAMMER on cooldown).
- `tyf-v2-10-phone-width-844.png`: the same frame **downscaled to phone width** (size check only, not an emulator or a phone).
- `tyf-v2-11-trap-closeups-sheet.jpg`: trap close-ups (hammer, chomper, spike pop, glove, causeway traps, TNT + turret).
- `tyf-v2-t01..t04-*.jpg`: the single close-ups.
- `tyf-v2-sky-preview.png`, `tyf-v2-textures-preview.png`: the art sheets.
- `tyf-v2-x-flash-too-strong-before-fix.jpg`: evidence of the whiteout before the fix.

![[tyf-v2-01-overview.jpg]]
![[tyf-v2-07-wrecking-ball-frozen.jpg]]
![[tyf-v2-11-trap-closeups-sheet.jpg]]

## Claude's honest critique (for Holden to judge; not decisions)
1. **Debris shape:** most fragments are still 1-stud cubes, because the cut stops at 1-stud pieces near the hit. JJS shows big irregular slabs. Options: merge neighbouring cut-out boxes into slabs on the client, cut walls on a 2-stud outer layer, or throw the outer pieces as whole slabs.
2. **Stud methods on walls:** the MaterialVariant puts studs on every face, so the east castle walls and merlons look like giant LEGO up close. Legacy studs only on tops read cleaner on walls. On floors both read; at phone size the variant studs soften.
3. **Environment still plain in places:**
   - the island is a flat green rectangle with no paths, flowers, rocks or height;
   - the castle stone is pale, with big plain wall faces;
   - the dark seam stripe reads like a road (test-only).
4. **Boxing glove** looks like a pink ball with eyes. It needs a real glove silhouette (thumb, cuff, laces).
5. **The courtyard gantry post** (west) still stands in the courtyard as an obstacle.
6. **The Brick Wall is rarely complete when runners are near.** It only rebuilds with nobody within 10 studs, so in a busy round it stays an arch. That's the rule Holden asked for, but it's worth judging in play.
7. **Island grass counts as a fall:** standing on the grass below the route is a catch. Fine for the moat; a design question for open ground.
8. **Hit-stop is local only** (debris and FX hold for 60 ms); Roblox can't pause the whole world.
9. **No sound:** the 18 SFX are ready and checked but not imported ([[Trap-Your-Friends-Sound-List]]).
10. The stud sign text is too long (wraps to 2 lines).

## Studio instances added or parked (for Holden; deletions are his)
- Built: `Workspace.StyleTestV2` (Environment + Route with sockets, traps, noob paths), Lighting values + `Sky` faces, collision groups.
- **Parked in ServerStorage, delete if unwanted:**
  - `ServerStorage.StyleTestV1` (v1 build; its code is replaced, so it won't run);
  - `ServerStorage.Baseplate_Template`;
  - `ServerStorage.SpawnLocation` (the template spawn from v1).
- Runtime only (not saved): `TYF_Noobs`, `Remotes`, the client debris pool, client FX folders.
- Vault file to delete: `attachments/tyf-v2-10-phone-844x390.png` (a cropped phone image that cut off the panel; replaced by `tyf-v2-10-phone-width-844.png`). Claude's delete was blocked by the safety check.

## Pitfalls found
- `screen_capture` resets the camera to Custom before grabbing the frame, so a Scriptable camera set once gets lost. Re-apply it every frame with `BindToRenderStep` after the camera priority.
- Studio drops to 15 fps when it isn't the front window, so frame numbers taken then are worthless.
- A `require` from `execute_luau` gets a separate module copy, so publish live stats as workspace attributes instead.
- Atmosphere haze paints over a skybox's below-horizon art.
- `CloneAndRequire`: clone the whole builder folder (not one module), or sibling requires stay cached.

## Related
[[Trap-Your-Friends]] · [[Trap-Your-Friends-Style-Test-v2-Plan]] · [[Trap-Your-Friends-Style-Test-v1-Feedback]] · [[Trap-Your-Friends-Art-Style-Guide]] · [[Trap-Your-Friends-Sound-List]] · [[Destruction-Modules-Audit]] · [[2026-10-05-Trap-Your-Friends-Style-Test]] · [[Roblox Studio MCP Quirks]]

## Sources
- Local Studio playtests by Claude Code, 2026-10-06 (MCP `execute_luau` stats and attributes, `get_console_output`, `screen_capture`). Code: `C:\Users\holde\Documents\GameDev\TrapYourFriends` (uncommitted after `411d4d4`).
