---
tags: [monetisation/economics, monetisation/devex]
status: draft
updated: 2026-10-04
confidence: high
---
# Robux Economy, DevEx and Platform Cuts

## TL;DR
- **Passes, developer products, Robux subscriptions, private servers, paid access (Robux):** you keep **70%** of the Robux price. Roblox takes 30%. Roblox Plus discounts (10–20%) are paid by Roblox, so you still get 70 R$ for each 100 R$ list price (creator-docs, 2026-10).
- **DevEx standard rate is $0.0038 per Earned Robux** for Robux earned since 2025-09-05 10:00 PT. It was $0.0035 before that date. The minimum cash-out is 30,000 Earned R$, which is $114. Old-rate Robux are always cashed out first.
- **U.S. 18+ rate is $0.0054.** It applies to products, passes, subscriptions and private servers bought by age-verified U.S. adults, in games where player characters use R15 or articulated rigs 100% of the time. In effect since 2026-06-08. A game that allows R6 at any point is not eligible.
- **Premium Payouts / Engagement-Based Payouts ended on 2025-07-24.** **Creator Rewards** replaced them: 5 R$ per day for each Active Spender, plus a 35% share for new or reactivated users you bring in. Premium itself closed to new sign-ups on 2026-04-30 and was replaced by **Roblox Plus** ($4.99/mo).
- Rule of thumb: **a 100 R$ sale is worth about $0.27 to you** (70 R$ × $0.0038). The player paid about $1.00–1.25. You receive about 21–27% of what the consumer spent.
- Plan cash flow around the escrow and hold periods: Creator Rewards and Plus sign-up bonuses have a 60-day hold, avatar commissions 30 days, Robux paid access up to 7 days, and local-currency paid access at least 60 days.

## Revenue streams and cuts (as of 2026-10-04)

| Stream | Your share | Paid as | Hold / timing | Notes |
|---|---|---|---|---|
| Developer products | 70% of price | Earned R$ | Pending ~3–7 days ⚠️ verify: current pending window | Price 1 – 1,000,000,000 R$ |
| Passes | 70% | Earned R$ | same | Same range. Promoted passes on the Buy Robux page must be priced 50–800 R$ |
| Subscriptions (Robux) | 70% each month | Earned R$ | monthly | Minimum 49 R$. Regional pricing is forced on |
| Subscriptions (local currency) | **70% in month 1, then 100%** | Earned R$ | monthly | Tiers $2.99 / 4.99 / 7.99 / 9.99 / 14.99. Requires ID or phone verification |
| Private servers | 70% | Earned R$ | monthly recurring | **Changing the price cancels all active PS subscriptions** |
| Paid access (Robux) | 70% ⚠️ verify (doc does not state the % explicitly) | Earned R$ | escrow up to 7 days | 25–1000 R$, no refunds. Cannot be combined with private servers |
| Paid access (local currency) | 50% at $9.99, 60% at $29.99, 70% at $49.99 (minus taxes/VAT) | Fiat | escrow ≥60 days, paid monthly | Requires ID-verified 13+ creator in a Tipalti-supported country |
| Avatar items sold in your game | **40% to game owner (affiliate)**, 30% to item creator, 30% to platform | Earned R$ | 30-day escrow | If you are both creator and game owner you get 70% |
| Creator Rewards – Daily Engagement | 5 R$ per Active Spender per day | Earned R$ | 60-day hold | Your game must be one of the first 3 the player plays for 10+ min that day |
| Creator Rewards – Audience Expansion | 35% of the new/reactivated user's first $100 of qualifying purchases anywhere on Roblox in their first 60 days | Earned R$ | 60-day hold | Game must average 100+ DAU over the 60 days. Needs an ID-verified creator with a DevEx account |
| Roblox Plus sign-ups (in-game prompt) | 250 R$/month for the subscriber's first 3 paid months (max 750) | Earned R$ | 60-day hold | Only counts sign-ups from `PromptRobloxSubscriptionPurchase` |
| Plus subscriber time in your paid PS | up to 100 R$ per subscriber per renewal (70% of PS price, capped) | Earned R$ | per renewal | Requires ≥60 cumulative min in 30 days, and your server must be in their top 5 |
| Robux transfers in-game (Plus users) | 10% of the transfer | Earned R$ | on settle | 10–500 R$ per transfer. No Roblox fee. DevEx-eligible for you, not for the recipient |
| Rewarded video ads | EPM × impressions | Earned R$ | ⚠️ verify | Eligibility: 13+, ID-verified, public game ≥2,000 unique visitors/month |
| Immersive ads (image/video/portal) | per impression / 15-s view / teleport | Earned R$ | paid on the 25th of the following month | Same publisher eligibility plus an approved Maturity questionnaire |

Source for all rows: Roblox creator-docs repo (snapshot 2026-10-02), pages: developer-exchange, roblox-plus, subscriptions, paid-access-*, private-servers, marketplace-fees-and-commissions, creator-rewards, rewarded-video-ads, immersive-ads.

### Creator Rewards details (replaced Premium Payouts on 2025-07-24)
- **Active Spender** = a user with ≥ $9.99 of qualifying purchases (Robux, Premium/Plus, UGC subs) in the past 60 days, who was **not** new or reactivated in that window.
- Daily Engagement: **5 R$ per Active Spender per day** if your game is among the **first 3 games they launch that day** and they play it **10+ minutes** in total. Design implication: **be a daily "first stop".** Daily login streaks, timed rewards and session-start hooks earn money directly. Rough value: 10,000 qualifying Active Spenders/day ≈ 50,000 R$/day ≈ $190/day.
- Audience Expansion: a new user, or a lapsed user (60+ days inactive), arrives through your **Share Link**, direct link, or a search for your exact game name. It must be their first session that day, and they must play 10+ min. You then get 35% of their first $100 of qualifying purchases **anywhere on Roblox** within 60 days, so up to $35 per user (paid in R$).
- Alt-account farming, bots and teleport manipulation lead to forfeiture or a ban.
- Developers pushed back on the 60-day hold and asked for the old system back (DevForum thread "Shorten the hold period of engagement payouts or restore the old premium payouts system", 2025).

### DevEx (verified 2026-10-04)
| Item | Value |
|---|---|
| Standard rate | **$0.0038 / Earned R$** (since 2025-09-05 10:00 PT; was $0.0035) |
| U.S. 18+ rate | **$0.0054 / Earned R$** on eligible purchases (since 2026-06-08) |
| Minimum | **30,000 Earned R$** ($114 at the standard rate) |
| Age | 13+ |
| Other requirements | Verified email, DevEx portal (Tipalti) account, W-9 or W-8 on file, compliance with ToS and Community Standards |
| Frequency | One completed request per calendar month |
| Processing | ~10 business days for a first request, ~5 for returning creators, plus bank time |
| Order | Pre-2025-09-05 balances are cashed out first at the old rate. Spending Robux does **not** use up the old-rate balance first |
| Not Earned Robux | Bought Robux, Plus/Premium stipends, trading/resale, received transfers, gift cards, passes from template games with no real visits |
| Premium requirement | The current docs list **no Premium/Plus requirement** for DevEx (the old rule needed Premium). ⚠️ verify: DevEx Terms of Use page |

## Robux → USD math

**Consumer side.** The $4.99 pack gives about 400 R$ in the mobile app and about 500 R$ on web or gift cards (differential pricing since Nov 2024). The player therefore pays about **$0.010–0.0125 per R$**. ⚠️ verify: current pack table on roblox.com/upgrades/robux.

**Creator side per item** (70% share, rounded down):

| List price (R$) | You get (R$) | USD @ $0.0038 | USD @ $0.0054 (US 18+) | Consumer paid (≈) |
|---|---|---|---|---|
| 49 | 34 | $0.13 | $0.18 | $0.49–0.61 |
| 99 | 69 | $0.26 | $0.37 | $0.99–1.24 |
| 199 | 139 | $0.53 | $0.75 | $1.99–2.49 |
| 499 | 349 | $1.33 | $1.88 | $4.99–6.24 |
| 999 | 699 | $2.66 | $3.77 | $9.99–12.49 |
| 1,999 | 1,399 | $5.32 | $7.55 | $19.99–24.99 |
| 4,999 | 3,499 | $13.30 | $18.89 | $49.99–62.49 |

⚠️ verify: whether Roblox rounds the 70% share down or to nearest. It matters by less than 1 R$ per sale.

**Scale table** (standard rate):

| Earned R$ | USD |
|---|---|
| 30,000 (minimum) | $114 |
| 100,000 | $380 |
| 1,000,000 | $3,800 |
| 10,000,000 | $38,000 |
| 100,000,000 | $380,000 |

**Reverse math:** $1,000 cash-out = 263,158 Earned R$ = **~375,940 R$ of gross sales** of passes/products.

**DAU model:** DAU × payer conversion × ARPPU(R$/payer/day) × 0.7 × 0.0038.
Example: 10,000 DAU × 2% × 300 R$ × 0.7 × 0.0038 = **$160/day ≈ $4.8k/month**, before Creator Rewards. See [[Conversion-Funnels]].

## Platform context (for sizing)
- Q2 2026: 123M DAU (+10% YoY), bookings $1.6B (+8%), ABPDAU $12.66 (−2% YoY). DevEx fees were $363M (+15% YoY), driven by the 8.5% DevEx increase and Creator Rewards. Bookings missed because per-hour monetisation fell with younger U.S./Canada cohorts (Roblox Q2 2026 shareholder letter, Aug 2026).
- FY2025: creators earned **$1,503.1M** via DevEx, up from $923M in 2024 (Roblox FY2025 10-K/ARS).
- Takeaway: platform ABPDAU is flat or falling, and younger users spend less per hour. Grow by **converting more payers**, especially 18+ U.S. players at the higher rate, and older audiences generally, rather than by pushing price.

## Decision rules
- **Choose fiat-priced subscriptions over Robux subscriptions** when you sell recurring value. Local currency pays 100% from month 2, against 70% for Robux. Use Robux subscriptions only where local currency is unavailable (Argentina, India, Indonesia, Japan, Türkiye, Vietnam, …) or when you need a price that isn't one of the fixed tiers.
- **Consider the U.S. 18+ rate (+42% per R$ vs. standard)** if your audience skews older. It requires R15-only avatars (Avatar Settings → R15 Only) and no R6 at any point. Decide this before you build animations.
- **Sell avatar items in-game** when cosmetics fit your game. You earn 40% as affiliate even on items you didn't make, so curate a UGC shop.
- **Add `PromptRobloxSubscriptionPurchase` at one natural moment**, e.g. near a paid private server or a discount callout. A new Plus subscriber is worth up to 750 R$ ≈ $2.85.
- **Never treat Pending Robux as cash.** Model cash flow with a 60-day lag for Creator Rewards and Plus bonuses.

## Checklist
- [ ] Revenue model spreadsheet uses 0.7 × 0.0038, with the 18+ rate shown as an upside case
- [ ] DevEx account (Tipalti), tax form, ID verification and 2FA done before launch (also needed for ads and Audience Expansion rewards)
- [ ] Group-owned game: the payout recipient with revenue permission is ID-verified
- [ ] Share Links created for every off-platform channel (Audience Expansion attribution)
- [ ] Decided between R15-only and R6 with the 18+ rate in mind
- [ ] Private server price fixed at launch (changing it later cancels all subscriptions)

## Pitfalls
- Using old guides with the $0.0035 rate, "Premium Payouts", or "Premium needed for DevEx". All three are outdated.
- Changing a private-server price: this silently cancels every active PS subscription.
- Hard-coding prices: Plus subscribers, regional pricing and price tests all show a different real price → the UI lies and players complain. See [[Pricing-Psychology]].
- Counting transfer Robux or bought Robux toward DevEx: they are not Earned Robux.
- Cross-game pass and developer product sales were **disabled from 2026-05-30**. Donation-style games must use Robux transfers instead.

## Related
- [[Monetisation/_Index]] · [[Subscriptions-And-Premium-Payouts]] · [[Gamepasses-vs-Developer-Products]] · [[Conversion-Funnels]] · [[Pricing-Psychology]]
- [[Economy-Design-Sinks-And-Faucets]] · [[Analytics-And-Instrumentation]] · [[Moderation-And-Policy-Compliance]]

## Sources
- Roblox creator-docs (GitHub `Roblox/creator-docs`, snapshot 2026-10-02): `production/monetization/developer-exchange.md`, `18-plus-devex-rate.md`, `roblox-plus.md`, `subscriptions.md`, `paid-access-robux.md`, `paid-access-local-currency.md`, `private-servers.md`, `robux-transfers.md`, `immersive-ads.md`, `engagement-based-payouts.md`; `creator-rewards.md`; `marketplace/marketplace-fees-and-commissions.md`; `production/promotion/rewarded-video-ads.md`. Mirrors https://create.roblox.com/docs/production/monetization (accessed 2026-10-04)
- DevForum, "Increasing DevEx — Creators Will Now Earn 8.5% More" (2025-09-05): https://devforum.roblox.com/t/increasing-devex-%E2%80%94-creators-will-now-earn-85-more/3920159
- Roblox Newsroom, "Introducing Roblox Plus" (2026-04): https://about.roblox.com/newsroom/2026/04/introducing-roblox-plus-subscription
- Roblox Q2 2026 Shareholder Letter (2026-08): https://s27.q4cdn.com/984876518/files/doc_financials/2026/q2/Roblox-Q2-2026-Earnings-Shareholder-Letter.pdf
- Roblox FY2025 Form 10-K/ARS: https://www.sec.gov/Archives/edgar/data/1315098/000110465926044380/rblx-20251231xars.pdf
- DevForum, "Shorten the hold period of engagement payouts or restore the old premium payouts system" (2025): https://devforum.roblox.com/t/shorten-the-hold-period-of-engagement-payouts-or-restore-the-old-premium-payouts-system/3956591
- Robux pack prices (third-party, unverified): https://gameboost.com/blog/robux-prices (2026)
