---
tags: [project/trap-your-friends, visuals/art-direction, systems/destruction, plan]
status: draft
updated: 2026-10-06
confidence: medium
---
# Trap Your Friends: Style Test v2 Plan, rev 2 (AWAITING HOLDEN'S OK)

## TL;DR
- Rev 2 (2026-10-06) follows Holden's "approved with changes":
  - the game is now Trappers vs Runners ([[Trap-Your-Friends-Round-Structure]]);
  - v2 is a **vertical slice of Map 1 (Castle Sky Island)**, not two team lanes;
  - **trap sockets** on the route, with the 12 traps sitting in them;
  - Legacy vs MaterialVariant stays as **two halves of the island**.
- New in rev 2:
  - original SFX (9 sounds), our own **painted skybox**;
  - a Studio-only **trapper panel** (live-trigger Hammer, Boxing Glove, TNT; with the first real client → server remote, fully validated);
  - [[Trap-Your-Friends-Map-Plan]] for Maps 2 and 3 (written, plan only).
- Unchanged from rev 1: the JJS destruction rework (cut around the hit, 1-stud minimum pieces, lingering mixed-size debris, impact VFX + local hit-stop, rebuild only when clear), black Highlight outlines + a SelectionBox test, and the environment and lighting quality fixes.
- v1 code is committed (`411d4d4 Style test v1`, the only commit Claude may make).

## 1. The slice: Map 1, Castle Sky Island
**Route (about 95 studs long, Runners go +Z):**
| Stretch | z (studs) | Width | Sockets on it |
|---|---|---|---|
| Gatehouse start room (towers, battlements, portcullis arch, banners); Runners wait here in the real game | −14 … 0 | 16 | none |
| Stone causeway over the moat | 0 … 30 | 12 | **lane-wide** ×1, floor 2×2 ×2, ceiling (arch gantry) ×1 |
| Courtyard (wider, a planter shortcut on one side) | 30 … 62 | 20 | floor 4×4 ×3, floor 2×2 ×2, wall ×2 (courtyard walls), ceiling (gantry) ×1 |
| Wall-walk ramp up towards the finish tower | 62 … 80 | 10 | floor 2×2 ×2, wall ×1 |
| Finish-tower base (the tower itself in view, the top not built) | 80 … 92 | 12 | none |
- **15 sockets, 12 filled, 3 left empty** so the socket markers can be judged. Sockets are marked with a dashed outline (our texture) and a type label, shown in the test (togglable: in the real game only Trappers see them during prep).
- **Socket types:** floor 2×2, floor 4×4, wall, lane-wide (Holden's list), **plus ceiling (gantry)** for the Swinging Hammer and Wrecking Ball. Ceiling is in the Round Structure note's socket list, but **not in Holden's v2 list: Holden to confirm**.
- **Stud halves:** the island and the route are split down the route's centre line: **left half legacy studs, right half our MaterialVariant**, with a 1-stud dark trim stripe on the seam. Both methods are in every shot, as in v1. (Alternative if Holden prefers: split along the route, so the first half is legacy and the second half is Variant.)
- **Environment:**
  - a grass/dirt sky island (3-tone greens and browns, big plates to keep the part count low) and a moat (part water);
  - edge trim, lamp posts, flags, crates and barrels, a fence, 3–4 varied classic block trees, distant floating islands;
  - the template baseplate parked out of view.
- **Sky:** our **own painted 6-face skybox** (see 5) + dynamic `Clouds` if it helps.
- **Lighting:** new direction A pass (afternoon, warm sun, softer shadows, light warm haze, Bloom ~0.4, Saturation +0.15, Contrast +0.1). The v1 preset is kept as its own module.
- **Colour:** floors/ground 3 tones (±5–8%, DRAFT exception now in the style guide), walls 2 tones max, no speckle.

## 2. The 12 traps in sockets (8 families)
| Trap | Family | Socket | Mode in the test |
|---|---|---|---|
| Glass Floor | Explosives/destruction | Lane-wide (causeway) | Passive: cracks on step 1–2, shatters on step 3 |
| Swinging Hammer (angry face) | Movers | Ceiling (causeway arch) | **Triggered** from the trapper panel; idle sway otherwise |
| Spike Pop (face) | Classic hazards | Floor 2×2 (causeway) | Passive: proximity, 0.5 s tell |
| Bounce Pad (mushroom with eyes) | Launchers | Floor 2×2 (causeway) | Passive |
| Trapdoor (googly eyes) | Floor tricks | Floor 4×4 (courtyard) | Passive: step → 0.4 s wobble → flips |
| Glue Plate (slime with eyes) | Sticky | Floor 4×4 (courtyard) | Passive: WalkSpeed ×0.3 (server-set) |
| Brick Wall (calm 2-tone running bond) | Explosives/destruction | Floor 4×4 (courtyard) | Breakable; in the Wrecking Ball's path |
| Wrecking Ball (grin) | Movers | Ceiling (courtyard gantry) | Passive swing through the Brick Wall: the destruction showcase |
| Boxing Glove Wall | Launchers | Wall (courtyard) | **Triggered** from the trapper panel; idle wiggle |
| Chomper (teeth, chewing idle) | Creatures | Floor 2×2 (courtyard) | Passive: bites within 3 studs, 0.4 s open-mouth tell |
| TNT Brick (eyes, our hazard-stripe bands) | Explosives | Floor 2×2 (wall-walk) | **Triggered** from the panel; also lit by touch |
| Dodgeball Turret (eyes) | Projectiles | Wall (wall-walk) | Passive timer; bouncy balls, knockback only |
- Every trap gets a face/eyes, an idle animation, a tell → wind-up → hit → recover, a big hit (VFX + SFX + shake), and a black Highlight.
- Catches (Spike Pop, Chomper, moat fall): players reset to the slice start. The **noob shatters (demo only; still UNDECIDED)**. Two noobs walk the route on a loop.

## 3. Trapper panel (Studio-only prototype of live triggering)
- `DevTrapperPanel.client.luau`: a small panel with 3 buttons (Hammer, Glove, TNT), each with a cooldown ring.
- Press → client sends **intent only**: `TriggerTrap(trapId)`. This is the first client → server remote, built to the security rules:
  - a rate limit per player;
  - type checks on every argument;
  - the trap exists, has a "Triggered" mode and is armed;
  - the server-side cooldown is over;
  - the player is a Trapper. In Studio the dev script marks Holden as Trapper; the real round system comes later.
- On a valid request the server starts the **0.4 s tell** (glow + shake + tell sound) and then fires. The cooldown (DRAFT 4 s Hammer, 3 s Glove, 8 s TNT incl. rebuild) is in Config.

## 4. Original SFX (9 sounds)
- **Sounds:** bonk, crunch, glass, spring, chomp, whoosh, explosion, trap tell, catch sting.
- **Sources (both allowed by Holden):**
  - **(a) our own procedural synthesis:** `art/sfx/make_sfx.py`, numpy DSP (damped sines, filtered noise, pitch sweeps), 2 variants per sound;
  - **(b) free licensed Creator Store audio:** found with the Studio MCP asset search; used by id, no upload.
  - Nothing ripped, no commercial audio. Note: the sound skill says "no AI-generated tracks". Procedural DSP code isn't an AI audio model, and Holden explicitly allowed synthesis.
- **Checks:** the roblox-sound-library soundcheck on every candidate (lead silence ≤ 50 ms, clipping, quiet, format/size/length), normalised to the catalogue SFX target.
- **Picking:** Claude can't listen. I'll wire one candidate per sound by measurement and Holden picks by ear later; the alternates stay as local files.
- **Upload:** private, OGG, ⚠️ within the 100 uploads / 30 days quota (catalogue upload log). **Problem:** `AssetLibrary/.secrets/roblox_open_cloud_key.txt` is **missing**, so `upload_audio.sh` can't run. Holden to choose: add a user-owned Open Cloud key (Assets write), import the OGGs himself in Studio's Asset Manager, or Creator Store sounds only.
- **Record:** every sound + source + id goes in a new vault note `Trap-Your-Friends-Sound-List` and the AssetLibrary audio catalogue.
- **Playback:** client-side, with ±5–10% pitch variance and a per-sound cooldown ([[Sound-Design]]); SFX bus volume.

## 5. Our own images (private uploads, approved categories)
- **Skybox (6 faces, 1024², `art/sky/make_skybox.py`):** rendered from one 3D sky so all the seams match:
  - a bright gradient;
  - stylised flat-shaded puffy cumulus with soft cel edges;
  - a **sea of clouds below the horizon** (sky island);
  - a soft sun glow.
  - A preview contact sheet goes in the vault before upload.
- **Textures (`art/textures/make_textures.py`):** hazard stripes, glass cracks (light, heavy), impact streak, dust puff, banner emblem, socket marker (dashed outline).
- **13 images in total.** Ids go in the hub.

## 5b. JJS destruction rework (same as rev 1)
- **Server:** cuts only around the hit (layered split along whole-stud lines, so studs stay aligned). The anchored remainder keeps the wall standing with a jagged hole.
- **Clients:** removed boxes become mixed slabs (0.5–3 studs) + chips that land and linger about **10 s** (less on low graphics quality, ⚠️ verify the quality read), with an oldest-first recycling pool (start cap 250, then measure).
- **Impact VFX:** flash, streaks, dust, shake, FOV punch, a 60 ms local hit-stop.
- **Rebuild:** 10 s after the last hit, and only with nobody within 10 studs.
- **References:** VoxBreaker and VoxelDestruct, read and audited in a vault note; **nothing installed**.

## 5c. Outlines (same as rev 1)
- A black `Highlight` per trap, noob and hero prop (budget about 25: 12 traps + 2 noobs + ~10 props).
- A client-side toggle for black `SelectionBox` edges on the left (legacy) half's route bricks, screenshotted on and off.

## 6. File list (rev 2)
**Code (`C:\Users\holde\Documents\GameDev\TrapYourFriends`; no more commits after `411d4d4`):**
- `src/shared/`:
  - `Config.luau` (v2 numbers), `Tags.luau`, `Remotes.luau` (Fractured, Rebuilt, TrapFx, Shatter, **TriggerTrap**);
  - `Traps/TrapDefs.luau` (data per trap incl. socket type, mode, cooldown);
  - `Audio/Sfx.luau` (ids + pitch/cooldown helper);
  - `Lighting/ModernRetro.luau` (v2) + `ModernRetroV1.luau` + `Apply.luau`.
- `src/shared/Rules/` (pure, Lune-tested): `Fracture`, `Pendulum`, `TrapCycle`, `Projectile`, `DebrisPlan`, `RebuildTimers`, **`Sockets`** (does a trap fit a socket type), **`RateLimit`** (token bucket).
- `src/server/Services/`: `DestructionService` (rewrite), `TrapService` (rewrite: sockets → traps, modes, **TriggerTrap validation**). `src/server/Traps/`: 12 small trap modules. `src/server/Util/Characters.luau`.
- `src/client/Controllers/`: `DebrisController` (rewrite), `ImpactFxController`, `TrapAnimController`, `TrapLocalController`, `OutlineController`, **`SfxController`**.
- Dev-only (gitignored): `src/server/DevStyleTest.server.luau` (noobs, dev commands, marks Holden as Trapper in Studio), `src/client/DevHud.client.luau`, **`src/client/DevTrapperPanel.client.luau`**.
- `tools/StyleTestV2/`: `Build.luau`, `Kit.luau`, `Environment.luau`, `Route.luau` (route + sockets), `Traps.luau`.
- `art/`: `textures/make_textures.py`, **`sky/make_skybox.py`**, **`sfx/make_sfx.py`** (+ generated files).
- `tests/`: specs for every Rules module (`Fracture`, `Pendulum`, `TrapCycle`, `Projectile`, `DebrisPlan`, `RebuildTimers`, `Sockets`, `RateLimit`).

**Place:** `Workspace.StyleTest` (v1) → parked as `ServerStorage.StyleTestV1`. New `Workspace.StyleTestV2` (the Map 1 slice).

**Vault:**
- [[Trap-Your-Friends-Map-Plan]] (done);
- `Trap-Your-Friends-Sound-List`, a VoxBreaker/VoxelDestruct audit note, a v2 playtest log, screenshots + skybox preview in `attachments/`;
- updates to the hub, style guide, Studio MCP quirks, Gap-Tracker and Verification-Log.

## 7. Gate for v2 (before Claude reports)
- Code gate PASS.
- The slice builds; all 12 traps run in their sockets; both noobs loop.
- The trapper panel fires the 3 traps with tell + cooldown. A forged or spammed `TriggerTrap` is rejected (tested from the client with bad args and rapid calls).
- Destruction demo on the Wrecking Ball, TNT and Brick Wall works.
- Sounds pass soundcheck; skybox seams checked.
- **Measured:** parts, live/peak debris vs cap, Highlight count, frame time (Studio PC only), server heartbeat.
- **Screenshots:** overview, close-ups (both halves, SelectionBox on/off), frozen Wrecking Ball/TNT destruction, a trap close-up sheet, the panel, phone-size view.
- Honest critique.

## Open questions (Holden)
1. **Audio upload route:** add a user-owned Open Cloud key to `AssetLibrary/.secrets/` (Assets read+write), or import the 9 OGGs yourself in Studio's Asset Manager, or Creator Store sounds only?
2. **Ceiling (gantry) sockets** for the Hammer and Wrecking Ball: OK to add to the socket types?
3. **Stud halves:** left/right down the route centre (recommended), or first half / second half along the route?

## Related
[[Trap-Your-Friends]] · [[Trap-Your-Friends-Round-Structure]] · [[Trap-Your-Friends-Map-Plan]] · [[Trap-Your-Friends-Style-Test-v1-Feedback]] · [[Trap-Your-Friends-Trap-Catalogue]] · [[Trap-Your-Friends-Art-Style-Guide]] · [[2026-10-05-Trap-Your-Friends-Style-Test]] · [[Sound-Design]]
