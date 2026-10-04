---
tags: [operations/team, monetisation/devex]
status: draft
updated: 2026-10-04
confidence: medium
---
# Team And Budget

## TL;DR
- **Default: solo or 2-person core + contractors.** Keep the core loop, data/economy code and live-ops in-house (the core team). Contract out bounded, spec-able work: 3D props/maps, UI art, icons/thumbnails, VFX, animation, music.
- **Own everything through a Roblox group (community) you control**, with 2-Step Verification, role-based permissions (no one else gets owner-level rank), **Place Copying off**, and a written agreement for every contributor. **Roblox won't arbitrate group disputes.**
- Pay in **Robux via group payouts** (one-time or recurring %) or in USD via PayPal/Wise/escrow. Remember the **DevEx value of Robux is $0.0038 / R$** (since 2025-09-05; $0.0054 for qualifying US 18+ verified purchases). So 10,000 R$ ≈ **$38** to the contractor, which is far below what the same Robux cost to buy.
- Contractor rate guide (2025–26, ⚠️ verify, wide variance): **scripters $15–40/h mid, $50–120/h senior**; builders/modelers/UI typically **$10–40/h** or per-asset. Pay per milestone and never 100% upfront.
- Revenue share for core partners (common pattern, ⚠️ verify by deal): **idea/lead dev 40–60%, second core 20–40%, contractor-turned-partner 5–15%**, implemented as **per-game recurring payouts** with a **vesting/cliff** clause in the written agreement.
- Budget a first game at **$0–3k cash** (mostly art and ads) and sweat equity. Scale spend only once D1 ≥ benchmark P50 ([[KPI-Dashboard-Spec]]).

## Solo vs team: decision rules
| Situation | Recommendation |
|---|---|
| First game, strong scripter, weak art | Solo + buy art per asset + Creator Store assets (licence-checked) |
| Strong builder/artist, weak code | Partner with a scripter on a revenue share (code is the bottleneck for live-ops) |
| Viral trend opportunity (2–3 week window) | Smallest team that ships in 1–2 weeks. Reuse a codebase ([[Post-Mortems-Real-Games]]: GaG v1 in 3 days) |
| Game reached ≥ 5k CCU | Hire (contract → part-time) for **content throughput**: 1 builder/modeler + 1 UI/VFX + community moderator(s). Consider a publisher or studio partner |
| ≥ 50k CCU | Studio-like structure: live-ops PM, 2+ scripters, QA, community manager, analytics. Adopt Me grew from 4 to 29 people in about 10 months at peak growth |

Publishers and studios (e.g. buying into a game for a share, as Splitting Point did with Grow a Garden at about 1k CCU) bring live-ops and marketing know-how. Negotiate on **traction metrics**, not the idea.

## Contractor rates (indicative; ⚠️ verify before budgeting)
| Role | Hourly (USD) | Per-task norms | Notes |
|---|---|---|---|
| Scripter (Luau), mid | $15–40 | Simple script 200–1,400 R$; systems 10k–35k R$+; DevForum posts show $500 USD commissions and 1,800 R$/task | Ask for a code sample with `--!strict` + a data-layer example |
| Scripter, senior (shipped titles) | $50–120+ | Monthly retainers seen at $350–450/mo + % (older listing) | Pay for architecture review even if you code it yourself |
| Builder / level designer | $10–40 ⚠️ | Per map 5k–50k R$ ⚠️ | Specify part count / triangle budget, streaming, mobile perf |
| 3D modeler (Blender) | $10–40 ⚠️ | Per prop $5–50; character $50–300 ⚠️ | Require .blend + FBX, UVs, PBR textures within your texture budget |
| UI designer | $10–40 ⚠️ | Per screen 2k–10k R$ ⚠️ | Require a Figma source + exported slices at 2×; mobile-first |
| Icon/thumbnail artist | — | $20–150 per icon/thumbnail ⚠️ | Highest-ROI art spend ([[Discovery-Algorithm]]) |
| Animator | $15–50 ⚠️ | Per animation 1k–5k R$ ⚠️ | R15 rig; deliver as KeyframeSequence plus uploaded asset under your group |
| VFX | $15–40 ⚠️ | Per effect 1k–8k R$ ⚠️ | Particle budget for mobile |

Robux ↔ USD for pricing: a contractor values 1 R$ at the **DevEx rate $0.0038** (they need ≥ 30,000 Earned R$, a verified email and the other DevEx terms to cash out). Group payouts count as Earned Robux eligible for DevEx (developer-exchange doc). 30,000 R$ ≈ $114.

## Where to hire
- **Roblox Talent Hub** (talent.roblox.com): the official job board and portfolios. DevForum feedback (2025) says it's noisy and hard to search, so post very specific jobs with budget, scope and deadline.
- DevForum "Find and Hire Talent" (legacy listings), Hidden Developers and similar Discord servers, X/Twitter portfolios, ArtStation (modelers), Fiverr/Upwork (icons, music; check Roblox experience).
- Vet: ask for shipped games (check the game page and credits), a paid trial task (2–4 h), references, and an age check. Many talented contractors are minors, which affects contracts and payment, so use group payouts and parental consent ⚠️ verify the legal requirements in your jurisdiction.

## Revenue splits and payouts (mechanics)
- **Group → Finances → Payouts:**
  - **One-time payouts** in batches (CSV `userId,payoutInRobux`), with 2FA challenges.
  - **Recurring payouts** at **group level and per game**: per-game percentages come off first, the remainder flows to group-level splits, and the rest stays in the group balance. Private-server subscriptions keep the split that applied **at purchase time**.
  - Some groups don't unlock Payouts immediately (group age, insufficient funds).
- Typical structures (⚠️ verify / negotiate):
  - **Partners:** recurring % per game, plus a written vesting clause ("% steps up monthly over 6 months; leaver forfeits unvested").
  - **Contractors:** fixed price per milestone, optionally plus a small % (1–5%) for 3–6 months on high-impact work (e.g. the icon artist during launch).
  - Keep **≥ 20–30% in the group balance** for ads, contractors and refunds.
- Taxes: DevEx payouts are income. US DevEx creators receive tax forms ⚠️ verify the current DevEx Terms and your local tax rules. Payments made off-platform (PayPal) are your expense records.

## Protecting IP and ownership
1. **Create the game under a group you own** from day one. Transferring later is painful, and user-owned games can't easily be shared.
2. Owner account: 2-Step Verification, a unique email, no shared logins. Consider a dedicated owner account kept off daily use.
3. **Roles:** contractors get the narrowest role (edit a specific game, no revenue view or spend, no role management, no "edit all group games"). Revoke access on project end. Audit logs are under group settings.
4. **Place Copying off**; uncopylock nothing. Assets (meshes, images, audio, animations) are **uploaded by the group** so they don't break or vanish if a contractor leaves or is banned.
5. **Written agreement** (even a one-page Google Doc signed by both, plus a guardian if a minor): scope, price, milestones, **IP assignment to the owner/group on payment**, confidentiality, revenue share and vesting, what happens on leave or ban.
6. Keep code in **git** (Rojo) under your account or organisation. Contractors work via pull requests, which gives you a timestamped record of authorship.
7. If a contractor leaks or reuploads your game: Rights Manager / DMCA ([[Moderation-And-Policy-Compliance]]).

## Budget template (first game, 8–12 weeks)
| Item | Lean | Comfortable | Notes |
|---|---|---|---|
| Icon + 3 thumbnails (×2 iterations) | $100 | $500 | Highest ROI |
| UI kit | $0 (self/Creator Store) | $500–1,500 | |
| Models / map | $0–300 | $1,000–3,000 | |
| Music / SFX | $0 (licensed library) | $200 | Roblox audio licensing rules apply |
| Ads test (Sponsored/Search) | 10k–50k R$ | 100k–300k R$ | Only after D1 is okay |
| Publishing fee (Kids/Select) | 1,000 R$ refundable, or Plus/Premium | 50,000 R$ refundable expedited review | [[Moderation-And-Policy-Compliance]] |
| Contingency | 20% | 20% | |

## Checklist
- [ ] Group created; game, assets and DevEx under the group; owner 2SV
- [ ] Role matrix documented; contractors have least privilege
- [ ] Written agreements with IP assignment for every contributor
- [ ] Milestone payments, nothing 100% upfront; trial task first
- [ ] Recurring payouts configured only after the agreement is signed
- [ ] Budget sheet tied to KPI gates (spend ads only after D1 ≥ P50)

## Pitfalls
- Building the game on a partner's personal account. If you fall out, you lose the game, and Roblox won't arbitrate.
- Giving contractors "Manage and spend group revenue" or owner-level roles.
- Pricing in Robux without converting at the DevEx rate. Contractors will re-price or leave.
- Big percentage promises with no vesting, given to people who leave in week 3.
- Assets uploaded under a contractor's account break if the account is terminated.
- Paying minors off-platform without guardian involvement.

## Related
- [[Operations/_Index]] · [[Post-Mortems-Real-Games]] · [[Moderation-And-Policy-Compliance]] · [[Live-Ops-Playbook]] · [[KPI-Dashboard-Spec]]
- [[Launch-Checklist]] · [[Growth-Metrics-And-Benchmarks]] · [[Discovery-Algorithm]]

## Sources
- Roblox creator-docs (mirror), commit 9f840b1, 2026-10-02: `production/monetization/developer-exchange.md` ($0.0038 standard since 2025-09-05 10am PT; $0.0035 before; 30,000 Earned R$ minimum = $114; $0.0054 US 18+ rate), `18-plus-devex-rate.md`, `projects/groups.md` (payouts, recurring splits, roles, "Roblox cannot help arbitrate"), `production/publishing/publish-games-and-places.md` (fees). Checked 2026-10-04.
- DevEx help page: https://en.help.roblox.com/hc/en-us/articles/13061189551124-Developer-Exchange-Help-and-Information-Page
- Rates: https://game-ace.com/blog/how-to-hire-the-best-roblox-game-developer/ (vendor blog, $15–40/h mid, $50–120+/h senior; ⚠️ verify); DevForum listings: https://devforum.roblox.com/t/searching-for-a-scripter-commission-500-usd/4082458 , https://devforum.roblox.com/t/hiring-roblox-scripter-%E2%80%93-1800-robux-per-task/4438381 , https://devforum.roblox.com/t/350450-usd-per-month-and-hiring-a-long-term-scripter/789157 , https://devforum.roblox.com/t/2021-commission-price-guide-for-new-developers/1356888
- Talent Hub feedback: https://devforum.roblox.com/t/talent-hub-thoughts/3988817
- Adopt Me team growth: https://www.playadopt.me/news/cute-pet-collecting-roblox-game-adopt-me-sets-new-record ; Grow a Garden share deal: https://gamesbeat.com/janzen-madsen-interview/
