---
tags: [growth/launch]
status: draft
updated: 2026-10-04
confidence: medium
---
# Launch Checklist (Pre-launch → Soft Launch → Launch Day → First 72 h)

## TL;DR
- **Do eligibility work ≥2 weeks early.** Publishing to 16+ needs an account ≥2 days old, an age check and the content-maturity questionnaire. **All-ages** (Kids & Select) also needs ID/face verification, 2FA, 2 months of Plus/Premium **or** a refundable **1,000 Robux** fee, an evaluation, and **250 highly engaged players** (threshold since 2026-08-19).
- **Soft launch first:** run Limited (Playtesters, Friends or Group) and then a quiet public week with small ads ($20–50/day ⚠️ verify heuristic) to measure **first-play bounce, D1 and session length** before any big push. Don't spend influencer budget until the first 60 seconds work.
- **Launch timing:** release on **Friday, or Saturday morning, US time** (Home traffic peaks on **Saturday**, officially). The update should be live by about **10:00–12:00 ET Saturday** or **15:00–16:00 ET Friday** (US after-school). Best seasons are **2–3 weeks before** summer break (mid-June) or winter break (around Dec 20). Avoid days when a top-10 game ships a mega-update or event.
- **Launch day = stack everything in a 24–48 h window:** update tag, thumbnail personalization (4–5), video, event listing, notification, group shout, Discord, 3–5 clips, influencer posts, a Plays ad campaign, a Today's Picks nomination. Stacking pushes CCU velocity into Charts (Up-and-Coming / Top Trending) and seeds RFY retrieval.
- **First 72 h:** watch error rate, bounce and D1 hourly or daily; hot-fix within hours; do **not** change thumbnails, genre or title mid-test; ship a small content patch on day 3–7 to trigger a second explore wave.

## Details

### T-30 to T-14 days: pre-launch
| Item | Detail |
|---|---|
| Publishing eligibility | Account ≥2 days old, in good standing; age check (face estimation or gov ID); content maturity questionnaire. All-ages: add 2FA plus verification plus (Plus/Premium for 2 consecutive months **or** 1,000 R$ fee, refunded if the game keeps 25 highly engaged players for 60 days without moderation) plus Kids & Select evaluation |
| Ownership | Publish under a **group** (recommended) for team, ads and revenue permissions |
| Public limit | Max **5 never-public games made public per day** per account |
| Genre and subgenre | Final choice. Locks for 3 months |
| Store page | Icon, 4–5 thumbnails, gameplay video (3/month upload quota), description per [[Titles-Descriptions-And-Tags]], social links |
| Analytics | Funnel events for onboarding steps, custom events, LaunchData per channel. See [[Analytics-And-Instrumentation]] |
| Onboarding | Time-to-fun <30–60 s; mobile UI pass (most players are on phones). See [[Onboarding-And-First-60-Seconds]] |
| Performance | Test low-end mobile memory and FPS; server stress test with 2× max players |
| Monetisation | Passes and products live and priced; a starter pack; receipts tested |
| Retention hooks | Daily reward, streak, notifications opt-in prompt, group perk |
| Social loops | Invite prompts, referral rewards. See [[Sharing-And-Referral-Loops]] |
| Community | Group, Discord, 20-clip backlog, share links per channel |
| Influencers | Outreach sent T-14 with an embargo date and codes. See [[Influencer-Coverage]] |
| Ads | Account funded; creatives approved (moderation up to 24–48 h); campaign scheduled |

### T-14 to T-3: soft launch and testing
1. **Limited → Playtesters / Friends / Group members**: 20–50 testers, 2 sessions each, recorded. Fix every point where testers stall in the first 2 minutes.
2. **Quiet public** (no promotion) for 3–7 days, plus an optional small Plays campaign targeting the core country and age.
3. Gates before the "real" launch (use your genre benchmark from Creator Analytics; defaults ⚠️ verify in [[Growth-Metrics-And-Benchmarks]]):
   - First-play bounce (<60 s) at or below benchmark
   - D1 retention ≥ benchmark median (rough floor: 10% for casual simulators/obbies, 15%+ for deeper games ⚠️ verify)
   - Average session ≥ 8–10 min ⚠️ verify
   - Crash/error rate low; no exploit in the economy
4. If the gates fail, iterate for 1–2 weeks. Do not launch on hype.

### Launch timing
| Factor | Rule | Basis |
|---|---|---|
| Day of week | Fri afternoon or Sat morning (US) | Official: Home traffic peaks on Saturday and is lower on weekdays |
| Time of day | Live by **15:00–16:00 ET** weekdays (after-school, still evening in Europe) or **10:00–12:00 ET** Saturday | Community consensus ⚠️ verify with your own hourly CCU |
| Season | 2–3 weeks before summer break (US schools ~mid-June → Aug) or winter break (~Dec 20 → Jan 2); spring breaks (Mar–Apr) and Thanksgiving week are mini-peaks | Official: summer/back-to-school/holiday seasonality. The "2–3 weeks before" timing is community advice ⚠️ verify |
| Avoid | Late Aug to Sept (back to school), exam weeks, the same day as a top-10 game's mega-update/event, or a Roblox platform event (e.g. The Hatch-style hunts) that pulls all traffic | Relative-competition factor (official) |
| Regions | If your top locale is non-US (e.g. Brazil, Philippines, Indonesia), shift to their evening | ⚠️ verify locale share in Demographics |

### Launch day (D0) run-sheet
| Time (ET) | Action |
|---|---|
| -24 h | Final publish to the private test place; smoke test; thumbnails activated; ad campaign scheduled |
| -1 h | Discord/group teaser; influencers confirmed |
| 0 | Set **Public**; title tag "[NEW]" or "[RELEASE]"; event listing live; notification sent |
| 0 to +2 h | Clips 1–2 posted; influencer videos go live; watch the server error log |
| +2 to +6 h | Check bounce, D0 session, error rate; hot-fix if needed (use "Migrate to latest update" sparingly) |
| +6 to +12 h | Clip 3; respond on Discord; nominate for **Today's Picks** |
| End of day | Snapshot metrics in `Projects/<name>/`: CCU peak, plays by source, PTR, bounce |

### First 72 hours
- **Hourly:** error rate, CCU, server crashes. **Daily:** bounce, D1 (from D2), session time, payer conversion, plays by source (Home Recs vs Ads vs Other).
- Expect PTR to drop as impressions grow. This is officially "normal" during exploration.
- Push a **small content or quality patch on day 3–7** with fixes plus one new thing, and new thumbnail challengers *including the winner*.
- Keep ads running only if the ad cohort's D1 is near the organic D1. Otherwise stop and fix.
- Don't rename the game, change genre or swap the icon in the first week. That confuses returning players and the tests.
- Thank creators publicly, post a "Thanks for X visits" milestone clip.

## Checklist
- [ ] Eligibility (age check, questionnaire, 2FA, Plus/fee if all-ages) done ≥14 days before.
- [ ] Soft-launch gates met (bounce, D1, session).
- [ ] Store page complete (icon, 4–5 thumbs, video, description, socials, genre).
- [ ] Analytics funnels plus LaunchData per channel live.
- [ ] Launch date set to Fri/Sat US and checked against big-game update calendars.
- [ ] Influencer embargo and codes ready; share links per creator.
- [ ] Ad campaign approved and scheduled.
- [ ] D0 run-sheet owner assigned; hot-fix process ready.
- [ ] Day 3–7 patch planned.

## Pitfalls
- Launching on a Tuesday in late August. Lowest traffic plus back-to-school.
- Big influencer push before onboarding works. You burn the "first impression" cohort and weak RFY signals follow.
- Forgetting the all-ages requirements, so the game is invisible to the under-13 audience.
- Changing many variables in the first 72 h. You can't attribute anything.
- Using "Exclude from Recommendations" during testing and forgetting to turn it off.

## Related
- [[Growth/_Index]] · [[Discovery-Algorithm]] · [[Thumbnails-And-Icons]] · [[Titles-Descriptions-And-Tags]] · [[Sponsored-Ads-And-Paid-Acquisition]]
- [[Influencer-Coverage]] · [[Organic-Growth]] · [[Growth-Metrics-And-Benchmarks]]
- [[Onboarding-And-First-60-Seconds]] · [[Analytics-And-Instrumentation]] · [[Live-Ops-Playbook]] · [[Sharing-And-Referral-Loops]]

## Sources
- Roblox Creator Docs, *Create and publish games* (publishing requirements, fees, audience, 5/day limit): https://create.roblox.com/docs/production/publishing/publish-games-and-places (GitHub mirror 2026-10-02)
- Roblox Creator Docs, *Roblox Kids and Select*: https://create.roblox.com/docs/production/publishing/kids-and-select
- DevForum, "Highly Engaged Player Threshold Drops to 250" (2026-08-19): https://devforum.roblox.com/t/4820164
- Roblox Creator Docs, *Discovery* (seasonality, Saturday peak; explore/expand): https://create.roblox.com/docs/discovery
- Roblox Creator Docs, *Discovery FAQ* (PTR dip on impression growth): https://create.roblox.com/docs/discovery-faq
- Roblox Creator Docs, *Thumbnails* (video quota): https://create.roblox.com/docs/production/publishing/thumbnails
- DevForum, "Player Peak Time?" (community, ~4 pm ET): https://devforum.roblox.com/t/player-peak-time/683105
- rolearn.dev, "When to Launch Your Roblox Game: Seasonal Timing Strategy" (third-party; 30–50% break uplift claim ⚠️ verify): https://rolearn.dev/guidance/roblox-game-launch-timing-seasonal-strategy/
