---
tags: [reference/video, reference/youtube]
status: draft
updated: 2026-10-04
confidence: medium
---
# YouTube Reference Library (2026-10-04 pass)

26 new YouTube videos found by searching YouTube in the logged-in browser (6 queries) and **deduplicated** against the 23
videos already in [[Video-Breakdowns]] (one search hit was already there and was skipped). Metadata (channel, length,
date, views) comes from YouTube's own video data; points marked with a timestamp come from the video's captions (read, not
watched). Local thumbnails are in `Assets/Reference-Captures/YouTube/` (gitignored). Part of the [[X-Reference-Library]]
family; X posts by the same creators are not repeated here.

## TL;DR — only what the vault didn't already have
- **'Change 20% of a proven game' (Tizzy RBLX).** Map hit games on one board (rows: fantasy, unique mechanic, core loop, RNG
  timing, level design, progression, long-term collection). Steal an Egg, Escape Tsunami, Ride a Pet, Dig and Clean and
  Surf and Rescue share the loop 'leave base → get a thing → bring it back', differing in a few cells (e.g. the RNG roll
  happens *after* bringing it home in Steal an Egg versus a visible spawn table in Steal a Brainrot). Pick a reference
  game and innovate in the cells that matter (14:20). Pairs with [[Genre-Playbooks]] and [[Core-Loops]].
- **Explain it in one sentence, or the thumbnail won't (AlvinBlox).** 'Could they understand the game if it was set to
  Chinese?' (2:28); simple, physical fun (a slap game) hooks before players realise (3:41).
- **Don't fix a weak game with ads (AlvinBlox).** Ad traffic disappears the moment spend stops if the loop doesn't hold
  (3:42); go idea → MVP → feedback → update fast (9:46). janisjanis01 adds a test: stop the ad and see if players stay (7:51).
- **The quiet phase is the real filter (waveshine, 510k views).** Your first games get no players (0:53); feedback and
  momentum arrive with just a few CCU (3:50–4:49); motivation dips mid-success (5:51). Expectations-setting more than technique.
- **Studio structure that scales (Leif, 257k views):** service modules split client/server/shared with explicit names,
  one startup script per side, a top-level UI module in ReplicatedStorage with folders per interface type, and a Signal
  package instead of BindableEvents. Compare with [[Systems/_Index|Systems]] architecture notes before adopting.
- **UI craft from Figma to Studio:** depth comes from a darker 'base' shape under the button flattened with a black outside
  stroke, blend-mode texture, edge highlight and drop shadow; structure is top bar → content → green price buttons with a
  Robux icon (Develuper 0:45–5:47). In Studio: stud texture via ImageLabel, align panel edges to whole studs, ZIndex layers,
  UIGradient on headers (Kingkade 3D). Kek's 3.5-hour importing masterclass: **don't export text**, keep images under
  1024 px, use a device emulator, and know ScreenGui vs BillboardGui vs SurfaceGui (chapters below).
- **AI-built games are now a YouTube genre** (Cole's 'GPT 6 Astra' Rocket League remake, 299k views; SmartyRBX's 'build
  with AI in 2026', 182k), alongside a backlash genre ('I made a viral game *without* AI', Duckable, 486k). The same split
  as the AI-thumbnail debate in [[X-Thumbnails-And-Icons]]. 'GPT-6 Astra' is described as OpenAI's newest model in Cole's video
  (2026-09-16); ⚠️ creator claim, still to verify officially.

## Catalogue

### UI design and building
| Video | Channel · length · date · views | Notes and timestamps |
|---|---|---|
| [Make Your Roblox UI Look 10x Better](https://www.youtube.com/watch?v=F6AtQKo3uIY) | Develuper · 7 min · 2026-08-21 · 107k | 0:16 main problem · 0:40 Figma tutorial (depth base shape 1:29, flatten + outside stroke 2:12, SVG icons 2:57, blend modes + edge highlight 3:40) · 5:03 frame structure, green = money, add Robux icons · 6:03 export/import |
| [The Ultimate Beginner's Guide to Roblox GUI](https://www.youtube.com/watch?v=lmNWskz9cEI) | Kek · 18 min · 2025-12-22 · 123k | 0:59 designing in Studio · 9:25 free UI resource pack · 10:30 Photoshop · 11:40 importing |
| [The Greatest Cartoony UI Tutorial (w/ Figma)](https://www.youtube.com/watch?v=z16zs2v-FNI) | Kek · 42 min · 2026-02-25 · 75k | 0:37 main frame · 5:30 search bar · **8:47 pet frames** · 19:32 main buttons · 29:03 close button · 31:27 header |
| [Roblox UI Importing Masterclass](https://www.youtube.com/watch?v=_6v86vc-9Xc) | Kek · 3 h 33 min · 2026-01-27 · 64k | 3:13 PNG vs JPG · **4:14 don't export text** · 5:40 keep images < 1024 px · 12:18 exporting from Figma · 22:11 device emulator · 23:27 uploading images · 26:23 ScreenGui · 28:28 BillboardGui · 30:31 SurfaceGui · 32:26 hierarchy · 33:17+ each GUI object |
| [How To Improve Your UI In Roblox Studio](https://www.youtube.com/watch?v=RPqIm0I_gsw) | Kingkade 3D · 12 min · 2026-05-27 · 39k | 1:02 stud texture ImageLabel · 2:03 end panels on whole studs · 3:05 ZIndex · 4:07 UIGradient header · 5:10 shadow colour · 7:16 TextScaled |
| [How to make Clean HUD Buttons on Figma](https://www.youtube.com/watch?v=Pq5SDrDsAq8) | RoXplode · 13 min · 2026-02-25 · 14k | 0:03 base · 1:49 corner stripes · 4:05 corner stars · 5:23 glossy glare · 7:49 dot texture · 9:55 icon + label (no captions available) |
| [How to make Animated Opening Shop Gui](https://www.youtube.com/watch?v=u404sKevMPU) | Rileybytes · 9 min · 2024-08-21 · 125k | 0:10 building the GUI · 3:48 scripting the open animation · 8:22 result |
| [How to make a Gamepass Shop (2026)](https://www.youtube.com/watch?v=sJhmHp9PK38) | Cheese Dev · 9 min · 2025-08-19 · 35k | 4:04 close button · 4:35 open-shop script · 5:12 gamepass setup · 6:42 gamepass scripts (⚠️ check purchase code against [[ProcessReceipt-Handling]] before copying) |

### Game design and growth
| Video | Channel · length · date · views | Notes and timestamps |
|---|---|---|
| [Roblox Game Design Explained Like You're 5](https://www.youtube.com/watch?v=CRCcsYEB_6A) | Tizzy RBLX · 18 min · 2026-09-23 · 44k | 1:17 foundation = fantasy + unique mechanic · 2:35 core loop 'leave base, get thing' · 5:12 Steal an Egg breakdown (get faster, get pets) · 6:30 roll *after* acquisition · 9:06 Steal a Brainrot: visible spawn table, no roll · 11:43 Surf and Rescue = same mechanics underneath · **14:20 pick a reference game, change 20%** · 16:55 what the video leaves out (first-5-minute progression, mutations) |
| [How To Make A Popular Roblox Game](https://www.youtube.com/watch?v=Le4QhC3dDGk) | AlvinBlox · 11 min · 2025-04-28 · 465k | 1:13 don't make a 10-minute game (an obby with no reason to return) · 2:28 build what you'd play · 3:42 can't fix a weak game with marketing · 7:21 make buying feel good · 8:34 innovate, but not beyond understanding · 9:46 fast MVP → feedback · 11:00 'reason to come back tomorrow?' |
| [Here's Why Roblox Games Blow Up](https://www.youtube.com/watch?v=Y93DRfB-Deo) | AlvinBlox · 11 min · 2025-06-07 · 271k | 1:15 one-sentence pitch · 2:28 understandable with no text · 3:41 stupidly simple fun · 4:54 accessible to all ages and play times · 7:22 limited-time content and FOMO (⚠️ see FOMO ethics in [[Events-And-Seasons]]) · 8:36 build IP players think about at school · 9:48 partner with devs to fund ads |
| [Avoid These 5 Roblox Dev Mistakes](https://www.youtube.com/watch?v=f63stwpsaXw) | AlvinBlox · 9 min · 2025-04-04 · 175k | 1:13 title + thumbnail: minimal words, explain simply · 2:25 start a community (Discord/group) first · 3:37 cheap TikTok/Shorts creators to springboard · 4:50 listen to players · 6:04 too complicated = new players leave · 7:19 giving up too soon |
| [Watch this before making ROBLOX Games](https://www.youtube.com/watch?v=xnlaYLnCtFc) | waveshine · 10 min · 2025-08-04 · 510k | 0:53 nobody plays your first games · 2:18 first results · 3:50 feedback is fuel · 4:49 momentum · 5:51 setbacks · 7:25 breaking through |
| [Before You Make Your Roblox Game, Study THIS First](https://www.youtube.com/watch?v=N2FND74tgGE) | SmartyRBX · 6 min · 2025-04-06 · 86k | player psychology: status flex (pets, skins, stats, 2:10), loss aversion (3:13), mastery (3:13); **4:18 lurk in popular games and watch what players click and ignore** |
| [The Secret To Making Your Roblox Game FUN!](https://www.youtube.com/watch?v=gc7K98RlOik) | SmartyRBX · 3 min · 2023-06-09 · 56k | short; overlaps with the above |
| [How I Made a Viral Roblox Game](https://www.youtube.com/watch?v=fjlOaEALWmg) | janisjanis01 · 13 min · 2026-08-02 · 125k | 1:17 the idea matters most, don't reinvent · 2:36 simple loop (fight, earn, upgrade) · 6:33 one viral TikTok beat weeks of ads · **7:51 stop the ad and see if players stay** · 9:08 don't disappear after first success · 10:25 make update day an event · 11:45 dips are normal (promotes an AI UI tool at 3:55) |
| [How to ACTUALLY get Players in 2026](https://www.youtube.com/watch?v=cfLbW2j2VLs) | DitchyDevelopments · 4 min · 2026-06-18 · 21k | 1:18 test in dev feedback Discords · 2:36 make the *dev journey* the content so Shorts work even if viewers don't care about the game |
| [I Made a VIRAL Roblox Game Without AI](https://www.youtube.com/watch?v=Cc7HT3uNjeQ) | Duckable · 23 min · 2026-08-04 · 486k | tycoon build without AI; 12:57 random rare-dropper crates for tycoons; 19:27 queue system with attachments; 'monetisation bombardment' near the end (18:10) |
| [How I Spent 700 DAYS making a Roblox game (The Movie)](https://www.youtube.com/watch?v=1fXK4BM_bAE) | mini · 73 min · 2026-10-03 · 32k | devlog compilation: 0:27, 8:13, 18:53, 35:06, 51:55 (not summarised yet) |
| [I Spent 24 Hours With Roblox Millionaires](https://www.youtube.com/watch?v=8xgnm6SynH4) | Starter Story · 21 min · 2025-04-23 · 4.3M | 4:05 how Roblox works · 9:15 / 13:28 / 14:35 three developers' business breakdowns · 12:32 what it takes to reach the top · 18:10 day in the life (⚠️ revenue claims are self-reported) |

### Systems: eggs, pets, project structure
| Video | Channel · length · date · views | Notes and timestamps |
|---|---|---|
| [How To Make An EGG HATCHING SYSTEM](https://www.youtube.com/watch?v=wip3VN-LUA0) | AlvinBlox · 45 min · 2020-05-29 · 502k | classic full tutorial; 6 years old, so check APIs against current docs |
| [Advanced Egg Hatching System, mini-project devlog](https://www.youtube.com/watch?v=re1GEA_0xDc) | Stewiepfing · 14 min · 2025-06-08 · 12k | 1:20 auto-hatch usually unlocked by joining a group · **2:15 rarity gradients on text** · 4:20 text on models · 6:05 inventory with ProfileService and a unique ID per hatched pet (12:31) · 12:51 optimisation |
| [The ONLY Pet Display System You'll Ever Need](https://www.youtube.com/watch?v=ErTOTGmAjNA) | Stewiepfing · 21 min · 2026-02-15 · 10k | 1:34 single-pet display · 3:27 grid display · 12:40 PetDisplay module |
| [How PRO Devs Set Up Roblox Games](https://www.youtube.com/watch?v=F3ASTJuO82A) | Leif · 11 min · 2025-08-29 · 257k | 1:13 service modules per feature · 2:27 explicit singleton names · 3:39 client startup · 4:52 Wally packages · 6:05 server validation with cooldown · **8:31 top-level UI module with folders per interface type** · 9:43 core packages (Signal) |

### AI workflow
| Video | Channel · length · date · views | Notes and timestamps |
|---|---|---|
| [GPT 6 Astra + Roblox Studio is Insane](https://www.youtube.com/watch?v=jld-8pFWj6M) | Cole · 9 min · 2026-09-16 · 299k | 0:25 Studio setup · 0:53 connecting 'Higgsfield' · 1:19 first result · 2:54 car physics · 4:48 wall rides, 3v3 · 6:57 thumbnail and publishing · 7:33 ranked mode, leaderboards |
| [How to Build Roblox Games With AI in 2026](https://www.youtube.com/watch?v=0ENeVVC9QT0) | SmartyRBX · 18 min · 2026-03-30 · 182k | overview; compare with [[Video-SyphoDev-Claude-Code-Roblox-Workflow]] |
| [Which AI Can Make the BEST Steal a Brainrot GAME?](https://www.youtube.com/watch?v=uzOyfbTUyFk) | RoDev · 17 min · 2026-03-14 · 285k | one fixed clone prompt across 5 models, 2 corrections each; Claude won with no corrections; lesson: put features in the first prompt (transcript read; [[Community-Prompt-Examples]] §2, §4) |
| [I Asked Opus 5.5 To Make My DREAM Game!](https://www.youtube.com/watch?v=IFtKCN8jw6o) | Scuppy · 16 min · 2026-10-03 · 19k | long design prompt, no references, extra-high effort, mid-run ideas; genre clarified late caused rework; 68% weekly usage in 90 min; one-line thumbnail ask failed (transcript read; [[Community-Prompt-Examples]] §6) |

## Duplicates and gaps found
- Video-Breakdowns #9 and #10 are the same talk (identical transcripts); merged there.
- Video-Breakdowns #17 (`LGVajPx6QNc`) is unavailable.
- TikTok search requires a login, so it was skipped (no TikTok sign-in in the Browser pane). Most Roblox dev TikToks found
  by web search are cross-posts by creators already captured from X.

## Pitfalls
- 'How to go viral' videos are survivorship-biased; treat claims as hypotheses ([[Growth-Metrics-And-Benchmarks]]).
- Tutorial code from older videos (2020–2024) may use deprecated APIs; check [[Deprecated-API-Replacements]].

## Related
[[Video-Breakdowns]] · [[X-Reference-Library]] · [[Genre-Playbooks]] · [[Core-Loops]] · [[UI-Polish-And-Juice]] ·
[[Organic-Growth]] · [[AI-Assisted-Workflow]]

## Sources
YouTube video pages (metadata and captions read 2026-10-04); links in each table row.
