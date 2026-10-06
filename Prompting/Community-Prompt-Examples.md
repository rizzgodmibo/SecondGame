---
tags: [prompting/examples, reference/community, meta/ai-workflow]
status: draft
updated: 2026-10-04
confidence: medium
---
# Community Prompt Examples (X, TikTok, YouTube, DevForum, GitHub)

Real prompts and prompting habits other Roblox developers share, collected 2026-10-04, with what's good, what's missing, and a version rewritten for Holden's setup (Claude Code + Rojo + Studio MCP, vault rules). Prompts by others are **paraphrased**, not copied. Evidence type for everything here: **practitioner self-report or vendor content**, not tested in Holden's games. The official rules are in [[Prompting-Principles]].

## TL;DR
- **What the people with real results say is the same everywhere:** build one system at a time, test it, paste the exact error and what you did back to the AI, and re-prompt with specifics. The creators with the biggest engagement on this (andythropic, 30K and 16K likes) say their game took months of this, not one prompt.
- **"One-shot" posts rarely show the prompt.** The 80K–460K-view "Opus 5.5 one-shot this game" posts on X show results only. Treat them as capability demos, not methods.
- **The best shared prompt is a spec, not a wish:** counts, types, behaviours and a delivery format ("import 1:1, with a setup script"). Marvin's 475-character sword prompt is the clearest example.
- **Name reference games and features up front.** Scuppy's game got reworked mid-build when he finally said which games he meant; RoDev's test showed Claude would have needed no corrections if the first correction had been in the first prompt.
- **Usage is the real limit.** One creator used 68% of a week's usage in 90 minutes at extra-high effort; a vendor says one one-shot test used about 20% of a weekly Max limit. Scope prompts and pick effort deliberately.

## Patterns worth copying

### 1. Spec, not wish (asset + VFX + animation)
**Source:** Marvin (@marvin_x1), X, 2026-09-30, describing a 3-minute "Roblox model generation with Claude" video (6.5K views).
**What the prompt contained (paraphrased):** the weapon's look (a blade in an ice-blue particle spiral; a second version with a teal "soulfire" blade and a lantern charm); exactly 4 attacks (1 basic slash, 2 advanced, 1 ultimate); player animations that move "like the weapon" in the same colour; and a delivery line asking for VFX settings that import into Roblox 1:1 with a setup script. A follow-up asked for a reaction set (dash, block, dodge, stun, knock-up, caught-in-ult, death) on a preview rig with buttons, plus an installer script.
**Why it works:** every output requirement is countable and checkable, and "import 1:1" makes Claude build for Roblox rather than a pretty preview.
**Holden version** (keeps his art rules; asset-prompt template in [[Prompt-Library]] §1):
```text
Make a Roblox-ready [ITEM] for [Game]. Style: clean flat-shaded low-poly, colour variation, read Resources/Art Direction Feedback.md. No Roblox AI meshes.
LOOK: [shape, colours, one signature detail]. Under [N] triangles, one atlas texture ≤ 1024 px, pivot at [grip], [N] studs long.
ACTIONS: exactly [4]: [1 basic, 2 advanced, 1 ultimate], each with a VFX burst from the roblox-vfx-review building blocks and a sound from my catalogue.
PLAYER ANIMATIONS: [R15], upper body only for attacks (Action priority) so walking still plays; check each as a contact sheet.
DELIVERY: must work in Roblox 1:1: a setup ModuleScript with [Item].play(character, "[Attack]"), a preview place or rig with one button per action, and a list of every asset to import and where it goes.
Ask me questions first if anything is unclear. Show renders, contact sheets and phase-freeze frames with your honest critique before I review.
```

### 2. One system at a time, with an error loop
**Sources:** andythropic, TikTok, 2026-04-23 (30.2K likes, 442K plays) and 2026-05-11 (16.1K likes, 325K plays); RoDev, YouTube, "Which AI Can Make the BEST Steal a Brainrot GAME?" (285K views, 2026-03-14).
**What they say:** don't ask for the whole game; give one small, specific task; test it in Studio; when it breaks, paste the error **plus what you clicked or did**, and say what to change. Say exactly what the system does, where it goes, how the player interacts with it, and the structure you want. RoDev's lesson: be specific enough that the first prompt already contains what you'd otherwise send as corrections, and know enough scripting to fix trivial errors yourself.
**Holden version:** this is already the vault method ([[Prompting-Gameplay-Systems]] P1–P2, [[Prompting-Debugging-And-Testing]] P1). The one-line correction form:
```text
[System] broke. What I did: [clicked/pressed/walked to X]. What happened: [symptom]. Error from Output: ### [paste] ###. Expected: [behaviour]. Find the root cause, change only [system], and show me the passing run.
```

### 3. Refactor spec (config split + UI templates)
**Source:** andythropic's on-screen example prompt (TikTok, 2026-04-23, about 1:02).
**What it asked (paraphrased):** split the unit config into two ModuleScripts: a client one in ReplicatedStorage (image, display name, training time) and a server one in ServerStorage (damage, HP, range). Then change the training scripts so that instead of looking up each unit's own hard-coded UI frame, they clone a shared template and fill its labels from the client config. The same for every other template (slots, attack radius, inventory).
**Why it works:** it names the exact modules, where each lives, which fields go where, and the pattern to replace. It also keeps stats you don't want datamined on the server ([[Module-Architecture]]).
**Holden version:**
```text
Refactor [system] in [Game]. Plan first, then stop.
1. Split Config.[X] into [X]ClientConfig (ReplicatedStorage: display data only: [fields]) and [X]ServerStats (ServerStorage: [fields]). Nothing the client doesn't need leaves the server.
2. Replace the per-item hard-coded UI frames with one template per panel in [location], cloned and filled from [X]ClientConfig.
3. No behaviour change: the same values and the same UI as before. Show before/after screenshots and the code gate result.
```

### 4. The clone brief (and why to add a twist)
**Source:** RoDev's fixed prompt used across ChatGPT, Gemini, Claude, Grok and DeepSeek: explain what the game is, the output format, concrete counts (8 bases, at least 6 slots each, 10 units from $1/s common to $1,000/s legendary), then "make sure it's balanced". Claude scored 9/10 with no corrections in that test; the creator still asked for everything "in one script", which is the opposite of good structure.
**Take:** concrete counts and price ranges made every model's output comparable and testable. But near-clones are deprioritised by Roblox's recommendations ([[Discovery-Algorithm]]), and "make it balanced" is not a check.
**Holden version:** use the counts-and-ranges style inside [[Prompting-Concept-And-Design]] P4 (economy with a Lune sim) and always add the twist line from P1.

### 5. Let another AI write the prompt
**Sources:** Code Coach (@MyCodeCoach), X, 2026-09-27: a one-line game idea is expanded by ChatGPT/Claude into a full prompt for a UI tool (vendor tool; promotional). lolstudios33, TikTok, about 2026-09-26 (3.7K likes, 74.8K plays): a Blender MCP model in 2 prompts; the prompt was generated by another AI and then hand-edited; references from the game's old design were attached; and the AI was told to ask questions when unsure.
**Take:** matches the vault's prompt-writer loop ([[AI-Assisted-Workflow]] §1). The useful extra: **edit the generated prompt yourself** and keep "ask me questions when you're not sure".
**Holden version:**
```text
Write the prompt I should give Claude Code to build [THING] for [Game]. Use the skeleton in Prompting/Prompting-Principles.md and the matching Prompting page. Fill every bracket from the vault where you can; where you can't, list the question you need me to answer. Don't build anything.
```

### 6. Name the reference games up front
**Source:** Scuppy, YouTube, "I Asked Opus 5.5 To Make My DREAM Game!" (2026-10-03, about 19K views). He sent a long written design with no references at extra-high effort. Mid-build he added ideas through chat (Claude picked them up), and an hour and a half in he clarified the genre he meant ("like Dead Rails and A Dusty Trip"), which forced a rework. A vague "make the UI look like a billion-dollar company made it" improved the UI; a one-line "make a high CTR thumbnail" produced something he called "insanely bad". He used 68% of his weekly usage in 90 minutes and hit the limit at 2 hours.
**Take:** name the reference games, the genre structure and the camera in the first prompt; send thumbnails to an image model with a real spec ([[Prompting-Launch-And-Marketing-Art]]); budget usage before long runs.

### 7. Formula prompts for quick prototypes (vendor blogs)
- **Five-part game prompt** (Obby blog, 2026-08-07): make a [genre] game where players [core action]; they progress by [progression]; include [three concrete systems]; a round ends when [win/loss]; use a [visual style] theme. Plus "describe one complete minute of gameplay before adding complexity".
- **Seven-component prompt** (SEELE blog, 2026-08-06): player goal, prototype scope (one mechanic/room/quest/NPC), context, rules and state, constraints, output format (table, beat sheet, pseudocode), success evidence. Templates for a mechanic, a level beat sheet, a quest state machine (available → accepted → active → blocked → completed → abandoned) and a bounded NPC (signals, states, cooldowns, fallback). Tuning values are labelled hypotheses.
**Take:** good for brainstorming one mechanic before planning it properly. The state-table idea is worth stealing for quests and NPCs (used in [[Prompting-Gameplay-Systems]] "More examples").

### 8. Scoped Studio MCP questions
**Source:** boshy_z's Roblox Studio MCP thread, DevForum, 2025-06-11: example asks like "what's the structure of this game?", "find scripts with deprecated APIs", "create 50 test NPCs in a grid", "take a screenshot and tell me what looks off", "run a playtest and fix any errors". Users reported Claude trying to read every script (including core scripts), which blew the context.
**Take:** say which folder or scripts to read; use a subagent for wide sweeps ([[Prompting-Principles]] rule 11).

### 9. Ideation conversation (older but sound)
**Source:** "Game Ideation with ChatGPT", DevForum community tutorial, 2023-07-24. Sequence: fresh chat → which genres are popular → subgenres → break the game into its core elements → technical and design challenges → what keeps players coming back → honest critique → come back with each update.
**Take:** the same order as [[Prompting-Concept-And-Design]] P1 → P5, with the critique step done in a fresh session.

### 10. Roblox's own example prompts (Assistant docs)
Official examples worth reusing as one-liners (paraphrased): fireballs that explode on impact; random team assignment into four colours; a power-up toggled with Q that triples jump height; an NPC that patrols between two points and chases players within 10 studs; a top-down camera locked on the player; a health bar that turns red below 20%; scatter 0–5 mushrooms near each tree; a day/night cycle with lights on at 7 pm and off at 8 am; a physics rope bridge with 10 planks; smoke on every chimney. For asset generation: start with the object's name, then add appearance one step at a time (mailbox → blue metal mailbox → weathered blue metal mailbox with a red flag), and leave out camera, lighting and "high quality" words. For procedural models: name the editable parameters and how parts respond when they change.
**Take:** exact names, numbers and conditions in one sentence. Holden doesn't use Assistant's mesh generation, but the sentence style works in Claude too.

### 11. Already in the vault: reference-first UI and "no one-shot" advice
palm_dev's TikTok "AI UI that doesn't look bad" (reference screenshots, say what you like, design in chat first) and jakeinatx's "no AI one-shot" advice are already catalogued in [[TikTok-Reference-Library]]; they agree with patterns 2 and 5. The UI method is written up in [[Prompting-UI]].

## Tools and skill packs seen (not installed)
| What | Notes |
|---|---|
| AshExplained/roblox-skills (GitHub, MIT, about 15 stars) | 40 Claude Code skills across the lifecycle, including concept → PRD → small playtestable vertical slices, a `handoff` skill for session summaries, and a `write-a-skill` skill. Ideas worth borrowing: the PRD → slices step and the handoff summary. |
| brockmartin/roblox-game-skill (GitHub, about 192 stars, no licence shown) | One big skill: 16 references, 7 genre templates, workflows including a 5-attempt debug loop, a 60+ item publish checklist and an A–F code review. |
| RBSmithy skill, ClaudeBlox | Similar "Claude as Roblox dev" packs; example asks like "create a server-authoritative inventory system" or "review this RemoteEvent for exploits and rewrite it safely". |
| Paid "AI for Roblox" wrappers, AI thumbnail generators (Clicklab, Vizzbees on TikTok) | Promotional. jasperdevs's widely shared setup article (X, 101K views) warns that third-party AI wrappers can see your data and game and cost more than a Claude plan. The thumbnail tools' sample prompts are one generic line, against the vault's "true and exciting" rule ([[Thumbnails-And-Icons]]). |
Per [[Third Party Claude Tools Evaluated]], nothing third-party is installed without reading it first and Holden's OK.

## Pitfalls
- **Copying a hype post's claim as a method.** No prompt, no repeatable result.
- **One giant script** (RoDev's format) is fast for a demo and bad for anything you'll update ([[Module-Architecture]]).
- **Old tooling in older videos:** copy-paste chat workflows predate the Studio MCP and Rojo loops; keep the prompt lessons, not the workflow.
- **Paraphrase, don't paste others' prompts into the vault wholesale**; credit the source.

## Related
[[Prompting/_Index|Prompting]] · [[Prompting-Principles]] · [[Prompt-Library]] · [[AI-Assisted-Workflow]] · [[TikTok-Reference-Library]] · [[YouTube-Reference-Library]] · [[X-Reference-Library]]

## Sources
- andythropic (TikTok): <https://www.tiktok.com/@andythropic/video/7632072838253530398> (2026-04-23) · <https://www.tiktok.com/@andythropic/video/7638783229322939679> (2026-05-11). Subtitles read; one frame viewed at about 1:02.
- lolstudios33 (TikTok), Blender MCP in 2 prompts: <https://www.tiktok.com/@lolstudios33/video/7690308892881882381> (subtitles read)
- Marvin (X): <https://x.com/marvin_x1/status/2105363013293502941> (2026-09-30, post text read; video not watched)
- Code Coach (X): <https://x.com/MyCodeCoach/status/2104291950408937500> · Belt (X): <https://x.com/bletDemonJH/status/2104871105752391780> · hiraeth (X): <https://x.com/WoahWurdz/status/2102487879809126834> · SuperbulletAI (X, vendor): <https://x.com/SuperbulletAI/status/2102525686644670844> · jasperdevs (X article): <https://x.com/jasperdevs/status/2024686068885229661>
- Scuppy (YouTube): <https://www.youtube.com/watch?v=IFtKCN8jw6o> (transcript read in full) · RoDev (YouTube): <https://www.youtube.com/watch?v=uzOyfbTUyFk> (transcript read in full) · SmartyRBX (YouTube, chapters only; transcript didn't load): <https://www.youtube.com/watch?v=0ENeVVC9QT0>
- DevForum: "Game Ideation with ChatGPT" <https://devforum.roblox.com/t/game-ideation-with-chatgpt/2484078> · Roblox Studio MCP v2.6.0 thread <https://devforum.roblox.com/t/v260-roblox-studio-mcp-speed-up-your-workflow-by-letting-ai-read-paths-and-properties/3707071>
- Roblox, Assistant prompt guide (creator-docs source): <https://github.com/Roblox/creator-docs/blob/main/content/en-us/assistant/prompt-engineering.md>
- GitHub: <https://github.com/AshExplained/roblox-skills> · <https://github.com/brockmartin/roblox-game-skill> · <https://github.com/gogolumo/rbsmithy-roblox-claude-skill>
- Vendor blogs: Obby, "25 Roblox Build Prompts" <https://www.obby.fun/blog/roblox-build-prompts> · Obby, "Lua Code Generator" <https://www.obby.fun/blog/lua-code-generator> · SEELE, "Roblox AI Game Prompts" <https://www.seeles.ai/resources/blogs/roblox-ai-game-prompts> · Roxlit, "How to Use Claude Code with Roblox Studio" <https://roxlit.dev/blog/how-to-use-claude-code-with-roblox>
