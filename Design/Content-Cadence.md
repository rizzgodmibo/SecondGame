---
tags: [design/live-content]
status: draft
updated: 2026-10-04
confidence: medium
---
# Content Cadence

## TL;DR
- Top Roblox games of 2025–26 run a **weekly update cadence**, usually landing **Friday–Saturday** at a fixed, announced time. Roblox traffic peaks on Saturday. Grow a Garden set successive all-time concurrency records on update Saturdays, and Adopt Me has shipped weekly since ~2021.
- An update makes Roblox **re-explore** your game: impressions spike for a new cohort. If that cohort engages, Roblox **expands** distribution. Each update is a fresh chance at the algorithm ([[Discovery-Algorithm]]).
- Size updates by tier: **weekly drop** (1–3 dev-days, new items/event), **monthly feature** (1–2 weeks, a new system/zone), **seasonal major** (4–8 weeks, a new world or mode). Never go more than 2 weeks without visible new content during the growth phase.
- Make content **data-driven** (tables of pets, seeds, towers, stages) so a weekly drop is mostly art + config, not code. That is the only way a small team can sustain weekly cadence.
- Announce every update in-game (countdown + "NEW" teleport), via an Experience Event on the game page, in the title/thumbnail, and with a Group/Discord post ([[Live-Ops-Playbook]]).

## What the platform rewards
- **Explore and expand**: after a content update you may see a spike of new users from recommendations (explore). Good engagement and monetisation from that cohort keeps the expanded reach. Bad engagement returns you to baseline.
- **"What you do" is factor #1** of four that affect recommendation impressions (updates and gameplay changes), alongside algorithm changes, total Home traffic (seasonality) and competitor performance.
- **Weekly seasonality**: peaks Saturday, dips on weekdays. Also summer/back-to-school and holiday seasons. Launch big updates into the weekend and before holidays.
- **Experience Events** on the game details page let players opt in to a notification when your event starts.

## Reference cadences (2025–26)
| Game | Observed cadence | Notes |
|---|---|---|
| Grow a Garden | weekly, Saturdays | records at 8.9M (May 24) → 11.7M (May 31) → 16.4M (Jun 14) → 21.3M (Jun 21) → ~22.3M (Aug 23, 2025), each tied to update weekends |
| Adopt Me (Uplift Games) | weekly "New Update" since ~2021; now more flexible slots | weekly cadence held since the studio professionalised |
| Pet Simulator 99 (BIG Games) | frequent numbered updates (Update 87 by 2026) | ≈ 1 update per 1–2 weeks since the Dec 2023 launch ⚠️ verify: exact dates |
| Steal a Brainrot | frequent updates + admin events | 25.2M CCU record (Oct 2025) |
| Blox Fruits | large updates months apart, smaller patches between | deep content; long dev cycles (Update 31, Mar 2026) |

Takeaway: **frequency beats size** for trend-driven simulators. Depth-driven RPGs can space big updates further apart if events fill the gaps.

## Update tiers: size vs. effort
| Tier | Frequency | Effort (small team) | Contents | Expected effect |
|---|---|---|---|---|
| Hotfix | as needed | hours | bugs, exploits, balance | protects retention |
| Weekly drop | weekly | 1–3 dev-days | 3–10 new items (pets/seeds/towers), a limited egg/shop rotation, a weekend event, a code | weekend CCU spike, returning players |
| Event | 2–4 weeks | 3–7 dev-days | event currency, event shop, event map tweak, limited items ([[Economy-Design-Sinks-And-Faucets]]) | D7/D30 support, monetisation spike |
| Feature | monthly | 1–2 weeks | new system (trading, fusing, quests), new zone | new meta loop, re-explore |
| Major / season | 6–12 weeks | 4–8 weeks | new world, mode, prestige layer, battle pass season | big re-explore, press/influencer moment |

Rule of thumb: **each weekly drop should create ≥ 1 new chase item and ≥ 1 new sink**, or it adds inflation without adding goals.

## Pipeline for weekly cadence
**Rolling 4-week plan** (always 3 weeks of content in the pipe):
```
Week N:   SHIP update N (Fri/Sat) · monitor · hotfix
Week N:   build update N+1 (config + art) · design N+2 · concept N+3
Mon       telemetry review of N-1 (funnel, economy, revenue) -> balance tickets
Tue-Wed   implement N+1 content (data tables, models, VFX)
Thu       internal test on a test place; balance sim re-run ([[Balancing-Methods]])
Fri       publish to production; update log; thumbnails/title; countdown ends at a fixed hour
Sat-Sun   weekend event live; admin/community moments; watch errors and economy
```
Content-as-data: pets/towers/seeds defined in a `ModuleScript` table (id, rarity, stats, price, model ref), so a new item is one row + one model. Validate tables with a unit test at server start.

**Release mechanics:**
- Use a **timed unlock**: publish early, then flip a server-side flag at the announced time (all servers switch together) and use a countdown. Check the time with `os.time()` on the server, or a Config value.
- Migrate old servers so players get the new version. Use soft shutdown (teleport to reserved server, then back). ⚠️ verify: current "Migrate to latest update" behaviour in Creator Hub.
- Run an update-countdown UI in the lobby for 24–48 h ahead. It builds a weekend spike.

## Announcing updates
- Title tag: `[UPDATE 12] Game Name` or `[🎃 EVENT]` (keep it accurate). Swap the thumbnail to show the new content. Metadata must match content, or recommendations penalise you.
- An Experience Event on the game page for every event, so players can opt in to notifications.
- In-game: an "UPDATE!" button that teleports to the new content, and a 1-screen changelog for returning players ([[Onboarding-And-First-60-Seconds]]).
- Off-platform: Roblox Group shout, Discord, TikTok/YouTube shorts of the new chase item ([[Live-Ops-Playbook]]).

## Checklist
- [ ] Cadence chosen (weekly / biweekly) and release slot fixed (e.g. Saturday 10:00 ET) ⚠️ verify: pick the slot from your own CCU-by-hour data
- [ ] Content-as-data tables in place before launch
- [ ] 3 weeks of content in the pipeline at launch (updates 1–3 ready)
- [ ] Every update: new chase + new sink + announcement checklist done
- [ ] Post-update review: re-explore cohort D1 and session time vs. previous cohort ([[Retention-Metrics-D1-D7-D30]])

## Pitfalls
- Launching with nothing in the pipeline. Week-2 silence kills a trend game's momentum.
- Updates that only add power (stronger pets) without new goals or sinks, which causes inflation and power creep.
- Missed announced times. Players arrive for a countdown and leave disappointed. Use feature flags so publish ≠ release.
- Breaking saves in a rush update. Version your data schema and test migrations ([[Data-Persistence-DataStores-And-ProfileStore]]).
- Burning out a 1–3 person team on weekly majors. Alternate small drops and larger features.

## Related
- [[Live-Ops-Playbook]] · [[Session-Length-And-Pacing]] · [[Economy-Design-Sinks-And-Faucets]] · [[Balancing-Methods]] · [[Genre-Playbooks]] · [[Prestige-And-Rebirth]]
- [[Discovery-Algorithm]] · [[Retention-Metrics-D1-D7-D30]] · [[Data-Persistence-DataStores-And-ProfileStore]] · [[Onboarding-And-First-60-Seconds]]

## Sources
- Roblox Creator Docs, Discovery (explore/expand; 4 factors; Saturday seasonality; Experience Events): https://create.roblox.com/docs/discovery (via github.com/Roblox/creator-docs, read 2026-10-04)
- Grow a Garden record progression: https://insider-gaming.com/roblox-grow-a-garden-shatters-all-time-player-record-for-second-week-in-a-row/ ; https://wnhub.io/news/other/item-48084
- Adopt Me weekly updates: https://allthings.how/adopt-me-new-update-schedule/ ; https://bloxswaps.com/blog/adopt-me-update-schedule
- BIG Games PS99 Update 87: https://www.biggames.io/post/pet-simulator-99-update-87
- Steal a Brainrot 25M CCU: https://www.pocketgamer.biz/robloxs-steal-a-brainrot-becomes-first-game-to-surpass-25m-concurrent-players/
- Blox Fruits Update 31: https://www.sportskeeda.com/roblox-news/what-max-level-blox-fruits
