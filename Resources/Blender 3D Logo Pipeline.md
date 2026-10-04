---
title: Blender 3D Logo Pipeline
date: 2026-10-03
tags: [blender, logo, ui, art, how-to]
source: codex
---
# Blender 3D Logo Pipeline

How the "+1 Paper Plane Toss" logo is made (`art/make_logo.py`, headless Blender). It's chunky 3D lettering like the big Roblox sim logos Holden sent (Project Slayers style), built in Blender rather than with AI image tools.

![[Render Logo v2.png|700]]

Not used in game any more: Holden replaced it with a Codex-generated logo (see [[Paper Plane Toss]]). v2 (uploaded as `rbxassetid://126534297266290`): badge tucked onto the "P", planes hugging the words, clouds behind the TOSS corners. v1 had the props floating loose around the edges, and Holden asked for them tighter.

## Recipe
1. **Letters:** a text curve with a TTF font (here Impact, `C:\Windows\Fonts\impact.ttf`). Settings: `extrude` 0.32, `bevel_depth` 0.035. Convert it to a mesh.
2. **Clean the font mesh:** remove doubles, triangulate, and recalc normals. Without this, flipped faces show through.
3. **Tip the letters back about 12°** so the extruded depth shows under them.
4. **Two materials per word:**
   - Faces pointing at the camera get a top-to-bottom gradient: Texture Coordinate (Object) → Separate XYZ → Map Range → ColorRamp, plus a little emission.
   - Every other face gets a darker side colour.
   - **For text, "up" is local Y,** because the text lives in its own XY plane. Using Z gives a flat colour.
5. **Props:** a starburst "+1" badge, paper planes on dotted trails, and puffy clouds with a gradient.
6. **Render:** orthographic, transparent film, 2048×1024.
7. **Outline:** one even dark outline round the whole logo, done as a 2D post-process in Blender's Python:
   - grow the alpha by about 16 px with a disc-shaped max filter in numpy;
   - fill the grown area with the outline colour;
   - lay the render on top.

## Don't
- **Inverted-hull outlines (solidify + flipped normals) on text.** Font meshes aren't watertight, so the dark hull pokes through the letters as slivers. Hulls are fine on simple solid props (pets, icons).
- **Judging a transparent PNG in an image viewer** that shows the hidden RGB of transparent pixels. Composite it onto a sky colour for previews (`art/preview_logo.png`).

Related: [[Blender to Roblox Asset Pipeline]], [[Art Direction Feedback]], [[Paper Plane Toss UI Redesign]]

## Using it in game
- **Check transparency with numbers, not eyes:** load the PNG in Blender's Python and read the alpha of the corners and edges (all 0 = no background box). The v2 logo is about 59% fully transparent pixels.
- **Size it in the UI's design space,** not as a fraction of the screen. Paper Plane's intro layer is 1280×720 design px, but with the phone ×1.25 boost a phone only has about 575 px of height. `Position = fromScale(0.5, 0.3)` with a 410 px tall logo pushed the top plane off screen. Pinning it by offset (centre 196 px down, 720×360) keeps it fully visible on both.

## 2026-10-03 approved title redesign

Holden rejected the attached earlier title and requested a more polished transparent title for the sky reveal, using Project Slayers references and broader Roblox branding research. His latest requested name is **Paper Plane Toss**, so this candidate omits the older +1 badge. Holden explicitly approved this logo in chat: "love that logo".

![[Paper Plane Toss Title v3.png|700]]

- Reviewed sampled frames from Holden's seven-second recording, `C:\Users\holde\Videos\2026-10-03 17-36-43.mp4`. The title appears over pale sky and also over the colorful island, so edge contrast matters in both situations.
- Art critique: the earlier title had rigid lettering, separated rows, detached ornaments, and a competing +1 badge. The candidate uses tightly arranged sculpted lettering, gold/amber above cyan/cobalt, one folded plane, and a curved flight trail.
- This candidate was made with the built-in image_gen tool, not the Blender procedure above. The historical Blender instructions and existing uploaded v2 remain intact. No game code or Studio assets were changed.
- Workspace deliverable: `C:\Users\holde\Downloads\SecondGame\art\title_research\Paper Plane Toss Title v3 Final.png`. Full initial prompt: `art/title_research/Title generation prompt.md`. A second edit requested transparent padding and cleaner outer edges while retaining the design.
- Transparency verified numerically from the PNG alpha channel; the final canvas borders are fully transparent. The first candidate's plane touched the right edge, which prompted the framing revision.
- Approved by Holden. The earlier concern about cloud trim is retained as an art-review observation, not a pending approval. Subsequent integration is recorded in [[Paper Plane Toss]] and confirmed by `src/shared/UIAssets.luau`: `rbxassetid://132608766133278`, using `art/ui/logo_codex.png`. The initial generation task itself did not perform that integration.
- Reference lessons are visual interpretation: Project Slayers for beveled depth and integrated motifs; Blox Fruits for title/icon cohesion; Blade Ball for a motion sweep; simulator branding for broad readable faces; Adopt Me for clarity and simple silhouette. No external logo assets were copied into the output.

Related: [[Paper Plane Toss]], [[Join Cutscene and Tutorial]], [[Paper Plane Toss UI Redesign]], [[Art Direction Feedback]], [[2026-10-03 Paper Plane Toss Phone Playtest]], [[Video Frame Extraction with Blender]].

## Lessons confirmed by Holden's approval

- Tightly composed sculpted lettering, strong gold/cyan color separation, one integrated paper plane and a sweeping flight motif succeeded where rigid Impact lettering and detached ornaments did not.
- Dark contours plus a fine light keyline help the title separate from both pale sky and a busy island. Use real alpha transparency; do not confuse an image viewer's backdrop with saved pixels.
- Inspect PNG alpha numerically and check every border. The first image clipped its plane at the right edge; the targeted padding edit corrected it. Final title: 1862×845, all border alpha values zero, approximately 42.36% fully transparent pixels.
- Use reference research for composition and polish, then validate against the actual reveal footage. Clearly distinguish viewed imagery from videos merely found in search.
- User approval of this title is not blanket approval for all similarly glossy art. Holden later requested a more literal Roblox gameplay style for the square icon; see [[Paper Plane Toss Thumbnails and Game Icon]].

## Redesign sources

- User-provided previous title: `C:\Users\holde\Downloads\image-1791063295476.png`.
- User-provided Project Slayers 2 logo references attached in this chat.
- User-provided reveal recording: `C:\Users\holde\Videos\2026-10-03 17-36-43.mp4` (sampled frames inspected).
- [Blox Fruits logo reference](https://www.pngaaa.com/detail/8557768) (visual reference, third-party reproduction).
- [Blade Ball merchandise branding](https://shop.app/m/592epqjxtm) (logo image found in image search).
- [BIG Games Pet Simulator 99 announcement and trailer link](https://www.biggames.io/post/pet-simulator-99-announcement) (announcement read; linked trailer not watched).
- [Pet Simulator 99 fan logo concept](https://devforum.roblox.com/t/pet-simulator-99-logo-concept-feedback/2723353) (image-search reference; not the official game logo).
- [Adopt Me official press and brand resources](https://www.playadopt.me/press).
- [Adopt Me wordmark visual reference](https://commons.wikimedia.org/wiki/File:Adopt_Me!_Wordmark.svg).
- [GFX COMET Roblox 3D text tutorial video](https://www.youtube.com/watch?v=_t5ULYrX9fo) (discovered through search; playback unavailable, not watched).
- [Roblox community advanced 3D text tutorial](https://devforum.roblox.com/t/how-to-make-advanced-3d-text-for-logos-step-by-step-tutorial/1436884) (located but body blocked by website verification; not relied upon for technical claims).

Vault conventions note: `C:\Vault\CLAUDE.md` was absent when checked. Followed Holden's supplied frontmatter, wikilink, and placement conventions.

