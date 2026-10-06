---
tags: [project/rubber-tower, project/status]
status: draft
updated: 2026-10-05
confidence: high
---
# Rubber Tower Build Status

Managed by the `roblox-game-manager` skill. Read this first every session. The plan and file lists are in [[Rubber-Tower-Build-Plan]]. Decisions are in [[Rubber-Tower]].

## TL;DR
- **PAUSED (Holden, 2026-10-05, ~19:20 EDT).**
  - Restart with [[Rubber-Tower-Slice-Fix-Pass-Prompt]], a fix pass on the slice: water, the visible void, ground. Places 3–6 stay untouched.
  - Holden has not given feedback on the slice yet beyond that prompt.
  - Models are archived in AssetLibrary `models/rubber-tower-kit-v6-map/`; the game repo gitignores the `.blend`/GLB files.
  - Rojo was stopped.
  - Nothing is committed: about 58 changed or new files in the game repo, plus the vault changes, are left for Holden to commit.
- **Now (2026-10-05, ~19:10 EDT): map v3 VERTICAL SLICE BUILT, STOPPED for Holden's review** ([[Rubber-Tower-Map-Build-Plan]] → "Vertical slice BUILT").
  - History today: Option B picked → build 1 (all six places) → Holden: "not an obby yet" → combo rework + mechanics approved → the slice.
  - The slice: hub v3, ground v3, cliff kit v2, waterfall v2, the START gate, Lily Lake (deep water) and the Village Rooftops (Miller's Yard).
  - New gameplay code: swings/fans/slingshot (`MoverController`), water hazards (`WaterController` + `HazardService`), seesaw + per-cube jelly stiffness (`WobbleController`). Evidence: `GATE PASS` (56 specs).
  - Measured: expert-style bot spawn → windmill ≈ 80–100 s of play (154 s with bot stuck-timeouts), 0 lake falls, 2 hammer bonks. The first-timer estimate (3–5 min, 4–8 falls) is a GUESS until Holden's phone run.
  - Open: the Leap lane is blocked by the S3/S4 greybox; places 3–6 are still build 1; real client FPS still needs a focused Studio.
- **Earlier (2026-10-05, late): map layout = WAITING FOR HOLDEN'S PICK (option A "Valley Ring" or B "Through the Middle").** → Holden picked B.
  - Layout v1 was rejected by Holden as "a classic linear obby" and stopped before any build; the critique and both options are in [[Rubber-Tower-Map-Build-Plan]].
  - **Test items done** ([[2026-10-05-Rubber-Tower-Studio-Test]], "Follow-up"):
    - phone-size (844×390) crowd shot;
    - textures pass after the 429 reset;
    - TP_Top_Hat streamer moved;
    - **leap pad v2** (bigger, readable arch, walkable, same arc standing or running);
    - own hats hidden under a game hat (dev tools).
  - **Real client FPS is not measured:** Studio caps at 15 FPS unless it's focused. Steps for Holden are in the test note.
  - Code gate `GATE PASS` (44 specs) after the leap-launch change (`BounceController`, `CheckpointService.LeapRangeStuds`, Config `LeapRangeStuds`/`LeapGetUpSeconds`).
  - **Built, ready for the map:**
    - `Valley_Floor_S1` + `Pond_Basin` (asset 89785848208249);
    - `tools/BuildValleyS1.luau` (kit placer, not run);
    - `art/map/kit_colliders.json`.
  - **Holden's own tests:** a 2-player checklist + Disco Duck test zone (`Workspace.TestPlace.DiscoDuckTestZone`).
- **2026-10-05, night: gaps closed, Studio checks run, test-place uploads done. STOPPED for Holden's review.** Full pass/fail list + screenshots: [[2026-10-05-Rubber-Tower-Studio-Test]].
  - **Built:**
    - Checkpoint Squishies (50/75/100/200, once each) and +20 replay (once per UTC day, clean runs only), session-only, logged to Output, total in the dev panel (`RewardService`).
    - **Leap of Faith** (USER): a summit pad tagged `LeapOfFaith` + `BouncePad` resets progress to 0. A run starts when you leave the ground floor (start top + 15 studs). A rise of more than 35 studs in one 10 Hz sample taints the run. Tainted runs get no summit reward, no summit titles and no Squishmaster count.
    - Kit models `Summit_Leap_Pad` + `Landing_Cushion` (batch h).
  - **Code gate:** `GATE PASS` (44 specs).
  - **Uploads (Holden's OK, private test place only):**
    - kit batches a–h as 13 GLBs;
    - 39 hats (built in Studio as Accessories);
    - 12 title icons.
    IDs are in [[Rubber-Tower-Valley-Kit]] and [[Rubber-Tower-Title-UI]]. The placeholders were swapped for the real icons.
  - **Studio results:**
    - Payouts, the Leap and the replay pass.
    - First jump passes (velocity rule).
    - Nunito Heavy passes.
    - Dance detection moved to animation IDs (⚠️ verify with a real `/e dance`).
    - **3 hat bugs + 2 title bugs found and fixed:** wobble-joint attachments, WeldConstraint baking, title height from all hat parts, title height while ragdolled, sparkle glyph.
  - **Not done, needs Holden:**
    - the 2-client test;
    - the phone-emulator 16-dummy shot + client FPS (Studio was minimized, which throttles rendering);
    - the real phone test.
  - **Next (after the review, plan only):** [[Rubber-Tower-Map-Build-Plan]] (ground floor + S1 with the obby pieces, then stop).
- **2026-10-05, evening: title system v1 BUILT** (the overhead title is approved for real). Evidence: `GATE PASS` (build, 41 specs incl. `Titles.spec`, lint, format). **Studio test pending:** Holden presses Connect in the Rojo plugin (`rojo serve dev.project.json` is running); the checks are listed in [[Rubber-Tower-Title-UI]].
  - **USER decisions (2026-10-05, evening):**
    - Saving is session-only for now (real saving later).
    - Squishies payouts are logged to Output, and the total shows in the dev panel. **No on-screen counter.**
    - **No HUD Titles button and no Titles menu yet.** For testing, titles are equipped from the dev panel (dev-only, gated like the other Dev scripts).
    - The style C overhead title gets built for real.
  - **Waiting for the UI pass** (Holden wants to plan it properly first; he has rejected primitive-built UI before, see [[Art Direction Feedback]]):
    - **Squishies counter.** Suggested spot: top-left under the Roblox menu buttons, a painted jelly-coin pill with the duck coin icon. Clear of the phone thumbstick (bottom-left) and jump button (bottom-right).
    - **Titles button.** Suggested spot: left edge, middle of the screen, in a short column of painted round buttons (Titles, Hats, Shop later). Thumb-reachable on phones and clear of the climb view.
    - **Titles menu.** Suggested: a centred panel (~70% of the phone screen) opened from that button. Rows grouped by rarity, each showing the real style-C preview; locked rows greyed with the unlock text + a progress bar; Equip/Unequip on the right; a "new" dot on fresh unlocks.
    - **Unlock toast** (title + Squishies payout). Suggested: top-centre, slides down, 2.5 s.
    - All four use painted image assets made in the UI pass, not primitives.
- **Now (2026-10-05, late afternoon):**
  - **Title UI = style C, ~13% smaller, your own title shown (USER).** The v2 mockup is fixed (gem shape per tier, Rare shine, small badge, tested on 4 backgrounds, final list).
  - **Final 27 titles are in Config** (Claude, as delegated; same rarity counts, still 2,975; gate PASS). Legendary stays 900 (USER).
  - **Batch (h) v3 kit fixes:** rocky secret-room hideout with a turf roof, smooth clipped hedge, winter twins of the batch (b) lantern post, bench, barrel, well and a frozen fountain.
  - **Waiting for Holden:** "go" on C v2, and approval of the **title system plan + file list** ([[Rubber-Tower-Title-UI]] "Build plan v1"), including 3 decisions (session-only saving shim vs phase 4 first, session Squishies wallet, Titles button placement).
  - **Next after that:** code the title system; then the test place, **asking before any upload.**
- **Earlier 2026-10-05:**
  - **2026-10-05:** the Squishies economy is locked (USER numbers; Config `Squishies`; code gate PASS; [[Rubber-Tower-Squishies-Economy]]). Holden still decides the missed-day rule (Restart vs the Grace PROPOSAL), the repeat-summit +20/day PROPOSAL and the title list. **Batch (h) extra + misc is built** (106 models, preflight PASS, gameplay UI icons). **Waiting for Holden's review.** Next after the review: upload the kit to the test place for the hat fit and ragdoll test, only with Holden's OK.
  - **The v5 style is approved and locked** (USER: "Lock it in"): [[Rubber-Tower-Art-Style-Guide]].
  - The v5 test pieces were uploaded with Holden's key (ids in `AssetLibrary/models/rubber-tower-kit-v5/README.md`) and staged in Studio under `workspace.StyleTest_v5`, at about (1500, 800, 1500).
  - Holden ordered TONS of models ([[Rubber-Tower-Kit-Full-Prompt]]), in review batches (a) to (e).
  - Batch (a) was reviewed: USER "keep the colors", "start with batch B and after batch B make even more".
  - **Git (2026-10-05, Holden asked Claude to commit):** vault commits merged into `main` (fast-forward; branch deleted). RubberTower repo first commit `fb9c092` on `main` (code + art scripts + manifests; generated art gitignored). Nothing pushed.
  - **Session end 2026-10-05:** batch (g) reviewed. Gamepass shop = **B Caravan** (USER, "for now"). Weak hats fixed (flaming crown, rune crown, hot dog); the rest are kept as they are (USER). **Next session: Holden sets the hat Squishies prices, then batch (h) extra + misc.**
  - **2026-10-05:** Squishies = D Duck on the Grape coin (USER). Cosmetics shop redone as a fantasy hat shack after Holden rejected the pink boutique; batch (f) preflight PASS. **Next: Holden reviews the shack, then batch (g) hats.**
  - **Session end 2026-10-04:** Holden reviewed (f): keep the colours, text fine. Weak pieces fixed. Squishies coin: 6 options built, **Holden picks one**. **Next session: batch (g) crazy hats** (USER: "we can move forward tomorrow").
  - **Batch (f) NPC shops and structures is built** (39 types, 47 meshes, preflight PASS, NPC spots and prompt anchors in the manifest), plus the fixes (dragon v2, crystal shard v2, spell books v2, rune stone v2). **Waiting for Holden's review**, then (g) hats and (h) misc, each with a review stop.
  - **Batches (b) to (e2) are built** (S1 meadow + props, S2 mushroom grove, S3 crystal-ice, S4 cloud kingdom + magic, landmarks + backdrop): [[Rubber-Tower-Kit-Batch-Results]]. They are **waiting for Holden's review**.
  - No uploads or map building until Holden says (USER).
  - **Studio leftovers for Holden to delete when done:** `Workspace.StyleTest_v5` (5 test models, 2 avatar dummies, `LedgeColliders`, `TestFloor`).
- **Earlier:** phases 0 and 1 passed. Phase 2 greybox v1 is built and passes every automated check, but Holden rejected the layout (too enclosed and narrow, no fantasy world feel). The **v2 plan is proposed** in [[Rubber-Tower-Build-Plan]], waiting for his answers. The code stays as is. Holden's first commit is still pending.
- **Project:** `C:\Users\holde\Documents\GameDev\RubberTower` (local git on `main`, no GitHub remote). Holden saved the place (2026-10-04).
- **Next step (proposed):**
  1. Holden saves the place, reviews it, and commits.
  2. Holden publishes the test place privately and runs the phone test with the dev panel.
  3. Phase 1 gate decision.
  4. Then phase 2 (tower greybox).
- **Phase mapping:** build-plan phase 0 (scaffold) = playbook phase 2 (Bootstrap). Build-plan phases 1 to 4b = playbook phases 3 to 4.

## Gates
| Build-plan phase | Playbook phase | Status | Evidence | Date |
|---|---|---|---|---|
| Concept | 0 Concept | passed | Holden chose Rubber Tower from [[Game-Concept-Shortlist-2026-10-04]] | 2026-10-04 |
| GDD | 1 GDD | **open** | GDD v0.1 is mostly DRAFT. Holden ordered the scaffold and ragdoll prototype first | |
| 0 Scaffold | 2 Bootstrap | **code checks passed; Holden's commit pending** | `gate.sh --scaffold`: `GATE build PASS`, `tests PASS (SPECS 5 passed)`, `lint PASS`, `format PASS`, `GATE PASS`. Rojo 7.7.0 synced into Studio. Output showed `[Boot] server ready: 1 services` and `[Boot] client ready: 2 controllers` with no errors. Note: by the time Studio first booted, phase 1 code was already present, so an empty phase-0-only boot was never run in Studio | 2026-10-04 |
| 1 Ragdoll prototype | 3 (slice, first part) | **passed** (phone cost numbers waived by Holden: "waive it") | See "Phase 1 evidence" below | 2026-10-04 |
| 2 Tower greybox | 3 (slice) | **open: v2 rejected by Holden ("a cage"); v3 kit (28 models) rendered, waiting for his upload OK** | See "Phase 2 evidence" below | 2026-10-04 |
| 3 to 8 | 3 to 9 | open | | |

### Phase 1 evidence (2026-10-04)
1. **Code gate:** `GATE PASS` with `SPECS 18 passed, 0 failed` after all fixes. The `roblox-dev:roblox-reviewer` audit found **no high-severity issues**:
   - Fixed in the code: M2 (short falls not confirmed), M3 (dev scripts could be published), L1–L5 and L8–L10.
   - M1 (shove immunity): partly fixed, since a shove now extends an existing ragdoll. A server fall cooldown is left for phase 3.
   - Left open: L6 (appearance wait, improved but not re-reviewed) and L7 (the loader stops if an Init errors; Init/Start order is not fixed).
2. **Studio test, one client:**
   - `[DevStress]` self-test **15/15 PASS**. It covers: your live R15 avatar ragdolls, recovers in 2.6 s (minimum 2.5 s), stays alive and ends upright (`up.Y = 1.00`); and 50 ragdoll cycles on an R15 and an R6 dummy add no instances (330 → 330, 119 → 119).
   - Walk-off-ledge fall test, 4 tries per height: **8 studs 0/4, 11 studs 0/4, 13 studs 4/4, 16 studs 4/4, 32 studs 4/4**. Alive and upright every time.
   - Bounce pads: default 90 studs/s rose 20.3 studs (20.6 predicted); strong 140 rose 50.4 (49.9 predicted); the angled pad moves you sideways. None of them ragdoll.
   - A screenshot shows the avatar fully limp on the floor.
   - **Two clients (Holden, 2026-10-04):** "testing with 2 players now, test went all good!"
3. **Real phone (Holden, 2026-10-04):** "saved the place, testing on my phone now, testing was fine". Holden's verdict on feel. No phone numbers recorded yet.
4. **Cost table:** Studio on Holden's PC only, see [[Avatar-Ragdoll]]. With 16 dummies ragdolling: server physics about 1.4 ms per frame (server-owned), client physics about 0.9 to 1.5 ms (client-owned), 60 FPS. **The phone row is still missing**: the dev panel numbers with 16 dummies, plus the phone model, are asked for.
5. **Holden's verdict:** positive on the phone and in the 2-player test. Phone cost numbers **waived** by Holden ("waive it", 2026-10-04), so the cost on a phone is **not measured**. Re-measure before lowering `MaxSimultaneous` or at soft launch.

### Phase 2 v3 progress (2026-10-04)
- **Holden's v2 critique is logged in [[Rubber-Tower]].** In short: a cage, all parts, one colour, no route, no goal, an empty floor. He wants mountain-wall terrain, real kit meshes, per-segment colour bands, landmarks, the obby lighting, and ground + S1 only before review.
- **Studio screenshots fixed:** Studio was maximised but covered, so it didn't draw. Bringing its window to the front (PowerShell SetForegroundWindow) before `screen_capture` works. "Before" shots taken: spawn looking up (the cage pillars), an outside corner overview.
- **"Random pieces" identified:** 20 translucent neon PillarCrystal caps (the see-through band), the neon FloatingCrystals and the glass Pond (cyan), the SummitPad (yellow on the white summit disc), and the phase 1 TestPlace outside the walls.
- **Kit v3:** 28 models (backdrop cliffs, arch, waterfall, spire, far mountains, clouds, ground, pond, gate, boulders, flowers, meadow islets S/M/L, mossy ledges S/M, flower bounce, checkpoint island, beacon, summit crystal). Preflight PASS (0 FAIL, 3 intentional WARN). Self-critique iterations are in [[Rubber-Tower-Valley-Kit]]. Imported into Holden's live Blender (scene `RT_ValleyKit`). **Upload waits for his OK on the renders.**
- **Next, after the OK:** upload with Open Cloud, insert into ServerStorage, then rebuild the ground and segment 1 with the meshes and invisible colliders, the obby lighting and beacons. Then the 4-angle screenshots with before/after, the map audit, and stop.

### Phase 2 evidence (valley v2, 2026-10-04)
- **Built:** `tools/BuildValleyGreybox.luau` (v1 tower builder deleted). 640 parts:
  - a 240×240 valley floor with a pond, meadow patches and a start plaza;
  - full-height rampart walls (440) with bands, pillars, crystal caps and battlements;
  - floating crystals in the middle;
  - 4 checkpoint islands (48 across) at 101/201/301/401;
  - each segment leaves its island, spirals round a 62-stud ring of islets with one wall-terrace run, and bridges back in;
  - 141 islets, 20 terraces, 12 wobble, 4 ice, 4 bounce, 6 soft rest islands;
  - 129 of Holden's existing low-poly props (trees, bushes, boulders, glow shrooms) as no-collide decor;
  - lavender Atmosphere and moderate ambient light.
- **Map audit** (per segment, spacing 1, MustReach on the next island's pad): **S1–S4 PASS, 0 FAIL, every cell reachable**. It found and fixed: a hovering low islet (floating FAIL) and bridge islets sinking into islands (overlap).
- **Bounce walk-tests:** 4/4 land (segment 3 after correcting the test's start position: it rose 23.6 studs and landed). Checkpoints claim 1→2→3→4. A fall below CP2 sends you back.
- **Art kit:** 9 Blender models, **preflight PASS (0 FAIL, 0 WARN)**, [[Rubber-Tower-Valley-Kit]]. **Not uploaded** (needs Holden's OK).
- **Not seen in Studio:** the Studio window wasn't drawing 3D, so every screenshot was white. The visual check waits for Holden.

### Phase 2 evidence (greybox v1, 2026-10-04)
- Code gate `GATE PASS`, `SPECS 23 passed`. The `roblox-dev:roblox-reviewer` audit of the phase 2 code found **no high-severity issues**. Fixed:
  - M3: the wobble push is capped after a frame hitch.
  - L1: one broken wobble platform no longer stops the rest.
  - L2 and L3: claims are now a server 10 Hz position check, not client Touched.
  - L4: progress is clamped.
  - L5: missing pads warn, removed pads are dropped.
  - L6: the spawn move waits for the character.
  - L7: weak mass cache.
  - L8: the toast fade is cancelled.
  Re-tested 7/7 checkpoint checks, and the dev "Reset progress" now moves you to the start.
- **Open for later phases:**
  - M1, titles: a teleporting exploiter could claim the summit without checkpoints, so the server should record a climb trace and a `skippedCheckpoints` flag before the "no checkpoints" title.
  - M2, phase 4: write progress through to the profile at claim time, not on PlayerRemoving.
  - L9, before publishing: ⚠️ verify that serving `default.project.json` removes Dev scripts synced earlier, and add a hard place-id guard.
  - L10: set PlayerCharacterDestroyBehavior.
  - The movement guard must allow players standing up to about 2 studs off a wobble platform's original.
- Map audit (roblox-map-audit, per segment, spacing 1, ladder tops and bounce landings as extra starts, the final ledge as MustReach): **S1–S4 PASS, 0 FAIL**. Remaining WARNs are expected: floating platforms, the tops of the hatch ladders, and sightline warnings that are false alarms in per-segment runs.
- Connector walk-tests (server MoveTo of Holden's character): 2 ladders, 3 bounce pads and 4 hatch ladders all OK (some on the 2nd try).
- Checkpoint tests 9/9 PASS:
  - claiming, and soft platforms never becoming a respawn;
  - a fall 40 below sends you back in 0.12 s;
  - skipping pad 2 is allowed, and a lower pad doesn't move you down;
  - after a reset you respawn on your checkpoint;
  - the summit claims index 4.
  Also sent back while ragdolled: the ragdoll ends and you land upright. A reset no longer counts a false send-back (fixed).
- Ice friction applied 6/6, 14 local wobble copies, and the ragdoll self-test still 15/15. No errors in Output.
- **Holden's verdict: layout rejected** ("wider", "a whole world inside a square border with walls", "fantasy feel", "super enclosed").

## Decisions log
`USER:` = Holden decided. `PROPOSAL:` = Claude suggested, not approved.
- 2026-10-04 USER: build order from the kickoff prompt: phase 0 scaffold, then phase 1 (avatar ragdoll prototype, a bounce area, a flat test place), then stop for review. The phone test is required. Tunables go in Config. The map lives in the saved place, not git.
- 2026-10-04 USER: phase 0 is a light scaffold, lighter than [[Project-Bootstrap-Checklist]] (no data layer or analytics yet).
- 2026-10-04 USER: approved the phase 0 and 1 plan. Answers:
  - "you can make a new one" (project folder and repo). Claude made `C:\Users\holde\Documents\GameDev\RubberTower` with a local git repo and no GitHub remote.
  - Support **both R6 and R15**.
  - **16** players per server.
  - Fall ragdoll at **12 studs** with **1.5 s** recovery ("we can tune later").
  - Bounce pads are **launch only**. Other platforms and structures will have various effects, **for example ice that makes you slide a bit** (not built; future map work).
  - Holden will do the phone test himself.
  - **No luau-lsp** type checking.
- 2026-10-04 USER (phase 2):
  - Tower: a square or long cylinder, with the obby in the middle and on the walls.
  - About 2 soft platforms per segment.
  - Add the ice and wobble platforms now and review them later.
  - Default movement.
  - Then the critique: wider, a whole world inside a square border with walls, a fantasy feel, less enclosed; take notes from the chained-together obbies.
- 2026-10-04 USER (v2): a walled mystical valley; floating islands and crystals; size about 240×240×400 for now; use the existing trees and rocks and make new models if needed (Blender MCP available).
- 2026-10-04 PROPOSAL (v2, in use): segment themes meadow / mushroom grove / crystal-ice / cloud kingdom; each segment spirals a 62-stud ring plus one wall-terrace run; decor props don't collide; the 9-model art kit.
- 2026-10-04 PROPOSAL (in use, not answered):
  - a fall more than 12 studs below your checkpoint pad sends you back;
  - 3 checkpoints + the summit;
  - always respawn at your highest checkpoint;
  - checkpoints as full floors in v1 (open islands proposed for v2);
  - ice friction 0.01;
  - wobble spring stiffness 800;
  - tiers eased to 5-stud gaps and a 2.5-stud rise in segments 3–4 after the audit;
  - Lighting.Ambient raised to 140 in the place (it was too dark inside v1).
- 2026-10-04 PROPOSAL (implemented, Holden to confirm):
  - A fall is measured from the take-off height, not the top of the jump.
  - Landing on a bounce pad resets the take-off height, so a pad catches a fall.
  - A shove on an already-ragdolled player extends the ragdoll.
  - Every ragdoll ends after 8 s at most.
  - Draft numbers in Config: settle speed 4 studs/s, bounce 90 studs/s.

- 2026-10-05 USER: Squishies amounts (checkpoints 50/75/100/200, titles 25/75/150/300, daily 25/30/40/50/60/75/150, packs 99→400 / 249→1,100 / 499→2,500 as developer products, hat prices by rarity 30/75/175/400/900/2,250; Summit_Crown never sold).
- 2026-10-05 PROPOSAL → decided: grace day declined (USER: Restart); +20 Squishies for re-reaching the summit once per day accepted (USER). Bag bonus label corrected to +9% (real +9.3%).
- 2026-10-05 USER: 27 titles with rarity payouts (Common 25, Uncommon 75, Rare 75, Epic 150, Legendary 300, Mythic 300; all = 2,975), one equipped at a time via a Titles menu, cheatable unlocks server-checked (M1). Title above the head = BillboardGui UI, mockups first.
- 2026-10-05 USER: title style C Clean Text ~13% smaller; own title shows (smaller); Legendary stays 900; Claude writes the final title names/rarities/unlocks (done: Config `Titles`, [[Rubber-Tower]]).
- 2026-10-05 PROPOSAL: title UI LOD (full <25 studs, title 25–45, badge 45–70, hidden >70), declutter by overlap, own title 12% smaller, Adornee root + StudsOffsetWorldSpace for ragdoll; Legendary 1,200 if Legendary-on-day-2 feels too fast.
- 2026-10-05 USER (night): pay checkpoint Squishies + the +20 replay now (session-only, Output + dev panel).
  - **Squishmaster via a summit "Leap of Faith"** edge/launch pad (ragdoll fall to the ground floor, also counts for Full Send) and a soft landing zone.
  - A new run starts when you leave the ground floor. A run counts for Squishmaster and the +20 only if the server's climb trace saw it climbed with no teleport up (teleporting down is fine).
  - Other hooks stay one line.
  - Upload OK for the **private test place only** (kit a–h, 39 hats, 12 title icons); nothing public.
  - After review: plan (don't start) the map build, ground floor + S1.
- 2026-10-05 PROPOSAL (Claude, built as config, tune freely): ground floor = start-pad top + 15 studs; teleport-up = >35 studs rise per 10 Hz sample; test leap pad LaunchSpeed 60 at a 10° tilt.

## Open questions
- Should a ragdoll happen when the player dies (falling into the void or resetting)? Today the body just stays stiff. Not specified.
- Phase 3: knockback has to be applied by the target's client (or the server briefly takes ownership). Is a server fall-ragdoll cooldown wanted? (Reviewer M1.)
- The note conflicts listed in [[Rubber-Tower]] are still open.

## Traps (with the reason)
- **Test accessories in play, not Edit** (2026-10-05): Edit mode doesn't simulate. Hat wobble joints with world coordinates in `Position` looked fine until play flung the parts away.
- **Equip multi-part hats by pre-positioning every part, then parenting** (2026-10-05): WeldConstraints bake their offset when they become active.
- **Studio minimized = white `screen_capture` and ~15 FPS** (2026-10-05): restore the window (no focus steal: `ShowWindow(h, 4)`) before screenshots or FPS numbers.
- A standing Humanoid puts no weight on the floor, so a wobble platform won't tilt unless the client pushes it ([[Obby-Special-Platforms]]).
- Distance along the track isn't the real gap at corners. The builder measures real edge-to-edge gaps; the first build had a 7-stud corner gap.
- Deleting a synced folder while `rojo serve` runs crashed Rojo 7.7.0. Restart it; the plugin reconnects by itself in about 20 s.
- Teleporting a character into the air makes fall tests read short, because Freefall starts a few frames late. Walk off ledges to test the threshold.
- Studio MCP `execute_luau` times out at about 60 s. Spawn long tests with `task.spawn`, write progress to a workspace attribute, and poll it.
- `.gitignore` doesn't stop Rojo syncing dev files. The publishing `default.project.json` ignores `**/Dev*.luau`. Serve `dev.project.json` while testing.

## Skills used so far (with result)
- `roblox-game-manager`: set up this note.
- `roblox-dev:setup`: scaffold, adapted to the vault layout (`Main.*.luau`, `Services/`, `Controllers/`).
- `roblox-code-gate`: `GATE PASS` (scaffold and phase 1).
- `roblox-dev:roblox-reviewer`: no high-severity findings; fixes applied.
- Roblox Studio MCP: joint inspection, greybox build, playtests (quirks recorded in [[Roblox Studio MCP Quirks]]).

## Related
- [[Rubber-Tower]] · [[Rubber-Tower-Build-Plan]] · [[Rubber-Tower-GDD]] · [[Avatar-Ragdoll]] · [[Game-Building-Playbook]] · [[Roblox Game Manager Skill]]
