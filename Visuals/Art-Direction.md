---
tags: [visuals/art-direction]
status: draft
updated: 2026-10-04
confidence: medium
---
# Art Direction

Art direction on Roblox has one job above all: **make the game read instantly at small sizes** — a 150 px thumbnail on a phone home feed, a character 40 px tall on a 6-inch screen, a button icon at 48 px. Beauty at 4K is secondary.

## TL;DR
- **Pick a style the team can produce consistently for 2+ years of updates.** For 1–3 person teams: low-poly / flat-shaded stylised with a palette atlas, `SmoothPlastic` + built-in materials, Soft or bright Realistic lighting. Avoid realistic PBR unless you have a dedicated 3D artist.
- **Readability rules**: strong silhouettes, value contrast (light vs dark) between player/interactive objects and background, saturated accent colour reserved for interactables and rewards, chunky proportions (big heads/hands/tools ~1.2–1.5× real).
- **Palette**: 1 dominant hue family for the world, 1–2 accent hues for gameplay-relevant things, rarity colours fixed across the whole game (Common grey, Uncommon green, Rare blue, Epic purple, Legendary gold/orange, Mythic red/pink — players already know this convention).
- **Match genre expectations**: simulators = bright, saturated, chunky; horror = desaturated, dark, high contrast pools of light; obby = clean primary colours on neutral; RPG/fantasy = warm, painterly; tycoon = clean plastic & clear zones.
- **Write a 1-page style guide** before mass production (palette hex codes, materials, proportions, tri/texture budgets, UI fonts/strokes, "do/don't" screenshots) and review every asset against it.
- **Art drives the thumbnail and icon** — design key characters/props as "thumbnail-able" from day one. See [[Thumbnails-And-Icons]].

## Choosing a style (decision table)

| Team / budget | Recommended style | Why |
|---|---|---|
| Solo dev, programmer-first | Flat-colour low-poly + Creator Store packs restyled to one palette + Roblox materials | Fastest; consistent if palette enforced |
| 2–5 people, 1 artist | Stylised low-poly with palette atlas or hand-painted 256–512² textures | Distinct identity, mobile-cheap |
| Studio with 3D team | Stylised PBR (SurfaceAppearance on hero assets, MaterialVariants for world) | Premium look, still mobile-viable with budgets |
| Retro / meme / "Roblox-classic" | Studs/blocky parts, `LightingStyle = Soft`, bright flat colours | Nostalgia; extremely cheap; strong with young audience |
| Horror | Realistic lighting, dark palette, limited asset set reused heavily | Lighting/sound do most of the work |

Low-cost style tactics: palette-atlas texturing (one 256² swatch for everything), vertex colours, kitbashing from a small modular set, Neon accents for interactables, stylised skybox + Atmosphere doing the mood, consistent outline via `Highlight` on key characters only.

## Readability at small sizes
- **Squint test / thumbnail test**: shrink a gameplay screenshot to 150×150 px (or 50% blur). Player, objective and reward must still be identifiable.
- **Silhouette**: fill each character/pet/tool solid black — it should still be recognisable and distinct from siblings. Vary shape language (round = friendly, square = sturdy, triangle = dangerous).
- **Value hierarchy**: background mid-to-low contrast and lower saturation; gameplay layer (player, enemies, pickups) highest contrast and saturation; UI on top with strokes.
- **Scale**: interactables slightly oversized; text in-world (BillboardGuis) ≥ 24 px with `UIStroke`.
- **Colour-blind safety**: don't encode team/rarity by red-vs-green alone — add icon shape or pattern (Roblox accessibility guidance: nothing relies solely on colour).

## Palette construction
1. Pick world base hue + time-of-day lighting first (see [[Lighting-And-Atmosphere]]) — lighting tints everything.
2. Define 5–7 world colours (dark, mid, light of 2 hue families) + 2 accent colours + rarity set + UI set (primary CTA green, premium/currency gold, danger red, neutral panel).
3. Keep accents ≥ 30% more saturated than world colours.
4. Store as `StyleSheet` tokens for UI ([[UI-Architecture]]) and as a palette texture/material list for 3D.
5. Validate in-engine under game lighting, not in Photoshop.

Example simulator palette (hex): grass `#5BC65B`, path `#E8D3A2`, rock `#8A8FA3`, sky tint `#8FD3FF`, accent/coin `#FFD23F`, CTA `#2ECC71`, premium `#B66DFF`, danger `#FF4D4D`, panel `#1E2235` @ 20% transparency.

## Consistency & style guide (template)
- **Proportions**: player:door:tree ratios; character head size; tool scale.
- **Geometry**: bevel size (or none), poly density per asset class, edge style (sharp/soft).
- **Materials**: allowed `Enum.Material` list; custom MaterialVariants list; no unapproved Creator Store textures.
- **Colour**: palette swatches + where each is allowed.
- **Lighting preset** name and values.
- **UI**: font family (e.g. Fredoka One / Gotham-class), sizes, stroke thickness, corner radius, button styles, icon style (flat vs 3D renders; same camera angle and lighting for all item icons — render via a single ViewportFrame/thumbnail rig).
- **VFX**: texture set and colour per element (fire/ice/poison).
- **Budgets**: tris and texture size per asset type (from [[Blender-To-Roblox-Pipeline]]).
- **Do/Don't screenshots**.

## Genre expectations (what players click on)
| Genre | Visual cues players expect |
|---|---|
| Simulator / clicker | Huge numbers, sparkly pets, bright saturated worlds, big chunky UI with strokes |
| Tycoon | Clean readable build zones, conveyor/money VFX, satisfying "buy button" pads |
| Obby | Clear path contrast, neon/kill bricks red, checkpoints obvious, colourful themed stages |
| Horror | Darkness + one strong light source, distinctive monster silhouette |
| Anime / battlegrounds | Big VFX, speed lines, R6 often, dramatic poses, high-contrast hit effects |
| Roleplay / life sim | Cozy realistic-lite houses, customisation, warm lighting |
| Tower defense | Distinct unit silhouettes, readable lanes, rarity colours |

When entering a genre, screenshot the top 10 games' thumbnails and in-game views; match the genre's **readability conventions** and differentiate with one memorable element (colour theme, mascot, camera angle). See [[Genre-Playbooks]].

## How art feeds marketing
- Design a **mascot/hero asset** early (pet, monster, character) with a strong silhouette — it becomes the icon focal point.
- Keep a **"photo booth" place/scene**: thumbnail lighting preset, posed rigs, clean backgrounds. Thumbnails/icons are owned by Growth — see [[Thumbnails-And-Icons]].
- In-game screenshots should look like the thumbnail (expectation match improves play-through and retention).

## Checklist
- [ ] Style chosen against team capacity; 1-page style guide written
- [ ] Palette defined with hex codes; rarity colours fixed
- [ ] Squint/thumbnail test passed for gameplay screenshot
- [ ] Silhouettes of characters/pets distinct
- [ ] Creator Store assets restyled to palette/materials before use
- [ ] Mascot/hero asset exists for icon/thumbnail

## Pitfalls
- Mixing free-model styles (realistic tree next to low-poly rock) — the #1 "cheap game" signal.
- Too many saturated colours → nothing stands out; the accent loses meaning.
- Dark scenes that look moody on a monitor and black on a phone at 50% brightness.
- Detailed small textures that become noise at mobile resolution.
- Changing art style mid-life without a full pass — old areas look abandoned.

## Related
- [[Visuals/_Index]] · [[Thumbnails-And-Icons]] · [[Lighting-And-Atmosphere]] · [[UI-Architecture]] · [[UI-Polish-And-Juice]] · [[Blender-To-Roblox-Pipeline]] · [[Shaders-Materials-And-Surfaces]] · [[Asset-Creation-Workflow-And-Marketplace]] · [[Genre-Playbooks]]

## Sources
- Roblox accessibility (colour non-reliance, contrast) — https://create.roblox.com/docs/production/publishing/accessibility
- Texture/texel guidance — https://create.roblox.com/docs/art/modeling/texture-specifications
- Lighting styles — https://create.roblox.com/docs/environment/lighting
- Checked via Roblox/creator-docs GitHub source (2026-10-02 commit) on 2026-10-04. Style, palette and genre guidance in this note is practitioner judgement (confidence medium), not Roblox policy.
