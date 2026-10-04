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
| Growth | Growth/ | 2026-10-04 | Re-verify the 2026-06-15 algorithm change details; benchmark table from real dashboards |
| Engineering | Systems/ | 2026-10-04 | Type-check all code; Studio MCP hands-on recipes |
| Visuals | Visuals/ | 2026-10-04 | Measure particle/triangle budgets on a real low-end phone; add a Blender export preset file |
| Design | Design/ | 2026-10-04 | Time real top games to calibrate time-to-milestone targets; add a worked economy spreadsheet |
| Monetisation | Monetisation/ | 2026-10-04 | Track Roblox Plus / Creator Rewards changes (2025–26 overhaul); test price heuristics |
| Retention | Retention/ | 2026-10-04 | Build own benchmark set from Roblox Analytics 'similar experiences'; seasonal event calendar |
| Operations | Operations/ | 2026-10-04 | Replace snippet-sourced case-study numbers with primary sources; write native Experiments (ConfigService) recipes |
| Reference | Reference/ | 2026-10-04 | Refresh icon/thumbnail gallery monthly (CDN URLs expire) |
| AI workflow | Meta/ | 2026-10-04 | Verify "Astra 6" and "6.1 SOL"; write Claude↔Codex handoff protocol if a 2nd agent joins |

## Open verifications (⚠️ claims to check against Tier-1 sources)
### Growth
- Whether "Deep play-through rate" (announced early 2026) is still a ranking signal; it's missing from the Oct 2026 signal table.
- Whether thumbnail personalisation still optimises on qualified play-through rate after the June 2026 change.
- Exact formulas behind the Charts sorts, e.g. whether Top Trending is playtime growth over ~2 weeks.
- Whether a "qualified play" really means ~5 minutes (old community lore).
- Cost per play: forum figures (~$0.01) conflict with a third-party $0.45 figure. Also check 4–12 Robux per visit and the 0.01-credit minimum bid.
- The suggested $20–50/day soft-launch ad budget.
- ~~DevEx rate / +42% 18+ rate~~ → resolved by Monetisation pass: $0.0038/R$ standard, $0.0054/R$ for age-verified U.S. 18+ purchases since 2026-06-08 (R15-only experiences). Update [[Sponsored-Ads-And-Paid-Acquisition]] break-even maths to match.
- The 50-character title cap and the ≤30 recommendation; whether "[UPD]" tags lift click-through.
- Current rules on "follow us for a code" and social-follow rewards.
- ≥1,000 impressions per thumbnail before judging, and the minimum test length.
- Community benchmark table (CTR, bounce, D1/D7, session length, payer conversion), the soft-launch gates, and the CCU milestone ladder.
- Launch timing windows and the 30–50% school-break uplift.
- Update cadence ladder (weekly → biweekly → monthly) and trend windows of 2–6 weeks.
- Influencer rates, agency claims, UK/EU disclosure law, and rules on paying minors.
- Accuracy of third-party stats sites; whether RoTrends has shut down.
- Locale share of the audience, for picking non-US launch times.
### Monetisation
- ProfileStore member names used in receipt code (`LastSavedData`, `OnAfterSave`, `Save`, `IsActive`) → check against the ProfileStore GitHub source.
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
- ProfileStore method names (`StartSessionAsync`, `Reconcile`, `EndSession`); check with the Monetisation items.
- Whether paid streak restores are allowed; whether a season pass can be a Subscription; the ~100 R$/month private-server price.
- ~~Whether the server-side `IsInGroupAsync` cache refreshes after `PromptJoinAsync`~~ → resolved: no. Only the client's cache is cleared (GroupService.yaml); the note's re-check-on-rejoin approach is correct.
- The Game Settings name for "leave slots for friends".
- Whether `GetRangeAsync` accepts a bound with sortKey only; the Open Cloud notification permission scope.
- Whether favourites/follows still trigger update notifications.
- Anti-alt `AccountAge` gating, the Discord mod ratio, title update-tag rules, and off-platform giveaway rules.
### Design
- Platform defaults: WalkSpeed 16, JumpPower 50, JumpHeight 7.2, Gravity 196.2; measure max running-jump distance in Studio.
- Whether the 120 s join timeout still applies; clock skew between servers; how AFK time counts toward playtime; maturity labels for horror; minimum mobile button size.
- Benchmarks: session length per genre, onboarding step completion rates, loot rarity percentages, daily free premium currency, time-to-milestone targets.
- Third-party facts: Cookie Clicker 1.15 cost growth, Genshin pity figures, PS99 rebirth cap and update cadence, whether the reference titles are still current.
### Systems
- Luau: whether Studio defaults to `--!optimize 1`; whether client-side native codegen is enabled; the default type solver; user-defined type functions in production; string requires (`require("./X")`) in live servers.
- Replication: which Humanoid properties replicate from the client; what happens when a client deletes parts of its own character; allowed attribute types; whether Server Authority mode (`Workspace.AuthorityMode`) is in beta or released.
- Networking: the ~50 KB/s per-client bandwidth guideline.
- Data: whether a per-key write cooldown still applies in practice; Roblox's recommended receipt pattern vs ProfileStore's; whether a bare `{UserId}` key works in deletion templates.
- Platform coverage of Hyperion (Byfron).
- Performance: where heap snapshots appear in the Dev Console; sources for the rules of thumb (Heartbeat ≥55 Hz, 20–30k parts, ~1–1.5 GB mobile memory).
- Parallel Luau thread-safety tags (e.g. Raycast); whether SharedTable can hold Instances; the default `StreamingIntegrityMode`.
- Server-wide (non-player) analytics events; whether client errors show in the Creator Hub Error Report.
- Tooling: is the standalone studio-rust-mcp-server superseded by the built-in MCP? setup-rokit behaviour; quotas for the Open Cloud Luau Execution API for CI; can MCP edits be undone?
- Library status: ByteNet maintenance; TopbarPlus v3.4.0 with the current topbar.
- Analytics custom-field limits; maturity questionnaire requirements; the name of the localization setting.
### AI workflow
- What "Astra 6" (image model) and "6.1 SOL" (coding model) are, and whether the benchmark claims hold.
- ~~Texture size~~ → resolved: upload max 4096², guidance ≤1024² (PBR ≤1024²). 8K is useful as source only. AI-Assisted-Workflow corrected.
### Visuals
- Current Avatar settings UI for locking body scale; Moon Animator 2 price; whether a client-created IKControl is visible to other players.
- Talent Hub status for commissions; Creator Store licence scope off-platform (ads/merch); typical asset moderation turnaround.
- Scene triangle and draw-call budgets on low-end mobile; whether `AudioPlayer:Play()` waits for loading.
- Fusion 0.3, Vide and React-lua maintenance status; current device split (~55–65% mobile); whether `AbsoluteSize` is in pixels or points for touch targets.
- VFX particle budgets (≤1,500 live particles on mid phones).
### Assets
- Licence of Free Icon Pack v3.1 (Basic): the zip has no licence file. Find the source page.

## Next session (start here — runs locally from C:\Vault)
1. Finish Reference/: write `VFX-And-Art-Style-Reference.md` and `Reference-Capture-Process.md`; add timestamps to [[Video-Breakdowns]].
2. Re-run the deprecated-API sweep (see [[Deprecated-API-Replacements]] → "Regenerating this list") over Visuals/ and Reference/.
3. Install luau-analyze and type-check every ```lua block.
4. Work down **Open verifications**, starting with Growth. On a local machine create.roblox.com and devforum are reachable, so check those directly.
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
| 2026-10-04 | Deprecated-API sweep + note; Visuals done; Reference partly done (stopped to save cloud credits; move to local) |
| 2026-10-04 | Vault bootstrapped: conventions, Home, playbook, 7 domain folders (~80 notes), Prompt Library, AI-Assisted Workflow (from owner's screenshots), icon pack + catalogue, 5 video breakdowns, Reference folder |
