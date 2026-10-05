---
tags: [reference/x, reference/ui, monetisation/shop]
status: draft
updated: 2026-10-04
confidence: medium
---
# X Reference: Shop and Seasonal UI

48 catalogued shop, store, starter-pack, seasonal and stud-style UI posts from X, plus one manually reviewed ice-shop supplement below. Catalogue order is by likes, not measured usability. Part of
[[X-Reference-Library]] (method, rights and storage are explained there). Media lives locally in
`Assets/Reference-Captures/X/`; video posts show a 12-frame contact sheet with a link to the MP4.
"**Take:** Viewed…" means the frames were actually reviewed; posts with no Take have only their caption.

## TL;DR
- **Seasonal = re-skin.** Same frame; swap the header icon (breaking the frame), divider icons, border motif and currency.
  Several captured Halloween mockups show a chest, quantity buttons and
  event boosts. These are observed motifs, not required mechanics. Use a timer only for a real, defined deadline.
- **2026 simulator shop order:** FEATURED limited egg/box (timer + pets with odds + quantity buttons) → PASSES (x2) → stat
  pack tiers → one oversized BEST VALUE bundle per section. Colour-code sections and add right-side jump tabs.
- **Several showcases put a Gift button beside Buy** (honey packs, cash packs, battlepass, Steal an Egg's 'Gift Player').
- **Feedback:** 'Processing…' → 'Purchase Complete!' + confetti → card flips to OWNED; a thank-you overlay with a huge
  number; booster cards float '+50% LUCK!'.
- **Reveal recipe:** hide UI → object to centre → shake → light rays → name + rarity + odds → '1 of N' for batches.
- **Stud style** (chunky outlines, stud texture, bright saturated fills) recurs in this curated sample; selection by likes is not a representative genre survey.

## Checklist for a new or seasonal shop (derived from these references; untested in Holden's games)
- [ ] Choose a layout appropriate to the actual offers; only show a countdown for a genuine deadline.
- [ ] If a random offer is approved, validate its actual outcome distribution and applicable disclosure requirements; never copy mockup percentages.
- [ ] Compute cost per item for every quantity tier; any discount or best-value claim must be true.
- [ ] Use offer tags only when accurate; justify any best-value claim with the actual quantities and prices.
- [ ] Add gifting controls only if gifting is implemented, authorized and tested; a reference icon is not an entitlement-delivery design.
- [ ] Processing state, success celebration, OWNED state; never a silent purchase.
- [ ] Seasonal skin = icon + border motif + currency swap on the existing frame.
- [ ] Test at phone width (most of these mockups are filmed on a PC baseplate).

## Review supplement — 2026-10-04

### DevionUI — Ice King shop practice image
[Original post](https://x.com/DevionUI/status/2084509518806077565), dated 2026-08-04. Original page and still image inspected in this pass; image saved at the resolution served by X, not claimed full resolution.
![[Assets/Reference-Captures/X/supplement-2026-10-04/devion-2084509518806077565-ice-shop.webp|600]]

**Observation:** cyan title bar, four equal cash cards in a 2×2 group, one tall pink character offer beside them, repeated green price buttons, purple gift buttons and snow accents at the frame corners. The large character card creates hierarchy without changing every card style.
**Useful pattern:** a featured card can span two standard rows; themed border pieces can sit outside a stable rectangular content area.
**Critique:** the cash cards repeat the same displayed amount and price. Treat this as practice composition, not calibrated bundle design. Small price and gift targets need a touch test; a PC screenshot does not establish mobile accessibility.

### Original Halloween reference — independent review
[DevionUI post](https://x.com/DevionUI/status/2104979132245479646), dated 2026-09-29. Two owner screenshots are preserved in the supplement folder. Existing full clip and contact sheet remain in `ui-seasonal/DevionUI-2104979132245479646/`; duplicate lower-resolution posters were not added.

**Observed:** pumpkin entry button; orange/brown panel against a blue-purple world; two-up pass cards and three-up currency cards; shop dimmed behind reward silhouettes with names/rarity below. A browser frame at 00:11 and the existing 12-frame sheet were inspected. This pass did not measure tween curves, animation timings or audio, and did not establish mobile performance.
**Critique:** long outlined italic labels and dense art compete at small size. Keep the framing and silhouette hierarchy; reduce secondary detail and test price readability. Preserve a close/skip path and prevent reveal decoration from swallowing input. Success animation must follow authoritative purchase/reward confirmation.

### Acceptance checks before adapting any showcase
- [ ] Separate visual observations, creator marketing claims and proposed implementation choices.
- [ ] Check phone-sized labels, touch targets, scrolling, controller focus and long/localized text in the actual implementation.
- [ ] Verify close/skip/re-entry while an animation runs and a reduced-motion alternative.
- [ ] Check pending, failed, cancelled, duplicate and successful purchase states; a celebratory prototype proves none of these.
- [ ] Verify displayed quantities, probabilities, timers and unit prices against real configuration. Jack's mockup shows 50+40+25+10+1 = 126%; its 5-pack is 50 per egg while its 10-pack is 100 per egg.

These are pending acceptance checks, not completed game tests. Style reference does not approve mechanics, paid randomness, pricing or purchases.

## Catalogue
<!-- catalogue:start -->
### Seasonal and event shops (5)

#### DevionUI — Halloween shop (the original reference post)
[post](https://x.com/DevionUI/status/2104979132245479646) · ♥ 816 · 2026-09-29 · [[Assets/Reference-Captures/X/ui-seasonal/DevionUI-2104979132245479646/vid-1.mp4|▶ video 1]]
![[Assets/Reference-Captures/X/ui-seasonal/DevionUI-2104979132245479646/sheet-1.jpg|480]]
> Looking for a ui designer for this upcoming halloween? contact me on dc @…
**Take:** Viewed (the reference post that started this library). Pixel-art Halloween shop opened from a pixel pumpkin 'SHOP' button on the left edge. Layout top to bottom: header bar (pumpkin icon, title, candy currency pill, close), a lucky-block row (block art + 5 pet portraits + egg-quantity buttons), a bat-icon divider labelled GAMEPASSES with two 2-up cards (X2 Upgrade, X2 Magnet), then a CANDY section with three 3-up currency packs. Motion: a pixel moon flies in and bounces over the header; buying the block plays a reveal (icons fly out, then pets burst in on glow rings with name and rarity, e.g. 'Pumpkin Crawler RARE'); the currency pill counts up. The frame is ordinary; the event is sold by re-skinning icons, dividers and currency.

#### jackdoesui — Halloween shop animated prototype
[post](https://x.com/jackdoesui/status/2104940273369514423) · ♥ 246 · 2026-09-29 · [[Assets/Reference-Captures/X/ui-seasonal/jackdoesui-2104940273369514423/vid-1.mp4|▶ video 1]]
![[Assets/Reference-Captures/X/ui-seasonal/jackdoesui-2104940273369514423/sheet-1.jpg|480]]
> Ended up animating it! Here's the prototype 👇 DM me if you need your…
**Take:** Viewed. Animated version of jackdoesui's Halloween shop: the chest card has a rotating sunburst behind it; buying hides the shop, the chest pops centre-screen with radial light rays and reveals 'Night Bat 1/25' (the odds shown on the reveal itself); buying a booster floats '+50% LUCK!' / 'MAGNET ON!' text over its card. Reveal = hide UI → centre object → rays → name + odds → return to the shop.

#### jackdoesui — practice Halloween shop
[post](https://x.com/jackdoesui/status/2104899811401212315) · ♥ 177 · 2026-09-29
![[Assets/Reference-Captures/X/ui-seasonal/jackdoesui-2104899811401212315/img-1.jpg|480]]
> ✦ Practice Halloween Shop UI &gt; thoughts? DM for commissions 👇 Discord: jackrblx
**Take:** Viewed. Pixel/voxel Halloween re-skin of a standard shop: themed title bar (pumpkin icon breaking the frame, spider hanging off the close button), one big LIMITED TIME chest row showing all 5 drop odds (50/40/25/10/1%) above 3 bulk buttons (1/5/10 eggs = 150/250/1k candy; unit costs are 150/50/100, so the middle tier is cheaper per egg than the largest), then two 2-up boost cards (+50% luck, candy magnet) priced in the event currency. Visual reference only: displayed odds sum to 126%, so these cannot be copied as one mutually exclusive outcome distribution. Pricing and percentages appear to be mockup data.

#### FurixShahin — summer event UI
[post](https://x.com/FurixShahin/status/2088297576097300736) · ♥ 155 · 2026-08-14
![[Assets/Reference-Captures/X/ui-seasonal/FurixShahin-2088297576097300736/img-1.jpg|480]]
> New Roblox UI Showcase 🔥 Summer event UI Open for commissions &amp; collaborations 📷
**Take:** Viewed (grid). Summer event shop: 'NEW SEASON' corner ribbon, a 'REFRESH IN 15M 52S' rotating-stock timer, LIMITED tags on two items, a mixed-size card grid (one wide hero item, smaller items, one tall card), page dots for multiple pages, and a jungle-leaf border breaking the frame.

#### absidev — christmas stud UI set
[post](https://x.com/absidev/status/1999874402394235137) · ♥ 10 · 2025-12-13 · 4 images
![[Assets/Reference-Captures/X/ui-seasonal/absidev-1999874402394235137/img-1.jpg|480]]
> Christmas Themed Stud UI Set 🎄❄️ Recently made for a client. thoughts?
**Take:** Viewed (grid). Christmas stud UI set: green stud header topped with snow drips, candy-cane striped borders, sections labelled FEATURED / IN GAME CURRENCY / REDEEM A CODE, NEW! tag. A seasonal skin = snow cap + striped border + colour swap on the same frame.

### Shops, stores and starter packs (30)

#### Zac1kio — shop UI gimmicks + animations (Anime Rivals)
[post](https://x.com/Zac1kio/status/1805840239199408229) · ♥ 539 · 2024-06-26 · [[Assets/Reference-Captures/X/ui-shop/Zac1kio-1805840239199408229/vid-1.mp4|▶ video 1]]
![[Assets/Reference-Captures/X/ui-shop/Zac1kio-1805840239199408229/sheet-1.jpg|480]]
> Rarely post my ui but trying out some cool gimmick's and animations :D Shop…
**Take:** Viewed. Anime Rivals shop (Zac1kio): a dark purple frame with an icon tab row and two currency pills (gems, coins); a 'DAILY SHOP' reset timer; tall crate cards colour-coded by tier (green, Ethereal cyan, Radiant orange, Celestial purple), each with a big 3D crate, a 399 price and a rank tag; unit cards with S/B grade letters; currency packs 1,000 / 10,000 / 100,000 rising in container size (coins → sack → crate); and a 'Support a Creator!' creator-code entry box at the bottom. Hovering lifts the card and adds a glow outline.

#### Bitohi2345 — Steal An Egg shop
[post](https://x.com/Bitohi2345/status/2101801910747443570) · ♥ 430 · 2026-09-20 · [[Assets/Reference-Captures/X/ui-shop/Bitohi2345-2101801910747443570/vid-1.mp4|▶ video 1]]
![[Assets/Reference-Captures/X/ui-shop/Bitohi2345-2101801910747443570/sheet-1.jpg|480]]
> Shop for @StealAnEggRblx Icons by goat @IAmAMSStudios
**Take:** Viewed (video). Steal An Egg shop: a green-header window with right-side jump tabs (Featured, Speed, Money, Samples); FEATURED has a NEW limited egg with a 02:05:09 timer and pets with odds; PASSES are tagged HOT; packs are tagged POPULAR / BEST VALUE. Buying shows a full-screen 'Thanks for your support!!' card with a chest and a huge '+340,431,002 SPEED' number plus a particle burst, and an 'x2!' sticker slaps onto the header. There's a 'Gift Player' picker (friends list with Select buttons). Big numbers + thank-you + gifting. Poster: Steal An Egg-style HUD: two stacked big buttons on the left (green Shop, cyan Index) plus a 'Slow Mode' toggle; three square icon buttons on the right (purple crystal, red egg, orange paw); currency bottom-left with a live multiplier '(x64)'; a countdown bottom-right with a character portrait ('In 1m 03s'). Very few buttons, all thumb-reachable.

#### Bitohi2345 — Steal An Egg UI
[post](https://x.com/Bitohi2345/status/2101789965612900527) · ♥ 369 · 2026-09-20 · [[Assets/Reference-Captures/X/ui-shop/Bitohi2345-2101789965612900527/vid-1.mp4|▶ video 1]]
![[Assets/Reference-Captures/X/ui-shop/Bitohi2345-2101789965612900527/sheet-1.jpg|480]]
> 😇👿 For @StealAnEggRblx
**Take:** Viewed. Steal An Egg 'Pick A Side!' server event: two tall team cards (gold Light Team angel vs red Dark Team demon, 'VS' between), the hovered card scales up and tints the whole background its colour, then Confirm. In the world a tug-of-war bar over the boss shows both teams' totals. A cheap, social, server-wide event: pick a side, contribute, watch the bar.

#### Pers_GFX — starter pack animated
[post](https://x.com/Pers_GFX/status/2006969237165011024) · ♥ 368 · 2026-01-02 · [[Assets/Reference-Captures/X/ui-shop/Pers_GFX-2006969237165011024/vid-1.mp4|▶ video 1]]
![[Assets/Reference-Captures/X/ui-shop/Pers_GFX-2006969237165011024/sheet-1.jpg|480]]
> Starter Pack I made a while ago that was never used. Fully made and…
**Take:** Viewed. 'Starter Pack!' of three exclusive skins (R$299 each) in glowing green cards with a gift button on each, plus 'BUY ALL! For a discount' at R$799 (cheaper than 3x299). A bundle priced below the sum is the classic starter-pack nudge.

#### ryzedevs — anime shop
[post](https://x.com/ryzedevs/status/1878074574249607596) · ♥ 267 · 2025-01-11
![[Assets/Reference-Captures/X/ui-shop/ryzedevs-1878074574249607596/img-1.jpg|480]]
> ⭐ Anime Shop UI 📷 Want to hire me? Discord: "ryzedevs" [ | |…
**Take:** Viewed (grid). Neon 'STORE!' gems section: five gem packs, the largest tagged '+10,000 EXTRA' and '20% OFF'.

#### jackdoesui — prototype shop
[post](https://x.com/jackdoesui/status/2079804927174738246) · ♥ 260 · 2026-07-22 · [[Assets/Reference-Captures/X/ui-shop/jackdoesui-2079804927174738246/vid-1.mp4|▶ video 1]]
![[Assets/Reference-Captures/X/ui-shop/jackdoesui-2079804927174738246/sheet-1.jpg|480]]
> Prototype Shop UI Commission me at discord: jackrblx
**Take:** Viewed (grid). 'Exclusive Shop' crate: Buy 1/3/10/100 crate prices, a '2x Server Luck' server-wide boost purchase, and a Gift button.

#### Scxiptifyz — brainrot stud GUI
[post](https://x.com/Scxiptifyz/status/2021003447546544224) · ♥ 249 · 2026-02-09 · 4 images
![[Assets/Reference-Captures/X/ui-shop/Scxiptifyz-2021003447546544224/img-1.jpg|480]]
> 🤯🥳 FREE STUD GUI! I Handcrafted this Brainrot Stud GUI, And it can be…
**Take:** Viewed (grid). Free brainrot stud GUI: Limited Pack with income-per-second labels on units ('23.8K/s'), a Limited Item card ('Earns 317 million offline', '20/999' stock). Scarcity via stock counters.

#### jackdoesui — limited shop, tween system, lucky box hatches
[post](https://x.com/jackdoesui/status/2046605530723127714) · ♥ 249 · 2026-04-21 · [[Assets/Reference-Captures/X/ui-shop/jackdoesui-2046605530723127714/vid-1.mp4|▶ video 1]]
![[Assets/Reference-Captures/X/ui-shop/jackdoesui-2046605530723127714/sheet-1.jpg|480]]
> Prototype Limited shop UI I built for fun Full tween system, lucky box hatches,…
**Take:** Viewed. 'Limited Shop' prototype with a full tween system: an Exclusive Lucky Box row (rainbow '?' cube, 4 units at 35%, 10/3/1-box prices, 10:15:15 countdown) above a Starter Pack with '40% OFF' and a struck-through old price. Opening a box dims the screen, flies the cube to centre, shakes it, and reveals units one at a time ('1 of 3' counter, RARE tag, light rays, name). Batch opens are shown one by one so each pull gets its own moment.

#### dearpureoni — shop + starter pack
[post](https://x.com/dearpureoni/status/1973789968909877629) · ♥ 221 · 2025-10-02 · [[Assets/Reference-Captures/X/ui-shop/dearpureoni-1973789968909877629/vid-1.mp4|▶ video 1]]
![[Assets/Reference-Captures/X/ui-shop/dearpureoni-1973789968909877629/sheet-1.jpg|480]]
> » Shop and Starter Pack UI
**Take:** Viewed. Dark red 'Duels Shop' for a fighting game: left category rail (Limited, Arena, Perks, Tags, Companions), item tiles with prices, a Purchase Item confirm dialog, Standard vs Premium crates (Premium tagged 50%), and a Starter Pack modal (contents, '30% off', R$ price). A competitive-game shop: dark, dense, confirm before every purchase.

#### DevionUI — Steal An Egg shop template with lucky box
[post](https://x.com/DevionUI/status/2098495013676298709) · ♥ 216 · 2026-09-11 · [[Assets/Reference-Captures/X/ui-shop/DevionUI-2098495013676298709/vid-1.mp4|▶ video 1]]
![[Assets/Reference-Captures/X/ui-shop/DevionUI-2098495013676298709/sheet-1.jpg|480]]
> Steal An Egg Shop UI Template for Sale Only 10 copies available. Includes a…
**Take:** Viewed. A Steal An Egg shop template (10 copies sold). The whole HUD is ONE yellow 'STORE' pill with a red '!' badge. The shop is one scroll: a ROYAL GOLD EGG banner (egg art, a winged pet breaking the frame, 4 pets with odds, a 12:12:12 timer, quantity buttons for 50/10/3/1 eggs), PASSES (X2 Growth, X2 Money, gold cards), SPEED (blue, 3x '+150K Speed' plus a '+1,000,000,000 Speed' bundle tagged BEST VALUE), and CASH (purple, same structure). Sections are colour-coded by what they boost; every section ends with one oversized 'best value' bundle.

#### Bitohi2345 — Steal An Egg UI 2
[post](https://x.com/Bitohi2345/status/2101810179754844448) · ♥ 181 · 2026-09-20 · [[Assets/Reference-Captures/X/ui-shop/Bitohi2345-2101810179754844448/vid-1.mp4|▶ video 1]]
![[Assets/Reference-Captures/X/ui-shop/Bitohi2345-2101810179754844448/sheet-1.jpg|480]]
> 🧑‍🔬for Steal An Egg
**Take:** Viewed. Event shop for Steal An Egg: a themed 'Dr Scramble's Experiments' frame (lab tubes and gears around the border) opened from a world NPC; a 3x2 grid of item cards; the frame shows an empty pixel-grid placeholder for a beat before items pop in one by one; a total-cost bar (100,000) and a purple 'Open Scramble' button. An event NPC gets its own branded frame, not the generic shop.

#### RealCresent — shop UI 4 images
[post](https://x.com/RealCresent/status/2084230205384610172) · ♥ 179 · 2026-08-03 · 4 images
![[Assets/Reference-Captures/X/ui-shop/RealCresent-2084230205384610172/img-1.jpg|480]]
> ✦ Shop UI &gt; Discord - realcresent | Open for work
**Take:** Viewed (grid). Dark premium 'Game Shop' with tabs (Bundles, Gamepasses, Currency, Boosts, Customization), two wide 'Polychrome' bundle banners with LIMITED TIME ONLY, a time-remaining line and a struck price, plus a note that purchases are permanent.

#### brickoUI — full store designed + animated with sound
[post](https://x.com/brickoUI/status/2055731297901826550) · ♥ 159 · 2026-05-16 · [[Assets/Reference-Captures/X/ui-shop/brickoUI-2055731297901826550/vid-1.mp4|▶ video 1]]
![[Assets/Reference-Captures/X/ui-shop/brickoUI-2055731297901826550/sheet-1.jpg|480]]
> 🔊 SOUND ON Designed AND Animated the full store UI for my upcoming Roblox…
**Take:** Viewed. A 'Weekly' store for Flowstate (designed and animated, with sound): the header shows a reset countdown ('Resets in 47:59:53'), a STARTER PACK card with a SALE corner ribbon and contents (x8,000 yen, x5 rolls, x10 packs) next to a 67 R$ price, a VALUE PACK at 999 R$, and bottom tabs (Weekly, Packs, Rolls, Yen). Purchase flow: native prompt → 'Processing…' with a spinning Robux icon → 'Purchase Complete!' with confetti → the card flips to OWNED. Show a processing state; never leave the player guessing.

#### angeisthere — shop GUI
[post](https://x.com/angeisthere/status/2104319890525929925) · ♥ 155 · 2026-09-27 · [[Assets/Reference-Captures/X/ui-shop/angeisthere-2104319890525929925/vid-1.mp4|▶ video 1]]
![[Assets/Reference-Captures/X/ui-shop/angeisthere-2104319890525929925/sheet-1.jpg|480]]
> ⚡ SHOP GUI — OPEN FOR COMMISSIONS New shop UI made for @x4yto 🛒✨…
**Take:** Viewed (grid). Shop with a Royal Abyss egg banner (timer, egg quantities 50/10/3/1) and a Passes row (x2 Growth faster, x2 Power).

#### ham3d777_ — store system scripted
[post](https://x.com/ham3d777_/status/2095136758681796680) · ♥ 150 · 2026-09-02 · [[Assets/Reference-Captures/X/ui-shop/ham3d777_-2095136758681796680/vid-1.mp4|▶ video 1]]
![[Assets/Reference-Captures/X/ui-shop/ham3d777_-2095136758681796680/sheet-1.jpg|480]]
> Store System UI by: @TravqaX (comms open) Scripted by: me (comms open) If you…
**Take:** Viewed (grid). 'STARTER BUNDLE' card: universal packs x3 plus items, 'The perfect start for your factory!', '80% VALUE' and LIMITED TIME tags; tabs for Packs and Gears.

#### brickoUI — revamped store with effects
[post](https://x.com/brickoUI/status/1958526453332512868) · ♥ 147 · 2025-08-21
![[Assets/Reference-Captures/X/ui-shop/brickoUI-1958526453332512868/img-1.jpg|480]]
> 🛒Revamped Store UI, last one was basic so I added more effects! 📕 Discord:…
**Take:** Viewed (grid). Exclusive store column: VIP, Godly Fish, bundle packs, small potion packs, and a Redeem Code box at the bottom.

#### immortal_dev777 — animated sakura shop
[post](https://x.com/immortal_dev777/status/2071960278451802473) · ♥ 145 · 2026-06-30 · [[Assets/Reference-Captures/X/ui-shop/immortal_dev777-2071960278451802473/vid-1.mp4|▶ video 1]]
![[Assets/Reference-Captures/X/ui-shop/immortal_dev777-2071960278451802473/sheet-1.jpg|480]]
> Animated Sakura Shop UI 🌸 DC: immortal_dev777 || UI Commissions open! | | |…
**Take:** Viewed (grid). Sakura scroll shop: a hanging scroll frame with cherry blossoms, 'Offers end in' timer, a Bundles row with a SPECIAL ribbon. Theme carried by the frame shape.

#### captideRBLX — crate shop
[post](https://x.com/captideRBLX/status/1681960416040157185) · ♥ 120 · 2023-07-20 · [[Assets/Reference-Captures/X/ui-shop/captideRBLX-1681960416040157185/vid-1.mp4|▶ video 1]]
![[Assets/Reference-Captures/X/ui-shop/captideRBLX-1681960416040157185/sheet-1.jpg|480]]
> 🎁 - Crate shop UI (Commissions Open)
**Take:** Viewed (grid). Crate shop: left nav (Character, Accessories, Credits, Fate Crystals, Crates, Gamepasses) and a grid of case cards colour-coded by rarity.

#### jackdoesui — brainrot shop
[post](https://x.com/jackdoesui/status/1968476656760442952) · ♥ 119 · 2025-09-18
![[Assets/Reference-Captures/X/ui-shop/jackdoesui-1968476656760442952/img-1.jpg|480]]
> 🛒 Brainrot Shop UI Looking for high-quality and fast ui work done? Add me…
**Take:** Viewed (grid). Brainrot 'Limited Shop': Exclusive Lucky Box (units at 35%, 10/3/1 box prices, timer) above a Starter Pack '40% OFF'.

#### brickoUI — stud store inspired by Steal a Egg
[post](https://x.com/brickoUI/status/2095572341858172929) · ♥ 116 · 2026-09-03 · [[Assets/Reference-Captures/X/ui-shop/brickoUI-2095572341858172929/vid-1.mp4|▶ video 1]]
![[Assets/Reference-Captures/X/ui-shop/brickoUI-2095572341858172929/sheet-1.jpg|480]]
> 🔥 HIGH PCR STORE UI! Stud styled UI inspired by Steal a Egg, with…
**Take:** Viewed. A stud-style 'Store' inspired by Steal an Egg (pitched as high conversion). Sections: Offers (GOLDEN EGG limited-time card with a countdown in days, 5 pets with % odds, egg-quantity prices 3499/759/249/99 R$), Passes (x2 Growth, x2 Money), Speed tiers (+150k/+1M/+10M up to +1B), Cash tiers, with the biggest pack tinted orange. One scrolling column; section titles are centred small caps.

#### b8ffc_ — Slime RNG shop redesign
[post](https://x.com/b8ffc_/status/2055189886831911115) · ♥ 107 · 2026-05-15
![[Assets/Reference-Captures/X/ui-shop/b8ffc_-2055189886831911115/img-1.jpg|480]]
> 💫Slime RNG - shop redesign for fun!
**Take:** Viewed (grid). Slime RNG shop redesign: roll passes (Double Roll R$599, Fast Roll R$299, Lucky Rolls R$75) and coin packs with escalating bonus (+15%, +50%, +100%), gift icon on every card, red '!' on featured items.

#### se9kq — stud style shop
[post](https://x.com/se9kq/status/2024109490321359220) · ♥ 83 · 2026-02-18
![[Assets/Reference-Captures/X/ui-shop/se9kq-2024109490321359220/img-1.jpg|480]]
> ✧ Stud Style Shop UI! For commissions, Contact 'se9kq' on discord.
**Take:** Viewed (grid). Stud shop: Sever Luck boost, Starter Pack '50% OFF', VIP and Gravity Coil cards; card colour by category.

#### NexusUI_RBLX — Escape Tsunami shop concept
[post](https://x.com/NexusUI_RBLX/status/2019075828039180669) · ♥ 64 · 2026-02-04
![[Assets/Reference-Captures/X/ui-shop/NexusUI_RBLX-2019075828039180669/img-1.jpg|480]]
> "Escape Tsunami For Brainrots" Shop UI concept Commisions are open
**Take:** Viewed (grid). Escape Tsunami-style store: a STARTER PACK 'Best Deal!' row (4 units joined by + signs, struck price) above Jump Coil and Speed Coil cards.

#### anthnyjhn_ — clicking simulator UI pack
[post](https://x.com/anthnyjhn_/status/1592125201357078528) · ♥ 55 · 2022-11-14
![[Assets/Reference-Captures/X/ui-shop/anthnyjhn_-1592125201357078528/img-1.jpg|480]]
> Clicking Simulator UI Pack for sale!😉♥️ The price starts at 15K! Offer below!
**Take:** Viewed (grid). Clicking-sim UI pack: inventory grid with Equip, search, '21/60' capacity, side boosts (100M+), Auto and x2 click buttons at the bottom.

#### jackdoesui — bomb chip shop
[post](https://x.com/jackdoesui/status/2007770032630071765) · ♥ 52 · 2026-01-04
![[Assets/Reference-Captures/X/ui-shop/jackdoesui-2007770032630071765/img-1.jpg|480]]
> Inspired "Bomb Chip" Shop UI For commissions — contact "jackrblx" on Discord.
**Take:** Viewed (grid). Bomb Chip-inspired shop: tabs (Food, Chairs, Cash), a VIP card with permanent 2x streak and 2x trophy, then x2 Cash / x2 Trophy / x2 Streak passes.

#### Byte_10 — cartoony simulator shop
[post](https://x.com/Byte_10/status/1962821995021602932) · ♥ 30 · 2025-09-02
![[Assets/Reference-Captures/X/ui-shop/Byte_10-1962821995021602932/img-1.jpg|480]]
> Made a Simulator/Cartoony Shop UI for fun! Price : $10/$3K RBX per frame Discord…
**Take:** Viewed (grid). Cartoony store with a Gamepasses grid (VIP, Luck x3 tiers), each card with a short benefit line and price.

#### buddingrblx — stud UI pack
[post](https://x.com/buddingrblx/status/2026262712796479830) · ♥ 13 · 2026-02-24 · [[Assets/Reference-Captures/X/ui-shop/buddingrblx-2026262712796479830/vid-1.mp4|▶ video 1]]
![[Assets/Reference-Captures/X/ui-shop/buddingrblx-2026262712796479830/sheet-1.jpg|480]]
> 💫 Stud UI Pack for ANY GAME!! ⭐️ 7+ Frames 🎁 Easy to customise…
**Take:** Viewed. A placeholder stud UI pack (7+ frames, $50 / 15k R$): Shop, Daily Rewards (days 1–7 with a big day-7 card), Rewards grid, Upgrades (+1 Pet Slot rows), Rebirth (rewards and requirements), Index with rarity tabs, a Yes/No confirm, and 'Friend Boost: 67%' on the HUD. The full simulator frame set in one template.

#### peek_ui — stud style shop/inventory/spin
[post](https://x.com/peek_ui/status/1964851170171834476) · ♥ 12 · 2025-09-08 · 4 images
![[Assets/Reference-Captures/X/ui-shop/peek_ui-1964851170171834476/img-1.jpg|480]]
> STUD STYLE shop, inventory/skins, spin the wheel, and confirm UI + HUD i did…
**Take:** Viewed (grid). Stud-style VIP shop: VIP Rank card (rewards list, 'was' price struck), three cash packs with gift buttons, and a 'Pick to Gift' friends list on the side; 'Starter Pack' countdown chip on the HUD.

#### Infinity_UI_ — dark simulator UI
[post](https://x.com/Infinity_UI_/status/1781734300330664251) · ♥ 8 · 2024-04-20
![[Assets/Reference-Captures/X/ui-shop/Infinity_UI_-1781734300330664251/img-1.jpg|480]]
> Roblox dark themed Simulator UI
**Take:** Viewed (grid). Dark simulator UI: a 'BUY VIP' popup listing perks (+30% coins, +25% speed, chat tag) with price and 'No Thanks', plus a Starter Pack bubble on the HUD.

#### Xad_91 — Blade Ball shop
[post](https://x.com/Xad_91/status/1810771259204194560) · ♥ 1 · 2024-07-09
![[Assets/Reference-Captures/X/ui-shop/Xad_91-1810771259204194560/img-1.jpg|480]]
> Shop UI for Blade Ball😊 Commissions are open!! Portfolio: Discord: xad91
**Take:** Viewed (grid). Blade Ball shop: top tabs (Battle Pass, Ability Spin, Daily Rewards, Galactic Crate, Merchant), 'Restocks in 11h 56m', item cards, and a big featured sword with 'Buy For 300'.

### Stud-style and cartoony UI (13)

#### cloudbeppXD — simple stud animated
[post](https://x.com/cloudbeppXD/status/2018135118066467305) · ♥ 316 · 2026-02-02 · [[Assets/Reference-Captures/X/ui-stud/cloudbeppXD-2018135118066467305/vid-1.mp4|▶ video 1]]
![[Assets/Reference-Captures/X/ui-stud/cloudbeppXD-2018135118066467305/sheet-1.jpg|480]]
> Simple UI Stud Animated - Fast Comm
**Take:** Viewed. Simple stud UI set (Shop bundle/items, Upgrade rows with +10 speed '3500 → 3600' previews, Rebirth with progress bar, Configs toggles). Every upgrade row shows before → after values.

#### reliskdev — anime + stud blend with tweens
[post](https://x.com/reliskdev/status/2019678685377491375) · ♥ 267 · 2026-02-06 · [[Assets/Reference-Captures/X/ui-stud/reliskdev-2019678685377491375/vid-1.mp4|▶ video 1]]
![[Assets/Reference-Captures/X/ui-stud/reliskdev-2019678685377491375/sheet-1.jpg|480]]
> Blend of anime &amp; studstyle ui and tweens all by me! Comms are open:…
**Take:** Viewed (grid). 'Your Plot' Robux Store with left tabs (Exclusive, Bundles, Cash): cash packs 4,000 → 650,000 where the art grows (bill stack → bag → chest of bills) and every card has BUY and GIFT side by side; 'Friend Luck +10%' chip bottom-right.

#### DevionUI — high quality UI for conversion
[post](https://x.com/DevionUI/status/2077402125660037496) · ♥ 253 · 2026-07-15 · [[Assets/Reference-Captures/X/ui-stud/DevionUI-2077402125660037496/vid-1.mp4|▶ video 1]]
![[Assets/Reference-Captures/X/ui-stud/DevionUI-2077402125660037496/sheet-1.jpg|480]]
> looking for high quality ui to increase your conversion? contact me on discord @…
**Take:** Viewed. 'Block Cup Shop' stud template: a Cup Block row (6 units with %, Buy 1/5/10, timer), Potions (Cash, Luck, Weight, Farming, each showing 'Owned: 15' with Use and Buy), Currency (3 small packs, 2 large 'BEST VALUE +20 FREE' packs). Showing owned count and a Use button inside the shop is handy.

#### DevionUI — stud UI animation
[post](https://x.com/DevionUI/status/2033441049323147481) · ♥ 228 · 2026-03-16 · [[Assets/Reference-Captures/X/ui-stud/DevionUI-2033441049323147481/vid-1.mp4|▶ video 1]]
![[Assets/Reference-Captures/X/ui-stud/DevionUI-2033441049323147481/sheet-1.jpg|480]]
> Little animation from my most recent stud ui showcase, let me know your thoughts…
**Take:** Viewed. Stud shop animation: an 'Exclusive Block' rainbow-cube row with a timer and unit odds, then three 1,000-cash cards each with price + gift icon; cards pop in left to right.

#### captideRBLX — stud styled buttons
[post](https://x.com/captideRBLX/status/1976642750494765132) · ♥ 182 · 2025-10-10
![[Assets/Reference-Captures/X/ui-stud/captideRBLX-1976642750494765132/img-1.jpg|480]]
> 🧱 - Stud Styled Buttons UI Commissions are open, DM to upgrade your game's…
**Take:** Viewed. Stud buttons set: slanted parallelograms (blue Collect with tick, yellow Purchase, green icon, purple Choose, red home), each with stud texture, a darker outline the same hue as the fill, and a white-outlined label. Colour per action; consistent slant.

#### DevionUI — animated showcase
[post](https://x.com/DevionUI/status/2085278298649894959) · ♥ 172 · 2026-08-06 · [[Assets/Reference-Captures/X/ui-stud/DevionUI-2085278298649894959/vid-1.mp4|▶ video 1]]
![[Assets/Reference-Captures/X/ui-stud/DevionUI-2085278298649894959/sheet-1.jpg|480]]
> ended up animating my previous showcase looking to improve your games ui and improve…
**Take:** Viewed. 'Ice King Shop': cash cards and a LIMITED character card; buying flies cash into a glowing case in the world with a CLAIM button; gifting shows a confirm dialog then a 'GIFT SENT!' burst. Gift flow fully animated.

#### reliskdev — stud UI conversion/trust
[post](https://x.com/reliskdev/status/2023382108409061620) · ♥ 167 · 2026-02-16 · [[Assets/Reference-Captures/X/ui-stud/reliskdev-2023382108409061620/vid-1.mp4|▶ video 1]]
![[Assets/Reference-Captures/X/ui-stud/reliskdev-2023382108409061620/sheet-1.jpg|480]]
> Increases conversion by 5x (trust). Some more stud UI but who doesn't love that,…
**Take:** Viewed (grid). 'Prove you are EPIC!!! Join the group + like the game → Claim Reward' free-reward popup, with a left vertical tag column (Shop, Index, Rebirth) and right VIP / FREE gift buttons. ⚠️ verify: group-join rewards are common; check current rules before rewarding 'likes' (open item in [[Gap-Tracker]]).

#### captideRBLX — cartoony buttons
[post](https://x.com/captideRBLX/status/1925925492466581601) · ♥ 165 · 2025-05-23
![[Assets/Reference-Captures/X/ui-stud/captideRBLX-1925925492466581601/img-1.jpg|480]]
> 🐛 - Cartoony Buttons
**Take:** Viewed. Cartoony buttons: square icon buttons (warning, shop, wand) and wide labelled buttons (Report Player purple, Enter Shop blue, Settings grey) with a large faint icon watermark inside each, a soft gloss and a darker bottom edge. The watermark icon is a cheap richness trick.

#### DevionUI — stud style client UI
[post](https://x.com/DevionUI/status/1943645281095909758) · ♥ 155 · 2025-07-11
![[Assets/Reference-Captures/X/ui-stud/DevionUI-1943645281095909758/img-1.jpg|480]]
> Stud Style UI I recently made for a client what do you guys think?…
**Take:** Viewed (grid). Bee/honey sim stud set: a Shop with Honey Pack tiers and a NEW Exotic Honey Pack (limited timer; 1 / 3 / 10 packs, each price button with a gift icon beside it); a WEATHER frame where players buy timed server weather ('+50% grow speed', 'higher celestial fruit chance'); Settings with a 'Receive Gifts' toggle and a Redeem Codes field. Buyable server weather is a Grow-a-Garden-era monetisation pattern; gift buttons sit next to every price.

#### Livvyjuju — RNG UI pack
[post](https://x.com/Livvyjuju/status/2056489743928713612) · ♥ 130 · 2026-05-18
![[Assets/Reference-Captures/X/ui-stud/Livvyjuju-2056489743928713612/img-1.jpg|480]]
> Working on a RNG UI Pack ❣️ Releasing this week :)
**Take:** Viewed (grid). RNG game HUD: one big central ROLL die button with BACKPACK and UPGRADE either side, a coin counter top-left, a right column of Shop / Rebirth / Teleport / Index, and potion and lucky-item stacks with counts bottom-left. The core verb button is the biggest thing on screen.

#### ProjectLarryUI — pixel stud obby UI
[post](https://x.com/ProjectLarryUI/status/2040982467620835437) · ♥ 114 · 2026-04-06
![[Assets/Reference-Captures/X/ui-stud/ProjectLarryUI-2040982467620835437/img-1.jpg|480]]
> Pixel Stud Style Obby UI First time trying out this pixel style, liked how…
**Take:** Viewed (grid). Pixel stud obby monetisation: top row of skip products (+10 Skips, +50 Skips, Finish Obby), a 'Stage 20 | 67%' progress bar, an Items shop of troll tools (e.g. a Lightning Bolt that stuns other players), and a right column of 'Sabotage' (Blind All, Kill All, Admin) and Cash products. The standard obby product set; the sabotage products are fun but risky for a kid audience if they feel unfair.

#### Livvyjuju — wait in line UI
[post](https://x.com/Livvyjuju/status/2000425150425256299) · ♥ 105 · 2025-12-15
![[Assets/Reference-Captures/X/ui-stud/Livvyjuju-2000425150425256299/img-1.jpg|480]]
> some more ui catered to wait in line :)
**Take:** Viewed (grid). 'Wait in line' genre HUD: a 'Cut the line' panel ($100,000 in-game OR Buy 1 Cut R$9 / Buy 10 Cuts R$79), Auto-Cut and Instant-Enter top-centre, left column Nuke / Riot / Invite / Auras / Skip To End, right column 3x Cash / Trail / Emotes / Revenge, a level bar and a 'Friend Boost +0%' chip. Every action has both a grind price and a Robux price.

#### veltrixui — stud UI Rescue Brainrots
[post](https://x.com/veltrixui/status/2007054676223840433) · ♥ 103 · 2026-01-02 · 4 images
![[Assets/Reference-Captures/X/ui-stud/veltrixui-2007054676223840433/img-1.jpg|480]]
> Stud UI I made for Rescue Brainrots Discord : veltrixui
**Take:** Viewed. Rescue Brainrots game page (not the UI itself): thumbnail with a giant '$983,676,937/s' income number, 95% rating, 4.9k active, and an Event card 'Update 4 + Admin Abuse' scheduled for Sun 9:00 AM. Shows the update + admin-abuse event pairing on a scheduled Roblox Event.
<!-- catalogue:end -->

## Pitfalls
- These are mostly portfolio mockups on empty baseplates; text sizes are often too small for a phone. Check against
  [[UI-Layout-And-Device-Scaling]].
- Loot boxes with Robux need the odds disclosed before purchase (⚠️ verify the current Roblox paid-random-item rules);
  every reference here does show odds.
- Don't copy branded art (Steal An Egg, Fisch, anime IP). Copy structure and motion only.

## Related
[[X-Reference-Library]] · [[X-HUD-And-Menus-UI]] · [[X-Animated-UI-Lessons-And-Tools]] · [[Bundles-And-Starter-Packs]] ·
[[Pricing-Psychology]] · [[Conversion-Funnels]] · [[Events-And-Seasons]] · [[UI-Polish-And-Juice]]

## Sources
Per-post X links are in each catalogue entry (captured 2026-10-04; like counts at capture time).
