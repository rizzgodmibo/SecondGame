---
tags: [reference/video]
status: draft
updated: 2026-10-04
confidence: medium
---
# Video Breakdowns: Talks, Devlogs and Tutorials Worth Learning From

Twenty-two videos and talks found by web search on 2026-10-04. **Every URL here appeared in a search result. None were invented.**
YouTube pages could not be opened from this environment (egress blocked), so the breakdowns come from the official descriptions,
companion articles and well-documented talk content. **No timestamps were captured.** Add them after watching
(⚠️ verify). Thumbnails are embedded with YouTube's standard `i.ytimg.com/vi/<id>/hqdefault.jpg` pattern (rendering not tested here).

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

---

## Game feel and F2P design (talks)

### 1. Juice It or Lose It, by Martin Jonasson & Petri Purho (GDC Europe 2012, Independent Games Summit)
![](https://i.ytimg.com/vi/Fy0aCDmgnxg/hqdefault.jpg)
- Link: <https://www.youtube.com/watch?v=Fy0aCDmgnxg> · Vault: <https://www.gdcvault.com/play/1016487/juice-it-or-lose> · about 15 min (⚠️ verify)
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
- Link: <https://www.youtube.com/watch?v=AJdEqssNZ-U> · mirror: <https://archive.org/details/the-art-of-screenshake> · about 30–45 min (⚠️ verify)
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
- Link: <https://www.youtube.com/watch?v=hohwBQGQO7c> · published late Sept or early Oct 2026 (search reported "3 days ago" on 2026-10-04) · creator: Roblox's "Made on Roblox" series (⚠️ verify channel).
- Hook from the description: the team shipped, got on a plane, and woke up to **1M concurrent players**.

### 6. "How 3 Friends Built a Roblox Game With 14 Million Players"
![](https://i.ytimg.com/vi/1cP-NN6nDvY/hqdefault.jpg)
- Link: <https://www.youtube.com/watch?v=1cP-NN6nDvY> · about Aug 2026 (search reported "56 days ago") · creator ⚠️ verify.
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
- Link: <https://www.youtube.com/watch?v=6iB5__RCQDc> · newsroom: <https://about.roblox.com/newsroom/2025/09/roblox-tech-talks-episode-29-creator> · **53 min · 2025-09-05**
- Chapters (from the newsroom listing): Grow a Garden overview → creator engineering → Jandel's vision → massive scale → dev tooling → how Jandel's team works → photorealism → removing toil → organic social experience → AI.
- Takeaways:
  - **"Players helping other players" fuelled growth** (Baszucki). Gifting, shared gardens and trading are growth features, not just social ones.
  - Roblox infra handled the highest CCU of any game ever (about 20M+). You don't need to engineer for scale yourself, but keep servers light.
  - Jandel *bought* Grow a Garden early (from BMWLux) and scaled it with a team ([wiki](https://growagarden.fandom.com/wiki/Jandel)). **Acquiring a promising prototype is a legitimate strategy.**
- Related: GDC 2026 session "Building Boundary-Pushing Games on Roblox" with Janzen Madsen (Splitting Point), Alex Hicks (Twin Atlas) and others. It covered real-player testing, experiment structure and monetisation players value ([GDC schedule](https://schedule.gdconf.com/session/building-boundarypushing-games-on-roblox-faster-iteration-bigger-audiences-better-monetization-developer-showcase-presented-by-roblox/917914)). No public recording was found (⚠️ verify on GDC Vault).

## Growth: thumbnails and ads

### 9. Thumbnail Personalization on Roblox (official)
![](https://i.ytimg.com/vi/I65eJ_uUsY8/hqdefault.jpg)
- Link: <https://www.youtube.com/watch?v=I65eJ_uUsY8> · staff-stream version: <https://events.roblox.com/public/videos/roblox-staff-streams-thumbnail-personalization-walkthrough-2024-11-04> (2024-11-04)

### 10. Thumbnail personalisation explainer embedded in the Roblox Thumbnails doc
![](https://i.ytimg.com/vi/5NvGzKVyKxg/hqdefault.jpg)
- Link: <https://www.youtube.com/watch?v=5NvGzKVyKxg> (found embedded in `creator-docs/production/publishing/thumbnails.md`, commit 9f840b1)
- Takeaways for #9–#10:
  - Personalisation starts with **2+ active thumbnails** (UI allows 2–5). Impressions start evenly split, then **re-weight hourly** toward the winner per user group.
  - The metric is **qualified play-through rate** (qualified plays ÷ home impressions). Average lift **+8.5%**, up to +50% (doc). A staff tips post quotes +12% average, up to +56% ([DevForum](https://devforum.roblox.com/t/5-tips-from-roblox-staff-to-get-the-most-out-of-thumbnail-personalization/3471689)) (⚠️ verify which is current).
  - **Keep losers active.** Test new sets with each major update, then leave them until the next one.

### 11. How to grow your experience with Roblox Ads Manager (official)
![](https://i.ytimg.com/vi/D_YmdVZxIZw/hqdefault.jpg)
- Link: <https://www.youtube.com/watch?v=D_YmdVZxIZw> · docs: <https://create.roblox.com/docs/production/promotion/ads-manager>

### 12. How To Advertise Your Game, Roblox Ads Manager (2024)
- Link: <https://www.youtube.com/watch?v=CPnSjyA1ylA> (community tutorial; creator ⚠️ verify)

### 13. How to make an ad campaign with Roblox Ads Manager
- Link: <https://www.youtube.com/watch?v=5HcH-9E7USc> (about Feb 2026 per "241 days ago"; creator ⚠️ verify)
- Takeaways for #11–#13 (cross-checked with the docs and DevForum):
  - Campaign objectives: **Plays**, **Earnings** (likely spenders) and **Engagement**. Pick Earnings only once monetisation is proven.
  - Placements: Sponsored Experiences on Home, search ads, and immersive ads (image, video, portal) inside other games.
  - Up to **10 thumbnail creatives per campaign**. Sponsored units moved from 1:1 to **16:9**, with up to +40% PTR in the Sponsored sort ([DevForum](https://devforum.roblox.com/t/leveling-up-ads-manager-with-new-features/3587640)) (⚠️ verify current spec).
  - Apply in [[Sponsored-Ads-And-Paid-Acquisition]].

## Engineering

### 14. Stop Using Default DataStores! Use ProfileStore Instead
![](https://i.ytimg.com/vi/m2SP_TLeWHI/hqdefault.jpg)
- Link: <https://www.youtube.com/watch?v=m2SP_TLeWHI> · uploaded **2025-01-22** · creator ⚠️ verify
- Takeaways: ProfileStore (by loleris, successor to ProfileService) gives **session locking** (one server owns a profile, which prevents dupes and rollback), auto-save and a template reconcile. Use one profile per player. Official thread: [DevForum](https://devforum.roblox.com/t/profilestore-save-your-player-data-easy-datastore-module/3190543).

### 15. Sell Developer Products EASILY with ProfileStore
- Link: <https://www.youtube.com/watch?v=8FIj3gmP5Ls> · also see the @Rileybytes "Secure Developer Product handling with ProfileStore" series
- Takeaways: record the receipt `PurchaseId` inside the profile before granting, and only return `PurchaseGranted` after the profile save path is safe. This is idempotent receipt handling. See [[ProcessReceipt-Handling]].

### 16. Roblox Staff Stream: Optimize your economy and funnels with Analytics
- Link: <https://youtu.be/NFLP-FVv834> · event page: <https://events.roblox.com/public/events/roblox-staff-streams-optimize-your-economy-and-funnels-with-analytics-7jkqamv5wr> (July 2024)
- Takeaways: instrument **onboarding, progression and shop funnels** with `AnalyticsService` funnel events, and economy sources and sinks with economy events. Find the step with the largest drop-off and fix that first. See [[Analytics-And-Instrumentation]] and [[Onboarding-And-First-60-Seconds]].

## Art pipeline

### 17. Particles, Beams and Trails, Roblox Effects Tutorial
![](https://i.ytimg.com/vi/LGVajPx6QNc/hqdefault.jpg)
- Link: <https://www.youtube.com/watch?v=LGVajPx6QNc>

### 18. Roblox Flipbook Particles Are Extremely Powerful
- Link: <https://www.youtube.com/watch?v=TdU0A8etl1o> · companion: "I Made 40+ Particle Flipbooks So You Don't Have To" <https://www.youtube.com/watch?v=IsbbYSKjTYo>

### 19. Roblox Beams Can Make Amazing VFX
- Link: <https://www.youtube.com/watch?v=yK_BSF3p8sk>
- Takeaways for #17–#19:
  - **Layer 3–5 systems per effect**: core flash (particle), shockwave (mesh tween), streaks (beam or trail), lingering embers (particle).
  - **Flipbooks** (`FlipbookLayout` grid 2×2, 4×4 or 8×8, with `FlipbookMode` Loop/OneShot/PingPong) give animated fire, smoke and electric effects from one emitter ([release thread](https://devforum.roblox.com/t/particles%E2%80%99-flipbook-release/2029388)).
  - **Beams** render a texture between two attachments. Use curve, width and transparency sequences for slashes, lasers and auras.
- Apply in [[VFX-Particles-Beams-Trails]] and [[VFX-And-Art-Style-Reference]].

### 20. Blender-to-Roblox Imports: Easy Step-by-Step Tutorial
- Link: <https://www.youtube.com/watch?v=edi2Z3kkIpk> · also "How To Make Roblox Animation In Blender [+Export/Import]" <https://www.youtube.com/watch?v=SFVrOP50hy0>
- Takeaways: export **FBX**. Apply rotation and scale first, **disable Add Leaf Bones**, enable Bake Animation for animations, and watch unit scale (0.01 vs 1.0 depending on scene units). Rigged meshes need clean weights before the 3D Importer ([Roblox export requirements](https://create.roblox.com/docs/art/modeling/export-requirements)). See [[Blender-To-Roblox-Pipeline]].

### 21. UI juice and style
- "How to Animate UI SMOOTHLY on Roblox (TweenService Tutorial)": <https://www.youtube.com/watch?v=9YbTZ8syR4c>
- "How To Make Simulator UI Buttons In Figma": <https://www.youtube.com/watch?v=k69tudey-vs> · "The Greatest Stud UI Tutorial on Roblox (w/ Figma)": <https://www.youtube.com/watch?v=gnIKtS3nUqo>
- Takeaways: design buttons in Figma with a thick dark stroke, an inner gradient, a drop shadow and a chunky rounded font (the simulator style). In Studio, use `UIStroke` + `UIGradient` + `UICorner`. Animate `.Activated` with a scale tween (press 0.9 → release 1.05 → 1.0) and hover with `MouseEnter` scale 1.05. See [[UI-Polish-And-Juice]].

### 22. How To Create Quality Roblox Thumbnails
![](https://i.ytimg.com/vi/uS4cB1w_7gI/hqdefault.jpg)
- Link: <https://www.youtube.com/watch?v=uS4cB1w_7gI> · also "How to Make a ROBLOX GFX in 2025": <https://www.youtube.com/watch?v=6oJeyR_HzNM>
- Takeaways: export avatar or scene from Studio (character at origin 0,0,0, then **Export Selection**). Import to Blender, then pose, add 3-point lighting and render. Add text and FX in a 2D editor. **Ad and video thumbnails must still represent real gameplay** ([Thumbnails doc](https://create.roblox.com/docs/production/publishing/thumbnails)). Stylised GFX are fine for static thumbnails, but avoid "artificially enhancing graphics" in video.

---

## Also found (lower priority)
- RDC playlists: [RDC 2025](https://www.youtube.com/playlist?list=PLd4YbQRYwtYs0VvyhEjNOEUVm_Ow7iFY1) (⚠️ verify it is official), [RDC (Roblox)](https://www.youtube.com/playlist?list=PLqPUvwA4HDG-l8HmVA--d80uEurDqPcBz). A "Science of Game Discovery" RDC session with 99 Nights and Ninja Challenge case studies was mentioned in search, but **no URL was found** (⚠️ find it).
- "Top 50 Most Played Roblox Games, AUGUST 3, 2026 (Daily Player Count)": <https://www.youtube.com/watch?v=sHi3oXV7sMM>. Useful for trend spotting.
- "Roblox ProfileStore Is a Great Alternative To ProfileService!": <https://www.youtube.com/watch?v=hh2nPZjKT4g>

## Checklist
- [ ] Watch #1, #2, #8 and #10 fully and add timestamps.
- [ ] Find official recordings for the RDC 2025 discovery session and GDC 2026 Roblox showcase.
- [ ] Fill creator names marked ⚠️ verify.

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
