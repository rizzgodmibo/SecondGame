---
tags: [project/trap-your-friends, design/maps, design/level-design]
status: draft
updated: 2026-10-06
confidence: low
---
# Trap Your Friends: Map 1 full layout, Castle Sky Island (PLAN ONLY)

## TL;DR
- **A plan, not a build. Nothing here is approved.** Targets come from Holden's v3 prompt (2026-10-06): a 2:30–3:00 run, ~800–1,200 studs, 12 Runners + 4 Trappers, 4 zones × 10–12 sockets, a checkpoint about every 30 s, folded into ~400×400 studs, and a glowing goal you can see early.
- **Route:** Barbican Hall start → **Zone 1 Moat & Outer Bailey** (orange) → **Zone 2 Courtyard Market** (blue) → **Zone 3 Keep Loop** (green) → **Zone 4 Mage Tower & Sky Bridge** (purple) → **finish beacon on the keep roof** (y 60), which you can see from the start.
- **Numbers:**
  - all-main run ~1,100 studs, **~2:45 including deaths**;
  - shortest routes ~890 studs, ~2:35 including deaths, ~2:08 for a runner who never dies;
  - **44 sockets** (11 per zone);
  - **4 checkpoints + the finish**, legs 26–41 s apart (one leg over 40 s, flagged below);
  - the route fits in ~330×380 studs.
- **Every zone has a long safe route and a short risky branch.** Main paths are 24–32 studs wide; branches are 12–16, never under 12.
- **Trappers:** each stands on a **lookout balcony above their zone**, out of Runner reach; **HUD buttons** for live triggers (USER); zone colours + banner arches with the Trapper's name (USER).
- **Holden's answers (USER, 2026-10-06):**
  - Runners **see the course but not the traps** during prep;
  - **HUD buttons** for triggers;
  - **Trapper names on the zone banners**;
  - a **3rd Zone 3 route (Dungeon Tunnel) added as DRAFT**;
  - 4 checkpoints + finish is OK if **no leg is over ~40 s**. One leg is over: Market Rooftops, 41 s (see the leg table);
  - run timer 3:30 (DRAFT);
  - the 16-player debris work happens with the greybox (step 4).

![[tyf-map1-layout.png]]
*Top-down plan (`attachments/tyf-map1-layout.png`): zones coloured, main routes drawn at their true width, branches dashed, socket icons by type, checkpoints, Trapper lookouts, start/finish, a 100-stud scale bar. The image comes from data: `TrapYourFriends/design/map1/make_layout.py` → `map1_layout.json` → `render_layout.ps1`.*

## Heights (DRAFT)
- **y 0:** the island meadow (decoration, out of bounds).
- **y 20:** the castle plateau and the main route. Falling to the meadow or the moat (water ~y 10) is a catch, so the v2 "grass below the route counts as a fall" question goes away: the meadow sits below the plateau.
- **Climbs:**
  - Curtain-Wall Ramp: up to y 30;
  - Market Rooftops: y 26–30;
  - Wall-Walk: up to y 34;
  - the tower: y 20 → 60;
  - Sky Bridge and keep roof: y 60;
  - the beacon rises to ~y 85.

## Section table (from `make_layout.py`; speeds are DRAFT averages including traps and deaths)
| Code | Section | Zone | Route | Length (studs) | Width | Height y | Sockets | Expected time |
|---|---|---|---|---|---|---|---|---|
| 1a | Moat Causeway | 1 | main | 40 | 24 | 20 | 1 | 6 s |
| 1b | Bailey Road | 1 | main (long, safe) | 183 | 28 | 20 | 6 | 26 s |
| 1c | Curtain-Wall Ramp | 1 | branch (gaps + Glass) | 134 | 14 | 20→30→20 | 4 | 24 s |
| — | **CP1 West Gate** | | | | | | | |
| 2a | West Gate Climb | 2 | main | 50 | 24 | 20 | 1 | 7 s |
| 2b | Market Street | 2 | main (long, safe) | 182 | 32 | 20 | 5 | 26 s |
| 2c | Market Rooftops | 2 | branch (5–6 stud roof jumps) | 184 | 14 | 26–30 | 5 | 33 s |
| — | **CP2 Fountain Square** | | | | | | | |
| 3a | Fountain Square | 3 | main | 30 | 30 | 20 | 1 | 4 s |
| 3b | Keep Wall-Walk Loop | 3 | main (long, safer) | 220 | 16 | 20→34→20 | 4 | 34 s |
| 3c | Great Hall | 3 | branch (trap-dense) | 169 | 24 | 20 | 3 | 34 s |
| 3d | Dungeon Tunnel (DRAFT, USER 2026-10-06) | 3 | branch (under the keep, dim, Trapdoor drops) | 150 | 14 | 20→8→20 | 3 | 30 s |
| — | **CP3 Keep West Gate** | | | | | | | |
| 4a | Tower Approach | 4 | main | 76 | 24 | 20 | 2 | 11 s |
| 4b | Spiral Ramp (1 turn) | 4 | main (long, safe) | 150 | 18 | 20→60 | 4 | 25 s |
| 4c | Ladder Shaft | 4 | branch (trusses + ledges) | 64 incl. 40 climb | 12 | 20→60 | 1 | 21 s |
| — | **CP4 Mage Tower top** | | | | | | | |
| 4d | Sky Bridge to the Keep Roof | 4 | main | 167 | 16 | 60 | 4 | 26 s |
| — | **Finish: keep-roof beacon** | | | | | | | |

- **Checkpoint legs** (USER, 2026-10-06: 4 checkpoints + finish is OK if no leg is over ~40 s for an average runner). Computed by `make_layout.py`:

  | Leg | Route | Length | Expected time | Check |
  |---|---|---|---|---|
  | Start → CP1 | Bailey Road | 223 | 32 s | ok |
  | Start → CP1 | Curtain-Wall Ramp | 174 | 30 s | ok |
  | CP1 → CP2 | Market Street | 232 | 33 s | ok |
  | CP1 → CP2 | **Market Rooftops** | 234 | **41 s** | **over 40 s: flagged** |
  | CP2 → CP3 | Keep Wall-Walk | 250 | 38 s | borderline |
  | CP2 → CP3 | Great Hall | 199 | 38 s | borderline |
  | CP2 → CP3 | Dungeon Tunnel | 180 | 34 s | ok |
  | CP3 → CP4 | Spiral Ramp | 226 | 36 s | ok |
  | CP3 → CP4 | Ladder Shaft | 140 | 32 s | ok |
  | CP4 → Finish | Sky Bridge | 167 | 26 s | ok |

- **Fix for the Rooftops leg (DRAFT, done in the greybox):** the rooftops are as long as the street, so they aren't a real shortcut. Cut ~15 studs: drop one roof and go straight from the West Gate onto the first roof. Then re-measure with the noob runners. The two 38 s legs in Zone 3 get re-measured too.
- **Routes per zone:** Zones 1, 2 and 4 have 2 (main + branch). **Zone 3 has 3:** Wall-Walk, Great Hall and the **Dungeon Tunnel (DRAFT, USER 2026-10-06)**. The tunnel runs under the keep (floor y 8), is dim with Trapdoor drops, adds ~400 parts and takes 3 of Zone 3's 11 sockets.
- Zone 4 is longer (~62 s over 2 checkpoints) because the tower climb and the bridge belong together.
- **Socket mix per zone (11):** 4 floor 2×2, 3 floor 4×4, 2 wall, 1 ceiling gantry, 1 lane-wide. **Map total:** 16 + 12 + 8 + 4 + 4 = **44**. The script spreads them along both routes of each zone by length. Exact spots get tuned in greybox (e.g. ceiling gantries go where there's an arch or beam).

## Runner start room (Barbican Hall, 52×26 studs, 12 Runners)
- **(USER, 2026-10-06) Runners CAN see the course but NOT the traps** (this replaced the DRAFT "can't see the course"). How:
  - Runners **can** see the course through a big gate grille and window, and the beacon is in view.
  - **Placed traps are not replicated to Runners until the run starts:** the server keeps them in ServerStorage and parents them at "TRAPS ARMED".
  - Trappers see their own placements as client-side ghosts.
  - The surprise stays, and nobody can peek by exploiting.
- **Things to do in the 40 s prep (proposals only, none approved):**
  1. a jump-practice strip with the map's max gaps (6 flat, 4.5 up), which teaches reach;
  2. a "trap tells" gallery: glass cases looping each trap's tell, which teaches the 0.4 s warnings;
  3. a smash corner of soft studded blocks to knock about (client-only debris, nothing saved);
  4. a board showing the map's 4 zones and who owns each.
- Exit: a portcullis that lifts at "GO" onto the causeway.

## Trappers: position, view and controls
- **Lookout balconies T1–T4** sit 35–45 studs above their zone (positions in the image), with railings, out of Runner reach (tagged `MapNoReach`) and no way down into the course.
  - **Prep:** Trappers spawn on their lookout.
  - **Run:** they stay there.
  - Walking into the course stays a "probably not" (Round Structure open question 2).
- **Prep placement:** tap a socket → pick a trap card. The camera orbits/pans inside the zone's bounds; the default view is from the lookout. Works with touch drag on phones.
- **Live triggers: HUD buttons (USER, 2026-10-06).** Why (Claude's reasoning):
  - Phones: walking to and jumping onto world buttons while watching Runners is hard on a touch screen, and slow.
  - The HUD shows only the Trapper's own triggerable traps (≤ 6 buttons in 2 rows). Each button has the trap icon, a zone-colour border, a cooldown ring and a "Runner in range" glow, so new Trappers know when to press.
  - Tapping the trap itself in the world triggers it too.
  - **Deathrun flavour without the mobile cost:** each lookout has a big lever/button prop that animates when its Trapper presses a HUD button (cosmetic only).
- **Zone readability:**
  - **For everyone:**
    - zone colours orange / blue / green / purple (no reds: Really red = Kill Brick, Bright red = TNT, [[Trap-Your-Friends-Art-Style-Guide]]);
    - a **banner arch at each zone entry** showing the zone number and the owning Trapper's name, e.g. "ZONE 2: MiboRBX's Market" (**USER, 2026-10-06: yes**);
    - a zone-colour trim stripe on the floor at the border;
    - zone-colour flags on each lookout.
  - **Trappers only (client-side):** their own sockets tinted in the zone colour, other zones' sockets grey, and a HUD minimap with their zone highlighted.
- **Merging (Round Structure DRAFT order):** 3 Trappers → zones 3 + 4 merge; 2 → 1 + 2 and 3 + 4; 1 → all. A Trapper who owns 2 zones can hop between both lookouts with a HUD "next lookout" button.

## Reach rules (from the measured defaults)
- WalkSpeed 16, JumpHeight 7.2, measured running-jump reach ~7.4 studs.
- **Design limits:**
  - flat gaps ≤ 6 studs (1.4 margin);
  - steps up ≤ 4.5 studs;
  - a gap with a step up of 2+ studs: ≤ 5 studs.
- Ladder Shaft: TrussParts plus ledges ≤ 4.5 apart. Rooftops: gaps 5–6 with 0–2 up.
- **Tags:**
  - every route landing `MapMustReach`;
  - lookouts, tower roof and keep-roof edges outside the path `MapNoReach`;
  - audited with the map-audit skill at the greybox gate.

## Budgets (DRAFT estimates, all ⚠️ verify by measuring in the greybox)
| Item | Estimate | Notes |
|---|---|---|
| Parts | **≤ 12,000** (est. ~10,600) | v2 slice: 935 parts for ~180 studs of route. Floors are big studded plates. Breakable 2×2/4×4 sub-tiles only on socket pads and Brick Wall traps. Est.: route floors ~2,000, walls and buildings ~5,000, props and trees ~2,000, sockets/markers ~400, lookouts ~400, island underside ~800 |
| Triangles in view | ~400k worst case (target < 1M) | Parts ~12 tris each (~130k if all were in view). Placed hero traps ≤ ~32 × 3–10k ≈ ≤ 200k. Cloud meshes ~70 × ~600 ≈ 42k |
| Draw calls | 300–700 in the widest view (target < 1,000 on phones) | Unknown until measured (Shift+F2 render stats). The big risk is per-colour variety: 3-tone floors and ±5–8% colour variation make more unique part colours. Mitigation: shared textures, and only colour variation that reads |
| Highlights | ≤ ~40 enabled at once on phones | Each is a draw call + a post pass ([[Trap-Your-Friends-Style-Test-v1-Feedback]]; limit 255). Client turns off Highlights on traps > ~150 studs away |
| Frame time | 16.67 ms target | Measured with Studio as the front window (v2 lesson); worst views: tower top looking over the map, and the busiest zone with 12 noobs. Not a phone measurement |

## StreamingEnabled plan (DRAFT; defaults from [[Streaming-And-Instance-Streaming]])
- **Settings:**
  - `StreamingEnabled = true`, `StreamingMinRadius = 64`;
  - `StreamingTargetRadius = 512` (the whole island fits inside 512 from most spots on good devices; phones stream out opportunistically);
  - `StreamOutBehavior = Opportunistic`, `StreamingIntegrityMode = PauseOutsideLoadedArea`.
- **Atomic:** every trap model, socket pad, checkpoint, lookout and moving prop.
- **Persistent (few parts):** a low-detail **landmark shell** (keep silhouette + beacon + mage tower outline + curtain wall top), so the goal is visible from anywhere even on phones. Wait for `Workspace.PersistentLoaded` before the HUD shows the goal arrow.
- **Trappers:** the server sets `player.ReplicationFocus` to their zone's centre part during prep and the run, and calls `player:RequestStreamAroundAsync(zoneCentre)` at role reveal. Their whole zone then streams even while their camera orbits.
- **Client-created, not streamed:** sky, clouds and cloud meshes ([[Trap-Your-Friends-Sky-v3-Plan]]).
- **Server trap logic doesn't depend on streaming.** Clients predict knockback only from traps near their own character, which are always streamed in.

## Debris with 16 players on phones (DRAFT; built with the step 4 greybox, USER 2026-10-06)
- Debris is client-only and capped per client, so the player count doesn't multiply it directly. But **4 Trappers fire more traps**, so more hits land in view, and the cap recycles faster.
- **Per-client quality tiers** (⚠️ verify the best signal: `UserGameSettings().SavedQualityLevel` vs device memory):

  | Tier | Live cap | Linger | Debris per hit | Chips per hit |
  |---|---|---|---|---|
  | High | 250 | 10 s | 60 | 14 |
  | Low / phone | 100 | 4 s | 30 | 6 |

- **Distance LOD:**

  | Hit distance from the camera | What the client shows |
  |---|---|
  | > 160 studs | the hole only, no debris |
  | 80–160 studs | slabs only (no chips, no dust) |
  | < 80 studs | everything |

- **Server:**
  - at most ~3 cut hits per second per zone (extra hits merge);
  - a server cap of ~2,000 live fractured pieces; at the cap, the oldest broken part rebuilds early, still only with nobody within 10 studs;
  - `Fractured` sent only to players within ~200 studs (`FireClient` loop instead of `FireAllClients`), about 1.7 KB per big hit per client.

## Claude's honest read of this layout
- **Height:** most of it is in Zones 3–4. Zones 1–2 are flat apart from the branches. A raised barbican ramp in Zone 1 would help.
- **The east third of the island is empty:** room for scenery (orchard, windmill), a Zone 3 dungeon route, or the island shrinks to ~340×400.
- **Overlap:** the Sky Bridge passes over the Zone 3 hall. That gives a nice "see where you're going" moment, but Zone 4 sockets on the bridge must belong to T4, not T3.
- **Branch times:** branches take about the same average time as main routes (risk vs reward). Good runners save ~30 s. Tune in playtest.
- **Run timer:** now 3:30 (USER, DRAFT; `Config.Round.RunSeconds = 210`), so an average runner (~2:45) finishes in time.

## Open questions
1. ~~Prep visibility, triggers, Zone 3 tunnel, run timer, banner names~~: answered by Holden 2026-10-06 (above).
2. Market Rooftops leg is 41 s: OK to shorten it in the greybox as proposed?
3. Exact start-room activities (all four are DRAFT proposals).

## Related
[[Trap-Your-Friends]] · [[Trap-Your-Friends-v3-Plan]] · [[Trap-Your-Friends-Map-Plan]] · [[Trap-Your-Friends-Round-Structure]] · [[Trap-Your-Friends-Sky-v3-Plan]] · [[Trap-Your-Friends-Hero-Traps-Plan]] · [[2026-10-06-Trap-Your-Friends-Style-Test-v2]] · [[Streaming-And-Instance-Streaming]] · [[Performance-And-Profiling]] · [[Destruction-Modules-Audit]]

## Sources
- Holden's v3 planning prompt and decisions, 2026-10-06 (hub "Decisions from Holden").
- v2 counts: [[2026-10-06-Trap-Your-Friends-Style-Test-v2]] (local Studio measurements).
- Mobile budgets: Roblox docs, performance design (1,000 draw calls / 1M triangles example, 16.67 ms), via [[Performance-And-Profiling]].
- Lengths and times: `design/map1/make_layout.py` (computed from the polylines; speeds are DRAFT guesses, not playtested).
