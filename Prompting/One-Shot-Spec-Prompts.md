---
tags: [prompting/examples, prompting/specs, meta/ai-workflow]
status: draft
updated: 2026-10-05
confidence: medium
---
# One-Shot Spec Prompts, Session Bootstraps and "Master Prompts" (analysis)

Analysis of the big community prompts in [[Discord-Prompt-Pack-2026-10-05]]: a 1,768-line spec for recreating Steal an Egg, a VFX session bootstrap for Claude Code + Studio MCP, and the "TDOD" Discord series of master prompts (polish, animation, VFX, map building). For each: what it does well, what doesn't fit Holden, and a version adapted to his setup. Originals stay local (gitignored); everything here is paraphrased. General rules: [[Prompting-Principles]].

## TL;DR
- **The Steal an Egg spec is the best one-shot prompt example in the vault.** It works because it is a contract, not a wish: evidence-tagged numbers, a file tree, a testable build order, a player-story acceptance test, a data-only map spec, automated geometry checks, fixed capture cameras, fresh-context verifiers with a scored JSON verdict, a conflicts list, known unknowns and a final checklist.
- **Copy its structure, not its target.** It recreates a live game (near-clones are deprioritised by Roblox's recommendations, and some of its numbers come from a decompiled client config), builds all art from parts (Holden rejects part-built final props), and uses emoji icons as fallbacks (which the vault flags as an AI-UI tell).
- **The VFX bootstrap shows how to start a Studio session safely:** ask which place first, ask for authorisation second, audit without reinstalling, never accept a licence for the user, test init → emit → cleanup, never fake a PASS, end with a fixed report form.
- **The TDOD master prompts are good checklists with weak stopping rules.** Their named anti-patterns, staged VFX timing, test matrices and "low-usage mode" are worth keeping. Their open-ended "don't stop because something works" and "AAA" language burns usage with no finish line, and the animation one is written for Unreal (Control Rig, Motion Matching, `.cpp` files), not Roblox.

---

## 1. The Steal an Egg one-shot spec

### What's in it (section → what it does)
| Section | What it does | Why it works |
|---|---|---|
| Header: how to use + **evidence tags** | Every number is tagged **[VERIFIED]** (read off the live game or official API, with a date), **[SOURCE]** (community wiki/guides/videos agree) or **[DESIGN]** (hidden server-side, so a tuned value). Keep VERIFIED/SOURCE exactly; DESIGN goes in one Config module | The builder knows what it may tune and what it must not. Same idea as the vault's evidence types ([[CLAUDE]]) |
| §0 Mission + 8 hard requirements | Everything generated from scripts, server-authoritative, persistent data with session locking, full UI list, monetisation plumbing with Studio-only test flag, typed Luau, no deprecated APIs, rate limits | Non-negotiables up front, numbered |
| §0.1 File tree + Rojo project | Every module named with a one-line purpose | Removes architecture guesswork; matches the vault's Services/Controllers pattern ([[Module-Architecture]]) |
| §0.2 Build order | 11 steps, each testable before the next | The "one system at a time" rule inside a one-shot |
| §0.3 Acceptance test | One paragraph walking a new player from join to the first reset, with exact texts and numbers | A story the builder can check itself against |
| §0.4–0.5 Map pipeline | Concept images (generated with references attached) → **MapSpec data module** (every element's position/size/colour) → builder reads only MapSpec → **geometry checks** (lanes contiguous, pathfinding from every plot to every nest, no spawn intersects a part, < 25,000 parts) → **captures from fixed camera coordinates** → **fresh-context verifier per area** | Fixes become data edits; checks are automatic; the verifier never sees the builder's reasoning |
| Verifier prompt (verbatim in the spec) | Strict QA reviewer, no context; scores 10 criteria 0–10 (layout, walls, floor, props, nests, guardian, signage, lighting, scale vs a 5-stud avatar, faithfulness); **JSON only** with blocking issues and exact MapSpec fixes; **pass = total ≥ 85 and no blockers**; max 4 rounds; never reuse a verifier | A concrete, repeatable critic. Note: the vault's [[Gauntlet-Loop]] prefers a forced A/B pick because scores drift up; this spec counters drift with blockers and a fresh verifier each round |
| §1 Game in one page | Genre, server size, loop in 8 steps, pacing, art direction | Short context before the detail |
| §4 Formulas | Income, weight, grow time, walk speed etc. as code blocks with reference values | Testable numbers, not adjectives |
| §17 UI spec | Global style rules (font, stroke, button gradient/corner/hover numbers, window header colours, close button) plus per-screen layout as screen fractions | The UI equivalent of MapSpec |
| §19 Data / remotes / anti-exploit | Data schema, every remote by direction with rate limits, position sanity checks | Security as spec items, not a hope |
| §21 Data appendices | Pets, rarities, mutations, products as ready Luau tables | Content is data |
| §22 Reference media index | Every reference file listed with LIVE / OFFICIAL / community labels and what it shows | References tied to sections |
| §23 Conflicts, §24 Known unknowns, §25 Final checklist | Rulings on contradictions; tuning knobs that are guesses; a done-when checklist ending "output every file completely" | Removes ambiguity; defines done |
| Tool gotcha | Codex CLI: the prompt must come before `-i` image flags or Codex fails with "No prompt provided" (verified on CLI 0.150.1, per the spec) | Write traps into the prompt |

### What doesn't fit Holden
- **It's a clone** of a live game (place 107778070777162). [[Discovery-Algorithm]]: near-copies are deprioritised and may not be able to buy ads. Use the pattern for Holden's own concept with a twist.
- **IP/ToS:** some numbers come from a "decompiled client config" published by a fan wiki. Don't copy data scraped that way into a game.
- **Art:** "everything built from Parts, voxel style" contradicts [[Art Direction Feedback]] (no part-built final props; Blender low-poly).
- **Emoji icon fallbacks** are listed as an AI-UI giveaway in the vault ([[Prompting-UI]]).
- **One pass for a whole game** is expensive (community reports: 68% of a week's usage in 90 minutes on a smaller build, [[Community-Prompt-Examples]] §6). Holden's plan-first rule still applies: use the spec, but approve phase by phase.

### Holden's version: a spec skeleton for his own game
Use this to turn an approved GDD into a build spec Claude Code can follow. Fill it from the vault; tag every number.
```text
# [GAME] — Build Spec v[N] (for Claude Code + Rojo + Studio MCP)
How to use: build phase by phase; stop after each phase for Holden's review. Numbers are tagged
[USER] (Holden decided, keep exactly), [VERIFIED] (platform fact with source/date), [DRAFT] (Claude's proposal: put in Config).

0. MISSION + HARD RULES
   - Server-authoritative; ProfileStore with schema versions; remotes in one registry with rate limits; --!strict; no deprecated APIs.
   - Art: Blender low-poly per Resources/Art Direction Feedback.md (no Roblox AI meshes, no part-built final props); UI from the painted kit.
   - Code gate (rojo build, specs, selene, stylua) must pass after every phase. No publishing, uploads or commits without Holden.
0.1 FILE TREE: every module with a one-line purpose (Services / Controllers / Shared/Rules / Config).
0.2 BUILD ORDER: phases, each with its gate (spec PASS, DevTest PASS lines, map audit, UI checker, phone test).
0.3 ACCEPTANCE TEST: one paragraph: a new player's first 3 minutes on a phone, with exact texts and timings.
0.4 MAP PIPELINE: MapSpec data module → builder reads only MapSpec → roblox-map-audit + extra checks → captures from fixed cameras [list] → fresh-context verifier per area (prompt in §V below) → fix MapSpec → max 4 rounds.
1. GAME IN ONE PAGE: genre, server size, core loop (Action → Reward → Upgrade, name the stat), session loop, meta loop, social hook, the twist.
2–N. SYSTEMS: one section each: rules, formulas (code blocks + reference values), data fields, remotes, edge cases, exploit cases.
UI SPEC: global style tokens (kit pieces, fonts, stroke, sizes for phone) + each screen's layout + states.
DATA APPENDICES: content tables (items, pets, zones, products with placeholder ids).
REFERENCES: each file → what it shows → which section uses it (third-party refs stay local).
CONFLICTS: rulings where notes disagree.
KNOWN UNKNOWNS: every [DRAFT] tuning knob and how we'll tune it (sim, playtest, analytics).
FINAL CHECKLIST: done-when items per phase.
§V VERIFIER PROMPT: (see below)
```

### The verifier prompt, adapted
```text
You are a strict level/UI reviewer with no prior context. Compare the BUILT captures of [area/screen] against (1) the reference images, (2) the written spec section, (3) Resources/Art Direction Feedback.md.
Score 0–10 each: layout and proportions; route readability; colour zones and variation; props/kit use (no plain parts as final art); landmarks and signage; lighting; scale vs a 5-stud avatar; phone readability; [2 game-specific criteria].
Return JSON only: {"area": "...", "scores": {...}, "total": 0-100, "blocking_issues": [...], "fixes": [{"element": "...", "problem": "...", "change": "exact MapSpec/UI edit with numbers"}]}. No praise.
Pass = total ≥ 85 and no blocking issues. A new verifier every round.
```
Use it alongside the map audit (reachability) and the UI checker (layout maths); those catch what a picture can't.

---

## 2. The VFX session bootstrap
**What it is:** a reusable first message for any new Claude Code session doing Roblox VFX with the VFX Forge plugin: pipeline (Node → Claude Code → `roblox-vfx` skill → Studio MCP → Studio → VFX Forge 1.4.5 → EmitModule → `shared.vfx`), strict scope, then 30 numbered sections.

**Good habits to keep:**
- **Target first, authorisation second.** "Which Studio place?" (never assume the focused window), then "Do you authorise modifications?" If no: inspect and report only.
- **Audit, don't reinstall.** Check what's there; don't upgrade because something newer exists.
- **Never accept a licence or agreement for the user** (VFX Forge's VFX-DL), and never bypass licensing with dev tools.
- **Don't invent APIs; inspect the real runtime.**
- **A minimal runtime test** (init → emit → completion → cleanup → deinit) before complex work, then a cleanup checklist (stop Play, remove temp scripts/parts/effects, check console).
- **Visual result matters:** don't stop at "the code runs"; iterate if it looks weak.
- **A fixed final report form** (environment, plugin, runtime, work, play test, changes: "list only what was actually changed").
- "Don't fabricate PASS results; don't replace a failed component with a fake one."

**Cautions:** it installs a third-party skill with an unpinned `npx skills add` from GitHub and expects Node.js. Review that repo first ([[Third Party Claude Tools Evaluated]]). VFX Forge itself is a third-party plugin; it's not part of Holden's setup.

**Holden version (any Studio session):**
```text
New Studio session for [Game]. Before changing anything:
1. Call list_roblox_studios and ask me which place is the target. Don't assume the focused window.
2. Ask: do I authorise changes in that place? If not, inspect and report only.
3. Audit without reinstalling anything: rojo serve running for the right project? Code gate status? Any Dev*.luau test scripts left in src/? Is the place saved? Report only problems.
4. Work. Test in Play; judge the visual result with screenshots, not just "it runs". Never invent APIs; read the real code.
5. Clean up: stop Play, delete temporary scripts and parts, confirm git status is clean and the console has no new errors.
6. Report: target place; what changed (only real changes); tests and their evidence; anything still open. Never report PASS without the evidence.
I accept any licence, purchase or upload myself.
```

---

## 3. The TDOD master prompts (Discord)
A series of short prompts posted in a dev Discord ("prompts for game developers using AI"): VFX, player movement, combat, map building, bug fixing, AI/NPCs, animation polish, audio, performance, AAA polish, full game review and a master rule. Four were in the pack: the master rule, animation polish, VFX and map building.

| Prompt | Worth keeping | Problems |
|---|---|---|
| **Master rule** ("don't stop because something works… build → test → fix → improve → test again") | The loop and "fix the root cause" | No stop condition or budget: a recipe for burning usage. "Make it cooler/memorable" isn't checkable |
| **Animation polish** | Named failure list (foot sliding, snapping, bad transitions, broken IK, hand/weapon placement, awkward landing, clipping, poor hit reactions); test in real gameplay; batch related animations and test once; "don't report after every tiny change"; final report **FIXED · IMPROVED · TESTED · FOUND · NEXT** | Written for **Unreal** (Motion Matching, Control Rig, Motion Warping, `.cpp` files in the screenshot). Roblox has none of those; use IKControl, Animator priorities and contact sheets instead ([[Prompting-Game-Feel]]) |
| **VFX** | Stages **anticipation → buildup → impact → follow-through → clean fade**; sync to the animation; named anti-patterns (giant random clouds, too much glow/bloom, effects blocking the screen, VFX that don't follow the character, unnecessary shake, laggy counts, generic copied effects); test matrix (idle, moving, attacking, jumping, camera angles, PC/mobile/console) | No numbers: no particle budgets, no lifetimes, no "readable from N studs". "How the hell is this Roblox?" isn't a check |
| **Map building** | Study → blockout → playtest → build → detail → optimise; anti-patterns (random box buildings, giant empty areas, useless rooms, repetitive hallways, fake doors, random props as "detail"); purposeful additions (interiors, shortcuts, alternate routes, rooftops, vertical paths, hidden areas, landmarks); checks (collision, scale, lighting, AI navigation, clipping, floating props, broken routes); **low-usage mode**: don't rescan unchanged files, batch changes, test once, one short report | No art direction, no measurable reachability check. Pair with the map audit and Holden's art rules |

### Holden versions
**VFX** (merges TDOD's stages with the vault's budgets and phase freeze, [[Roblox VFX Review Skill]]):
```text
Make the [effect] for [ability/moment] in [Game]. Build it in stages: anticipation (0–[0.15] s), buildup, impact, follow-through, clean fade, synced to the animation's key frames.
Use only what fits: ParticleEmitters (bursts via Emit on the client), Beams, Trails, a short light flash, a FOV kick or small shake for big moments, layered sound.
Avoid: giant random particle clouds, glow or bloom that whites out the scene, anything covering the player's view, effects that don't follow the character, shake on small hits, copied generic effects.
Budgets: [small hit ≤ 30 / ability ≤ 150] particles, ≤ 1,500 live on screen, lifetime ≤ 20 s, LightEmission ≤ 0.5 on bright skies.
Test: idle, moving, attacking, jumping, from 3 camera angles, at phone size. Run the roblox-vfx-review lint and the phase freeze at anticipation, impact and fade.
Stop when the lint passes and all freeze frames read clearly, or after [3] rounds; then report FIXED · IMPROVED · TESTED · FOUND · NEXT.
```
**Map** (merges TDOD's map prompt with [[Prompting-3D-Assets-And-Maps]] P3):
```text
Improve [area] of [Game] like a real game environment, not an AI blockout. Read Resources/Art Direction Feedback.md first.
Every area needs a purpose: [what players do there]. Add only meaningful structure: shortcuts, alternate routes, vertical paths, a hidden area, a landmark visible from spawn. No random boxes, empty plains, fake doors or props scattered as "detail".
Kit meshes only (no plain parts as final art), crisp zone colours, colour variation, varied trees.
Checks: roblox-map-audit PASS with MapMustReach/MapNoReach tags, no floating props, collision on walkables only, readable on a phone, 4 screenshot angles + 150 px view.
Low-usage mode: don't rescan unchanged files, batch related changes, test once per batch, one short report at the end: FIXED · IMPROVED · TESTED · FOUND · NEXT.
```
**Polish pass with a finish line** (replaces the open-ended master rule):
```text
Polish [system/screen] in [Game] for one pass. Find the 5 biggest problems in feel or clarity (test it in Play on a phone-sized viewport), fix the root causes, batch related changes, and test once per batch. Stop after those 5, or when [the check] passes, whichever is first. Don't report after every small change. Final report only: FIXED · IMPROVED · TESTED · FOUND · NEXT.
```

## Pitfalls
- **Treating a community mega-prompt as approval to clone a game.** It's a structure lesson; Holden's projects need their own design and his decisions.
- **Pasting a 190 KB prompt into a session** without the reference folder it depends on. This one references about 230 images and 4 clips that weren't in the zip.
- **Open-ended "make it better" loops** with no stop rule.
- **Engine mismatch:** check that every tool named in a borrowed prompt exists in Roblox.
- **Installing what a prompt tells you to** (unpinned `npx` skills, plugins) without reviewing it.

## Related
[[Discord-Prompt-Pack-2026-10-05]] · [[Community-Prompt-Examples]] · [[Prompting-Principles]] · [[Gauntlet-Loop]] · [[Prompting-3D-Assets-And-Maps]] · [[Prompting-Game-Feel]] · [[Steal-An-Egg-Teardown]]

## Sources
- `STEAL_AN_EGG_ONE_SHOT_PROMPT.md`, `OneShotInstallForgeVFX.txt` and TDOD Discord screenshots in Holden's Discord prompt pack (local, 2026-10-05). Read in full or in relevant sections; the referenced `reference/` folder was not supplied.
