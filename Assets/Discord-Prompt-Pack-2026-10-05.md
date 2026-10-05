---
tags: [assets/community, prompting/examples, security/audit]
status: reviewed
updated: 2026-10-05
confidence: high
---
# Discord Prompt Pack (2026-10-05)

A zip Holden supplied on 2026-10-05 (two big AI prompts, four Discord screenshots, six Roblox model/place files shared in Discord servers), plus a second batch the same night (three VFX/crate files and a short video) and two more prompt screenshots pasted in chat. Stored locally in `Assets/Community-Drops/2026-10-05-Discord-Prompt-Pack/` (**gitignored**: other creators' work, and the vault repo is public). This note is the catalogue and the safety report. The prompt analysis is in [[One-Shot-Spec-Prompts]].

## TL;DR
- **Safe to keep as reference.** No executables. The Roblox files were parsed offline with Lune (nothing ran); 4 of 6 contain no scripts at all, and the scripts in the other 2 are benign (details below).
- **Most valuable:** `STEAL_AN_EGG_ONE_SHOT_PROMPT.md`, a 1,768-line spec for recreating Steal an Egg from code. Its structure (evidence tags, file tree, build order, acceptance test, map spec + fresh-context verifier loop, conflicts, known unknowns, final checklist) is the best one-shot prompt example in the vault ([[One-Shot-Spec-Prompts]]).
- **Also useful:** a VFX session bootstrap prompt for Claude Code + Studio MCP + the VFX Forge plugin, and a Discord "prompts for game developers" series with a polish loop and an animation-polish prompt.
- **Don't ship any of the Roblox files in Holden's games.** The guardian, pet and GUI files appear to be other games' assets (Steal an Egg guardians, Pet Simulator-style pets, a Steal-a-Brainrot-style HUD) uploaded by a third party; ownership and licence are unknown. Use them to study structure only. The stud props are part-built, which Holden rejects as final art anyway.
- **The `reference/` folder** the Steal an Egg prompt depends on (about 230 images and 4 clips) was **not** in the zip.

## Contents
| File (in the drop folder) | What it is | Scripts | Notes |
|---|---|---|---|
| `prompts/STEAL_AN_EGG_ONE_SHOT_PROMPT.md` | One-shot recreation spec for Steal an Egg (Roblox place 107778070777162) | — | Plain markdown. Tells the builder to use Codex CLI image generation and fresh-context verifier subagents. Some data is credited to a "decompiled client config" from a fan wiki ⚠️ (IP/ToS grey area; don't copy it into a game) |
| `prompts/OneShotInstallForgeVFX.txt` | "Roblox VFX one-shot session bootstrap" prompt | — | Plain text. Asks Claude to verify Node/npm, a `roblox-vfx` skill, the Studio MCP, VFX Forge 1.4.5 and its EmitModule. One install line pulls a third-party skill with `npx skills add https://github.com/nonlooped/roblox-suite` (unpinned; not run) |
| `roblox-files/VFX.rbxmx` | Source of the **VFX Forge 1.4.5** Studio plugin (289 instances: 194 ModuleScripts, the plugin bootstrap, an emitter worker) | 196 | See security review. Bundles Fusion. Its EmitModule carries a "VFX-DL" licence: runtime use in Roblox experiences only, not inside plugins or tools |
| `roblox-files/Animals-Steal A EGG STRXPE.rbxm` | 9 guardian models (Abyss Ocean, Jungle, Volcano, Cosmic, Forest, Desert, Snow, Lake, Prehistoric) with rigs, keyframe animations, sounds and "Z z Z"/alert billboards | 0 | 8,069 instances (6,370 animation poses). Looks like Steal an Egg's guardians |
| `roblox-files/Main_Gui_Strxpe.rbxm` | A full HUD + 23 interface frames (Brainrot-style: money/friend boost/power, rebirth, index, daily missions, boss HUD, distance marker with luck) | 2 | 3,669 instances, 774 UIStrokes, 323 UIGradients |
| `roblox-files/Premium Backpack UI Set.rbxm` | Backpack/inventory UI: hotbar card template, grid, search, sort, equip/place best, Robux capacity upgrades | 0 | 321 instances |
| `roblox-files/Pets Asset Pack.rbxl` | A place with about 20 pet models (Mega King Ant, Mega Gumball Machine, Black Dominus, Floppa, Dragon, Ultra Capybara…) | 0 | Mesh pets in a Pet Simulator-like style; meshes referenced by asset id |
| `roblox-files/StudPack1.rbxl` | Stud-style part-built props: pine/palm trees, bush, rocks, campfire, shop, car, bed, street lights… | 0 | 3,403 Parts; classic stud look |
| `screenshots/*.png` (4) | Discord posts explaining the VFX files, the Steal an Egg prompt, and the TDOD prompt series | — | Viewed |
| `scan/*.txt` | My offline dumps: instance trees, class counts and every script's source | — | For audit only |

## Batch 2 (sent the same night)
Files Holden added straight from Downloads, stored in `batch-2/`:
| File | What it is | Scripts | Notes |
|---|---|---|---|
| `roblox-files/WeatherVfx.rbxm` | 5 weather/"event" effects: Lighting (storm), Clover, Sand Brush, Snow, Void. 49 ParticleEmitters, 33 Beams | 0 | Each effect is about 190–385 particles/s and about 220–370 live particles (my estimate from rate × lifetime). Emitters run at 35–50/s each, above the vault's ambient guide of ≤ 20/s per emitter ([[VFX-Particles-Beams-Trails]]) |
| `roblox-files/vfx.rbxl` | A VFX showcase place: "Fire Explosion" (20 emitters), "Crimson VFX" (4 emitters on a mesh) and a "Purple Blue Mega Effect" rig with wings | 1 | The one script re-fires the explosion's emitters every 3.3 s with `wait()` (deprecated; demo only). **The mega effect is 152 emitters, about 7,100 particles/s and roughly 5,800 live**: about 4× the vault's ~1,500 live-particle phone budget. A PC showcase, not shippable |
| `roblox-files/Crate Scripted.rbxl` | 3 crates (dark wood, frosted silver, blue/gold glow), each a Base + hinged Top MeshPart with an AnimationController and a 157-keyframe open animation | 0 | Animation is keyframed in AnimSaves, so it plays from an Animator, no code |
| `video/crate-open-animation-0701.mov` (+ contact sheet) | 1.9 s, 854×480, 60 fps clip of the crate animation | — | Frames reviewed: the middle crate drops in tilted, bounces and settles, wobbles (anticipation), the lid pops open and over-rotates back, then slams shut with a small dip and a final settle. Squash-and-settle timing worth copying for a crate/egg reveal ([[Prompting-Game-Feel]], [[Reward-Schedules]]) |

**Batch 2 security:** parsed offline the same way; the only script is the 182-character emitter loop above. No asset-id loaders, no network calls.

### Two more TDOD prompts (pasted in chat, not saved as files)
Holden pasted two more screenshots from the same "TDOD" Discord series: a **VFX master prompt** (build in stages anticipation → buildup → impact → follow-through → clean fade; avoid giant random particle clouds, too much glow/bloom, effects blocking the screen, floating VFX that don't follow the character, unnecessary shake, laggy counts and generic copied effects; test idle/moving/attacking/jumping, several camera angles, PC/mobile/console) and a **map-building master prompt** (study → blockout → playtest → build → detail → optimise; no random box buildings, giant empty areas, useless rooms, repetitive hallways or fake doors; add interiors, shortcuts, alternate routes, rooftops, vertical paths, hidden areas, landmarks; check collision, scale, lighting, AI navigation, clipping, floating props, broken routes; a "low-usage mode" that batches changes and reports once). Analysed in [[One-Shot-Spec-Prompts]].

## Security review (2026-10-05)
**Method:** listed the zip before extracting; extracted to the session scratchpad; parsed every `.rbxm/.rbxl/.rbxmx` with Lune's `@lune/roblox` (deserialise only, no execution); dumped all script sources; searched for backdoor patterns: `require(<number>)`, `getfenv/setfenv`, `loadstring`, `HttpService` calls, `InsertService/LoadAsset`, `MarketplaceService` prompts, obfuscation (`string.char`, escape runs), `_G/shared`, `Kick/BanAsync`, webhooks, Discord, DataStores.

| File | Findings | Verdict |
|---|---|---|
| Animals, Pets Asset Pack, Premium Backpack UI, StudPack1 | No scripts of any kind | Safe (assets only) |
| Main_Gui_Strxpe | `GlowAnimator` (rotates and pulses a sunburst image, 563 chars) and a tutorial rig's `Animate` (Roblox's standard animate script) | Safe |
| VFX.rbxmx (VFX Forge) | No `require(<id>)`, `loadstring`, `getfenv`, webhooks or script-source writes. `HttpService` is used for `GenerateGUID` and to fetch Roblox's official API dump from `setup.rbxcdn.com`; `MarketplaceService:GetProductInfo(133927382668067)` reads its own asset description for an update check; `StudioService:PromptImportFiles` imports flipbook images; a Discord invite appears in its update-log UI; `shared.vfx` is its runtime API | Looks like the genuine plugin. Prefer installing it from its official Creator Store listing over a Discord-shared file, since a shared copy could be altered in future versions ⚠️ verify the official listing |
| Batch 2 (WeatherVfx, vfx, Crate Scripted) | One demo script (emitter loop with `wait()`); everything else is emitters, beams, meshes and keyframes | Safe |
| The two prompts | Plain text. They contain instructions for an AI agent (normal for prompts), nothing hidden. The VFX one wants Node.js and an unpinned `npx` skill install | Safe to read. Don't run the install lines without reviewing that repo ([[Third Party Claude Tools Evaluated]]) |

## UI structure worth studying (from the GUI files)
- **HUD layout (Main_Gui):** left column = values (Money, Friend Boost, Power) above a button stack (Invite, Rebirth, Settings, Index, Rewards, Shop with a rotating glow); top = Home and Sell; right = Starter Pack and Pro Pack offer buttons; plus a notification holder, an events display, server luck, a boss health bar ("Click to deal damage!"), a critical-hit "Click To Boost!" bar and a distance marker showing the current reward and luck multiplier. Compare with the Paper Plane Toss HUD in [[Roblox Mobile UI Layout]].
- **Backpack (Premium Backpack UI):** a hotbar card template with amount, star rating, type, equipped and farming tags, a $/s line, level and a favourite icon; the panel has search, sort by rarity, Place Best, Equip/Unequip Selected, a capacity counter ("0/500") and **Robux capacity upgrades priced against a "Worth" anchor** ("+1,500 Backpack" R$109 "Worth 349"; "+INF" R$279 "Worth 1299"). The same anchor-price trick as the shop's struck-through "worth" in [[Shop Gauntlet Workbench]] and [[Pricing-Psychology]].
- Heavy use of UIStroke (774) and UIGradient (323) confirms the "every element outlined + gradient" simulator look ([[UI-Polish-And-Juice]]).

## How to use this pack
- **Read** the prompts for structure and copy the patterns ([[One-Shot-Spec-Prompts]]).
- **Open** the GUI/guardian files in a throwaway Baseplate (not a game place) if you want to look at them in Studio, with scripts disabled on insert ([[Asset-Creation-Workflow-And-Marketplace]] audit routine).
- **Don't** publish or reuse these assets in Holden's games. Don't install VFX Forge or the `roblox-suite` skill without Holden's decision.

## Related
[[One-Shot-Spec-Prompts]] · [[Community-Prompt-Examples]] · [[Steal-An-Egg-Teardown]] · [[Third Party Claude Tools Evaluated]] · [[Asset-Creation-Workflow-And-Marketplace]] · [[VFX-Particles-Beams-Trails]]

## Sources
- Holden's zip `{39D2270D-…}.zip` (2026-10-05), contents as listed; screenshots are of Discord posts by "TDOD" and others (names as shown in the images).
- Lune `@lune/roblox` (offline Roblox file parsing), used via Rokit.
