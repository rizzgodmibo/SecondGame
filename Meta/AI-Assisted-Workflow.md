---
tags: [meta/ai-workflow]
status: draft
updated: 2026-10-04
confidence: low
---
# AI-Assisted Workflow (community advice)

How to get good results from AI tools (Claude, ChatGPT/Codex, image models, Meshy) when building Roblox games.
Source: community advice from Discord screenshots supplied by the vault owner (Sept 2026). These are
**practitioner opinions, not verified facts**. Platform limits below were checked where marked.
For saved prompt wording, see [[Prompt-Library]].

## TL;DR
- **Always start from a reference image.** Have the AI *analyse* it first (no building), then build in small passes.
- **Work in passes:** dimensions/layout → colours → icons/details. Check each pass, then re-prompt with the exact faults.
- **Use a reasoning model as the prompt writer.** Show it the reference, have it write the build prompt for the
  agent doing the work, then show it the result and ask what to improve. Repeat.
- **Close the loop with renders/screenshots.** The agent renders in Blender (or screenshots Studio), compares to the
  reference, fixes faults and repeats until it's close.
- **Match the model to the job** (see the table) and write your own skills for repeated tasks.
- **Low-poly AI meshes:** target **≤ 20,000 triangles per mesh** (Roblox hard limit), keep the detail in the texture.

## 1. Reference-image, multi-pass method (UI, models, VFX)
1. **Get a reference image.** Generate it with an image model or collect it (see `Reference/` for real-game refs).
2. **Analyse only.** Prompt: *"Analyse this reference image. Do not implement anything yet. Describe the structure,
   canvas dimensions, X/Y positions of every element, and all visible UI components."*
3. **Build step by step, one pass per prompt:**
   1. Dimensions and layout correct (sizes, positions, anchoring). Check it before continuing.
   2. Colours, stated exactly (hex/RGB values, not "blue-ish").
   3. Icons and detail elements.
4. **When a pass is wrong, re-prompt with what exactly is wrong** ("the shop button is 40px too low and the stroke is
   grey, should be #1E1E1E 3px"), not "make it better".
5. **Prompt-writer loop:** give a reasoning model the design intent + reference, and have it write the prompt for the
   executing agent. After a run, send the result images back to it with "this is what we have so far, what can be
   done better?" and run the new prompt it gives. Repeat until it matches.
6. **Autonomous render-compare loop** (when you have usage to spare): tell the agent to render in Blender
   (or screenshot in Roblox Studio via [[Tooling-Rojo-Wally-And-Studio-MCP]]), compare against the reference, list the
   faults, fix them and repeat. It should only stop once the result is close to the reference. A goal-style
   instruction ("don't finish until…") works well for this.
   - Reported result: a polished stylised butterfly/creature with orbiting trail VFX, made in Blender with this loop.

## 2. AI 3D models with fewer faces (image → Meshy → Roblox)
1. Generate a concept image in an image model (give it a template image plus what to change: texture, colour scheme).
2. In Meshy, use the **built-in agent rather than the plain modeler**. Give it the reference picture and say:
   *"Keep it under 20k faces (or lower), keep all the details, make it low poly."*
3. If Meshy outputs a high-poly model anyway, **remesh to the target face count**.
4. Advice says pick 8192 (8K) texture for better quality.
   ⚠️ verify: Roblox docs cite **4096×4096 max** texture support but recommend ≤1024×1024 for most objects.
   An 8K texture will be downscaled on import, so its only benefit is a cleaner source for downscaling/baking.
   Export at 1024 (or 2048 for hero props) yourself to control the result. See [[Blender-To-Roblox-Pipeline]].
- Roblox limit (verified 2026-10-04): **an individual mesh cannot exceed 20,000 triangles.** Split bigger models
  into several MeshParts. Note that "faces" in Meshy may mean quads (1 quad = 2 triangles), so target ~10k quads
  to land at 20k triangles.

## 3. Which model for which job (community opinion, Sept 2026)
| Job | Suggested model | Notes |
|---|---|---|
| 3D modelling scripts, backend, implementation, animation | Claude Opus 5.5 | Highest quality, most tokens |
| UI, light project management, bug fixes | Claude Sonnet 5.5 | One user reports similar results to Opus at about half the token cost. Good default on a $20 plan |
| Icons / thumbnails (image generation) | "Astra 6" | ⚠️ verify: what this tool is and how it compares |
| Coding (benchmark claim) | "6.1 SOL" | ⚠️ verify: claimed to top coding benchmarks. Can be called from Opus via a custom MCP relay. Unverified |
- Building in Studio: **give Claude reference images**. Quality comes from references, not from the model alone.
- **Create your own skills** for repeated jobs (e.g. "build a UI from reference in 3 passes",
  "import + set up a mesh with SurfaceAppearance").

## 4. Making Claude and ChatGPT/Codex work together
- Composio can let Claude **call OpenAI models via the API**. That is billed separately from a ChatGPT subscription,
  the call is stateless (you have to pass context every time) and has no ChatGPT history. If you loop it, set a hard cap on turns.
- **Better: use this vault as the shared hand-off.** Each tool reads and writes notes in agreed places:
  - Claude: builds systems, writes findings/harvested patterns into the vault.
  - Codex/ChatGPT: reads them, writes audits and research updates back.
  - Use a `RESEARCH BACKLOG` note as the hand-off queue and a `VAULT CHANGELOG` note as the log,
    plus a short hand-off protocol in `CLAUDE.md` and `AGENTS.md` (who writes where, how tasks are claimed,
    how results are logged). It's free, every exchange is readable, and it can't spiral.
  - ⚠️ todo: write that protocol if/when a second agent starts using this vault.

## Pitfalls
- Skipping the analyse-only step → the AI guesses the layout and every later pass inherits the error.
- Vague corrections ("looks off") waste a whole pass. Give coordinates, sizes, hex colours.
- Render-compare loops burn lots of usage. Cap the iterations or reserve them for hero assets.
- Model recommendations go out of date fast. Re-check this table every few months.

## Related
- [[Prompt-Library]] · [[Blender-To-Roblox-Pipeline]] · [[UI-Architecture]] · [[UI-Layout-And-Device-Scaling]]
- [[Tooling-Rojo-Wally-And-Studio-MCP]] · [[Thumbnails-And-Icons]] · [[Home]]

## Sources
- Community advice screenshots (Discord, 2026-09-18 to 2026-09-29), supplied by vault owner, 2026-10-04.
- Roblox mesh specifications (20,000-triangle limit): https://create.roblox.com/docs/art/modeling/specifications
- Roblox texture specifications: https://create.roblox.com/docs/art/modeling/texture-specifications
