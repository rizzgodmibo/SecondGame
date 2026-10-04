---
tags: [reference/gallery, growth/thumbnails]
status: draft
updated: 2026-10-04
confidence: medium
---
# Icon and Thumbnail Gallery: Top Roblox Games (snapshot 2026-10-04)

A breakdown of the icons and thumbnails of 21 top and recently viral Roblox games, with the patterns they share turned into
rules you can copy. Use it with [[Thumbnails-And-Icons]] (the how-to). This note is the evidence behind it.

## TL;DR
- **Sell one verb and one creature/object.** Every top icon promises a single action: steal, grow, survive, escape, dress, fight. Do not show the whole game.
- **One focal subject fills 50–70% of the 512×512 frame.** Icons are shown as small as 150×150 ([Roblox Icons doc](https://create.roblox.com/docs/production/publishing/experience-icons)). Anything smaller than about 1/6 of the frame disappears.
- **Use colour to say the genre.** Saturated rainbow colours mean a simulator, tycoon or "steal a" game. Dark, cold colours with one warm light mean horror or survival. Royal pink or purple means fashion or roleplay ([Roblox colour guidance](https://create.roblox.com/docs/production/publishing/experience-icons)).
- **Text on the icon is optional. Text on thumbnails is 1–3 words, top half only.** The bottom of a thumbnail can be covered by player-count metadata ([Roblox Thumbnails doc](https://create.roblox.com/docs/production/publishing/thumbnails)).
- **Rotate on updates.** Top games swap the icon emoji, the title tag (`[🥚]`, `[UPD + x2]`) and the thumbnails with every update. Treat the icon as a live-ops surface, not a logo.
- **Keep 2–5 thumbnails active** so thumbnail personalisation can pick a winner for each audience. Roblox measured an average of +8.5% qPTR, and some games gained up to +50% ([Thumbnails doc](https://create.roblox.com/docs/production/publishing/thumbnails)).

> ⚠️ **Capture status (2026-10-04):** this session's network egress **blocked** `apis.roblox.com`, `games.roblox.com`,
> `thumbnails.roblox.com`, `www.roblox.com`, Rolimons, RoMonitor and Wikipedia (HTTP 403 at the proxy). So:
> 1. **The live game icons and thumbnails could not be resolved or embedded.** Each game below has a ready-to-run
>    resolve link. Use the script in [[Reference-Capture-Process]] to turn those links into `![](…)` embeds.
> 2. **The stats below come from tracker pages (Rolimons, RoWatcher, RoVitals, Studiokrew) as quoted in web-search
>    results on 2026-10-04.** They were not read live from the Roblox API. Trackers disagree by up to about 15% on visits.
> 3. **The visual breakdowns rely on wiki, press and guide descriptions plus each game's long-running brand.
>    No pixel inspection was possible.** Each breakdown is marked `⚠️ verify` until someone looks at the resolved image.

### Reference images (Roblox official docs, CC-BY-4.0, pinned to commit `9f840b1`)
These come from the Roblox Creator Docs repo (licence CC-BY-4.0, © Roblox). They show the good and bad icon patterns that the
platform itself recommends.

| Good | Bad |
|---|---|
| ![Icon expresses theme park](https://raw.githubusercontent.com/Roblox/creator-docs/9f840b170b3e472c705e035126b45e3e050daed2/content/en-us/assets/publishing/experience-metadata/Icon-Theme-Park.jpg) Clear theme | ![Ambiguous symbol](https://raw.githubusercontent.com/Roblox/creator-docs/9f840b170b3e472c705e035126b45e3e050daed2/content/en-us/assets/publishing/experience-metadata/Icon-Theme-Park-Symbol.jpg) Ambiguous corner graphic |
| ![High res](https://raw.githubusercontent.com/Roblox/creator-docs/9f840b170b3e472c705e035126b45e3e050daed2/content/en-us/assets/publishing/experience-metadata/Icon-High-Res.jpg) Sharp 512×512 | ![Low res](https://raw.githubusercontent.com/Roblox/creator-docs/9f840b170b3e472c705e035126b45e3e050daed2/content/en-us/assets/publishing/experience-metadata/Icon-Low-Res.jpg) Blurry |

Colour sets the mood: fantasy (bright), somber (muted), horror (heavy contrast).

![Bright](https://raw.githubusercontent.com/Roblox/creator-docs/9f840b170b3e472c705e035126b45e3e050daed2/content/en-us/assets/publishing/experience-metadata/Icon-Colorization-A.jpg)
![Muted](https://raw.githubusercontent.com/Roblox/creator-docs/9f840b170b3e472c705e035126b45e3e050daed2/content/en-us/assets/publishing/experience-metadata/Icon-Colorization-B.jpg)
![Horror](https://raw.githubusercontent.com/Roblox/creator-docs/9f840b170b3e472c705e035126b45e3e050daed2/content/en-us/assets/publishing/experience-metadata/Icon-Colorization-C.jpg)

Thumbnails: a clear action read versus an unclear one.

![Urban Rush good](https://raw.githubusercontent.com/Roblox/creator-docs/9f840b170b3e472c705e035126b45e3e050daed2/content/en-us/assets/publishing/experience-metadata/Thumbnail-Urban-Rush.jpg)
![Unclear bad](https://raw.githubusercontent.com/Roblox/creator-docs/9f840b170b3e472c705e035126b45e3e050daed2/content/en-us/assets/publishing/experience-metadata/Thumbnail-Unclear.jpg)

---

## How to read each entry
- **IDs.** `place` is the number in `roblox.com/games/<place>`. `universe` is needed by the thumbnails and games APIs. A universe ID
  marked * was recalled from memory, not confirmed in a source today (⚠️ verify with the universe API).
- **Resolve.** Paste `https://thumbnails.roblox.com/v1/games/icons?universeIds=<u>&size=512x512&format=Png` and
  `https://thumbnails.roblox.com/v1/games/multiget/thumbnails?universeIds=<u>&size=768x432&format=Png&countPerUniverse=3`
  into a browser. Each `imageUrl` that comes back is a `tr.rbxcdn.com/<hash>/…` CDN URL. The hash changes whenever the creator
  re-uploads and old hashes can expire, so re-resolve before relying on an embed.
- **Breakdown fields.** Composition, focal point, faces/emotion, colour, text, small-size readability, promise.

---

## 1. Steal An Egg: the platform #1 in Sept–Oct 2026
- Page: <https://www.roblox.com/games/107778070777162> · place `107778070777162` · universe `10563114921`
- Snapshot: created **2026-07-25**. All-time peak about **14.29M CCU** (Rolimons; RoVitals logged 14,272,591 on 2026-09-19). At least **6.37B visits**. Reported at about **1.4M CCU on 2026-10-02**. Developer: group "And Collect Rare Pets" ([Rolimons](https://www.rolimons.com/game/107778070777162), [RoVitals](https://rovitals.com/game/107778070777162), [Fandom](https://roblox.fandom.com/wiki/And_Collect_Rare_Pets/Steal_An_Egg)).
- Breakdown (⚠️ verify against the resolved icon):
  - **Promise:** grab an egg, outrun its guardian, hatch a rare pet. This combines the "Steal a…" heist verb with the egg-hatch gacha of pet simulators.
  - **Focal point:** expect one oversized, glowing egg as the hero object. The egg is the reward symbol, so it must read at 150 px.
  - **Emotion:** urgency, from a guardian chasing you or a character sprinting. Speed and treadmill progression are core ([TechWiser guide](https://techwiser.com/steal-an-egg-beginner-guide/)).
  - **Lesson:** name a verb from a proven trend plus a reward object that the genre already understands (the egg). The title alone explains the loop.

## 2. Steal a Brainrot
- Page: <https://www.roblox.com/games/109983668079237> · place `109983668079237` · universe `7709344486`
- Snapshot: created **2025-05-16** by BRAZILIAN SPYDER (SpyderSammy). Its all-time peak of **25,836,222 CCU on 2025-10-11** is the platform record. Visits are about **65.8B (RoWatcher)** or **73.8B (Rolimons)**; the trackers disagree. Current CCU is about 205K ([Rolimons](https://www.rolimons.com/game/109983668079237), [RoWatcher](https://rowatcher.com/games/7709344486/steal-a-brainrot), [PocketGamer.biz](https://www.pocketgamer.biz/robloxs-steal-a-brainrot-becomes-first-game-to-surpass-25m-concurrent-players/)).
- Breakdown:
  - **Focal point:** Italian-brainrot meme characters such as Tralalero Tralala (a blue shark with sneakers, blank stare) ([wiki](https://stealabrainrot.fandom.com/wiki/Tralalero_Tralala)). The characters are already famous on TikTok, so the icon trades on recognition, not art quality.
  - **Text:** the title carries a rotating emoji tag (`[🥚]`, etc.) that signals the current event.
  - **Colour:** bright, saturated, cartoon (⚠️ verify).
  - **Lesson:** **borrowed recognisability beats polish.** If your theme rides a meme, put the most recognisable meme character big and centred.

## 3. Grow a Garden
- Page: <https://www.roblox.com/games/126884695634066> · place `126884695634066` · universe `7436755782`
- Snapshot: created **2025-03-25**. Peak about **22.3M CCU on 2025-08-23** (an earlier record of 21.6M in June 2025 beat Fortnite's 15.3M). About **35.9B visits**. About 20–100K CCU in Sept 2026 ([Rolimons](https://www.rolimons.com/game/126884695634066), [RoWatcher](https://rowatcher.com/games/7436755782/grow-a-garden), [Fortune](https://fortune.com/2025/07/30/roblox-video-game-grow-a-garden-viral-summer-hit/)).
- Breakdown:
  - **Promise:** calm, cosy, a "switch off" game ([Fortune](https://fortune.com/2025/07/30/roblox-video-game-grow-a-garden-viral-summer-hit/)). Visuals are minimalist, Minecraft-like.
  - **Colour:** greens plus warm crop colours. Low threat, high friendliness.
  - **Text:** the title uses seasonal emoji (`🌶️`, `🍂`, `🐿️`) that change per update (Rolimons and RoMonitor titles differ on the same day).
  - **Lesson:** **a calm game still needs a bold icon.** Make the plant or crop huge and use one cartoon character at most.

## 4. Grow a Garden 2
- Place `97598239454123` ([Rolimons](https://www.rolimons.com/game/97598239454123)) · universe: resolve with the universe API.
- Snapshot: launched **2026-06-12**, developer Strawberreh Squad. Reached **432,856 CCU one hour after going public** and **1B visits by 2026-07-05**. Had 171.8K CCU on 2026-08-20 ([games.gg](https://games.gg/news/grow-a-garden-2-release-date/), [Studiokrew](https://studiokrew.com/blog/top-roblox-games-august-2026/)).
- **Lesson:** **a sequel icon re-uses the parent's colour palette and logotype** so returning players recognise it instantly. Verify how much it changed (⚠️ verify).

## 5. Animal Hospital (Anomaly)
- Page: <https://www.roblox.com/games/78515283254292> · place `78515283254292` · universe `10148749921`
- Snapshot: created **2026-05-10** by Animal Anomaly. Peak **about 1.27M CCU on 2026-07-10**. At least **2.38B visits**. 358.5K CCU on 2026-08-20 ([Rolimons](https://www.rolimons.com/game/78515283254292), [GosuGamers](https://www.gosugamers.net/entertainment/news/78741-animal-hospital-becomes-roblox-s-latest-horror-sensation-here-s-everything-you-need-to-know)).
- Breakdown:
  - **Promise:** "cute animal patient… or is it?" It is a spot-the-anomaly horror game in the style of *I'm On Observation Duty*. Tells include three eyes, human teeth, and eyes that follow you ([Destructoid guide](https://www.destructoid.com/animal-hospital-walkthrough-guide/)).
  - **Faces:** the face *is* the hook. Expect a close-up animal face with one wrong detail (⚠️ verify).
  - **Title tags** like `[UPD + x2]` advertise updates and boosts.
  - **Lesson:** **horror on Roblox sells "cute plus wrong," not gore.** One uncanny detail on a friendly face reads at small size and passes moderation.

## 6. Murder Mystery 2
- Page: <https://www.roblox.com/games/142823291> · place `142823291` · universe `66654135`
- Snapshot: created **2014** by Nikilis. Set a new all-time peak of **1,352,075 CCU on 2026-08-16**, 12 years after launch. Visits about 24.5B (RoWatcher) or 31B (Rolimons). Monthly revenue estimated at about $1.06M (RoWatcher, model confidence 0.58) ([Rolimons](https://www.rolimons.com/game/142823291), [RoWatcher](https://rowatcher.com/games/66654135/murder-mystery-2)).
- Breakdown:
  - **Promise:** the three roles (Innocent, Sheriff, Murderer) and the knife and gun skins that drive its trading economy ([MM2 guide](https://mm2guide.com/guides/beginner-guide/)).
  - **Focal point:** iconic weapon silhouettes. Knives and guns are cosmetic but they *are* the brand (⚠️ verify the current art).
  - **Lesson:** **for an old game, the icon shows the collectible, not the gameplay.** Players return for the items.

## 7. Brookhaven 🏡RP
- Page: <https://www.roblox.com/games/4924922222> · place `4924922222` · universe `1686885941`
- Snapshot: created **2020-04-21**. Acquired by Voldex **2025-02-04**. The most-visited game on Roblox at **80–88B visits**. About 300–490K CCU. Revenue estimated at about $2.3M/month ([RoWatcher](https://rowatcher.com/games/1686885941/brookhaven-rp), [Rolimons](https://www.rolimons.com/game/4924922222)).
- Breakdown:
  - **Text:** the house emoji 🏡 sits in the title itself.
  - **Promise:** "be whoever you want": houses, cars, a sunny suburb.
  - **Colour:** daylight blue sky and clean pastel houses (⚠️ verify).
  - **Lesson:** **roleplay icons sell a place to be, not a goal.** Show the aspirational home or vehicle with people in it.

## 8. Blox Fruits
- Page: <https://www.roblox.com/games/2753915549> · place `2753915549` · universe `994732206`
- Snapshot: created **2019-01-16** by Gamer Robot Inc. All-time peak **2,781,531 CCU on 2024-12-31**. About **64.8B visits**. About 250–420K CCU in Aug–Sept 2026 ([Rolimons](https://www.rolimons.com/game/2753915549), [Studiokrew](https://studiokrew.com/blog/top-roblox-games-august-2026/)).
- Breakdown:
  - **Promise:** anime power fantasy (One Piece–style devil fruits).
  - **Focal point:** a glowing fruit or ability effect plus a character mid-attack. VFX are the selling point (⚠️ verify).
  - **Lesson:** **for combat and RPG games, put the signature VFX in the icon.** Glow sells power.

## 9. 99 Nights in the Forest 🔦
- Page: <https://www.roblox.com/games/79546208627805> · place `79546208627805` · universe `7326934954`
- Snapshot: created **2025-03-04** by Grandma's Favourite Games. Peak about **14.2M CCU**. About **29.8B visits**. Winner of the 2025 Innovation Awards for Best Adventure and Best Horror. A film adaptation was announced in **April 2026** ([Rolimons](https://www.rolimons.com/game/79546208627805), [Variety](https://variety.com/2026/film/news/99-nights-in-the-forest-movie-20th-century-studios-1236720515/)).
- Breakdown:
  - **Colour:** dark forest blues and greens with **one warm light source** (campfire or flashlight 🔦; the flashlight emoji is in the title).
  - **Faces/emotion:** dread, from the Deer monster silhouette.
  - **Promise:** survive the night together; cosy and scary at once.
  - **Lesson:** **horror icons need one warm, high-contrast light in a dark frame.** It gives the eye a focal point at small size.

## 10. Adopt Me!
- Page: <https://www.roblox.com/games/920587237> · place `920587237` · universe `383310974`
- Snapshot: created **2017** by Uplift Games. About **44.9B visits**. All-time peak quoted as **1,884,171** (⚠️ verify; the date quoted, 2021-04-16, conflicts with older press reports of about 1.6M in 2020). Its 30-day peak was 1.34M in Sept 2026 ([Rolimons](https://www.rolimons.com/game/920587237)).
- Breakdown:
  - **Promise:** cute pets to raise and trade.
  - **Focal point:** big-eyed baby pets. The emotion is cuteness and affection.
  - **Text:** an event tag in the title (`[🏚️]`).
  - **Lesson:** **big eyes and a soft palette sell nurture loops.** The faces are the focal point.

## 11. RIVALS
- Page: <https://www.roblox.com/games/17625359962> · place `17625359962` · universe `6035872082`
- Snapshot: created **2024-05-26** by Nosniy Games. All-time peak **967,342 CCU on 2026-02-14**. About **18.5B visits** ([Rolimons](https://www.rolimons.com/game/17625359962)).
- **Lesson:** competitive FPS on Roblox uses clean, stylised weapons and bold team colours, not realism (⚠️ verify). **Readable silhouettes beat detail.**

## 12. Dress To Impress
- Page: <https://www.roblox.com/games/15101393044> · place `15101393044` · universe `5203828273`*
- Snapshot: released **2023-11-11**. All-time peak **1,743,147 CCU on 2024-12-14**. About **11.1B visits** ([Rolimons](https://www.rolimons.com/game/15101393044)).
- Breakdown:
  - **Promise:** a themed runway, voting, stars ([guide](https://pixeltwelve.com/articles/dress-to-impress-beginner-guide)).
  - **Focal point:** a posed, stylised model avatar. The emotion is confidence.
  - **Colour:** pink and lavender glamour.
  - **Text:** a ⭐ or seasonal tag in the title.
  - **Lesson:** **when the avatar is the product, show the avatar.** Use full-body or 3/4 framing, a hero pose and a fashion palette.

## 13. DOORS
- Page: <https://www.roblox.com/games/6516141723> · place `6516141723` · universe `2440500124`*
- Snapshot: released **2022-08-10** by LSPLASH. About **7.8B visits**. Recent peaks of about 227K (RoVitals, 2026-08-28) ([Rolimons](https://www.rolimons.com/game/6516141723), [RoVitals](https://rovitals.com/game/6516141723)).
- Breakdown:
  - **Focal point:** one entity close-up. Icons have featured **Seek** (originally) and **Dupe** (Hotel+ and current); an April Fools icon used Jeff ([DOORS Wiki](https://doors-game.fandom.com/wiki/DOORS)). Thumbnails rotate entities (Rush, Eyes, Seek, Groundskeeper…).
  - **Emotion:** an eye or face looking at the viewer is a gaze-capture trick.
  - **Lesson:** **give each entity, creature or boss its own icon, and swap it per update.** The roster becomes a content calendar for the icon.

## 14. The Strongest Battlegrounds
- Page: <https://www.roblox.com/games/10449761463> · place `10449761463` · universe `3808081382`
- Snapshot: created **2022-08-02** by Yielding Arts. All-time peak **1,395,324 CCU on 2024-12-22**. About **19.3B visits** ([Rolimons](https://www.rolimons.com/game/10449761463), [RoWatcher](https://rowatcher.com/games/3808081382/the-strongest-battlegrounds)).
- **Lesson:** anime-parody characters (One Punch Man–style archetypes) in an impact pose with radial speed lines and VFX (⚠️ verify). **The pose and impact frame is the thumbnail.**

## 15. Fisch
- Page: <https://www.roblox.com/games/16732694052> · place `16732694052` · universe `5750914919`*
- Snapshot: created **2024-03-13** by Fisching. About **4.97B visits**. Recent 30-day peak about 439K. The all-time peak quoted in search snippets (1,273,618 on 2025-10-18) is ⚠️ unverified and may be mis-attributed ([Rolimons](https://www.rolimons.com/game/16732694052)).
- Breakdown:
  - **Promise:** the catch reveal, a giant or rare fish.
  - **Colour:** ocean teal with a vivid fish.
  - **Text:** an event tag in the title (`[RACING]`, `[BUDLING]`).
  - **Lesson:** **show the jackpot outcome (the rare catch) at hero scale.**

## 16. Dead Rails
- Page: <https://www.roblox.com/games/116495829188952> · place `116495829188952` · universe `7018190066`*
- Snapshot: all-time peak **1,476,198 CCU on 2025-04-19**. About **6.59B visits**. About 15–30K CCU in Sept 2026, a viral spike that decayed ([Rolimons](https://www.rolimons.com/game/116495829188952)).
- **Lesson:** a train plus Wild West zombies in one frame (⚠️ verify). It shows that **a fresh setting mash-up can spike CCU, and the decay shows a hook is not retention** (see [[Retention-Metrics-D1-D7-D30]]).

## 17. Pet Simulator 99
- Page: <https://www.roblox.com/games/8737899170> · place `8737899170` · universe `3317771874`*
- Snapshot: by BIG Games. Visits quoted as about 2.65B (⚠️ verify; that looks low for PS99 and may be a single-place count). Title tags rotate per update (`⛏️ [MINE]`, `👆 [TAP HEROES]`) ([Rolimons](https://www.rolimons.com/game/8737899170)).
- **Lesson:** **a franchise number in the title plus the update emoji.** The icon is a pet mascot with sparkle and rarity glow.

## 18. Tower Defense Simulator
- Page: <https://www.roblox.com/games/3260590327> · place `3260590327` · universe `1176784616`*
- Snapshot: created **2019-06-05** by Paradoxum Games. About **4.99B visits**. Title tag `[🪓EXE REWORK]` ([Rolimons](https://www.rolimons.com/game/3260590327)).
- **Lesson:** **the title tag names the exact update** (a tower rework). Returning players learn what changed without opening the page.

## 19. Jailbreak
- Page: <https://www.roblox.com/games/606849621> · place `606849621` · universe `245662005`
- Snapshot: created **2017-01-06** by Badimo. About **8.06B visits** ([Rolimons](https://www.rolimons.com/game/606849621)).
- **Lesson:** the classic cop-versus-robber split composition (⚠️ verify). **Two opposed characters is the clearest way to signal PvP roles.**

## 20. "+1 Speed … Escape" wave (e.g. +1 Speed Keyboard Escape)
- Example place `85800076296380` ([Rolimons](https://www.rolimons.com/game/85800076296380)). ⚠️ verify that this is the SecretVerse Studio version Studiokrew ranked #3 at **358.0K CCU on 2026-08-20**. Dozens of clones exist: Slime, ASMR, Underwater, Brainrot ([Rolimons search](https://www.rolimons.com/game/96947338677734)).
- **Lesson:** **a trend template ("+1 Speed X Escape") is a title formula plus a near-identical icon formula.** Expect a huge "+1" or speed numeral as text. If you copy a trend, you must still own one distinct visual (theme, mascot) or you are invisible among the clones.

## 21. Anime Expeditions
- Place `84515722934860` ([Rolimons](https://www.rolimons.com/game/84515722934860)) · created 2025-04-28 · all-time peak **342,296** · about 795M visits.
- **Lesson:** anime tower defence keeps a `[🔥]`-style tag and a roster lineup composition (⚠️ verify).

---

## Cross-game patterns: actionable rules
1. **Verb plus object in the title, and the same object on the icon.** Steal + Egg, Grow + Garden, Steal + Brainrot, Dress + Impress. Before drawing, write the title as `<verb> a <object>`. If that sounds weak, the icon will be too.
2. **One hero subject at 50–70% of the frame, centred or on a third, with a clean background.** Test at 150×150 and at 64×64. If you can't name the subject in one second, simplify.
3. **Faces win when the face is the hook.** Use big cute eyes (Adopt Me), an uncanny face (Animal Hospital, DOORS) or a meme face (Brainrot). Otherwise show the reward object (egg, fish, fruit).
4. **Pick the palette by genre.** Simulator and tycoon: saturated, warm, high-key. Horror and survival: dark, low-key, one warm light. Fashion and RP: pastel or pink. Combat: dark background plus bright VFX.
5. **Keep text out of the icon** (the title is printed beside it). On thumbnails, use 1–3 words in the top half, heavy font, stroke or outline.
6. **Treat the title tag as an update banner.** Use `[🥚]`, `[UPD + x2]`, `[🪓EXE REWORK]`. Change it on *every* update, together with an icon variant. Top games do this weekly.
7. **Ship 3–5 thumbnails with personalisation on.** Make one per audience (cute, competitive, social, event). Keep losers active at low traffic, per the Roblox recommendation.
8. **Trend clones need one owned distinctive.** In a clone wave (+1 Speed, Steal a…), the winner has the most recognisable mascot or theme, not the best art.
9. **Old games show the collectible. New games show the verb.** Pick based on whether your audience is returning or new.
10. **No misleading art.** Video thumbnails must be authentic gameplay. No "50% off" or "Free UGC" text, and no voice-over ([Thumbnails doc](https://create.roblox.com/docs/production/publishing/thumbnails)).

## Checklist
- [ ] Resolve icons and thumbnails for all 21 entries with the script in [[Reference-Capture-Process]] and embed them here.
- [ ] Replace each `⚠️ verify` breakdown with an observed one.
- [ ] Confirm the universe IDs marked *.
- [ ] Re-snapshot the CCU and visits from the API (not trackers). Next refresh is due **2026-11-04**.

## Pitfalls
- Tracker numbers disagree (Steal a Brainrot visits: 65.8B vs 73.8B). Always cite which tracker and the date.
- `tr.rbxcdn.com` hashes rotate when creators update. A broken embed means re-resolve; it does not mean the game is gone.
- Do not download or commit game icons. They are the creators' copyright. Embed by URL only.

## Related
- [[Reference/_Index|Reference index]] · [[Thumbnails-And-Icons]] · [[Titles-Descriptions-And-Tags]] · [[Discovery-Algorithm]]
- [[Sponsored-Ads-And-Paid-Acquisition]] · [[Genre-Positioning]] · [[Reference-Capture-Process]] · [[Video-Breakdowns]]

## Sources
(All accessed 2026-10-04 via web search. Live pages were not fetchable from this environment.)
- Roblox Creator Docs: [Icons](https://create.roblox.com/docs/production/publishing/experience-icons), [Thumbnails](https://create.roblox.com/docs/production/publishing/thumbnails). Repo [Roblox/creator-docs](https://github.com/Roblox/creator-docs) @ `9f840b1` (images CC-BY-4.0).
- Rolimons game pages linked per entry. [RoWatcher](https://rowatcher.com/), [RoVitals](https://rovitals.com/), [Studiokrew Aug 2026 ranking](https://studiokrew.com/blog/top-roblox-games-august-2026/).
- [PocketGamer.biz: SAB 25M](https://www.pocketgamer.biz/robloxs-steal-a-brainrot-becomes-first-game-to-surpass-25m-concurrent-players/), [Fortune: Grow a Garden](https://fortune.com/2025/07/30/roblox-video-game-grow-a-garden-viral-summer-hit/), [GosuGamers: Animal Hospital](https://www.gosugamers.net/entertainment/news/78741-animal-hospital-becomes-roblox-s-latest-horror-sensation-here-s-everything-you-need-to-know).
- [DevForum: Thumbnail personalization announcements](https://devforum.roblox.com/t/live-now-personalize-your-thumbnails-to-attract-more-users/3257233).
