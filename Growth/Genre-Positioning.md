---
tags: [growth/positioning, design/genre]
status: draft
updated: 2026-10-04
confidence: medium
---
# Genre Positioning (Finding a Gap, Competitor Analysis, Clone vs Innovate, Trend Lifecycle)

## TL;DR
- Pick a position on two axes: **demand** (players and playtime in the genre) × **supply quality** (how good the top 5 incumbents are, and how fresh). The target is *high demand with dated or few incumbents*, or a *proven loop in an under-served setting or audience*.
- **Use a "familiar loop + one novel twist".** Pure clones get de-prioritised by Roblox (non-unique metadata or place files: lower RFY and search, ads may not spend). Pure innovation carries onboarding and expectation risk. Since June 2026, RFY rewards **28-day retention**, so pick loops with daily-habit potential.
- Roblox has said publicly what it wants more of: **RPG, strategy, puzzle and shooter** for older players (Standout Games), and growth genres **open-world action, sports, driving, social co-op**, plus markets **Japan, India, Germany, Brazil, South Korea** (2024–25 programme docs).
- Do competitor analysis in **1 day** with Charts plus a stats site (RoMonitor Stats, Rolimons, Bloxism or similar): CCU history, visits, favourites ratio, like ratio, update dates, monetisation surface. Then play the top 5 for 30 minutes each and log the first 60 seconds, the loop, sinks and passes.
- **Trend lifecycle:** spark (TikTok meme or new mechanic) → first breakout game → 5–50 copycats within 2–4 weeks → consolidation to 1–3 winners → decay or evergreen. Enter **before copycat saturation**, or later only with a clearly better twist.

## Details

### Step 1: Market scan (2–4 hours)
| Source | What to pull | Notes |
|---|---|---|
| **roblox.com/charts** (official) | Top Playing Now, Top Trending, Up-and-Coming, Top Revisited, Top Earning, genre sorts | Non-personalised. Use a logged-out or alt account too |
| **Creator Analytics benchmarks** | Your "similar games" list in the Home Recommendations tab | Shows who Roblox thinks you compete with (doesn't affect ranking) |
| **RoMonitor Stats** (romonitorstats.com + Chrome extension) | CCU/visit history, milestones, charts history per game | Free, ad-supported |
| **Rolimons** (rolimons.com/games) | Game CCU and visits tracking | Free |
| **Bloxism / rblxdb / SpawnRadar / RivalDucks** | Chart history, records, rising games | Third-party. Accuracy varies ⚠️ verify each |
| **RoTrends (Super League)** | Genre and keyword trends, estimated revenue | Reported as discontinuing in 2026 ⚠️ verify availability |
| TikTok/YouTube search "roblox <genre>" | Views per week, creator interest | Proxy for clip-ability and influencer demand |

### Step 2: Competitor teardown (per top-5 game)
| Field | How |
|---|---|
| CCU now / 30-day avg / peak | Stats site |
| Age of game, last update, cadence | Details page "Updated", stats history |
| Visits ÷ favourites; like % | Details page. A low like % in a high-CCU genre means an exploitable quality gap |
| First 60 s (time to fun, tutorial, first reward) | Play it. Record the screen |
| Core loop, session length, D1 hooks (dailies, streaks) | Play 30 min plus a return next day |
| Monetisation: passes, products, price points, battle pass | Store page plus in-game |
| Thumbnail / icon style | Screenshot the Charts row |
| Weaknesses (bugs, P2W complaints, stale content) | Comments, Discord, YouTube comments |

### Step 3: Gap scoring (pick the highest total; score 1–5 each)
| Criterion | Weight |
|---|---|
| Demand (genre CCU, growth trend) | ×3 |
| Incumbent weakness (age, like %, update staleness) | ×3 |
| Retention potential (habit loops, social and co-play) | ×3 (the June 2026 RFY weights play days) |
| Monetisation depth fit | ×2 |
| Clip-ability (video moments) | ×2 |
| Team fit / scope (ship ≤3 months for a first game) | ×2 |
| Curation upside (novel, under-served genre or audience) | ×1 |

### Clone vs innovate decision rule
| Situation | Choose |
|---|---|
| First game, small team, proven loop with weak incumbents | **"Better + twist"**: same loop, better first 60 s, polish, plus one twist (setting, social mechanic, progression) |
| Hot trend, peak <2 weeks old, you can ship in ≤2 weeks | **Fast follower with a twist**. Unique name and art are mandatory |
| Trend >4–6 weeks old and saturated | **Skip**, or mash it with a different genre |
| Experienced team, under-served genre (RPG/strategy/puzzle/shooter, 13+/18+) | **Innovate**. Aim for Standout Games curation |
| Any case | Never copy titles, thumbnails or place files. That gets you de-prioritised and invites IP takedowns |

### Trend lifecycle (observed pattern, use as heuristic)
| Phase | Signal | Typical duration ⚠️ verify | Move |
|---|---|---|---|
| Spark | Meme or mechanic spreads on TikTok; a small game spikes in Up-and-Coming | days | Prototype in 48 h |
| Breakout | One game hits Top Trending and creators pile on | 1–3 weeks | Ship the twist version now |
| Copycat flood | Dozens of near-identical games; Charts clogged | 2–6 weeks | Only enter with a clearly better twist; strong art |
| Consolidation | 1–3 winners take most CCU (e.g. Grow a Garden 2025, Steal a Brainrot 2025) | months | Compete on live-ops or pivot |
| Decay / evergreen | Winners either fade or become evergreen with live-ops | months to years | Evergreen needs D30 habits |

### Audience positioning notes (2026)
- Platform: **123M DAU** in Q2 2026 (+10% YoY). Roblox reported weaker under-13 U.S. monetisation and an RFY shift to retentive games (Q2 2026 letter).
- Older audiences: Roblox raised the qualifying DevEx rate for 18+-earned Robux in April 2026 (headline "+42%") ⚠️ verify: exact rate and conditions in the `Monetisation/` notes. Combine with Standout Games' ask for RPG/strategy/shooter for older groups.
- Kids and Select (all-ages reach) requires publisher verification plus a **highly-engaged-player threshold of 250** (since 2026-08-19; maintenance 25). Factor this into the launch plan if targeting under-13s. See [[Launch-Checklist]].

## Checklist
- [ ] Charts plus stats-site scan saved (date-stamped) in `Projects/<name>/`.
- [ ] 5 competitor teardowns completed.
- [ ] Gap score table filled in; one position chosen with a stated twist.
- [ ] Twist validated: can it be shown in a 3-second clip and a thumbnail?
- [ ] Genre and subgenre chosen (locks for 3 months). See [[Titles-Descriptions-And-Tags]].
- [ ] Unique name, icon and art direction. See [[Art-Direction]].

## Pitfalls
- Picking by CCU alone. The top genre may have unbeatable incumbents (Brookhaven-type roleplay).
- Reading stats-site "estimated revenue" as fact. These are models.
- Entering a trend at the copycat-flood phase with no differentiation.
- Innovating in the core *and* the controls *and* the setting at once. Players bounce in 60 s.
- Ignoring localisation. Big growth markets are non-English.

## Related
- [[Growth/_Index]] · [[Genre-Playbooks]] · [[Discovery-Algorithm]] · [[Organic-Growth]] · [[Titles-Descriptions-And-Tags]]
- [[Art-Direction]] · [[Retention-Metrics-D1-D7-D30]] · [[Launch-Checklist]]

## Sources
- Roblox Creator Docs, *Standout Games*: https://create.roblox.com/docs/creator-programs/standout-games (GitHub mirror 2026-10-02)
- Roblox Creator Docs, *Creator Affiliate Pilot* (growing genres and markets list): https://create.roblox.com/docs/creator-programs/creator-affiliate
- Roblox Creator Docs, *Discovery* / *Discovery FAQ* (non-unique games; genre not a ranking factor): https://create.roblox.com/docs/discovery-faq
- Roblox Creator Docs, *Ads Manager* (non-unique games may get no spend): https://create.roblox.com/docs/production/promotion/ads-manager
- Roblox Newsroom, Genre insights (2024-07): https://corp.roblox.com/newsroom/2024/07/roblox-genre-insights-what-will-you-create-next
- Roblox Q2 2026 Shareholder Letter: https://s27.q4cdn.com/984876518/files/doc_financials/2026/q2/Roblox-Q2-2026-Earnings-Shareholder-Letter.pdf
- Roblox Newsroom, 18+ DevEx rate (2026-04): https://about.roblox.com/newsroom/2026/04/roblox-fuels-high-fidelity-games-over-18-players-increases-qualifying-devex-rate-42
- DevForum, "Highly Engaged Player Threshold Drops to 250" (2026-08-19): https://devforum.roblox.com/t/4820164
- RoMonitor Stats: https://romonitorstats.com/ ; Chrome Web Store listing
- lensblox, "Best Roblox Game Analytics Tools Compared (2026)": https://lensblox.com/blog/best-roblox-game-analytics-tools-compared-2026-guide/
