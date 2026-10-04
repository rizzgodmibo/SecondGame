---
tags: [project/paper-plane-toss, ui/shop, meta/ai-workflow]
status: reviewed
updated: 2026-10-04
confidence: medium
---
# Shop Gauntlet Workbench (trial run, 2026-10-04)

The log of the one-off [[Gauntlet-Loop]] trial on the Paper Plane Toss Robux shop, run under the limits in
[[Shop Gauntlet Loop Plan]]. **Holden published the shop (after the polish pass) on 2026-10-04**; the game code is committed in
SecondGame `19a3a10` ("Redesign the Robux shop and fix 9-slice borders on stored images").
One trial does not make this a standard workflow.

## TL;DR
- 4 rounds (r0 baseline + 3 builder rounds). Blind critic wins for ours: **r0 0/4 → r1 2/4 → r2 3/4 → r3 4/4**. Stopped at 4/4, inside the 4-round cap.
- Biggest single fix was not a layout change. **Studio served the painted kit images at most 1024 px on the long side**, so 9-slice rects written in source pixels cut off every panel's right and bottom border, game-wide. Fixed in `UIKit.storedSlice` (local observation, see Pitfalls).
- Prices, products, server code, odds display and PolicyService hiding were untouched. Every number on the new tags (SAVE %, per-egg, WORTH, +% PER R$) is computed from live prices and config, not typed in.
- New uploaded images: `tag_red` 77197077014216, `tag_gold` 96264698064651, `ribbon_green` 133838757920990 (rendered by `art/uikit/gen_shop.sh`).
- Holden still needs to review the art honestly. The critic was an AI picking between two pictures, not a playtest.

## Setup (how it ran)
- **Builder:** the lead session edited `src/client/UI/ShopPanel.luau`. Gates after every edit: StyLua, Selene (0 warnings), `rojo build`.
- **Pixels:** Studio MCP `screen_capture` in play mode at 1591×690 (phone-landscape aspect). Two temporary Studio-only scripts
  (`DevShopPreview.server/client.luau`) sent a display-only profile without passes/potions/starter pack and opened a tab.
  Both were **deleted** after the loop.
- **Critic:** a fresh general-purpose subagent per round, shown only `blind/rN/pairX-A/B` (ours vs a reference, sides shuffled,
  answers in a KEY file it was told not to open). It picked a winner per pair and listed concrete fixable problems.
- **Bar:** `ref-steal-an-egg` (Holden's style source) for Passes and Eggs, `ref-jack-halloween` for Boosts, `ref-devion-f5`
  for Tokens (all from [[X-Shop-And-Seasonal-UI]]; kept local only, gitignored).

## Rounds

| Round | Passes | Boosts | Eggs | Tokens | Main changes |
|---|---|---|---|---|---|
| r0 (baseline) | lost | lost | lost | lost | Original shop. |
| r1 | lost | lost | **won** | **won** | Centred panel, 950 px content width, odds tiles with pet art, green section ribbon, rays/bobbing icons, red/gold tags. |
| r2 | **won** (close) | lost | **won** | **won** | `storedSlice` border fix, VIP hero card + "3 PERKS IN 1", 5 vertical pass cards, starter pack hero with contents, tags repositioned. |
| r3 | **won** (high) | **won** (medium) | **won** (high) | **won** (high) | Starter: bigger contents, struck-through separate price + computed "SAVE 71%", odds moved under the button. Potions: time badge, rays, forced line break. Egg packs: quantity badge top-left on every pack (x1/x3/x10). Token coins larger. |

Screenshots (our own game, tracked): `attachments/shop-gauntlet/r0-*.jpg` … `r3-*.jpg`.

### Before / after
Passes: ![[r0-passes.jpg|420]] ![[r3-passes.jpg|420]]
Boosts: ![[r0-boosts.jpg|420]] ![[r3-boosts.jpg|420]]
Eggs: ![[r0-eggs.jpg|420]] ![[r3-eggs.jpg|420]]
Tokens: ![[r0-tokens.jpg|420]] ![[r3-tokens.jpg|420]]

## Polish pass after the loop (2026-10-04, Holden: "fix the weak spots, make the small text bigger")
Not a critic round: fixes for the round-3 notes, checked by screenshot (buy state and owned state).
- Small text up: card descriptions 19→22, pass descriptions 17→20 (wrap to two lines above the button), VIP sub-line 19→22,
  starter "Egg odds" 17→20, odds-tile rarity 17→20, ribbon side texts 19→22.
- Rays tinted to each card's tier colour (`RAY_TINT` + `tintedRays`); rays added behind the pass icons. They now show on the pastel cards.
- Starter contents sit on the kit's round `portrait` slot (existing image, no upload), so the dark egg reads on purple.
- Odds-tile pet art 92→106; token coins 140/170/200 (was 110/150/190).
- Token sticker now says "+47% MORE TOKENS" (same computed number; was "+47% PER R$").
- Still weak: pass icons are flat 2D renders (needs new Blender art, not done); potion cards are still near-identical.

Screenshots: `r4-passes.jpg`, `r4-passes-owned.jpg`, `r4-boosts.jpg`, `r4-eggs.jpg`, `r4-galaxy.jpg`, `r4-tokens.jpg`.
![[r4-boosts.jpg|420]] ![[r4-passes.jpg|420]]

## What the round-3 critic still disliked (fix list; most handled in the polish pass above)
- Small sub-text on phones: pass description lines, the VIP sub-line, "Egg odds: …", "R$ 99 per egg", "Packs grow as you level up!".
- Pass icons look flat next to the reference's 3D art.
- Potion cards are near-copies with empty middles; the rays barely show (white rays on pastel cards).
- Egg pet art is small inside the odds tiles.
- Token cards: empty top half; Pile of Tokens coin still small.
- "+47% PER R$" reads as jargon for young teens. The critic suggested "+47% BONUS". ⚠️ Holden decides wording; it is the same computed number.
- One critic claim was wrong: it said the x1 card had no badge, but the r3 screenshot shows "X1". Critics misread small details.

## Files changed (SecondGame, uncommitted)
- `src/client/UI/ShopPanel.luau`: shop layout rewrite (helpers `priceButton`, `buyCard`, `stackCard`, `heroCard`, `tag`, `ribbon`, `row`, `oddsTiles`, `trackPrice`).
- `src/client/UI/UIKit.luau`: `storedSlice` + `MAX_IMAGE = 1024`. **This changes every 9-slice panel in the game**, not just the shop. Other panels should be eyeballed once.
- `src/shared/UIAssets.luau`: Kit entries `tag_red`, `tag_gold`, `ribbon_green`.
- New: `art/uikit/gen_shop.sh`, `art/uikit/src/{tag_red,tag_gold,ribbon_green}.html`, `art/uikit/out/*.png`, `art/uikit/slices_shop.txt`.

## Lessons about the method
- **Blind A/B picks gave concrete, fixable notes**, not vague scores, which is the point of the loop. Rounds took roughly 20–40 min each.
- **Real pixels found the real bug.** The border cut-off looked like "content overflowing" until the screenshot made it obvious it hit every panel.
- Critics confuse details at screenshot size (the x1 badge). Check every claimed defect against the image before acting on it.
- A reference that is a concept mockup (Devion) or crowded (Jack's Halloween) is an easier bar to beat than a clean live game. Use a clean live shop as the bar when one is captured.
- Copies of reference images inside `blind/` must stay out of the public repo (see Pitfalls).

## Pitfalls
- ⚠️ verify: **uploaded UI images were served at max 1024 px on the long side** in this place (2026-10-04, via the Studio MCP `upload_image`). Kit slice rects in source pixels then point outside the stored image. Fix: scale the rect by `k = 1024 / max(w, h)` and set `SliceScale = 0.5 / k` for 2× renders. Roblox's June 2024 announcement says images up to 8k are now stored, and a DevForum bug report says the decal page still says 1024. Check which upload path gives full resolution before relying on either.
- Auto Throw (owned on the test account) can close the shop mid-capture. Check `SHOPPanel.Visible` before every screenshot.
- Captures taken while images are still loading show no plates; wait ~2.5 s after opening.
- `blind/r0` and `blind/r1` were included in local commit `b83e061` (not pushed on 2026-10-04) and contain copies of third-party reference shots. `blind/` is now gitignored and the pairs were untracked in the next commit, but they remain in `b83e061`'s history until that commit is rewritten before pushing.

## Related
[[Shop Gauntlet Loop Plan]] · [[Gauntlet-Loop]] · [[Paper Plane Toss]] · [[Paper Plane Toss UI Redesign]] · [[X-Shop-And-Seasonal-UI]] · [[UI-Polish-And-Juice]]

## Sources
- Local: SecondGame working tree (`ShopPanel.luau`, `UIKit.luau`, `UIAssets.luau`) and Studio play-mode captures, 2026-10-04.
- DevForum, "Warn user about resolution limits before uploading an image" (the search summary credits a June 2024 Roblox note about storing images above 1k; the original announcement was not opened): <https://devforum.roblox.com/t/warn-user-about-resolution-limits-before-uploading-an-image/2779568>
- DevForum, "Decal Upload Page Still Mentions 1024x1024 Limit Instead of 4096x4096": <https://devforum.roblox.com/t/decal-upload-page-still-mentions-1024x1024-limit-instead-of-4096x4096/4526770>
- DevForum, "GUI ImageLabel Pixels Limit": <https://devforum.roblox.com/t/gui-imagelabel-pixels-limit-ask/1731035>
