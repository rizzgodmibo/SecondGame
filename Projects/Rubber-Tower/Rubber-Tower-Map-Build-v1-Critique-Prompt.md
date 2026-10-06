---
tags: [project/rubber-tower, design/level, feedback/map]
status: final
updated: 2026-10-05
---
# Rubber Tower: first Option B build critique (prompt)

Holden's critique of the first Option B build (3 screenshots, 2026-10-05). Paste the block into Claude Code.

```
First build feedback: there's progress, but it isn't an obby yet, and parts of it look lazy. Your self-critique should have caught most of this. Read [[Difficulty-And-Mastery]], [[Obby-Special-Platforms]], [[Rubber-Tower-Ideas-Bank]] (section A, wobble and bounce areas), [[Art Direction Feedback]] and [[Rubber-Tower-Art-Style-Guide]] again before fixing.

WHAT'S WRONG
1. The bottom part isn't an obby. Lily Lake etc. lets you just walk around freely: the lily pads and raft sit on a shallow pond next to the grass, so there's no challenge and no fail. We made all these special models and effects, and they're used as decoration.
2. The upper part IS an obby but it's way too easy: about 20 of the same small plank/beam hops in a row, same gap, same size, no timing, no mechanics. I ran through it with no effort.
3. The hub feels like all the models are huddled together around the pond. It doesn't feel like a world with an obby mixed in; it feels like a pile of props.
4. The ground is lazy: one flat green with a sand ring, no height, no paths, no zones, no detail.
5. The cliff walls are the same rock model stacked over and over, and I don't like the black lines/cracks on every rock. It looks repetitive and fake.
6. The waterfall is a flat blue strip with dashes.
7. The floating islets in a row all look identical.

WHAT I WANT
A. Make it a REAL obby built from our special pieces. Chain them into combos, so each section is a little set piece. Examples:
   - jump on a bounce mushroom → fly forward → grab onto a ladder/vine wall;
   - wobbly lily pads over DEEP water (falling in = a splash and a swim back to the section start, not wading);
   - run up a seesaw log as it tips, onto a ledge;
   - an ice slide that launches you onto a bounce pad onto a moving windmill blade;
   - the slingshot to a far floating island;
   - fan vents pushing you sideways across a gap;
   - timing jumps past swinging rubber hammers/paddles;
   - a chain of jelly cubes where each one wobbles more;
   - a soft rest (hay bale, moss cushion, pillow cloud) after each hard combo.
   Every one of the special pieces should be used as gameplay in S1, with ice saved mostly for S3 as planned.
B. Real difficulty. No more 20 identical hops. Vary gap length, height, platform size (shrinking platforms), direction changes, run-up jumps, precise landings on small/wobbly things, and timing. Follow the sawtooth (teach → test → twist → rest) and ramp from easy at the start gate to medium by CP1. Still fair on a phone with default movement. A first-time player should fall a few times in S1 and take 5–8 minutes. Measure it: run it yourself with character navigation, count falls and time it, and tell me honestly if it's still too easy.
C. Make the hub feel like a world:
   - The ground floor is the safe village/hub. The obby starts at a clear START GATE, and the spawn faces that gate and the tower.
   - Lay it out like a real place: a village square with the shops facing it, paths/streets connecting areas, little districts (market, garden, pond, grove), groves of trees instead of single scattered props, fences/hedges/walls framing spaces, breathing room between areas.
   - Add height: hills, raised grass terraces, small cliffs, ramps and steps, a stream from the waterfall to the pond, a bridge over it.
D. Ground: crisp v5-style zones with curved borders: stone paths, dirt trails, flower beds, darker grass patches, grass edges hanging over paths, pebbles. Not one flat colour (I've rejected that before) and not blurry.
E. Walls/cliffs:
   - Make at least 5–6 different cliff/wall pieces (different shapes, heights, overhangs) plus colour variants, and mix them with random rotation and scale so you never see the same rock repeating.
   - Remove the black crack lines; use soft darker-tone crevices and colour variation instead.
   - Break the walls up with grass ledges, vines, trees growing out, crystals, caves, arches and more waterfalls.
F. Waterfall: a real one, with layered see-through sheets, white foam at the top and bottom, mist/splash particles and a splash pool.
G. Floating islets: vary size, shape, tilt, colour, and what's on them (a tree, crystals, a mushroom, a little house).

PROCESS
- Write the new section-by-section combo list into [[Rubber-Tower-Map-Build-Plan]] first (each combo: which pieces, what the challenge is, where you fall to). Keep Option B's route and places.
- Build ONE vertical slice first: the hub layout + ground + start gate + Lily Lake + Village Rooftops, at full quality with the new walls and waterfall. Then stop and show me: spawn view, the start gate, each combo, the walls up close, the ground from player height, your fall count and time. Wait for my OK before the rest.
- Keep the Leap lane, checkpoint tags/heights, colliders and phone-friendliness as before. Log this critique in [[Rubber-Tower]] and [[Rubber-Tower-Map-Build-Plan]].
```
