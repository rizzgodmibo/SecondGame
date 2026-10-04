---
tags: [growth/influencers]
status: draft
updated: 2026-10-04
confidence: medium
---
# Influencer Coverage (YouTube, TikTok, Streamers)

## TL;DR
- **Micro first:** 10k–200k-subscriber Roblox creators who already cover *your genre* give the best cost per player. Many will cover a fun game **for free** if you give them an exclusive (early access, a custom code, a named in-game item). Pay only for proven ROI or for mid/macro creators.
- Give **every creator their own Share Link** (tracks new users, D7, 30-day revenue/user) plus a **creator code** (in-game reward). That gives clean attribution and lets you renew the winners.
- **Disclosure is mandatory** when there is any compensation (money, Robux, items, early access with obligations): FTC rules in the U.S. ("#ad", platform paid-partnership toggle), plus Roblox's advertising standards. From **2026-05-04**, paid brand integrations *inside* Roblox games must be **registered as Advertising Integrations** in Ads Manager.
- Roblox programs: **Video Stars** (≥100k subs plus ≥25k avg long-form views, **or** ≥100k plus ≥50k avg short views, **or** ≥10k followers plus ≥300 avg live CCV, over the last 6 months) give creators a **5% Star Code** and **Creator Rewards** eligibility. The old **Creator Affiliate** programme was **deprecated 2025-07-24**, replaced by **Creator Rewards**.
- Time the coverage: posts go live **within 24–48 h of your launch or update**, on Fri/Sat US, so the spike stacks into Charts and RFY retrieval. See [[Launch-Checklist]].

## Details

### Finding creators
| Method | How |
|---|---|
| YouTube / TikTok search | "roblox <genre>", "new roblox game", "roblox codes <genre>" in the last 30 days; sort by upload date; note channels with steady 10k–500k views |
| Competitor tracing | Who covered the top 5 games in your genre (see [[Genre-Positioning]])? Check video descriptions for codes and links |
| Code sites | Creators who post "codes" videos cover many small games. Good for update pushes |
| Video Stars roster | influencers.roblox.com (program members) |
| Discord communities | Roblox YouTuber or creator servers; your own Discord's content-creator role |
| Agencies / marketplaces | Use for macro budgets only. Ask for Roblox-specific case studies ⚠️ verify any agency claims |

Shortlist sheet columns: channel, platform, subs, avg views (last 10 videos), genre fit (1–5), audience age/locale, contact, rate, status, share link, code, results (new users, D7, revenue).

### Costs (no official data; third-party 2026 ranges; treat as negotiation anchors ⚠️ verify)
| Tier (YouTube subs) | Per dedicated video |
|---|---|
| 1k–10k | $20–100 (or free with an exclusive) |
| 10k–50k | $100–300 |
| 50k–200k | $300–1,000 |
| 200k–1M | $1,000–5,000 |
| 1M+ | $5,000–25,000+ |
Alternative models: **CPM** ($5–20 per 1,000 views), performance (per new player via share link), or rev-share via code. A reported blended cost per player of $0.05–0.20 for micro creators ⚠️ verify (bloxg.com, third-party). Compare with your ads CPP ([[Sponsored-Ads-And-Paid-Acquisition]]).

### Creator codes (in-game)
- Ship a code UI with **per-creator codes** (e.g. `ALEX2X` → 2× coins for 30 min plus an exclusive cosmetic). Log redemptions with the creator ID to analytics.
- Also offer **LaunchData share links**: `GetJoinData().LaunchData` tags the join source automatically, which is more reliable than typed codes.
- Rewards must be in-game items, not Robux. Keep them cosmetic or a time-limited boost to avoid economy damage.

### Outreach templates
**Cold DM / email (free coverage ask):**
> Subject: Early access: new Roblox [genre] game where you [one-line hook]
> Hi [Name], loved your video on [specific video]. We're launching **[Game]** on **[date, time ET]**: [hook in one sentence, the clip-able moment]. We'd like to give you **early access** (private server) plus a **custom code "[NAME]"** that gives your viewers [reward], and a **named [item] in the game**. No obligation. If you enjoy it, an upload around launch would mean a lot. 20-second gameplay clip: [link]. Embargo: [date]. Thanks! [Name, role, Discord handle]

**Paid offer:**
> We'd like to sponsor a dedicated video or short about **[Game]** going live **[date]**. Offer: **$[X] flat** (or $[Y] CPM capped at $[Z]), plus a custom code and an exclusive item. Requirements: real gameplay, **disclosed as sponsored** (#ad / paid-partnership toggle), Share Link in the description and pinned comment. Live within 48 h of [date]. Could you share your rate and recent average views?

**Follow-up (once, after 4–5 days):** a one-line reminder with a new hook (e.g. "just added [feature] that would be great for your channel").

### Disclosure and policy rules
| Rule | Detail |
|---|---|
| FTC (U.S.) | Any "material connection" (payment, free valuable items, Robux, affiliate earnings) must be disclosed clearly and up front. The Creator Affiliate docs required an FTC disclosure for affiliate links ⚠️ verify: equivalent rules for other jurisdictions (UK ASA/CMA, EU) |
| Platform tools | YouTube "includes paid promotion", TikTok "Paid partnership/branded content" toggle |
| Roblox Advertising Standards | Ads must be disclosed in a way users understand and must not mimic Roblox's official ad labels. Ads cannot be shown to ad-ineligible users (`PolicyService:GetPolicyInfoForPlayerAsync().AreAdsAllowed`) |
| 2026-05-04 Independent Advertising Policy update | Content is an "ad" if a brand pays for placement in a game or it promotes off-platform products. **Advertising Integrations must be registered** in Ads Manager and assets moderated before going live. U13 ad formats must be COPPA-compliant |
| Minors | Many Roblox creators are under 18. Contract with a parent or guardian; pay via a compliant method ⚠️ verify local law |
| Never | Pay for fake reviews, likes or bot views, or ask creators to hide sponsorship. This breaks advertising-integrity rules and risks suspension |

### Roblox programmes relevant to creators
| Programme | What | Status (2026-10) |
|---|---|---|
| **Video Stars** | Star Code (5% of Robux/Premium/Plus purchases), verified badge, early access; criteria above. Members can also earn Creator Rewards via share links | Active |
| **Creator Rewards** | 35% of new/reactivated users' first $100 (60 days) via your Share Link, if the game has ≥100 DAU; daily engagement 5 R$ per active spender | Active since 2025-07-24 |
| Creator Affiliate Pilot | Up to 50% of new users' spend (cap $100/user, 6 months) | **Deprecated 2025-07-24** |

## Checklist
- [ ] 30–50 creator shortlist (70% micro, 25% mid, 5% macro).
- [ ] Share link plus code per creator; redemption analytics.
- [ ] Press kit: 20-s clip, 5 screenshots, logo, 3-line pitch, update notes, private-server link.
- [ ] Outreach at T-14; embargo at T-0; follow-up at T-9.
- [ ] Written terms for paid deals: deliverable, timing, disclosure, share link, payment terms.
- [ ] Post-campaign table: cost, new users, D7, 30D revenue/user, cost per retained user.

## Pitfalls
- Paying macro creators before the first 60 seconds work. The spike bounces and the RFY cohort is poisoned.
- Generic mass DMs. Personalise with a specific video reference.
- Codes that dump currency into the economy. Cap them; prefer cosmetics.
- No attribution, so you can't tell which creator worked.
- Undisclosed paid content creates legal risk and Roblox account risk.

## Related
- [[Growth/_Index]] · [[Organic-Growth]] · [[Launch-Checklist]] · [[Sponsored-Ads-And-Paid-Acquisition]] · [[Growth-Metrics-And-Benchmarks]]
- [[Sharing-And-Referral-Loops]] · [[Analytics-And-Instrumentation]]

## Sources
- Roblox Video Stars requirements: https://influencers.roblox.com/requirements ; Help article: https://en.help.roblox.com/hc/en-us/articles/360026092011-Roblox-Video-Stars-Program
- Roblox Creator Docs, *Creator Rewards*: https://create.roblox.com/docs/creator-rewards (GitHub mirror 2026-10-02)
- Roblox Creator Docs, *Creator Affiliate Pilot Program* (deprecated 2025-07-24): https://create.roblox.com/docs/creator-programs/creator-affiliate
- Roblox Creator Docs, *Share links*: https://create.roblox.com/docs/production/promotion/share-links
- Roblox Creator Docs, *Advertising standards*: https://create.roblox.com/docs/production/promotion/comply-with-advertising-standards
- Roblox Help, Advertising Standards: https://en.help.roblox.com/hc/en-us/articles/13722260778260-Advertising-Standards
- DevForum, "New Advertising Policies & Standards" (effective 2026-05-04): https://devforum.roblox.com/t/4527365
- FTC, Disclosures 101 for Social Media Influencers: https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers
- Third-party rate data (unverified): https://hypertube.io/blog/how-much-do-roblox-youtubers-really-make-2026-data ; https://bloxg.com/guides/roblox-influencer-guide
