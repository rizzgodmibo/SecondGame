---
tags: [assets/models, project/rubber-tower]
status: draft
updated: 2026-10-05
confidence: medium
---
# Rubber Tower Valley Kit

## TL;DR
- **Style:** v5 is LOCKED ([[Rubber-Tower-Art-Style-Guide]]). The mechanic colour code is approved: pink = bounce, pale cyan = ice, lime = wobble, cream = soft, red rubber = movers.
- **Status (2026-10-04):**
  - Built and reviewed by Holden: (a) mechanics, (b)–(e) segments + magic, (e2) landmarks + backdrop, and (f) NPC shops + structures (plus fixes).
  - **Next session:** (g) crazy hats, then (h) misc, each with a review stop.
  - **Squishies coin: CHOSEN** (USER 2026-10-05): D Duck on the Grape purple coin.
  - **Gamepass shop: CHOSEN** (USER 2026-10-05, "for now"): `Shop_Gamepass_Fantasy_B_Caravan`.
  - **Batch (g) hats: built and reviewed** (39 hats + display set). Prices set by rarity on 2026-10-05 (USER): [[Rubber-Tower-Squishies-Economy]].
  - **Batch (h) extra + misc: BUILT 2026-10-05**, reviewed by Holden, then **v2 fixes the same day**: secret room exterior + cutaway, chunky segment gates, clipped hedge, readable moon lantern, emblem-only badges, Hidden_Duck, and a snowy twin of the hub decor; then v3: rocky hideout secret room, smooth hedge paint, batch (b) winter twins. **Waiting for Holden's review.** Next after (h): upload the kit to the test place to check hats on real avatars and in ragdoll (only with Holden's OK).
  - **Cosmetics shop v3** is a fantasy hat shack (Holden rejected the pink boutique). See [[Rubber-Tower-Kit-Batch-Results]].
- **Code:**
  - `RubberTower/art/batch_*.py` on `kitlib5.py` (paint recipes + bake), `kitlib6.py` (primitives, recipes, review stage) and `kitrun.py` (runner: bake, export, manifest, sheets, diorama).
  - Each batch outputs to `art/kit_batch_<x>/`: GLBs, textures with colour variants, and `manifest.json` (tags, colliders, pivots, `npc_spot`, `prompt_anchor`, refs, tris).
- **UPLOADED 2026-10-05 (Holden's OK: private test place only, nothing public).** See "Test-place upload" below.
  - Batches (a)–(h) as 13 GLB Models (one per batch; a and h split under the 50 MB Open Cloud limit).
  - Staged in Studio as `ServerStorage.Kit.Batch_A…H` (557 models).
  - 39 hats built as Accessories in `ServerStorage.Hats`.
  - Nothing is placed in the map yet; the only placed pieces are the test leap pad + cushion in `Workspace.TestPlace.LeapTest`.
- **New 2026-10-05 (USER Leap of Faith):**
  - `Summit_Leap_Pad`: a stone base with a crooked plank over the edge; the pink spring tip is its own part `LeapPad`, tagged `LeapOfFaith` + `BouncePad` with a `LaunchSpeed` attribute; plus a "LEAP OF FAITH!" sign and a wind sock.
  - `Landing_Cushion`: a mallow cushion r12 with a target and puffy rim.
  - Both in batch (h).
- **Results and sheets** per batch: [[Rubber-Tower-Kit-Batch-Results]]. **Style history** (v1 to v5): [[Rubber-Tower-Kit-Style-History]].

## Full kit list (v5 style, ordered by Holden 2026-10-04)
**How to read the list:**
- **Columns:** name — sizes in studs (S/M/L) — tri budget per mesh — references — segment — notes.
- **Variant colours** reuse the same mesh with a re-baked texture.
- **Reference keys:**
  - **V5:** v5 kit (`AssetLibrary/models/rubber-tower-kit-v5/`);
  - **OK1–4:** OmniKoi2 img-1–4;
  - **HAO:** haooffiso Sky_Island;
  - **MR:** Mossy Rocks;
  - **ORCA:** Orca_Environ;
  - **M0TO:** M0TOPRINCESS variants;
  - **PPS:** Parkour Spiral;
  - **TOS:** Tower of Sky;
  - **FIS:** Fisch;
  - **VFX:** `Assets/VFX/TexturePack`;
  - **HP:** Holden-Picks (empty so far).
- **Segments:** S1 meadow, S2 mushroom grove, S3 crystal-ice, S4 cloud kingdom, All = any.
- **Tags:** B = `BouncePad`, I = `IcePlatform`, W = `WobblePlatform` (a single MeshPart, about 12×12, 4+ studs clear underneath).
- **Status:** ticked = built, rendered and preflight-passed; Holden's review is a separate gate.

### Batch (a): obby mechanic models (built first)
**Fixes to v5 pieces**
- [x] Obby_Wall_A v5.1: varied mass sizes and depths, no grid (68×64) — 9k — V5, OK1, PPS — S1
- [x] Checkpoint_Beacon v5.1: chunky stones, fewer bigger bricks (15×15×21) — 2k — V5, HAO — S1
- [x] Meadow_Islet_M v5.1 and Checkpoint_Islet v5.1: puffy canopy bush (r7 / r11) — 1.5k / 2k — V5, OK1 — S1

**Bounce (hot pink and magenta; tag B on an invisible top collider)**
- [x] Bounce_Mushroom S/M/L (cap ⌀8/12/16): fat cap with spots and a goofy face on the stem — 1.2k — OK3, V5 — S1/S2 — variants red, pink, purple, orange
- [x] Bounce_FlowerPad S/M (⌀10/14): giant flat flower — 900 — OK1 — S1
- [x] Bounce_Jelly S/M (8/10): slime dome with a face and bubbles — 800 — ORCA — All — variants pink, green, blue
- [x] Bounce_SpringPad (⌀8): cushion on a metal coil — 1k — V5 — All
- [x] Bounce_Leaf (14×7): giant curved leaf ledge — 600 — OK1 — S1/S2

**Ice (pale cyan and white; tag I)**
- [x] Ice_Slab S/M/L (8×8 / 12×12 / 16×10): frost cracks, snow lumps, icicles — 800 — HAO, V5 — S3
- [x] Ice_PuddleIslet (r7): snowy islet with a frozen puddle top — 1.4k — V5 — S3
- [x] Ice_CrystalLedge (10×7): snowy rock ledge with icicles and shards — 1.2k — V5 — S3
- [x] Ice_Slide (6×20, 8 drop): ramp with snowy rails — 1k — TOS — S3

**Wobble (lime and yellow jelly; tag W; one MeshPart, no glow)**
- [x] Wobble_JellyCube (12×12×4): wobbly outline, bubbles — 600 — ORCA — All — variants lime, orange, purple
- [x] Wobble_LilyPad (⌀12): notch and veins — 400 — OK1 — S1/S2
- [x] Wobble_SeesawLog (14×4) + Seesaw_Base (stump fulcrum) — 800 + 400 — V5 — S1
- [x] Wobble_Raft (12×12): logs with rope bindings and corner rings — 1.2k — FIS — S1
- [x] Wobble_StoneDisc (⌀12) + Spring_Base (metal coil decor) — 800 + 600 — HAO — S3/S4

**Soft rest (cream, white and pastel; no tag; never a spawn)**
- [x] Soft_Cloud S/M (10/14): puffy cloud pad — 900 — HAO, PPT — S4/All
- [x] Soft_Pillow (10×7×2.5): seams, buttons, tassels — 600 — M0TO — All — variants pink, blue, cream
- [x] Soft_Marshmallow (⌀6 stack): 2–3 stacked marshmallows — 500 — OK3 — S4/All
- [x] Soft_HayBale (8×5×4): straw and twine — 400 — FIS — S1
- [x] Soft_MossCushion (⌀8): moss mound on rock with flowers — 900 — MR — S1/S2

**Movement (future mechanics; moving parts are separate MeshParts)**
- [x] Move_RopeBridge (24 long): sagging planks, posts — 1.5k — V5 — All
- [x] Move_Tightrope (20): two posts and a rope — 400 — V5 — All
- [x] Move_SwingPaddle: pivot hub + arm with a red rubber paddle — 800 — PPS — All
- [x] Move_SwingHammer: pivot + rubber mallet — 800 — PPS — All
- [x] Move_Windmill: crooked tower + Blades part — 2.5k — OK1 — S1
- [x] Move_FanVent (⌀8): stone ring, grate, Fan part, glow — 1k — HAO — S3/S4
- [x] Move_Slingshot: Y-frame, rubber band, pouch — 700 — V5 — S1
- [x] Move_VineConveyor (4×20): braided vine belt with leaves and rollers — 1.2k — MR — S2

**Climbing**
- [x] Climb_Ladder (12 tall): crooked rungs, rope bindings — 500 — V5 — All
- [x] Climb_VineWall (10×16): vine net on rock — 1.5k — MR — S1/S2
- [x] Climb_MushroomSteps: 4 stair-step shelf mushrooms on a rock strip — 2k — OK3 — S2
- [x] Climb_ShelfFungus S/M (6/9 wide): wall ledge — 500 — MR — S2 — variants orange, teal
- [x] Climb_Scaffold (10×10×16): 2 decks + ladder — 2.5k — V5 — S1
- [x] Climb_SpiralSteps (pillar ⌀8, 30 tall, 12 steps): stone steps round a pillar — 4k — PPS — All

**Checkpoint**
- [x] Checkpoint_Island S1/S2/S3/S4 (r11, themed tops and undersides) — 2k — V5, HAO — per segment
- [x] Checkpoint_Beacon S1/S2/S3/S4 (stone / mushroom-wood / ice-crystal / gold temple arch) — 2k — V5, HAO — per segment
- [x] Soft_FallNet (14×14): rope net on 4 posts — 1k — V5 — All

### Batch (b): S1 meadow + fantasy props (BUILT 2026-10-04, see [[Rubber-Tower-Kit-Batch-Results]])
- [x] Meadow islets S/M/L (r5/7/10), Log_Platform S/M, Stump_Platform S/M/L, Plank_Platform S/M, Picket_Fence (straight, corner, broken), Haystack, Windmill (big landmark)
- [x] Props: Lantern (post and hanging), Signpost ×4 silly signs, Treasure_Chest (open/closed), Barrel, Crate S/M, Banner, Flag, Bench, Fountain, Wood_Bridge S/M, Well, Cart
- [x] Trees: Puffy_Tree S/M/L (3 tints), Blossom_Tree (pink), GlowFruit_Tree, Twisted_Magic_Tree, Crystal_Tree; Bush S/M ×3 tints; Giant_Flower ×4 colours; Vines (hanging, wall); Lily_Pad; Glow_Grass patch
- [x] Creatures (decor): Slime ×4 colours, Frog_On_LilyPad, Bird ×2, Butterfly ×3 colours

### Batch (c): S2 mushroom grove (BUILT 2026-10-04)
- [x] Mushroom_Cap platforms S/M/L × 4 colours, Shelf_Fungus wall ledges (shared with (a)), Spore_Mushroom (glowing) ×3, Toadstool_House (door and windows, glow), Mushroom_House S/M, Roots (arches, strands), Vine curtains, Glow_Moss, Fairy_Treehouse, S2 cliff wall variant (teal grass, purple rock)

### Batch (d): S3 crystal-ice (BUILT 2026-10-04)
- [x] Crystal_Shard platforms S/M/L, Ice_Slab (from (a)), Frozen_Arch, Snowy_Islet S/M/L, Frozen_Waterfall, Icicle clusters, Crystal clusters in 5+ colours, Snow_Pine trees ×3, Ice cliff wall variant, Igloo/ice hut

### Batch (e) + (e2): S4 cloud kingdom + magic (e), landmarks + backdrop (e2, first built as "f") (BUILT 2026-10-04)
- [x] Cloud platforms S/M/L, Sky_Temple pieces (floor tile, column, broken column, stairs, arch), Rainbow_Bridge, Floating_Pillar, Sky_Castle_Gate, Floating_Castle, Airship
- [x] Magic: Rune_Stone ×3, Obelisk (v5 fix: thicker, chunky chains, big runes), Floating_Chained_Rock S/M, Portal (real spiral), Spell_Circle (decal + glow ring), Potion_Bottles ×5, Cauldron, Spell_Books (floating), Wizard_Hat_Post, Orb_Pedestal ×3, Rune_Door
- [x] Buildings: Wizard_Tower, Crooked_Lighthouse, Ruined_Arch, Ruined_Pillars, Giant_Rubber_Duck statue, Wobbly_Knight statue, Sleeping_Dragon (far peak)
- [x] Backdrop: cliff and wall variants per segment, Waterfall S/M, Distant_Floating_Islands ×3, Distant_Mountains ×2, Cloud puffs ×3

### Fixes ordered 2026-10-04 ("redo the dragon, finish the rest")
- [x] Sleeping_Dragon v2: proper curled body, readable head with snout, horns, closed eyes, folded wings with arm bones, spade tail, painted scales — (e2)
- [x] Crystal_Shard_Platform v2: cluster of columns, faceted inset top, glow cracks (was squat and plain) — (d)
- [x] Spell_Books v2: corner caps, straps, ribbons, rune on the cover — (e)
- [x] Rune_Stone v2: bold carved glyphs with a carved border — (e)

### Batch (f): NPC shops and structures (Holden 2026-10-04)
**Rules for every structure:**
- Scaled to R15 (5–6 studs). Counters about 3.2 studs high (waist).
- Roofs at least 11 studs high, so the camera never clips.
- An open front, so the NPC is visible from the plaza and on a phone.
- One strong colour per structure.
- The manifest lists `npc_spot` and `prompt_anchor`.

**Colour code (PROPOSAL):**
- Cosmetics: magenta/purple tent.
- Gamepass: gold + Robux green.
- Halfway: S2 teal mushroom.
- Portal: cyan.
- Leaderboard: gold.
- Clinic: white + red cross.

**Shops (each with an NPC):**
- [x] Shop_Cosmetics (hub): tailor tent/boutique, mannequins in a trail + hat, clothes rack, mirror, counter — new — refs OK3, AYZ — Hub
- [x] Shop_Gamepass (hub): different shape (round kiosk-pavilion), gold trim, Robux-green accents. Pass props: Banana_Bunch, Piggyback_Saddle (Buddy Carry), SKIP_Balloon — new — HAO, AYZ — Hub
- [x] Shop_Halfway_S2 (CP2): small mushroom stall, reuses S2 cap paint and teal palette — new (mushroom parts reuse the batch-c builders) — OK4 — S2

**Structures (not shops):**
- [x] World_Portal_Plaza: big gate ring (scaled-up Magic_Portal design, new mesh), World_Pedestal Locked/Unlocked (variants) — Hub
- [x] Leaderboard_Plaza: Podium_123 (shared with the summit), Noticeboard_Frame (blank SurfaceGui face), Statue_Plinth — Hub
- [x] Quest_Board (blank paper face) · Daily_Mailbox · Gift_Chest_Pedestal — Hub
- [x] Codes_Wishing_Well: new mesh, glowing water, coins and a blank code sign (the (b) Well stays for decor) — Hub
- [x] Town_Crier_Podium + Bell — Hub
- [x] Tutorial_Hut (by the start gate) · Bonk_Clinic tent (bandages, goofy stretcher, red-cross flag) — Hub
- [x] Friend_Campfire: fire ring (glow), log seats — Hub/All
- [x] Waystone S1/S2/S3/S4 (themed checkpoint teleport kiosks) — per segment
- [x] Summit set: Victory_Podium (= Podium_123), Confetti_Cannon, Photo_Frame, You_Made_It_Arch — Summit

**Modular stall kit (for future shops):**
- [x] Stall_Frame S/M/L · Stall_Counter S/M · Awning ×6 colours (variants) · Tent_Roof · Kiosk
- [x] Hanging_Sign (blank) · Sign_Board (blank) · Shelf · Jar_Set · Goods_Crate · Display_Pedestal · Price_Tag · Squishies_Pile · Cash_Register · Service_Bell
- Reused from earlier batches, not rebuilt: Crate, Barrel, Lantern_Post, Lantern_Hanging, Banner, Flag, Bench, Signposts, Treasure chests, Potion_Bottle.
- ⚠️ PROPOSAL: the Squishies look. The currency's appearance is undecided, so the coin piles use a gold jelly-blob coin until Holden picks a design.

### Batch (g): crazy hats (Holden 2026-10-04; prices later)
**Rules:**
- Each hat is an Accessory: a Handle MeshPart + HatAttachment.
- 500–2k tris, on shared atlases.
- Wobble parts are separate, with pivots in the manifest.
- Fit-tested on R6 and R15 heads and hair, and stays on during ragdoll.
- Rendered with one icon rig, plus on a dummy head.

**Rarity colours (Art-Direction):** Common grey, Uncommon green, Rare blue, Epic purple, Legendary gold, Mythic red/pink.

| # | Hat | Rarity | Segment / where sold | Wobble or glow part |
|---|---|---|---|---|
| 1 | Bucket_Hat | Common | Hub | — |
| 2 | Traffic_Cone | Common | Hub | — |
| 3 | Plunger | Common | Hub | wobble: handle |
| 4 | TP_Top_Hat (toilet-paper roll) | Common | Hub | wobble: paper tail |
| 5 | Banana_Peel_Hat | Common | Hub | wobble: peel flaps |
| 6 | Sock_Puppet | Common | Hub | wobble: mouth |
| 7 | Pizza_Slice | Common | Hub | wobble: cheese drip |
| 8 | Propeller_Beanie | Uncommon | Hub | spin: propeller |
| 9 | Hot_Dog | Uncommon | Hub | — |
| 10 | Fish_Hat | Uncommon | Hub | wobble: tail |
| 11 | Googly_Antennae | Uncommon | Hub | wobble: 2 antennae |
| 12 | Rubber_Duck_Hat | Uncommon | Hub | — |
| 13 | Mushroom_Cap_Hat | Uncommon | Hub | — |
| 14 | Snowman_Head | Uncommon | Hub | — |
| 15 | Rubber_Chicken | Rare | Hub | wobble: floppy neck |
| 16 | Birthday_Cake | Rare | Hub | glow: candle flames |
| 17 | Wizard_Star_Hat | Rare | Hub | wobble: floppy tip |
| 18 | Jelly_Slime_Hat | Rare | Hub | wobble: whole slime |
| 19 | Rain_Cloud | Rare | Hub | glow: rain drops |
| 20 | Witch_Cauldron_Hat | Rare | Hub | glow: brew |
| 21 | Frog_Hat | Rare | Hub | wobble: tongue |
| 22 | Dragon_Hood | Epic | Hub | wobble: horns |
| 23 | Tiny_Castle | Epic | Hub | wobble: flag |
| 24 | Crystal_Halo | Epic | Hub | glow + spin: halo |
| 25 | Rune_Crown | Epic | Hub | glow: runes |
| 26 | Spring_Head (boing ball) | Epic | Hub | wobble: spring + ball |
| 27 | Viking_Rubber_Helmet | Epic | Hub | wobble: floppy horns |
| 28 | Giant_Gold_Crown | Legendary | Hub | glow: gems |
| 29 | Rainbow_Arch_Hat | Legendary | Hub | — |
| 30 | Orbiting_Planet | Legendary | Hub | spin: planet + ring |
| 31 | Mini_Wobbly_Tower ("Rubber Tower" on your head) | Legendary | Hub | wobble: tower |
| 32 | Flaming_Crown | Legendary | Hub | glow: flames |
| 33 | Summit_Crown | Mythic | Summit only (reward) | glow + spin |
| 34 | Cosmic_Jellyfish | Mythic | Hub | glow + wobble: tentacles |
| 35 | Duck_King (duck wearing a crown, riding a wave) | Mythic | Hub | wobble: duck |
| 36 | Snail_Shell_Helm | Uncommon | **Halfway (S2) only** | wobble: eye stalks |
| 37 | Spore_Puff_Cap | Rare | **Halfway (S2) only** | glow: spores |
| 38 | Firefly_Jar_Hat | Rare | **Halfway (S2) only** | glow: fireflies |
| 39 | Toadstool_Top_Hat | Epic | **Halfway (S2) only** | wobble: brim |

**Hat display set:** Hat_Stand · Mannequin_Head · Hat_Rack · Glass_Display_Case (for rares).

**BUILT 2026-10-05:** all 39 hats + the display set, with icons and on-head fit renders. See [[Rubber-Tower-Kit-Batch-Results]]. **Uploaded and Studio-tested 2026-10-05:** fit + ragdoll pass after the attachment fix (see "Test-place upload").

### Batch (h): extra and misc (Holden 2026-10-04; variants over unique meshes)
"(reuse X)" means it already exists in the kit and gets placed or recoloured instead of rebuilt.

**Hub and village:**
- [x] Plaza_Floor tiles · Path pieces (straight, curve, T) · Hedge S/M · Flower_Box · Spawn_Pad · Segment_Entry_Gate S1–S4 · Height_Marker sign (blank number face) · AFK_Seat
- Reuse: Lantern_Post, Bench.

**Fantasy:**
- [x] Sword_In_Stone · Dragon_Skeleton · Garden_Gnome ×3 poses · Beehive · Watermill_Wheel · Mine_Cart + Track · Hot_Air_Balloon (×3 colours) · Kite (×3) · Sky_Jellyfish · Sky_Whale · Totem · Bell_Tower · Wind_Chimes · Firefly cluster (glow points)
- Reuse: toadstool street lamp (= Mushroom_Lamp), magic fountain (Fountain + glow water variant), airship.

**Secrets:**
- [x] Hidden_Cave_Entrance · Secret_Ledge with a chest (reuse Treasure_Chest) · Goofy_Secret_Room shell

**Gameplay items:**
- [x] Banana_Peel (placeable, pass) · Squishies_Pickup (CHOSEN 2026-10-05: D Duck on the Grape purple coin) · Summit_Crown prop (reuse: the hat on a display pedestal) · Trophy Gold/Silver/Bronze (variants) · Title_Plaque · Checkpoint_Flag S1–S4 · **Daily_Chest_Day7** (added 2026-10-05; days 1–6 reuse Daily_Mailbox + Gift_Chest_Pedestal)

**Goofy:**
- [x] Rubber_Chicken · Rubber_Band_Ball · Squeaky_Hammer · Whoopee_Cushion · Cone_With_Wizard_Hat · Wet_Floor_Sign · Pool_Ring · Donut_Float · Toy_Blocks · Scarecrow · Lost_Sock_Branch · Rubber_Boot

**Ground clutter:**
- [x] Pebble_Cluster · Rock_Pile · Fallen_Log · Decor_Stump · Clover_Patch · Reeds_Cattails · Stepping_Stones · Puddle · Leaf_Pile · Giant_Acorn · Giant_Pinecone
- Reuse: mushroom rings = Fairy_Ring.

**Village life:**
- [x] Picnic_Blanket + basket · Laundry_Line · Flower_Pot ×3 · Wheelbarrow · Garden_Tools · Apple_Crate · Pumpkin_Patch · Carrot_Patch · Birdhouse · Doghouse · Camping_Tent · Telescope · Arrow_Street_Sign · Water_Trough · Bunting · String_Lights · Weather_Vane

**Magic clutter:**
- [x] Crystal_Ball_Stand · Alchemy_Table · Floating_Candles · Magic_Mirror · Enchanted_Broom · Levitating_Teacups · Scroll_Rack · Wand_Rack · Star_Lantern · Moon_Lantern

**Per segment:**
- S2: reuse Puffball_Cluster (giant scale) and Spore_Mushroom; new Giant_Snail (scaled-up variant of Snail).
- S3: reuse Snowman and Penguin; new Frozen_Fish_Block, Ice_Sculpture ×2.
- S4: new Cloud_Sheep, Star_Decor, Golden_Harp, Sundial, Winged_Statue.

**Seasonal swap set:**
- [x] Pumpkin, Jack_O_Lantern (glow) · Wrapped_Present ×3 colours
- [x] snowy hub set (USER 2026-10-05: "not just the hedge"): `*_Snowy` twins with real snow caps for Plaza_Floor, Path_Piece, Hedge, Flower_Box (holly), Spawn_Pad, Height_Marker, Swing_Bench. Batch (b) hub decor twins added the same day: Lantern_Post, Bench, Barrel, Well and a frozen Fountain (built from batch (b)'s own functions + snow). The shops (batch f) have no winter twin yet: their roofs are custom shapes, so snow would need per-shop work. Worth doing when a winter event is planned.
- [x] Hidden_Duck (yellow + Pink/Blue/Mint) for the Duck Whisperer title · Checkpoint_Emblem S1–S4 (emblem-only badges for small icons)

**BUILT 2026-10-05:** everything above except the extra snowy variants (reuses as noted, Decor_Stump = Stump_Platform, Apple_Crate = Goods_Crate, Rubber_Chicken prop = the hat). Results, icons and self-critique: [[Rubber-Tower-Kit-Batch-Results]]. Waiting for Holden's review.

## Test-place upload (2026-10-05, Holden's OK, private test place only)
**Asset IDs** (Model, creator MiboRBX, via `AssetLibrary/tools/upload_model.sh`; also in `RubberTower/art/upload/ids.txt`):

| GLB | Asset ID |
|---|---|
| kit_batch_a_p1 | 74227909319514 |
| kit_batch_a_p2 | 125790743025557 |
| kit_batch_b | 84718417988392 |
| kit_batch_c | 111213643907842 |
| kit_batch_d | 131748576604721 |
| kit_batch_e | 82281656179651 |
| kit_batch_e2 | 99310856467237 |
| kit_batch_f | 120090100629543 |
| kit_batch_g (hats) | 120005431087435 |
| kit_batch_h_p1 | 138076362223921 |
| kit_batch_h_p2 | 89689331119959 |
| kit_batch_h_p3 | 116120445346284 |
| kit_batch_h_p4 | 136072609509109 |

| kit_batch_h_leap3 (Summit_Leap_Pad v2 + Landing_Cushion) | 134520179836644 |
| kit_map (Valley_Floor_S1 + Pond_Basin, map v3) | 89785848208249 |

**Later on 2026-10-05:**
- **Summit_Leap_Pad v2** (Holden: bigger and readable): 12×10 base, 18-stud 3-plank board with white chevrons pointing over the edge, a gold arch whose "LEAP OF FAITH!" banner faces the player walking up, a big pink spring tip (`LeapPad` part), wind sock. Staged in `Kit.Batch_H` (v1 parked as `ServerStorage.Summit_Leap_Pad_v1`).
  - Place it with the base sunk so its top is ~0.5 above the ground (the base is a 2.6-stud step otherwise).
  - Board collision = PreciseConvexDecomposition (Default fidelity floats ~2 studs above the plank).
- **batch_map.py** (new):
  - `Valley_Floor_S1`: 260×260, 8.2k tris, a 2048 atlas, crisp per-face zones (3 meadow greens in big blobs + dirt paths) and a square hole for the pond.
  - `Pond_Basin`: 44×44 with a bowl 5 deep, sand shore and a `Water` part.
- **`batch_h.py --out <folder>`** builds into another folder (avoids the `--only` wipe pitfall).
- **`art/map/dump_colliders.py`** → `kit_colliders.json`: every kit collider and stand point as an offset from the main mesh centre in Studio axes. **Blender (x, y, z) → Studio (−x, z, y)**, verified on the leap pad: the predicted base top 401.55 matched the measured one.

**How it was staged:**
- `art/export_batches.py` writes one GLB per batch (`dir:N` splits it). Colour variants become re-textured copies named `<Instance>__<Variant>`. It also writes `upload/<batch>_index.json` (glow colours, hat data, pivots).
- In Studio the import nesting is flattened, and each MeshPart gets a SurfaceAppearance ColorMap. Glow parts become Neon in the spec colour.
- The importer turns models 180°, so the hat attachment offset in Studio = (−x, y, −z) of the manifest value.

**Hats (Studio test 2026-10-05, [[2026-10-05-Rubber-Tower-Studio-Test]]):**
- Fit is OK on R6/R15, 4 avatars, and big hair.
- Fixed: 58 wobble-joint attachments had world coordinates in `Position` (the parts got flung away in play).
- **Equip rule:** move every part to its final spot, then parent (WeldConstraints bake their offset). See `DevStress putHat`.
- Weak: the TP_Top_Hat streamer hangs over the face.

## Map v3 slice pieces (2026-10-05 evening, private test place)
After Holden's build-1 critique ([[Rubber-Tower-Map-Build-Plan]]):
- **`art/batch_v3.py`:**
  - the soft rock paint `rocks` (no black crack lines: facet tones + soft crevices in a darker shade of the same rock);
  - **cliff kit v2:** CliffV2_Tall / Stepped / Overhang / Buttress / Arch / Rubble / Cave, each × base, Sand, Moss, Rose, angular slabs over a solid core;
  - Waterfall_V2 (Body + Sheet1–3 + Pool);
  - Lake_Rock_Island (vine net = TrussPart collider), Lake_Rock_Small, Wood_Pile;
  - Yard_Wall (warm dry stone, 9 tall), Hedge_Tall (8 tall);
  - Start_Gate_V3 (3D "START").
  - Uploads: kit_v3w_p1 **78370018555865**, kit_v3w_p2 **85508406559984** (split: 63 MB > the 50 MB Open Cloud cap), kit_v3g **81495698382164**.
- **`art/ground_v3.py`:** 16 ground tiles + 4 stylised water meshes, painted per texel with numpy. Upload kit_ground3c **88000763253329** (PNG textures). The earlier kit_ground3 96861660767510 (JPEG) came in untextured; kit_ground3b 94927423577960 is superseded.
- Preflight PASS on all (the stepped cliff is 11k tris, over its 9k target and under the 20k cap).

## Pitfalls
- **GLB with JPEG textures imports untextured** (2026-10-05, kit_ground3): use PNG (`export_image_format="AUTO"`).
- **Blender's `image.save()` on a generated image wrote all-black PNGs** in headless runs (2026-10-05). `ground_v3.py` writes its PNGs itself (numpy + zlib) and loads them back.
- **Setting `MeshPart.CollisionFidelity` from the Studio MCP is silently ignored.** `ApplyMesh` from `AssetService:CreateMeshPartAsync(..., {CollisionFidelity = ...})` works (`BuildValleyB.setFidelity`). And a real Hull fills an arch's opening: decor keeps Default.
- **Test hats in play, not Edit** (2026-10-05). Edit mode doesn't simulate constraints. Wobble joints 7,600 studs off looked fine in Edit and destroyed the parts in play.
- **Studio TexturePack 429** (2026-10-05): at play start Studio may log `Failed to upload TexturePack … Rate limit exceeded` for SurfaceAppearances. The textures still showed. ⚠️ verify after publishing.
- **Convex hulls fill concave shapes.** A star made with `m.hull` turns into a pentagon, and a "rim" hull of two rings is a solid disc that hides anything under it (batch (h) spawn pad). Use `star()` in `batch_h.py`, or `tube()` for rims.
- **`--only` rebuilds wipe the batch folder.** `run_batch` writes the manifest, .blend and models for ONLY the specs it built. Running `batch_x.py -- --only A` after `rm -rf kit_batch_x` leaves just A. This happened to batch (f) on 2026-10-05: a gamepass test left 3 of 52 models, and it was caught at commit time and fully rebuilt. **Test builds go to a copy with a different OUT folder**, as was done for the batch (g) hat fixes.
- **Git:** generated output (GLBs, .blend, textures, renders) is gitignored in the Rubber Tower repo and rebuilds from the seeded scripts. Only scripts, manifests, preflight logs and hat icons are committed. Approved models are archived in `AssetLibrary/models/rubber-tower-kit-v4`/`-v5`.
- **Public vault:** review sheets that composite third-party references ("model | reference") are gitignored; our own renders are tracked.

## Where the rest lives
- **[[Rubber-Tower-Kit-Batch-Results]]**: results, sheets, preflight and self-critique per batch, for the fixes, (f), (a) and (b)–(e2), plus the Squishies coin options.
- **[[Rubber-Tower-Kit-Style-History]]**: the v1 to v5 style tests and the pipeline lessons behind the locked style.
- **[[Rubber-Tower-Valley-Kit-E-Copy-2026-10-04]]** (archived): the pre-restructure version of this note from E:\Vault, kept during the 2026-10-06 sync so no detail was lost. Statuses there are out of date.

## Related
- [[Rubber-Tower]] · [[Rubber-Tower-Kit-Batch-Results]] · [[Rubber-Tower-Kit-Style-History]] · [[Rubber-Tower-Build-Status]] · [[Roblox Asset Pipeline Skill]] · [[Blender to Roblox Asset Pipeline]] · [[Art Direction Feedback]] · [[Rubber-Tower-Reference-Obbies]]
