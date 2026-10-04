---
title: Paper Plane Toss UI Redesign
date: 2026-10-03
tags: [roblox, ui, design, critique]
project: Paper Plane Toss
---
# Paper Plane Toss UI Redesign

## What went wrong
The first in-game UI was built from Roblox primitives: gradient frames with thin outlines. Holden: "you got lazy with the ui", too dark, boxed icons, bad spacing.

![[UI First Build Rejected.webp|450]]

**Lesson:** high-quality Roblox UIs use **painted image assets** (9-slice frames, buttons, pills, cards), not primitives. Figma mockups alone didn't fix this.

## Process that worked
1. Pull frames from Holden's reference video (about 6 fps through the menu) using Blender, because there's no ffmpeg. See [[Video Frame Extraction with Blender]].
2. Redesign in a **Claude Design canvas**: https://claude.ai/artifact/LmsZwKGxVNg5UzYMhDhNX7. Boards: HUD, Planes, Dialogue, ChallengeList, Invite, Kit.
3. Holden's notes: raise the dialogue box and use bigger, shorter lines; put the shine *behind* the reward text; THROW! in **Luckiest Guy** with the plane inside the circle; declutter the shop; split the challenge screens; keep strong outlines only on primary actions.
4. **v2 chosen** (canvas Version 7). v1 and v2 are saved in `SecondGame/design/` and in `AssetLibrary/ui-designs/candy-shop-ui/` for future games.
5. Render each piece with headless Chrome (`art/uikit/gen.sh`), upload, and record the ids and slice rects in `UIAssets.Kit`. Only the text is live (Fredoka One).

Reference video: ![[Ref UI Style Video.mp4]]

Design v1 boards, before Holden's notes:

![[Design v1 HUD.png|380]] ![[Design v1 Planes Shop.png|380]]
![[Design v1 Coach Dialogue.png|380]] ![[Design v1 Challenge Invite.png|380]]

## Style rules taken from the video
- Frameless big 3D icons with outlined labels.
- Cream pills with plum borders; a round glowing main button.
- Magenta frames with gold bolts; header art breaking out of the frame.
- Cream text with a thick plum outline.
- Each layer is its own ScreenGui; popups always draw on top.

## Later tweaks
![[Dialogue Box Too Big.png|350]]

The dialogue box was too big twice. Final: scale 0.78, centred at 70% down the screen, text size 30.

2026-10-04: the shop was reworked in a blind-critic trial ([[Shop Gauntlet Workbench]]). It also found that every panel's right and
bottom border was being cut off because the kit images are stored at max 1024 px; `UIKit.storedSlice` fixes this (uncommitted).

Related: [[Paper Plane Toss]], [[Art Direction Feedback]]
