---
tags: [prompting/3d, visuals/pipeline, design/maps]
status: draft
updated: 2026-10-04
confidence: medium
---
# Prompting: 3D Assets, Characters and Maps

How to ask Claude for props, creatures and maps that meet Holden's art rules and are actually playable. General rules: [[Prompting-Principles]]. Asset-prompt templates with full wording are already in [[Prompt-Library]] (§1 template, §4 Dragon's Hoard, §5 creatures); this page links them rather than repeating them.

## TL;DR
- **Every 3D prompt starts with "read the AssetLibrary README and [[Art Direction Feedback]]".** Rules: Blender-made or free sources (Poly Pizza, Poly Haven, Sketchfab), clean flat-shaded low-poly, crisp zone colours, colour variation on every model, varied trees. No Roblox AI meshes, no part-built final props.
- **Ask for renders and an honest self-critique before Claude shows anything,** and renders before any upload. Holden wants weak points named, and self-critique removed several problems before he saw them ([[Art Direction Feedback]], [[Dragons-Hoard-Set]]).
- **Anatomy before detail for creatures:** grey model in front, side and three-quarter views, approved first, then surface and colour. "Detail on a toy base stays a toy" ([[Art Direction Feedback]]).
- **Maps are measured, not eyeballed.** Ask for the [[Roblox Map Audit Skill]] with real movement numbers, and tag where players must and must not reach (ask Holden; don't guess level design).
- **Write critiques as numbered faults → what I want → process.** [[Rubber-Tower-Map-v3-Critique]] is the model: scope the redo to one area, require 4 screenshot angles plus a 150 px version, self-critique, keep the audit passing, show before/after.

## What Claude needs from you
- What the asset is used for in game (held, placed, worn, walked on), its size in studs, and states (open/closed, dirty/clean).
- Style references with what each one is for, and the colour palette or zone colours.
- Triangle and texture budgets (≤ 20k tris per mesh is the hard limit; Holden's prop warning at 10k; textures ≤ 1024 px), collision type, and pivot location.
- For maps: the route, landmarks, checkpoints, themes per area, and the default movement numbers or the game's own.
- Whether you approve uploading (uploads publish to Holden's account; each batch needs an explicit OK).

## Vault notes to point Claude at
| Note | Gives Claude |
|---|---|
| `C:\Users\holde\Documents\GameDev\AssetLibrary\README.md` | The pipeline, reusable models, ids, Holden's art feedback |
| [[Art Direction Feedback]] · [[Art-Direction]] | Rejected/wanted lists; readability, palette and genre rules |
| [[Blender-To-Roblox-Pipeline]] · [[Blender to Roblox Asset Pipeline]] · [[Roblox Asset Pipeline Skill]] | Export settings, limits, GLB rotation, no vertex colours, preflight checks + preview renders |
| [[Creature-Anatomy-And-Proportions]] · [[Fantasy-Creatures-Set]] · [[Dragons-Hoard-Set]] | Measured limb ratios; what went wrong and right in two practice sets |
| [[Roblox Map Audit Skill]] · [[Difficulty-And-Mastery]] · [[Lighting-And-Atmosphere]] | Reachability checks; checkpoint and retry rules; lighting presets |
| [[X-Low-Poly-Builds-And-Maps]] · [[Rubber-Tower-Reference-Obbies]] · [[Fish a Monster Map Iterations]] | References and the history of what Holden rejected |

## Prompts

### 1. A prop set
Use the full template in [[Prompt-Library]] §1 (filled example: §4). Its must-haves: in-game use, style with "do NOT" list, quality budget (tris, texture size, pivot, scale in studs), collision, visuals and a callable VFX API, out-of-scope, exact deliverables (format, asset list with where each goes), "ask me questions first". Add this line at the end:
```text
Before showing me anything, render every model (Workbench, textured), critique each against Resources/Art Direction Feedback.md, fix the weak points, and run the roblox-asset-pipeline preflight. Show the renders with your honest critique of what's still weak.
```

### 2. A creature or character, anatomy first
```text
Make [CREATURE] for [purpose], about [N] studs tall. One creature at a time.
READ FIRST: Resources/Art Direction Feedback.md (creature sections), Visuals/Creature-Anatomy-And-Proportions.md, the AssetLibrary README.
STAGE 1, anatomy only: an untextured grey model under neutral light, rendered front, side and three-quarter. Check limb thickness against the reference ratios before showing me (forearm about 0.14–0.17 × shoulder height for a heavy predator). Self-critique against the known failures (balloon muscles, beaded joints, sausage legs, button eyes, saw-blade back) and fix them first. Then stop for my approval.
STAGE 2, only after I approve: surface and colour following the anatomy (plates over back and shoulders, finer scales at joints, a restrained palette, glow in only a few deliberate places).
```
Why: the drake took three passes because detail was added to a toy-like base; the grey-model gate fixed that ([[Art Direction Feedback]]).

### 3. A map or level
```text
Plan [AREA] for [Game]. Plan only first.
READ FIRST: the project hub and build plan, Resources/Art Direction Feedback.md, Visuals/Lighting-And-Atmosphere.md, Design/Difficulty-And-Mastery.md, [reference notes].
Give me: the route from spawn to goal, where each checkpoint and landmark sits, sight lines (can I see the next checkpoint from the last?), the theme and colour band for each part, and which kit meshes you'll use (no plain parts as final art).
Ask me where players must reach and must not reach; don't guess. After I approve, build it, tag MapMustReach / MapNoReach, and run the roblox-map-audit skill with the game's real movement numbers. Fix every FAIL.
Before showing me: screenshots from player-eye at spawn, standing on the first checkpoint looking up, an overview from above a corner, and a 150 px shrunk version. Critique them honestly against the art rules and fix weak points first.
```
Why: Rubber Tower's valley v2 passed every automated check but Holden rejected it as a cage; the screenshot angles and the art critique catch what the audit can't ([[Rubber-Tower-Map-v3-Critique]]).

### 4. Turn your critique into a fix prompt
```text
[Area/asset] critique: [one-line verdict]. Read [notes] before you change anything.
WHAT'S WRONG
1. [fault, with what you see]
2. [...]
WHAT I WANT
- [concrete target for each fault: colours, shapes, references, numbers]
PROCESS
- Redo only [smallest area] first, fully dressed, then stop for my review.
- Before showing me: [screenshot angles], honest self-critique against Art Direction Feedback, fix weak points.
- Keep [audit/gates] passing. Show before/after side by side. Log this critique in [hub/status notes].
```
Why: this structure turned a "still not what I asked for" into a scoped, checkable task ([[Rubber-Tower-Map-v3-Critique]]).

### 5. Upload a batch
```text
Prepare [assets] for upload. Run the roblox-asset-pipeline preflight on the export scene (0 FAIL; explain any WARN), render the previews, and list every file with its triangle count, texture size and intended name. Don't upload until I reply "upload OK". After uploading, list every new asset id and where it's recorded.
```

## More examples (added 2026-10-04)
Shorter prompts for other common jobs. Same rules: fill every bracket, keep the check. Sourced patterns are credited in [[Community-Prompt-Examples]].

### Tree variety pack
```text
Make a varied tree set for [Game]'s [biome] in Blender: at least [4] species (rounded layered canopies, a tall pine type, a bushy type, a dead/odd one), 3 sizes each and 3 tints per species so no two neighbours look alike. Flat-shaded low-poly, one shared atlas, under [1,500] tris per tree, pivot at the base. Render a lineup and a scattered patch, and critique the variety before showing me.
```
Holden's standing asks: varied trees, colour variation on every model ([[Art Direction Feedback]]).

### Modular building kit
```text
Make a modular kit for [style] buildings: wall, wall with window, wall with door, corner, floor, roof pieces, trims, all on a [4]-stud grid so pieces snap. Colour variation via the atlas, crisp edges, no z-fighting (offset trims). Build 3 example buildings from the kit to prove it works and render them.
```

### Procedural prop with parameters
```text
Make a [bridge/fence/rail] generator for Studio: a ModuleScript that builds it from kit meshes with editable parameters ([length, plank count, sag, rail height]) and keeps proportions when they change. Show it at 3 different settings. Edit-time tool only; it doesn't run in the live game.
```
Roblox's procedural-model guidance says to name editable parameters and how parts respond when they change ([[Community-Prompt-Examples]] §10).

### Hub / lobby layout
```text
Plan the hub for [Game]: spawn plaza, the main activity entry, shop, upgrade area, leaderboards and the [pets/eggs] area, all visible from spawn within [N] studs, with signs players can read on a phone. Give a top-down sketch with distances, then build a greybox and run the map audit. Keep it compact; Holden prefers smaller hubs (Paper Plane Toss went from 240×190 to 164×132).
```

### Obby stage set
```text
Design [10] obby stages for [Game] that get harder in a sawtooth (hard stage, then an easy recovery stage), with a checkpoint each early on and every 3–5 later (Design/Difficulty-And-Mastery.md). Each stage: the obstacle, the skill it tests, its theme kit pieces, and why a phone player can beat it. Then build them and run the map audit with MapMustReach on every checkpoint.
```

## How to check the result
- Preflight: 0 FAIL (> 20k tris, vertex colours, textures > 4096) and every WARN explained.
- Renders with Claude's own critique, before Holden sees them; Holden's approval quoted before textures, VFX or uploads.
- Map audit PASS for every segment; the 4 screenshot angles and the 150 px view look right to Holden.
- In Studio: correct scale (Holden checks), GLB rotation fixed, no z-fighting.

## Pitfalls
- **"In the style of the reference" means its rendered 3D look,** not its layout. A flat vector sheet was rejected at once ([[Fantasy-Creatures-Set]]).
- **Blank screenshots:** Claude built the Rubber Tower valley without ever seeing it. Require the screenshots, and say "if they're white, tell me".
- **Single-colour models and blurred gradient ground** ("one dimensional", "a smudged mess") are standing rejections ([[Fish a Monster Map Iterations]]).
- **Imported GLBs arrive rotated 180°**; vertex colours turn the ground black; transparent leaf edges render black ([[Blender to Roblox Asset Pipeline]]).
- **Coplanar faces z-fight**; offset trims by 0.015–0.03 studs ([[Dragons-Hoard-Set]]).
- **AI image→3D routes** (Hi3DGen, Hunyuan3D) conflict with Holden's rules, and Hunyuan3D's licence excludes the UK ([[Video-SyphoDev-Claude-Code-Roblox-Workflow]]).

## Related
[[Prompting/_Index|Prompting]] · [[Prompting-Principles]] · [[Prompt-Library]] · [[Prompting-Game-Feel]] · [[Art Direction Feedback]] · [[Roblox Map Audit Skill]]

## Sources
- Local: [[Art Direction Feedback]], [[Rubber-Tower-Map-v3-Critique]], [[Fantasy-Creatures-Set]], [[Dragons-Hoard-Set]], [[Fish a Monster Map Iterations]], [[Roblox Asset Pipeline Skill]] (2026-10-01 to 2026-10-04).
- Roblox mesh specifications (20,000-triangle limit): <https://create.roblox.com/docs/art/modeling/specifications>
- Anthropic, Claude Code best practices (visual targets, screenshot-compare loop): <https://code.claude.com/docs/en/best-practices>
