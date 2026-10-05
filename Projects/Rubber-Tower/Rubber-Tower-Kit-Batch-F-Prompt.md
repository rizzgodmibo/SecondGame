---
tags: [project/rubber-tower, feedback/art]
status: final
updated: 2026-10-04
---
# Rubber Tower: batches (f)–(h) prompt (shops, hats, extra models)

Paste the block into Claude Code AFTER batch (e) is finished and reviewed. Everything here is NEW: not in the batch (a)–(e) lists in [[Rubber-Tower-Valley-Kit]].

```
Batches (a)–(e) are done. Next come three NEW batches, in this order:
- (f) NPC shops and structures;
- (g) a crazy hats collection;
- (h) extra and misc models.
Add all of it to the checklist in [[Rubber-Tower-Valley-Kit]] first. Check the list against what (a)–(e) already built and skip anything that already exists (reuse it or make a colour variant instead).

WHY: we need a few NPCs in this game, and they need places to be. Not full houses: storefronts, stalls or small open structures where an NPC stands and players walk up to them. For now that's three shops (below). Other structures support systems from [[Rubber-Tower]] (checkpoint teleport, worlds, leaderboards, events) without being shops.

BATCH (f): NPC SHOPS AND STRUCTURES (v5 style, goofy, each one readable from far away)
Only THREE shops for now (each has an NPC):
1. Cosmetics shop (main hub, start plaza): a tailor tent/boutique with mannequins wearing trails and hats, a clothes rack, a mirror and a counter. Spends Squishies.
2. Gamepass shop (main hub, start plaza): one goofy shop that sells all the passes (banana peel, Buddy Carry, skip checkpoint, and future ones). Show the passes as props on display: a banana bunch, a piggyback saddle-backpack, a little "SKIP" hot-air balloon or cannon. It has to look clearly different from the cosmetics shop (different shape and colour), more "premium" (gold trim, Robux-green accents).
3. Halfway cosmetics shop (up the tower, at the checkpoint around the middle of the climb, CP2): a smaller themed cosmetics stall that fits that segment (e.g. a mushroom stall if it's in the mushroom grove), so players can spend Squishies without going back down.

Other structures (no shop, but keep them):
- World portal plaza: a big gate/portal ring for future worlds, with locked/unlocked world pedestals.
- Leaderboard plaza: a trophy podium (1st/2nd/3rd), a big noticeboard frame for a SurfaceGui board, a statue spot.
- Quest/notice board and a daily reward mailbox or gift chest pedestal (future dailies).
- Codes wishing well.
- Town crier podium with a bell for server-wide twist events (low gravity etc.).
- Tutorial sign/hut by the start gate, and a "Bonk Clinic" ragdoll recovery tent (bandages, a goofy stretcher) as a fun spawn-area landmark.
- Friend campfire: a campfire circle with log seats (social spot).
- A small waystone/teleport kiosk at each checkpoint island (themed per segment), for the checkpoint teleport menu.
- Summit: victory podium, confetti cannons, a photo spot frame, a "you made it" arch.
Modular stall kit, so we can add more shops later: stall frames (2–3 sizes), counters, striped awnings in 6 colours, tent roofs, kiosks, hanging shop signs and standing sign boards with a BLANK face for a SurfaceGui icon/text, shelves, jars, crates of goods, display pedestals, price tags, Squishies coin piles, a cash register, a bell.

RULES FOR NPC STRUCTURES
- Scale everything to a Roblox avatar (R15 about 5–6 studs). Counters at waist height, roofs high enough that the camera never clips, and an open front so the NPC is visible from the plaza and on a phone screen.
- Mark the NPC standing spot and a ProximityPrompt anchor point in the manifest for each structure (like the stand points in batch (a)).
- Each one needs a clear silhouette and one strong colour so players can tell the shops apart from a distance (shape language from [[Art-Direction]]).
- Leave the NPC characters themselves for later. Just leave room for them.

BATCH (h): EXTRA AND MISC MODELS (after (g); variants over unique meshes)
Hub, fantasy and secrets:
- Hub/village: a start plaza village layout set (paths, lamp posts, flower boxes, hedges, a market square floor), a spawn pad, segment entry gates (a themed archway welcoming you into each world), height marker signs ("100m!") for the climb, benches and AFK seating spots.
- Fantasy: a sword in a stone, a dragon skeleton, garden gnome statues (goofy), toadstool street lamps, a magic fountain, beehives, a watermill wheel, a crystal mine cart on tracks, hot-air balloons and kites in the sky, floating sky jellyfish and a sky whale (S4 backdrop), totems, a bell tower, wind chimes, fireflies (as glow particles points).
- Secrets: a hidden cave entrance, a secret ledge with a treasure chest, a goofy hidden room for a future secret title.

Misc:
- Gameplay items: a banana peel (the placeable one for the pass), a Squishies pickup/currency blob, a summit crown, trophy cups (gold/silver/bronze), a title plaque, checkpoint flags per segment.
- Goofy stuff: a rubber chicken, a giant rubber band ball, a squeaky toy hammer, a whoopee cushion, a traffic cone wearing a wizard hat, a "wet floor" sign for the ice, an inflatable pool ring, a giant donut float, toy blocks, a goofy scarecrow, a lost sock on a branch, a rubber boot.
- Ground clutter: pebble clusters, rock piles, fallen logs, decor stumps, mushroom rings, clover patches, reeds and cattails, stepping stones, puddles, leaf piles, giant acorns and pinecones.
- Village life: a picnic blanket with a basket, a laundry line, flower pots, a wheelbarrow, garden tools, an apple crate, pumpkin and carrot patches, a birdhouse, a doghouse, a camping tent, a telescope, arrow street signs, a water trough, bunting and string lights, a weather vane.
- Magic clutter: a crystal ball on a stand, an alchemy table, floating candles, a magic mirror, an enchanted broom, levitating teacups, a scroll rack, a wand rack, star and moon lanterns.
- Per-segment extras:
  - S2: giant puffballs, spore clusters, a giant snail;
  - S3: a goofy snowman, a fish frozen in an ice block, penguins, ice sculptures;
  - S4: cloud sheep, star decorations, a golden harp, a sundial, a winged statue.
- Seasonal swap set for future events: pumpkins and jack-o'-lanterns, wrapped presents, a snowy version of the hub decor.

BATCH (g): CRAZY HATS COLLECTION (cosmetics bought with Squishies)
A whole collection of goofy hats that players wear on their own avatar and buy in the cosmetics shops. 
- Aim for about 30–40 hats across rarity tiers, using the vault rarity colours ([[Art-Direction]]: Common grey, Uncommon green, Rare blue, Epic purple, Legendary gold, Mythic red/pink). Higher rarities get more detail, glow pieces and a wobbly/bouncy bit.
- Ideas (go wild, add more):
  - Goofy: a rubber chicken hat, a plunger, a traffic cone, a banana peel hat, a toilet-paper-roll top hat, a fish hat, a cake with candles, a beanie with a propeller, a hot dog, a pizza slice, a bucket, a sock puppet, a rubber duck, googly-eye antennae.
  - Fantasy/magic: a wizard hat with stars, a floating crystal halo, a mini cloud with rain, a dragon head hood, a mushroom cap hat, a snowman head, a tiny castle, a glowing rune crown, a witch hat with a little cauldron, a jelly slime sitting on your head.
  - Show-off (Legendary/Mythic): a giant gold crown, a flaming/glowing crown, a rainbow arch hat, a tiny orbiting planet, a mini wobbly tower ("Rubber Tower" on your head), a summit-only crown.
  - Themed per segment: a few hats sold ONLY in the halfway shop, themed to that segment, so it's worth stopping there.
- Make them for wobble: build the parts that should jiggle (antennae, propellers, flopping chicken, slime) as separate pieces with pivots in the manifest, so code can make them bounce when you ragdoll.
- Roblox setup: each hat is an Accessory (Handle MeshPart + HatAttachment), oversized and readable, low tris (about 500–2k), sharing atlases. Test the fit on R6 and R15 and a few different heads and hairstyles so nothing floats or clips badly. It also has to stay on during the ragdoll.
- For the shop and UI: render every hat with the same icon camera and lighting (one rig, as in [[Art-Direction]]), plus a version on an avatar-sized dummy head. Add a hat display set for the shops: hat stands, mannequin heads, a hat rack, glass display cases for the rare ones.
- List every hat in the checklist with its rarity and segment. Squishies prices come later (I'll decide).

PROCESS
- Same as before: v5 style locked ([[Rubber-Tower-Art-Style-Guide]]), references next to every model, colour/size variants over unique meshes, preflight PASS, phone-friendly.
- For batch (f), also render a hub diorama: the start plaza with the two hub shops and the other structures placed around it and avatar-sized dummies standing at each NPC spot, from the player's camera height.
- Stop for my review after (f), after (g) and after (h). Render a diorama per batch, like before. Don't upload or build the map yet. Log this in [[Rubber-Tower]] and [[Rubber-Tower-Valley-Kit]].
```
