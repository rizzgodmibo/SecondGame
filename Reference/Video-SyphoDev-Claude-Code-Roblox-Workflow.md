---
tags: [reference/video, meta/ai-workflow]
status: draft
updated: 2026-10-04
confidence: medium
---
# Video Breakdown: "How to Make a Roblox Game With AI (Claude Opus 5.5 Full Tutorial)" (SyphoDev)

- **Link:** <https://www.youtube.com/watch?v=afuKhenJldY> · channel **SyphoDev** (473 subs, 169 likes when watched) · **24:45** · uploaded **2026-10-04**
- **Watched:** 2026-10-04, in full. I read the whole auto-caption transcript and reviewed **about 300 frames** (one every 5 s, as contact sheets).
  Then I read **37 key frames** at full size. The frames are saved in `Assets/Reference-Captures/SyphoDev-AI-Workflow/` (local only, gitignored: third-party video).
- **What it is:** a creator's tour of their **Claude Code + skills + MCP + external-API** system for building whole Roblox games
  (code, UI, maps, VFX, sound, animation, 3D models). The video is talking-head with motion-graphic overlays. It includes short real
  screen-recordings of Studio's MCP settings, the Claude Code desktop app, the Creator Hub and the Open Cloud docs.
- **Evidence type:** **practitioner self-report**. No skill source code is shown and none is downloadable. The skills are promised free "at 1,000 subscribers".
  The description advertises a **paid course** (payhip). Treat every workflow claim as a hypothesis. Platform and third-party facts that I
  checked are marked ✅ below.

## TL;DR (what to act on)
- **Architecture:** Claude is the "brain". **Every discipline gets its own skill with its own checker** (code, UI, map, VFX, sound,
  animation, 3D), plus one "manager" skill that runs research → design → assembly. The pitch is that one-AI-writes-everything-as-code games
  "all look the same".
- **Skills should ship tested scripts and a growing rules list.** When something breaks, the fix and *why* get written into the skill, so the
  next session can't repeat the mistake. This matches the vault's own "write the fix down" rule.
- **Make as much of the game checkable while it is not running as possible.** Pure-number rules modules are tested off-Roblox. Every change must pass
  **Rojo build → tests → linter (Selene) → formatter (StyLua)** before Studio sees it, and **the empty scaffold must pass all four first**.
- **UI from one spec → preview image + UI file + build script**, so the preview can't drift from the game. A **"depth stack"** goes on every panel
  (blue-tinted drop shadow, face gradient, top lift/highlight, *uniform* outline). An automated checker runs at 4 screen sizes.
  **Mixed outline thickness is the #1 tell of AI-made UI.**
- **Maps are measured, not eyeballed.** Raycasts plus the game's real movement numbers (from config) drive 9 automated checks: floating, no footing,
  unreachable, shouldn't-reach, no way out, sight lines, overlaps, uneven rings, short falls vs ragdoll.
- **VFX:** don't generate from scratch. **Harvest free toolbox packs → classify into building blocks → compose.** Verify bursts with a
  **"phase freeze"**: fire the effect, wait an exact time, freeze the particles, and check start/middle/end.

## Chapters (from the description)
| Time | Chapter |
|---|---|
| 00:00 | How to make a Roblox game with AI |
| 00:56 | Claude Code |
| 01:41 | Claude Code skills |
| 04:00 | MCPs: connecting Claude to Roblox Studio |
| 05:31 | The AI models and APIs I use |
| 08:18 | Setting it all up |
| 10:05 | Every skill explained |
| 23:36 | Putting it all together |

---

## 1. Framing (00:00–00:56)
- Problem: most "AI makes a game" videos ask one AI to emit everything as code. Map, UI and models are all scripted parts, so
  the output looks samey.
- Their flip: Claude orchestrates, but each discipline has **its own workflow, tools and self-check**. There are three building blocks:
  **skills, MCPs, APIs**.

## 2. Claude Code (00:56–01:41)
- Everything runs through **Claude Code in the Claude desktop app**, not the chat website. The reason: it runs locally, so it can run Python,
  drive Blender, edit files and drive Studio, where the website can only hand you text to paste.
- Needs at least a **Claude Pro plan**, stated as "around £18–20/month" (⚠️ verify current pricing on claude.com/pricing).
- Model: **Claude Opus**, because long jobs need it to track many moving parts. (Matches the vault's model table in [[AI-Assisted-Workflow]] §3.)

## 3. Skills (01:41–04:00)
![](../Assets/Reference-Captures/SyphoDev-AI-Workflow/02-0222-skillmd-loading-tiers.jpg)
- A skill = **a folder of instructions + tools** that Claude loads when a task needs it. Its core is `SKILL.md`, with `name` +
  `description` frontmatter. The example on screen is a `map-design` skill whose description starts "Use when building or changing a Roblox map…".
  Its body is a numbered "How to build a map" procedure ("Read the movement numbers", "Block out, then prove it").
- **Three loading tiers** (frame 02:22):
  - **always read:** the name + description of every skill, all the time
  - **only when needed:** the full instructions
  - **references:** only when that step comes up
  → so ~20 skills can be installed without bloating context.
- **`scripts/` folder (the part people skip):** the skill ships **pre-written, tested Python** instead of Claude rewriting code every run.
  The loop (frames 02:45–03:05): *Claude hits an issue → fixes it → saves the script → never again*. Every breakage becomes
  **a rule with the reason why**.
- **Making one:** create a folder under `.claude/skills/`, add `SKILL.md` with name + description, then write how you want the job done. "It's
  just a big prompt". Or run the built-in **skill-creator** skill: it interviews you and drafts the first version. Then iterate by
  testing repeatedly. Updating or running is "just ask Claude".
- Vault cross-check: this matches how skills load in this Claude Code install. The `anthropic-skills:skill-creator` skill
  exists here.

## 4. MCPs (04:00–05:31)
![](../Assets/Reference-Captures/SyphoDev-AI-Workflow/04-0452-which-mcp.jpg)
- MCP = Model Context Protocol, a standard way to plug app tools into Claude.
- Main one: **Roblox Studio's built-in MCP server.** Claude can create objects, set properties, run code in Studio, take screenshots and start a
  playtest.
- **Which MCP:** they started with a third-party Roblox MCP that **couldn't reach the running game**. The built-in one has **proper play-mode
  tools**, so they switched. Because the built-in one **sometimes breaks**, their workflow **falls back to the third-party one automatically**.
- **Code lives in files, synced into Studio with Rojo**, so Claude can test code before Studio even opens.
- General advice: MCPs exist for many apps (Figma, Blender and Discord icons are shown on screen). Worth learning.

## 5. AI models and APIs (05:31–08:18)
![](../Assets/Reference-Captures/SyphoDev-AI-Workflow/11-0748-decimate-then-bake.jpg)
- Rule: **Claude writes text. It can't paint or sculpt**, so images and 3D models go to other AIs via API. **"Each API: one job, one file back."**
  Everything else happens locally.
- **Images and icons: Cloudflare Workers AI running `flux-1-schnell`** (free tier, fast, and doesn't spend GPU hours).
  - ✅ Verified 2026-10-04: a 12B-parameter rectified-flow text-to-image model. `steps` max 8 (default 4), prompt up to 2,048 chars, returns base64 JPEG.
    Workers AI free allocation is **10,000 neurons/day**, then $0.011 per 1,000 neurons. flux-1-schnell is priced at **$0.0000528 per 512×512
    tile + $0.0001056 per step**. Model terms are Black Forest Labs' (⚠️ verify commercial-use terms for game assets).
- **3D: Hi3DGen** (repo `Stable-X/Stable3DGen`), open source, **single image → 3D mesh**.
  - ✅ Verified: **MIT licence**. It adapts Microsoft TRELLIS and removes NVIDIA-licensed dependencies (kaolin, nvdiffrast, flexicube) so it can be used
    commercially. The repo is marked WIP. GPU/VRAM needs aren't documented on the README.
  - **Licence screening ruled other models out:** **Tencent Hunyuan3D's licence excludes the UK** (the creator is UK-based).
    ✅ Verified: the Hunyuan3D-2 licence territory is worldwide *excluding the EU, the UK and South Korea*. It also requires a separate
    commercial licence above **1M monthly active users**. **Holden is also UK-based → Hunyuan3D is not usable for him.**
    (The Blender MCP on this PC exposes Hunyuan3D generation tools. **Don't use them** for Holden's games.)
- **GPU: Kaggle notebooks** because the creator's own GPU is weak. Claimed **30 free GPU hours/week** and **~100 GPU-seconds per asset**.
  - ✅ Verified: the quota resets weekly and is **30 h or sometimes higher**. Sessions run up to 9 h. GPUs are Tesla P100 (16 GB) or 2× T4.
  - My arithmetic, not a test: 30 h ≈ 108,000 s ÷ ~100 s ≈ **~1,000 assets/week** of GPU time, ignoring setup/model-load overhead.
- **The catch:** Hi3DGen returns **~600k faces**. ✅ Roblox's limit is **20,000 triangles per mesh** (already verified in vault).
  Claude runs **headless Blender** to decimate to **~6k triangles** (later stated as "60:1 → 6–10k"). Detail lost in decimation is **baked
  back on as a texture**. Colour is painted from a small spec rather than guessed.
- **Not everything goes this route:** hard-edged items (crates, guns) are **built directly in Blender** (frame 08:00, "Colour / Crates + guns").
- **Uploads: Roblox Open Cloud API.** With a key, finished models and images upload straight into the account, ready in Studio.

## 6. Setup walkthrough (08:18–10:05)
![](../Assets/Reference-Captures/SyphoDev-AI-Workflow/14-0842-studio-mcp-quick-connect.jpg)
1. **Studio MCP:** in Studio, open the **Assistant** panel → **⋯** → **Manage MCP servers** → toggle **"Enable Studio as MCP server"**.
   Under **Quick connect** the options shown are *Antigravity, ChatGPT (codex), Claude Code CLI, Visual Studio Code*. Pick **Claude Code CLI**
   and copy the command. It's a `claude mcp add --transport stdio Roblox_Studio -- "cmd.exe" "/c" … %LOCALAPPDATA%\Roblox … mcp.bat` line.
   In a Claude Code session, paste it with *"I have an MCP running, use this to connect."* Studio warns that connecting a third-party LLM
   shares data with that provider. **This matches the vault's existing setup** (`Roblox_Studio` → `mcp.bat`, see [[Roblox Studio MCP Quirks]]).
2. **Open Cloud key:** Creator Hub (create.roblox.com) → **All tools** → **Open Cloud API** → **API keys** → follow the documented steps (Creator
   Dashboard → API Keys → Create API Key → name it → pick API system + operations → optionally restrict by experience). They didn't show
   their own key screen.
3. **Never paste the token into Claude Code chat.** It gets stored in the chat history. Instead ask Claude: *"I have a Roblox API key to let you import
   assets into my game. Tell me how to store it as a secret variable on my machine so you can access it without it being in the chat."* Then run
   the terminal commands it gives. This matches [[Keeping API Keys Out of Git]], which records that a key pasted into chat was treated as
   exposed and regenerated.
4. If replication breaks, ask Claude Code to debug it.

## 7. Every skill (10:05–23:36)

### 7.1 Code skill (10:05–11:57)
![](../Assets/Reference-Captures/SyphoDev-AI-Workflow/18-1107-four-checks-before-studio.jpg)
- **The hardest problem: Claude can't watch a running game.** Their claim: screenshots only work in edit mode, and **the output log is the only
  thing that comes out of a running game.** ⚠️ This conflicts with the vault's local observation that UI still captures in play mode
  ([[Roblox Studio MCP Quirks]]). The behaviour may differ by MCP version or window state. Re-test.
- Rule: **as much of the game as possible must be checkable while it is not running.**
  - **Game rules** (damage per hit, upgrade costs…) live in **their own folder as plain numbers, with no Roblox objects**, so they're unit-tested on
    the PC without Roblox.
  - **4 checks before Studio:** ① **Rojo build** (assembles the game, catches broken files in ~1 s), ② **tests** (rules still hold),
    ③ **linter** (sloppy code), ④ **formatter**.
  - **The empty scaffold must pass all four before any game code is written**, otherwise real mistakes can't be told apart from AI slop.
- **Rules from a rebuilt game** (their first version died from Studio/file drift):
  1. **Code lives in files, never typed into Studio.**
  2. **Every tweakable number** (speed, damage, prices) **lives in one config folder**, so balancing = changing data.
  3. **All client↔server messages go through one file**, so every remote name is written down in one place.
  4. **A list of traps that each cost real days.**
  (The narration says "five standard rules" but the slide lists four, the fourth being the traps list.)
- Vault cross-check: Holden's stack already does ①–④ (`rojo`, `selene`, `stylua` via Rokit; `Config.luau`; [[Studio Only Dev Test Scripts]];
  the `roblox-dev:roblox-testing` skill covers TestEZ). What's **new** is the hard gate *"scaffold green before game code"* and *"pure-number rules modules testable outside Roblox"*.

### 7.2 UI skill (11:57–14:40)
![](../Assets/Reference-Captures/SyphoDev-AI-Workflow/21-1243-ui-depth-stack.jpg)
- **No design tool.** A design is just a picture, and the real UI drifts from it. Instead **one spec produces three things: a preview image, the
  UI file, and a script that builds it in Studio**. They can't disagree on size or colour.
- **Depth stack**, applied automatically to every panel and button:
  **shadow** (offset slightly, **tinted blue**), **gradient** on the face, **lift** from the top, **outline of the same thickness everywhere**.
  Their claim: this is most of the gap between flat and professional UI. **"Mixed outline thickness = the AI giveaway"** (frame 12:51).
- **Icons:** AI-made UI has no icon access, so it falls back to emoji. Their icons are **generated with Flux on Cloudflare** (frame 13:14
  shows a set of purple/blue fantasy icons).
- **The checker** (frame 13:46):
  1. **4 real screen sizes** (small phone → full-HD monitor)
  2. **thumb-sized buttons**
  3. **nothing touches** (no overlaps)
  4. **centred to within 1.5 px**
  5. **no tiny text, no random boxes** (no frame drawing a stray box around a button, a recurring AI bug)
- **Style is "trained, not guessed"**: the house style came from Claude studying many Roblox UIs. You can **take the #1 game's UI → give it to
  Claude → keep it as a template** in the skill, and it takes the good parts to make its own (frame 14:37). (Ties to [[X-Reference-Library]] /
  [[UI-And-Gameplay-Reference]], which are this vault's reference sets.)
- Example UI shown: a "The Settlement" panel ("Stable a sheep" / "Supplies" lists with STABLE buttons, a "Leave for the pass" CTA).

### 7.3 Map skill (14:40–18:08)
![](../Assets/Reference-Captures/SyphoDev-AI-Workflow/27-1546-map-nine-checks.jpg)
- A map is **a space a player moves through, not a pile of parts**. The key questions have measurable answers: can you get there? get back?
  see across? how long do you fall?
- **The skill measures itself** with **raycasts + the game's real movement numbers** (jump height, speed read from the game's config). **Every
  number is labelled with its source**, and **guesses are listed in every report**.
- **9 checks:** **floating** platforms · **no footing** (tops you can't stand on) · **unreachable** high ground · **shouldn't reach** (reachable
  places that shouldn't be) · **no way out** (pits you can't climb out of) · **sight lines** too open/closed · **overlaps** (parts inside
  parts) · **uneven** rings of platforms · **short falls** vs the ragdoll-recovery height.
- The checks came from their own failed runs. **A skill is personal**: tune it to your maps, UI, code and models.
- **Looks:** scripted part-maps look obviously AI-made. They use **meshes made in Blender or via the 3D skill**. Map style can also be
  "trained" on screenshots of games you like (they used a stylised anime-texture game, frame 17:17), or on two games blended into something new.
- **Must stay optimised:** every model is checked before import. No meshes with tens of thousands of triangles.

### 7.4 VFX skill (18:08–20:12)
![](../Assets/Reference-Captures/SyphoDev-AI-Workflow/30-1907-vfx-harvest-pipeline.jpg)
- Roblox ParticleEmitter VFX are hard to simulate outside Roblox, so the skill doesn't generate effects from nothing. Instead:
  **free packs from the toolbox → harvested in Studio → classified → turned into building blocks**, then effects are composed from blocks
  (e.g. fireball = **ball + flame + beam**).
- **Phase freeze** (frame 19:52): a burst lasts **under 1 s**, so a random screenshot is a coin flip. Instead **fire the effect, wait the exact time,
  freeze the particles, check start, middle and end.** That shows whether the effect is coherent across its lifetime.
  (Implementation guess, ⚠️ untested: `ParticleEmitter:Emit(n)`, `task.wait(t)`, then set `TimeScale = 0` on the emitters and screenshot.)
- They'll give away the **collector** skill, **not their library**: the pack textures are other people's work. Build your own library from packs.
  (Vault has [[VFX-Texture-Pack]] and [[X-VFX-Reference]] as starting material. Check each toolbox pack's licence/creator before reuse.)

### 7.5 Sound skill (20:12–20:58)
- **Sound uploads are limited each month** via the API, so instead of generating audio, Claude uses **pre-harvested sounds classified by name**
  (boom, fire effect, gunshot) and **combines them**.
- ✅ Verified 2026-10-04 (Open Cloud usage guide): Assets-API audio uploads are **≤100/month if ID-verified, ≤10 total/month if not**. Max 7 min,
  mp3/ogg/wav/flac, 20 MB per request. Generate-Speech uploads count toward the quota. See [[Roblox Audio Pipeline]].

### 7.6 Animation skill (20:58–22:08)
![](../Assets/Reference-Captures/SyphoDev-AI-Workflow/33-2121-animation-poses-as-data.jpg)
- **Poses as data:** which joint, how far, when. **Blender** turns that into a real animation on an **R6/R15 rig**, **renders every frame onto one
  contact sheet**, and **Claude checks the sheet**.
- Honest caveat: **Claude isn't good at this.** Feed it real Roblox animations to copy and learn from. Expect lots of trial and error.
- Same advice as [[AI-Assisted-Workflow]] §6 (labelled rig, contact sheets, recreate real animations first).

### 7.7 3D model skill (22:08–23:36)
![](../Assets/Reference-Captures/SyphoDev-AI-Workflow/35-2256-3d-model-skill-loop.jpg)
1. **Flux image** on Cloudflare → 2. **Claude checks it** → 3. if bad, **new prompt** and retry → 4. if good, send it to a **Kaggle notebook**
   that runs the image→3D model ("Stable3DGen"/Hi3DGen; chosen because it's free).
5. Claude **checks every angle** of the returned model and regenerates on failure.
6. **~600k faces → decimate ~60:1 → ~6–10k faces**, then **bake the lost detail on as a texture**.
7. **Upload via Open Cloud** into the game.

### 7.8 create-roblox-game, the manager (23:36–24:03)
- Owns the three jobs no other skill does: **research → design → assembly**. It delegates everything else, making sure "every skill does
  its job".

## 8. Close (24:03–24:45)
- "Try it yourself": **install Claude Code → pick the one thing AI does worst for you → build one skill for it → write every fix down.**
- Promos: Discord ("OG role" before 1K subs), all skills free at 1K subs, paid course link.

---

## How this maps onto Holden's setup (gap analysis)
| Video practice | Holden today | Gap / candidate action (needs approval) |
|---|---|---|
| Rojo + tests + Selene + StyLua gate | rojo, selene, stylua, wally in Rokit | Gate "scaffold must be green first" + run all 4 before every Studio sync |
| Pure-number rules folder, unit-tested off-Roblox | `Config.luau` in Fish a Monster | Move formulas (costs, rolls) into pure modules with tests |
| One remotes file | Server-validated remotes in Fish a Monster | Already similar; confirm a single registry per game |
| Studio built-in MCP | Registered `Roblox_Studio` | Fallback to a 2nd MCP is optional; re-test play-mode screenshots |
| Open Cloud key as secret | `upload_model.sh` / `upload_audio.sh` + gitignored key | Already done |
| UI spec → preview + file + builder; depth stack; 5-check UI checker | Manual UI passes ([[UI-Polish-And-Juice]]) | **Candidate skill:** UI checker (4 sizes, touch size, overlap, centring, min text) |
| Map raycast checks (9) | None | **Candidate skill:** map-audit script using real WalkSpeed/JumpHeight from config |
| VFX harvest → blocks + phase freeze | [[VFX-Texture-Pack]], X VFX refs | **Candidate:** phase-freeze capture recipe for VFX review |
| Sound library by tag | Pixabay → Open Cloud ([[Roblox Audio Pipeline]]) | Tag/classify a local sound library to save the upload quota |
| AI image→3D (Hi3DGen on Kaggle) → decimate → bake | Poly Pizza/Poly Haven/Blender only | ⚠️ **Conflicts with Holden's art rules** (no AI meshes; clean flat-shaded low-poly). Baked-texture realism also clashes with the flat-shaded style. Do **not** adopt without Holden's explicit decision |
| Flux icons | Icon packs ([[Free-Icon-Pack-v3.1-Basic]]) | Option for custom icons; check the anti-AI-art sentiment in [[X-Thumbnails-And-Icons]] |

## Checklist (if Holden approves adopting parts of this)
- [x] Built the skill set 2026-10-04 (all but animation, parked): see [[Roblox Game Manager Skill]] for the status table.
- [ ] Add a "scaffold green" gate to the project template (`rojo build`, tests, `selene`, `stylua --check`).
- [x] Prototype the UI checker → built 2026-10-04 as [[Roblox UI Checker Skill]]; Studio self-test passed.
- [x] Prototype the map audit → built 2026-10-04 as [[Roblox Map Audit Skill]]; Studio self-test passed.
- [x] Phase-freeze VFX capture → built 2026-10-04 as [[Roblox VFX Review Skill]]; works in Edit mode, self-test passed.
- [ ] Re-test whether Studio MCP screenshots work during play mode on the current Studio build.

## Pitfalls
- **Self-reported workflow, no artefacts.** Nothing here is proven to make better games. The skills aren't public, and the video also sells a course.
- **Licences per model and region:** Hunyuan3D is unavailable in the UK/EU. Check Flux (Black Forest Labs) terms and toolbox-pack licences before shipping.
- **Decimation + baked detail** gives a realistic-ish look that doesn't fit flat-shaded low-poly art direction ([[Art-Direction]]).
- **Audio quota:** 10/month unverified, so don't build workflows that upload per-iteration.
- **Kaggle quota is shared and variable** ("30 h or sometimes higher"). Notebook model-load time isn't included in the 100 s/asset claim.

## Open questions / ⚠️ verify
- ⚠️ verify: do Studio MCP screenshots work in play mode? The video says no; the vault observed UI captures working in play mode.
- ⚠️ verify: Black Forest Labs FLUX.1 [schnell] licence for commercial game assets (the model card says Apache-2.0 for schnell; check BFL terms via Cloudflare).
- ⚠️ verify: Hi3DGen VRAM needs and real per-asset time on a Kaggle T4/P100.
- ⚠️ verify: Claude Pro price in GBP.
- Which third-party Roblox MCP they fall back to (not named).

## Related
- [[AI-Assisted-Workflow]] · [[Video-Breakdowns]] · [[Roblox Studio MCP Quirks]] · [[Tooling-Rojo-Wally-And-Studio-MCP]] · [[Roblox UI Checker Skill]] (built from §7.2) · [[Roblox Map Audit Skill]] (built from §7.3) · [[Roblox Code Gate Skill]] (built from §7.1) · [[Roblox VFX Review Skill]] (built from §7.4) · [[Roblox Asset Pipeline Skill]] (Blender-only take on §7.7) · [[Roblox Sound Library Skill]] (built from §7.5) · [[Roblox Game Manager Skill]] (built from §7.8; full skill-set status table there)
- [[Keeping API Keys Out of Git]] · [[Blender to Roblox Asset Pipeline]] · [[Roblox Audio Pipeline]] · [[UI-Polish-And-Juice]]
- [[VFX-Texture-Pack]] · [[X-VFX-Reference]] · [[Art-Direction]] · [[Reference/_Index|Reference]]

## Sources
- Video + description + auto-captions: https://www.youtube.com/watch?v=afuKhenJldY (watched 2026-10-04)
- Frames: `Assets/Reference-Captures/SyphoDev-AI-Workflow/` (37 key frames + 20 contact sheets, local only)
- Cloudflare flux-1-schnell model page: https://developers.cloudflare.com/workers-ai/models/flux-1-schnell/
- Cloudflare Workers AI pricing: https://developers.cloudflare.com/workers-ai/platform/pricing/
- Hi3DGen / Stable3DGen repo (MIT): https://github.com/Stable-X/Stable3DGen
- Hunyuan3D-2 licence (territory excludes EU/UK/South Korea): https://github.com/Tencent-Hunyuan/Hunyuan3D-2/blob/main/LICENSE
- Kaggle GPU tips (30 h/week quota): https://www.kaggle.com/docs/efficient-gpu-usage
- Roblox Open Cloud assets usage guide (audio quotas, formats): https://create.roblox.com/docs/cloud/guides/usage-assets
- Roblox mesh specifications (20k triangles): https://create.roblox.com/docs/art/modeling/specifications
