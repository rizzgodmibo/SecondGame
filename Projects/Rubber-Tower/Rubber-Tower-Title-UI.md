---
tags: [project/rubber-tower, visuals/ui, design/progression]
status: draft
updated: 2026-10-05
confidence: medium
---
# Rubber Tower: Title UI above the head

Holden's brief (USER, 2026-10-05):
- The title above the head is **UI (a BillboardGui), not a 3D plaque**. Title_Plaque stays a world prop only.
- Research first, then **2–3 style mockups**. Holden picks one before any code.
- The title list itself is in [[Rubber-Tower]] (27 titles, Config `Titles`).

## TL;DR
- **2026-10-05, night: Studio-tested in play** ([[2026-10-05-Rubber-Tower-Studio-Test]]).
  - **Passing:** 27 grants = 2,975; titles above tower, castle and planet hats; no spin in ragdoll; LOD/declutter visually OK.
  - **Fixed:**
    - the height now uses every hat part (it used the Handle only);
    - the ragdoll height follows the hat top every frame (a fixed 2.3 studs let tall hats poke above);
    - the `✦` sparkle showed as an empty box, so it's now a white diamond Frame.
  - **Real icons are live:** the 12 uploaded decals → image IDs in Config `TitleUI.BadgeImage` / `GemImage` (table below).
  - **Still open:** the phone-emulator check at ~30 studs and the 2-player check (Holden).
- **Holden picked style C Clean Text (USER, 2026-10-05)**, ~13% smaller. **His own title shows**, a bit smaller than other players'.
- **The v2 mockup is ready** (below):
  - smaller;
  - a **gem shape per rarity** after the text (dot, diamond, shiny diamond, double diamond, star, rainbow crown), so tiers read without colour;
  - a shine on Rare and a small category badge;
  - an 8 px ink stroke on every tier;
  - tested on all 4 segment backgrounds (grass, purple mushroom cliff, ice cliff + snow, white clouds);
  - the final 27-title list.
- **The build plan + file list are below, waiting for Holden's approval.** No code yet.
- **Crowds:** levels of detail by distance + declutter (nearer on top, an overlapped farther title fades to 30%).

## Research (captures + sources: `Assets/Reference-Captures/Titles/MANIFEST.md`)
**What we take:**
- **Shiny Spotter** (Holden's earlier capture): badge left, rarity outline, bold stroked text, name underneath, only 2 lines. This is the base for style A.
- **DefaultOverheads** (DevForum):
  - distance scaling 1.0 under 20 studs, 0.75 to 50, 0.5 beyond;
  - a fade over the last 10% of the display distance;
  - raycast occlusion.
  - That's the source of our LOD and scale steps.
- **Blox Fruits:** the Titles menu pattern. A list with Equip buttons; locked rows show "???" and the goal. That's how our Titles menu should list locked titles ("Unlock" text from Config).

**What we avoid:**
- 3–4 line stacks (two DevForum showcases) and oversized text (Epic Minigames "Youtuber"). They block the climb, and 16 of them would cover the screen.

**Checked and not applicable:**
- Pet Simulator 99's VIP tag is a chat nametag.
- Bee Swarm shows names over hives.
- Grow a Garden, Islands and the game-page media of all five games show no overhead titles.
- ⚠️ verify in a live server; this is from wikis and game pages only.

## Mockups v1 (2026-10-05; Holden picked C)
**How they were made:**
- `RubberTower/art/title_mockups/scene.py` (Blender) renders the kit scene at phone landscape size: 844×390 pt @2x, Roblox FOV 70.
- Avatars wear Mini_Wobbly_Tower, Tiny_Castle, Orbiting_Planet, Duck_King, Propeller_Beanie, Traffic_Cone and Wizard_Star_Hat; one is ragdolled, one stands on a floating island.
- The script exports the anchor above each head or hat.
- `gen.py` draws each style as HTML at those anchors (Roblox fonts Fredoka One / Luckiest Guy / Nunito), screenshotted with headless Chrome.

**Each mockup shows:** the scene, a rarity ladder (all 6 tiers at full size) and the 6 category badge icons.

![[Title_Style_A.png|900]]
![[Title_Style_B.png|900]]
![[Title_Style_C.png|900]]

**Honest read:**
- **A Badge Banner:**
  - The most readable plate.
  - Rarity reads instantly from the fill colour.
  - Closest to the reference.
  - The widest of the three.
- **B Ribbon:**
  - The most "reward" feel, with chunky Luckiest Guy letters.
  - The tails and gem make it the biggest silhouette, which is the worst in crowds.
  - All-caps hurts long names a bit.
- **C Clean Text:**
  - The lightest; best in crowds.
  - Rare and Common look plain, because the stroke does most of the work.
  - Gradient text needs a thick stroke to stay readable on grass and sky.

## Style C v2 (2026-10-05, waiting for Holden's "go")
![[Title_Style_C_v2.png|900]]

**Honest read:**
- **Readable on all 4 backgrounds.** The weakest case is the Common light fill over white clouds; the 8 px stroke holds it.
- The gem glyphs are small (about 21 px @2x, i.e. ~10 pt): they're a glance cue, not a feature.
- **Ragdoll offset:** a lying body's title sits 2.3 studs above the root, lower than the 3.2 in v1, which floated over the next player.
- In a tight crowd the farther titles fade, as designed. A title can still sit over someone else's body from some camera angles. That's a limit of overhead titles, not a bug.

## Spec (Holden's requirements → plan)
| Requirement (USER) | Plan (PROPOSAL until Holden picks; then built and tested) |
|---|---|
| Banner: title on top, name below, rarity border, category badge on the left | Style per pick. Categories: Climb, Social, Collection, Secret, Joke, Daily (Config `Titles[*].Category`) |
| Bold rounded font, thick UIStroke, readable on a phone at ~30 studs | Title ≥ 15 pt on a phone at full size (30 px @2x in the mockups); UIStroke 3–4, round joins. At 30 studs the title-only LOD shows at 0.85 |
| Rarity effects | Common grey · Uncommon green · Rare blue + a shine sweep every ~4 s · Epic purple UIGradient scrolling · Legendary gold shimmer + 3 sparkles · Mythic rainbow/pink scrolling gradient + 4 sparkles (hat rarity colours from batch (g)) |
| Above tall hats | Offset = head top + equipped hat height + 0.5 studs (the hat's bounding box, read once on equip; anchors in the mockup do exactly this) |
| Ragdoll: follow smoothly, no spinning | Adornee = HumanoidRootPart with **StudsOffsetWorldSpace** (world-up offset, not the head's local axes), so it never rotates with a tumbling body. ⚠️ verify in Studio during the hat fit/ragdoll test |
| Fade with distance, small, fine with 16 players | Fixed-pixel size; client-side LOD every ~0.2 s: full under 25 studs, title only 25–45, badge only 45–70, hidden past 70 (MaxDistance 80 as a backstop); declutter by screen-space overlap (nearer on top, overlapped farther → 30%) |
| One title equipped, Titles menu, locked titles show how to unlock | Titles menu lists all 27 with rarity colours; locked rows grey with the `Unlock` text; Equip button; server stores `EquippedTitle` and validates ownership |

**Build notes (for after the pick):**
- One BillboardGui per character, created by the client for every player, so each client can do its own LOD.
- The server only replicates the equipped title id (an attribute on the Player).
- Hide the default Roblox name, since the banner shows it: `Humanoid.DisplayDistanceType = None`. ⚠️ verify it doesn't hide anything we need.
- Performance: up to 16 animated UIGradients + sparkles. Animate only titles within 45 studs. ⚠️ measure on a phone.

## Title system v1: BUILT 2026-10-05 (code gate PASS; Studio-tested the same night)
**Holden's answers (USER 2026-10-05, evening):**
- Session-only saving.
- Squishies payouts logged to Output, with the total in the dev panel.
- **No HUD counter, Titles button or Titles menu until the UI pass.** Titles are equipped from the dev panel (dev-only, gated).
- The overhead title is built for real.

**Evidence:** `gate.sh .` gives `GATE build PASS`, `tests PASS (SPECS 41 passed, 0 failed)`, `lint PASS`, `format PASS`, `GATE PASS`. The new specs:
- `tests/Titles.spec.luau`: 27 titles, ≤16 characters, 5/7/7/4/2/2 rarities = 2,975, categories/checks/colours, equip validation, counters, summit rules, LOD, size steps, declutter overlap, signal.
- 3 new fall-drop cases in `tests/Ragdoll.spec.luau`.

**Run in Studio 2026-10-05 (night).** The Rojo plugin still wasn't connected, so the sources were synced by hand (execute_luau, each file checksum-verified against the local file). Results are below the file table.

| File | Status | What it does |
|---|---|---|
| `src/shared/Rules/Titles.luau` | new | Pure rules: byId, payout, canEquip, reached, summitUnlocks (Checkpoint Who? / Speedy Noodle / False Conqueror), lod, sizeScale, overlaps |
| `src/shared/Util/Signal.luau` | new | Synchronous signal; one bad handler can't break the others |
| `src/shared/Rules/Ragdoll.luau` | changed | `fallDrop()`: speed before the confirm (v²/2g) + confirm height to lowest point |
| `src/shared/Config.luau` | changed | Final `Titles` (with `Check`), `TitleUI` (scale 0.87, own 0.88, LOD 25/45/70, size steps, rarity colours/gradients, empty icon-id tables), `WorldTitles`, `Checkpoints.MaxMoveStudsPerSample` |
| `src/shared/Remotes.luau` | changed | `EquipTitle` (client → server), `TitlesState` (server → owner) |
| `src/server/Services/PlayerDataService.luau` | new | Session store (ProfileStore-shaped API); `AddSquishies` logs `[Squishies] name +75 (title X) = total` and sets the attribute `Squishies` |
| `src/server/Services/TitleService.luau` | new | Grant (idempotent, pays once), AddProgress, AddUnique, Equip (+ remote: rate limit 4/s, type/length check, must own) → attribute `EquippedTitle`; checkpoint + summit + fall titles; hides the default name |
| `src/server/Services/CheckpointService.luau` | changed | `Claimed` signal + climb trace (start time, claimed set, teleport taint outside grace periods, `MarkSkipUsed` for the future skip pass) |
| `src/server/Services/RagdollService.luau` | changed | `Fell` (confirmed fall) and `FallEnded(dropStuds)` |
| `src/server/Services/WorldTitleService.luau` | new | First jump, secret room (+ dance), hidden ducks, server-counted bounces (20 Hz), 3 friends in the server |
| `src/client/UI/TitleBillboard.luau` | new | Style C v2 billboard: badge, gradient title with ink stroke, gem, name, sparkles; LOD, scale, fade, effects. **Icons are text stand-ins (emoji badge, glyph gem) until the icon upload** |
| `src/client/Controllers/TitleController.luau` | new | Billboards for every player (yours ×0.88) + `TitleBearer`-tagged models; hat-height offset, ragdoll offset (eased), 5 Hz LOD/size/declutter, effects within 45 studs |
| `src/server/DevStress.server.luau`, `src/client/DevPanel.client.luau` | dev only (gitignored) | Commands `grantTitle <id>`, `grantAllTitles`, `titleDummies`; panel shows Squishies + equipped title, a scrolling title list (tap = grant if needed + equip, tap again = off), "Title off", "Titles on dummies" |

**Not wired yet (hooks ready: one `Grant`/`AddProgress`/`AddUnique` call each):**
- shop: Fresh Fit, Shroom Drip, Hat Goblin, Mad Hatter;
- skip pass: Millionaire, plus `MarkSkipUsed` for False Conqueror;
- dailies: Loyal Squish, Streak Freak;
- hand-up: Human Ladder;
- shove: Pushy (`AddUnique` "pushTargets");
- banana peel: Banana Bandit (`AddUnique` "slipVictims").
- ~~Squishmaster needs a way to climb again~~ → **done 2026-10-05:** the Leap of Faith (USER) + clean-run trace. The checkpoint and +20 replay payouts are now paid too (`RewardService`).

**Studio checks to run after Connect:**
- **Boot:** Output shows 6 server services and 5 client controllers, no errors.
- **Titles:**
  - Grant all from the dev panel: 27 `[Titles]` lines, Squishies total 2,975.
  - Equip each rarity and look at the billboard (fonts: ⚠️ verify the Nunito Heavy face loads).
  - Tall hats (until the hat upload, test with Holden's own accessories).
- **Ragdoll:** "Ragdoll me": the title eases down and doesn't spin.
- **Crowd:** 16 dummies + "Titles on dummies": LOD/declutter, FPS in the panel.
- **Climb titles:** checkpoints → Meadow Hopper / Mushroom Muncher / Frostbitten / Rubber Champion, summit without CPs → Checkpoint Who? (dev "goto" teleports taint the climb, as designed).
- **First jump:** ⚠️ verify the server sees the Jumping state.
- **Bounce counting:** check the 20 Hz bounce count matches real bounces.

**Studio check results (2026-10-05, night; full list in [[2026-10-05-Rubber-Tower-Studio-Test]]):**
- **Boot:** 7 services, 5 controllers, no errors.
- **Grant all:** 27 lines, 2,975.
- **Nunito Heavy:** loads.
- **First jump:** the server sees it (velocity ≥ 20 studs/s; jump states don't replicate).
- **Disco Duck:** names → animation IDs (⚠️ verify).
- **Climb titles:** Meadow Hopper, Mushroom Muncher, Frostbitten, Rubber Champion and Speedy Noodle on a clean run; none on a tainted run.
- **Full Send:** "fell 413 studs" on the Leap.
- **Ragdoll:** fixed (see TL;DR).
- **Not run:** a real bounce-count comparison; 2 players; phone emulator.

**Title icons (uploaded 2026-10-05 as Decals by MiboRBX; Config uses the decal's image ID):**
| Icon | Decal ID | Image ID (Config) |
|---|---|---|
| Badge_Climb | 121622160581958 | 129415727616119 |
| Badge_Social | 79082910871187 | 79530242352141 |
| Badge_Collection | 135871972352416 | 88348599910785 |
| Badge_Secret | 131181118835123 | 92030161377315 |
| Badge_Joke | 112776375307107 | 96296488031072 |
| Badge_Daily | 84496206903669 | 124450320881807 |
| Gem_Common | 98467924406810 | 111576296771291 |
| Gem_Uncommon | 82204106935917 | 95865183972064 |
| Gem_Rare | 119373946045896 | 126537853516169 |
| Gem_Epic | 97333935392706 | 136487588416237 |
| Gem_Legendary | 77437168915099 | 95625885449081 |
| Gem_Mythic | 107003972485786 | 76482573304558 |

## After the title system: the test place (DONE 2026-10-05 with Holden's OK)
- **Upload:** the kit (batch (a)-(h) GLBs, the hats as Accessories, and the 12 title icons) to the test place. **Only after Holden says OK; nothing uploads before that.**
- **Check:**
  - hats on real avatars (R6 + R15, hair);
  - hats + titles during ragdoll;
  - titles with 16 dummies on a phone (Studio device emulator + Holden's phone).

## Checklist
- [x] Holden picks a style: **C Clean Text**, ~13% smaller (USER 2026-10-05); v2 mockup made
- [x] Holden says go on C v2 and approves the build plan (USER 2026-10-05: no HUD/menu until the UI pass; dev-panel equip)
- [x] Title system v1 built, gate PASS (41 specs)
- [x] Studio checks (2026-10-05, manual sync instead of Rojo Connect; 2 bugs fixed)
- [x] `TitleController` (client) + `TitleService` (server) built
- [x] Studio test: tall hats, ragdoll tumble, 16 dummies (server cost only)
- [ ] Phone emulator at 30 studs + client FPS (Studio window visible), 2-player test, real phone (Holden)
- [ ] Titles menu screen (locked/unlocked/equipped states): **waits for the UI pass** (USER)

## Related
[[Rubber-Tower]] · [[Rubber-Tower-Squishies-Economy]] · [[Rubber-Tower-Valley-Kit]] · [[UI-Polish-And-Juice]] · [[UI-And-Gameplay-Reference]] · [[X-HUD-And-Menus-UI]]

## Sources
- DevForum: https://devforum.roblox.com/t/defaultoverheads-a-familiar-overhead-gui-system/2730927 ; https://devforum.roblox.com/t/player-ui-overhead-title-username-display-name/1682758 ; https://devforum.roblox.com/t/i-made-a-fun-little-gradient-nametag-module/1151099
- Blox Fruits titles: https://www.youtube.com/watch?v=CbHxNK0kG-o ; https://blox-fruits.fandom.com/wiki/Titles (the page returned HTTP 402 to the fetch tool; not read)
- Pet Simulator 99 VIP chat tag: https://pet-simulator.fandom.com/wiki/VIP_Gamepass_(Pet_Simulator_99) ; Bee Swarm names over hives: https://bee-swarm-simulator.fandom.com/wiki/Hive
- Accessed 2026-10-05.
