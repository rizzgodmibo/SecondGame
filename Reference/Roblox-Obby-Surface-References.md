---
tags: [reference/games, visuals/art-direction, project/rubber-tower]
status: draft
updated: 2026-10-04
confidence: medium
---
# Roblox obby and climb games: what makes surfaces look "real Roblox"

Study for Rubber Tower kit v5, after Holden said v4 looked like "cheap plastic". The images are listed in `Assets/Reference-Captures/Roblox-Games/MANIFEST.md`, and the inspection was stills only.

**Evidence types used on this page:**
- **Observation (obs):** what the screenshots show.
- **Principle:** my inference from the observations.
- **Proposal:** not approved.

## TL;DR
- **The top ragdoll and troll towers are not fantasy at all.**
  - Obs: Troll Ragdoll Tower, TROLL Hug Tower, Tower of Hell, Chained and Ragdoll Physics Tower are saturated single-colour parts inside a square tower.
  - Obs: every surface carries Roblox's crisp **stud or tile pattern**.
  - Principle: their "real Roblox" feel comes from that small repeating surface pattern plus strong colour and lighting, not from sculpted detail.
- **For stylised terrain the best in-game refs are Fisch and Fish a Monster's "Mossy Rocks".**
  - Obs: faceted rock with a faint painted texture, wood with plank and grain texture, dense grass-blade geometry, water with crisp caustics, bloom and soft shadows.
- **For the climb itself the refs are Parkour Spiral and Tower of Sky.**
  - Obs: themed bands of ledges spiral around one central mass, and the whole climb reads from below and from outside.
  - Principle: put the obby on the outside of the mass, stack it visibly, and show the goal overhead.
- **An avatar in the shot sells the scale and the "this is a game" feel.**
  - Obs: almost every thumbnail has one; the Mossy Rocks ref has Holden's own.
- **Thumbnails are not the game.**
  - Obs: many of these images are posed and edited, with text, glow, depth of field and dramatic angles.
  - Principle: judge our art in Studio, not against marketing renders.

## Per game
| Game | Surfaces (obs) | Take for Rubber Tower |
|---|---|---|
| Troll Ragdoll Tower (6 imgs) | Neon-pastel parts with stud texture and studded walls; segments colour-coded (pink, cyan, red). Enclosed tower | Colour per segment works. Its texture density is what we lack. Not its enclosed look |
| TROLL Hug Tower (5) | Edited thumbnails: blue studded platforms over lava, big avatars, UI prompts | The avatar is the hero in thumbnails |
| Squishy Troll Tower (3) | Pastel pink and blue studded floors, a cloud-like sky, a slime toy | Soft pastel plus a squishy material is a hook |
| Ragdoll Physics Tower (3) | Studded walls, a pile of ragdolled noobs: goofy | The goofy ragdoll pile is a strong image |
| Chained / Chained Together (1 each) | Grey studded climbing wall with a red/blue frame; a lava-hell art render | A climbing wall with handholds reads instantly as "up" |
| Tower of Hell (3) | Clean grey interiors, glowing exit | Simple and readable, not our style |
| Parkour Spiral (3) | A **spiral ledge path around a mountain or tower**, each band a different theme, an island at the base, a blue sky | **Closest structure to our brief.** The climb reads from far away |
| Tower Of Sky (5) | White and pale-blue studded platforms and clouds in a sky tower | Our S4 cloud-kingdom palette, but plain |
| ONLY UP / New Only Up / Glide Tower (7) | Floating everyday objects in haze (Only Up); a voxel-like city (Glide Tower) | The haze and depth make height feel huge |
| Fisch (9) | Thumbnails, but the in-game assets show **faceted rocks with painted texture, plank wood, sand with hard-edged facets**, bloom and colour grading | **Surface reference for v5:** painted texture on chunky shapes |

## Principles applied in kit v5 (proposals until Holden approves)
- **Paint every surface:** crisp cracks and strata on rock, grass stipple and clover, wood grain and nails, bricks with moss in the corners. Use hard edges, never blurry noise.
- **Bake AO into creases and a light rim on exposed edges.** In Roblox lighting this gives the depth the flat colours lacked.
- **Build for the climb:** ledges every ~5 studs that read from the ground, and the checkpoint goal visible on top.
- **Judge in Studio** with Holden's avatar and the obby lighting, not in Blender on a flat background.

## Pitfalls
- Don't copy the stud texture wholesale. Holden wants fantasy and goofy, not a parts tower.
- Don't treat a thumbnail as in-game quality. Many are posed renders.

## Related
[[Rubber-Tower-Reference-Obbies]] · [[Rubber-Tower-Valley-Kit]] · [[Rubber-Tower-Art-Style-Guide]] · [[Reference-Capture-Process]] · [[Art Direction Feedback]]

## Sources
- Roblox game pages and thumbnail API, captured 2026-10-04 (place and universe ids are in the manifest), e.g. https://www.roblox.com/games/139788637490504 (Troll Ragdoll Tower), https://www.roblox.com/games/16732694052 (Fisch), https://www.roblox.com/games/18152595062 (Chained Together).
- Fish a Monster in-game screenshot `Projects/Fish a Monster/attachments/Ref Mossy Rocks and Curved Trees.png` (Holden's own game).
