---
tags: [project/rubber-tower, project-hub]
status: draft
updated: 2026-10-04
confidence: low
---
# Rubber Tower (project hub)

## TL;DR
- Holden chose Rubber Tower on 2026-10-04 as the next game, from the brainstorm in [[Game-Concept-Shortlist-2026-10-04]].
- Pitch: an endless tower obby where everything is wobbly and each player's own avatar is the ragdoll. Falling is funny and cheap; free falls with checkpoints.
- Status: **concept only. No plan, file list or code approved.** Per vault rules, a plan and file list come first and Holden must approve before any game code.
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
- Friend boost: a reward while invited friends are in the server, tied to the currency (assumed, confirm).
- Titles instead of badges: unlockable, shown above the player's head. Unlocks include checkpoints, completing worlds, buying a first cosmetic, events, plus unique ones: invite 4+ friends, push 5+ different players down (the same player counts once), reach the top without claiming checkpoints. If invite verification can't be done, Holden is fine with changing the invite title to "3 friends in the server". The full title list is decided later.
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
- **Batches (f)–(h) ordered (Holden, 2026-10-04; brief in [[Rubber-Tower-Kit-FGH-Prompt]]):**
  - **USER:** "redo the dragon, finish the rest of the models you have to do".
  - **Batch naming:** (a)–(e) count as done. The old landmarks batch is now (e2).
  - **USER: only three shops for now, each with an NPC:**
    - a cosmetics shop in the hub (Squishies);
    - a gamepass shop in the hub, premium, showing the banana peel, Buddy Carry and skip-checkpoint passes as props;
    - a smaller halfway cosmetics stall at CP2, themed to that segment.
  - **USER: structures that support existing systems (not shops):**
    - world portal plaza, leaderboard plaza, quest board + daily reward spot, codes wishing well;
    - town crier podium (server twist events);
    - tutorial hut, Bonk Clinic, friend campfire;
    - a waystone per checkpoint (teleport menu);
    - summit podium and arch;
    - a modular stall kit for later shops.
  - **USER:** NPC characters come later; structures leave room for them, and the manifest marks the NPC spot and the ProximityPrompt anchor.
  - **USER:** about 30–40 hats across rarity tiers; some are sold only at the halfway shop. **Squishies prices: Holden decides later.**
  - **USER:** review stops after (f), after (g) and after (h). No uploads and no map building yet.
  - **Halfway stall theme:** CP2 sits at the top of S2, so it's **mushroom** (Holden's own example). If CP2 moves, an S3 ice version is a palette swap.
- **Batch (f) review (Holden, 2026-10-04):**
  - **USER, Squishies look:** "a pink/purple jelly coin, it should also have a cool icon on it as well, make a few so I have options". The options are in [[Rubber-Tower-Valley-Kit]]; **Holden picks one**.
  - **USER:** keep the per-structure colours "for now". The hub diorama layout is only a render, not the map layout.
  - **USER:** the text I added ("SUMMIT!", "!", "?") is fine.
  - **USER:** "fix what's weak, then we can move forward tomorrow". So: fix the saddle, waystone scale and mannequin trail, then stop. Batch (g) hats starts next session.
- **Squishies + shop (Holden, 2026-10-04):**
  - **USER: the Squishies coin is "the purple with duck on it"** = option D (rubber duck icon) in the **Grape** (purple) colour. Model `Squishies_Coin_D_Duck` + `Squishies_Coin_Grape_Paint.png`.
  - **USER (2026-10-05):** "do the gamepass shop the same way (but give me a few options), and move on to batch g".
    - Built `Shop_Gamepass_Fantasy` options A Treasury tower / B Merchant caravan / C Mossy gazebo, all green + gold + gem. **Holden picks one.**
    - Batch (g) hats built: review stop.
  - **USER (2026-10-05, batch g review):**
    - **Gamepass shop = option 2: B Merchant Caravan**, "for now".
    - Fix the weak hats (Flaming_Crown, Rune_Crown, Hot_Dog); otherwise keep all the hats as they are.
    - Hat Squishies prices: decide tomorrow. Then move on (batch h).
  - **USER:** "the shop could use some work, I want a cool storefront". Read as the hub **cosmetics shop**: it becomes a boutique storefront; the tent stays as `Shop_Cosmetics_Tent`.

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
1. Squishies: rewards per checkpoint, world and title, Robux pack sizes, and confirm the friend boost multiplies Squishies (Holden: decide later).
2. Invite title: ⚠️ verify what Roblox exposes about invited players; the fallback "3 friends in the server" is approved if needed.
3. Later: titles list, wobble/bounce areas, the three free emotes, world 2's unique mechanic.

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
