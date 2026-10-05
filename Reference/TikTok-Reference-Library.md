---
tags: [reference/tiktok, reference/video]
status: draft
updated: 2026-10-04
confidence: medium
---
# TikTok Reference Library (2026-10-04 pass)

26 Roblox-dev TikToks picked from 8 searches (logged in as Holden), out of about 190 results. Each is **deduplicated** against the
vault: [[X-Reference-Library]] (306 posts and their authors), [[YouTube-Reference-Library]] and [[Video-Breakdowns]].
I skipped Adopt Me hatch clips (already covered in [[X-Hatching-And-Pet-Systems]]), creators already saved from YouTube
(e.g. Paul1Rb), plain AI-tool ads and off-topic clips.
Stats (likes / plays / saves) come from TikTok's page data and the summaries from TikTok's own captions (read, not watched).
Thumbnails are in `Assets/Reference-Captures/TikTok/` (gitignored).

## TL;DR — what TikTok adds that the vault didn't have
- **Five things to remove from your game (jakeinatx, 9.6k likes):** a read-only 'how to play' wall of text (make the
  tutorial playable); a cinematic Play/Settings menu on join (extra friction unless you truly need save slots); **UI tweens
  longer than about 0.1–0.2 s** ('snappy, not cool'); and a tutorial that shows every feature at once (breadcrumb features
  so each unlock feels like a reward). ⚠️ community rule of thumb; check against [[UI-Polish-And-Juice]] durations.
- **Do's and don'ts (jakeinatx, 16k):** release small games fast to get data; play your own game a lot; don't spend hundreds
  of ad credits forcing the front page; **use funnels to see exactly when players leave the first session**; don't
  one-shot a whole game with AI; use Roblox Events to announce updates and lift D7. Matches [[Analytics-And-Instrumentation]].
- **Supdoggy (Final Swarm, 12k CCU claimed):** build one feature into a small game, then grow; don't do too much at once.
- **'Why your game gets no players' (whyitsjohnny):** no feedback on clicks (add sound and animation), no goal, no progression.
- **Get feedback, not defensiveness:** Blocks Mayhem (vice_dev, 13k) was told it looked too much like Rivals and restyled
  in a few hours. Reference games are fine, but players notice clones.
- **AI-assisted UI, done right (palm_dev):** don't let the AI 'make it look better' vaguely. Feed it screenshots of UI you
  like plus what you like about them, and iterate the design in a normal chat before building. Same direction as
  [[AI-Assisted-Workflow]].
- **UI craft not seen elsewhere:** spinning light rays behind a VIP icon with one local script (fishmopf, 18k likes, 13.6k
  saves); Figma layer-name tags (spin, gleam, fall) turned into tweens by a free plugin (phoxik.dev); a hand-drawn
  Procreate frame workflow (sketch → outline → clipped fill → shading and highlight layers; haizoops, 431k plays); a
  SurfaceGui prize wheel built from 8 equal quadrants (gfxcomet).
- **Engineering shorts:** zombie-horde pathfinding optimisation (letundev, 46k); Bezier curves for VFX paths (pr0_devv);
  Studio tips (Alt-select inside models, Ctrl mirror-scale; zzdocs 31k); builder plugins (Quick Stairs, Archimedes;
  dearwhimsi).
- **Two trend signals:** an AI 'vibe-coding' ad, 'Scripting manually is over' (lemonade.gg, 574k likes / 7.5M plays), is
  the most-viewed clip found. And **animated Roblox story shorts promoting a game** ('A pro gave this noob a Kitsune egg', Steal
  An Egg, 163k likes in a day) are a marketing format. Pairs with [[Influencer-Coverage]] and [[Organic-Growth]].

## Catalogue
| TikTok | Likes · plays · saves · date · length | Takeaway |
|---|---|---|
| [jakeinatx: 5 things to remove](https://www.tiktok.com/@jakeinatx/video/7671398345696431373) | 9.6k · 100k · 4.7k · 2026-08-07 · 77 s | wall-of-text tutorial, join cinematic menu, tweens > 0.2 s, all-features-at-once tutorial (see TL;DR) |
| [jakeinatx: do's and don'ts](https://www.tiktok.com/@jakeinatx/video/7672821361944939807) | 16k · 166k · 6.6k · 2026-08-11 · 29 s | ship fast, play your game, no ad brute-forcing, funnels, no AI one-shot, Events for D7 |
| [jakeinatx: Supdoggy advice](https://www.tiktok.com/@jakeinatx/video/7672254609963945230) | 43.6k · 593k · 8k · 2026-08-10 · 43 s | one feature → small game → grow (Final Swarm, 12k CCU, self-reported) |
| [whyitsjohnny: why no players](https://www.tiktok.com/@whyitsjohnny/video/7620205568451513614) | 3.2k · 70k · 1.2k · 2026-03-22 · 71 s | feedback on every click, a clear goal, progression |
| [vice_dev: fixing my biggest problem](https://www.tiktok.com/@vice_dev/video/7636480999240617238) | 13.2k · 315k · 3.6k · 2026-05-05 · 33 s | restyled after 'looks like Rivals' feedback |
| [palm_dev: AI UI that doesn't look bad](https://www.tiktok.com/@palm_dev/video/7684777669875027231) | 8.8k · 99k · 5.5k · 2026-09-12 · 60 s | reference screenshots + say what you like; design in chat first |
| [fishmopf.rodev: UI effects part 3](https://www.tiktok.com/@fishmopf.rodev/video/7676125691745783073) | 18.1k · 297k · 13.7k · 2026-08-20 · 47 s | spinning light rays behind icons, more effects |
| [phoxik.dev: no-code UI animation tags](https://www.tiktok.com/@phoxik.dev/video/7687380373663206678) | 4.8k · 64k · 3.9k · 2026-09-19 · 47 s | Figma tags spin / gleam / fall → tweens (free plugin; unvetted) |
| [haizoops: how I make my UI](https://www.tiktok.com/@haizoops/video/7390858001206234410) | 29.3k · 431k · 7.5k · 2024-07-12 · 153 s | Procreate: sketch, symmetry, clipped fills, add/multiply layers for gold shine and depth |
| [gfxcomet: samurai wheel UI](https://www.tiktok.com/@gfxcomet/video/7659648726075559198) | 7.1k · 99k · 3k · 2026-07-07 · 67 s | 8 equal quadrants on a SurfaceGui, particles |
| [devfenzo: Figma UI part 2](https://www.tiktok.com/@devfenzo/video/7688818757652778262) | 17.4k · 690k · 4.1k · 2026-09-23 · 59 s | translucent coin counter with gold border and a + button; base and shop teleports on top |
| [uhskit: UI showcase](https://www.tiktok.com/@uhskit/video/7544785569474202911) | 43.8k · 259k · 6.9k · 2025-08-31 · 16 s | concept UI showcase (no captions) |
| [loooni_sdm: inventory UI (no AI)](https://www.tiktok.com/@loooni_sdm/video/7677977187575778593) | 3k · 93k · 860 · 2026-08-25 · 21 s | 'no AI' is now a selling point |
| [solosdev: UI same on all devices](https://www.tiktok.com/@solosdev.official/video/7690908364758338838) | 1.7k · 26k · 1.2k · 2026-09-29 · 40 s | scaling tutorial (no captions); see [[UI-Layout-And-Device-Scaling]] |
| [flayodev: how big games make UI](https://www.tiktok.com/@flayodev/video/7646512631758605601) | 24.2k · 398k · 20k · 2026-06-01 · 20 s | **duplicate info**: recommends ui-resources.com, already in [[X-Animated-UI-Lessons-And-Tools]] |
| [letundev: pathfinding optimisation](https://www.tiktok.com/@letundev/video/7666292888753556756) | 46.3k · 406k · 11k · 2026-07-25 · 181 s | crowd zombies without lag; see [[Performance-And-Profiling]] |
| [netkadev: performance habits](https://www.tiktok.com/@netkadev/video/7673303202162363680) | 7k · 93k · 4.6k · 2026-08-13 · 21 s | on-screen tips (no captions) |
| [pr0_devv: Bezier curves for VFX](https://www.tiktok.com/@pr0_devv/video/7679364442194234646) | 10.8k · 97k · 5.1k · 2026-08-29 · 53 s | lerp → quadratic Bezier explained |
| [zzdocs: 5 Studio tips](https://www.tiktok.com/@zzdocs/video/7555276012947344662) | 30.7k · 451k · 19.2k · 2025-09-28 · 72 s | Alt-select in models, Ctrl mirror-scale, more |
| [dearwhimsi: building plugins](https://www.tiktok.com/@dearwhimsi/video/7635038819242347809) | 8k · 120k · 6.6k · 2026-05-01 · 80 s | Quick Stairs, Archimedes and more |
| [vfxloom: procedural flipbook plugin](https://www.tiktok.com/@vfxloom/video/7669434564153969942) | 6.4k · 85k · 3.8k · 2026-08-02 · 42 s | node-based flipbook texture editor inside Studio (unvetted) |
| [dev_forgestudio: building crazy VFX](https://www.tiktok.com/@dev_forgestudio/video/7591987449778179359) | 147.8k · 1.2M · 26.8k · 2026-01-05 · 12 s | short VFX showcase |
| [hamburtoons1: Steal An Egg story short](https://www.tiktok.com/@hamburtoons1/video/7692424296349617426) | 163k · 1.4M · 18k · 2026-10-03 · 59 s | animated noob/pro story promoting a game |
| [lemonade.gg: 'scripting manually is over'](https://www.tiktok.com/@www.lemonade.gg/video/7672698129032006934) | 574k · 7.5M · 76k · 2026-08-11 · 162 s | AI tool ad; prompts a stud tree that breaks, flashes and auto-loots (trend signal only) |
| [mmii665_: every game getting AI thumbnails](https://www.tiktok.com/@mmii665_/video/7675982434738932999) | 384 · 20k · 71 · 2026-08-21 · 8 s | same sentiment as [[X-Thumbnails-And-Icons]] (low reach) |
| [devmindofficial: growth site ad](https://www.tiktok.com/@devmindofficial/video/7633564458714959118) | 29.8k · 441k · 17.6k · 2026-04-27 · 14 s | ad for a growth-advice site; listed only because of reach (unvetted) |
| [andythropic: Claude scripting, not one prompt](https://www.tiktok.com/@andythropic/video/7632072838253530398) | 30.2k · 442k · 14.5k · 2026-04-23 · 118 s | one system at a time; say what it does, where, how players interact; on-screen refactor prompt ([[Community-Prompt-Examples]] §2–3) |
| [andythropic: how I vibe coded a game with Claude Code](https://www.tiktok.com/@andythropic/video/7638783229322939679) | 16.1k · 325k · 8k · 2026-05-11 · 154 s | Rojo + Claude Code; small specific tasks; paste the error plus what you clicked; 3 months of work, not a one-shot |
| [lolstudios33: Blender MCP model in 2 prompts](https://www.tiktok.com/@lolstudios33/video/7690308892881882381) | 3.7k · 75k · 2.7k · 2026-09-27 · 53 s | references from the old design; prompt written by another AI then hand-edited; "ask questions when unsure" ([[Community-Prompt-Examples]] §5) |

## Pitfalls
- Many high-reach Roblox-dev TikToks are ads for AI tools or paid services (ForgeGUI, Bloxsmith, ClickLab, Lemonade,
  devmind). Their numbers show reach, not quality.
- Likes and saves are a snapshot from 2026-10-04.

## Related
[[X-Reference-Library]] · [[YouTube-Reference-Library]] · [[Video-Breakdowns]] · [[UI-Polish-And-Juice]] ·
[[Onboarding-And-First-60-Seconds]] · [[Organic-Growth]] · [[AI-Assisted-Workflow]]

## Sources
TikTok video pages (stats and auto-captions read 2026-10-04); links in the table.
