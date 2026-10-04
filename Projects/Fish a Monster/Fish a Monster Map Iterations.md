---
title: Fish a Monster Map Iterations
date: 2026-10-02
tags: [roblox, map, art, critique]
project: Fish a Monster
---
# Fish a Monster Map Iterations

How the map changed and what Holden said each time. The lessons are in [[Art Direction Feedback]].

1. **v1, realistic terrain island** (misty dusk, terrain water). Holden: not this realistic style; wants cartoony and fleshed out.
2. **v2, retro part-built island** (brick tiers, block trees, noob NPCs Finn, Rodney and Old Salt). Holden: "decent but not good."
3. **v2 mood pass and reshape** (twilight, organic coastline, cobblestone plaza). Holden rejected the models as low quality and outdated.
4. **Roblox AI mesh generator test tree.** Holden: don't use it; use free tools via Blender instead. This led to the [[Blender to Roblox Asset Pipeline]] and Quaternius CC0 trees.
5. **v3, big island from Holden's sketch** ([[Fish a Monster Island v3 Design]]). Critique: models were "one dimensional", one colour, trees repetitive.
6. **v3 detail pass** (4 shades per colour, 11 tree species, ground scatter). In Studio: "very geometric", docks didn't reach the beach, lake hovered, no real water physics.
7. **v4 rebuild** (smooth ground, Terrain water, new ponds and tarn, reference-style boulders and layered trees). The rocks and trees were approved, but the blurred, noisy ground baking looked "like a smudged mess."
8. **v4 ground redo:** flat, crisp zone colours with clean borders, faceted rock cliffs. This was the last pass before the project was parked.

## Pictures by stage
More in [[Fish a Monster Image Gallery]].

| Stage                           | Image                                         |
| ------------------------------- | --------------------------------------------- |
| 5. v3 first layout              | ![[Render v3 Layout SE.png\|300]]             |
| 5. v3 second pass               | ![[Render v3 Pass2 SE.png\|300]]              |
| 6. v3 detail pass               | ![[Render v3 Detail Forest1.png\|300]]        |
| 7. v4 smudged ground (rejected) | ![[Render v4 Smudged Oblique.png\|300]]       |
| 8. v4 crisp zones               | ![[Render v4 Crisp Zones Oblique 2.png\|300]] |

The reference Holden used to explain what "smooth" meant:

![[Ref Crisp Ground and Rock Cliffs.png|450]]

## Technical lessons
- Terrain heights snap to 4-stud voxels, and terrain collision lags right after a write, so re-measure after a short wait.
- ProximityPrompts only show when they're on screen.
- Anything over water needs `CanQuery = false`, or casts hit it instead of the water.
- Big merged meshes get collision that bridges over rivers. Small invisible collision tiles fixed that.
- Terrain water can't carry area labels, so per-area catches need region volumes.
- Performance flags: palms at about 3.4k triangles each, and see-through leaves.

Related: [[Fish a Monster]], [[Roblox Studio MCP Quirks]]
