---
tags: [project/paper-plane-toss, ui/shop, meta/ai-workflow]
status: draft
updated: 2026-10-04
confidence: medium
---
# Shop Gauntlet Loop Plan (not started)

A one-off trial of the [[Gauntlet-Loop]] method on the Robux shop. **Holden's answer on 2026-10-04: "Not yet."** Nothing has been
run and no code changed. He also said **new painted UI images are allowed** if the trial goes ahead. Trying the method once
does not make it a standard workflow.

## Target
`SecondGame/src/client/UI/ShopPanel.luau` (586 lines; tabs Passes / Boosts / Eggs / Galaxy / Tokens / Codes), built on
the UIKit painted-asset kit from [[Paper Plane Toss UI Redesign]]. The game is live, so nothing is published without
Holden.

## Bar (what the critic compares against, blind)
- Holden's original style source: `Ref Steal an Egg Shop UI.webp` ([[Paper Plane Toss Image Gallery]]).
- Captured shops in [[X-Shop-And-Seasonal-UI]]: DevionUI's Steal An Egg template (2098495013676298709), Bitohi2345's Steal
  An Egg shop (2101801910747443570), brickoUI's stud store (2095572341858172929).

## Loop
1. Pieces: header + tabs, pass cards, boosts + starter pack, egg packs + odds, token packs, purchase feedback.
2. Per piece and round, a builder subagent edits. Hard gates: `rojo build`, Selene, StyLua, and the UI checker at 4 screen sizes.
3. Studio screenshots at phone and PC size via the Studio MCP, with a Studio-only `DevShopPreview.client.luau` opening the shop
   on a fake profile (never committed).
4. A fresh critic subagent sees only two unlabeled images (ours vs reference), picks one and names the biggest gap.
5. Cap: max 4 rounds per piece, about 2–3 h total; then a before/after for Holden.
6. Progress page: `Shop Gauntlet Workbench.md` in this folder.

## Locked
Prices, products, passes, server systems (`Systems/Shop`, `Products`, `Purchase`), odds shown before buying, PolicyService
hiding of paid eggs, no commits (Holden commits), no publishing.

## New art (allowed)
Render with `art/uikit/gen.sh`, upload through the Studio MCP (`upload_image` via a local HTTP server, see SecondGame
CLAUDE.md), record ids and slice rects in `src/shared/UIAssets.luau`, and list every new asset id for Holden.

## Before starting
- Open the Paper Plane Toss place in Studio (on 2026-10-04 only "Place1" was open) and run `rojo serve`.
- Holden says go.

## Related
[[Paper Plane Toss]] · [[Paper Plane Toss UI Redesign]] · [[Gauntlet-Loop]] · [[X-Shop-And-Seasonal-UI]]
