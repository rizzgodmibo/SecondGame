---
title: Video Frame Extraction with Blender
date: 2026-10-03
tags: [blender, video, reference, workaround]
---
# Video Frame Extraction with Blender

This PC has **no ffmpeg**, and Claude can't watch videos directly. Instead, load the video as a VSE movie strip in headless Blender and render stills at a set interval.

- **UI reference video:** 47 frames at about 6 fps through the menu section. These drove [[Paper Plane Toss UI Redesign]].
- **Steal an Egg tutorial video:** 22 frames, one every 2 s. These drove [[Join Cutscene and Tutorial]].

Both videos are saved in the vault: [[Ref UI Style Video.mp4]] and [[Ref Steal an Egg Tutorial Video.mp4]].

Go denser (several fps) when studying UI details, and sparser when you only need the flow of steps.

**Gotcha (phone recording, Oct 3):** set the render to the video's full size and lower `resolution_percentage` (e.g. 33). If you shrink `resolution_x/y` instead, the movie strip is not scaled and you only get a centre crop, losing the HUD at the screen edges. Tile frames into 3×4 contact sheets with numpy to review a whole playtest at once. Used for [[2026-10-03 Paper Plane Toss Phone Playtest]].

Related: [[Blender MCP Setup]]
