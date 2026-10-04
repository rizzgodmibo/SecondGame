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
| Engineering | Systems/ | 2026-10-04 | (pending agent report) |
| Visuals | Visuals/ | 2026-10-04 | (pending agent report) |
| Design | Design/ | 2026-10-04 | (pending agent report) |
| Monetisation | Monetisation/ | 2026-10-04 | Track Roblox Plus / Creator Rewards changes (2025–26 overhaul); test price heuristics |
| Retention | Retention/ | 2026-10-04 | (pending agent report) |
| Operations | Operations/ | 2026-10-04 | (pending agent report) |
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
### AI workflow
- What "Astra 6" (image model) and "6.1 SOL" (coding model) are, and whether the benchmark claims hold.
- Texture size: whether 8K source textures help at all given the 4096 max and the ≤1024 recommendation.
### Assets
- Licence of Free Icon Pack v3.1 (Basic): the zip has no licence file. Find the source page.

## Known infrastructure gaps
- create.roblox.com and devforum.roblox.com are **blocked by the cloud network proxy**. Agents use the official
  GitHub mirror `Roblox/creator-docs` instead. DevForum claims come from search summaries, so re-check them from a local machine.

## Session log
| Date | Work done |
|---|---|
| 2026-10-04 | Vault bootstrapped: conventions, Home, playbook, 7 domain folders (~80 notes), Prompt Library, AI-Assisted Workflow (from owner's screenshots), icon pack + catalogue, 5 video breakdowns, Reference folder |
