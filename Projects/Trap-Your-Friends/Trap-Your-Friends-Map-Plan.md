---
tags: [project/trap-your-friends, design/maps]
status: draft
updated: 2026-10-06
confidence: low
---
# Trap Your Friends: Map Plan (Maps 2 and 3, PLAN ONLY)

## TL;DR
- (USER, 2026-10-06) 3 maps, voted each round. **All 3 must be bigger than the v2 slice.** A full server is **16 = up to 4 Trappers + 12 Runners**, with **4 fixed Trapper zones per map** (merge when fewer Trappers).
- Map 1 = **Castle Sky Island**: full layout in [[Trap-Your-Friends-Map1-Layout]] (DRAFT, not built).
- This note proposes Maps 2 and 3: **3 options each + a recommendation**. Holden picks the themes later. Nothing here is approved or built.
- **Recommendation: Map 2 = Candy Factory, Map 3 = Giant's Toy Room** (outdoor sky, indoor industrial, giant-scale indoor: three different looks, palettes and route shapes).
- **Size per map (DRAFT, same targets as Map 1):** ~1,000 studs of route centreline (800–1,200), 2:30–3:00 for an average runner incl. deaths, folded into ~400×400 studs, **4 zones × 11 sockets = 44**, 5–6 checkpoints (about every 30 s).

## Shared map rules (DRAFT)
- **Structure:** start room → 4 Trapper zones in a row along the route → finish with a glowing goal visible early. Each zone ≈ 250 studs of route ≈ 40 s, ends at a checkpoint.
- **Routes:** main paths 20–32 studs wide (never under 12); **2–3 alternative routes per zone**: a long, safe main route and a short, risky branch (narrow, gaps, more sockets per stud). Every branch rejoins before the zone's checkpoint.
- **Sockets per zone (11):** 4 floor 2×2, 3 floor 4×4, 2 wall, 1 ceiling gantry, 1 lane-wide. Every route in a zone gets sockets, so no route is trap-free.
- **Jumps:** all gaps within measured reach (WalkSpeed 16, JumpHeight 7.2, running reach ~7.4 studs): ≤ 6 studs flat, ≤ 4.5 studs up. Landings tagged `MapMustReach`, Trapper areas tagged `MapNoReach`; audited with the map-audit skill.
- **Trapper lookouts:** one balcony per zone, out of Runner reach, with the zone's colour and banner ([[Trap-Your-Friends-Map1-Layout]]).
- A route must always exist: no socket combination fully blocks the way (lane-wide sockets are always jumpable or timed; Brick Walls are Bash-able).
- Retro stud style with a themed environment, 3-tone floors (DRAFT ±5–8% exception), black outlines on traps. Each map gets its own sky mood ([[Trap-Your-Friends-Sky-v3-Plan]]).
- Indoor maps (2 and 3) still need a sky: windows, a skylight or an open roof, so the sky mood shows.

## Map 1: Castle Sky Island (USER: Map 1)
- See [[Trap-Your-Friends-Map1-Layout]]: Barbican start → Zone 1 Moat & Outer Bailey → Zone 2 Courtyard Market → Zone 3 Keep Loop → Zone 4 Mage Tower & Sky Bridge → keep-roof beacon. ~1,100 studs, 44 sockets, 5 checkpoints.

## Map 2 options
| Option | Look | Route sketch (4 zones) | Why / risk |
|---|---|---|---|
| **A. Candy Factory** (recommended) | Pink, mint, cream and chocolate studded bricks; conveyor belts, gumdrop piles, candy-cane pipes, a giant mixer | Loading-dock start → **Z1 Conveyor Hall** (belts vs a catwalk shortcut over them) → **Z2 Mixing Vats** (bridge over vats vs pipe crawl) → **Z3 Packing Line** (switchback catwalks on 2 floors) → **Z4 Silo Climb** (spiral around the candy silo vs elevator shaft) → silo-top finish with a glowing lollipop beacon | Brightest palette, totally different from the Castle; theme skins write themselves (gumdrop bounce, chocolate glue, jawbreaker wrecking ball). Risk: busy colours, so outlines matter; conveyors are new tech |
| B. Pirate Cove | Sand, wood docks, a ship deck, blue water, palm trees | Beach start → Z1 dock maze → Z2 ship deck (cannons) → Z3 rope bridges between sea stacks → Z4 lighthouse spiral → lighthouse finish | Sunny and outdoor like the Castle (less contrast); water edges are natural fall hazards |
| C. Spooky Mansion | Purple, dark wood, green ghost light | Foyer start → Z1 long hallway → Z2 library (bookshelf shortcut) → Z3 grand staircase → Z4 attic and roof → weather-vane finish | Kids love spooky, but darkness is bad on phones; needs bright stylised moonlight |
- Map 2 A footprint (DRAFT): a 3-floor factory ~360×360 studs, with zones 1–2 on the ground floor and zones 3–4 climbing.

## Map 3 options
| Option | Look | Route sketch (4 zones) | Why / risk |
|---|---|---|---|
| **A. Giant's Toy Room** (recommended) | Runners are tiny in a kid's bedroom: floor, desk and bookshelf are giant studded toy bricks; crayons, blocks, a toy train | Toy-box start → **Z1 Rug Plains** (open, wide; train track vs block maze) → **Z2 Bookshelf Climb** (vertical; ladder of books vs shelf ledges) → **Z3 Desk Top** (past the lamp; pencil bridge vs ruler shortcut) → **Z4 Windowsill & Toy Rocket** (along the sill, up the rocket) → rocket-nose finish | Leans hardest into "classic studded bricks are toys"; great destruction (block towers to topple); a vertical section the other maps lack. Risk: scale must read (big props, small runners) |
| B. Space Station | White and orange panels, neon, stars | Airlock start → Z1 hangar → Z2 low-gravity zone → Z3 reactor ring → Z4 escape-pod bay → pod finish | Distinct, but neon and dark space fight the bright retro look; low gravity changes movement balance |
| C. Volcano Forge (Lava Factory) | Black rock, orange lava, iron | Mine-cart start → Z1 lava river bridges → Z2 forge hall → Z3 magma elevator → Z4 crater rim → crater finish | In the old GDD theme list; strong hazard read, but red/orange clashes with the trap danger colours |
- Map 3 A footprint (DRAFT): one giant room ~400×300 studs, ~150 studs tall (the vertical climb makes up the length).

## Socket counts (DRAFT, every map)
| Type | Per zone | Per map (4 zones) |
|---|---|---|
| Floor 2×2 | 4 | 16 |
| Floor 4×4 | 3 | 12 |
| Wall | 2 | 8 |
| Ceiling gantry | 1 | 4 |
| Lane-wide | 1 | 4 |
| **Total** | **11** | **44** |
- With fewer Trappers zones merge (Round Structure), so 1 Trapper owns more sockets than they can fill with the trap budget. That's fine: empty sockets are just floor. ⚠️ verify by playtest: the per-Trapper budget (GDD DRAFT ~30) may need to scale with zones owned.

## Recommendation (Claude's, for Holden to decide)
- **Map 2 = Candy Factory, Map 3 = Giant's Toy Room.** Three different silhouettes and palettes on the vote screen (grey-green castle, pink-mint factory, bright toy primaries) and three different route shapes (outdoor loop around a keep, multi-floor factory, a vertical climb). Trap reskins per theme stay cheap (same trap module, new mesh).
- Build order after Map 1 is locked: Toy Room (closest to the stud style, reuses most of the Castle's brick kit) before Candy Factory (needs conveyor tech).

## Open questions
1. Map 2 and Map 3 themes (above). Holden picks later.
2. Branching shortcuts: open to everyone (current plan), or opened by Trappers?
3. Should the trap budget scale with the number of zones a Trapper owns?

## Related
[[Trap-Your-Friends]] · [[Trap-Your-Friends-Map1-Layout]] · [[Trap-Your-Friends-v3-Plan]] · [[Trap-Your-Friends-Round-Structure]] · [[Trap-Your-Friends-GDD]] · [[Trap-Your-Friends-Trap-Catalogue]] · [[Trap-Your-Friends-Sky-v3-Plan]] · [[Trap-Your-Friends-Style-Test-v2-Plan]]

## Sources
- Holden's decisions 2026-10-06 ([[Trap-Your-Friends-Round-Structure]], hub). Route lengths are estimates from WalkSpeed 16 (DRAFT, untested).
