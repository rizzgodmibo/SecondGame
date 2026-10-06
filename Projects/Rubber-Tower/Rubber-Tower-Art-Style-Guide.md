---
tags: [project/rubber-tower, visuals/art-direction]
status: reviewed
updated: 2026-10-04
confidence: high
---
# Rubber Tower Art Style Guide (v5: LOCKED)

**Approved by Holden (2026-10-04):** "we can work with this style. Lock it in." Every new model must match the v5 wall, islet, beacon and crystal (`AssetLibrary/models/rubber-tower-kit-v5/`; Studio screenshots are in [[Rubber-Tower-Valley-Kit]]). Holden's standing rules: [[Art Direction Feedback]]. Kit list and status: [[Rubber-Tower-Valley-Kit]].

## TL;DR
- **USER override (2026-10-05, after map build 1):** "I don't like the black lines/cracks on every rock. It looks repetitive and fake." **No black crack lines on rock**: use soft darker-tone crevices (a darker shade of the rock, not near-black), colour variation between masses, and light edge highlights. Cliff walls need 5–6 different pieces + colour variants, randomly rotated/scaled, broken up with ledges, vines, trees, crystals, caves, arches and waterfalls ([[Rubber-Tower-Map-Build-Plan]]).
- **The look:**
  - chunky faceted rock with ~~dark cracks~~ **soft darker crevices** and light edge highlights;
  - **bright grass caps with tufts and blades hanging over the edges**, and a darker band where grass meets rock;
  - **crisp painted zones**;
  - little pebbles, flowers and props for detail;
  - a **goofy, slightly crooked** feel.
- **Surfaces are hand-painted, never plain:** each mesh gets a baked painted texture (cracks, strata, AO in creases, edge highlights, darker bottoms and lighter tops). All patterns have hard edges; Holden rejects blurry noise.
- **Every obby mechanic has its own instantly readable look and colour** (see the mechanic colour language below), so players know what a platform does before they touch it.
- **The world goes UP:** ledges, terraces and stacked islands. Checkpoints are visible from below.
- **Judge in Roblox lighting where possible.** In Studio, every textured MeshPart gets a `SurfaceAppearance` (ColorMap = its texture); without one, the default material looks like glossy plastic.

## References (what each is for)
| Reference | Use |
|---|---|
| **v5 kit** (`AssetLibrary/models/rubber-tower-kit-v5/`) | **The bar.** Match its texture density, crack style, grass fringe and colours |
| `Assets/Reference-Captures/Holden-Picks/` | Holden's own picks: **these outrank everything** (empty on 2026-10-04) |
| OmniKoi2 img-1..4 (`Assets/Reference-Captures/X/lowpoly/OmniKoi2-1915887634809033098/`) | Warm tan rock, lime caps, puffy canopies, candy palette (img-3) |
| haooffiso Sky_Island (`…/haooffiso-2003000840785944688/img-1`) | Magic level: white and gold stone, domes with glowing windows, portals, airships (S4) |
| Fish a Monster `Ref Mossy Rocks and Curved Trees.png` | In-game faceted rock with painted texture, grass blades, avatar scale |
| Orca_Environ (`…/Orca_Environ-*`) | Lollipop trees, pastels, lagoon |
| M0TOPRINCESS (`…/M0TOPRINCESS-1969917863705326000`) | One mesh in several colour variants |
| Roblox games (`Assets/Reference-Captures/Roblox-Games/`, [[Roblox-Obby-Surface-References]]) | Parkour Spiral and Tower of Sky for the climb layout; Fisch for painted surfaces |
| `Assets/VFX/TexturePack/` | Studio decals and particles: spell circles, flares, cloud puffs |

## Palette (hex, from `kitlib5.py`)
| Material | Light | Mid | Dark | Accents |
|---|---|---|---|---|
| Warm rock (S1) | `#F4C287` | `#D48C52` | `#93573A` | crack `#5C3020`, highlight `#FFE6B8`, strata `#A05C36` |
| Grass | `#A2E85E` | `#79CF47` | stipple `#4FA83A` | clover `#C4F57A`, drape `#4FAE3E`/`#2E7F34` |
| Dirt (islet undersides) | `#C98856` | `#9C6038` | `#6A3E26` | pebble `#E2B184` |
| Wood | `#D9995A` | `#B0703F` | `#74462A` | nails `#55576A`, rope `#F0D394`/`#B48C52` |
| White/lavender stone | `#F6F2FF` | `#DAD3F3` | `#A69CD6` | mortar `#8A80BA`, moss `#74C44C` |
| Gold | `#FFE47A` | `#F2B632` | `#B87A18` | `#FFF8D2` |
| Crystal cyan / pink | `#C8FAFF`/`#FFD2F6` | `#62E4FF`/`#FF78E4` | `#1E9AD8`/`#B83AAE` | white edges |
| Glow (Neon) | cyan `#6FF0FF`, magenta `#FF6AE8`, gold `#FFE070` | | | |

### Mechanic colour language (USER-approved 2026-10-04: "keep the colors")
| Mechanic | Colour and shape cue |
|---|---|
| Bounce (`BouncePad`) | **Hot pink and magenta**, squashy domes, white spots or stars, springs |
| Ice (`IcePlatform`) | **Pale cyan and white**, frost cracks, snow lumps, icicles under the edges |
| Wobble (`WobblePlatform`) | **Lime and yellow jelly**, wobbly outlines, rounded |
| Soft rest | **Cream, white and pastel**: puffy clouds, pillows, hay |
| Hazards and movers | **Red and orange rubber**: paddles, hammers |
| Checkpoint | White and gold stone + **cyan glow** beacon, themed per segment |

## Shapes and proportions
- Big chunky forms first; then painted detail; then small geometric detail (tufts, pebbles, flowers, nails, rope).
- **Rock:**
  - faceted hulls of 10–20 points with chipped bevels of 0.25–0.4;
  - masses vary ×2 or more in size and stick out by different amounts (no grid);
  - no back slabs or sky gaps.
- **Grass caps:** 0.6–1.0 thick, overhanging 0.5–0.6, with an irregular double-sided blade fringe 0.5–1.8 long.
- **Goofy:** tilt things 2–9°, use crooked blocks, oversized flowers and faces on mushrooms and slimes, squashed caps.
- **Standing tops** of obby platforms are flat and fair (tilt under 2°) and at least 6×6 for a normal jump target.
- **Wobble platforms** are about 12×12, a single MeshPart, with 4+ studs clear underneath for the springs.

## Technical (phone-friendly)
| Asset type | Triangles (target / max) | Texture |
|---|---|---|
| Small decor and props | 150 / 600 | shared batch atlas |
| Platforms | 400 / 1,500 | shared or own 1024² |
| Trees, mushrooms, mechanic pieces | 600 / 2,000 | shared or own |
| Landmarks and buildings | 1,500 / 5,000 | own 1024² |
| Climb and wall sections | 3,000 / 9,000 (split into parts of 1,024² each) | own |

- **Bake:** `kitlib5.py` paint recipes are emission-baked in Cycles to 1024² PNGs.
  - Small models share an atlas (UVs packed together) for at least about 12 px per stud.
  - Colour variants re-bake the same UVs with another palette: one mesh, several textures (the M0TOPRINCESS idea).
- **Glow parts** are separate `*_Glow` MeshParts (Neon, no shadow, no collision). Wobble platforms have none.
- **Colliders:** platforms get simple invisible box colliders that carry the tag. A wobble platform is its own tagged MeshPart (Box fidelity).
- **Preflight PASS** ([[Roblox Asset Pipeline Skill]]). The known intentional WARNs are double-sided blade twins and single-colour glow parts.

## Checklist per model
- [ ] Matches the v5 bar: painted cracks and edges, grass fringe where there's rock, crisp zones, a goofy touch
- [ ] 1–3 references, shown next to it on the sheet
- [ ] Mechanic pieces: readable colour cue, flat standing top, tag and collider plan
- [ ] Within the tri budget; preflight PASS; glow split out
- [ ] An avatar-sized dummy (5.3 studs) in the shot for scale

## Pitfalls
- Workbench and flat-cyan renders make everything look plastic. Use a sky gradient, a sun, a ground and a dummy.
- Heavy crack contrast up close reads like marker lines. ~~Keep the cracks~~ (USER 2026-10-05: no black crack lines at all; soft darker crevices only), and give big faces enough texture density (split big meshes).
- One rock model stacked into a wall reads as fake (USER 2026-10-05). Mix 5–6 shapes, rotations, scales and tints.

## Related
[[Rubber-Tower]] · [[Rubber-Tower-Valley-Kit]] · [[Obby-Special-Platforms]] · [[Roblox-Obby-Surface-References]] · [[X-Low-Poly-Builds-And-Maps]] · [[Art-Direction]]
