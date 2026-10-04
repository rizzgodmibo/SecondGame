---
tags: [monetisation/pricing]
status: draft
updated: 2026-10-04
confidence: medium
---
# Pricing Psychology (Robux)

## TL;DR
- Build a **price ladder** for each item family: an entry price (≤99 R$), a core price (199–499 R$), a premium price (799–1,499 R$), and a whale anchor (2,499+ R$). Players mostly buy the middle rung. The top rung exists so the middle looks reasonable.
- Use **charm prices ending in 9** (49, 99, 199, 399, 499, 799, 999, 1,499) and **align prices to Robux pack sizes**. Price a key item just under a common pack (≤399 for a ~400–500 pack) so one pack purchase buys it.
- Currency packs: **bonus % grows with tier** (0 / +10 / +20 / +35 / +50%). Show the bonus and a "Best value" tag on the second-highest tier (the decoy target).
- **Do not hand-tune forever. Turn on Managed Pricing** (regional pricing + price optimization). Regional prices range 30–100% of your default. Price tests need about **60,000 transactions per 30 days**, run about 3 weeks, re-run at least every 90 days, and only apply changes with positive incremental revenue.
- Every displayed price must come from `GetProductInfoAsync` at runtime, otherwise Managed Pricing and Plus discounts make your UI lie.
- Never raise the price of something players already compare publicly (passes, VIP) without grandfathering. See [[Monetisation-Mistakes]].

## Core techniques

| Technique | Roblox implementation | Expected effect / rule |
|---|---|---|
| **Anchoring** | Show the most expensive bundle first or at the top of the shop. Show "was 1,499" strike-through only for genuine discounts | Middle items feel cheap. Fake strike-throughs are misleading and breach Community Standards on deceptive commerce ⚠️ verify: wording in Community Standards "Roblox economy" |
| **Decoy** | 3 tiers where tier 2 is 80% of tier 3's price for 50% of the value → tier 3 sells | Use on currency packs and bundles |
| **Charm pricing** | 99 / 199 / 499 instead of 100 / 200 / 500 | Convention on Roblox. Players read 499 as "400-something" |
| **Pack alignment** | Robux packs cost $4.99 / $9.99 / $19.99 / … The R$ amount depends on platform (≈400 app vs ≈500 web per $4.99 ⚠️ verify: current table) | Keep impulse items ≤ the smallest pack (≤399 R$). An item priced just above a pack size forces the next pack, and the leftover Robux becomes your next sale |
| **Bonus framing** | "+50% BONUS" ribbons on currency packs, with % computed against the base tier rate | Higher tiers get bigger ribbons |
| **Unit price display** | "1,000 gems = 99 R$ · 10.1 gems/R$" | Helps players justify the higher tier |
| **Bundling** | Bundle = items whose separate prices sum to 2–3× the bundle price | See [[Bundles-And-Starter-Packs]] |
| **Loss aversion** | Time-limited offers with a countdown. Streak-protection products | Must be genuinely time-limited. Don't re-run "last chance" offers weekly |
| **Zero-price effect** | Free tier, rewarded-ad reward, daily free spin | Builds the habit. Ad rewards are worth about 3–10 R$ of value (Roblox recommendation) |
| **Endowed progress** | A season pass shows progress already earned for free before the upsell | Converts free players at the moment of visible loss |

## Typical Roblox price points (heuristics, 2024–2026 top-chart observation)
These are not Roblox-published numbers, so treat them as starting priors and let price tests decide. ⚠️ verify: against your genre's top 10 games (open their Store tab) before launch.

| Item type | Common range (R$) | Notes |
|---|---|---|
| Starter pack (one-time product) | 49–149 | Goal is the first purchase, not revenue. See [[Bundles-And-Starter-Packs]] |
| Speed / jump / small QoL pass | 49–149 | |
| Extra inventory/storage slots | 99–299 | Per tier, or one pass |
| VIP pass (tag, chat colour, small perks, VIP area) | 199–499 | Avoid power in competitive games |
| 2× currency / 2× XP pass | 199–499 | The most common "core" pass in simulators |
| Auto-collect / auto-farm / auto-hatch pass | 249–799 | High value in idle and sim games |
| Radio / boombox pass | 99–249 | Audio privacy: check moderation implications |
| Consumable boosts (15–30 min) | 19–99 | Price so ~5 uses ≈ a 2× pass. The pass becomes the obvious upgrade |
| Revive / skip / retry | 9–49 | Peak-frustration moments. Cap use to avoid P2W perceptions |
| Currency pack ladder | 49 / 99 / 249 / 499 / 999 / 2,499 (+0 → +75% bonus) | 6 tiers max |
| Exclusive cosmetic / pet | 299–1,499 | Limited editions are higher |
| Whale anchor (huge pet, mega bundle) | 2,499–10,000+ | Few buyers, but anchors everything else |
| Private server | 0–100 / month | Free private servers can help virality. Plus subscribers get paid private servers free, and you're paid for their time (≥60 min) |
| Subscription (Robux) | ≥49 (minimum). 99–499 typical | Or fiat $2.99–14.99 tiers. See [[Subscriptions-And-Premium-Payouts]] |
| Paid access game | 25–1,000 R$, or $9.99/$29.99/$49.99 local | Only with a strong IP or community |

## Price ladder template (copy into each family)

| Rung | Purpose | Example (gems) | Price | Gems/R$ | Ribbon |
|---|---|---|---|---|---|
| 1 Entry | Impulse, first purchase | 100 | 49 | 2.04 | — |
| 2 Small | Light payer | 220 | 99 | 2.22 (+9%) | — |
| 3 Core | Default choice | 600 | 249 | 2.41 (+18%) | Popular |
| 4 Large | Decoy target | 1,300 | 499 | 2.61 (+28%) | **Best value** |
| 5 Huge | Anchor | 2,800 | 999 | 2.80 (+37%) | +37% |
| 6 Whale | Anchor | 7,500 | 2,499 | 3.00 (+47%) | +47% |

Rule: the **value per R$ must be monotonically increasing**. Otherwise players who do the maths call it a scam on social media.

## Managed Pricing (regional pricing + price optimization), as of 2026-10
- **Regional pricing** has been on by default for passes since Apr 2025. Products need opt-in plus dynamic prices plus `GetUsersPriceLevelsAsync` trade/gift gating. Robux subscriptions are forced on. Prices are bounded to **30–100% of default**, so the price never goes above your default. "Economic location" uses VPN, billing and account history.
- Roblox reported regional pricing for passes lifted paying users **+22.4% in Brazil, +44.8% in the Philippines, +13.8% in Mexico** (Roblox, 2025).
- **Price optimization** splits users into cohorts and runs tests of about 3 weeks, re-tested at least every 90 days. It needs about **60k transactions/30 days**. Roblox reported **+4% median earnings** for eligible creators (Roblox, Feb 2025 expansion).
- **Managed Pricing** (2026) unifies both. New games and new items are **enrolled by default**. The opt-in flow blocks you until hard-coded prices are fixed (Dynamic Price Check tool: "Price pinned" / "Location pinned", up to 5 test accounts).
- Decision rule: under 60k transactions/month, keep regional pricing on and A/B test **offer structure** (bundles, placement) yourself with [[AB-Testing]]. Above that, let price optimization run, but **exclude** items whose price is part of your social contract (VIP, founder packs) to avoid "why did my friend pay less?" drama.

## Checklist
- [ ] Each item family has a 3–6 rung ladder with monotonic value per R$
- [ ] Charm prices. Key impulse items ≤399 R$
- [ ] All shop prices fetched at runtime (Dynamic Price Check passed)
- [ ] Managed Pricing enabled. Trade/gift gating implemented if items are transferable
- [ ] Discounts are real (the base price was actually charged recently), and countdowns are real
- [ ] Genre top-10 Store tabs reviewed for price anchors

## Pitfalls
- **Inverted value ladders** (a bigger pack is worse per R$): very common, and players notice.
- **Regional arbitrage:** tradeable items bought cheap in low price-level regions and traded to high-level players. Gate with `GetUsersPriceLevelsAsync`. Donation games (PLS DONATE-style) faced backlash when regional pricing hit passes used as donations (DevForum thread, 2025).
- **Price tests on social-contract items** (VIP, founders) cause fairness complaints when screenshots of different prices circulate.
- Too many rungs (>6) causes choice paralysis and lowers conversion.
- Fake "sale" prices: a deception risk, and they train players to wait for sales.

## Related
- [[Monetisation/_Index]] · [[Bundles-And-Starter-Packs]] · [[Conversion-Funnels]] · [[Gamepasses-vs-Developer-Products]] · [[Robux-Economy-DevEx-And-Platform-Cuts]]
- [[Economy-Design-Sinks-And-Faucets]] · [[AB-Testing]] · [[Genre-Playbooks]]

## Sources
- Roblox creator-docs (snapshot 2026-10-02): `production/monetization/managed-pricing.md`, `price-optimization.md`, `regional-pricing.md`, `subscriptions.md`, `paid-access-*.md`, `promotion/rewarded-video-ads.md`. https://create.roblox.com/docs/production/monetization/managed-pricing (accessed 2026-10-04)
- Roblox Newsroom, "Launching Regional Pricing…" (2025-04): https://about.roblox.com/newsroom/2025/04/roblox-launches-regional-pricing-for-in-experience-items
- DevForum, "Introducing Price Optimization" (2024-10): https://devforum.roblox.com/t/introducing-price-optimization-find-the-best-prices-for-in-experience-items-and-passes/3186081
- DevForum, "Managed Pricing: One System for Better Pricing and Earnings Growth" (2026): https://devforum.roblox.com/t/managed-pricing-one-system-for-better-pricing-and-earnings-growth/4684738
- Game Developer, "Roblox rolls out automated regional pricing tools" (2025): https://www.gamedeveloper.com/business/roblox-rolls-out-regional-pricing-tools-for-developers
- DevForum regional pricing thread, donation-game concerns (2025): https://devforum.roblox.com/t/introducing-regional-pricing-for-passes/3621382?page=6
- Price-point ranges: author heuristics from top-chart Store tabs, not an official source. ⚠️ verify per genre
