---
tags: [visuals/art-direction, visuals/retro]
status: draft
updated: 2026-10-05
confidence: medium
---
# Retro Stud Style Guide (classic 2006–2012 Roblox look)

## TL;DR
- The classic look comes from **rules, not textures**: a 1-stud grid, three part heights (Brick 1.2, Plate 0.4, Symmetric 1.0), 90° rotations, a **small fixed BrickColor palette**, studs on top / inlets underneath, tiny compact maps.
- Studs come from one of three sources: **legacy `SurfaceType`** (Parts only, free, crisp), a **stud `MaterialVariant`** (works on meshes/unions), or a **`Texture`** per face (`StudsPerTileU/V = 4` is the common community value). Pick one per game.
- Lighting: `LightingStyle = Soft`, flat bright sky, no or very thin Atmosphere, `ColorGradingEffect.TonemapperPreset = Retro`, low `EnvironmentDiffuse/SpecularScale`. Starting point only. Tune it by eye on a phone.
- Make the style **do gameplay work**: the limited palette and identical primitives are a mechanic (hiding, building, reading a scene at a glance), not just a skin.
- ⚠️ **Conflicts with a vault rule.** [[CLAUDE]] says "no final part-built props; use Blender low-poly". A stud game is part-built by definition. **Holden must approve an exception per project** before any build work.
- No ripped assets. Don't extract textures or sounds from old clients (a devforum tip) or reuse the old "oof" sound, which Roblox replaced over licensing in 2022 (⚠️ verify date). Make original stud textures, faces and SFX.

## Why now (context, 2026-10)
- Roblox ran **"The Hunt: Roblox 20"** (Sep 17–28 2026), a 20th-anniversary event with a limited **Classic app theme** (old logo, colours, font). Plus subscribers keep the theme permanently. Nostalgia for the classic look is high with players right now. Source: Roblox newsroom.
- The 2024 event "The Classic" did the same: remade classic gear and a hub. Brickbattle remakes (Super Doomspire, Crossroads remakes) still have audiences.
- Note: the audience of young teens never played 2008 Roblox. To them the look reads as **"Roblox meme / old Roblox"**, not personal nostalgia. Lean into the jokes (noobs, free models, kill bricks, "anchored"), not the history lesson. This is a hypothesis.

## Building rules
| Rule | Value | Why |
|---|---|---|
| Grid | Move snap **1 stud** on X/Z; **0.2** on Y for plates/bricks | Stud/inlet alignment; no partial studs |
| Part heights | Brick **1.2**, Plate **0.4**, Symmetric **1.0** (X/Z any whole number) | The old FormFactor sizes give the chunky look |
| Rotation | 90° only (45° sparingly for roofs) | Classic builds never had free rotation |
| Thickness | Walls ≥ 1 stud, floors ≥ 1 plate | Thin walls look modern and clip |
| Map size | A few hundred studs across; thousands of parts, not tens of thousands | Classic maps were compact and cozy; also good for mobile |
| Shapes | Block, Wedge, CornerWedge, Cylinder, Ball, TrussPart, SpawnLocation | The classic toolbox. Avoid meshes except hero props |
| Unions | Avoid | Unions lose legacy surfaces and look smooth |
| Decals | Low-res (256²), flat, hand-drawn signs | The early "MS Paint" decal charm |

Tools named by the community (audit before installing; see [[Asset-Creation-Workflow-And-Marketplace]] for the backdoor checklist): **Resurface** (bulk surface/stud conversion), FormFactor plugin, Classic-Colors-V2 (32/64-colour palettes), CTools, Classic-Mesh-Kit, "2008–2024 Studs As PBR Materials" (MaterialVariants). ⚠️ verify each still exists and is clean.

## Getting studs on parts
1. **Legacy surfaces (default choice for Parts).** In the Command Bar with parts selected:
   ```lua
   for _, p in game.Selection:Get() do
   	if p:IsA("BasePart") then
   		p.TopSurface = Enum.SurfaceType.Studs
   		p.BottomSurface = Enum.SurfaceType.Inlet
   	end
   end
   ```
   Free and crisp. Parts only. Some community posts say legacy surfaces don't respond well to modern lighting. ⚠️ verify: how they render on `Plastic` vs `SmoothPlastic` and on low-end mobile.
2. **Stud MaterialVariant.** Put a variant under `MaterialService` and set it as the Plastic override, or apply by name. Works on MeshParts and unions. Costs texture memory, so keep to 1–2 variants ([[Shaders-Materials-And-Surfaces]]).
3. **Texture per face.** `Texture` with `StudsPerTileU/V = 4`. Most control, most instances. Use it for meshes that need studs on one face.
4. **Blender route for complex shapes.** Remesh modifier → blocky shape → stud texture in Studio (devforum). Keeps [[Blender-To-Roblox-Pipeline]] for hero props.

## Palette
Lock the game to **16–24 BrickColors**, and use nothing outside them for world parts. Working set to start from (the exact membership of the historical "32" is unverified; ⚠️ verify with Classic-Colors-V2):
Bright red, Bright blue, Bright yellow, Bright green, Dark green, Earth green, Bright orange, Bright violet, Medium blue, Sand blue, Sand green, Brick yellow, Nougat, Reddish brown, Medium stone grey, Dark stone grey, Light stone grey, Institutional white, Black.
- Gameplay colours (team, hazard, pickup) are **reserved** and never used for decoration. Example: Really red = kill brick only.
- Baseplate: classic grey or green with studs. Sky: flat bright blue.

## Lighting starting preset (tune on phone)
| Property | Value |
|---|---|
| `LightingStyle` | Soft |
| `PrioritizeLightingQuality` | false (keep draw distance; maps are small anyway) |
| `Brightness` | 2–3 |
| `Ambient` / `OutdoorAmbient` | ~(110,110,110) / ~(140,140,140) (bright, flat) |
| `EnvironmentDiffuseScale` / `EnvironmentSpecularScale` | 0–0.2 / 0 (kills the modern PBR sheen) |
| Atmosphere | none, or Density ≤ 0.2 |
| `ColorGradingEffect` | TonemapperPreset = Retro |
| `ColorCorrectionEffect` | Saturation +0.1, Contrast +0.05 |
| `ClockTime` | 14 (classic midday) |
| Bloom / SunRays / DepthOfField | off |
From [[Lighting-And-Atmosphere]] (Soft = flat retro look; Retro tonemapper). Values are author starting points, not Roblox guidance.

## Characters
- Set the game to **R6** (classic six-part body, classic animations) or offer an R6 "Classic mode". R6 also makes ragdolls and costumes cheaper ([[Animation-Rigging-And-IK]]).
- **Project override (2026-10-05):** where a project style guide disagrees with this general guide, the project guide wins. Example: Trap Your Friends direction A uses players' own R15 avatars and `LightingStyle = Realistic` ([[Trap-Your-Friends-Art-Style-Guide]]), not R6 and Soft.
- Optional **"brickify" pass**: apply a `HumanoidDescription` with palette body colours, keeping the player's hats and face. Players keep their identity and the scene stays on-palette.
- Faces: the default smile face, or original simple faces. Don't use paid catalog faces as game assets.

## UI: two directions
| Direction | Looks like | Use when |
|---|---|---|
| Authentic 2008 | Grey translucent panels, square buttons, Arial/Legacy font, small text | Parody or meme moments (fake "old Studio" popups, a fake 2008 error box) |
| **Modern-classic (recommended)** | The chunky bevelled "stud UI" from the vault references (`Assets/Reference-Captures/X/ui-stud`, `_review/ui-stud-1.jpg`): thick strokes, bright fills, stud pattern on panel backs, palette colours | Main HUD. Readable on mobile ([[UI-Layout-And-Device-Scaling]]) |

## Sound
- Original SFX only: brick clack, plastic snap, a cartoon "uh-oh" death sound, an 8-bit-ish jingle. Classic sound effects are a big part of the memory, so make **soundalike-in-spirit**, not copies ([[Sound-Design]]).

## Checklist
- [ ] Holden approved the part-built exception for this project
- [ ] Snap set to 1 / 0.2 and rotation to 90° before building
- [ ] Palette module (ReplicatedStorage/Palette) holds the only allowed BrickColors; a lint script flags off-palette parts
- [ ] Stud source chosen (surfaces vs variant vs texture), tested on a phone at low graphics quality
- [ ] Lighting preset saved as a module; thumbnail preset separate ([[Thumbnails-And-Icons]])
- [ ] R6 or Classic-mode decision recorded
- [ ] No ripped or legacy-copyright assets

## Pitfalls
- "Retro" done half-way (modern smooth parts + one stud texture) reads as low effort, not style.
- Too many colours breaks the look faster than anything else.
- A map that is too big kills both the cozy feel and mobile performance.
- Old-Roblox jokes that need 2008 knowledge fall flat with a 12–15 audience.
- Brand risk: avoid Roblox's own marks (old logo, Builderman, Bloxy Cola, Tix logo) as game art. ⚠️ verify Roblox brand guidelines before any classic reference in thumbnails.

## Related
[[Art-Direction]] · [[Lighting-And-Atmosphere]] · [[Shaders-Materials-And-Surfaces]] · [[Animation-Rigging-And-IK]] · [[UI-Polish-And-Juice]] · [[Retro-Party-Game-Concepts-2026-10-05]]

## Sources
- woodreviewer, "On Retro Looking Games" (2025-05-23): 1×1 grid, studs/inlets alignment, 32 BrickColors, compact maps, FormFactor increments, 256² decals — https://woodreviewerrbx.com/2025/05/23/on-retro-looking-games/
- Devforum "Roblox – Classic Building Guide": Brick 1.2 / Symmetric 1 / Plate 0.4, 1-stud grid, 90° rotations — https://devforum.roblox.com/t/roblox-classic-building-guide/3297677
- Devforum "The Old Roblox Ultimate Guide": FormFactor table, 32/64 palettes, plugin list — https://devforum.roblox.com/t/the-old-roblox-ultimate-guide/3962532
- Devforum "How to change a part's surface to Studs": Command Bar surface script — https://devforum.roblox.com/t/how-to-change-a-parts-surface-to-studs-no-textures-or-decals-required/3497234
- Devforum "How do you build like this?" (Nostalgic Homestore): Blender remesh, kitbash clusters, ≤3 browns — https://devforum.roblox.com/t/how-do-you-build-like-this/3152921
- Devforum "How do you recreate a retro/classic Roblox design?" — https://devforum.roblox.com/t/how-do-you-recreate-a-retroclassic-roblox-design/2210840
- TextureGen stud guide: MaterialVariant, Texture StudsPerTile 4, Resurface — https://texturegen.com/how-to-get-the-stud-texture-in-roblox-studio/
- Roblox newsroom, "Join The Hunt: Roblox 20" (Sep 2026) — https://about.roblox.com/newsroom/2026/09/join-the-hunt-roblox-20
- All fetched 2026-10-05. Community sources, not Roblox docs. Lighting values are hypotheses.
