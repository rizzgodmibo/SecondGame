---
tags: [playtest/studio, project/rubber-tower]
status: draft
updated: 2026-10-05
confidence: high
---
# Rubber Tower: Studio test of Squishies, Leap of Faith, hats and titles (2026-10-05)

A Studio Play Solo test run by Claude through the Studio MCP on Holden's PC, in the **private test place** (nothing public).
The 2-client test and the real phone test are Holden's to run (MCP can't start 2-client mode or the device emulator).

## TL;DR
- **Squishies faucets: PASS.** CP1/2/3 pay 50/75/100 once each. The first clean summit pays 200. The replay +20 pays once per UTC day ("already paid today" on the next one). A teleported (tainted) run pays nothing at the summit and doesn't count toward Squishmaster.
- **Leap of Faith: PASS** (reset to start, ragdoll fall, Full Send "fell 413 studs", recover, next run starts on leaving the ground floor). **The greybox lane isn't clear**, though: a running leap hit a segment piece at y≈130 and missed the cushion. Plan for a clear lane in the map build ([[Rubber-Tower-Map-Build-Plan]]).
- **Hats: 3 bugs found and fixed.**
  1. All 25 wobble hats lost their wobble parts in play: 58 joint attachments had world coordinates in `Position`.
  2. WeldConstraint glow parts stayed at the template spot when a hat was parented as-is.
  3. The title ignored hat parts above the Handle, so it sat inside the Mini_Wobbly_Tower.
  After the fixes all 8 test hats keep every part, jiggle in ragdoll (0–27°) and stay on (handle-to-head distance unchanged).
- **Titles:**
  - Above tower, castle and planet hats: **PASS**.
  - During ragdoll: **FAIL → fixed** (a fixed 2.3-stud offset let a tall hat poke above the title; now it follows the hat top, worst gap +0.12 studs).
  - Sparkle glyph showed as empty boxes: **FAIL → fixed** (white diamonds).
  - The title doesn't spin while tumbling: **PASS**.
- **Not done (needs Holden):**
  - the 16-dummy shot on the phone emulator at ~30 studs;
  - client FPS for the crowd (Studio was minimized, which throttles rendering to ~15 FPS);
  - the real 2-player test;
  - a real `/e dance` for Disco Duck.

## Results (pass/fail)
| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Boot | PASS | `[Boot] server ready: 7 services`, `[DevStress] loaded`, `[Boot] client ready: 5 controllers`, no script errors |
| 2 | Grant all titles | PASS | 27 `[Titles] … unlocked` lines; `[Squishies] … = 2975` |
| 3 | Nunito Heavy loads | PASS (earlier today) | TextBounds width 115 (Heavy) vs 112 (Bold) |
| 4 | Server sees the first jump | PASS | `[Titles] MiboRBX unlocked "Wobbly Beginner" (Common) - first jump` (velocity rule; jump states don't replicate) |
| 5 | Disco Duck real emote names | FAIL → changed to animation **IDs** | ⚠️ verify: not yet triggered with a real `/e dance` in play |
| 6 | Checkpoint payouts once each | PASS | `+50 (checkpoint 1)`, `+75 (checkpoint 2)`, `+100 (checkpoint 3)`; stepping back on CP2 paid nothing |
| 7 | Teleported summit pays nothing | PASS | `rose 99 studs in one sample: run tainted` → `reached the summit on a tainted run: no summit reward` / `no summit titles` |
| 8 | Clean first summit | PASS | `+200 (first summit)`, Rubber Champion +150, Speedy Noodle +300 (`summit in 13 s, skippedAll=false, tainted=false`) |
| 9 | Leap of Faith | PASS | `[Climb] MiboRBX took the Leap of Faith`; Checkpoint 4 → 0 at once; ragdoll at y≈383; `Full Send … fell 413 studs` |
| 10 | Replay +20 once a day | PASS | climb 2: `+20 (replay summit (once a day)) = 1170`; climb 3: `replay summit: already paid today` |
| 11 | Squishmaster counter | PASS | `TitlesState.counters.summits = 3` after 3 clean + 1 tainted summit |
| 12 | Hats on R6/R15, 4 avatars, big hair | PASS after fixes | Screens 03–06. Rigs: Holden's avatar (big emo hair), userId 1, userId 156, default, each R6 + R15 |
| 13 | Hats in ragdoll | PASS | 8 ragdolled dummies: every hat still has all its parts, handle-to-head distance unchanged; wobble tilt 0–26.6° then settles |
| 14 | Title above tallest hats | PASS after fix | Screens 03 and 08 (tower, castle, planet, rainbow arch) |
| 15 | Title during ragdoll | FAIL → fixed | Before: title 2.4 vs hat top 2.5 lying, 3.1 vs 7.1 mid-fall. After: worst gap +0.12 studs, 0.82 lying |
| 16 | LOD / declutter | PASS (visual) | Screen 07 (far line shows badge-only), screen 09 (a row of titles: nearer on top, farther faded) |
| 17 | 16 dummies + hats + titles, cost | PARTIAL | Server physics 1.58 ms / heartbeat 0.32 ms with 16 ragdolled; Studio memory 2,045 → 2,047 MB (+2 MB: Studio's whole process, not a phone figure). **Client FPS not valid** (window minimized). **No phone-emulator screenshot** |
| 18 | 2 players: titles for others, payouts once | NOT RUN | Needs Holden (Studio 2-client mode). Dummies tagged `TitleBearer` stand in for "other players" |

## Follow-up test items (Holden's list, later on 2026-10-05)
| Item | Result | Evidence |
|---|---|---|
| 16 dummies + hats + titles at ~30 studs, phone size | DONE as a stand-in | Studio's Device emulator can't be driven from the API, and clicking it would have taken over Holden's mouse while he used the PC. Instead, the Studio window was resized so the game view is **844×390** (iPhone-class landscape, logical px). Screen 10. Near titles read but small; farther ones become badge dots; overlapping titles get busy (BaseScale left as is until Holden's phone test, USER) |
| Real client FPS with Studio visible | NOT VALID | Studio throttles to **15 FPS when it isn't the focused window** (measured 15 FPS / 69 ms frames even un-minimized behind the browser). Proxy numbers with 16 dummies + hats + titles: render CPU peak **2.9 ms**, **79 draw calls**, **120.8k triangles**, client physics 0.27 ms. Real FPS needs Studio focused: Holden clicks into Studio, presses Play, then dev panel "Dummies: 16" → "Hats on dummies" → "Titles on dummies" → "Log numbers" |
| TexturePack 429 errors | PASS | After the 18:19 UTC reset: 0 TexturePack lines in a fresh play session. A kit atlas, a hat texture and a title icon all report `ImageLabel.IsLoaded = true`; Open Cloud shows the assets `Approved`/`Active` (`ContentProvider:PreloadAsync` reported "Failure" for these, which was misleading) |
| TP_Top_Hat streamer | FIXED | Wobble tail + joint rotated 110° about the hat's up axis in `ServerStorage.Hats` (now side/back); `art/batch_g.py` notes it for any re-export |
| Leap pad bigger + readable + proper standing launch | FIXED | `Summit_Leap_Pad` v2 (asset 134520179836644): 12×10 base, 18-stud board with white chevrons, gold arch whose "LEAP OF FAITH!" faces the approach (screen 11). The base is sunk so every step is ≤1 stud (a 2.6-stud base blocked walking). Launch code: the pad sets velocity outright, Physics state (no air control), re-applied for 3 frames. Standing and running players both land at x≈−104…−110 (same arc). Precise collision on the board (Default fidelity floated the collision ~2 studs above the plank) |
| Player's own hats hidden under a game hat (USER) | DONE (dev tools) | `DevStress putHat` hides the avatar's `AccessoryType.Hat` accessories and `hatOff` restores them; hair stays. Holden's avatar has no Hat-type accessories (shades = Face, hair = Hair), so it wasn't visible on him |

### Checklist for Holden's own tests
**2-player test** (Studio → Test → Clients and Servers → 2 players):
1. Each player sees the OTHER player's title above their head (name + title + gem), and their own a bit smaller.
2. Walk apart: the other player's title shrinks, then shows the badge only (~45–70 studs), then disappears (>70).
3. Stand together in a crowd: the farther title fades when it overlaps a nearer one.
4. Equip a title on player 1 (dev panel title list): player 2 sees it change within a second.
5. Payouts: player 1 claims CP1 (+50 in Output once); player 2 claims CP1 (+50 for player 2 only); player 1 steps on CP1 again (nothing).
6. Ragdoll player 1 (R): player 2 sees the title stay upright above the body.

**Disco Duck:** no secret room is placed yet, so Claude added a pink see-through test box `Workspace.TestPlace.DiscoDuckTestZone` (tagged `SecretRoom`, at (30, 5.5, −60) beside the dummy area; delete it after the test). Stand inside it (Nosy Noodle unlocks) and type `/e dance` (and try a wheel emote). Output should show `unlocked "Disco Duck"`. If not, copy the Output lines for Claude.

## Bugs found and fixed
1. **Hat wobble joints** (the Studio hat build script): the joint attachment `Position` held world coordinates such as (−7600, 0.19, 5200). In play the BallSocket yanked each wobble part 7,600 studs and it was destroyed. Edit mode never simulates it, so it looked fine there. **Fixed in `ServerStorage.Hats`:** 58 attachments set via `WorldPosition` (one undo step); every BallSocket pair now coincides.
2. **Equipping a multi-part hat:** parenting a template as-is leaves WeldConstraint parts behind, because the offset is baked when it becomes active. **Rule:** move every part to its final spot before parenting (`DevStress putHat`). The real hat shop must equip the same way.
3. **Title height:** it measured only `Handle`. Now it measures every accessory part, and while ragdolled it re-measures every frame (`TitleController.luau`).
4. **Sparkles:** `✦` isn't in Roblox fonts (it showed as an empty box). Now a rotated white Frame (`TitleBillboard.luau`).

## Weak spots (honest)
- **TP_Top_Hat:** the paper streamer hangs over the face on R15 (screen 06). Proposal: swing it to the side/back.
- **Small titles:** at ~15 studs on a 1,591 px wide viewport they read fine, but small. The phone test decides; `TitleUI.BaseScale` is the knob.
- **Floating hats:** hats rest on top of big hair (Holden's emo hair), so they look a little perched. That's normal Roblox behaviour (accessories don't collide). Whether to hide players' own hat accessories while a game hat is on is an **open question for Holden**, not decided.
- **Leap pad:** the kit leap pad looks small on the summit island, and with LaunchSpeed 60 at 10° tilt a standing player just hops on the tip; a running player goes off. Tune in the map build.
- **TexturePack upload errors (429):** Studio logged `Failed to upload TexturePack … Rate limit exceeded` for some SurfaceAppearances at play start. The textures still showed in the screenshots. ⚠️ verify: they appear after a publish once the rate limit resets.

## Screenshots
Files are in `Assets/Rubber-Tower-Studio-Test-2026-10-05/`:
- `01-leap-board-summit-edge.jpg`
- `02-BEFORE-fix-tower-missing-sparkle-boxes.jpg`
- `03-tall-hats-titles-fixed.jpg`
- `04-hats-r6-r15-bighair.jpg`
- `05-dragon-hood-front.jpg`
- `06-tp-top-hat-streamer-over-face.jpg`
- `07-ragdoll-8-dummies-hats-titles.jpg`
- `08-own-title-above-tower.jpg`
- `09-declutter-titles-in-a-row.jpg`

![[03-tall-hats-titles-fixed.jpg]]
![[08-own-title-above-tower.jpg]]

## Studio instances added (for Holden's review / deletion later)
- `ServerStorage.Kit.Batch_A…H` (557 staged models).
- `ServerStorage.Hats` (39 Accessories, attachments fixed today).
- `Workspace.TestPlace.LeapTest` (Summit_Leap_Pad on the summit west edge + Landing_Cushion at (−52, 2.75, 420)). Test only; delete when the map is built.
- Scripts written by the manual sync (Rojo wasn't connected): the services and controllers listed in [[Rubber-Tower-Title-UI]], `ServerScriptService.Server.DevStress`, `StarterPlayerScripts.Client.DevPanel`. `rojo serve dev.project.json` is still running, so a Connect reconciles them.

## Pitfalls
- **Studio has to be visible to render.** When it's minimized, `screen_capture` returns a white 3D view and the client runs at ~15 FPS. The FPS numbers from that state are worthless.
- **A `require` from `execute_luau` gets its own module copy,** so it can't read live service state. Use attributes, remotes or Output.
- **Edit-mode hat checks prove nothing about physics:** always test accessories in play.

## Related
[[Rubber-Tower-Build-Status]] · [[Rubber-Tower-Title-UI]] · [[Rubber-Tower-Squishies-Economy]] · [[Rubber-Tower-Valley-Kit]] · [[Rubber-Tower-Map-Build-Plan]] · [[Rubber-Tower]]
