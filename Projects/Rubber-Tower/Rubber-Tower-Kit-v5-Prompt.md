---
tags: [project/rubber-tower, feedback/art]
status: draft
updated: 2026-10-04
---
# Rubber Tower: kit v4 critique → v5 prompt (detailed, climbable, "real Roblox")

This is Holden's critique of the v4 style test ([[Rubber-Tower-Valley-Kit]]), pasted in chat on 2026-10-04, together with "first of all save these models in case I want to use them later". The v4 models are archived in `AssetLibrary/models/rubber-tower-kit-v4/`.

```
v4 style test feedback: some models are fine, but I don't like the style of most of it. I want it to look like an actual ROBLOX game: high quality, in that Roblox/goofy style. Two big problems:

1. IT'S AN OBBY. The terrain has to go UP.
The diorama is a flat canyon floor with a path through it, like an adventure map. Rubber Tower is a climb. The walls, cliffs and platforms should be built for going up: ledges, terraces, platforms spiralling up the valley, checkpoint islands stacked above each other, the summit visible overhead. The ground floor is just the start.

2. EVERYTHING IS TOO SMOOTH. It looks like cheap plastic.
Especially the terrain. Big flat single-colour faces, no surface detail, rendered on a flat cyan background: it looks like a toy, not a real game. I want high quality, not plain.

WHAT "HIGH QUALITY ROBLOX / GOOFY" MEANS
- Surface detail on everything, in a crisp stylised way (NOT blurry noise, which I've rejected before):
  - rock: chunky cracks, chipped bevelled edges, strata lines, pebbles and small rocks at the base, light edge highlights;
  - grass: grass tufts and blades spilling over edges, flowers, clover patches, a darker band where grass meets rock;
  - wood: planks, grain lines, nails, rope bindings;
  - stone/buildings: individual bricks, trims, cracked tiles, moss in the corners.
- Hand-painted style textures: paint the detail into the atlas (edge highlights, baked ambient occlusion in the creases, darker bottoms and lighter tops). Shapes stay chunky but surfaces aren't flat.
- Goofy: things slightly crooked, wobbly and exaggerated. Leaning towers, bent pillars, squashed mushroom caps, bouncy rounded shapes, oversized props, silly details (a mushroom with a face, a cracked signpost). It fits the wobbly ragdoll theme.
- Look at real top Roblox games, not just low-poly art. Go through [[Rubber-Tower-Reference-Obbies]] (Troll Ragdoll Tower, Squishy Troll Tower, Chained Together and the others), capture in-game screenshots and thumbnails into Assets/Reference-Captures per [[Reference-Capture-Process]], and note what makes their surfaces look good. Also reuse the in-game vault refs: Ref Mossy Rocks and Curved Trees.png (textured faceted rock + grass tufts, with an avatar for scale) and haooffiso's Sky_Island (textured stone, glowing windows). I'll also drop my own screenshots in Assets/Reference-Captures/Holden-Picks/. Those beat everything else if they're there.

KEEP / CHANGE
- Keep: the crystals, the islet, the checkpoint beacon and the portal. Upgrade their surfaces and fix the weak points you listed (puffy canopy on the islet bush, a real spiral on the portal, thicker obelisk with chunky chains and bigger rune stones).
- Redo: the cliffs and terrain. Build them as a climbable vertical obby wall with detailed rock, not flat stacked slabs.
- Still in Blender by script, still low-poly enough for phones, still made by us (no AI meshes, no downloads).

PROCESS
1. Judge it IN ROBLOX, not Blender. Upload the test pieces to a private test place only (you have my OK for these test uploads), put them in Studio with the obby lighting, a skybox and my Roblox avatar standing next to them for scale. Screenshot them there. Blender renders on cyan make everything look like plastic.
2. Style test first: one detailed cliff/obby wall section going up about 60 studs (with ledges and a checkpoint island on top), plus the upgraded islet, crystal and beacon. Show me: v4 | v5 in Studio | the closest real Roblox game reference. Wait for my OK.
3. Add one more test shot: standing at the bottom looking up the climb, so I can see the obby going up.
4. Self-critique honestly against the references first. Specifically check: "does this look like a real Roblox game or a plastic toy?" and "can you see the climb?"
5. Keep the art pipeline checks (preflight PASS, sensible tris and texture size for mobile). Log this critique in [[Rubber-Tower]] and [[Rubber-Tower-Valley-Kit]].
```

## Related
[[Rubber-Tower]] · [[Rubber-Tower-Kit-v4-Style-Prompt]] · [[Rubber-Tower-Valley-Kit]] · [[Roblox-Obby-Surface-References]]
