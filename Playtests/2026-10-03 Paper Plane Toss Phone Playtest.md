---
title: 2026-10-03 Paper Plane Toss Phone Playtest
date: 2026-10-03
tags: [playtest, mobile, roblox, ui, audio]
project: Paper Plane Toss
---
# Paper Plane Toss: first phone playtest (2026-10-03)

Holden published the game as a private experience and played on his iPhone (2532×1170, landscape). He recorded the screen for 2:23. Claude broke the video into frames every 1.5 s (see [[Video Frame Extraction with Blender]]) and reviewed it alongside Holden's own notes.

![[Phone Playtest HUD and Tutorial.jpg|700]]
*Fresh save: arrival, Jet's tutorial and the first throws on the phone.*

## Holden's notes
1. **The training pad gives no feedback** while you stand on it. Fix: you now bounce like a trampoline, with a boing sound.
2. **THROW! sits right where Roblox's mobile jump button is.** Fix: a touch layout (see [[Roblox Mobile UI Layout]]).
3. **The music is very loud**, even with the slider. Fix: the whole music mix is halved in `Config.Audio`.
4. **The arrival title needs more style.** Fix: a 3D logo rendered in Blender (see [[Blender 3D Logo Pipeline]]).

## What Claude found in the video
| Issue | Cause | Fix |
|---|---|---|
| Everything is tiny and the text is hard to read | The UI scales to a 1280×720 design, and a phone is about 844×390 points, so everything shrank to about 54% | Touch screens get a ×1.25 UI scale on top |
| The Roblox thumbstick covers PLANES | The bottom-left menu sits exactly where the thumbstick lives | On touch screens, PLANES / CHALLENGE move bottom-centre |
| World signs fill the screen up close (egg odds, Group Chest, rebirth pads) | A BillboardGui sized in studs keeps growing as the camera gets near | `DistanceLowerLimit` ≈ 20 studs on every world sign, and slightly smaller sizes |
| Plane-pedestal LOCKED tags pile on top of each other | 12 signs visible from 70 studs | Plane tags now show only within 45 studs |
| About 4.5 s of white screen at the end of the cutscene | The arrival flight path went straight through the plaza's paper-plane statue | The path swings round the statue (x ±7.8, z 41–59) |
| Your own VIP tag floats in front of the camera all the time, and is huge in the cutscene | The server-made BillboardGui is visible to its owner too | Hidden for the owner on the client; everyone else still sees it |
| The Golden Pad sign is cut by its posts and a lamp | StudsOffset was too low | Raised to 7.5 |

![[Phone Playtest Egg Signs.jpg|700]]
*Egg odds signs growing to fill the screen near the pedestals: the BillboardGui scaling problem.*

## Looked wrong but was fine
- **The tutorial hand near REBIRTH:** it points down at THROW! from above, and on the phone layout that happens to sit next to the menu column.
- **The "giant white wing" near the chest:** it's the plaza statue seen up close.

## Lessons
- **Test on a real phone early.** Studio's PC view hid every layout problem above.
- **World signs** should always get `DistanceLowerLimit` and a sensible `MaxDistance`.
- **Cutscene camera paths** must be checked against the real map geometry, not just the waypoints.

## Playtest 2 (same day, after the fixes)
![[Phone Playtest 2 HUD.png|700]]

| Holden's note | Fix |
|---|---|
| The trampoline boing plays too often | It now plays on every 3rd bounce (`Config.Training.boingEvery`) |
| The HUD is "all over the place" | The HUD layer ignores the notch safe area and keeps half of it as a margin, so the left stack and right column hug the edges (see [[Roblox Mobile UI Layout]]) |
| Right column too big and too far in | Gear, PETS, REBIRTH and SHOP are about 20% smaller, against the right edge |
| PLANES and AUTO should be bottom-left | PLANES, CHALLENGE and AUTO share one bottom-left row with smaller icons; BEST went back to bottom-centre |
| Title logo | Holden made a new one with Codex image generation (`art/ui/logo_codex.png`, `rbxassetid://132608766133278`). It replaced the Blender logo. |

![[Logo Codex v1.png|600]]

All of these are mobile-only; the PC layout is unchanged. After the next phone check Holden called it "almost perfect" and moved BEST to the top-centre. Last nitpick: PLANES / CHALLENGE still hit the thumbstick, so they moved to the top (right of BEST, smaller) and AUTO to the bottom-middle.

Related: [[Paper Plane Toss]], [[Paper Plane Toss UI Redesign]], [[Join Cutscene and Tutorial]], [[Roblox Audio Pipeline]]
