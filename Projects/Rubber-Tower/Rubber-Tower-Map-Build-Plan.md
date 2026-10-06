---
tags: [project/rubber-tower, design/level]
status: draft
updated: 2026-10-05
confidence: medium
---
# Rubber Tower: map build plan, ground floor + segment 1 (PLAN ONLY)

Holden (USER, 2026-10-05): the next big step after his review of the test place is building the map with the kit. **Ground floor + segment 1 first, using the obby pieces, then stop for review** (as in [[Rubber-Tower-Map-v3-Critique]]). This note is the plan. **Nothing is built yet**, and every layout number is a PROPOSAL.

## TL;DR
- **2026-10-05 ~17:30, USER:** build 1 is "not an obby yet" (see *Build 1 critique* below). The new plan = the **combo rework** (every special piece as gameplay, real difficulty, 5–8 min measured) + a world-like hub, ground v3, cliff kit v2 and a real waterfall, starting with ONE vertical slice (hub + Lily Lake + Village Rooftops), then stop.
- **Scope:** valley floor + start plaza + S1 meadow (start → CP1, ~100 studs up). Then stop for Holden's review. S2–S4 untouched (greybox stays, hidden).
- **Built from** the staged kit in `ServerStorage.Kit` (557 models, uploaded today). No primitives except invisible colliders.
- **Order:** top-down layout sketch for Holden (1 image) → ground floor → S1 route → CP1 landmark → walls/backdrop → lighting → audit + timing → screenshots + self-critique → stop.
- **Must keep working:** checkpoint tags/`Index`, `BouncePad`/`IcePlatform`/`WobblePlatform` tags, fall send-back, the climb trace, and a **clear Leap of Faith lane** from the summit down to a landing cushion on the ground floor.

## Steps
1. **Layout sketch first (stop if Holden wants changes):** a top-down + side view of the 240×240 valley.
   - Start plaza with gate, pond, meadow zones, tree clusters, boulders.
   - The S1 route as a numbered path.
   - CP1 island, the reserved Leap lane and the landing zone.
2. **Ground floor** (S1 meadow palette, crisp zones):
   - `Checkpoint_Island`-style start plaza with a gate;
   - pond;
   - 3+ tree species with size/tint variation (batch b + asset library trees);
   - boulders, flowers, hedges;
   - the batch (f) shops placed where they'll live (only placed, not wired).
3. **S1 route, start → CP1** (PROPOSAL, 10–14 jumps; length tuned by the dev timer to the 5–8 min target):
   - Pieces: Meadow islets, `Bounce_Mushroom`/`Bounce_FlowerPad`, `Wobble_LilyPad`/`Wobble_Raft`, `Soft_HayBale`/`Soft_MossCushion` rests, `Climb_VineWall`/`Climb_Ladder`, `Move_RopeBridge`, one `Move_Windmill`.
   - Every jump inside the default-movement limits; the next platform is always visible.
4. **CP1 landmark:** `Checkpoint_Island` S1 + `Checkpoint_Beacon` S1, visible from the plaza; re-tag as checkpoint `Index` 1 at the same height (≈100) so the code needs no change.
5. **Walls as backdrop:** `Rampart_Wall` pieces with tints/moss, corner towers, uneven heights, gaps/arches looking out to the batch (e2) backdrop (mountains, floating islands, clouds). No pillar grid.
6. **Leap of Faith lane (from today's test):** a running leap carried the player ~30–40 studs out and hit a segment piece at y≈130.
   - Reserve a vertical column (~40×40 studs) under the summit's leap edge with nothing in it at any height.
   - Put the `Landing_Cushion` (or two) under it on the ground floor, sized for the measured drift.
7. **Lighting:** the vault obby preset (blue sky, Atmosphere ~0.2 sky-blue, Saturation ~+0.2, readable sun shadows).
8. **Checks before review:**
   - `roblox-map-audit` (S1 reachable with default movement);
   - dev segment timer runs;
   - walk-test every bounce/wobble/ice piece;
   - fall from S1 lands on soft ground or sends back;
   - tri/instance counts;
   - phone FPS in the emulator (Studio window visible!).
9. **Show Holden:** 4 angles (player-eye at spawn, on CP1 looking up, outside overview from a corner, a 150 px shrunk version), before/after next to the v2 shots, and an honest self-critique against [[Art Direction Feedback]]. Then **stop**.

## Files (proposed)
| File | What |
|---|---|
| `RubberTower/tools/BuildValleyS1.luau` (dev-only, `dev.project.json`) | Places kit models from a layout table; idempotent rebuild of `Workspace.Valley_v3` |
| `RubberTower/tools/layout_s1.luau` | The layout table (model name, CFrame, tint variant, tags) so the map is reviewable as text |
| Place only | `Workspace.Valley_v3` (new); the old `Workspace.Valley` greybox is hidden, and **Holden deletes it** when happy |
| No game-code changes expected | Checkpoint pads keep their tags and heights |

## Layout v1 REJECTED (USER, 2026-10-05, evening): "a classic linear obby"
The first sketch (`Assets/Rubber-Tower-Map-v3/01-layout-sketch-ground-s1.png`) was stopped before any build. Holden's critique:
- **What was wrong:**
  - One thin route up the west side; the rest of the valley is decoration.
  - Kit models sit next to the path instead of BEING the path.
  - A dotted line: no places, no moments, nothing to discover.
  - Special pieces barely used (a couple of bounces).
- **Wants:**
  1. **The models ARE the obby:** over shop rooftops and chimneys, up the windmill (inside/around its blades), up a giant tree / the fairy treehouse, across a pond on wobbly lily pads, along cliff ledges past the waterfall, through a cave/tunnel in the cliff, across the rope bridge, up the scaffold and spiral steps. Floating islands, crystals and mushrooms are stepping stones.
  2. **Use the whole valley:** the route wraps around (walls, centre, floating islands) and crosses over itself at different heights. From each area you see the next landmark and other players above and below.
  3. **Areas, not dots:** 4–6 themed "places" in S1, each with a moment (teach, test or twist one thing).
  4. **All unique pieces, introduced teach → test → twist** (bounce, wobble, ice teaser, soft rests, movement, climbing), with a plan for what S2–S4 bring back and twist.
  5. **Exploration:** 1–2 optional side paths per area that rejoin, hidden rubber ducks, the secret room off the route, goofy details.
  6. **Rules kept:**
     - default movement, phone-fair jumps;
     - the next landmark always visible;
     - an easy first jump, and the first fall within ~20 s lands soft;
     - 5–8 min for S1;
     - checkpoint tags and heights unchanged;
     - the Leap lane and splash pond clear;
     - shops on the ground floor.
- **Process:**
  - Two layout options, each with:
    - a top-down map;
    - a side view of the WHOLE tower route (S1 detailed, S2–S4 rough);
    - a 5–6 moment player's-eye storyboard.
  - Stop for his pick, then build, audit, timer, 4 angles + a fly-through, self-critique, and stop.
- What survives from v1: the valley floor mesh + splash pond (uploaded, asset 89785848208249), the leap pad v2, `tools/BuildValleyS1.luau` (generic kit placer, not yet run), the collider table (`art/map/kit_colliders.json`).

## Layout options A and B (2026-10-05) → **USER PICK: Option B "Through the Middle"**
**USER (2026-10-05, 15:28 EDT):**
- Option B. A detailed spec first (below), then build ground + places 1–3 with a check-in (4 screenshots + timer), then places 4–6 + CP1 + 5 ducks + the secret room, then checks, then stop.
- Windmill blades static first; a slow spin behind a Config toggle, which Holden decides after playing.
- The skyway under CP1 needs headroom; the figure-8 crossing must not allow a skip (no bounce from the skyway reaching the upper path); a fall from the upper crossing onto the skyway should be a funny catch, not a softlock.
- Missing kit pieces are made in the v5 style with the same pipeline + preflight.

Sheet: `Assets/Rubber-Tower-Map-v3/02-layout-options-A-B.png` (generator `RubberTower/art/map/options_s1.py`). Both options are PROPOSALS.
- **Option A, "Valley Ring":** S1 makes one big anticlockwise lap of the valley walls and ends with a sky bridge 90 studs above the village it started in (~835 studs of route).
  1. Village Rooftops
  2. Windmill Hill
  3. Cliff Pool Lily Pads (a pool shelf on the west cliff)
  4. Waterfall Ledges + Cave (tunnel behind the falls, secret room off it)
  5. Treetop Path (east)
  6. Sky Bridge Home (behind the splash pond, over the village, into CP1 from the south-west)
- **Option B, "Through the Middle":** a figure-8 crossing the valley centre twice (~708 studs). The skyway passes under CP1 at y~55, and the treetop bridge crosses back over it at y~90.
  1. Lily Lake (a ground-level meadow lake by the spawn; the first wobble, where a fall is a splash)
  2. Village Rooftops
  3. Windmill Climb (west wall)
  4. Crystal Skyway (across the middle, under CP1)
  5. Waterfall Ledges + Cave (east → north)
  6. Treetop Return (north-west → back over the skyway into CP1)
- **Both:**
  - pieces introduced teach → test → twist:
    - bounce: flower pad → mushroom → jelly;
    - wobble: lily pads → raft → jelly cubes / seesaw;
    - climbing: ladder → scaffold → vine wall / shelf fungus → spiral steps;
    - one frosty ledge as the ICE teaser;
    - soft rests (hay, moss cushion) after the hard bits;
    - rope bridge + tightrope (static).
  - 1 optional side path per area; 5 hidden ducks; the secret room behind the waterfall.
  - The Leap lane is clear (every route point and segment checked); CP heights/tags and shops on the ground are unchanged.
- **S2–S4 rough (both):**
  - S2 Mushroom Grove: bounce chains, shelf fungus/mushroom steps, vine conveyor*, swing paddles*, halfway shop at CP2.
  - S3 Crystal Caves: ICE becomes the main thing; frozen waterfall climb, fan-vent updrafts*.
  - S4 Cloud Kingdom: clouds, rainbow bridge, swing hammers*, slingshot*, spring pads; summit castle + Leap.
  - \* = needs new mover code, a separate PROPOSAL that needs Holden's OK.
- **Needed for either (PROPOSALS):**
  - New kit models: a walk-through cliff tunnel/cave; a giant meadow tree with walkable branches/canopies; for A, a cliff pool shelf; for B, a lake in the floor mesh (floor rebuild); maybe 2–3 village cottages so the rooftop street has enough roofs.
  - Roof colliders for the shops (builder work).
  - Windmill blades stay static until mover code is approved.
- **Time:** 5–8 min is a GUESS from route length (~50 obstacles) until the dev timer runs.

## Build 1 critique (USER, 2026-10-05 ~17:30 EDT) → combo rework
**Holden's words, condensed** (also logged in [[Rubber-Tower]]): "there's progress, but it isn't an obby yet, and parts of it look lazy. Your self-critique should have caught most of this."
1. The bottom isn't an obby. In Lily Lake you can just walk around: pads and raft sit on a shallow pond next to the grass, so there's no challenge and no fail. The special models are decoration.
2. The upper part is an obby but far too easy: ~20 of the same small plank/beam hops in a row (same gap, same size, no timing, no mechanics).
3. The hub is all the models huddled round the pond: "a pile of props", not a world with an obby mixed in.
4. The ground is lazy: one flat green with a sand ring, no height, paths, zones or detail.
5. The cliff walls are the same rock model stacked over and over, and he doesn't like the black lines/cracks on every rock: repetitive and fake.
6. The waterfall is a flat blue strip with dashes.
7. The floating islets in a row all look identical.

**What he wants (USER):**
- A. A REAL obby built from the special pieces, chained into combos (each section a little set piece). His examples:
  - bounce mushroom → vine wall;
  - wobbly lily pads over DEEP water (falling in = splash + swim back to the section start);
  - a seesaw log you run up as it tips;
  - ice slide → bounce pad → moving windmill blade;
  - the slingshot to a far floating island;
  - fan vents pushing you sideways across a gap;
  - timing jumps past swinging rubber hammers/paddles;
  - a chain of jelly cubes where each wobbles more;
  - a soft rest after each hard combo.
  - Every special piece is used as gameplay in S1; ice is saved mostly for S3.
- B. Real difficulty: vary gaps, heights, platform sizes (shrinking), direction changes, run-up jumps, precise landings, timing. Sawtooth teach → test → twist → rest, easy at the start gate to medium by CP1, phone-fair with default movement. A first-timer falls a few times and takes 5–8 min. **Measured** by playing it (fall count + time, honest about "still too easy").
- C. A hub that feels like a world:
  - a safe village with a clear START GATE that the spawn faces (with the tower behind it);
  - a square with the shops facing it, streets connecting districts (market, garden, pond, grove);
  - groves instead of scattered props, fences/hedges/walls framing spaces, breathing room;
  - height: hills, raised grass terraces, small cliffs, ramps/steps, a stream from the waterfall to the pond with a bridge.
- D. Ground: crisp v5 zones with curved borders: stone paths, dirt trails, flower beds, darker grass patches, grass edges over paths, pebbles. Not flat, not blurry.
- E. Walls: at least 5–6 different cliff/wall pieces (shapes, heights, overhangs) + colour variants, randomly rotated and scaled; **no black crack lines** (soft darker crevices + colour variation; this overrides the "dark cracks" line in [[Rubber-Tower-Art-Style-Guide]]); broken up with grass ledges, vines, trees, crystals, caves, arches, more waterfalls.
- F. A real waterfall: layered see-through sheets, white foam at the top and bottom, mist/splash particles, a splash pool.
- G. Islets varied in size, shape, tilt, colour and topper (tree, crystals, mushroom, little house).
- **Process (USER):** the combo list below first; then ONE vertical slice (hub layout + ground + start gate + Lily Lake + Village Rooftops at full quality, with the new walls and waterfall); then stop and show: spawn view, start gate, each combo, walls up close, ground from player height, fall count and time. Wait for his OK before the rest. Keep the Leap lane, checkpoint tags/heights, colliders, phone-friendliness.

**My self-critique miss (lesson):** I judged "does every jump pass the gap rule", not "is this fun, varied and hard enough". A route of 60 beats that all pass a 0.7-reach rule is exactly 20 copies of one easy hop. The checks need a variety/difficulty report (gap, rise, size and direction spread per place, timing/mechanic beats per place), not only a pass/fail.

**What the build-1 checks found (2026-10-05, evidence for the rework):**
- The RouteBot's `Humanoid.Jump = true` is ignored in MCP play sessions (no PlayerModule there); `ChangeState(Jumping)` jumps. Every bot timer before that fix is invalid.
- With real jumps (expert bot, default movement): places 1–5 = 7.1 + 4.3 + 7.0 + 11.8 + 11.9 s, place 6 ≈ 13–33 s, **≈ 60–70 s for S1, 0–1 falls**. That confirms point 2: far too easy and far too short.
- Fixed on the way (kept for the rework): windmill hatches + upright ladder 2 + gallery step crates; solid chimney collider; V7 bridge off the ridge; V4 leaf no longer over the shed; E4/E5 moved; tree pads 4/5 clear of the canopy; signs non-colliding; the builder now sets collision fidelity through `ApplyMesh` (direct assignment was silently ignored, which wrapped the windmill balconies in hull lumps).
- **Leap lane is NOT clear:** a real leap lands on the old S4 greybox `09_ledge` (y 317), and the computed lane also passes the old S3 `16_soft` (y 230). The ideal landing is the pond centre (0.5 off). To fix with the S2–S4 rework (move those two pieces, or re-aim the pad).
- Skip check (`art/map/skip_check.py`): no skip at the figure-8 crossing; four 2-beat local shortcuts inside places.
- Triangles (`art/map/tri_count.py`): 309k for ground + S1, of which the cliff walls are 127k (41%).

## Combo rework: S1 section-by-section (PROPOSAL, 2026-10-05; keeps Option B's route and 6 places)
How to read: each combo = pieces → the challenge → where a fall lands. Tier per [[Difficulty-And-Mastery]] (Tutorial ≤4 gap / ≥6 wide; Easy 4–6 / 4–6; Medium 6–8 / 2–4). Every place runs **teach → test → twist → rest**, and every hard combo ends on a soft rest (cream/white: hay, moss cushion, pillow, cloud). Timing windows ≥ 1 s, swing periods ≥ 3 s, every hazard telegraphed by red rubber colour + a whoosh sound. Times are first-timer guesses (falls included) to be **measured**.

### 1 Lily Lake: deep water (Tutorial → Easy, ~70–90 s, expect 1–3 falls)
The lake becomes a real deep basin (8+ studs of water, no wading). The shore is fenced/hedged on the village side, so you can only get round it on the pads. A fall = a splash, then you **swim** to the nearest combo-start jetty steps (swimming = Roblox terrain water in the basin, see mechanics).
- **1A "Jetty hop" (teach wobble):** jetty → 3 big lily pads (12 wide, gaps 3, level) in a straight line. Fall: water, swim 6 studs back to the jetty steps.
- **1B "Lily chain" (test):** 4 pads shrinking 12 → 9 → 7 → 5.5 wide, gaps 4 → 5 → 5.5, one 60° turn, the last pad a little lower. Fall: water, swim back to 1B's start pad.
- **1C "Jelly chain" (twist):** 3 jelly cubes on posts, each softer (spring k 1400 → 900 → 500: it tilts more), gaps 5, rise +1 each. Fall: water, swim to the 1C steps.
- **1D "Mushroom to vine" (combine, USER example):** a pink bounce mushroom on a rock in the lake throws you forward onto a vine wall on the west rock island; climb 10 to a grass ledge. Fall: water, back to 1D's rock.
- **Rest:** moss cushion + hay on the rock island top (the first soft rest), with the village roofs in view.
- **Side path:** "frog hop", 3 small pads (×0.6) to duck 1, rejoining at 1C.

### 2 Village Rooftops (Easy, ~70–90 s, 1–2 falls)
- **2A "Roof steps" (teach heights):** hay bale (rest) → shed roof (+1) → roof terrace (+3.9, a run-up jump).
- **2B "Seesaw log" (USER example):** a seesaw log from the terrace to the next roof: you run up it as it tips, then jump off the high end onto a ledge (+3). Too slow = it tips back and you slide off. Fall: the street, ~15 s back to the hay.
- **2C "Leaf launch" (bounce):** the giant roof-garden leaf throws you onto the thatched cottage's ridge (13 long, 3 wide).
- **2D "Paddle ridge" (twist, timing):** 2 swinging red rubber paddles sweep across the ridge (period 3.5 s, offset half a period). A bonk = a floppy ragdoll tumble into the street (soft hay piles there). Fall: the street, ~20 s back.
- **2E "Chimney tightrope":** chimney → tightrope (1 wide, 20 long) → windmill balcony 1. Fall: hay + fall net at the windmill foot, ~25 s back.
- **Rest:** balcony 1 (pillow).
- **Side path:** turret detour → duck 2.

### 3 Windmill Climb (Easy → Easy+, ~60–80 s, 1–2 falls)
- **3A "Ladder round" (teach climbing):** ladder 1 → walk round balcony 2 → ladder 2 (kept; built and bot-tested).
- **3B "Ice slide to the blade" (USER example; the ONE S1 ice teaser):** from the gallery a short icy chute slides you onto a pink bounce pad, which throws you onto a **slowly turning** blade spar.
- **3C "Ride the blade":** ride the spar up and jump off near the top of its turn onto the skyway's first islet (window ~1.5 s each 90°). Needs the spin turned on (see mechanics).
- **Rest:** a cloud pillow on the first skyway islet.
- Falls: each balcony is narrower than the one below; from the blades → windmill hill hay (costs more, ~45 s).

### 4 Crystal Skyway (Easy+ → Medium-, ~80–100 s, 1–3 falls)
- **4A "Raft + jelly" over the lake (test wobble high up):** raft → jelly cube (softest). Fall: the deep lake, swim to the windmill steps (costly, which is fair this high).
- **4B "Jelly jump" (bounce):** blue jelly (+12) onto an islet at CP1's edge.
- **4C "Shrinking crystals" (precision):** crystal shards 8 → 6 → 4 → 3 wide, gaps 5 → 6 → 6.5, two direction changes, passing UNDER CP1 (headroom kept ≥ 13).
- **Rest:** moss cushion under CP1.
- **4D "Slingshot" (USER example):** step into the slingshot pouch on a small islet; after a 0.6 s stretch it flings you on a fixed arc across the middle to a far floating island (replaces the old S11–S14 plank hops).
- Falls: the cloud catch layer ~12 below → walk back to 4B (~25 s).

### 5 Waterfall Ledges + Cave (Medium-, ~90–110 s, 2–3 falls)
- **5A "Vine wall + shelves" (test climbing):** vine wall (16) → shelf fungus ledges shrinking 6 → 4 → 3, alternating sides, with one run-up jump (gap 6.5).
- **5B "Fan gap" (USER example):** two fan vents in the cliff push you sideways across a 10-stud gap that is too far without the push. They run 2 s on / 1.5 s off, shown by a dust plume.
- **5C "Hammer ledge" (timing, USER example):** a narrow ledge (3 wide) with 2 swinging rubber hammers (period 3 s). A bonk knocks you onto the catch shelf below.
- **5D ice-spray ledge → bridge → the tunnel behind the falls** (the tunnel is the rest; secret room off it).
- Falls: the catch shelf at the cliff foot → back to 5A (~30 s).

### 6 Treetop Return: the final exam (Medium, ~80–100 s, 2–3 falls)
- **6A "Spiral pads" (varied, not identical):** pad sizes alternate 7 / 5 / 7 / 4, rises 3–4.5, one run-up jump across the trunk side, one direction reversal.
- **6B "Canopy tightrope":** canopy deck → tightrope → a wobbly rope bridge OVER the skyway (the funny catch onto the skyway's fall net is kept).
- **6C "Last combo" (combine):** jelly cube (soft) → seesaw log → small islet → drop onto CP1 (rest + checkpoint).
- Falls: pads → the tree's islet → vines up to pad 1 (~15 s); bridges → the skyway catch.

**S1 estimate:** ~8–9 min worth of content, so a first-timer lands at roughly 5–8 min with ~8–14 falls; an expert ~2.5–3 min. **To be measured** with the RouteBot (expert floor, real jumps) and Studio character navigation (a first-timer-like run that counts falls), then reported honestly.

**Every special piece in S1 as gameplay:** bounce mushroom/leaf/jelly (1D, 2C, 3B, 4B), lily pads + raft + jelly cubes (1A–1C, 4A, 6C), seesaw (2B, 6C), swing paddle (2D), swing hammer (5C), tightrope (2E, 6B), rope bridge (6B), windmill blade (3C), slingshot (4D), fan vent (5B), ladder/vine wall/shelf fungus (1D, 3A, 5A), ice (3B teaser + 5D only), soft rests (after every combo). Vine conveyor stays S2 (as the kit plans).

### Mechanics this needs (USER-approved 2026-10-05 ~17:45: "approve all")
- **USER water decision (replaces the terrain-water row below):** stylised mesh water in the v5 look, deep and dark in the middle, lighter edge band, painted ripples + lily shadows. Falling in = ragdoll, a big goofy splash + "bloop", bob up, then a ~1 s tween back to the combo start; counts as a fall (Bonk Survivor / Pro Faller); reused for the splash pond and all water hazards. Files added: `src/client/Controllers/WaterController.luau`, `src/server/Services/WaterService.luau` (validates, ragdolls, counts the fall), a `WaterSplash` remote, `Config.Water`.
- **USER:** windmill blades spin for combo 3B/3C (`Config.Map.WindmillSpin = true`).
| Mechanic | How (proposal) | Files |
|---|---|---|
| ~~Deep water + swim~~ (superseded, see above) | ~~Roblox **terrain water** fills the Lily Lake basin (and the pond), 8+ deep, so swimming is native; tuned to the v5 palette (`Terrain.WaterColor`, low `WaveSize`, transparency ~0.4). `SplashController` already fires the splash. Each combo start has jetty steps out of the water. | builder only (`tools/BuildValleyB.luau`); ⚠️ verify the terrain-water look against the low-poly style |
| Jelly chain "each wobbles more" | `WobbleController` reads an optional `WobbleStiffness` attribute (default = Config k 800). | `src/client/Controllers/WobbleController.luau` (edit), `Config.luau` |
| Seesaw log | Same local-copy pattern as wobble, but one `HingeConstraint` at the fulcrum (±22°), the client weight push tips it, and a weak spring returns it to level. Tag `SeesawPlatform`. | `WobbleController.luau` (edit) |
| Swing paddle / hammer | Anchored, animated on every client from `workspace:GetServerTimeNow()` (everyone sees the same phase, nothing replicates). Touching your own character → a knock along the swing direction + the existing ragdoll. Tag `SwingHazard`, attributes Period / Amplitude / Phase. | `src/client/Controllers/MoverController.luau` (new), `Config.luau` |
| Fan vent | A box zone per vent; while your root is inside and the vent is "on" (server-time rhythm), add a sideways velocity. Dust particles show on/off. Tag `FanVent`. | `MoverController.luau` |
| Slingshot | Touch the pouch → 0.6 s stretch (band anim + sound) → launch along a fixed arc (the Leap's launch code path, Physics state + velocity re-applied for 3 frames). No aiming, so it's phone-safe. Tag `Slingshot`, attribute `LaunchVelocity`. | `MoverController.luau` (+ reuse the `BounceController` launch helper) |
| Turning blade | `Config.Map.WindmillSpin = true` (the motor already exists). Holden had said static first, his call after playing; his new combo example asks for a moving blade. | `Config.luau` |
| Specs | Pure functions (swing angle at time t, fan on/off at time t, seesaw limits) with specs under the code gate. | `src/shared/MoverMath.luau` (new) + spec |

### Art this needs (PROPOSAL, v5 pipeline + preflight, private test place only)
- **Cliff kit v2:** 6 different pieces: tall slab, stepped terrace, overhang, buttress/pillar, arch, low rubble ridge. Each in 3 colour variants (warm tan, sandy, mossy). Soft darker crevices, no black lines. Grass ledges with drape, optional vines/trees/crystals sockets. Placed with random yaw/scale, never the same piece twice in a row.
- **Waterfall v2:** 3 layered alpha sheets (scrolling textures), a white foam lip at the top, a foam ring + mist/splash particles at the bottom, a splash pool basin; the stream mesh from the pool to the lake, with a wooden bridge.
- **Ground v3:** sculpted floor tiles with real height (a hill, raised grass terraces with small cliff edges, ramps and steps) and crisp painted zones (stone paths, dirt trails, flower beds, darker grass patches, grass fringe over path edges, pebbles). Split into tiles so the texture stays crisp at player height.
- **Hub re-layout:** a village square with the shops facing it, a market street, a garden, the pond district, a grove; fences/hedges framing them; a clear START GATE that the spawn faces, with the tower behind it.
- **Islet variants:** 4–5 shapes × size/tilt/colour, with toppers (tree, crystals, mushroom, little house).

### Vertical slice (do this first, then STOP for Holden)
Hub layout + ground v3 + start gate + Lily Lake (1A–1D) + Village Rooftops (2A–2E), with cliff kit v2 and waterfall v2 on the walls you can see from there. Show: spawn view, the start gate, each combo, walls up close, ground at player height, the fall count and time. Places 3–6 wait for his OK.

### Vertical slice BUILT (2026-10-05, ~19:10 EDT): stopped for Holden's review
Screenshots: `Assets/Rubber-Tower-Map-v3/slice-2026-10-05/` (00 plan, 01 spawn view, 02 START gate, 03–04 Lily Lake combos, 05 island + Miller's Yard, 06 hammer ridge, 07 waterfall, 08–09 ground at player height, 10 cliff kit sheet, 11 gate model).

**What's in the private test place (Workspace.Valley_v3):**
- **Hub v3:** a cobbled square (r 22) with the shops/boards facing in; the spawn faces the **Start_Gate_V3** (big 3D gold "START" on a blue board, checkered line) with Lily Lake and the tower behind it. Market street west to the Miller's Yard wall, garden district SE (campfire nook, hedges, swing bench), the pond district (splash pond = the Leap landing), groves of 1–2 species, a stream from the waterfall to the pond with a footbridge.
- **Ground v3** (`art/ground_v3.py`): 16 height tiles (66 studs, painted per texel with numpy: crisp curved zones, cobble paths with grass lips, dirt trails with pebbles, flower beds, dark grass patches, sand rings, terrace rock rims), raised terraces (SW +3, SE +2, NE hill +5) + ramps + mounds. Tiles have holes under the water; collision = precise decomposition.
- **Water hazards** (USER design): stylised mesh water (lake, pond, stream, pool), deep-dark middle, light edge band, ripple arcs, lily shadows. Fall in = splash + bloop, ragdoll, the fall counts, bob, ~1 s glide back to the combo start (10 return zones). A catch floor under the holes is a hazard too.
- **Cliff kit v2:** 7 shapes × 4 tints (tan / sand / moss / rose), angular faceted slabs over a solid core, soft darker crevices (no black lines), grass ledges, vines, ledge trees, glowing crystals, a cave mouth; placed with random shape/tint/yaw/scale, never the same shape twice in a row, two tiers on the N and E walls. Backdrop pyramids replaced by distant cliff mesas.
- **Waterfall_V2:** rock lip + foam, 3 layered see-through sheets, mist/streak/foam particles (play mode), set into the north wall with the ground pool + stream below; a second fall on the west wall.
- **Lily Lake (deep):** 1A 3 big pads → 1B 4 shrinking pads with turns (stiffer springs on the small ones so they tilt like the big one) → 1C 3 jelly cubes on piles, k 1400 / 900 / 500 → the seesaw log (rests far end up, tips as you cross) → 1D a pink mushroom tilted 35° (LaunchSpeed 70) throws you at the rock island's vine wall → climb → moss cushion rest.
- **Village Rooftops (the walled Miller's Yard, only reachable across the lake):** island → drop to the shed roof → run-up jump to the terrace → leaf bounce (LaunchSpeed 75) → the thatch ridge with 2 swinging rubber hammers (3.6 s, ±55°, same phase) → chimney → tightrope (walk collider widened to 1.4) → windmill balcony 1. Falls land in the yard; a crate stile lets you climb OUT of the yard, never in.

**Code (gate PASS, 56 specs):** `MoverController` (swings / fans / slingshot, server-time synced), `WaterController`, `HazardService` (validates water/bonk claims, ragdolls, counts water falls), `WobbleController` (seesaw hinge + `WobbleStiffness`), `Rules/Movers` + `tests/Movers.spec.luau`, `Config.Movers/Seesaw/Water`, `Map.WindmillSpin = true`, 2 remotes.

**Measured (Studio, default movement):**
- Expert-style bot (aims its jumps, steers in the air, real jumps): spawn → windmill balcony 1 in **154 s including ~3 bot stuck-timeouts (≤25 s each)**, so roughly **80–100 s of real play**: Lily Lake ~70 s, rooftops ~30 s. **Falls: 0 in the lake, 2 on the rooftops (hammer bonks).**
- A clumsier bot (jumping off the dipped edge of a tilting pad) fell **15–24 times in a row** on 1B's small pads. So the small wobbly pads punish late jumps.
- Studio's character navigation passed some pad jumps, then reported "Path Blocked" on fair ones and "Success" while ending in the water: not usable as a playtester.
- **Honest estimate (a GUESS until Holden plays it on a phone):** a first-timer takes 3–5 min for places 1–2 with 4–8 falls (1B, the jelly chain, the mushroom aim and the hammers). Places 3–6 are still build 1, so S1 can't be timed yet.
- **Is it still too easy?** Lily Lake 1A is tutorial-easy on purpose. 1B, 1C, the mushroom throw and the hammers have real fails and are not trivial for a bot. The rooftop steps 2A–2C are still easy. Overall it's Tutorial → Easy as planned; the medium by CP1 comes from places 3–6.

**Fixed during the build (checks found them):**
- Streaming: hammer models arrived before their arms, so they never moved. Now Atomic streaming + a retry.
- The server rejected water claims (its copy of a falling body lags ~9 studs high). It now allows up to 30 studs above the water.
- Float-back looped: a limp body slid off a wobbling pad. Now it lands just above the combo start and the body is held still until the ragdoll ends.
- Untextured ground: the JPEG GLB came in with no textures; switched to PNG.
- Blender's save of generated images wrote black PNGs; switched to our own PNG writer.
- The old `TestPlace.LeapTest` cushion sat in the new lake: parked, not deleted.
- The waterfall stood in a wall gap with floating side rocks; moved into the wall.
- The yard's lavender brick wall and the spiky hedge were redone.

**Self-critique** (against [[Art Direction Feedback]] and "does it feel like climbing through a world?"):
- Better:
  - the spawn reads at once (START gate, lake, tower);
  - crisp painted ground with real paths and zones;
  - varied cliff walls with no black lines;
  - water that reads deep;
  - every lake piece is gameplay now.
- Still weak:
  - The Miller's Yard is cramped (island, cottages, windmill and hay jammed together), and the stepped cottage reads as a plain white box.
  - The market street is cluttered (the tutorial hut crowds it) and the noticeboard is a blank white panel.
  - The square is a big plain cobble disc.
  - The waterfall sheets still read as one streaky strip in still shots.
  - The ground is slightly soft at player height (~15 px/stud), and the grass two-tone is subtle.
  - The hammer frames are thin poles.
  - The sky over the hub is crowded by the old S2–S4 greybox.
  - Some cliff slabs read as stacked bricks.
- Not done yet:
  - the Leap lane is still blocked by the S3/S4 greybox;
  - places 3–6 are build 1;
  - the fan vents and slingshot are coded and spec-tested but not placed (places 4–5);
  - the bloop/whoosh sounds are built-in placeholders.

**For Holden (Studio):**
- Parked, nothing deleted: `ServerStorage.Greybox_Hidden.TestPlace_LeapTest_parked`.
- Dev-only, delete when done: `Workspace.TestPlace.DevSliceBot` (the playtest bot module).
- Superseded kit copies you can delete: `ServerStorage.Kit.Ground3`, `ServerStorage.Kit.Ground3B`.

## Option B detailed spec (2026-10-05, Claude; numbers are PROPOSALS checked by `art/map/layout_b.py`)
> **Superseded in part (2026-10-05 ~17:30):** the beat lists below are build 1, which Holden rejected as "not an obby yet". The combo rework above replaces the challenges; the route, places and heights stay.
**How to read it:**
- One file (`RubberTower/art/map/layout_b.py`) generates the Studio layout (`tools/LayoutB.luau`), the floor paths/lake/pond, and the tables below.
- It checks every beat:
  - edge-to-edge gap <= 70% of a default jump's reach (WalkSpeed 16, JumpHeight 7.2, gravity 196.2) and rise <= 4.5;
  - bounces: rise 7-17, gap <= 8;
  - headroom under CP1;
  - no skyway bounce reaching the upper path;
  - nothing inside the Leap lane.
- Current result: **NO PROBLEMS, 60 route beats + 25 side/catch nodes**.
- "A fall lands on" = the highest walkable surface under the beat's centre and corners. "ground (y1)" listed next to a catch means only a corner overhangs.

**Whole-tower picture:**
- S1 0 -> 101; S2-S4 rough as in the options sheet.
- Figure-8: the skyway passes UNDER CP1 at y 64-66; the treetop bridges come back OVER it at y 105-108 and drop onto CP1 from the north.
- **No skip:** the only skyway bounce (S5, y 52) is 40+ studs west of the upper path, and the height difference is 37+ studs (a bounce reaches 20.6).
- **Funny catch:** a fall from the upper bridges lands on the skyway's S11 islet / S10 fall net. That sets you back to the end of the skyway, not a softlock (the skyway leads straight on to place 5).
- **Headroom:** the CP1 island (kit island x2) bottom is y 79.4. Skyway beats under it are at 64.4-65.7, so 13.7-15 studs clear (a jump + body needs ~12.5).
- **Leap lane:** clear; checked for every placement.

### 1 Lily Lake (y 1 -> 4, ~45 s)
- **Teach** wobble on wide lily pads (12 studs) right by the spawn.
- **Test:** pads turned and further apart, then the raft (tilts more).
- **Soft rest:** the shore.
- **Falls:** knee-deep water everywhere (a splash, wade to any pad or the shore); the first fall in ~20 s is soft.
- **Side path:** "frog hop", 3 smaller pads (x0.6) north to **duck 1**; rejoins at the raft.
- **Dressing:** reeds, lily clusters, a frog on a lily pad, the fishing gnome, a "Wobbly" signpost and the S1 gate at the jetty, lanterns.
- **You see:**
  - the windmill across the lake (next);
  - the skyway crystals right above the lake and players bouncing on its jelly;
  - CP1's island + beacon over the middle.
- **Mood:** sparkly water, warm jetty lantern.

### 2 Village Rooftops (y 5 -> 24, ~60 s)
- **Teach** bounce: a giant leaf in the stepped cottage's roof garden throws you onto the thatched cottage's long ridge (a 13-stud target).
- **Test:** roof steps (shed -> terrace, +3.9).
- **Twist:** the 3-wide ridge walk -> chimney.
- **Soft rest:** the haystack start, the rope bridge.
- **Falls:** the village lane at street level, ~15 s back to the haystack (cheap).
- **Side path:** the turret detour (**duck 2** by the flag; best view of the windmill + skyway).
- **Dressing (shops on the ground, placed only, not wired):** the hat shack, Caravan, kiosk, stall, quest board, bell tower, Bonk Clinic, campfire + benches; plus a scarecrow, flower boxes and chimney smoke puffs.
- **You see:** the windmill balcony across the rope bridge, the lake below, the skyway + CP1 ahead.
- **Mood:** glowing cottage windows, lantern posts.

### 3 Windmill Climb (y 23 -> 47, ~70 s)
- **Teach** climbing: ladder 1, with balcony 1 under you.
- **Test:** walk round the narrower balcony 2 to ladder 2 on the far side.
- **Twist:** walk the 3.4-wide blade spar 46 up, then jump off its tip onto the skyway.
- **Soft rest:** the gallery under the blades.
- **Falls:**
  - each balcony is narrower than the one below, so you land a level down;
  - **costs more (~45 s):** from balcony 1, the gallery or the spar you land on the windmill hill (hay + fall net), then go back through the village;
  - a cloud catch under the skyway start drops you back onto balcony 2.
- **Side path:** the south blade spar (**duck 3** at its tip).
- **Blades: STATIC** (USER). A slow spin is ready behind `Config.Map.WindmillSpin = false` (HingeConstraint motor, ~4 deg/s); Holden decides after playing.
- **Dressing:** haystacks + fall net at the foot, flour sacks, balcony lanterns, a "Don't Look Down" sign at the spar.
- **You see:** the whole lake + village below, the skyway crystals leading east under CP1, the treetop bridges high over the middle.

### 4 Crystal Skyway (y 48 -> 68, ~90 s)
- **Test:** wobble over the lake (raft, purple jelly cube), then a bounce (blue jelly, +12) onto an islet at CP1's edge.
- Pass **under CP1**: a moss cushion rest right under the island.
- **ICE teaser:** a wide frozen puddle islet (a ~4.6-stud slide).
- Crystal steps, then the fall net under the treetop bridge, then meadow islets east.
- **Falls:**
  - over the lake -> water;
  - after that, a **cloud catch layer** ~12 below (soft clouds + islets) walks back to the S5 bounce (~25 s).
- **Side path:** the crystal shortcut (one small, harder crystal skipping the cushion).
- **You see:** CP1's underside + beacon light, players on the treetop bridge above, the splash pond and leapers to the south-east, the east cliff + waterfall ahead.
- **Mood:** cyan crystal glow, soft clouds.

### 5 Waterfall Ledges + Cave (y 68 -> 94, ~90 s)
- **Test** climbing: the vine wall up the east cliff (16 studs), ledges round the NE corner (shelf fungus, secret ledge, stump).
- **Twist:** the frosty ledge in the waterfall spray (ice), then a wooden bridge into the **tunnel behind the falls**.
- **Falls:**
  - east ledges -> the catch shelf (logs at the cliff foot), walk back to the vine wall (~25 s);
  - north path -> the north catch shelf, back east (~40 s);
  - the tunnel can't be fallen out of.
- **Side paths:**
  - the catch shelf is also the scenic lower path (**duck 4** at its NE end);
  - the **secret room** through the tunnel's side door (Nosy Noodle; the Disco Duck dance spot; **duck 5**).
- **Dressing:** two stacked waterfalls, glow crystals + moss in the tunnel.
- **You see:** the whole valley, the skyway below, the windmill across, the giant tree ahead.
- **Mood:** waterfall mist, cyan cave glow.

### 6 Treetop Return (y 94 -> 108 -> CP1 101, ~60 s)
- **Test:** the tree's spiral pads (+4 each, 0.7 gaps): a climbing rhythm.
- **Combine:** rope bridges back OVER the skyway, descending onto CP1 from the north.
- **Falls:**
  - pads -> the tree's floating islet -> vines up the trunk to pad 1 (~15 s);
  - bridges -> the skyway (funny catch) or CP1.
- **Side path:** the vine climb from the islet (scenic).
- **You see:** CP1's beacon ahead, players on the skyway below, the summit stack above, the windmill across.
- **Mood:** fireflies + a lantern in the tree, golden beacon.

**S1 total ~7 min** (45+60+70+90+90+60 s): a GUESS until the dev timer runs. A scripted bot run gives the expert floor, and Holden's phone run gives the median.

**Kit pieces made for this layout (v5, same pipeline + preflight, uploaded to the private test place):**
- `Giant_Windmill` (+ walkable `Blades`, `Sails`), `Cottage_Stepped`, `Cottage_Thatch`, `Cliff_Tunnel`, `Giant_Meadow_Tree`: asset 108426222163735.
- `Lake_Basin` + floor v2 (lake hole, Option B paths) + `Pond_Basin`: asset 76476942044528.
- Skyway platforms and stepping stones reuse kit islets, crystal shards, clouds and nets.

**Beat tables (generated; `#` = beat id):**

**1 Lily Lake**

| # | Beat | Piece | Top y | Gap → next | Rise → next | A fall lands on |
|---|---|---|---|---|---|---|
| L0 | Plank_Platform_M | `Plank_Platform_M` | 1.9 | 1.8 | -0.8 | ground (y1), Lily Lake water (soft) |
| L1 | Wobble_LilyPad | `Wobble_LilyPad` | 1.1 | 0.0 | +0.0 | Lily Lake water (soft) |
| L2 | Wobble_LilyPad | `Wobble_LilyPad` | 1.1 | 0.0 | +0.0 | Lily Lake water (soft) |
| L3 | Wobble_LilyPad | `Wobble_LilyPad` | 1.1 | 0.0 | +0.9 | Lily Lake water (soft) |
| L4 | Wobble_Raft | `Wobble_Raft` | 2.0 | 0.0 | -0.9 | Lily Lake water (soft) |
| L5 | Wobble_LilyPad | `Wobble_LilyPad` | 1.1 | 2.4 | +3.9 | ground (y1), Lily Lake water (soft) |

**2 Village Rooftops**

| # | Beat | Piece | Top y | Gap → next | Rise → next | A fall lands on |
|---|---|---|---|---|---|---|
| V1 | Haystack | `Haystack` | 5.0 | 1.5 | +1.1 | ground (y1) |
| V2 | V2 Cottage_Stepped shed roof | `Cottage_Stepped` | 6.1 | 0.2 | +3.9 | ground (y1) |
| V3 | V3 Cottage_Stepped roof terrace | `Cottage_Stepped` | 10.0 | 0.0 | +1.7 | ground (y1) |
| V4 | Bounce_Leaf | `Bounce_Leaf` | 11.7 | 5.0 | +9.3 | V2 Cottage_Stepped shed roof, ground (y1) |
| V5 | V5 Cottage_Thatch ridge walk | `Cottage_Thatch` | 21.0 | 0.2 | +3.2 | ground (y1) |
| V6 | V6 Cottage_Thatch chimney | `Cottage_Thatch` | 24.3 | 0.0 | +0.0 | V5 Cottage_Thatch ridge walk, ground (y1) |
| V7 | Move_RopeBridge | `Move_RopeBridge` | 24.3 | 0.0 | -1.2 | ground (y1) |

**3 Windmill Climb**

| # | Beat | Piece | Top y | Gap → next | Rise → next | A fall lands on |
|---|---|---|---|---|---|---|
| W1 | W1 balcony 1 (bridge end) | `Giant_Windmill` | 23.0 | 0.0 | +10.6 | ground (y1) |
| W2 | W2 ladder 1 (truss) | `Giant_Windmill` | 33.6 | 0.0 | -0.6 | W1 balcony 1 (bridge end), ground (y1) |
| W3 | W3 balcony 2 (walk round, narrower) | `Giant_Windmill` | 33.0 | 11.6 | +0.0 | S1_V7_Move_RopeBridge, W1 balcony 1 (bridge end), ground (y1) |
| W4 | W4 balcony 2 north side (walk round) | `Giant_Windmill` | 33.0 | 0.0 | +10.6 | ground (y1) |
| W5 | W5 ladder 2 (truss) | `Giant_Windmill` | 43.6 | 0.0 | -0.6 | W4 balcony 2 north side (walk round), ground (y1) |
| W5b | W5b top deck (ladder 2 end) | `Giant_Windmill` | 43.0 | 10.1 | +0.0 | W4 balcony 2 north side (walk round), ground (y1) |
| W6 | W6 gallery under the blades (walk round the deck) | `Giant_Windmill` | 43.0 | 0.0 | +4.4 | ground (y1) |
| W7 | W7 north blade spar (plank walk) | `Giant_Windmill` | 47.4 | 1.3 | +1.0 | W6 gallery under the blades (walk round the deck), ground (y1) |

**4 Crystal Skyway**

| # | Beat | Piece | Top y | Gap → next | Rise → next | A fall lands on |
|---|---|---|---|---|---|---|
| S1 | Meadow_Islet_S | `Meadow_Islet_S` | 48.4 | 2.1 | +1.0 | S1_C1_Soft_Cloud_M, ground (y1) |
| S2 | Wobble_Raft | `Wobble_Raft` | 49.4 | 3.7 | +1.0 | S1_C1_Soft_Cloud_M, ground (y1), Lily Lake water (soft) |
| S3 | Crystal_Shard_Platform_M | `Crystal_Shard_Platform_M` | 50.4 | 1.1 | +1.0 | Lily Lake water (soft) |
| S4 | Wobble_JellyCube | `Wobble_JellyCube` | 51.4 | 0.5 | +0.5 | Lily Lake water (soft) |
| S5 | Bounce_Jelly_M | `Bounce_Jelly_M` | 51.9 | 1.2 | +12.0 | S1_L2b_Wobble_LilyPad, Lily Lake water (soft) |
| S6 | Meadow_Islet_M | `Meadow_Islet_M` | 63.9 | 4.2 | +0.5 | S1_C2_Soft_Cloud_M |
| S7 | Soft_MossCushion | `Soft_MossCushion` | 64.4 | 4.8 | +0.5 | S1_C3_Soft_Cloud_M, S1_C2_Soft_Cloud_M, ground (y1) |
| S8 | Ice_PuddleIslet | `Ice_PuddleIslet` | 64.9 | 5.0 | +0.5 | S1_C3_Soft_Cloud_M, ground (y1) |
| S9 | Crystal_Shard_Platform_S | `Crystal_Shard_Platform_S` | 65.4 | 4.4 | +0.3 | S1_C4_Soft_Cloud_M |
| S9b | Crystal_Shard_Platform_S | `Crystal_Shard_Platform_S` | 65.7 | 0.0 | +0.4 | S1_C4_Soft_Cloud_M, ground (y1) |
| S10 | Soft_FallNet | `Soft_FallNet` | 66.1 | 4.2 | +0.3 | S1_C5_Meadow_Islet_L, ground (y1) |
| S11 | Meadow_Islet_M | `Meadow_Islet_M` | 66.4 | 4.4 | +0.5 | S1_C5_Meadow_Islet_L, ground (y1) |
| S12 | Stump_Platform_L | `Stump_Platform_L` | 66.9 | 2.4 | +0.5 | S1_C5_Meadow_Islet_L |
| S13 | Log_Platform_M | `Log_Platform_M` | 67.4 | 2.8 | +0.5 | S1_C6_Meadow_Islet_L, S1_C5_Meadow_Islet_L |
| S14 | Meadow_Islet_S | `Meadow_Islet_S` | 67.9 | 4.8 | +1.0 | S1_C6_Meadow_Islet_L, ground (y1) |

**5 Waterfall Ledges + Cave**

| # | Beat | Piece | Top y | Gap → next | Rise → next | A fall lands on |
|---|---|---|---|---|---|---|
| E1 | Stump_Platform_L | `Stump_Platform_L` | 68.9 | 3.9 | +1.0 | S1_C7_Meadow_Islet_L |
| E2 | Log_Platform_M | `Log_Platform_M` | 69.9 | 6.2 | +16.3 | S1_C7_Meadow_Islet_L, ground (y1) |
| E3 | Climb_VineWall | `Climb_VineWall` | 86.2 | 1.7 | +0.7 | S1_E0c_Log_Platform_M, ground (y1) |
| E4 | Plank_Platform_M | `Plank_Platform_M` | 86.9 | 3.0 | +1.3 | S1_E0c_Log_Platform_M, ground (y1) |
| E5 | Climb_ShelfFungus_M | `Climb_ShelfFungus_M` | 88.2 | 5.6 | +1.0 | S1_E1c_Log_Platform_M, ground (y1) |
| E6 | Secret_Ledge | `Secret_Ledge` | 89.2 | 5.6 | +1.0 | S1_E2c_Log_Platform_M, ground (y1) |
| E7 | Climb_ShelfFungus_M | `Climb_ShelfFungus_M` | 90.2 | 5.4 | +1.0 | S1_E2c_Log_Platform_M, ground (y1) |
| E8 | Stump_Platform_M | `Stump_Platform_M` | 91.2 | 3.2 | +1.0 | S1_E3c_Log_Platform_M, ground (y1) |
| E9 | Plank_Platform_M | `Plank_Platform_M` | 92.2 | 2.2 | +0.5 | S1_N1_Log_Platform_M, S1_N2_Log_Platform_M, ground (y1) |
| E10 | Ice_CrystalLedge | `Ice_CrystalLedge` | 92.7 | 0.1 | +1.3 | S1_N2_Log_Platform_M, ground (y1) |
| E11 | Wood_Bridge_M | `Wood_Bridge_M` | 94.0 | 0.0 | +0.0 | S1_N3_Log_Platform_M, S1_N2_Log_Platform_M, ground (y1) |
| E12 | E12 tunnel behind the waterfall | `Cliff_Tunnel` | 94.0 | 2.4 | +0.0 | ground (y1) |

**6 Treetop Return**

| # | Beat | Piece | Top y | Gap → next | Rise → next | A fall lands on |
|---|---|---|---|---|---|---|
| T1 | Wood_Bridge_M | `Wood_Bridge_M` | 94.0 | 1.6 | +0.5 | S1_N6_Log_Platform_M, ground (y1) |
| T2 | Meadow_Islet_S | `Meadow_Islet_S` | 94.5 | 0.0 | +0.0 | T0c floating islet under the tree (catch), ground (y1) |
| T3 | Wood_Bridge_M | `Wood_Bridge_M` | 94.5 | 0.0 | -2.5 | T0c floating islet under the tree (catch) |
| T4 | T4 tree pad 2 | `Giant_Meadow_Tree` | 92.0 | 0.7 | +4.0 | T0c floating islet under the tree (catch) |
| T5 | T5 tree pad 3 | `Giant_Meadow_Tree` | 96.0 | 0.7 | +4.0 | T0c floating islet under the tree (catch) |
| T6 | T6 tree pad 4 | `Giant_Meadow_Tree` | 100.0 | 0.7 | +4.0 | T0c floating islet under the tree (catch) |
| T7 | T7 tree pad 5 | `Giant_Meadow_Tree` | 104.0 | 0.0 | +4.0 | T0c floating islet under the tree (catch) |
| T8 | T8 canopy deck | `Giant_Meadow_Tree` | 108.0 | 0.8 | -0.5 | T6 tree pad 4, T5 tree pad 3, T0c floating islet under the tree (catch) |
| T9 | Move_RopeBridge | `Move_RopeBridge` | 107.5 | 0.0 | -1.5 | T4 tree pad 2, T0c floating islet under the tree (catch), ground (y1) |
| T10 | Meadow_Islet_M | `Meadow_Islet_M` | 106.0 | 0.0 | -0.5 | S1_S11_Meadow_Islet_M, ground (y1) |
| T11 | Move_RopeBridge | `Move_RopeBridge` | 105.5 | 0.0 | -4.5 | CP1 top (claim pad), S1_S11_Meadow_Islet_M, ground (y1) |

**CP1**

| # | Beat | Piece | Top y | Gap → next | Rise → next | A fall lands on |
|---|---|---|---|---|---|---|
| CP1 | CP1 top (claim pad) | `Checkpoint_Island_S1` | 101.0 | — | — | S1_S8_Ice_PuddleIslet, ground (y1), Lily Lake water (soft) |

**Side paths, catches and secrets**

| Node | Piece | Top y | Note | A fall lands on |
|---|---|---|---|---|
| L2a | `Wobble_LilyPad` | 1.0 | frog hop (smaller pads) | Lily Lake water (soft) |
| L2b | `Wobble_LilyPad` | 1.0 | frog hop | Lily Lake water (soft) |
| L2c | `Wobble_LilyPad` | 1.0 | frog hop -> duck, rejoins at the raft | Lily Lake water (soft) |
| V3a | `Cottage_Stepped` | 15.0 | V3a turret (side) | V3 Cottage_Stepped roof terrace, ground (y1) |
| W7a | `Giant_Windmill` | 47.4 | W7a south blade spar (side) | W6 gallery under the blades (walk round the deck), S1_V4_Bounce_Leaf, ground (y1) |
| S7a | `Crystal_Shard_Platform_S` | 65.4 | crystal shortcut (harder) | S1_C3_Soft_Cloud_M, ground (y1) |
| E1c | `Log_Platform_M` | 71.9 | catch shelf (lower path back to the vine wall) | ground (y1) |
| E2c | `Log_Platform_M` | 71.9 | catch shelf (lower path back to the vine wall) | ground (y1) |
| E3c | `Log_Platform_M` | 72.9 | catch shelf (lower path back to the vine wall) | ground (y1) |
| E0c | `Log_Platform_M` | 70.9 | catch shelf start (by the vine wall foot) | ground (y1) |
| C1 | `Soft_Cloud_M` | 36.0 | cloud catch (walk back to the S5 bounce) | ground (y1), Lily Lake water (soft) |
| C2 | `Soft_Cloud_M` | 51.9 | cloud catch (walk back to the S5 bounce) | ground (y1), Lily Lake water (soft) |
| C3 | `Soft_Cloud_M` | 52.4 | cloud catch (walk back to the S5 bounce) | ground (y1), Lily Lake water (soft) |
| C4 | `Soft_Cloud_M` | 52.9 | cloud catch (walk back to the S5 bounce) | ground (y1) |
| C5 | `Meadow_Islet_L` | 53.4 | cloud catch (walk back to the S5 bounce) | ground (y1) |
| C6 | `Meadow_Islet_L` | 53.9 | cloud catch (walk back to the S5 bounce) | ground (y1) |
| C7 | `Meadow_Islet_L` | 54.4 | cloud catch (walk back to the S5 bounce) | ground (y1) |
| N1 | `Log_Platform_M` | 73.9 | north catch shelf (back to the vine wall) | ground (y1) |
| N2 | `Log_Platform_M` | 73.9 | north catch shelf (back to the vine wall) | ground (y1) |
| N3 | `Log_Platform_M` | 73.9 | north catch shelf (back to the vine wall) | ground (y1) |
| N4 | `Log_Platform_M` | 73.9 | north catch shelf (back to the vine wall) | ground (y1) |
| N5 | `Log_Platform_M` | 73.9 | north catch shelf (back to the vine wall) | ground (y1) |
| N6 | `Log_Platform_M` | 73.9 | north catch shelf (back to the vine wall) | ground (y1) |
| T4c | `Giant_Meadow_Tree` | 88.0 | T4c tree pad 1 (catch) | T0c floating islet under the tree (catch) |
| T0c | `Meadow_Islet_L` | 57.4 | T0c floating islet under the tree (catch) | ground (y1) |

**Hidden ducks:** 1 on the last frog-hop lily pad; 2 on the turret top by the flag; 3 at the tip of the south blade spar; 4 end of the catch shelf under the NE corner; 5 inside the secret room

## Holden's answers (USER, 2026-10-05) — GO given
1. **Footprint:** keep 240×240 and 100 studs per segment "for now". If the dev timer shows S1 under the 5–8 min target, make the **route** longer (more zigzag, wall runs, more height per jump section), **not** the valley wider. Claude says so if a segment seems to need more than 100 studs of height.
2. **Leap landing:** next to the start plaza (fast Squishmaster replays) but in its **own splash zone**:
   - land in the **pond**, ringed by soft jelly/cushion pads, so nobody lands on a spawning player;
   - make the splash a fun moment (big splash/boing);
   - **keep the full lane clear from the summit to the pond at every height.**
3. **Shops:** YES, place them on the ground floor now (placement only, not wired) to judge the hub as a whole: the cosmetics hat shack, the Caravan gamepass shop and the other hub structures. Leave space for the halfway shop at CP2 later.
4. **Player hats:** while a game hat is equipped, hide the player's own **hat** accessories only (keep hair and everything else) and restore them when the game hat comes off. Hats perching on big hair is fine.
- Also USER: finish the test items first (phone-emulator 16-dummy shots + real FPS, TP_Top_Hat streamer, a bigger/readable leap pad with a proper standing launch, TexturePack re-check). Leave `TitleUI.BaseScale` until his phone test. Delete `Workspace.TestPlace.LeapTest` only once the real leap lane works.

## Pitfalls
- Kit meshes collide with their render mesh unless the manifest's invisible top colliders are used. Use the colliders for walkable tops.
- Every kit model imported 180° rotated. The staging already flattens it; re-check facing for directional pieces (signs, gates).
- Keep Studio visible while taking screenshots or measuring FPS.

## Related
[[Rubber-Tower-Build-Status]] · [[Rubber-Tower-Build-Plan]] · [[Rubber-Tower-Map-v3-Critique]] · [[Rubber-Tower-Valley-Kit]] · [[Rubber-Tower-Art-Style-Guide]] · [[2026-10-05-Rubber-Tower-Studio-Test]] · [[Rubber-Tower]]
