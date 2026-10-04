---
title: Join Cutscene and Tutorial
date: 2026-10-03
tags: [roblox, cutscene, onboarding, story]
project: Paper Plane Toss
---
# Join Cutscene and Tutorial (Phase 7)

## Cutscene story (Holden's)
The player sits in class while bullies throw paper planes at them. A ninja, **Jet** (Holden picked the name), bursts in and knocks the bullies out with one plane. He invites the player to Sky Island, and they ride a giant paper plane there; the title card "+1 PAPER PLANE TOSS" pops up. It plays once on first join, has a Skip button, and saves `introSeen` (save v2).

- **Built with:** a Blender classroom set, catalog-outfit rigs, and a `Puppet` module that converts AnimationConstraint joints to Motor6D so poses can be set in code, so no animation uploads were needed.
- **Fixes from Holden's review:**
  - Characters standing up looked robotic. The player now sits in the **front** row and the bullies in the **back** row, so nobody has to stand.
  - The seat markers didn't move the first time because Studio was in play mode, so the bullies threw backwards.
- **Later:** a sound effects pass and outfit swaps.

![[Render Classroom Front.png|350]] ![[Cutscene Bullies Throwing Backwards.webp|400]]
*Left: the classroom set render. Right: Holden's screenshot of the backwards-throwing bug.*

## Tutorial (Steal an Egg style)
Holden's video of Steal an Egg's tutorial was broken into frames. The takeaway: no menus, chunky red arrows on the ground and a bobbing cartoon hand; you learn by doing.

1. Throw (hand on THROW!)
2. Stand on the training pad for about 5 s (arrow trail)
3. Throw again; Jet gifts **75 Tokens**
4. Buy the Notebook plane (arrow trail to its pedestal)
5. Done

Steps are tracked on the server and saved (`tutorialStep`, save v3). There's no skip. The `client/Guide` module is reusable for later hints.

Reference video: ![[Ref Steal an Egg Tutorial Video.mp4]]
Ground arrow model: ![[Render Guide Arrow.png|200]]

## Cast outfits (release prep, 2026-10-03)
- **The Coach is now SENSEI** (Holden). Only the player-facing text changed; the model is still `Lobby.Coach`. Outfit: white karate gi, rice hat, full white beard, and Roblox's "Old Timer" dynamic head (big brows, round glasses).
  ![[Sensei Outfit.jpg|400]]
- **The bullies now have names** (generic, Holden's call): **KYLE** (red hoodie, backwards cap), **BRAD** (jacket, sunglasses, brown spiky hair) and **TYLER** (varsity jacket, blonde spiky hair).
- **Each bully gets a close-up** with their own portrait and name tag on their line, then the shot cuts back wide for the throw. Before, all three lines showed Bully1's portrait.
  ![[Cutscene Kyle Closeup.jpg|400]]
- **Avoided:** "Sensei Wu" catalog items. They're LEGO Ninjago-based and turned his head yellow.
- **Gotchas:**
  - The rigs have dynamic heads, so `HumanoidDescription.Face` (classic face decals) does nothing. Change `Head` to a dynamic head instead.
  - `ApplyDescription` leaves the old accessories on these rigs; remove them by name.
  - It also un-anchors the new head and accessory handles; re-anchor them on anchored NPCs.
  - Roblox shows a Humanoid NPC's model name above its head ("Coach" over Sensei). Set `Humanoid.DisplayDistanceType = None` on every NPC.
  - The catalog's item names don't always match the look, and Studio can show the wrong classic-shirt texture until it loads. Check in a play test.

Related: [[Paper Plane Toss]], [[Paper Plane Toss UI Redesign]], [[Paper Plane Toss Release Prep]]
