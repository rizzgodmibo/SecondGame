---
tags: [meta/gaps]
status: reviewed
updated: 2026-10-04
confidence: high
---
# Gap Tracker

Work queue for the vault. Each session should take items from the top of **Rotation** and **Open verifications**,
then log what it did in **Session log**. Rotate areas so none goes stale.

## Rotation (next area due → last)
| Area | Folder | Last deep pass | Next focus |
|---|---|---|---|
| Visuals | Visuals/ | 2026-10-04 | Measure particle/triangle budgets on a real low-end phone; add a Blender export preset file |
| Design | Design/ | 2026-10-04 | Time real top games to calibrate time-to-milestone targets; add a worked economy spreadsheet |
| Monetisation | Monetisation/ | 2026-10-04 | Track Roblox Plus / Creator Rewards changes (2025–26 overhaul); test price heuristics |
| Retention | Retention/ | 2026-10-04 | Build own benchmark set from Roblox Analytics 'similar experiences'; seasonal event calendar |
| Operations | Operations/ | 2026-10-04 | Replace snippet-sourced case-study numbers with primary sources; write native Experiments (ConfigService) recipes |
| Growth | Growth/ | 2026-10-04 | Re-verify the 2026-06-15 algorithm change details; benchmark table from real dashboards |
| Engineering | Systems/ | 2026-10-04 | Type-check all code; Studio MCP hands-on recipes |
| Reference | Reference/ | 2026-10-04 | Refresh icon/thumbnail gallery monthly (CDN URLs expire); run the remaining X queries listed in [[X-Reference-Library]] |
| AI workflow | Meta/ | 2026-10-04 | Run the 7 new Claude Code skills on a real (non-frozen) game; test SoundPlayer in Studio; verify "Astra 6" and "6.1 SOL" |

## Open verifications (⚠️ claims to check against Tier-1 sources)
### Growth
- Whether "Deep play-through rate" (announced early 2026) is still a ranking signal; it's missing from the Oct 2026 signal table.
- Resolved 2026-10-04: personalization objective verified from the live primary page in [[Thumbnails-And-Icons]]; distinct from Home ranking.
- Exact formulas behind the Charts sorts, e.g. whether Top Trending is playtime growth over ~2 weeks.
- Whether a "qualified play" really means ~5 minutes (old community lore).
- Cost per play: forum figures (~$0.01) conflict with a third-party $0.45 figure. Also check 4–12 Robux per visit and the 0.01-credit minimum bid.
- The suggested $20–50/day soft-launch ad budget.
- ~~DevEx rate / +42% 18+ rate~~ → resolved by Monetisation pass: $0.0038/R$ standard, $0.0054/R$ for age-verified U.S. 18+ purchases since 2026-06-08 (R15-only experiences). Update [[Sponsored-Ads-And-Paid-Acquisition]] break-even maths to match.
- The 50-character title cap and the ≤30 recommendation; whether "[UPD]" tags lift click-through.
- Current rules on "follow us for a code" and social-follow rewards. Seen in the wild on X (an X-follow codes board, 'join group + like the game' rewards); see [[X-Reference-Library]].
- Current Roblox rules on odds disclosure for paid random items (every X shop reference shows odds; confirm whether it is required).
- Corrected 2026-10-04: removed universal thumbnail sample/duration gates. They are unvalidated heuristics; establish project-specific evidence requirements before judging results.
- Community benchmark table (CTR, bounce, D1/D7, session length, payer conversion), the soft-launch gates, and the CCU milestone ladder.
- Launch timing windows and the 30–50% school-break uplift.
- Update cadence ladder (weekly → biweekly → monthly) and trend windows of 2–6 weeks.
- Influencer rates, agency claims, UK/EU disclosure law, and rules on paying minors.
- Accuracy of third-party stats sites; whether RoTrends has shut down.
- Locale share of the audience, for picking non-US launch times.
### Monetisation
- ~~ProfileStore member names used in receipt code (`LastSavedData`, `OnAfterSave`, `Save`, `IsActive`)~~ → resolved 2026-10-04: all present in ProfileStore.luau (commit 45c9847, 2025-07-31): `Profile.LastSavedData` (read-only), `Profile.OnAfterSave` signal, `Profile:Save()`, `Profile:IsActive()`.
- The pending/escrow window for pass and product sales; payout timing for rewarded video ads.
- Whether paid access (in Robux) pays 70%.
- That DevEx has no Premium or Plus requirement (DevEx Terms of Use).
- How the 70% share is rounded.
- The Robux pack price table (app vs web).
- Whether ad rewards arrive with 0 Robux spent.
- That there's no native gifting API for passes.
- Plus Robux bundles; legacy Premium; how `MembershipType` reports Plus users; what `PromptPremiumPurchase` does now.
- Third-party conversion and ARPDAU benchmarks; whether Creator Hub monetisation charts show gross or net.
- Price-range, starter-pack and offer-timing heuristics (synthesised, need A/B data).
- The pay-to-win acceptance matrix; the ">10% PvP odds" rule of thumb; dated backlash examples.
- Subscription conversion and lifetime-value claims; the Pet Simulator 99 odds-nerf date; the 1,000 R$/month transfer cap; Community Standards wording on misleading commerce.
### Operations
- AnalyticsService: whether `LogJourneyEvent` shows in dashboards and its limits; which keys `GetPlayerSegmentsAsync` returns; whether "120 + 20×CCU" means per server or per game.
- GameAnalytics Roblox SDK: is it still maintained? GameAnalytics 2026 median D1 of 10.3% (not read at source).
- HttpService 500 requests/min per server; 700-player maximum server size.
- Fallback KPI targets and the bad-launch triage/pivot thresholds; whether relaunching in the same place is penalised.
- Best update day/time (Saturday? Grow a Garden's 10:00 ET schedule comes from fan sites).
- Current list of allowed off-platform links (Community Standards).
- All case-study figures in [[Post-Mortems-Real-Games]] (from search snippets); BedWars ">90% decline".
- Contractor rates and revenue-share norms; legal rules for paying minors; DevEx tax forms.
### Retention
- GameAnalytics 2026/2025 benchmark figures (from snippets); the DevForum 2023 D1 p50/p90 example.
- Which timezone the Roblox Analytics D1 day boundary uses (assumed UTC).
- ~~ProfileStore method names (`StartSessionAsync`, `Reconcile`, `EndSession`)~~ → resolved 2026-10-04: `ProfileStore:StartSessionAsync`, `Profile:Reconcile()`, `Profile:EndSession()`, `Profile.OnSessionEnd` and `ProfileStore:MessageAsync` all in source commit 45c9847.
- Whether paid streak restores are allowed; whether a season pass can be a Subscription; the ~100 R$/month private-server price.
- ~~Whether the server-side `IsInGroupAsync` cache refreshes after `PromptJoinAsync`~~ → resolved: no. Only the client's cache is cleared (GroupService.yaml); the note's re-check-on-rejoin approach is correct.
- The Game Settings name for "leave slots for friends".
- Whether `GetRangeAsync` accepts a bound with sortKey only; the Open Cloud notification permission scope.
- Whether favourites/follows still trigger update notifications.
- Anti-alt `AccountAge` gating, the Discord mod ratio, title update-tag rules, and off-platform giveaway rules.
### Design
- ~~Platform defaults~~ → measured 2026-10-04 in a fresh Baseplate: WalkSpeed 16, JumpHeight 7.2 (UseJumpPower off, so JumpPower 50 not exercised), Gravity 196.2, MaxSlopeAngle 89. Still open: a physical max running-jump test (calculated ≈ 8.7 studs) and the Humanoid auto-step height (map audit guesses 1.5).
- Whether the 120 s join timeout still applies; clock skew between servers; how AFK time counts toward playtime; maturity labels for horror; minimum mobile button size.
- Benchmarks: session length per genre, onboarding step completion rates, loot rarity percentages, daily free premium currency, time-to-milestone targets.
- Third-party facts: Cookie Clicker 1.15 cost growth, Genshin pity figures, PS99 rebirth cap and update cadence, whether the reference titles are still current.
### Systems
- 2026-10-04: remote mutation contract and interaction-authority review added to [[Remotes-And-Networking]] and [[Anti-Exploit-And-Server-Authority]]. Pending: type-check snippets; execute adversarial matrix in an authorized game test; verify limiter configuration/lifecycle and durable retry behavior.

- Luau: whether Studio defaults to `--!optimize 1`; whether client-side native codegen is enabled; the default type solver; user-defined type functions in production; string requires (`require("./X")`) in live servers.
- Replication: which Humanoid properties replicate from the client; what happens when a client deletes parts of its own character; allowed attribute types; whether Server Authority mode (`Workspace.AuthorityMode`) is in beta or released.
- Networking: the ~50 KB/s per-client bandwidth guideline. The live RemoteEvent page extraction on 2026-10-04 did not expose the existing 500 requests/s claim; verify the method-level docs/source before reconfirming it (absence from extraction is not a contradiction).
- Data: whether a per-key write cooldown still applies in practice; Roblox's recommended receipt pattern vs ProfileStore's; whether a bare `{UserId}` key works in deletion templates.
- Platform coverage of Hyperion (Byfron).
- Performance: where heap snapshots appear in the Dev Console; sources for the rules of thumb (Heartbeat ≥55 Hz, 20–30k parts, ~1–1.5 GB mobile memory).
- Parallel Luau thread-safety tags (e.g. Raycast); whether SharedTable can hold Instances; the default `StreamingIntegrityMode`.
- Server-wide (non-player) analytics events; whether client errors show in the Creator Hub Error Report.
- Tooling: is the standalone studio-rust-mcp-server superseded by the built-in MCP? setup-rokit behaviour; quotas for the Open Cloud Luau Execution API for CI; can MCP edits be undone?
- Library status: ByteNet maintenance; TopbarPlus v3.4.0 with the current topbar.
- Analytics custom-field limits; maturity questionnaire requirements; the name of the localization setting.
### AI workflow
- **Parked 2026-10-04 (Holden: skip): animation skill** from the SyphoDev video (§7.6). Plan kept for later: poses-as-data → procedural colour-coded R15 rig in Blender → frame sheets; deterministic checks (joint limits, foot slide, loop seam, floating, symmetry, joint names); KeyframeSequence preview via MCP; spike to read default R15 anims as references. Pick up if a game needs custom animations.
- Audio: confirm whether Holden is ID-verified (catalogue assumes the 100/month cap); test SoundPlayer in Studio; confirm PPT sound tags by ear ([[Roblox Sound Library Skill]]).
- VFX limits (400/s, 100/s mobile, 20 s lifetime) are vault claims. Studio accepts 450/s and 25 s when set, so check whether rendering actually caps them; also the ~1,500 live-particle phone budget ([[Roblox VFX Review Skill]]).
- roblox-ui-checker: default grey, `TextFits` on copies and the TextScaled estimate were confirmed by the 2026-10-04 self-test. Still open: whether UIScale scales UIStroke thickness; a first run on a real (non-frozen) game; a type-check once luau-lsp is available ([[Roblox UI Checker Skill]]).
- What "Astra 6" (image model) and "6.1 SOL" (coding model) are, and whether the benchmark claims hold. Partial 2026-10-04: a 299k-view creator video (Cole, 2026-09-16) calls 'GPT-6 Astra' OpenAI's newest public model and uses it to build a Roblox game; still needs an official OpenAI source, and 6.1 SOL is unverified ([[YouTube-Reference-Library]]).
- ~~Texture size~~ → resolved: upload max 4096², guidance ≤1024² (PBR ≤1024²). 8K is useful as source only. AI-Assisted-Workflow corrected.
- Studio MCP screenshots in play mode: the SyphoDev video says they do not work; a local observation says UI still captures. Re-test on the current Studio build ([[Video-SyphoDev-Claude-Code-Roblox-Workflow]]).
- FLUX.1 [schnell] commercial terms for game icons/assets when run through Cloudflare (BFL terms); Hi3DGen VRAM needs and real per-asset time on a Kaggle T4/P100; Claude Pro GBP price.
### Visuals
- Current Avatar settings UI for locking body scale; Moon Animator 2 price; whether a client-created IKControl is visible to other players.
- Talent Hub status for commissions; Creator Store licence scope off-platform (ads/merch); typical asset moderation turnaround.
- Scene triangle and draw-call budgets on low-end mobile; whether `AudioPlayer:Play()` waits for loading.
- Fusion 0.3, Vide and React-lua maintenance status; current device split (~55–65% mobile); whether `AbsoluteSize` is in pixels or points for touch targets.
- VFX particle budgets (≤1,500 live particles on mid phones).
- Which image upload paths keep resolution above 1024 px for ImageLabels. Studio MCP `upload_image` uploads were served at max 1024 on 2026-10-04 (see [[Shop Gauntlet Workbench]]); the 2024 Roblox note and decal docs disagree.
### Assets
- Licence of Free Icon Pack v3.1 (Basic): the zip has no licence file. Find the source page.
- Dragon's Hoard set ([[Dragons-Hoard-Set]]): parked at v1 on 2026-10-03; get Holden's critique list before v2. Not yet imported into Studio. Verify OBJ pivot/size/texture handling in the 3D Importer, type-check HoardVFX with luau-analyze, and check the blade shine Beam and particle look in play.
- Fantasy Creatures set ([[Fantasy-Creatures-Set]]): the **Cinder Drake v3.1 is approved** (2026-10-04): hinged jaw, SurfaceAppearance maps, VFX spec v3 as data. The **golem is parked** for another time; the **wolf is dropped**. Nothing is imported into Studio yet. Open, pending Holden: whether the new flame flipbook goes into the roblox-vfx-review library and replaces the fire flipbook in its `fireball-impact` recipe (needs a Studio self-test with him connected). Verify:
  - a multi-object OBJ becomes one Model with 3 MeshParts;
  - the shared texture is uploaded once;
  - Neon parts take the MTL `Kd`;
  - the import size matches `build_report.json`;
  - the drake's VFX attachment frame (bounding-box centre) and breath reach (see `models/CinderDrake/VFX.md`).
  - Roblox scripts: not yet (Holden).

## Next session (start here — runs locally from C:\Vault)
Next bounded maintenance pass: **Visuals/assets**, following Rotation. Research and documentation are authorized; installing tooling or changing game code is a separate scope. The numbered backlog below is preserved, not an override of the seven-domain rotation.

1. X reference library (2026-10-04) is captured, including the queued searches. Next: a Christmas X pass in late November; (done 2026-10-04: captideRBLX thread replies read and added); then run `build_notes.py`.
2. Finish Reference/: write `VFX-And-Art-Style-Reference.md` and `Reference-Capture-Process.md`; ~~add timestamps to [[Video-Breakdowns]]~~ (done 2026-10-04 from captions; #17 needs a replacement video). TikTok pass done 2026-10-04.
2. Re-run the deprecated-API sweep (see [[Deprecated-API-Replacements]] → "Regenerating this list") over Visuals/ and Reference/.
3. Install luau-analyze and type-check every ```lua block.
4. Work down **Open verifications** within the next domain in Rotation. On a local machine create.roblox.com and devforum are reachable, so check those directly.
5. Update `Growth/Sponsored-Ads-And-Paid-Acquisition.md` break-even maths to the $0.0038 / $0.0054 DevEx rates.

## Cross-vault follow-ups
- [x] 2026-10-04: swept the vault against all 423 deprecated engine members and wrote [[Deprecated-API-Replacements]].
  Fixed `GetRankInGroup(Async)` in Live-Ops-Playbook and Community-Management (now `GroupService:GetRolesInGroupAsync` + role Ids) and `GetProductInfo` in Error-Handling.
  - [ ] Re-run the sweep after the Visuals and Reference agents land, and after every large batch of new code.
- [ ] Replace hand-rolled soft-shutdown patterns with the built-in "restart only outdated servers" + `DataModel.ServerRestartScheduled`.
- [ ] Point A/B and feature-flag mentions everywhere to native `ConfigService` / Experiments.
- [ ] Check `Growth/Launch-Checklist.md` against the 2026 Kids/Select eligibility rules in [[Moderation-And-Policy-Compliance]].
- [ ] Install `luau-analyze` (or luau-lsp) in CI and type-check every ```lua block in the vault; no agent could run Luau this session.
- [ ] Note in onboarding/UI notes: chat requires an age check (Jan 2026), so core gameplay must work without chat.

## Known infrastructure gaps
- create.roblox.com and devforum.roblox.com are **blocked by the cloud network proxy**. Agents use the official
  GitHub mirror `Roblox/creator-docs` instead. DevForum claims come from search summaries, so re-check them from a local machine.

## Session log
| Date | Work done |
|---|---|
| 2026-10-04 | Holden approved Cinder Drake v3.1. He parked the golem for another time and dropped the wolf. Recorded in [[Fantasy-Creatures-Set]], [[Art Direction Feedback]] and here. No model or canvas changes. |
| 2026-10-04 | Cinder Drake v3.1 (Holden: legs skinny + fix the weak points I listed). Researched big-cat/dragon limb proportions → new note [[Creature-Anatomy-And-Proportions]]. Thickened the legs to lion-or-heavier ratios (forearm 0.11→0.15 × shoulder height), bulked the feet and tail, measured before/after on the high-res mesh. The jaw is now a separate hinged MeshPart, baked with the mouth open, sharing the Body maps. Our own procedural flame flipbook for the breath. Tighter pose cards. Re-rendered the sheet, re-exported (20,207 tris over 4 parts), VFX spec v3, IMPORT.md, canvas version 8. Nothing tested in Studio. Next: Holden's review, then golem/wolf v2 (apply the proportion checklist before texturing). |
| 2026-10-04 | Cinder Drake VFX + sheet update (Holden's request). The v3 sheet render set (hero, orthos, portrait poses, parts, materials, VFX key, scale, habitat) and a rewritten `Main.dc.html` were republished to the private canvas (version 7). The OBJ was re-exported with the mouth interior and lower teeth (Body 16,490 tris). A data-only Roblox VFX spec v2 was written (`models/CinderDrake/VFX.md` + `vfx_spec.json`: 4 attachments, 7 emitters, 2 lights, budgets, hand-checked against the roblox-vfx-review lint rules). Found that the pack fire flipbook is a torch-flame sheet (flat-cut bases, wrong for flying fire) and the smoke flipbook fades over its frames (OneShot only); the breath was switched to tinted soft puffs + a Glow core and the previews re-rendered. Logged in VFX-Texture-Pack and as skill traps. The ParticleEmitter Attachment/Acceleration/flipbook facts were verified from the creator-docs source. Fixed board card captions/tags in the shared `sheet.css`. Nothing was built in Studio. Next: Holden's review, then golem/wolf v2 or the setup scripts once approved. |
| 2026-10-04 | Built the `roblox-game-manager` Claude Code skill: runs [[Game-Building-Playbook]] phases 0–9 with evidence-backed gates, a per-game Build-Status template (USER vs PROPOSAL decisions), a Concept template and a runnable phase-4 simulation example. **Self-test PASSED** (24 vault links, 10 skills, sim specs). Animation skill parked (Holden). No active game yet: phase 0 starts when Holden has an idea. Note: [[Roblox Game Manager Skill]]. |
| 2026-10-04 | Built the `roblox-sound-library` Claude Code skill: Blender headless soundcheck, Lune catalogue tool (validate/find/quota/export), SoundPlan (pure, 6 specs) + SoundPlayer (Studio glue untested). New catalogue `AssetLibrary/audio/catalogue.json` with PPT's 18 sounds (read-only). **Self-test PASSED.** Found 9 PPT SFX start 59–216 ms late (reported, not changed). Calibrated targets sfx −19.7 dB / music −30.3 dB. Note: [[Roblox Sound Library Skill]]. Next: plan for the animation skill. |
| 2026-10-04 | Built the `roblox-asset-pipeline` Claude Code skill (user-level): Holden's Blender → Open Cloud → Studio steps + a headless Blender preflight (9 checks incl. new `uv-missing`) and per-object preview renders; uploads still need Holden's OK. **Self-test PASSED** in Blender 5.2.2 after the first run exposed a fixture bug and a real gap. No AI generation. Note: [[Roblox Asset Pipeline Skill]]. Next: plan for the sound-library skill. |
| 2026-10-04 | Built the `roblox-vfx-review` Claude Code skill (user-level) from the SyphoDev video's VFX skill: budget lint (11 checks incl. timeline gaps), phase-freeze helpers, 17-block library mapped to Holden's pack (built-in placeholders until an approved upload), 4 recipes, fixture place on Rojo port 34882. Edit-mode phase freeze **confirmed** in Studio; **self-test PASSED** (14 effects). Phase-freeze review of the fireball recipe: washed-out start, near-empty middle; retune pending Holden. Found: Edit-mode `require` caches across MCP calls. Note: [[Roblox VFX Review Skill]]. Next: plan for the asset-pipeline skill. |
| 2026-10-04 | Built the `roblox-code-gate` Claude Code skill (user-level) from the SyphoDev video's code skill: read-only `gate.sh` (rojo build, Lune specs, Selene incl. warnings, StyLua check), `--scaffold` mode, pure-rules guide. Installed **Lune 0.10.5** via Rokit (Holden approved; pinned in the skill only). **Self-test PASSED** 8/8 after fixing an unreported-fallback bug it caught. Note: [[Roblox Code Gate Skill]]. Next: plan for the VFX review skill. |
| 2026-10-04 | Built the `roblox-map-audit` Claude Code skill (user-level) from the SyphoDev video's map skill: Humanoid-measured movement, 2-stud raycast grid, walk/jump/drop graph, 9 checks + spawn check, fixture place on Rojo port 34881. **In-Studio self-test PASSED** (12/12 planted flaws, 0 false flags, 0.6 s). Measured the default movement numbers (Design verification item resolved except a physical jump test). Note: [[Roblox Map Audit Skill]]. Next: plan for the code-gate skill. |
| 2026-10-04 | Built the `roblox-ui-checker` Claude Code skill (user-level, `~/.claude/skills/roblox-ui-checker`) from the SyphoDev video's UI checker: 9 checks, 4 virtual screen sizes, UIKit adapter, fixture place + self-test on Rojo port 34880. StyLua, Selene (0/0) and Rojo build pass. **In-Studio self-test PASSED** (blank Baseplate): 11/11 planted issues found, 0 false flags. Paper Plane Toss was not touched (frozen after release, Holden's instruction). Note: [[Roblox UI Checker Skill]]. |
| 2026-10-04 | Watched SyphoDev's "How to Make a Roblox Game With AI (Claude Opus 5.5 Full Tutorial)" (24:45) in full (Holden's request, Browser pane). Read the full auto-caption transcript; reviewed ~300 frames (5 s contact sheets) and 37 key frames at full size; saved them to `Assets/Reference-Captures/SyphoDev-AI-Workflow/` (gitignored, third-party). New note [[Video-SyphoDev-Claude-Code-Roblox-Workflow]] with chapters, per-skill breakdown and a gap analysis against Holden's setup. Updated [[AI-Assisted-Workflow]] §8, [[Video-Breakdowns]] #23, Reference index, [[Roblox Studio MCP Quirks]] and [[Roblox Audio Pipeline]]. Verified 5 claims: Hunyuan3D licence excludes the UK; Hi3DGen is MIT; Kaggle gives 30 h/week; Workers AI free tier is 10k neurons/day; Open Cloud audio is capped at 100 or 10 uploads/month. Workflow claims are self-reported, not tested here. |
| 2026-10-04 | Ran the Gauntlet Loop trial on the Paper Plane Toss shop (Holden approved): 4 rounds, blind critic wins for ours 0/4 → 2/4 → 3/4 → 4/4, stopped inside the cap. Found and fixed a game-wide 9-slice border bug (kit images stored at max 1024 px; `UIKit.storedSlice`). 3 new kit images uploaded. Temp Dev scripts deleted. Then a polish pass (bigger small text, tinted rays, starter item slots); Holden published it the same day; game code committed as SecondGame 19a3a10. `blind/` is now gitignored; local commit b83e061 includes blind r0/r1 with copies of third-party refs (flagged to Holden). Note: [[Shop Gauntlet Workbench]]. |
| 2026-10-04 | Planned a Gauntlet Loop trial on the Paper Plane Toss shop ([[Shop Gauntlet Loop Plan]]). Holden: not yet; new images allowed if it runs. No code changed. |
| 2026-10-04 | Wrote takeaways for the remaining X posts (all 306 now have one; fixed three mismatched low-poly takeaways). Researched Matt Shumer's Gauntlet Loop from his guide, original prompt, follow-up posts and test write-ups → [[Gauntlet-Loop]]. Open: verify community cost figures ($1.2–1.7k runs, 1.7B tokens) at source. |
| 2026-10-04 | TikTok pass (Holden signed in): 8 searches, about 190 results; kept 26 non-duplicate videos with stats and caption summaries in [[TikTok-Reference-Library]]; skipped Adopt Me hatch clips (already in X), YouTube creators already captured, and AI-tool ads; one duplicate tip (ui-resources.com) flagged. |
| 2026-10-04 | YouTube pass: verified channel, length, date and views for all 22 Video-Breakdowns links; added transcript timestamps for 9 talks; found #9/#10 are duplicate uploads and #17 is unavailable; added 26 new deduplicated videos in [[YouTube-Reference-Library]]. Read the captideRBLX thread replies (6 UI mistakes, 4 font pairs). Resolved the ProfileStore member-name verifications from library source. TikTok skipped (login wall). |
| 2026-10-04 | X reference pass 2 (queued searches): +74 posts (306 total; 200 videos, 163 images, about 1.6 GB) across hatching, low-poly/lobby, animation, fishing, paper and The Hatch event post-mortem; 113 takeaways; 4 new notes ([[X-Hatching-And-Pet-Systems]], [[X-Low-Poly-Builds-And-Maps]], [[X-Animation-Reference]], [[X-Fishing-And-Paper-References]]); added a The Hatch case to [[Events-And-Seasons]]. Browser rendering stalls when the app window is minimised. |
| 2026-10-04 | X/Twitter reference scrape (Holden's request, logged-in X search in the Browser pane): 232 posts (156 videos, 107 images, about 1.3 GB) saved to `Assets/Reference-Captures/X/` (media gitignored because the repo is public), with 12-frame Blender contact sheets, a manifest, and takeaways for all 306 posts (completed later the same day). Notes: [[X-Reference-Library]] + 6 catalogue notes. Flagged an AI-thumbnail reputational risk on [[Paper Plane Toss Thumbnails and Game Icon]] and [[Thumbnails-And-Icons]] (46.5k-like X sentiment, not CTR data). Added the colour-ramp rule to [[Art-Direction]]. X search rate-limited after about 5 queries; remaining queries are queued. Takeaways are observations of mockups, not tested in Holden's games. |
| 2026-10-04 | Paper Plane Toss artwork v6: refined three user-selected assets using new rendering references and inspected official artwork from four games. Saved originals, results, comparisons and prompts in [[Paper Plane Toss Thumbnails and Game Icon]]. Verified PNG sizes and local +1/+10K values. Next: Holden's art review and actual small-size upload previews; conversion remains untested. This task did not change the maintenance rotation. |
| 2026-10-04 | Fantasy Creatures practice set: three Kingshot-style reference sheets (Claude Design canvas files, local; publish was blocked by auto mode). Creatures were sculpted with SDFs in headless Blender and rendered in Cycles, then baked to OBJ + MTL + 1024² PNG (6.3–7.8k tris each). See [[Fantasy-Creatures-Set]] |
| 2026-10-03 | Added Holden's VFX texture pack (25 PNG + 2 MP4) to Assets/VFX/TexturePack with catalogue [[VFX-Texture-Pack]]; asset ids still to record after upload |
| 2026-10-03 | Dragon's Hoard set built in Blender (11 OBJ models, atlas, 7 particle PNGs, HoardVFX/HoardSetup scripts, IMPORT guide, zip); see [[Dragons-Hoard-Set]] |
| 2026-10-04 | Deprecated-API sweep + note; Visuals done; Reference partly done (stopped to save cloud credits; move to local) |
| 2026-10-04 | Vault bootstrapped: conventions, Home, playbook, 7 domain folders (~80 notes), Prompt Library, AI-Assisted Workflow (from owner's screenshots), icon pack + catalogue, 5 video breakdowns, Reference folder |

| 2026-10-04 | Growth maintenance: updated [[Thumbnails-And-Icons]] using live primary documentation; corrected unsupported sample gates and causal interpretations; added evidence acceptance checks. No analytics or runtime tests performed. Reconciled legacy maintenance tracker. Engineering next; all seven domain rows rotate before Growth repeats. |

| 2026-10-04 | Engineering maintenance: verified boundary validation and prompt/detector ownership risks from live primary docs; clarified incomplete shop excerpt and added mutation/retry acceptance matrix. No game edits, type checks or runtime tests. Visuals/assets next: verify a UI/VFX API constraint in canonical notes before hardware-dependent budgets. |
| 2026-10-04 | Cinder Drake screenshot critique: recorded request for realistic/scary creatures and anatomy-first revision recommendations in [[Fantasy-Creatures-Set]]. Next: review neutral-lit silhouette/anatomy pass before materials; no model changes performed. |
