---
tags: [project/rubber-tower, prompting]
status: draft
updated: 2026-10-05
confidence: high
---
# Rubber Tower: slice fix-pass prompt (restart prompt)

## TL;DR
- On 2026-10-05 (~19:20 EDT) Holden **paused Rubber Tower**. When work starts again he will use the prompt below.
- It is a **fix pass on the map v3 slice only**:
  - water that "almost teleports" you out;
  - the Studio void showing at the edges;
  - ground that reads as random models.
- Places 3–6 stay untouched.
- **Before starting, check two things:**
  1. Holden must pick water option A or B; the prompt leaves it as a bracket.
  2. Either option changes the earlier USER water decision (float-back), so confirm that change with him.
- State at pause: [[Rubber-Tower-Build-Status]]. Map plan and slice record: [[Rubber-Tower-Map-Build-Plan]]. Model archive: AssetLibrary `models/rubber-tower-kit-v6-map/`.

## The prompt (Holden, verbatim, 2026-10-05)
> Fix pass on the current slice. Do not touch Places 3-6. Three problems from playtesting:
>
> 1. WATER: falling in almost teleports the player out. First find the cause (Touched handlers, kill parts, scripts setting position/velocity, Terrain vs part water, Humanoid state changes, anything shared with leaf launch) and report it BEFORE changing anything. Then implement: [A: swimmable water with clear exits / B: fail zone with splash VFX + sound + short fade + respawn at last checkpoint].
>
> 2. ENCLOSURE: the Studio void/horizon is visible. Delete stray greybox/baseplate parts, add a perimeter of tall cliffs above camera sightlines, a terrain skirt below the world, and invisible walls just inside the visual edge. Tune Sky/Atmosphere so the horizon blends (lower skybox half darker and close to terrain color).
>
> 3. GROUND: it reads as random models. Ground every prop (contact dirt/grass, foundations), blend materials (grass/dirt/stone with worn paths between landmarks), cluster props into purposeful small scenes with empty space between, add gentle elevation, shrink cobble scale, add fading ground clutter.
>
> Check each against Projects/Rubber-Tower/Rubber-Tower-Art-Style-Guide.md. Screenshot every fix from at least 3 angles, including fully zoomed out and from the highest point. Keep Rojo synced, do not commit, and list anything for me to delete in Explorer. Update Projects/Rubber-Tower/Rubber-Tower-Build-Status.md and Meta/Gap-Tracker.md in the vault.

## Notes for the session that runs it (Claude, 2026-10-05; not decisions)
- **Conflict: water design.**
  - The current water is Holden's own USER design from earlier on 2026-10-05: ragdoll, splash + bloop, a short bob, then a ~1 s glide back to the combo start, counted as a fall. See [[Rubber-Tower]] decisions.
  - Option A (swim) and option B (respawn at the last checkpoint) both replace it. B also sends the player much further back than the combo start.
  - Ask which option he wants, then record it as a new USER line.
- **Lead for the "teleport" cause (hypothesis, not checked).** The float-back is short by design: `Config.Water` has Bob 0.6 s and Return 1 s. The cause list he gave is still the checklist to run, and the report comes before any change. Files and settings to check:
  - `WaterController.luau`: zeroes every body velocity each frame during the glide;
  - `HazardService` + `RagdollService:HazardRagdoll`;
  - `Config.Water`;
  - the WaterReturn zones in `layout_b.py`;
  - the `WaterCatchFloor` at y −14;
  - the bounce/leaf code in `BounceController.luau`, for anything shared with the leaf launch.
- **Conflict: "Delete stray greybox/baseplate".** Studio deletions through MCP are blocked by Holden's rule.
  - List the exact instances for him to delete instead.
  - Candidates: the old S2–S4 greybox in the sky; `ServerStorage.Kit.Ground3` / `Ground3B`; `Workspace.TestPlace.DevSliceBot`.
  - Keep `TestPlace_LeapTest_parked` until the real Leap lane works (USER rule).
- **Check before building: "Terrain skirt".** Holden ruled out *terrain water*, not terrain ground. The art style guide still asks for crisp, flat-shaded zones, so a terrain skirt must be invisible from play height, or the perimeter cliffs must hide it.
- **Art style guide reminders:** crisp zone colours, no blurry gradients, no black crack lines, never repeat one rock model, and every model has colour variation.
- **How to rebuild the slice:**
  - `art/map/layout_b.py` → `LayoutB.luau`, then run `tools/BuildValleyB.luau` from a temp folder clone in Studio.
  - Rojo: `rojo serve dev.project.json` in the game repo. It was stopped at the pause.

## Related
- [[Rubber-Tower]] · [[Rubber-Tower-Build-Status]] · [[Rubber-Tower-Map-Build-Plan]] · [[Rubber-Tower-Art-Style-Guide]] · [[Obby-Special-Platforms]] · [[Rubber-Tower-Valley-Kit]]

## Sources
- Holden's chat message, 2026-10-05.
