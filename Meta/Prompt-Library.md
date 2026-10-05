---
tags: [meta/prompts]
status: draft
updated: 2026-10-04
confidence: medium
---
# Prompt Library

Prompts that worked well (or are worth reusing) when asking Claude to produce Roblox work.
Store the original wording verbatim, then a reusable template and why it works.
For prompts covering every part of game development (systems, UI, maps, monetisation, launch…), see [[Prompting/_Index|Prompting]]; this note keeps the saved asset prompts.

## TL;DR — what makes a good asset prompt
- Say **what the asset is used for in-game** (held, placed in a machine, worn, etc.) — it decides rigging, collision and scale.
- Say **what is out of scope** (e.g. "I'll code pickup myself, only do visuals") so Claude doesn't overbuild.
- Name the **art style** explicitly, including what *not* to do (e.g. "not blocky Roblox style, realistic").
- Name the **delivery format** exactly (file types, zip, what to exclude — e.g. OBJ+MTL, not GLB).
- Ask for **a full list of assets to download/import**, plus the scripts that set them up.
- Invite questions ("ask as many as you need") so gaps get filled before work starts.

---

## 1. 2D clothing → realistic 3D props with VFX (held items, not wearables)

### Original prompt l of each of these 2d models of clothing for my roblox game. Make sure to make them polished and nice looking with good vfx that can be imported through roblox with a script. Give me all of the assets i will have to download and import to roblox if you use custom vfx/assets. Do not make them in a roblox blocky style, make them in a realistic style. After done Make a zip of all the vfx and scripts i will need and have the zip contain the obj and mtl of each model and not the glb. Ask questions if needed. The clothing are meant to be held and put in washing machines and dont need to be rigged to roblox avatars or be able to be worn. Ask as questions as you want to make the best result possible. I intend on coding the picking up and what not separately only code the vfx and other things that are visual for the clothes.

### Reusable template
```text
Generate a 3D model of each of these [2D references: attach images] for my Roblox game.

Use in-game: [held / placed in <machine> / decoration / worn]. [Do / do not] rig them to Roblox avatars.
Style: [realistic / stylised / low-poly]. Do NOT use [blocky Roblox style].
Quality: polished, game-ready (sensible triangle count, clean UVs, textures ≤1024px).

Visuals to include: [VFX, e.g. sparkle on pickup, steam/bubbles in washer, wet/clean state swap],
set up by a script so they can be imported into Roblox.
Out of scope: [pickup / interaction logic — I'll code this myself]. Only code visual things.

Deliverables:
- A zip containing: [OBJ + MTL + textures per model] (NOT [GLB]), all VFX assets, and all scripts.
- A list of every asset I must download and import to Roblox, with where each goes
  (Workspace / ReplicatedStorage / etc.) and the import settings to use.

Ask me as many questions as you need before starting to get the best result.
```

### Why it works / what to add next time
- ✅ States use (held + washing machine) → no rigging, no layered-clothing cage needed.
- ✅ States scope boundary (visuals only) and format (OBJ+MTL, not GLB).
- ➕ Add: target **triangle budget** per model and **texture size** (see [[Blender-To-Roblox-Pipeline]]).
- ➕ Add: **CollisionFidelity** wanted (Box/Hull is fine for held props) and whether they need physics.
- ➕ Add: how VFX are triggered (an attribute, a BindableEvent, or a function you call) so your pickup code can hook in — e.g. "expose `ClothingVFX.play(model, "Wash")`".
- ➕ Add: number of items and any **states** (dirty / wet / clean / folded) that need texture swaps.
- ⚠️ Note: OBJ carries no PBR maps beyond what MTL references; for realistic look in Roblox, ask for separate
  albedo/normal/roughness/metalness PNGs to use in a `SurfaceAppearance` (see [[Shaders-Materials-And-Surfaces]]).

## 2. Creature reference sheet → model with animations (community, Sept 2026)
Context: sent to Claude Design along with a generated reference sheet (see [[AI-Assisted-Workflow]] §5).
> lets do these sheets next, since this is a creature, it should be slightly different than a humanoid form, just keep that in mind.. Remember to use work flows and they need animations with vfx. Ask questions if needed

Companion instruction for animations: *"I want idle, walk and attack animations with VFX. Ask me questions."*
Answer the 2–3 questions it asks.

## 3. UI polish pass from references (community, Oct 2026)
Attach: reference UI screenshots + an icon pack.
> Now i want the UI to be better visually. Make it more polished and use these references. Use this icon pack and redesign the UI perfectly. I want there to be good looking gradients, drop shadows, fredoka one style and highlights etc.

➕ Improve it by: listing the screens to redo, giving hex colours, and running it as the 3-pass method
(layout → colours → icons) from [[AI-Assisted-Workflow]] §1.

## 4. Template filled in: fantasy "Dragon's Hoard" prop set (no references, 2026-10-03)
Context: learning/reference set, not for a specific game; written with Claude to paste into Claude Design.
Holden asked for every item to be a **separate model**, kept OBJ + MTL as the format, and let Claude pick the VFX per item.
Not yet run, so the result is unknown (⚠️ verify: update this entry with what Claude Design produced).

```text
Generate a 3D model of each item in this fantasy "Dragon's Hoard" set for Roblox.
This is a standalone learning/reference set, not for a specific game.
Every item must be its OWN separate model and file (nothing merged together):

1. Dragon Egg – Ember (red/orange scales, gold speckles)
2. Dragon Egg – Frost (icy blue/white scales)
3. Dragon Egg – Venom (green/purple scales)
4. Gold Coin (single)
5. Small Coin Pile
6. Large Coin Pile (with a few gems mixed in)
7. Jewelled Goblet
8. Crown (gold, coloured gems)
9. Treasure Chest – Base
10. Treasure Chest – Lid (separate model, pivot on the hinge so it can rotate open)
11. Sword (ornate hilt, can be placed standing upright in the Large Coin Pile)

Use: should work as either held pickups or placed decoration. Do NOT rig them to Roblox avatars.
Style: clean, flat-shaded stylised low-poly, with colour variation on every model (tones and accents,
no single-colour models). Do NOT use blocky Roblox style, part-built props or Roblox AI mesh generation.
Quality: polished and game-ready. Under ~2,000 triangles per model (coins much less), clean UVs,
one small shared colour-atlas texture (256–512px, max 1024px), pivot at the base centre (lid: at the
hinge), real-world scale noted in studs. No vertex colours.
Collision: Box for small items, Hull for the chest. No physics needed.

Visuals to include (set up by a script so they can be imported into Roblox):
- Dragon eggs: slow pulsing glow in each egg's colour, plus a few small particles (embers / frost
  flakes / green bubbles).
- Coins, coin piles, goblet, crown: occasional gold sparkle twinkle.
- Chest: lid swings open with a gold light burst and coin-sparkle particles.
- Sword: soft shine sweep along the blade and a faint magical glow.
- Any item: optional "pickup" idle (slow bob and spin + shine) that can be switched on or off.
Expose the VFX through one ModuleScript with simple functions my own code can call, e.g.
HoardVFX.enable(model, "Sparkle"), HoardVFX.disable(model), HoardVFX.openChest(chestModel).
Out of scope: pickup / interaction logic. I'll code that myself. Only code visual things.

Deliverables:
- A zip containing: OBJ + MTL + textures per model (NOT GLB), all VFX assets (particle textures etc.),
  and all scripts.
- A list of every asset I must download and import to Roblox, with where each goes
  (Workspace / ReplicatedStorage / ServerStorage / etc.) and the import settings to use.
- A short note on how to assemble the chest (base + lid) and stand the sword in the coin pile.

Ask me as many questions as you need before starting to get the best result.
```

What changed versus the bare template (recommendations, not tested):
- No 2D references → the first line lists each item with colours instead.
- Parts that move or combine (chest lid, sword) are split into their own models because OBJ has no hierarchy or pivots.
- Adds the ➕ items from §1: triangle budget, texture size, collision, and a callable VFX API.

Idea packs considered (Holden picked Dragon's Hoard): Wizard's Workshop, Enchanted Forest, Adventurer's Gear,
Floating Ruins, Magical Creatures' Things. These are candidates for future practice sets.

## 5. Template filled in: three fantasy creatures from a reference-sheet style (2026-10-04)
Context: Holden pasted the §1 template with a Kingshot "unit design bible" screenshot (Mercenary Lancer) as the style
reference and the Discord advice from [[AI-Assisted-Workflow]] §5. The session started from the Claude Design template.

```text
Generate a 3D model of each of these [2D references] for my Roblox game. (I want three fantasy creatures in the style as the reference)
use Claude design and blender (mcp is connected)
Use in-game: These are for practice(maybe used later) we are just making the models no specifics [Do / do not] rig them to Roblox avatars.
Style: [same as the reference image]. Do NOT use [blocky Roblox style].
Quality: polished, game-ready (sensible triangle count, clean UVs, textures ≤1024px).
Visuals to include: [VFX, e.g. sparkle on pickup, steam/bubbles in washer, wet/clean state swap], set up by a script so they can be imported into Roblox.
Only code visual things.(for now)
Deliverables: (same as §1)
Ask me as many questions as you need before starting to get the best result.
i want you to make it like this screenshot. dont slack or worry about usage, use all resources from the vault aswell
```

What happened (local observations):
- **Placeholders left in.** Three were left unfilled: `[Do / do not]`, the washer VFX examples from §1 and `[2D references]` (there were none). Claude had to propose the creatures and the VFX itself. Next time, fill in each bracket or delete it.
- **"In the style of the reference" means rendered 3D art,** not just the layout. A flat vector first pass was rejected at once ("looks nothing like the reference"). The fix was rendering the real model for every view. See [[Fantasy-Creatures-Set]].
- **"mcp is connected" was only true in another project.** The Blender MCP is registered in Fish a Monster's `.mcp.json`, not the vault's. Headless Blender did the work instead. Its safe mode would also have blocked numpy.
- **Claude Design publishing was blocked by auto mode.** The sheets were authored as canvas files to publish later.
- ➕ Add next time:
  - which creatures (or "you pick, show me 3 options first");
  - target size in studs (pet / mount / boss);
  - whether VFX should be ambient loops, triggered bursts or both;
  - the trigger API you want, e.g. `CreatureVFX.play(model, "Roar")`.

## Related
- [[Blender-To-Roblox-Pipeline]] · [[VFX-Particles-Beams-Trails]] · [[Shaders-Materials-And-Surfaces]] · [[Asset-Creation-Workflow-And-Marketplace]] · [[Home]] · [[Fantasy-Creatures-Set]]
