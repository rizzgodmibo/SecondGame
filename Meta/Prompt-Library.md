---
tags: [meta/prompts]
status: draft
updated: 2026-10-04
confidence: medium
---
# Prompt Library

Prompts that worked well (or are worth reusing) when asking Claude to produce Roblox work.
Store the original wording verbatim, then a reusable template and why it works.

## TL;DR — what makes a good asset prompt
- Say **what the asset is used for in-game** (held, placed in a machine, worn, etc.) — it decides rigging, collision and scale.
- Say **what is out of scope** (e.g. "I'll code pickup myself, only do visuals") so Claude doesn't overbuild.
- Name the **art style** explicitly, including what *not* to do (e.g. "not blocky Roblox style, realistic").
- Name the **delivery format** exactly (file types, zip, what to exclude — e.g. OBJ+MTL, not GLB).
- Ask for **a full list of assets to download/import**, plus the scripts that set them up.
- Invite questions ("ask as many as you need") so gaps get filled before work starts.

---

## 1. 2D clothing → realistic 3D props with VFX (held items, not wearables)

### Original prompt (verbatim, 2026-10-04)
> Generate me a 3d model of each of these 2d models of clothing for my roblox game. Make sure to make them polished and nice looking with good vfx that can be imported through roblox with a script. Give me all of the assets i will have to download and import to roblox if you use custom vfx/assets. Do not make them in a roblox blocky style, make them in a realistic style. After done Make a zip of all the vfx and scripts i will need and have the zip contain the obj and mtl of each model and not the glb. Ask questions if needed. The clothing are meant to be held and put in washing machines and dont need to be rigged to roblox avatars or be able to be worn. Ask as questions as you want to make the best result possible. I intend on coding the picking up and what not separately only code the vfx and other things that are visual for the clothes.

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

## Related
- [[Blender-To-Roblox-Pipeline]] · [[VFX-Particles-Beams-Trails]] · [[Shaders-Materials-And-Surfaces]] · [[Asset-Creation-Workflow-And-Marketplace]] · [[Home]]
