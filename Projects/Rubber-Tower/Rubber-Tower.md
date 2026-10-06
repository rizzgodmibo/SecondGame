---
tags: [project/rubber-tower, project-hub]
status: draft
updated: 2026-10-05
confidence: low
---
# Rubber Tower (project hub)

## TL;DR
- Holden chose Rubber Tower on 2026-10-04 as the next game, from the brainstorm in [[Game-Concept-Shortlist-2026-10-04]].
- Pitch: an endless tower obby where everything is wobbly and each player's own avatar is the ragdoll. Falling is funny and cheap; free falls with checkpoints.
- **PAUSED 2026-10-05 (~19:20 EDT) by Holden.** Restart prompt: [[Rubber-Tower-Slice-Fix-Pass-Prompt]] (water fix, enclosure, ground). Model archive: AssetLibrary `models/rubber-tower-kit-v6-map/`.
- Status (2026-10-05, ~19:30): phases 0–1 passed. Ragdoll, checkpoints, titles and Squishies faucets are built and Studio-tested. Build 1 of the map was critiqued ("not an obby yet"). **A map v3 vertical slice (hub, ground, Lily Lake, Village Rooftops) is built in the test place and STOPPED for Holden's review.** Plan: [[Rubber-Tower-Map-Build-Plan]]. Live status: [[Rubber-Tower-Build-Status]]. A plan and file list still come first for every new system.
- Target: young teens, mobile and PC first. Scope: small game.
- Reference research: [[Rubber-Tower-Reference-Obbies]] (observations of other games, not approved mechanics). Design draft: [[Rubber-Tower-GDD]]. Build plan (awaiting go-ahead): [[Rubber-Tower-Build-Plan]]. Kickoff prompt for Claude Code: [[Rubber-Tower-Claude-Code-Prompt]]. Brainstormed ideas: [[Rubber-Tower-Ideas-Bank]].

## Decisions from Holden (2026-10-04, user-approved)
**World and structure**
- One very tall fixed first map at launch; new worlds come in future updates and unlock after beating the first, each with a unique mechanic. Shared server, all players in the same world.
- 3 to 4 big checkpoints plus a few free soft platforms between them. Soft platforms can be fallen onto but are never a spawn or respawn point. A fall respawns you at your latest checkpoint.
- Checkpoint progress is saved. A menu shows your checkpoints and lets you teleport (free, no cooldown) to any checkpoint you have claimed, up or down (and to other worlds in the future). You must reach a checkpoint before you can teleport to it. Teleporting does not change your respawn point: you still respawn at your latest checkpoint.
- First-clear target: about 4 big segments of 5 to 8 minutes each; roughly 20 to 40 minutes for a median player (often over more than one session), about 10 minutes for fast players. Tune by playtest.
- Wobble/bounce areas: ragdoll mainly on falls and pushes, plus specific areas that make you wobble or bounce. Which areas: decided later.

**Player and interactions**
- The player's own Roblox avatar is the ragdoll.
- Shove (everyone): close range, 30-second cooldown, pushes the target a set distance and ragdolls them. Starting values accepted by Holden, editable later: about 10 studs of push and about 2 to 3 seconds of ragdoll. Converted to studs, tune by playtest.
- Hand-up (free, friendly): helps a nearby player onto a ledge.
- Banana peel (pass): 30-second cooldown after placing; one per player on the map; placing a new one removes the old.
- Buddy Carry (pass): requires an accept prompt.
- Skip-checkpoint pass: skippers still unlock next worlds the same way; paying to the top earns a joke/show-off title (examples "Millionaire", "False Conqueror"; names undecided).

**Currency, titles, social**
- Currency instead of XP: **Squishies** (name chosen by Holden). Earned at checkpoints, new levels/worlds and title unlocks; also sold for Robux; spent on cosmetics and future items. Every payout can be earned only once per player.
- **(USER, 2026-10-05) Squishies economy locked** (full table + model: [[Rubber-Tower-Squishies-Economy]], numbers in Config `Squishies`): checkpoints CP1 50 / CP2 75 / CP3 100 / Summit 200 (first clear 425; new worlds pay more later); titles Easy 25 / Medium 75 / Hard 150 / Very hard 300 (once each); daily 7-day streak 25/30/40/50/60/75/150 (430 per week, day 7 milestone); 3 Squishies packs as developer products: 99 R$ → 400, 249 → 1,100 ("Popular"), 499 → 2,500 ("Best value"); hat prices by rarity Common 30 / Uncommon 75 / Rare 175 / Epic 400 / Legendary 900 / Mythic 2,250; halfway-only hats cost the same as their rarity; Summit_Crown is the summit reward, never sold. **(USER 2026-10-05) Missed daily = restart at day 1. Re-reaching the summit pays +20, once per day. Title payouts by rarity: Common 25, Uncommon 75, Rare 75, Epic 150, Legendary 300, Mythic 300** (all 27 titles = 2,975; model v2 in [[Rubber-Tower-Squishies-Economy]]).
- Friend boost: a reward while invited friends are in the server, tied to the currency (assumed, confirm).
- Titles instead of badges: unlockable, shown above the player's head. Unlocks include checkpoints, completing worlds, buying a first cosmetic, events, plus unique ones: invite 4+ friends, push 5+ different players down (the same player counts once), reach the top without claiming checkpoints. If invite verification can't be done, Holden is fine with changing the invite title to "3 friends in the server". The full title list was decided on 2026-10-05 (below).
- **(USER 2026-10-05) Title list and rules:**
  - Rarity uses the hat tiers and colours. Every title pays once, by rarity (locked payouts).
  - Anything cheatable is checked on the server (climb trace + `skippedCheckpoints`, reviewer M1).
  - One title equipped at a time, picked in a Titles menu; locked titles show how to unlock them.
  - Max ~16 characters.
  - **Holden delegated the final names / rarities / unlocks to Claude (USER, afternoon of 2026-10-05)**, keeping his approved ones: summit without checkpoints, push 5+ players, friends in the server, first cosmetic, and the Millionaire / False Conqueror jokes.
  - Final list below. Data in Config `Titles`, with a `Check` field saying what the server must see.
  - Same counts per rarity as his draft, so all 27 still pay **2,975**.

  | Title | How to get it | Rarity | Category (badge) |
  |---|---|---|---|
  | Wobbly Beginner | Make your first jump | Common | Climb |
  | Meadow Hopper | Reach checkpoint 1 | Common | Climb |
  | Fresh Fit | Buy your first hat | Common | Collection |
  | Millionaire | Skip a checkpoint with Robux (joke) | Common | Joke |
  | False Conqueror | Reach the summit after a skip (joke) | Common | Joke |
  | Mushroom Muncher | Reach checkpoint 2 | Uncommon | Climb |
  | Bonk Enjoyer | Fall 100 times | Uncommon | Climb |
  | Boing Boing | Bounce 100 times on bounce pads | Uncommon | Climb |
  | Human Ladder | Give 10 hand-ups | Uncommon | Social |
  | Shroom Drip | Buy a halfway-shop hat | Uncommon | Collection |
  | Loyal Squish | Finish a 7-day daily streak | Uncommon | Daily |
  | Disco Duck | Dance (emote) in the secret room | Uncommon | Secret |
  | Frostbitten | Reach checkpoint 3 | Rare | Climb |
  | Gravity's Pet | Fall 1,000 times | Rare | Climb |
  | Full Send | Fall 100 studs in one go | Rare | Climb |
  | Pushy | Shove 5 different players off a ledge | Rare | Social |
  | Banana Bandit | 10 players slip on your banana peel | Rare | Social |
  | Hat Goblin | Own 10 hats | Rare | Collection |
  | Nosy Noodle | Find the secret room | Rare | Secret |
  | Rubber Champion | Reach the summit | Epic | Climb |
  | Squad Leader | Play with 3 friends in your server | Epic | Social |
  | Streak Freak | Finish 4 full daily streaks | Epic | Daily |
  | Duck Whisperer | Find every hidden rubber duck | Epic | Secret |
  | Squishmaster | Reach the summit 10 times | Legendary | Climb |
  | Speedy Noodle | Summit in under 12 minutes (tune by playtest) | Legendary | Climb |
  | Checkpoint Who? | Reach the top without claiming any checkpoint | Mythic | Climb |
  | Mad Hatter | Own every hat in the shop | Mythic | Collection |

  **Changes from Holden's draft:**
  - Renamed: Bonk Survivor → Bonk Enjoyer, Helping Hand → Human Ladder, Mushroom Fashion → Shroom Drip, Pro Faller → Gravity's Pet, Hat Collector → Hat Goblin, Secret Finder → Nosy Noodle, Party Starter → Squad Leader, Daily Wobbler → Streak Freak.
  - **Moonwalker → Boing Boing:** the low-gravity event doesn't exist, so the title was unobtainable. Moonwalker is saved for that event.
  - **Long Way Down → Full Send ("fall 100 studs in one go"):** a fall more than 12 studs below your checkpoint respawns you, so "segment 4 to the ground" can't happen once you've claimed a checkpoint.
  - **Squad Leader uses the approved fallback** (3 friends in your server). ⚠️ verify invite tracking before switching to "invite 4 friends".
- **(USER 2026-10-05, afternoon) Title UI decisions:**
  - Style **C Clean Text**, made ~13% smaller (v2 mockup: [[Rubber-Tower-Title-UI]]).
  - **Your own title shows** above your head, a bit smaller than other players'.
  - The **Legendary price stays 900** (economy unchanged).
- **(USER 2026-10-05) Title above the head = UI, not a 3D plaque.**
  - A BillboardGui banner: title on top, player name below, rarity border + a badge icon per category.
  - Bold rounded font with a thick stroke, readable on a phone at ~30 studs.
  - Rarity effects: Common grey, Uncommon green, Rare blue + soft shine, Epic purple animated gradient, Legendary gold shimmer + sparkles, Mythic animated rainbow/pink + sparkles.
  - Sits above tall hats; follows the body smoothly in ragdoll; fades with distance; fine with 16 players.
  - **2–3 style mockups first, Holden picks before any code.** Mockups A Badge Banner / B Ribbon / C Clean Text + research + build plan: [[Rubber-Tower-Title-UI]] (waiting for Holden's pick; Claude recommends A).
  - Title_Plaque stays a world prop only.
- **(USER 2026-10-05, night) Squishmaster and replays: the Leap of Faith.**
  - At the summit there's a "Leap of Faith" edge/launch pad. Using it sends you on a ragdoll fall to the ground floor (it also counts for Full Send) onto a soft landing zone, so you can climb again.
  - **A new run starts when you leave the ground floor.**
  - A run counts toward Squishmaster and the +20 replay only if the server's climb trace shows it was climbed with **no teleport up the tower** during that run. Teleporting down is fine.
  - Built and Studio-tested 2026-10-05: [[2026-10-05-Rubber-Tower-Studio-Test]]. The "ground floor" height (start + 15 studs) and the teleport threshold (35 studs per 0.1 s) are Claude's PROPOSAL numbers in Config.
  - ⚠️ The future checkpoint-teleport menu (USER 2026-10-04: free teleports up or down to claimed checkpoints) will taint a run when used upward, as the rule says.
- **(USER 2026-10-05, night) Map + hat answers** (details in [[Rubber-Tower-Map-Build-Plan]]):
  - The footprint stays 240×240 with 100 studs per segment "for now". If S1 is too short, lengthen the route, not the valley.
  - The Leap lands in a **pond splash zone** next to the start plaza (soft jelly/cushion pads around it, a fun big splash). The lane stays clear from the summit to the pond at every height.
  - Shops are placed on the ground floor now (not wired): the hat shack, the Caravan gamepass shop and the hub structures. Space is kept for the CP2 halfway shop.
  - While a game hat is on, the player's own **hat** accessories are hidden (hair etc. stays) and restored when it comes off.
- **(USER 2026-10-05, evening) Map layout critique: "a classic linear obby"** (full text in [[Rubber-Tower-Map-Build-Plan]]):
  - Layout v1 (a dotted line of hops up the west side) was stopped before building.
  - He wants:
    - the kit models to BE the obby: rooftops, windmill, giant tree, lily pads, cliff ledges, waterfall, cave, rope bridge;
    - the whole valley used, with the route crossing over itself at different heights;
    - 4–6 themed places with a moment each, introducing all special pieces teach → test → twist;
    - side paths, hidden ducks, the secret room and goofy details.
  - Next: two layout options (top-down + whole-tower side view + storyboard), then his pick before any build.
- **(USER 2026-10-05, 15:28 EDT) Map layout = Option B "Through the Middle"**: a figure-8 crossing the valley centre twice (skyway under CP1 at ~y55, treetop bridge over it at ~y90). Places: Lily Lake → Village Rooftops → Windmill Climb → Crystal Skyway → Waterfall Ledges + Cave → Treetop Return → CP1. Windmill blades static first (spin behind a Config toggle, his call after playing). Detailed spec + build: [[Rubber-Tower-Map-Build-Plan]].
- **(USER 2026-10-05, ~17:30 EDT) First Option B build critique: "progress, but it isn't an obby yet, and parts of it look lazy"** (full text + the rework plan in [[Rubber-Tower-Map-Build-Plan]]):
  - The bottom isn't an obby: lily pads/raft on a shallow pond next to grass, so no challenge and no fail. The special models are used as decoration.
  - The upper part is ~20 identical small plank hops (same gap, same size, no timing, no mechanics): far too easy.
  - The hub is props huddled round the pond, not a world. The ground is one flat green with a sand ring.
  - The cliff walls repeat one rock model, and he doesn't like the black crack lines on every rock. **This overrides the "dark cracks" line in the locked [[Rubber-Tower-Art-Style-Guide]]: use soft darker-tone crevices and colour variation.**
  - The waterfall is a flat blue strip with dashes. The floating islets in a row look identical.
  - **Wants:**
    - a REAL obby of combos built from the special pieces, every special piece used as gameplay in S1 (ice mostly saved for S3);
    - real difficulty: sawtooth, easy at the start gate → medium by CP1, a few falls and 5–8 min for a first-timer, phone-fair, measured by playing it;
    - a hub that feels like a world: a safe village with a clear START GATE that the spawn faces, a square with shops facing it, streets, districts, groves, fences/hedges, height (hills, terraces, ramps, a stream from the waterfall to the pond with a bridge);
    - crisp v5 ground zones;
    - 5–6 different cliff pieces with variants, mixed with random rotation and scale, broken up with ledges, vines, trees, crystals, caves, arches and waterfalls;
    - a real layered waterfall with foam, mist and a splash pool;
    - varied islets.
  - **Process:** the combo list first, then ONE vertical slice (hub + ground + start gate + Lily Lake + Village Rooftops, with the new walls and waterfall), then stop with: spawn view, start gate, each combo, walls up close, ground at player height, fall count and time. Keep the Leap lane, checkpoints, colliders and phone-friendliness.
- **(USER 2026-10-05, ~17:45 EDT) Combo-rework decisions:**
  - **Mechanics code approved (all):** swing paddles/hammers, fan vents and the slingshot (time-synced from server time, a bonk = the existing ragdoll), the seesaw log and a per-cube jelly stiffness, plus a shared maths module with specs.
  - **Water hazards = stylised mesh water, no terrain water:** v5 look (crisp colour zones, a lighter edge band, a few painted ripples and lily shadows), clearly deep and dark in the middle so it reads as "don't fall". Falling in = ragdoll, a big goofy splash + "bloop", you bob up for a moment, then a quick ~1 s tween floats you back to the combo's start. **It counts as a fall** for Bonk Survivor / Pro Faller. The same water + splash is reused for the splash pond and every other water hazard.
  - **Windmill blades spin** (the slow spin, ~4°/s) for the ice slide → bounce → blade combo.
- Open (titles):
  - Moonwalker (Uncommon) returns when a low-gravity event exists; it isn't in the list now.
  - Disco Duck needs a server check that an emote animation is playing inside the room. Built 2026-10-05 as "a non-default animation ID is playing" (emote names don't replicate usefully); ⚠️ verify with a real `/e dance` in play.
  - Party Starter: ⚠️ verify what Roblox exposes about invites (the fallback is approved).
- Emotes: 3 basic free ones (picked later); the rest sold in an emote pack.
- Server-wide twist events such as low gravity, cosmetics (more brainstorming later).

**Left out for now**
- Eggs and other random items; speed boards (Holden unsure).

**Build answers (2026-10-04, kickoff session)**
- Avatars: support both R6 and R15. Server size: 16 players.
- A fall ragdolls at 12 studs, with 1.5 s recovery after landing ("we can tune later").
- Bounce pads are launch only, with no ragdoll. Other platforms and structures will have various effects, for example ice that makes you slide a bit (which effects and where: later).
- Project folder: `C:\Users\holde\Documents\GameDev\RubberTower` (local git). Holden tests on his phone himself. No luau-lsp type checking.
- Phase 1: Holden waived the phone cost numbers ("waive it"); phase 1 passed.

**Map answers and critique (2026-10-04, phase 2)**
- Shape: "kind of a square or long cylinder", with the obby in the middle and on the walls. Soft platforms: about 2 per segment, as proposed ("lets go with those platforms for now"). Add the special platforms (ice, wobble) to the greybox now and review them later. Keep Roblox's default movement (WalkSpeed 16, JumpHeight 7.2).
- Critique of greybox v1 (60×60 hollow tower): **make it wider with more space; it should look like a whole world inside a square border with walls; it needs a fantasy feel to match the theme; v1 feels super enclosed.** Take inspiration from open/outdoor obbies, especially the multiplayer chained-together obbies with their unique worlds (research in [[Rubber-Tower-Reference-Obbies]]).
- Not answered, so the proposals are in use and still open: what sends you back (a fall below your checkpoint), 3 checkpoints + summit, always respawning at your highest checkpoint.
- **v2 critique (Holden, 2026-10-04, his prompt; full text summarised):** still a box ("a cage now"): pillars and flat full-height walls block every view; everything is parts, with none of the Blender kit used ("low quality, outdated"); one lavender/white colour; no readable route; no visible goal or recognisable checkpoints; stray see-through pieces; no visible themes; an empty floor. **Wants v3:**
  - **Walls:** a backdrop, not a cage. A square border of **mountain-wall terrain** ("we want to be immersed in the world"), with corner towers, uneven heights, cliffs and waterfalls at the base, and arches or gaps to see out to distant mountains, islands and clouds.
  - **Models:** real kit meshes everywhere, as a **reusable per-segment Blender kit** (2–3 sizes per platform type, landmarks, backdrop, decor). **Show renders before uploading.** Placed copies get colour and size variation and simple invisible collision on platforms.
  - **Colour:** each segment its own colour band (S1 meadow warm greens and flowers, S2 mushroom red/pink with deeper greens, S3 crystal-ice cyan/blue glowing, S4 cloud white/gold sunlit). The background is lower saturation; walkable surfaces are the brightest.
  - **Route and goal:** a readable route (the next checkpoint visible from each one); checkpoint landmarks with beacons; a summit landmark visible from the ground.
  - **Ground floor:** crisp-zone meadow, pond, 3+ tree species, boulders, flowers, start plaza with a gate.
  - **Lighting:** the obby preset (sky-blue Atmosphere about 0.2, Saturation about +0.2, readable shadows).
  - **Process:** ground + segment 1 only, then stop. 4-angle screenshots (spawn eye, on CP1 looking up, outside corner overview, 150px), self-critique, map audit passing, before/after side by side.
  - The themes are fine (USER).
- **v2 answers (2026-10-04):** a walled mystical valley (full-height walls, sky above). The middle is floating islands and crystals, not one spine. Size about 240 × 240 × 400 "for now". Use the existing low-poly trees and rocks for the fantasy feel, "but dont slack, make other models if needed"; Blender MCP is available. **Segment themes not answered**, so meadow, mushroom grove, crystal/ice and cloud kingdom are in use as PROPOSALS.
- **Kit v3 critique (Holden, 2026-10-04; full prompt in [[Rubber-Tower-Kit-v4-Style-Prompt]]):**
  - **Verdict:** keep the v3 models, but add MORE models with far more fantasy and magic, in a **Roblox style**. v3 is "too realistic and muted".
  - **Problems:**
    - Too realistic and dull: beige, grey and olive.
    - The cliffs look like stacked boxes, with dark back slabs showing.
    - The grey rock is one flat colour.
    - The ground blobs look like camo.
    - Barely any fantasy.
    - Workbench renders are too dark.
  - **What "Roblox style" means:**
    - Chunky, soft and toy-like, with bevels and exaggerated proportions.
    - Bright and saturated, with crisp zones and 3 tones per material.
    - Grass caps spilling over rock tops.
    - Flat-shaded low-poly. Not cubes, not parts, not realistic.
    - Glowing magic accents.
  - **Main references:**
    - OmniKoi2 img-1..4: the main style target.
    - haooffiso Sky_Island: the magic level.
  - **Process:**
    1. Write a style guide ([[Rubber-Tower-Art-Style-Guide]]).
    2. Style test: 3 restyled models plus 3 new magic models, shown as v3 vs v4 vs the reference, then **stop for his OK**.
    3. Build in batches per segment, with Eevee renders, a sun, a blue sky and a diorama.
    4. **No upload until he approves the renders.**
  - **The new model list is his request, not yet built:** crystals, rune stones, portal, spell circle, lanterns, cauldron, books; 3+ tree species, mushrooms, flowers, vines; wizard tower, mushroom house, ruins, bridge, castle, airship; themed platforms per segment.
  - **Style test status (2026-10-04):** built, not yet approved. See the v4 section in [[Rubber-Tower-Valley-Kit]].
- **Kit v4 critique (Holden, 2026-10-04; full prompt in [[Rubber-Tower-Kit-v5-Prompt]]):**
  - **Save the v4 models** in case he wants them later. Done: `AssetLibrary/models/rubber-tower-kit-v4/`.
  - **Verdict:** "some models are fine, but I don't like the style of most of it". He wants an **actual Roblox game look: high quality, Roblox/goofy**.
  - **Problem 1, it's an obby, so the terrain must go UP:**
    - Walls, cliffs and platforms built for climbing: ledges, terraces, spiralling platforms, checkpoint islands stacked.
    - The summit visible overhead. The ground floor is only the start.
    - The flat canyon diorama is rejected.
  - **Problem 2, too smooth ("cheap plastic"):**
    - He wants crisp, stylised surface detail everywhere, and still no blurry noise.
    - Rock: cracks, chipped bevels, strata, pebbles, edge highlights.
    - Grass: tufts and blades over edges, flowers, clover, a dark band.
    - Wood: planks, grain, nails, rope.
    - Stone: bricks, trims, cracked tiles, moss.
    - Hand-painted textures with baked AO, darker bottoms and lighter tops.
  - **Goofy:** crooked, wobbly, exaggerated, silly details (a mushroom with a face, a cracked signpost).
  - **Keep and upgrade:** crystals, islet, beacon, portal, plus the listed fixes (bush canopy, portal spiral, thicker obelisk).
  - **Redo:** cliffs and terrain, as a climbable vertical obby wall.
  - **Process:**
    - **Test uploads to a private test place are OK'd.**
    - Judge in Studio with the obby lighting, a skybox and his avatar.
    - Style test: a 60-stud wall with ledges and a checkpoint island, plus the islet, crystal and beacon. Show v4 | v5 in Studio | the closest real Roblox ref, plus a shot looking up the climb from the bottom.
    - Self-critique ("real Roblox game or plastic toy?", "can you see the climb?"), then **wait for his OK**.
  - **His own screenshots in `Assets/Reference-Captures/Holden-Picks/` outrank all other references.**
- **v5 approved, full kit ordered (Holden, 2026-10-04; full prompt in [[Rubber-Tower-Kit-Full-Prompt]]):**
  - **USER:** "we can work with this style. Lock it in." The v5 look is the standard ([[Rubber-Tower-Art-Style-Guide]]).
  - **USER:** "save those models we will use them". Done: `AssetLibrary/models/rubber-tower-kit-v5/`, uploaded ids in its README.
  - **USER:** he wants TONS of models ("we are putting time into this game … go hard").
  - **Fixes:**
    - The wall masses are too even and grid-like.
    - The beacon bricks are too busy, so use chunkier stones.
    - The islet bush should be a puffy canopy.
  - **The kit:**
    - (1) obby mechanic models: bounce, ice, wobble, soft rest, movement, climbing, checkpoint pieces;
    - (2) platforms per segment;
    - (3) fantasy models: magic, buildings, plants, creatures as decor, props, backdrop.
  - **Process:**
    1. The full kit list as a checklist in [[Rubber-Tower-Valley-Kit]] first.
    2. Batches with a review stop after each: (a) mechanics, (b) S1 + props, (c) S2, (d) S3, (e) S4 + backdrop.
    3. Each batch gets render sheets (model | reference) and a diorama with an avatar-sized dummy.
    4. Colour and size variants reuse meshes. Phone-friendly, with shared atlases and colliders planned.
  - **USER: don't upload or build the map yet.**
  - **The mechanics must fit the existing tags and code** (`IcePlatform`, `WobblePlatform`, `BouncePad`; wobble about 12×12 with room underneath for the springs).
- **Batch (a) review (Holden, 2026-10-04):**
  - **USER:** "keep the colors". The mechanic colour language is approved: bounce hot pink, ice pale cyan/white, wobble lime jelly, soft rest cream/pastel, movers red rubber, checkpoint white/gold + cyan glow.
  - **USER:** "start with batch B. and after batch B make even more if you can". So after batch (b), keep building further batches (c onwards) before the next stop.

**Process and look**
- Built in Claude Code connected to this vault; the project folder is created in that session. Holden is preparing a kickoff prompt: [[Rubber-Tower-Claude-Code-Prompt]]. Building does not start until Holden says go.
- Art: flat-shaded low-poly Blender assets for now; specifics later. Title "Rubber Tower" stays.
- References: the obbies in his screenshot plus other ragdoll obbies, see [[Rubber-Tower-Reference-Obbies]].

## Concept (from brainstorm, not yet approved as mechanics)
- **Core loop:** climb a tower of wobbling platforms, springs and swinging bars; fall, land on a soft pad or checkpoint, retry.
- **First 60 seconds:** easy first jump on a wobbling platform; first fall within about 20 s lands softly; first checkpoint appears before frustration.
- **Progression:** themed sections that each add a wobble mechanic; cosmetic trails and ragdoll styles; optional best-height or best-time boards.
- **Rough scope:** about 5 to 6 themed sections, about 8 wobble mechanics (placeholder numbers).

## Known risks
- Ragdolling every player's avatar costs physics on server and phone, and avatars vary: test on a real phone early (see [[Roblox Mobile UI Layout]], [[Rubber-Tower-Reference-Obbies]]).
- One launch map is thin for retention; cosmetics, friends and a planned world 2 must carry it.
- With only 3 to 4 checkpoints on a very tall tower, segments are long; playtest early.
- Tower of Hell has no checkpoints and timed rounds; our choices differ, so do not assume its retention carries over.
- A push move can be used to grief; needs server validation, cooldown and a force cap. Banana-peel and carry/throw passes raise the same risk for paying players.

## Open questions (Holden to decide, nothing assumed)
1. Squishies: amounts, the missed-daily rule (Restart), the replay reward (+20/day) and the title list are DECIDED 2026-10-05 ([[Rubber-Tower-Squishies-Economy]]). Still open: whether the friend boost multiplies Squishies, and the Legendary-on-day-2 pace (PROPOSAL: Legendary 1,200).
2. Invite title: ⚠️ verify what Roblox exposes about invited players; the fallback "3 friends in the server" is approved if needed.
3. Later: wobble/bounce areas, the three free emotes, world 2's unique mechanic. Title UI style: Holden picks from the mockups.

## Note conflicts found in the kickoff run (2026-10-04, for Holden to settle)
The decisions above win over every line listed here. Nothing was edited silently.
1. This hub's TL;DR ("endless tower obby") and its "Concept" section (5 to 6 themed sections) disagree with the decisions (one very tall fixed map, about 4 segments). The TL;DR and open questions 1 to 4 in [[Rubber-Tower-Reference-Obbies]] are stale for the same reason.
2. [[Rubber-Tower-GDD]] §5 says "Whether checkpoint progress saves between sessions is UNDECIDED", but the decisions and the same section say checkpoints are saved.
3. GDD §8 and the [[Rubber-Tower-Ideas-Bank]] TL;DR call soft platforms DRAFT or UNDECIDED, but they are approved above.
4. The friend-boost line above includes "(assumed, confirm)". Treat the Squishies multiplier as undecided.
5. Respawn uses your "latest" checkpoint, but the draft data schema stores `highestCheckpoint`. If you teleport down and touch a lower claimed checkpoint, does your respawn move down? This is not stated.
6. Hand-up is approved, but it has no phase, file or behaviour in [[Rubber-Tower-Build-Plan]].
7. The GDD gate is still open (the one-liner, pillars and core loop are DRAFT). Holden's kickoff prompt orders the scaffold and ragdoll prototype first. This is logged in [[Rubber-Tower-Build-Status]].

## Next steps
0. 2026-10-04: phases 0 and 1 passed (Holden waived the phone cost numbers). The phase 2 plan is proposed in [[Rubber-Tower-Build-Plan]] and waits for Holden's answers. Holden's first commit is pending. Status and evidence: [[Rubber-Tower-Build-Status]]. How the ragdoll works: [[Avatar-Ragdoll]].
1. Holden answers the open questions.
2. GDD draft exists ([[Rubber-Tower-GDD]]); Holden reviews it.
3. Holden approves, edits or rejects [[Rubber-Tower-Build-Plan]].
4. Bootstrap per [[Project-Bootstrap-Checklist]] (phase 2). Holden makes commits.

## Checklist
- [ ] Open questions answered
- [ ] GDD reviewed by Holden
- [ ] Plan and file list approved by Holden
- [x] Avatar ragdoll prototype tested in Studio (2026-10-04, see [[Rubber-Tower-Build-Status]])
- [x] Prototype of avatar ragdoll tested on a real phone (Holden: "testing was fine", 2026-10-04; cost numbers from the phone still to record)
- [ ] Thumbnail readable at 150 px ([[Thumbnails-And-Icons]])

## Pitfalls
- Do not convert brainstorm or research suggestions into approvals; only lines under "Decisions from Holden" are approved.

## Related
- [[Home]] · [[Rubber-Tower-Build-Status]] · [[Game-Building-Playbook]] · [[Game-Concept-Shortlist-2026-10-04]] · [[Rubber-Tower-Reference-Obbies]] · [[Paper Plane Toss]]

## Sources
- Brainstorm conversation with Holden, 2026-10-04 (chat); reference list from his screenshot. See [[Rubber-Tower-Reference-Obbies]] for web sources.
