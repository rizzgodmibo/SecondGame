---
tags: [project/rubber-tower, feedback/map]
status: draft
updated: 2026-10-04
---
# Rubber Tower: map v2 critique → v3 prompt

Holden's critique of valley v2 (screenshot 2026-10-04). Paste the prompt below into Claude Code.

```
Map v2 critique: it's still not what I asked for. It still feels like being in a box. Actually a cage now. Read [[Art Direction Feedback]], [[Art-Direction]], [[Lighting-And-Atmosphere]], the "Chained-together obbies" section of [[Rubber-Tower-Reference-Obbies]] and [[Rubber-Tower-Valley-Kit]] before you change anything.

WHAT'S WRONG
1. Cage, not valley. Pillars every few studs plus full-height flat walls block the view in every direction. I can't see a sky, a horizon or anything outside.
2. It's all parts. Nothing from the Blender Valley Kit is in. Everything is plain cylinders and blocks, which I've already rejected ("low quality, outdated").
3. One colour. Walls, floor, platforms and lighting are all lavender/white. That's the "flat single-colour, stale" look I rejected. Nothing pops and you can't tell what's walkable.
4. No route. From the start I can't see where to go. The path is scattered tiny discs and white stools with huge empty space around them.
5. No goal. There's no summit landmark visible from the ground and the checkpoints don't look like checkpoints.
6. Random pieces: a see-through slab/band across the top of the walls, a cyan glass block, and pink/yellow rectangles on the big white disc. Remove them or tell me what they are.
7. No themes. Meadow / mushroom / crystal-ice / cloud should look totally different. Right now every height looks the same.
8. The floor's empty. Where are the meadow, pond, trees and boulders?

WHAT I WANT (v3)
- Walls are a backdrop, not a cage. Keep the square border but remove the pillar grid. Use the Rampart_Wall kit with colour variation (stone tints, moss, vines), corner towers, uneven heights, and faceted rock cliffs + waterfalls at the base. Add a few big arches/gaps so you can see OUT: distant mountains, floating islands, clouds. It should feel like a world that continues past the walls.
- Upload the Valley Kit (you have my OK) and swap every placeholder islet, mushroom, cloud, crystal and wall for the real meshes. Make more kit pieces if anything is still a primitive (themed platforms: mushroom caps, crystal shards, cloud puffs, mossy stone ledges).
- Each segment gets its own colour band so you can tell your height at a glance: S1 meadow (warm greens, flowers), S2 mushroom grove (red/pink caps, deeper greens), S3 crystal-ice (cyan/blue, glowing crystals), S4 cloud kingdom (white/gold, sunlit). Background stays lower-saturation, and walkable surfaces are the brightest, most saturated thing on screen.
- A readable route. From any checkpoint I should be able to see the next one. Lead the eye with the path, crystals and light.
- Checkpoints are landmarks: big islands with an obvious beacon (light beam/banner/arch) visible from below.
- A summit landmark (castle/giant crystal/light beam) visible from the ground floor, so the goal is always overhead.
- Ground floor: crisp-zone meadow, the pond, 3+ tree species with varied size and tint, chunky boulders, flowers, and a start plaza with a gate.
- Lighting from the vault obby preset: brighter blue sky, Atmosphere ~0.2 sky-blue (not lavender), Saturation ~+0.2, a sun angle that gives readable shadows. Don't wash it out.

PROCESS
- Only redo the ground floor + segment 1 first, fully dressed, then stop for my review. Don't do all 4 segments.
- Fix your Studio screenshots (they were blank last time; you never actually saw this map). Before showing me anything, take screenshots from these 4 angles: player-eye at spawn, standing on checkpoint 1 looking up, outside overview from above a corner, and a 150px shrunk version. Critique your own work honestly against [[Art Direction Feedback]] and fix the weak points first.
- Keep the map audit passing (every segment reachable, default movement).
- Show me the before/after next to each other.
- Log this critique in [[Rubber-Tower]] and [[Rubber-Tower-Build-Status]].
```
