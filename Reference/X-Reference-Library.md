---
tags: [reference/x, reference/ui, reference/vfx]
status: draft
updated: 2026-10-04
confidence: medium
---
# X (Twitter) Reference Library

306 high-engagement Roblox posts from X (UI, VFX, game feel, showcases), saved locally with full-res images, best-quality
videos (200 videos, 163 images, about 1.6 GB), 12-frame contact sheets, and the post text and like count. Collected 2026-10-04 by searching X while logged in
as Holden, sorted by likes. Started from Holden's example: DevionUI's Halloween shop (815 likes).

| Note | What's in it |
|---|---|
| [[X-Shop-And-Seasonal-UI]] | 48 posts: seasonal/event shops, shop and store layouts, starter packs, stud-style UI |
| [[X-HUD-And-Menus-UI]] | 42 posts: HUDs, daily rewards, battlepass, quests, results, map vote, inventory |
| [[X-Animated-UI-Lessons-And-Tools]] | 28 posts: animated UI and motion, designer lessons (mistakes, fonts, colour), UI tools and plugins |
| [[X-VFX-Reference]] | 52 posts: cosmetic and environmental VFX, auras, TD indicators, pickups, pets, combat (for contrast) |
| [[X-Hatching-And-Pet-Systems]] | 15 posts: Adopt Me's redesigned world hatch, rarity-escalating reveals, hatch battles, pet-system kits |
| [[X-Low-Poly-Builds-And-Maps]] | 23 posts: pastel low-poly lagoon, fantasy city hub, RPG builds, maps, 256px-texture proof, lobby showcases |
| [[X-Animation-Reference]] | 11 posts: animation packs, comedy timing, rigging tools |
| [[X-Fishing-And-Paper-References]] | 12 posts: Fisch's rise to #1, the 'every fishing game is the same' critique, open-source fishing minigame, paper style |
| [[X-Thumbnails-And-Icons]] | 25 posts: the anti-AI-thumbnail backlash (46k likes), human-made thumbnails for big games, event badges, jandel and 'Timmy' first-impression threads |
| [[X-Game-Feel-And-Showcases]] | 37 posts: game feel (FadedB_Fox / Scrapbook Saga), events, viral game reveals, tech demos, art, tools |

## TL;DR — patterns that repeat across the best posts
- **A seasonal shop is a re-skin, not a rebuild.** Keep the frame; swap the header icon (pumpkin breaking the frame), the
  section dividers (bats), the border motif (snow caps, candy cane, jungle leaves) and the currency (candy). Every Halloween
  shop here sells the same three things: a lucky block or chest with odds shown, bulk egg buttons, and two event boosts
  (luck, magnet). Examples: DevionUI, jackdoesui, absidev, FurixShahin.
- **The 2026 'Steal an Egg' shop anatomy** is one scrolling column: a FEATURED limited egg or box (countdown, 4–5 pets with %
  odds, quantity buttons such as 1/3/10/50) → PASSES (x2 Growth / x2 Money) → stat packs in tiers, each ending in an
  oversized **BEST VALUE** bundle. Sections are colour-coded (speed blue, cash purple), tags are HOT / POPULAR / NEW /
  LIMITED, and jump tabs sit down the right side (Bitohi2345, DevionUI, brickoUI).
- **Close the purchase loop loudly.** Show a processing state ('Processing…' → 'Purchase Complete!' + confetti → OWNED), then
  a full-screen thank-you with a huge number ('+340,431,002 SPEED'). Gacha reveals follow one recipe: hide the UI → fly the
  object to centre → shake → light rays → name + rarity + odds → '1 of 3' for batch opens.
- **The HUD size depends on genre.** Steal-an-Egg-style games strip the HUD to 1–3 buttons (one STORE pill with a '!' badge).
  The '+1 / simulator' genre (the closest neighbour to Paper Plane Toss) still expects a 2x3 icon grid on the left, an
  offers column on the right (limited-offer timer, 2x, auto-win), and a stat + level bar at bottom centre.
- **Juice comes from about five reusable tweens:** a spring press (squash to about 0.9, overshoot back), a hover shine sweep, odometer
  number rolls, NEW / '!' badges, and bobbing icons. Build them once as shared modules (see [[UI-Polish-And-Juice]]).
- **Put a Gift button next to Buy** (stud stores, cash packs, battlepass, Steal an Egg's 'Gift Player' picker), with a
  'Receive Gifts' toggle in settings.
- **AI thumbnails are a reputational risk.** The single most-liked post captured (46.5k) says players skip games with AI
  thumbnails; studios now advertise human-only art. Relevant to [[Paper Plane Toss Thumbnails and Game Icon]], whose candidates are AI-generated.
  This is sentiment on X, not CTR data. See [[X-Thumbnails-And-Icons]].
- **Strong, cute art direction gets shared most.** Scrapbook Saga's paper-craft game feel got 24k likes and Fisch's
  crescent-moon cosmetic boats got 11k; most UI showcases sit at 100–800. Paper-craft is directly on-theme for
  [[Paper Plane Toss]].

## Relevance to current projects (recommendations, not approvals)
- **Paper Plane Toss:** study FadedB_Fox's Scrapbook Saga posts for paper and scrapbook UI language (paper-strip toasts,
  folder and paper-clip menus, sewing-button currency), and mlaskaczz's '+1 something' HUD for what the genre expects on
  screen. Halloween falls inside the current window (today is 2026-10-04); the re-skin pattern above is the cheap version.
  Any event plan needs Holden's approval first.
- **Fish a Monster:** DKEaterrr's Fisch boat and jet-ski VFX and the 'Lovely Boats' cosmetic are the closest reference for
  cosmetic boats and rods.

## Policy and ethics flags spotted in references
- ⚠️ verify: Biscuit_Designs' codes board asks players to follow an X account for rewards, and reliskdev's popup asks them
  to 'join the group + like the game'. Rules on social-follow rewards are an open item in [[Gap-Tracker]]; copy the toast
  feedback, not the gate.
- reliskdev's purchase one-liners ('Leaving empty handed? Brave.') are guilt copy. Don't use them for a young-teen
  audience; see [[Monetisation-Mistakes]] and [[Pay-To-Win-Boundaries]].
- Designer claims such as 'increases conversion by 5x' or 'high PCR' are marketing, not data. Likes measure reach among
  devs, not player conversion.

## Designers worth following (by what they're good for)
| Area | Accounts |
|---|---|
| Simulator / stud shops | DevionUI, jackdoesui, Bitohi2345 (Steal An Egg), brickoUI, ProjectLarryUI, Livvyjuju |
| Anime / premium UI | Zac1kio (Anime Rivals), unouiux, AltroUIUX, acturko_, oreuiz |
| UI lessons and juice | captideRBLX (mistakes, fonts, buttons), dearpureoni, mashdee_, httptotem |
| Icons and colour | RhosGFX (colour-ramp rule in [[X-Game-Feel-And-Showcases]]) |
| Game feel | FadedB_Fox (Scrapbook Saga) |
| VFX | DKEaterrr (Fisch), BardVfx_x (pickups, pets), RGUYW / justhazu (TD indicators), leollopesss (Forsaken) |

## How this was collected (repeatable)
1. **Search X while logged in** (Browser pane) using advanced operators, Latest tab:
   `#RobloxUI min_faves:100`, `#RobloxVFX min_faves:200`, `#RobloxDev min_faves:2000 -filter:replies`, `roblox thumbnail min_faves:300`, `roblox hatch min_faves:150`, `roblox "low poly" min_faves:100`,
   `#RobloxAnimation min_faves:300`, `roblox fishing min_faves:200`.
   A small JS collector scrolls the timeline and records post id, author, date, likes and media type from the page.
   Gotchas: X only loads more posts while the pane is being drawn (take periodic screenshots if the pane is hidden),
   and search rate-limits after about 5 heavy queries ('Something went wrong. Try reloading.'); wait about 15+ minutes.
2. **Curate:** skip website parodies, drama posts, UGC and fan-animation spam; keep posts relevant to young-teen simulator,
   tycoon, obby and +1 games.
3. **Fetch** with `Assets/Reference-Captures/X/fetch_x.py <list.txt>` (lines: `url category note`). It uses X's public
   embed endpoint (`cdn.syndication.twimg.com/tweet-result`), so no login or API key is needed; it saves `post.json`, images
   (`?name=orig`) and the highest-bitrate MP4 into `X/<category>/<author>-<id>/` and appends to `manifest.json`.
   Already-fetched ids are skipped.
4. **Contact sheets:** `blender -b --factory-startup --python contact_sheets.py` (12 evenly spaced frames per video; no
   ffmpeg on this PC, see [[Video Frame Extraction with Blender]]). `review_grids.py` builds 12-up review pages in `X/_review/`.
5. **Write takeaways** into `takeaways.json` (keyed by post id; 'Viewed' means the frames were actually looked at), then
   run `build_notes.py`. It rewrites only the `<!-- catalogue -->` block in each X-* note.

**Storage and rights:** the vault's GitHub mirror is public, so all X media (`*.jpg/png/mp4`, `post.json`) is gitignored and
stays on this PC. Only notes, the manifest, takeaways and scripts are tracked. This is third-party art for private study:
don't upload, trace or resell it. Credit the author if a design is closely followed.

## Next queries
All queued queries ran on 2026-10-04 (hatch, low poly, lobby/map, #RobloxAnimation, paper, fishing). Next: a Christmas pass
in late November, `blender roblox` model breakdowns, and a monthly re-run of `#RobloxUI min_faves:100` for new shop and HUD trends.

## Pitfalls
- Like counts are a snapshot from 2026-10-04 and are inflated for designer-network accounts. Use them to rank, not as
  evidence of player response.
- Several 'UI' posts are mockups running on an empty baseplate. They show visual polish, not proven in-game usability on
  a phone.
- The embed endpoint returns `TweetTombstone` for deleted or protected posts. One of the seeded posts was already gone.

## Related
[[Reference/_Index|Reference index]] · [[UI-And-Gameplay-Reference]] · [[Community-Showcase-Breakdowns]] · [[UI-Polish-And-Juice]] ·
[[UI-Layout-And-Device-Scaling]] · [[VFX-Particles-Beams-Trails]] · [[Art-Direction]] · [[Events-And-Seasons]] ·
[[Bundles-And-Starter-Packs]] · [[Daily-Rewards-And-Streaks]] · [[Paper Plane Toss]] · [[Fish a Monster]]

## Sources
- X advanced search (logged in), queries listed above, run 2026-10-04. Per-post links are in each catalogue note and in
  `Assets/Reference-Captures/X/manifest.json`.
- Seed posts found via web search (`site:x.com` queries) on 2026-10-04.
- X embed endpoint used by `fetch_x.py`: `https://cdn.syndication.twimg.com/tweet-result?id=<id>&token=<t>`
  (undocumented; ⚠️ verify it still works before each refresh).
