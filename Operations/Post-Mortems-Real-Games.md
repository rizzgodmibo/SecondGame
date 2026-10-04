---
tags: [operations/post-mortems, growth/case-studies]
status: draft
updated: 2026-10-04
confidence: medium
---
# Post Mortems Real Games

## TL;DR
- The record-breaking hits of 2025 (**Grow a Garden** 22.3M CCU, **Steal a Brainrot** 25.8M CCU) share one template: a **dead-simple loop understood in 10 seconds**, **randomised collectibles with visible rarity**, **social flexing or stealing between players in the same server**, and **weekly timed updates or events at a fixed hour** that pack servers.
- **Speed beats polish at the start.** Grow a Garden's first version was reportedly built in **3 days**. Steal a Brainrot rode a meme (Italian brainrot) within weeks of the trend. Polish and live-ops came *after* traction, often by bringing in an experienced studio (Splitting Point bought into GaG at about 1k CCU).
- **Content gaps kill.** Frontlines (a technically superb shooter) fell from an 11.6k CCU peak to a few hundred, attributed to lack of content. Doors waited about 2 years between floor 1 and floor 2. Communities outlast trends only if updates keep coming ([[Content-Cadence]]).
- **The economy is the game** in trading titles (Adopt Me, Pet Sim, GaG). Dupes, inflation and scams are the main live-ops risk. Policy flags (`IsPaidItemTradingAllowed`, `ArePaidRandomItemsRestricted`) apply ([[Moderation-And-Policy-Compliance]]).
- **Data incidents happen even at the platform level** (Roblox's Oct 2020 DataStore incident reverted about 1 h of saves). Design saves and backups so you can restore ([[Bad-Launch-Response]]).
- These cases are survivorship-biased. Use them for *mechanisms*, not as proof that copying a genre works.

## Case studies

### Grow a Garden (2025): trend + weekly event cadence
- **Facts:** released **2025-03-26** by BMWLux (an anonymous 16-year-old); the first version was reportedly built in **3 days**. **Splitting Point Studios (Jandel)** bought a share in **April 2025 at around 1,000 CCU**; the original dev reportedly kept 50%. Passed 16M CCU on 2025-06-21 (beating Fortnite's 15.3M), **21.3M** in July, and **22,346,725 on 2025-08-23** with the "Admin War" update, when Roblox as a whole hit about **47.3M** concurrent users. About 30B visits within months.
- **Mechanics:** plant, wait, harvest, sell, buy seeds. Rare seeds/pets in a **restocking shop on a global timer**, so everyone checks at the same moment. Weather and mutation events multiply value. Trading and flexing. Offline growth gives a reason to return.
- **Live ops:** **weekly updates on Saturdays at 10:00 ET**, preceded by an approximately 1 h **"admin abuse"** event where the owner triggers rare weather and restocks live. That turns each update into an appointment.
- **Lessons:**
  1. A low-skill, idle-friendly loop that works on mobile can reach every age group.
  2. Global timers (restock, weather) create shared moments and social proof inside servers.
  3. Experienced studios can multiply a viral prototype. Plan the cap table and IP ownership early ([[Team-And-Budget]]).
  4. A fixed weekly update slot is part of the product.

### Steal a Brainrot (2025): meme timing + PvP-lite stealing
- **Facts:** released **2025-05-15** by BRAZILIAN SPYDER (@do_small, @SpyderSammy). Became the first game over 25M CCU: **25,836,222 on 2025-10-11** (Update 20). A movie deal was announced later (GameSpot). Clones appeared in Fortnite UEFN.
- **Mechanics:** buy brainrot characters off a conveyor, they generate income in your base, and other players can **steal** them by carrying them out. Base locks and timers.
- **Lessons:** riding a meme at the right moment matters a lot. Asymmetric "steal" interactions create stories, revenge and sessions. Simple base-defense provides social conflict without combat skill. Expect clones, and ship faster than they do.

### Adopt Me! (2017–): the trading-economy archetype
- **Facts:** Uplift Games. First game to cross 1M CCU: **1,615,085 on 2020-04-11**; record **1,920,887** in April 2021. The team grew **from 4 to 29 people** between June 2019 and about April 2020.
- **Mechanics:** a roleplay hub became a **pet-collecting and trading economy** (eggs, limited pets that rotate out, neon/mega fusions).
- **Lessons:** limited-time eggs plus trading create durable value and FOMO, but they also invite **scams and real-money trading**, so build trade-confirmation UX and logging from day one. Scale the team *after* traction. A cosy roleplay theme gives broad reach across ages and genders.

### Doors (LSPLASH, 2022–): YouTuber-driven co-op horror
- **Facts:** released **2022-08-10**. Went viral through top Roblox YouTubers (KreekCraft, Thinknoodles, Flamingo) and streamers (iShowSpeed, xQc). About 2B visits by Feb 2023. All-time peak about **381,720 CCU on 2023-01-29**. Floor 2 "The Mines" shipped **2024-08-30**, roughly 2 years later, with smaller updates (Hotel+) in between.
- **Lessons:** reaction-friendly design (jump scares, named entities, procedural rooms) is free marketing. The lobby → elevator → reserved-server pattern ([[Server-Scaling-And-Matchmaking]]) suits co-op. Long gaps between big content drops are survivable only with a strong brand and merch, which most games don't have.

### Pet Simulator 99 (BIG Games, 2023–): sequel launch muscle
- **Facts:** launched **2023-12-01** (Pet Simulator X's successor). Peak **732,936 CCU on 2023-12-09**, 8 days after launch. Frequent numbered updates and limited "Huge" pets. Off-platform reselling of pets and gems on marketplaces like eBay shows the RMT pressure.
- **Lessons:** a franchise with an existing audience gives the launch spike up front. The challenge then shifts to update cadence and economy integrity. Watch the DMCA backlash risk: BIG Games was criticised in 2023 for DMCA'ing PSX lookalikes, and the community reacted against it.

### Dress to Impress (Gigi / DTI Group, 2023–): underserved audience
- **Facts:** created 2023-10-18, public **2023-11-11**. Routinely Roblox's top game in Sept 2024 (about 250k average). **Charli XCX "Brat" collab** (Aug 2024) brought about 600k CCU on release day. **About 1.8M CCU** with the Dec 2024 winter update. Won Builderman Award of Excellence, Best Creative Direction and Best New Experience at the 2024 Roblox Innovation Awards.
- **Mechanics:** a timed theme prompt, dress up in about 5 min, a runway, players vote. A short round that produces a shareable outcome (TikTok/YouTube Shorts).
- **Lessons:** a large audience (fashion, mostly girls) was underserved. Rounds that produce shareable content act as user acquisition. Brand collabs work once you have scale.

### Blox Fruits (Gamer Robot, 2019–): big numbered updates
- **Facts:** launched 2019. Hit **1M CCU for the first time around Update 20 (2023-10-21)**. About 60B visits by 2026 (RoWatcher). Big updates arrive months apart with countdown hype, and patches in between.
- **Lessons:** a deep progression grind (levels, seas, fruits) plus anime IP-adjacent fantasy keeps players for years. Big numbered updates with announced dates create spikes. Long-lived games can grow years after launch.

### Frontlines (MAXIMILLIAN, 2023): quality is not retention
- **Facts:** released **2023-02-22**, a "CoD-quality" shooter. 13M visits in under a month on creator buzz. Peak **11,650 CCU**. Later about 300–1,100 average and a recent 30-day peak of about 594, attributed to **lack of content** (fan wiki / Rolimons).
- **Lessons:** AAA visuals win attention, not retention. Shooters need a steady stream of maps, modes and progression, plus enough server fill for matchmaking. High production cost per update is a cadence trap. Plan content you can ship weekly before you plan graphics.

### BedWars (Easy.gg): decline after the peak
- **Facts:** once among Roblox's top games; YouTube analyses describe a **> 90% player-base decline** from peak (⚠️ verify exact numbers on Rolimons/RoMonitor).
- **Lessons:** balance churn, monetised kits perceived as pay-to-win, and the competitive meta can push casual players out. Protect the new-player experience in PvP (skill-based or casual queues) ([[Pay-To-Win-Boundaries]]).

### Platform data incident: Roblox DataStores, Oct 2020
- **Facts:** a game-server update broke `GetDataStore` requests. **Data saved between 10:02 and 11:15 AM PST on affected servers was lost or reverted.** Backup systems that used OrderedDataStore pointers (DataStore2 pattern) went out of sync. Roblox published an incident report and recovery guidance.
- **Lessons:** design for platform failure. Use versioned saves, a schema version, "never save if the load failed", and a tested restore script. Keep your own receipt ledger for Robux purchases.

### Generic "died after launch" pattern (DevForum)
- **Pattern:** a few hundred players at launch, then a slow fade over weeks. The thread "So your game died…" (DevForum, 2023) attributes this to saturated genres, no hook beyond the trend, and no update plan.
- **Lessons:** validate the concept with thumbnails and ads before building, plan 6–8 weeks of updates before launch, and build a community (Discord, groups) that outlives the trend.

## Cross-case patterns → rules for this vault
| Pattern | Rule | Note |
|---|---|---|
| Fixed-time global events | Schedule weekly events and updates at a fixed hour | [[Live-Ops-Playbook]] |
| Collectibles + rarity + trading | Build trade UX, logs and dupe detection before launch | [[Data-Persistence-DataStores-And-ProfileStore]] |
| Meme/trend timing | Keep a reusable codebase so a trend game ships in 1–2 weeks | [[Team-And-Budget]] |
| Creator/streamer fuel | Design for reaction moments; ship influencer-friendly codes | [[Discovery-Algorithm]] |
| Content cadence | No gap > 2 weeks without new content or events in year one | [[Content-Cadence]] |
| Economy integrity | Server-authoritative grants, analytics on sources and sinks | [[Analytics-And-Instrumentation]] |

## Checklist (apply to your own game quarterly)
- [ ] Which case is your game closest to? Which of its failure modes apply?
- [ ] Is there a shared, timed moment each week?
- [ ] Is there a 6-week content runway?
- [ ] Trading/economy: dupe detection, trade logs, rollback plan?
- [ ] Is your save system restorable within 1 hour?

## Pitfalls
- Copying the surface (theme) instead of the mechanism (shared timers, stealing, round-based sharing).
- Treating CCU records as typical. The median game never reaches 1k CCU.
- Many figures here come from fan wikis and press. Re-verify before quoting them externally.

## Related
- [[Operations/_Index]] · [[Bad-Launch-Response]] · [[Live-Ops-Playbook]] · [[KPI-Dashboard-Spec]] · [[Team-And-Budget]]
- [[Content-Cadence]] · [[Discovery-Algorithm]] · [[Growth-Metrics-And-Benchmarks]] · [[Pay-To-Win-Boundaries]] · [[Retention-Metrics-D1-D7-D30]]

## Sources
(All accessed 2026-10-04 via web search; some summaries come from search snippets because Wikipedia was unreachable from this environment. ⚠️ verify the specific numbers before citing externally.)
- Grow a Garden: https://en.wikipedia.org/wiki/Grow_a_Garden ; https://x.com/Roblox_RTC/status/1959281995453706447 ; https://www.pocketgamer.biz/robloxs-grow-a-garden-hits-industry-record-213m-concurrent-users-surpassing-pubg-fortnite-and-more/ ; https://www.gamedeveloper.com/business/roblox-s-grow-a-garden-had-nearly-22-million-concurrent-users-in-july ; https://gamesbeat.com/janzen-madsen-interview/ ; https://about.roblox.com/newsroom/2025/06/roblox-infrastructure-supporting-record-breaking-games ; schedule: https://www.pcgamesn.com/grow-a-garden/update-schedule
- Steal a Brainrot: https://en.wikipedia.org/wiki/Steal_a_Brainrot ; https://www.pocketgamer.biz/robloxs-steal-a-brainrot-becomes-first-game-to-surpass-25m-concurrent-players/ ; https://www.gamespot.com/articles/steal-a-brainrot-the-incredibly-popular-roblox-game-gets-a-movie-deal/1100-6537778/
- Adopt Me!: https://x.com/Bloxy_News/status/1383068710567485441 ; https://www.playadopt.me/news/cute-pet-collecting-roblox-game-adopt-me-sets-new-record ; https://en.wikipedia.org/wiki/Adopt_Me!
- Doors: https://en.wikipedia.org/wiki/Doors_(game) ; https://www.pcgamesn.com/roblox/doors-horror-game
- Pet Simulator 99: https://pet-simulator.fandom.com/wiki/Pet_Simulator_99 ; https://www.dexerto.com/roblox/pet-simulator-x-creator-under-fire-for-hypocritical-dmca-on-roblox-games-2284798/
- Dress to Impress: https://en.wikipedia.org/wiki/Dress_to_Impress_(video_game) ; https://www.crossplay.news/p/who-makes-dress-to-impress-on-roblox
- Blox Fruits: https://rowatcher.com/news/the-blox-fruits-timeline-from-2019-launch-to-60-billion-visits-in-2026 ; https://www.pockettactics.com/blox-fruits/update
- Frontlines: https://frontlinesroblox.fandom.com/wiki/FRONTLINES_Wiki ; https://insider-gaming.com/roblox-frontlines-developers/ ; https://www.rolimons.com/game/5938036553
- BedWars: https://www.youtube.com/watch?v=m8UTnnN2c7c (⚠️ secondary source)
- DataStores incident: https://devforum.roblox.com/t/datastores-incident-report/829962
- "So your game died…": https://devforum.roblox.com/t/so-your-game-died-a-thread-on-game-design-and-the-market/2644450
