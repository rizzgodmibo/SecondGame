---
tags: [playtest, project/trap-your-friends, visuals/retro, systems/destruction]
status: draft
updated: 2026-10-05
confidence: medium
---
# Trap Your Friends: style test v1, direction A (Studio, 2026-10-05)

## TL;DR
- Built the phase 1 style test in `TrapYourFriends\places\StyleTest.rbxl` (a Team Create place, placeId 79250742543087): **direction A only**, two copies of one 12 × 35 segment side by side, **Legacy** (`SurfaceType` Studs/Inlet) and **Variant** (our own `TYF_Studs` MaterialVariant), with six traps, the destruction prototype and two walking noobs. **Awaiting Holden's review; nothing is locked.**
- **Counts:** 494 visible parts per copy (988 in total), 479 of them breakable cells per copy, plus 12 invisible waypoints per copy. Client debris: peak **200 of the 200-part pool** (the cap held), 54–176 alive at a time with both noobs looping. Each hit stayed at or under 40 cubes by design (DebrisPlan; specs pass).
- **Frame time, Studio on Holden's PC only:** client 16.7 ms average (Studio's 60 fps cap), 18–22 ms worst frame per second. Server heartbeat 0.01–0.15 ms, physics 0.02–0.15 ms, about 10 kbps sent. **Not measured on a phone**: Holden tests on his phone himself.
- **Biggest findings:** the Spinner Bar keeps re-carving the Brick Wall (a hole in its bottom two rows is always there), MaterialVariant studs also cover side faces, and TNT vs Kill Brick only separate by the white bands and shape (see "Holden to judge").
- 24 Lune specs and the code gate pass. No errors or warnings in Output across the session.

## What was built (all classic primitives on the 1-stud grid, markings from parts, no decals)
| Piece | Spec in the test |
|---|---|
| Lane | Floor top at Y 10, floating over the baseplate (classic obby look), trusses at the side to climb back up. 1 × 1.2 × 1 floor cells: Medium stone grey, about 10% Light stone grey, Dark stone grey edges, black/white checker finish, Bright green start pad (SpawnLocation) |
| Disappearing Plate | 12 × 3 plate cells (0.4 tall) over a pit; Cool yellow with a dashed Bright yellow outline. Flickers 0.6 s, crumbles into debris, back after 3 s |
| Brick Wall | 10 × 5 bricks (gap of 2 on one side). Nougat / Brick yellow 2-stud running bond; cracks are diagonal staircases of Reddish brown cells. **v1 cracks were vertical runs that read as stripes and were recoloured to diagonals before the screenshots** |
| Spinner Bar | Dark grey hub, Bright orange bar 11 long at 1.6 above the floor, Neon orange tips; one turn per 3 s. Smashes wall cells it passes through and knocks runners back (maths shared by server and client, no physics collisions) |
| Bounce Pad | Dark grey base, grey spring, Hot pink pad and dome. Launch 80 studs/s up (the noob rose about 6 studs in a sampled bounce) |
| TNT Brick | 3 × 2.4 × 3 **Bright red** body, two white bands, black fuse, Neon New Yeller spark. 1.5 s fuse → 3 × 3 floor-cell hole, 8-stud knockback, flash, dust, small shake; rebuilds after 6 s |
| Kill Brick | 4 × 1 **Really red** bricks with a gentle client-side pulse. Kills: players reset to the segment start; the noob **shatters into 1-stud cubes (demo only, still UNDECIDED in the GDD)**; the brick itself shatters and rebuilds |
| Noob | R6 from a `HumanoidDescription` with body colours only (Bright yellow head and arms, Bright blue torso, Br. yellowish green legs), walks 12 waypoints per lane and respawns 3 s after a shatter or fall |
| Lighting | Direction A preset module (`src/shared/Lighting/ModernRetro.luau`): Realistic, ClockTime 13.5, Brightness 3, light Atmosphere, Bloom 0.5, Saturation +0.15, SunRays 0.05, DepthOfField disabled. Every property applied (nothing skipped) |

## Observed in the playtest (play solo, 2026-10-05)
- The noobs completed the loop: plate → wall gap → spinner zone → bounce (Y 13 → 18.9) → TNT → Kill Brick → shatter → respawn about 3 s later.
- In 6 s, with both noobs looping, 130 cells broke: plates 36 + 36, walls 18 + 18, kill bricks 4 + 4, one TNT (5 parts) and its 9 floor cells.
- **The spinner never lets the wall heal.** Wall cells rebuild after 6 s and get hit again on the next pass (3 s per turn), so 36 wall cells stayed hidden even with the noobs switched off. In the close-ups the wall looks like it stands on legs. Design options for Holden: a longer rebuild for spinner hits, a higher bar, or moving the wall out of the sweep.
- Server: 0 unanchored parts outside characters; the debris folder exists only on clients. Phase 1 has **no client → server remotes**.
- Studio-on-PC frame numbers above. At 844 × 390 the Legacy studs still read; Variant studs blur to faint circles at distance.

## Screenshots (`Projects/Trap-Your-Friends/attachments/`)
Angles 1–3 are the requested three angles for direction A; 10 is the phone-size view.
- `tyf-style-a-01-overview.jpg`: high overview of both copies. Variant is on the left and Legacy on the right because the camera faces +Z. The Legacy noob is mid-shatter.
- `tyf-style-a-02-runner-legacy.jpg`: runner's eye down the Legacy lane (the plate had just crumbled).
- `tyf-style-a-03-runner-variant.jpg`: runner's eye down the Variant lane, with the spinner mid-smash on the wall.
- `tyf-style-a-04-tnt-vs-killbrick.jpg`: TNT next to the Kill Brick (Legacy).
- `tyf-style-a-05-tnt-blast-frozen.jpg`: TNT blast frozen 0.28 s after detonation.
- `tyf-style-a-06-noob-shatter-frozen.jpg`: noob + Kill Brick shatter frozen 0.22 s in.
- `tyf-style-a-07-closeup-legacy.jpg` / `tyf-style-a-08-closeup-variant.jpg`: matched close-ups of the two stud methods.
- `tyf-style-a-09-follow-cam-source.jpg` → `tyf-style-a-10-phone-844x390.png`: a follow-camera framing cropped to the phone aspect and **downscaled to 844 × 390**. This is a size check only: it is not a device emulator or a real phone.
- `tyf-stud-tile-preview.png`: our stud tile (4 × 4, tinted Bright red).

![[tyf-style-a-01-overview.jpg]]
![[tyf-style-a-07-closeup-legacy.jpg]]
![[tyf-style-a-08-closeup-variant.jpg]]
![[tyf-style-a-05-tnt-blast-frozen.jpg]]
![[tyf-style-a-06-noob-shatter-frozen.jpg]]
![[tyf-style-a-10-phone-844x390.png]]

## Holden to judge (Claude's honest read, not decisions)
- **Stud method.** Legacy gives crisp squared classic studs on tops only, so wall faces are smooth and walls look flat. Variant gives round, chunky studs on **every face** (walls look like LEGO on its side), which reads "toy brick" more than "2008 Roblox", and it blurs at distance. Variant costs one texture pair; Legacy is free.
- **TNT vs Kill Brick.** Up close, the bands, fuse and cube shape separate them. From the overview both read as "red block". A non-red TNT body would remove the risk entirely (Holden's call).
- **Weak spots:** the wall pattern is still busy (two tans + cracks), the 10% light-grey floor speckle reads as glare in places, and the template baseplate grid is still visible below. The noob shatter and the TNT blast read well.
- The JJS-style debris feel works with 1 cube per cell + up to 2 chips. Debris doesn't collide with characters (collision groups).

## Studio instances added (for Holden; deletions are his)
- `Workspace.StyleTest` (Legacy + Variant segment models) and `MaterialService.TYF_Studs`.
- Collision groups `TYF_Debris` and `TYF_Characters`. Lighting properties changed, plus Atmosphere/Bloom/ColorCorrection/SunRays tuned; DepthOfField disabled (not deleted).
- **Parked, delete if unwanted:** `ServerStorage.SpawnLocation` (the template's spawn, disabled and moved out of the shots).
- Runtime only (not saved): `Workspace.TYF_Noobs`, `ReplicatedStorage.Remotes`, the client `Workspace.TYF_ClientDebris` pool.

## Pitfalls found
- `MaterialVariant.Pattern` doesn't exist in this Studio build: the builder errored once (before building anything) and now sets `MaterialPattern` inside a pcall.
- In play mode, `screen_capture`'s camera parameters lose to the follow camera. Set `CurrentCamera.CameraType = Scriptable` and the CFrame from a Client `execute_luau` first, then capture with no camera parameters.
- `screen_capture` saves every image under `~/.claude/projects/<project>/<session>/tool-results/`, so captures can be copied into the vault.
- Studio must be in front, or captures come back white (bring it forward with `SetForegroundWindow`).

## Related
[[Trap-Your-Friends]] · [[Trap-Your-Friends-Art-Style-Guide]] · [[Trap-Your-Friends-GDD]] · [[Retro-Stud-Style-Guide]] · [[Roblox Studio MCP Quirks]] · [[Roblox Code Gate Skill]]

## Sources
- Local Studio playtest by Claude Code, 2026-10-05 (MCP `execute_luau` stats, `get_console_output`, `screen_capture`). Code: `C:\Users\holde\Documents\GameDev\TrapYourFriends` (uncommitted).
