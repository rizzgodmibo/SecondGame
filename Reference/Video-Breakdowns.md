---
tags: [reference/video]
status: draft
updated: 2026-10-04
confidence: medium
---
# Video Breakdowns: Talks, Devlogs and Tutorials Worth Learning From

Twenty-two videos and talks found by web search on 2026-10-04, plus #23 (watched in full, with its own note). **Update 2026-10-04 (later):** YouTube opened in the logged-in browser, so channels, durations, dates and view counts are now verified and timestamps come from the captions; #9 and #10 turned out to be the same talk. **Every URL here appeared in a search result. None were invented.**
Original breakdowns came from descriptions and companion articles; timestamps marked 'from the transcript' were read from YouTube captions on 2026-10-04 (not watched frame by frame). Thumbnails are embedded with YouTube's standard `i.ytimg.com/vi/<id>/hqdefault.jpg` pattern (rendering not tested here).

## TL;DR
- **Game feel first:** watch *Juice It or Lose It* (#1) and *The Art of Screenshake* (#2) before building any UI or combat. Together they give about 40 concrete tweaks that turn a flat prototype into a satisfying one.
- **Copy how the hits were made:** 99 Nights was a one-week jam that grew into a 3-month sprint. It mashed a trend ("survive N days") with a hit (Dead Rails) and a cosy theme (#5–#7). Grow a Garden grew through players helping other players (#8).
- **Growth levers are measurable:** thumbnail personalisation (#9–#10) and Ads Manager objectives Plays/Earnings/Engagement (#11–#13) are free or self-serve. Learn both before launch.
- **Data:** use ProfileStore with session locking, not raw DataStores (#14–#15). See [[Data-Persistence-DataStores-And-ProfileStore]].
- **Art pipeline:** layer VFX from 3–5 systems (particles + beams + trails + meshes) and use flipbooks for animated textures (#17–#19). FBX from Blender: apply transforms, no leaf bones, check scale (#20).

## Quick index
| # | Video | Type | Topic |
|---|---|---|---|
| 1 | Juice It or Lose It | GDC Europe 2012 | Game feel |
| 2 | The Art of Screenshake | INDIGO 2013 | Game feel |
| 3 | Economic Balancing… Clever Sink Design | GDC Vault | F2P economy |
| 4 | Monetizing Economy Based F2P Games | GDC Vault | F2P monetisation |
| 5 | They built 99 Nights in 3 months (Made on Roblox #1) | Roblox documentary | Origin story |
| 6 | How 3 Friends Built a Roblox Game With 14 Million Players | Documentary/analysis | Origin story |
| 7 | Creator Spotlight: Story Behind 99 Nights (article) | DevForum | Origin story |
| 8 | Tech Talks EP29: Creator (Baszucki × Jandel × Tornow) | Roblox podcast | Grow a Garden, scale |
| 9 | Thumbnail Personalization on Roblox | Roblox official | Thumbnails |
| 10 | Thumbnail personalization (embedded in Roblox docs) | Roblox official | Thumbnails |
| 11 | How to grow your experience with Roblox Ads Manager | Roblox official | Paid UA |
| 12 | How To Advertise Your Game, Roblox Ads Manager (2024) | Community tutorial | Paid UA |
| 13 | How to make an ad campaign with Roblox Ads Manager | Community tutorial | Paid UA |
| 14 | Stop Using Default DataStores! Use ProfileStore Instead | Tutorial | Data |
| 15 | Sell Developer Products EASILY with ProfileStore | Tutorial | Receipts |
| 16 | Roblox Staff Stream: economy & funnels with Analytics | Roblox official | Analytics |
| 17 | Particles, Beams and Trails, Roblox Effects Tutorial | Tutorial | VFX |
| 18 | Roblox Flipbook Particles Are Extremely Powerful | Tutorial | VFX |
| 19 | Roblox Beams Can Make Amazing VFX | Tutorial | VFX |
| 20 | Blender-to-Roblox Imports: Easy Step-by-Step | Tutorial | 3D pipeline |
| 21 | How to Animate UI SMOOTHLY (TweenService) / Simulator UI Buttons in Figma | Tutorials | UI juice |
| 22 | How To Create Quality Roblox Thumbnails | Tutorial | Thumbnail GFX |
| 23 | How to Make a Roblox Game With AI (Claude Opus 5.5 Full Tutorial), SyphoDev | Workflow tutorial (watched in full) | Claude Code skills + MCP + APIs |

---

## Game feel and F2P design (talks)

### 1. Juice It or Lose It, by Martin Jonasson & Petri Purho (GDC Europe 2012, Independent Games Summit)
![](https://i.ytimg.com/vi/Fy0aCDmgnxg/hqdefault.jpg)
- Link: <https://www.youtube.com/watch?v=Fy0aCDmgnxg> · Vault: <https://www.gdcvault.com/play/1016487/juice-it-or-lose> · **15:37 · grapefrukt · 2012-05-24 · 612k views** (verified 2026-10-04)
- Timestamps (from the transcript): 0:35 'juice = maximum output for minimum input' · 2:22 add colour · 2:43 tweening (ease-out, then overshoot 'Back' at 4:38) · 5:44 paddle/ball stretch and wobble, white hit flash (6:52) · 8:00 sound demo (two balls, with vs without sound) · 9:08 music · 9:37 particles (smoke, shattering at 11:20) · 12:24 ball trail ('comet') · 13:28 give the paddle a face that smiles or frowns · 15:18 wrap-up.
- They turn a grey Breakout clone into a "juicy" one live on stage ([roblog summary](https://roblog.co.uk/2024/03/juicy-games/)).
- Takeaways for Roblox:
  - **Tween everything.** Nothing should snap into place. Use ease-out-back or elastic on spawn (`TweenService`, `Enum.EasingStyle.Back`).
  - **Squash and stretch** on impact, and scale-pop on collect (UI and parts).
  - **Particles on every event** (hit, break, collect). Add colour variation and randomised size.
  - **Sound on every interaction**, with pitch variation (±5–10%) so repeats don't fatigue.
  - **Screen shake on big events only.** Keep it small and short. Respect a reduce-motion setting.
  - **Personality:** give objects eyes or reactions. Even blocks become characters.
- Apply in: [[UI-Polish-And-Juice]].

### 2. The Art of Screenshake, by Jan Willem Nijman, Vlambeer (INDIGO Classes 2013)
![](https://i.ytimg.com/vi/AJdEqssNZ-U/hqdefault.jpg)
- Link: <https://www.youtube.com/watch?v=AJdEqssNZ-U> · mirror: <https://archive.org/details/the-art-of-screenshake> · **44 min · Dutch Game Garden · 2013-12-16 · 384k views** (verified 2026-10-04)
- Timestamps (from the transcript): 0:05–7:50 intro and what game feel is · **7:51–29:52 the live tweak-by-tweak demo** (bigger, faster bullets and a higher fire rate about 9:25; muzzle flash 10:58; enemy knockback 12:31; camera 15:40; hit sleep and impact about 18:47; permanence about 20:21; camera kick 25:09) · 29:52 before/after comparison · 30:00+ Q&A (designers stop seeing their own game after a while, 32:59).
- He applies about 30 tiny tweaks to a boring platform shooter ([summary](http://notebook.maryrosecook.com/Theartofscreenshake,JanWillemNijman.html)).
- Takeaways (in order of impact):
  - Bigger bullets, faster bullets, less accuracy (random spread) so it feels like spray.
  - **Muzzle flash, impact effects, enemy hit flash (white frame), knockback** on hit.
  - **Hit-stop ("sleep")**: freeze 20–60 ms on a heavy hit. On Roblox, briefly drop the animation speed on attacker and victim.
  - **Permanence:** shell casings and debris stay. Players like seeing the mess they made.
  - **Camera:** lerp toward aim direction, kick on fire, shake on explosion.
  - Explosions are always bigger than you think. Add a sound bass layer.
- Apply in: combat games ([[VFX-Particles-Beams-Trails]], [[Animation-Rigging-And-IK]]).

### 3. Economic Balancing and Improved Monetization Through Clever Sink Design (GDC Vault)
- Link: <https://www.gdcvault.com/play/1020085/Economic-Balancing-and-Improved-Monetization>
- Takeaways: sinks (things that remove currency or items) keep an economy balanced *and* make purchases meaningful. Every faucet needs a sink at a similar rate. Apply in [[Economy-Design-Sinks-And-Faucets]].

### 4. Monetizing Economy Based Free-to-Play Games, by Teut Weidemann, Ubisoft (GDC Vault)
- Link: <https://www.gdcvault.com/play/1016680/Monetizing-Economy-Based-Free-to>
- Takeaways: uses *The Settlers Online* as a case study. Monetise **time and convenience** inside a working economy, not power. This maps to Roblox dev products such as boosts and skips (see [[Robux-Economy-DevEx-And-Platform-Cuts]]).
- See also the [Game Developer write-up on gacha's dark side](https://www.gamedeveloper.com/business/video-monetization-design-and-overcoming-the-dark-side-of-gacha). War Robots' economy change raised revenue but hurt the community. It is a cautionary example.

## How the big Roblox hits were made

### 5. "They built 99 Nights in 3 months… it blew up overnight" (Made on Roblox #1)
![](https://i.ytimg.com/vi/hohwBQGQO7c/hqdefault.jpg)
- Link: <https://www.youtube.com/watch?v=hohwBQGQO7c> · **52 min · Roblox Learn · 2026-09-30** (verified 2026-10-04)
- Chapters (official): 0:45 Grandma's Favourite Games · 2:00 Roblox origin story · 7:00 Parkour Tower · 9:20 Mall Tycoon · 11:20 Wacky Wizards · 12:15 Break In 1 & 2 · 15:00 99 Nights · 25:00 getting feedback from other creators · 30:30 99 Nights origin · 32:45 hitting a million CCU · 34:00 updates and live-ops schedule · 36:00 community feedback · 40:00 lessons · 44:00 the movie · 47:00 advice to creators · 50:00 future.
- From the transcript: **honest feedback comes from watching strangers play who don't know you're watching**, e.g. from alt accounts (about 27:15); some 'programmer art' was kept because it read clearly (about 21:13); new players arriving so fast meant no urgency for new content early on (about 33:20); **after burnout the team took a six-week break and the game trended up** (36:24–42:34); the four rescued kids got gameplay uses because the community asked (about 39:31); advice: pick a bite-size project to find the fun (about 48:43).
- Hook from the description: the team shipped, got on a plane, and woke up to **1M concurrent players**.

### 6. "How 3 Friends Built a Roblox Game With 14 Million Players"
![](https://i.ytimg.com/vi/1cP-NN6nDvY/hqdefault.jpg)
- Link: <https://www.youtube.com/watch?v=1cP-NN6nDvY> · **15 min · Mina RS (third-party explainer) · 2026-08-08** (verified 2026-10-04)
- From the transcript: opens with '14,153,173' concurrent players on 2025-10-04 (⚠️ third-party figure; check against Roblox records) · 1:33 Studio sitting next to the player app is how kids crossed over · 4:39 Break In was 'naturally good content' for YouTubers (story games give creators a beginning, chaos, characters) · 7:45 built March, launched June, their fastest cycle (earlier projects took about 6 months) · 9:18 speed came from years of working together · 10:50 the game keeps 'manufacturing video ideas' for creators and TikTok · **12:23 weekly 45-minute sandbox 'update party' before each update** (rules off, devs spawn rewards and chaos) · 13:58 film rights.
- Covers Alec "Cracky4" Kieft, Cameron Angland and Matt Hufton of Grandma's Favourite Games (NZ). They met through Roblox war clans.

### 7. Creator Spotlight: The Story Behind 99 Nights in the Forest (DevForum article plus Roblox X post)
- Link: <https://devforum.roblox.com/t/creator-spotlight-the-story-behind-99-nights-in-the-forest/4036940> · interview: [PCGamesN](https://www.pcgamesn.com/roblox/99-nights-in-the-forest-interview)
- Combined takeaways from #5–#7:
  - **Start as a one-week jam, then commit.** It became a 3-month sprint before launch, now daily live-ops.
  - **The idea formula:** trending format ("survive # days") + current hit's mechanic (Dead Rails) + a fresh, cosy theme (forest campfire).
  - **Years of team workflow before the hit.** The trio had shipped together for years. The hit came from a practised pipeline, not luck.
  - Peak of **14M CCU within months** of a June launch. Seasonal updates (Halloween) keep it alive.

### 8. Tech Talks EP29: "Creator" (David Baszucki, Nick Tornow, Jandel of Grow a Garden)
![](https://i.ytimg.com/vi/6iB5__RCQDc/hqdefault.jpg)
- Link: <https://www.youtube.com/watch?v=6iB5__RCQDc> · newsroom: <https://about.roblox.com/newsroom/2025/09/roblox-tech-talks-episode-29-creator> · **53 min · Roblox · 2025-09-05 · 79k views** (verified 2026-10-04)
- Transcript timestamps: 0:00 intros · 4:04 Jandel's years of games ('10,000 hours') · 8:09 creator-engineering mandate · 12:12 imagining 20M players in one event · 16:15 planning capacity for explosive games · 20:19 team-create collaboration · 24:23 Jandel's team still uses external git-style review for leads · **32:33 Grow a Garden is fun to return to every two weeks with no pressure to log in daily (not engagement hacks)** · 36:37 AI assistant ('add 10,000 trees') · 40:42 frequent updates and experiments versus games left unchanged for 6 months · 44:46 balancing A/B tuning with big leaps.
- Chapters (from the newsroom listing): Grow a Garden overview → creator engineering → Jandel's vision → massive scale → dev tooling → how Jandel's team works → photorealism → removing toil → organic social experience → AI.
- Takeaways:
  - **"Players helping other players" fuelled growth** (Baszucki). Gifting, shared gardens and trading are growth features, not just social ones.
  - Roblox infra handled the highest CCU of any game ever (about 20M+). You don't need to engineer for scale yourself, but keep servers light.
  - Jandel *bought* Grow a Garden early (from BMWLux) and scaled it with a team ([wiki](https://growagarden.fandom.com/wiki/Jandel)). **Acquiring a promising prototype is a legitimate strategy.**
- Related: GDC 2026 session "Building Boundary-Pushing Games on Roblox" with Janzen Madsen (Splitting Point), Alex Hicks (Twin Atlas) and others. It covered real-player testing, experiment structure and monetisation players value ([GDC schedule](https://schedule.gdconf.com/session/building-boundarypushing-games-on-roblox-faster-iteration-bigger-audiences-better-monetization-developer-showcase-presented-by-roblox/917914)). No public recording was found (⚠️ verify on GDC Vault).

## Growth: thumbnails and ads

### 9–10. Thumbnail Personalization walkthrough (official; one talk, two uploads)
![](https://i.ytimg.com/vi/I65eJ_uUsY8/hqdefault.jpg)
- Links: <https://www.youtube.com/watch?v=I65eJ_uUsY8> (Roblox Learn, 2024-11-13, 9 min) and <https://www.youtube.com/watch?v=5NvGzKVyKxg> (Roblox Documentation, 2024-10-31, embedded in the Thumbnails doc). **Duplicate content**: the transcripts are identical (checked 2026-10-04). Staff-stream page: <https://events.roblox.com/public/videos/roblox-staff-streams-thumbnail-personalization-walkthrough-2024-11-04>
- Timestamps: 0:07 intro (Discovery and Creator Analytics leads) · 1:11 why one thumbnail can't fit every player · 2:15 how it works: per-group qualified play-through, with a little traffic kept for exploration · 4:27 creator pilot results · 5:32 Creator Hub demo (set all to active, save) · **6:34 today's winner won't always win** · **7:38 restart personalization at each content update or big event** · 8:40 tips: try new perspectives (e.g. first-person behind the wheel for a driving game).
- Takeaways:
  - Personalisation starts with **2+ active thumbnails** (UI allows 2–5). Impressions start evenly split, then **re-weight hourly** toward the winner per user group.
  - The metric is **qualified play-through rate** (qualified plays ÷ home impressions). Average lift **+8.5%**, up to +50% (doc). A staff tips post quotes +12% average, up to +56% ([DevForum](https://devforum.roblox.com/t/5-tips-from-roblox-staff-to-get-the-most-out-of-thumbnail-personalization/3471689)) (⚠️ verify which is current).
  - **Keep losers active.** Test new sets with each major update, then leave them until the next one.

### 11. How to grow your experience with Roblox Ads Manager (official)
![](https://i.ytimg.com/vi/D_YmdVZxIZw/hqdefault.jpg)
- Link: <https://www.youtube.com/watch?v=D_YmdVZxIZw> · docs: <https://create.roblox.com/docs/production/promotion/ads-manager> · **60 min · Roblox Learn · 2025-06-09** (verified 2026-10-04)

### 12. How To Advertise Your Game, Roblox Ads Manager (2024)
- Link: <https://www.youtube.com/watch?v=CPnSjyA1ylA> · **11 min · DSCreations · 2024-05-04 · 49k views** · chapters: 1:00 Ads Manager and ad credits · 3:30 setting up sponsors · 5:50 getting the best players

### 13. How to make an ad campaign with Roblox Ads Manager
- Link: <https://www.youtube.com/watch?v=5HcH-9E7USc> · **3 min · Roblox Learn · 2026-02-04 · 88k views** · chapters: 0:42 picking goals · 1:04 audiences · 1:43 budget · 2:16 creative · 2:36 advanced targeting · 2:56 reporting
- Takeaways for #11–#13 (cross-checked with the docs and DevForum):
  - Campaign objectives: **Plays**, **Earnings** (likely spenders) and **Engagement**. Pick Earnings only once monetisation is proven.
  - Placements: Sponsored Experiences on Home, search ads, and immersive ads (image, video, portal) inside other games.
  - Up to **10 thumbnail creatives per campaign**. Sponsored units moved from 1:1 to **16:9**, with up to +40% PTR in the Sponsored sort ([DevForum](https://devforum.roblox.com/t/leveling-up-ads-manager-with-new-features/3587640)) (⚠️ verify current spec).
  - Apply in [[Sponsored-Ads-And-Paid-Acquisition]].

## Engineering

### 14. Stop Using Default DataStores! Use ProfileStore Instead
![](https://i.ytimg.com/vi/m2SP_TLeWHI/hqdefault.jpg)
- Link: <https://www.youtube.com/watch?v=m2SP_TLeWHI> · **27 min · Rileybytes · 2025-01-22 · 128k views** · chapters: 1:09 how it works · 2:04 vs DataStores · 2:42 upgrading from ProfileService · 5:39 testing trick · 6:23 profile creation · 12:05 DataManager · 17:48 player leaving · 19:29 enable API access · 24:38 peeking inside a profile
- Takeaways: ProfileStore (by loleris, successor to ProfileService) gives **session locking** (one server owns a profile, which prevents dupes and rollback), auto-save and a template reconcile. Use one profile per player. Official thread: [DevForum](https://devforum.roblox.com/t/profilestore-save-your-player-data-easy-datastore-module/3190543).

### 15. Sell Developer Products EASILY with ProfileStore
- Link: <https://www.youtube.com/watch?v=8FIj3gmP5Ls> · **38 min · Rileybytes · 2025-01-30** · key chapters: 12:12 what ProcessReceipt is · 14:45 the callback · 18:16 using profiles · **23:11–34:50 CheckPurchaseIdAsync using `Profile.LastSavedData`, `Profile:IsActive()`, `Profile:Save()` and `Profile.OnAfterSave:Wait()`** (read from the transcript; all four confirmed in ProfileStore source commit 45c9847)
- Takeaways: record the receipt `PurchaseId` inside the profile before granting, and only return `PurchaseGranted` after the profile save path is safe. This is idempotent receipt handling. See [[ProcessReceipt-Handling]].

### 16. Roblox Staff Stream: Optimize your economy and funnels with Analytics
- Link: <https://youtu.be/NFLP-FVv834> · **21 min · Roblox Learn · 2024-07-24** · event page: <https://events.roblox.com/public/events/roblox-staff-streams-optimize-your-economy-and-funnels-with-analytics-7jkqamv5wr> (July 2024)
- Takeaways: instrument **onboarding, progression and shop funnels** with `AnalyticsService` funnel events, and economy sources and sinks with economy events. Find the step with the largest drop-off and fix that first. See [[Analytics-And-Instrumentation]] and [[Onboarding-And-First-60-Seconds]].

## Art pipeline

### 17. Particles, Beams and Trails, Roblox Effects Tutorial
![](https://i.ytimg.com/vi/LGVajPx6QNc/hqdefault.jpg)
- Link: <https://www.youtube.com/watch?v=LGVajPx6QNc> · ⚠️ **unavailable**: no video data on 2026-10-04 (likely removed or private). Use #18–#19 instead.

### 18. Roblox Flipbook Particles Are Extremely Powerful
- Link: <https://www.youtube.com/watch?v=TdU0A8etl1o> · **12 min · Paul1Rb · 2024-06-22** · chapters: 0:00 flipbook explanation · 2:45 using flipbooks · 3:43 realistic particles · 9:25 demo place · 10:41 examples · companion: "I Made 40+ Particle Flipbooks So You Don't Have To" <https://www.youtube.com/watch?v=IsbbYSKjTYo>

### 19. Roblox Beams Can Make Amazing VFX
- Link: <https://www.youtube.com/watch?v=yK_BSF3p8sk> · **10 min · Paul1Rb · 2024-10-02** · chapters: 0:14 using beams · 0:53 properties · 2:31 texture · 3:40 making a beam · 4:33 laser · 6:41 beam zone · 8:02 where to get textures
- Takeaways for #17–#19:
  - **Layer 3–5 systems per effect**: core flash (particle), shockwave (mesh tween), streaks (beam or trail), lingering embers (particle).
  - **Flipbooks** (`FlipbookLayout` grid 2×2, 4×4 or 8×8, with `FlipbookMode` Loop/OneShot/PingPong) give animated fire, smoke and electric effects from one emitter ([release thread](https://devforum.roblox.com/t/particles%E2%80%99-flipbook-release/2029388)).
  - **Beams** render a texture between two attachments. Use curve, width and transparency sequences for slashes, lasers and auras.
- Apply in [[VFX-Particles-Beams-Trails]] and [[VFX-And-Art-Style-Reference]].

### 20. Blender-to-Roblox Imports: Easy Step-by-Step Tutorial
- Link: <https://www.youtube.com/watch?v=edi2Z3kkIpk> (2 min · PrizeCP Roblox · 2025-05-17) · also "How To Make Roblox Animation In Blender [+Export/Import]" <https://www.youtube.com/watch?v=SFVrOP50hy0>
- Takeaways: export **FBX**. Apply rotation and scale first, **disable Add Leaf Bones**, enable Bake Animation for animations, and watch unit scale (0.01 vs 1.0 depending on scene units). Rigged meshes need clean weights before the 3D Importer ([Roblox export requirements](https://create.roblox.com/docs/art/modeling/export-requirements)). See [[Blender-To-Roblox-Pipeline]].

### 21. UI juice and style
- "How to Animate UI SMOOTHLY on Roblox (TweenService Tutorial)": <https://www.youtube.com/watch?v=9YbTZ8syR4c> (8 min · script_ing · 2022)
- "How To Make Simulator UI Buttons In Figma": <https://www.youtube.com/watch?v=k69tudey-vs> (4 min · voidryxUI, very low views) · "The Greatest Stud UI Tutorial on Roblox (w/ Figma)": <https://www.youtube.com/watch?v=gnIKtS3nUqo> (**62 min · Kek · 2026-06-12 · 52k views**; chapters: 2:33 main frame · 3:50 header · 7:30 exit button · **9:29 stud texture** · 14:57 Robux icon on the buy button · 20:06 gem icon · 34:04 top buttons · 39:15 left buttons · 51:25 currency · 56:30 slow-mode button)
- Takeaways: design buttons in Figma with a thick dark stroke, an inner gradient, a drop shadow and a chunky rounded font (the simulator style). In Studio, use `UIStroke` + `UIGradient` + `UICorner`. Animate `.Activated` with a scale tween (press 0.9 → release 1.05 → 1.0) and hover with `MouseEnter` scale 1.05. See [[UI-Polish-And-Juice]].

### 22. How To Create Quality Roblox Thumbnails
![](https://i.ytimg.com/vi/uS4cB1w_7gI/hqdefault.jpg)
- Link: <https://www.youtube.com/watch?v=uS4cB1w_7gI> · **36 min · Cyress · 2024-02-17 · 98k views** · chapters: 2:37 export avatar from Studio · 4:41 rig in Blender · 14:44 thumbnail idea · 16:25 pose and render · 21:34 rough layout · 27:36 advanced effects · 35:32 export · also "How to Make a ROBLOX GFX in 2025": <https://www.youtube.com/watch?v=6oJeyR_HzNM>
- Takeaways: export avatar or scene from Studio (character at origin 0,0,0, then **Export Selection**). Import to Blender, then pose, add 3-point lighting and render. Add text and FX in a 2D editor. **Ad and video thumbnails must still represent real gameplay** ([Thumbnails doc](https://create.roblox.com/docs/production/publishing/thumbnails)). Stylised GFX are fine for static thumbnails, but avoid "artificially enhancing graphics" in video.

---

## AI workflow

### 23. How to Make a Roblox Game With AI (Claude Opus 5.5 Full Tutorial), by SyphoDev (2026-10-04)
- Link: <https://www.youtube.com/watch?v=afuKhenJldY> · 24:45 · **watched in full with timestamps and frames**. Full breakdown: [[Video-SyphoDev-Claude-Code-Roblox-Workflow]].
- One skill per discipline (code, UI, map, VFX, sound, animation, 3D) plus a manager skill; each skill has its own automated checker.
- Takeaways: gate every change on Rojo build + tests + Selene + StyLua; UI "depth stack" + 5-point checker; 9 raycast map checks; VFX "phase freeze"; Flux (Cloudflare) + Hi3DGen (Kaggle) for images/3D, which conflicts with Holden's no-AI-mesh rule.

## Also found (lower priority)
- RDC playlists: [RDC 2025](https://www.youtube.com/playlist?list=PLd4YbQRYwtYs0VvyhEjNOEUVm_Ow7iFY1) (⚠️ verify it is official), [RDC (Roblox)](https://www.youtube.com/playlist?list=PLqPUvwA4HDG-l8HmVA--d80uEurDqPcBz). A "Science of Game Discovery" RDC session with 99 Nights and Ninja Challenge case studies was mentioned in search, but **no URL was found** (⚠️ find it).
- "Top 50 Most Played Roblox Games, AUGUST 3, 2026 (Daily Player Count)": <https://www.youtube.com/watch?v=sHi3oXV7sMM>. Useful for trend spotting.
- "Roblox ProfileStore Is a Great Alternative To ProfileService!": <https://www.youtube.com/watch?v=hh2nPZjKT4g>

## Checklist
- [x] 2026-10-04: timestamps added for #1, #2, #5, #6, #8, #9–10 from transcripts read in the browser; chapters for #12–#15, #18–#19, #21–#22.
- [ ] Replace #17 (video unavailable).
- [ ] Find official recordings for the RDC 2025 discovery session and GDC 2026 Roblox showcase.
- [x] Creator names, durations and dates verified from YouTube video data (2026-10-04).
- New videos found 2026-10-04 are in [[YouTube-Reference-Library]] (deduplicated against this note).

## Pitfalls
- YouTube auto-generated titles and "x days ago" dates came from search snippets. Confirm the exact upload date before citing it.
- Community tutorials go stale when Roblox ships new APIs (e.g. UI styling, the new Audio API). Check the upload date versus current docs.

## Related
- [[Reference/_Index|Reference index]] · [[UI-Polish-And-Juice]] · [[VFX-Particles-Beams-Trails]] · [[Blender-To-Roblox-Pipeline]]
- [[Thumbnails-And-Icons]] · [[Sponsored-Ads-And-Paid-Acquisition]] · [[Data-Persistence-DataStores-And-ProfileStore]] · [[Core-Loops]]

## Sources
- URLs per entry above (web search, 2026-10-04).
- [roblog: Juicy games summary](https://roblog.co.uk/2024/03/juicy-games/) · [Mary Rose Cook: Art of Screenshake notes](http://notebook.maryrosecook.com/Theartofscreenshake,JanWillemNijman.html)
- [Roblox newsroom: Tech Talks 29](https://about.roblox.com/newsroom/2025/09/roblox-tech-talks-episode-29-creator) · [PCGamesN 99 Nights interview](https://www.pcgamesn.com/roblox/99-nights-in-the-forest-interview)
- Roblox Creator Docs repo @ `9f840b1`: `production/publishing/thumbnails.md`.
