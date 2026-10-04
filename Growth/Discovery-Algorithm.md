---
tags: [growth/discovery]
status: draft
updated: 2026-10-04
confidence: high
---
# Discovery Algorithm (Home / Recommended For You, Charts, Search)

## TL;DR
- **Home → "Recommended For You" (RFY) is the main traffic source** on Roblox. Since the **June 15 2026** rollout it ranks on a **28-day view** of *organic RFY-acquired* players: Play-through rate (PTR), First-play bounce rate, Play days/user and Playtime/user are "most important"; co-play days, qualified sessions, spend days and Robux spent/user are "important". QPTR (qualified play-through rate) was **removed** as an RFY signal at that rollout.
- **Every signal is a per-user average over users who came organically from RFY.** Players from ads, search, friends, socials, curation or Charts are *not* counted in ranking, but they *do* help a game get into the **Retrieval** stage (the candidate pool). Rule: outside traffic gets you *tested*; RFY players' behaviour decides how far you *expand*.
- The algorithm "explores then expands": a content update leads to a test cohort; if that cohort retains and spends, it gets more cohorts. **No permanent penalty**: signals use a moving window, and the game is re-tested daily, so old or failed games can grow back.
- Optimise in this order: **the first 60–180 s (bounce)** → **D1 playtime** → **D2–7 / D8–28 play days** → co-play → monetisation. If retention is weak, fix the core loop before you push monetisation (Roblox FAQ).
- **Charts (formerly "Discover") sorts are not personalised.** Everyone sees the same stat-based lists (Top Trending, Up-and-Coming, Top Playing Now, Top Revisited, Fun with Friends, Top Earning, Top Rated, plus genre-specific sorts). **Search** now uses semantic matching, not just exact title matching.
- Discovery is throttled for **giveaway-led metadata, mismatched metadata and non-unique games** (clones). Check the Creator Dashboard banner, which updates daily.

## Details

### 1. Official model: two stages (create.roblox.com/docs/discovery, current 2026-10-02)
| Stage | What it does | What feeds it |
|---|---|---|
| **Retrieval** | Picks a per-user subset of all games ("might enjoy") using engagement, retention, monetisation | *Any* traffic: sponsored ads, curation, search, charts, friends, teleports, notifications, social sharing. "Games that have even a small number of people playing can signal to the system that the game is worth considering." The FAQ says retrieval needs "only a very low minimum number of plays from any source." |
| **Ranking** | Orders the retrieved games for that user, narrowing to **~100 games shown on Home** | **Only** players organically acquired from RFY. "Roblox doesn't count the engagement, monetization, or retention of users first acquired from ads, curation, friends, search, social media, or any other source in the ranking stage." |

### 2. Official RFY signals (since 2026-06-15)
| Priority | Signal | Time segments | Notes |
|---|---|---|---|
| Most important | **Play-through rate (PTR)** | n/a | RFY impression → play. Only first sessions of RFY-acquired users. |
| Most important | **First-play bounce rate** (negative) | <60 s avg; 61–180 s avg | Leaving early in the first session. See [[Onboarding-And-First-60-Seconds]]. |
| Most important | **Play days per user** | D1, D2–7, D8–28 | D2–7 = how many of those 6 days the user played. |
| Most important | **Playtime per user** | D1, D2–7, D8–28 | **Capped at 60 min per user per game per day**, so marathon sessions are not rewarded beyond 1 h/day. |
| Important | Intentional co-play days per user | D1, D2–7, D8–28 | Joining friends, invites, private servers. See [[Sharing-And-Referral-Loops]]. |
| Important | Qualified play sessions per user | D1, D2–7, D8–28 | "Qualified" filters accidental clicks and quick bounces. |
| Important | Spend days per user | D1, D2–7, D8–28 | Number of days a player spends, not the amount. Many small purchases beat one whale. |
| Important | Robux spent per user | D1, D2–7, D8–28 | |

Other official statements (Discovery FAQ, 2026):
- The time segments are "considered both separately and combined". In practice, a strong D8–28 is unlikely if D1 and D2–7 are poor.
- **New games do not wait 28 days.** PTR and bounce start immediately, then D1, then D2–7, then D8–28.
- **Genre is not an explicit ranking factor.** The model learns implicitly that "shooter fans retain on shooters". Story or finite games are "not penalized" for low D8–28. Wrong genre tags hurt only indirectly, through bounces.
- **Per-user averages, not totals**, so small games are not disadvantaged.
- Strong in only retention or only monetisation still gets impressions. Strong in both gets "broader distribution".
- Benchmarks (similar games in the Home Recommendations tab) **do not affect ranking**. They are for comparison only.
- Ads: an ad-acquired user is treated as "already acquired" and will generally not see you in RFY later, so **RFY impressions can dip while total acquisition rises. Roblox says this is not a penalty.**

### 3. Four things that move your Home impressions (official)
1. Your changes (updates, gameplay).
2. Roblox changes (algorithm).
3. Home traffic seasonality: **weekly peak on Saturday**, a weekday dip, summer and back-to-school, holidays.
4. Relative competition: "If other games are significantly more successful at engaging players, your distribution may decrease, even if your own signals remain steady." This is a relative race. Example from the FAQ: your signals rise 50% while competitors improve more, so you see little growth.

### 4. Timeline of official changes (cite these when explaining history)
| Date | Change | Source |
|---|---|---|
| 2024-05 | Discover page test: top charts and new non-personalised sorts (Top Trending, Top Revisited, Fun with Friends). Page renamed **Charts** in mid-2024 | DevForum "Testing an Enhanced Discover Page" (/t/2954676); RTC/RoNews posts 2024-06 |
| 2024-07 | Analytics: QPTR and similar-experience benchmarks | DevForum /t/3075185 |
| 2024-11 | Thumbnail personalization live (optimises QPTR per user segment) | DevForum /t/3257233 |
| 2024-12 → 2025 | Improved RFY rolled out globally, plus a **Home Recommendations** analytics tab; intentional co-play signal added | DevForum /t/3275201, /t/3587441 |
| 2026 (early) | "How we are improving Home this year": **Deep play-through rate** signal, Today's Picks evolving into **Standout Games** (novel games), video autoplay on hover/scroll, Recently Played/Favorites flyout | DevForum /t/4502571 ⚠️ verify: whether DPTR survived the June 2026 signal list. It is not in the 2026-10 docs table. |
| **2026-06-15** | RFY moves from a **7-day to a 28-day view**; QPTR removed; PTR and first-play bounce added; full signal list and priorities published | Roblox Newsroom "Optimizing Discovery…" (John Ciancutti, 2026-06-15); DevForum /t/4684575; docs |
| 2026-07-31 | Roblox Q2 2026 letter: the RFY change "intentionally provides more impressions for highly retentive games at the expense of near term monetization". Bookings growth slowed, mostly in U.S. under-13 per-hour monetisation | Q2 2026 Shareholder Letter |

**Implication (inference):** after June 2026, short-session "cash-grab" designs (huge first-session spend, poor D8–28) lose Home share, while evergreen designs with daily habits gain. Design for **play days** and plan monetisation as **many spend days** (dailies, battle passes, small offers) rather than a single front-loaded spike. See [[Retention-Metrics-D1-D7-D30]].

### 5. Other surfaces
| Surface | How it ranks | How to win |
|---|---|---|
| **Continue Playing** | Recency for returning users. Not RFY. | Habits: dailies, notifications, events ([[Live-Ops-Playbook]]) |
| **Charts** (roblox.com/charts) | Non-personalised, stat-based, all games auto-eligible. Genre-specific top/trending sorts use your **genre setting**. | Spike CCU/playtime growth within a short window (update + influencer + ads stacked). Top Trending is commonly described as "playtime growth over ~2 weeks". ⚠️ verify: Roblox has not published exact formulas. |
| **Standout Games** (curated) | Hand-picked **novel** games: deep mechanics, distinctive visuals, under-represented genres (RPG, strategy, puzzle, shooter for older players). Reskins are "a hard sell". | Nominate via the survey at create.roblox.com/docs/creator-programs/standout-games. Have a trailer, localisation and compliant thumbnails ready. |
| **Today's Picks / Live Events** | Editorial: updates, new and notable games, seasonal moments | Re-nominate with each notable update |
| **Sponsored** | Ads auction, blended through RFY and labelled | [[Sponsored-Ads-And-Paid-Acquisition]] |
| **Search** | Relevance to the query plus semantic understanding (natural language like "food games") across supported languages | [[Titles-Descriptions-And-Tags]] |
| **Game details page "similar games"** | Recommendations; counted as *Search* in acquisition analytics | Accurate genre and metadata |
| **Notifications** | Experience notifications / opt-in prompts | Resurrect lapsed users |

### 6. Official vs community belief
| Claim | Status |
|---|---|
| "Ads boost your RFY ranking" | **False (official).** Ad users are excluded from ranking. Ads only help *retrieval* and give extra reach. |
| "Ads hurt your RFY" | **False (official)**, but RFY impressions can dip because ad users count as already acquired. |
| "Updating often = algorithm boost" | **Partly.** Updates trigger an "explore" spike, but expansion only follows if the new cohort retains. A publish alone is not a signal. |
| "Big games get favoured" | **Official no**: per-user averages. In practice large games have strong signals and the race is relative. |
| "Bigger session time is always better" | **Capped at 60 min/user/day** for the playtime signal. Daily return (play days) matters more after 2026-06. |
| "The first 5 minutes define a qualified play" | Community lore (old QPTR ≈ 5 min). Roblox never published a threshold. ⚠️ verify. QPTR is no longer a ranking signal, but it is still shown in thumbnail personalization. |
| "Exact title match wins search" | Partly. An exact name match gets the large hero tile, but search is now semantic. |
| "Genre tag changes my ranking" | **False (official).** It only affects Charts genre sorts and player expectations. |
| "Changing thumbnails resets the algorithm" | False. Personalization now keeps the incumbent winner (2025 update). See [[Thumbnails-And-Icons]]. |

## Checklist
- [ ] Analytics → Acquisition → **Home Recommendations** tab checked weekly: PTR, bounce (<60 s, 61–180 s), playtime and play days for D1 / D2–7 / D8–28 vs benchmark.
- [ ] Diagnose an impression drop in this order: PTR ↓ or bounce ↑ → D1 playtime/days → D2–7 → D8–28 → secondary signals.
- [ ] Each content update: new thumbnail set (2–5 active), Today's Picks nomination, an experience event, a notification.
- [ ] Before launch, seed traffic from any source (ads, socials, friends) so retrieval picks the game up. See [[Launch-Checklist]].
- [ ] No giveaway or Robux wording in title, icon or thumbnails. Metadata matches gameplay. Original art and name.
- [ ] Creator Dashboard: no "reduced exposure" banner.
- [ ] Genre and subgenre are accurate (changeable only every 3 months).

## Pitfalls
- Optimising thumbnails for clicks that bounce. PTR goes up, bounce rises, and impressions fall.
- Reading total DAU instead of the **RFY-sourced cohort**: ad and influencer spikes hide a weak organic cohort.
- Panicking at the PTR dip that follows an impressions increase. Roblox says this is normal while exploring.
- Cloning a hit's name, thumbnail or place file. These are "no longer prioritized for recommendations" and ads may not even spend.
- Turning on **Exclude from Recommendations** by accident (Settings → Audience). RFY traffic drops to 0.
- Assuming the June-2026 weights are permanent. Roblox says it "will continue to add and remove signals". Re-check docs each quarter.

## Related
- [[Growth/_Index]] · [[Growth-Metrics-And-Benchmarks]] · [[Thumbnails-And-Icons]] · [[Titles-Descriptions-And-Tags]]
- [[Sponsored-Ads-And-Paid-Acquisition]] · [[Launch-Checklist]] · [[Genre-Positioning]]
- [[Onboarding-And-First-60-Seconds]] · [[Retention-Metrics-D1-D7-D30]] · [[Analytics-And-Instrumentation]] · [[Live-Ops-Playbook]] · [[Sharing-And-Referral-Loops]]

## Sources
- Roblox Creator Docs, *Discovery*: https://create.roblox.com/docs/discovery (read via github.com/Roblox/creator-docs `content/en-us/discovery.md`, commit 9f840b1, 2026-10-02)
- Roblox Creator Docs, *Discovery FAQ*: https://create.roblox.com/docs/discovery-faq (same commit)
- Roblox Creator Docs, *Acquisition*: https://create.roblox.com/docs/production/analytics/acquisition
- Roblox Newsroom, "Optimizing Discovery: How Great Games Reach Millions of Players on Roblox", 2026-06-15: https://about.roblox.com/newsroom/2026/06/optimizing-discovery-great-games-reach-millions-players-roblox
- DevForum, "Recommended For You Algorithm Improvements That Better Value Long-Term Retention" (2026-06): https://devforum.roblox.com/t/4684575
- DevForum, "How we are improving Home this year" (2026): https://devforum.roblox.com/t/4502571
- DevForum, "Testing More Recommended For You Algorithm Signals" (2026): https://devforum.roblox.com/t/4568033
- DevForum, "Boost Your Discovery with the Improved Recommended For You Algorithm…" (2025): https://devforum.roblox.com/t/3587441
- DevForum, "Testing an Enhanced Discover Page: Top Charts and New Sorts" (2024-05): https://devforum.roblox.com/t/2954676
- Roblox Q2 2026 Shareholder Letter (2026-07-31): https://s27.q4cdn.com/984876518/files/doc_financials/2026/q2/Roblox-Q2-2026-Earnings-Shareholder-Letter.pdf
- Note: DevForum and create.roblox.com were not directly fetchable in this session. DevForum content above comes from search-engine summaries, and docs content from the official GitHub mirror.
