---
tags: [assets/models, project/rubber-tower]
status: draft
updated: 2026-10-05
confidence: medium
---
# Rubber Tower Kit: Batch Results

Split out of [[Rubber-Tower-Valley-Kit]] (the kit list and status) on 2026-10-04, when that note passed 500 lines. Results, sheets, preflight and self-critique per batch, newest first.

## Batch (h) v3 (2026-10-05, late afternoon): the remaining weak points
Holden asked for the last weak points to be fixed, or for an explanation of why one can't be.

**Changes:**
- **Secret room:**
  - Mossy grey stone walls (`stone_dark`), a turf roof, boulders hugging the walls, a stone chimney.
  - Tried a rock paint on the flat walls first; it looked like cardboard.
  - Still a little "brick hut" from outside. The real fix is placing it into a cliff when the map is built, since the shell is meant to be embedded.
- **Hedge:** smooth `hedge` paint (the leaf-outline paint read as scales). Now it reads as a clipped hedge.
- **Winter twins of the batch (b) hub decor**, built from batch (b)'s own functions:
  - `Lantern_Post_Snowy`, `Bench_Snowy`, `Barrel_Snowy`, `Well_Snowy` (snow on the roof slopes + rim);
  - `Fountain_Snowy` (frozen: the water is ice, snow on both rims).
- **Not done, with the reason:** the shops (batch f) have no winter twin. Their roofs are custom shapes, so snow would need per-shop work; worth doing when a winter event is planned.

**Result:**
- 104 specs, 127 models, 64k tris; preflight `PASS objects=166 fails=0 warns=103`.
- Small overruns, all accepted kinds: Squishies_Pickup, Hedge_Snowy_M, Wet_Floor_Sign, Scroll_Rack, Barrel_Snowy (878 / 800).

## Batch (h) v2 fixes (2026-10-05, after Holden's review): built, waiting for review
Holden's list (USER): fix the secret room, gates, hedge and moon lantern; give the hub decor a snowy version; add emblem-only icons; add a Hidden_Duck; leave the 3 tri overruns.

**Changes:**
- **Goofy_Secret_Room v2** (1.5k tris). The outside now has:
  - a crooked half-open door with a glowing keyhole;
  - a duck-shaped glowing window in a wooden frame;
  - a glowing "?" and vines from the eaves;
  - a crooked purple gable roof with a chimney.
  - The roof is a separate **Roof** part, so the room can be shown open.
  - A **cutaway render** shows the inside: disco ball, duck shrine, blank plaque, glowing dance floor.
- **Segment_Entry_Gate v2:** pillars 2.6–3 wide, a fat 1.8-deep arch, a big top piece per segment and a bigger blank sign:
  - S1: log pillars + a giant smiling flower;
  - S2: mushroom stems + a spotted cap arch + a giant cap;
  - S3: ice pillars wrapped in crystals + a crystal crown;
  - S4: white/gold columns + a cloud + a smiling gold star.
- **Hedge v3:** a rounded block covered in smooth round puffs, in a deeper hedge green (`hedge` recipe), with flowers.
  - v1 read as a log; v2's random-point puffs looked like shards.
- **Moon_Lantern v2:** a fat crescent with a big closed eye + lashes, a pink cheek and a smile, a gold back rim and glow sparkles.
- **Checkpoint_Emblem S1–S4 (new, Gameplay):** round theme-colour badges with a gold rim and the 1.25× emblem, rendered face-on as UI icons. S3 uses a deeper blue so the glowing snowflake reads.
- **Hidden_Duck (new, Gameplay):** a 1.4-stud rubber duck with a trigger collider, for Duck Whisperer. Yellow + Pink/Blue/Mint variants.
- **Snowy twins (new, Seasonal):**
  - `Plaza_Floor_Snowy` (drifts in the corners), `Path_Piece_Snowy` (snow on the edge stones), `Hedge_Snowy` (snow on each top puff);
  - `Flower_Box_Snowy` (snow + holly with red berries), `Spawn_Pad_Snowy` (banks outside the rim; the glow stays clear);
  - `Height_Marker_Snowy`, `Swing_Bench_Snowy`.
  - These replace the old colour-only "Snowy" hedge variant.
- New helpers in `batch_h.py`: `emblem()`, `snow_cap()`, `snowy_twin()`.

**Result:**
- 99 specs, 122 models, 59k tris.
- Preflight `PASS objects=160 fails=0 warns=97` (same WARN kinds as before: glow parts, open double-sided shells, moving/floating parts).
- Over budget, all small and far under the 10k limit: the 3 accepted ones + Hedge_Snowy_M 1,578 / 1,500.

![[BatchH_SecretRoom_Cutaway.png|700]]

**Still weak, honest:**
- The secret room's walls are the lavender brick from the kit. It reads as a cute cottage rather than a "secret" until it's hidden in the map.
- Older hub decor (Lantern_Post, Bench, the shops) has no snowy twin yet.
- The hedge is fine, not great: a hand-modelled hedge would beat the procedural puffs.

## Batch (h) extra + misc (2026-10-05): reviewed by Holden the same day (fixes in v2 above)
**What was built:**
- Code: `RubberTower/art/batch_h.py`, output in `art/kit_batch_h/`.
- **90 specs, 106 models, 40.9k tris in total** (checked against `manifest.json`).
  - Two budgets were raised during the fixes: Path_Piece (T junction 1,660, budget 1,800, for the chunky edge stones) and Rubber_Band_Ball (888, budget 900).
  - **3 are slightly over budget and left as they are** (all far under the 10k prop limit): Squishies_Pickup 1,284 / 1,200 (the both-sided icon), Scroll_Rack 816 / 700, Wet_Floor_Sign 512 / 400 (the text).
- Preflight: `PASS objects=139 fails=0 warns=86`.
  - Most WARNs are `_Glow` parts (Neon, single colour, floating) or open double-sided shells (flag cloth, text, blades, tent).
  - 6 origin WARNs are by design: moving parts (Swing_Bench_Seat, Watermill_Wheel_Wheel) and floating items (Sky_Jellyfish, Star_Lantern, Enchanted_Broom, Squishies_Pickup).
- Reused instead of rebuilt (in the script docstring): Decor_Stump = Stump_Platform, Apple_Crate = Goods_Crate, mushroom rings = Fairy_Ring, toadstool lamp = Mushroom_Lamp, fountain = Fountain, Giant_Snail = Snail ×3, puffballs = Puffball_Cluster, Snowman / Penguin, Rubber_Chicken prop = the hat, Summit_Crown prop = the hat on Display_Pedestal or Glass_Display_Case, chests = Treasure_Chest, days 1–6 rewards = Daily_Mailbox + Gift_Chest_Pedestal.

**Groups:**
- **Gameplay (UI-quality, transparent icons from one rig, like the hats):**
  - Banana_Peel: classic cartoon peel with a trigger collider r 1.8.
  - Squishies_Pickup: the chosen duck Grape coin with icons on both faces, a glow halo and sparkles; spin pivot in the manifest.
  - Trophy: Gold, plus Silver and Bronze as re-baked variants; BLANK plaque.
  - Title_Plaque: BLANK face for a SurfaceGui.
  - Checkpoint_Flag S1–S4: white/gold pole, cyan glow ring and a themed cloth (flower, mushroom, snowflake, star) with the emblem on both sides.
  - **Daily_Chest_Day7:** the big purple + gold "7" chest with a pink bow and sparkles. It was missing from the kit.
- **Hub:**
  - Plaza_Floor (square, round), Path_Piece (straight, curve, T), Hedge S/M (+ Snowy variant), Flower_Box.
  - Spawn_Pad (SpawnLocation collider), Segment_Entry_Gate S1–S4 (blank signs), Height_Marker (blank board).
  - AFK_Beanbag ×3 colours, Swing_Bench (swinging Seat part).
- **Fantasy:**
  - Sword_In_Stone, Dragon_Skeleton (landmark scale, ~27 studs), Garden_Gnome ×3 poses, Beehive, Watermill_Wheel (Wheel part + axis).
  - Mine_Cart + Mine_Track, Hot_Air_Balloon ×3, Kite ×3, Sky_Jellyfish (Tentacles part), Sky_Whale.
  - Totem, Bell_Tower, Wind_Chimes, Firefly_Cluster.
- **Secrets:** Hidden_Cave_Entrance, Secret_Ledge, Goofy_Secret_Room shell.
- **Goofy:** Rubber_Band_Ball, Squeaky_Hammer, Whoopee_Cushion, Cone_With_Wizard_Hat, Wet_Floor_Sign ("SLIPPY!"), Pool_Ring, Donut_Float, Toy_Blocks, Scarecrow, Lost_Sock_Branch, Rubber_Boot.
- **Clutter (one shared atlas):** Pebble_Cluster, Rock_Pile, Fallen_Log, Clover_Patch, Reeds_Cattails, Stepping_Stones, Puddle, Leaf_Pile, Giant_Acorn, Giant_Pinecone.
- **Village:** Picnic_Blanket, Laundry_Line, Flower_Pot ×3, Wheelbarrow, Garden_Tools, Pumpkin_Patch, Carrot_Patch, Birdhouse, Doghouse, Camping_Tent, Telescope, Arrow_Street_Sign, Water_Trough, Bunting, String_Lights, Weather_Vane.
- **Magic:** Crystal_Ball_Stand, Alchemy_Table, Floating_Candles, Magic_Mirror, Enchanted_Broom, Levitating_Teacups, Scroll_Rack, Wand_Rack, Star_Lantern, Moon_Lantern.
- **Segment:** Frozen_Fish_Block, Ice_Sculpture (Duck, Swan), Cloud_Sheep, Star_Decor, Golden_Harp, Sundial, Winged_Statue.
- **Seasonal:** Pumpkin S/M/L, Jack_O_Lantern, Wrapped_Present S/M ×3 colours. Snowy hub variant = the Hedge "Snowy" re-bake.

![[BatchH_Icons.png|700]]
![[BatchH_Diorama.png|900]]

**Self-critique (done before review, local observation):**
- **Fixed after the first full build:**
  - Banana peel was pale and flat (it read as a starfish).
  - Flags: thin poles, plain cloth, no checkpoint colours.
  - Chest: small "7" and bow.
  - Spawn pad: a gold hull "rim" was a solid disc that hid the glow.
  - Path edges were invisible.
  - Cave: the dark opening read as a black cube. Now it's a rock tunnel with darkness 3 studs deep.
  - Dragon skeleton: small and flat.
  - Mine cart: white body.
  - Sky jellyfish dome: faceted like a gem.
  - Rubber-band ball: over budget, and looked like a gem.
  - Pumpkins and jack-o'-lantern: crumpled lobes; the grin was a slab sticking out.
  - Leaf pile was a blob; pebbles and stepping stones were too pale.
  - Candle flames were invisible; the moon lantern was a thin line; the weather vane was too light.
  - Stars: convex hulls flattened them into pentagons, so a `star()` helper was added.
  - The diorama cropped its front rows.
- **Still weak, honest:**
  - Goofy_Secret_Room is a plain brick box from outside. The fun is inside (disco ball, duck shrine, plaque), and the tile doesn't show it.
  - Segment_Entry_Gates are thin for "welcome" arches.
  - Hedge reads as a lumpy log.
  - Moon_Lantern face marks are tiny.
  - Flag icons will be thin at very small UI sizes. Use the emblem alone for tiny icons.

**Review sheets:**
- Group sheets with reference columns (Gameplay, Hub, Fantasy, Secrets, Goofy, Clutter, Village, Magic, Segment, Seasonal) are gitignored because they composite third-party references.
- Tracked: `BatchH_Icons.png`, `BatchH_Diorama.png`, `icons/`.

## Batch (g) crazy hats + gamepass shop options (2026-10-05): reviewed. Gamepass = B Caravan; hats kept as they are; prices tomorrow
**Gamepass shop, 3 fantasy options** (Holden: "do the gamepass shop the same way, but give me a few options"; `Shop_Gamepass_Fantasy`):
- All three keep the premium green + gold and a big gold gem on top, show the 4 pass props, and have an NPC spot + prompt anchor.
- **A Treasury** (5.8k tris): round stone tower, open front arch with counter, crooked green onion dome, a giant gold vault door swung open, green banners.
- **B Caravan** (3.7k, **CHOSEN by Holden "for now", 2026-10-05**): green/white striped canvas wagon with big spoked wheels; the side folds down as the counter with the passes on it; hanging lanterns.
- **C Gazebo** (4.9k): crooked bark posts with gold rings on a mossy rock, green shingle cone roof, round counter, pedestals, vines.
- The old white pavilion `Shop_Gamepass` stays until Holden picks.

![[BatchF_Gamepass_Options.png|900]]

**Batch (g) hats:**
- Code: `RubberTower/art/batch_g.py`, output in `art/kit_batch_g/`.
- **All 39 hats from the checklist table + the 4-piece display set** (Hat_Stand, Mannequin_Head, Hat_Rack, Glass_Display_Case).
- 16,566 tris for the whole collection (72–1,040 per hat, all under the 2k budget). One atlas per rarity.
- Preflight `PASS objects=88 fails=0`. Every colour-variation WARN is a `_Glow` part.

**Accessory data** (`manifest.json`, per hat):
- `roblox.handle_hat_attachment_studs`: where the HatAttachment goes on the Handle (Body MeshPart), in Roblox axes, relative to the Handle's bounding-box centre.
- `wobble_pivot` (and `wobble2_pivot`) + `*_from_part_centre`: the hinge or spring point for each Wobble MeshPart. That's 28 wobble pivots across the collection, plus `wobble_spin_axis` for the propeller, halo, planet and summit crown.
- `rarity`, `sold` (the 4 halfway-only hats say "Halfway S2 only").
- **Studio setup still to do (code session):** Accessory → Handle = Body; HatAttachment at that offset; weld the Glow part; hinge or spring the Wobble parts at their pivots; check they stay on during ragdoll.

**Renders:**
- **UI icons**, `art/kit_batch_g/icons/<Hat>.png`: transparent, 512², one fixed rig (3/4 front, slightly above, auto-fit). Ready to drop into the shop UI.
- **Icon sheet** on rarity-coloured tiles.
- **On-head fit renders** per rarity: each hat on an R6 noob head and on an R15-style round head with a hair cap.

![[BatchG_Icons.png|900]]
![[BatchG_OnHeads_Common.png|900]]
![[BatchG_OnHeads_Epic.png|900]]

**Fit-test status (honest):**
- Fit was checked in Blender on R6 and R15/hair head proxies. Hats sit on the crown point and read at avatar scale.
- **Not yet tested in Studio** on real avatars: various head shapes and big hair, and staying on during ragdoll. That needs an upload (Holden: no uploads yet). ⚠️ verify in Studio before release.
- Expect big hair to poke through brimless hats (the bucket and cone); Roblox hats attach to the head top regardless of hair.

**Self-critique fixes:**
- Banana peel v2 (it was unreadable thin flaps).
- Rubber chicken v2: a bigger body with wings and drumsticks (it was a blob).
- Explicit white spots on the mushroom and spore caps (the paint spots didn't show at icon size).
- Fireflies escaping the jar (they were hidden in the opaque glass).
- Crystal halo lowered.
- Render fixes: dummies leaking into icons, overlapping and stray dummies in the on-head shots, framing.

**Weak hats fixed (Holden 2026-10-05: "fix the weak hats", then keep everything else as is):**
- **Flaming_Crown v2:** PAINTED orange/yellow teardrop flames with yellow inner cores and side licks, readable without Neon, plus glow cores (1,208 tris).
- **Rune_Crown v2:** chunky stone crown, a big glowing rune gem in front, carved glowing runes, and 3 rune stones orbiting (Wobble = spin).
- **Hot_Dog v2:** googly eyes and a grin on the sausage end, ketchup + mustard zigzags, a toothpick flag.
- Final rebuild: 43 models, 39 icons, 17,827 tris (max 1,208), `PREFLIGHT RESULT PASS objects=89 fails=0`.
- A replace script briefly dropped Summit_Crown; it was restored from a backup and verified (all 39 hats present).

## Squishies pick + cosmetics shop redo (2026-10-05)
- **USER:** Squishies = **"the purple with duck on it"**: option D Duck in **Grape**, i.e. `Squishies_Coin_D_Duck` + `Squishies_Coin_Grape_Paint.png` (`art/kit_batch_sq/`).
  - The `Squishies_Pile` S/M props are rebuilt from that exact coin: a low-poly copy with the icon only on the up-facing side and only on the top coins, 1.2k / 2.1k tris.
- **Cosmetics shop, two passes:**
  - **v2** was a pink boutique storefront. Holden: *"I don't want the shop in all that pink style, I want a fantasy shop/shack/storefront, use references from other games as well"*. Kept as `Shop_Cosmetics_Boutique` (rejected alternate).
  - **v3 `Shop_Cosmetics` (current)** is a fantasy hat shack, 6,190 tris:
    - a crooked 2-storey half-timbered building (cream plaster, dark beams, X-braces) on a chunky blue-grey cobble base;
    - an overhanging upper floor with round glowing lattice windows, a purple shingle gable roof and a crooked stone chimney with smoke puffs;
    - a corner turret whose roof is a giant floppy wizard hat (gold band, glowing stars: the shop icon from across the plaza);
    - a propped plank-shutter awning with a purple and gold valance and lanterns over an open counter (hat stands, register), and back shelves of hat boxes;
    - an iron-bracket hanging sign (BLANK faces) topped with a little hat, plus a barrel, crates, a mannequin, a flower pot and moss.
    - The NPC spot is behind the counter; the prompt anchor is at the counter front.
  - **Why it looks like this (references):**
    - **Islands** (screens 2, 6, 7): half-timber + stone shops, purple accents, lanterns, open counters.
    - **ayzenrbx** workshop sheet: a big readable icon on top of a chunky building.
    - **Fisch:** plank counters.
    - **OmniKoi2:** crooked, goofy shapes.
    - New captures are in `Assets/Reference-Captures/Roblox-Games/` (Islands, Bee Swarm, Grow a Garden, World // Zero, Arcane Odyssey, Adopt Me, Dungeon Quest; see the MANIFEST).
  - The shop accent is now purple and gold, not pink. Holden kept the per-structure colours "for now", so the gamepass (green/gold dome) and halfway (teal mushroom) shops are unchanged.
- Batch (f) rebuilt: `PREFLIGHT RESULT PASS objects=70 fails=0`. Final full rebuild with the gamepass options on 2026-10-05: 42 types, 52 models, `PASS objects=76 fails=0`.
- **Honest:** the shack is the strongest shop now. Next to it, the gamepass pavilion looks a bit "clean plastic", so it may want the same fantasy treatment (wood, stone, a crooked roof) if Holden agrees.

![[Shop_Cosmetics_Shack.png|600]]
![[BatchF_Hub_PlayerView.png|700]]

## Squishies coin options + weak-point fixes (2026-10-04, after Holden's batch (f) review)
**Squishies coin options** (`art/batch_sq.py`, `art/kit_batch_sq/`):
- **Holden:** "a pink/purple jelly coin, it should also have a cool icon on it as well, make a few so I have options".
- **The coin:** a round jelly coin with a soft bulge and a darker rim. The icon is raised on BOTH faces, because the pickup spins about Z. Radius 1.6, about 0.8 thick.
- **Colours:** pink base, plus the colour variants **Grape** and **Lavender** (same mesh).
- **Six icon options:**
  - **A** Face (cute face with blush)
  - **B** Star (gold)
  - **C** Heart (white)
  - **D** Duck (yellow rubber duck)
  - **E** Tower (a little wobbly tower: the game itself)
  - **F** Letter (bubbly gold "S")
- 828–1,340 tris. Preflight `PASS objects=6 fails=0 warns=1`.
- **Holden picks the icon and colour.** The Squishies_Pile props already switched to pink jelly and get the chosen icon after his pick.

![[Squishies_Options.png|700]]

**Weak-point fixes (Holden: "fix what's weak"):**
- **Pass_Piggyback_Saddle v2:** a big brown leather riding saddle (curved seat, pommel horn with a gold knob, raised cantle, stirrups, gold studs) strapped to a smaller green pack. It now reads as a saddle; v1 read as a green jar.
- **Waystone v2:** scaled ×1.45 (about 11.5 studs, taller than an avatar), so it holds its own next to the r11 checkpoint islands.
- **Mannequin trail:** about twice as thick, plus 6 sparkles.
- Batch (f) rebuilt: preflight `PASS objects=66 fails=0`.

## Fixes + batch (f) results (2026-10-04): waiting for Holden's review
**Fixes:**
- **Sleeping_Dragon v2** (in `batch_e2.py`): one continuous curled body with small painted scales and back spikes, a spade tail, a head resting on its paws (snout, nostrils, closed eyes, smile, horns, frills), folded wings and a glowing "Zzz". Variants: green, red, purple. 1,592 tris.
  - Honest: it reads as a sleeping dragon from a distance. Up close, the hull-merged body is a smooth blob without a distinct neck. That's fine for a far peak, but not as a hero prop.
- **Crystal_Shard_Platform v2:** a main flat-topped column plus 5 leaning pointed side columns, an inset top facet, glow cracks and a rock base.
- **Spell_Books v2:** 3 coloured tomes with straps, gold corner caps, runes and a ribbon, plus a floating open book with a glowing rune page.
- **Rune_Stone v2:** flat face, gold border, a different bold glyph per size, moss on top.
- **Text meshes** (signs, letters) now use curve resolution 2. Signposts dropped from 1.4k–3k tris to under 1k, and the batch (b) rebuild picked this up.

**Batch (f):**
- Code: `RubberTower/art/batch_f.py`, output in `art/kit_batch_f/`.
- **39 types, 47 meshes, 32 textures, 28,326 tris** (max 5,376: Shop_Gamepass).
- Preflight: `PASS objects=66 fails=0 warns=53`. Every colour-variation WARN is a `_Glow` part.
- **The manifest has `npc_spot` (10 structures) and `prompt_anchor` (22)** in local studs: origin at the bottom centre, front facing Blender −Y.

**Colour code per structure (PROPOSAL, for Holden):**
- Cosmetics: magenta tent.
- Gamepass: white + gold + green dome.
- Halfway: teal mushroom.
- Portal: cyan.
- Leaderboard: gold/white.
- Clinic: red/white + red cross.
- Tutorial: straw + green chalkboard.

**Text on models:**
- From Holden's own wording: "SKIP" on the pass props, "BONK CLINIC", "YOU MADE IT!".
- Mine, as placeholders: "SUMMIT!" on the photo frame, "!" and "?" toppers.
- Every other sign is a BLANK face for a SurfaceGui.

**Sheets:**

![[BatchF_Hub_PlayerView.png|700]]
![[BatchF_Hub_Overview.png|700]]
![[BatchF_Shops.png|700]]
![[BatchF_Structures.png|700]]
![[BatchF_Summit.png|700]]
![[BatchF_StallKit.png|700]]

**Self-critique:**
- **Fixed before showing:** the gamepass shop was 6.5k tris because of the text, now 5.4k. The hub layout was cramped, so it's spread out with a paved plaza and path. The crier's NPC spot hid the bell, now moved beside it.
- **Weak, honestly:**
  - ~~Pass_Piggyback_Saddle reads as a jar~~ (fixed, see above).
  - ~~The waystones are too small~~ (fixed: ×1.45).
  - The noticeboard's reference image is weak (no good leaderboard ref in the vault yet).
  - ~~Thin mannequin trail~~ (fixed).
- **Not done in this batch (later batches, per the brief):** NPC characters (Holden: later) and the real plaza floor tiles (batch h).

## Batch (a) results (2026-10-04): waiting for Holden's review
**Output and checks:**
- **Built:** 46 model types, 54 meshes with sizes, **55 textures** (43 base atlases + 12 colour variants), **55,366 tris in total**. The biggest is Obby_Wall_A at 10,292 across 4 parts.
- **Code:** `RubberTower/art/batch_a.py` (models) on `kitlib6.py` (framework).
- **Output:** `art/kit_batch_a/`: `models/*.glb`, `textures/`, `tiles/`, `sheets/`, and `manifest.json`. The manifest holds per-model tags, collider boxes (Blender coords; `rx`/`rz` in degrees), pivots for moving parts, stand points, refs, segment and tris.
- **Preflight:** `PREFLIGHT RESULT PASS objects=74 fails=0 warns=51`.
  - Glow parts: single colour and shared origin.
  - Moving parts (Blades, Arm, Fan): pivot origins.
  - Normals: the twins of double-sided blades, straw and leaves.
  - ⚠️ verify: 2 inward faces on Wobble_LilyPad, to check in Studio.
- **Not uploaded** (USER: not yet).

**Sheets (model | reference) and the diorama:**

![[BatchA_Diorama.png|700]]
![[BatchA_Bounce.png|700]]
![[BatchA_Ice.png|700]]
![[BatchA_Wobble.png|700]]
![[BatchA_Soft.png|700]]
![[BatchA_Movement.png|700]]
![[BatchA_Climbing.png|700]]
![[BatchA_Checkpoint.png|700]]
![[BatchA_Fixes.png|700]]

**Studio setup rules (from the code, for placement later):**
- **Wobble pieces** are single MeshParts tagged `WobblePlatform` directly (Box collision), with 4+ studs clear below.
- **Bounce and ice** carry the tag on the invisible top collider listed in the manifest.
- **Moving parts** rotate about their manifest pivot.
- **Glow parts** become Neon.
- **Every textured part** gets a SurfaceAppearance (ColorMap = its texture).

**Self-critique, first pass (all fixed before showing):**
- **Obby_Wall_A v5.1:** random placement exposed a flat core slab. It's now jittered rows that always cover the face, with masses varying ×2.5 and 30% jutting out 2–4 studs.
- **Stone:** the bricks were still too busy, which was Holden's beacon complaint. Now scale 0.14–0.15 (bricks about 3.5×1.6 studs) with 3 tone steps per stone.
- **Sky stone:** no more moss on S4 sky stone.
- **Ice and snow:** read as plain white. The ice palette is now bluer and the snow has blue shading and sparkles.
- **Smaller fixes:** the moss cushion drape is thinner, the mushroom spots are bigger, the lily pad is darker, and the cloud refs are corrected (the PPT image is a snow thumbnail).

**Honest weak points still open:**
- **Checkpoint_Island_S3:** the top is plain white snow and needs a frozen pond or more crystals. Will fix in batch (d).
- **Climb_MushroomSteps:** the rock backing reads as stacked boulders, not a wall.
- **Mushroom caps:** smoother than the v5 rock standard.
- **Ice slabs:** the S size is small next to the dummy.
- **Wall:** 10.3k tris, over the 9k budget, so the next pass reduces masses.
- **Variety:** many pieces share the same lavender-white stone. Segment palettes should diverge more in batches (c)–(e).

## Batches (b)–(e2) results (2026-10-04): built after Holden's "start with batch B, and after batch B make even more" (the landmarks batch was renamed (e2) when Holden assigned (f)–(h) to new work)
**How they're built:**
- Code: `RubberTower/art/batch_b.py` … `batch_f.py`, sharing `kitrun.py`, the runner (helpers, bake, export, manifest, sheets, an auto-framed diorama).
- Output: each batch has its own `art/kit_batch_<x>/` (GLBs, textures with colour variants, `manifest.json`, tiles, sheets, .blend).
- **Nothing is uploaded or placed** (USER).

**Colour language, held across every batch:**
- **Pink appears only on bounce pads.** S2 standing mushroom caps are teal, purple, tan or blue; the houses are classic red or purple; the decor mini-mushrooms are orange.
- **Pale cyan appears only on ice.** S3 standing crystal platforms are violet; snow is matte white with blue shading.

| Batch | Contents | Types / meshes / textures | Tris (total, max) |
|---|---|---|---|
| (b) S1 meadow + props + trees + creatures | Islets S/L, log S/M, stump S/M/L, plank S/M platforms; fence ×3, haystack, lanterns ×2, **silly signs ×4** (placeholder texts "THIS WAY UP ^", "DON'T LOOK DOWN", "CAUTION: WOBBLY", "<- NOPE"), chests open/closed, barrel, crate S/M, banner, flag, bench, fountain, bridge S/M, well, cart; puffy tree S/M/L (×3 tints), blossom, glow-fruit, twisted magic, crystal tree, bush S/M (×3 tints), giant flower (×4 colours), hanging and wall vines, lily cluster, glow grass; slime (×4), frog on a lily, bird (×3), butterfly (×3) | 38 / 50 / 40 | 34,686, max 3,092 |
| (c) S2 mushroom grove | Cap platforms S/M/L (teal/purple/tan/blue), mushroom islet M/L, root bridge, hollow log, shelf-fungus cluster; spore mushroom S/M/L (×4), fairy ring, mushroom lamp, glow moss, puffballs; toadstool house, mushroom house S/M (×2), fairy treehouse, giant mushroom tree; fern, root arch, root strands, Cliff_S2 module, snail, firefly jar | 20 / 26 / 22 | 30,288, max 6,610 |
| (d) S3 crystal-ice | Violet crystal shard platform S/M/L (×3), snowy islet S/M/L, crystal bridge, frozen pond (ice); frozen arch, frozen waterfall, icicles S/M, crystal cluster S/M/L (**6 colours**), crystal lantern, crystal rock S/M; snow pine S/M/L (×2), igloo, snowman, penguin, Ice_Cliff module | 15 / 25 / 21 | 15,100, max 5,400 |
| (e) S4 cloud kingdom + magic | Sky platforms round S/M/L and square S/M, temple column intact/broken, temple stairs, temple arch, rainbow bridge, floating pillar S/M, sky castle gate; rune stone S/M/L, **obelisk (v4 fix: thick, chunky chains, big runes)**, chained floating rock S/M, **portal (v4 fix: real 4-arm spiral)**, spell circle, potion bottles ×3 shapes (**×5 colours**), cauldron, spell books, wizard-hat post, orb pedestal, rune door | 19 / 29 / 23 | 24,220, max 3,210 |
| (e2) landmarks + backdrop | Wizard tower, crooked lighthouse, ruined arch, ruined pillars, **giant rubber duck**, wobbly knight on a spring, sleeping dragon, airship, floating castle; waterfall S/M, distant islands S/M/L, distant mountains ×2, cloud puffs S/M/L, Cliff_S1 and Cliff_S4 modules | 15 / 21 / 15 | 27,678, max 6,370 (Cliff_S1) |

**Self-critique fixes made before showing Holden:**
- **Rule-breaking colours:** pink mini-mushrooms on the stump and log, and pink toadstool and mushroom-house caps, broke the "pink = bounce" rule. Now orange, red and purple.
- **Diorama framing:** the (b) diorama was framed badly, so all dioramas now pack items by size and auto-frame.
- **(b):** the crystal tree was thin, now bulked up; vines and glow grass are thicker and denser; the leaf "turtle-shell" outlines are thinner.
- **(c):** spore mushrooms had flat "table" caps, now domed; the fairy ring was 4,000 tris, now about 800 with low-poly mushrooms; glow moss was a blob, now a rock with a moss cap and mini mushrooms.
- **(d):** the snow-pine caps were too small, now bigger.
- **(e):** the potion liquid was hidden inside the opaque glass, so the variants looked identical. The body is now the coloured liquid.
- **(e2):** Cliff_S4 had brick paint on boulders, now a white-lavender rock paint; the cloud puffs were jagged, now rounder.


**Preflight, all PASS with 0 FAILs (2026-10-04):**
- (b) 59 objects, 45 WARNs · (c) 42 / 44 · (d) 40 / 29 · (e) 43 / 33 · (e2) 27 / 23.
- Verified that every colour-variation WARN is a single-colour `_Glow` (Neon) part.
- The remaining WARNs are origin (glow, moving and offset parts) and normals (the twins of double-sided blades, leaves, cloth and straw).

**Totals so far:**
- Batches (a)–(e2): **153 model types, 205 meshes, 176 textures** (base atlases + colour variants).
- About 187k tris across the whole library. It's a kit, not one scene.
**Still weak (honest):**
- **Sleeping_Dragon** is a lumpy blob, needs a proper redo.
- **Crystal_Shard_Platform** is squat and plain.
- **Spell_Books and Rune_Stone glyphs** are simple.
- **Dioramas (c) and (d):** the big cliff modules hog the frame.
- **Distant islands** are very plain (fine at 100+ studs, weak up close).


## Related
[[Rubber-Tower-Valley-Kit]] · [[Rubber-Tower-Kit-Style-History]] · [[Rubber-Tower-Art-Style-Guide]] · [[Rubber-Tower]]
