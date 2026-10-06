---
tags: [reference/captures, project/rubber-tower, visuals/ui]
status: draft
updated: 2026-10-05
confidence: medium
---
# Overhead title / nameplate references (manifest)

**What this is:** examples of player titles shown above heads in Roblox games, captured for the Rubber Tower title UI ([[Rubber-Tower-Title-UI]]).
- **Captured:** 2026-10-05.
- **Rights:** third-party images, kept local (gitignored, the vault repo is public). Study only, never game assets.

**Method:**
- DevForum images via their `devforum-uploads` S3 links.
- YouTube thumbnails via `i.ytimg.com/vi/<id>/maxresdefault.jpg` (falls back to `hqdefault`).

**Not useful (checked):**
- The game-page carousels of Pet Simulator 99, Bee Swarm Simulator, Blox Fruits, Grow a Garden and Islands (Roblox thumbnails API, 33 images, scratchpad only). They're marketing art with no overhead titles visible.
- Pet Simulator 99's VIP perk is a **chat** nametag, not an overhead one (fandom wiki).
- Bee Swarm shows usernames **over hives**, not over heads (fandom wiki).
- ⚠️ verify in game: neither was checked in a live server.

| File | Source | What it shows | What we take from it |
|---|---|---|---|
| (vault) `Projects/Fish a Monster/attachments/Ref Mossy Rocks and Curved Trees.png` | Holden's earlier capture (game not recorded) | "Shiny Spotter": rounded white/blue banner, round gold badge on the left, bold outlined text, player name underneath | **The base for style A:** badge on the left, rarity outline, bold stroked text, name below, compact (2 lines) |
| `devforum-DefaultOverheads-1.png`, `-2.png` | https://devforum.roblox.com/t/defaultoverheads-a-familiar-overhead-gui-system/2730927 | A Roblox-default-looking overhead name made as a GUI (rich text, gradients) | Its documented behaviour: **fade over the last 10% of the display distance**, **size steps by distance (1.0 under 20 studs, 0.75 to 50, 0.5 beyond)**, raycast occlusion. Our LOD plan builds on this |
| `devforum-GradientNametag.jpeg` | https://devforum.roblox.com/t/i-made-a-fun-little-gradient-nametag-module/1151099 | Rainbow gradient name + "level: 1" + "[TAG] name" + star: 3 stacked lines | UIGradient on text works for the rainbow tier. **Avoid:** 3+ lines and gradient on every line; too busy |
| `devforum-PlayerUI-overhead.png` | https://devforum.roblox.com/t/player-ui-overhead-title-username-display-name/1682758 | Crown + "CREATOR" + "LEVEL: 1000" + display name + name, with moving gradients | Moving gradients for the top tiers. **Avoid:** a 4-line stack is far too tall for a 16-player obby |
| `yt-CbHxNK0kG-o.jpg`, `yt-yNNkTpAqGKQ.jpg`, `yt-KtPfa6vWnEs.jpg` | YouTube "How to equip titles in Blox Fruits" videos (ids in the file names) | Blox Fruits: a Titles menu (list, Equip buttons, locked "???" rows, "Obtain N titles" goals); small title text near the name | **Titles menu pattern:** locked rows show the unlock goal, one Equip button each. ⚠️ verify the in-world look (thumbnails only) |
| `yt-khOWBIEeHDo.jpg` | YouTube "How to get a custom nametag title — Epic Minigames" | A huge gradient "Youtuber" title over a player | **Avoid:** oversized overhead text blocks the view; ours steps down with distance |
| `yt-CaPtqZo2xmk.jpg` | YouTube "TDS Pls Donate skins + nametag showcase" | Tower Defense Simulator nametags as event cosmetics | Nametag styles can be rewards themselves (a later idea; not proposed now) |
| `yt-YcMBM6bTgnU.jpg`, `yt-Y-uqUZp2GOg.jpg` | YouTube nametag tutorials (rainbow gradient nametag; custom nametag) | Name with a gradient title line underneath ("President") | UIGradient + UIStroke on TextLabels in a BillboardGui is the standard build |

## Related
[[Rubber-Tower-Title-UI]] · [[Rubber-Tower]] · [[UI-Polish-And-Juice]] · [[X-HUD-And-Menus-UI]] · [[UI-And-Gameplay-Reference]]
