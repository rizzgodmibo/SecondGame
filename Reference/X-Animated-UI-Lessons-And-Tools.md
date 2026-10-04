---
tags: [reference/x, reference/ui, visuals/ui-juice]
status: draft
updated: 2026-10-04
confidence: medium
---
# X Reference: Animated UI, Designer Lessons and UI Tools

28 posts: UI motion and juice, short design lessons from working Roblox UI designers, and plugins that bring Figma-style
workflows into Studio. Part of [[X-Reference-Library]].

## TL;DR — reusable motion primitives seen here
| Primitive | What it looks like | Reference |
|---|---|---|
| Spring press | Hover shrinks slightly; press squashes to about 0.9 and springs back with overshoot | captideRBLX 'satisfying buttons' |
| Shine sweep | A diagonal white band crosses the button on hover; slight scale-up | dearpureoni 'juicy buttons' |
| Odometer number | The old digit slides out and the new one slides in vertically | mashdee_ 'numbers go brrr' |
| Badge | A red NEW / '!' pip on a button with something new behind it | dearpureoni, DevionUI |
| Reveal | Dim → centre → shake → rays → name + rarity | jackdoesui, AstralDefined, Ang3lzUI |
| Card hover | Card lifts, glow outline, slight tilt | Zac1kio cards / shop |

## Designer lessons (short, actionable)
- **Price buttons must look pressable:** a chunky green button with the Robux glyph and an outlined number beats a flat
  box with '500 robux' text (captideRBLX).
- **Don't use pure black;** use a dark tinted colour (httptotem).
- **Font pairs (title + body), from captideRBLX:** Barlow + Poppins; Fira Sans + Prompt; Roboto Slab + Ubuntu (mythical or
  anime feel); Barlow + Cairo (FPS). Rule: 'the best UI is no UI', meaning readable, style-matching and out of the way.
  ⚠️ verify each font is available in Roblox's Font library.
- **Six UI mistakes (two captideRBLX threads):** buttons that don't look tappable; confusing navigation, popups and close
  buttons; cheap-looking, inconsistent styling; no visual hierarchy (the best-value item must stand out); the wrong
  control (toggle = on/off, slider = range, button = action); styling before structure (fix spacing and layout first).
- **Material metaphors** (stitched felt notebook with binder rings) make panels tactile without gradients (captideRBLX).
- **Colour ramps:** shift the hue toward blue as you darken (RhosGFX; worked numbers in [[X-Game-Feel-And-Showcases]]).

## Tools spotted (unevaluated; ⚠️ check safety, price and maintenance before installing)
Figblox (Figma → Studio, two plugins), Sketch (Figma-like editor inside Studio), Blob Canvas (UI import plugin),
an optimised UI blur module, a free viewport editor, ui-resources.com (free effects, backgrounds, icon packs).
Holden's existing tooling notes: [[Third Party Claude Tools Evaluated]].

## Catalogue
<!-- catalogue:start -->
### Animated UI and motion (17)

#### Simoon67 — Persona-inspired WIP (top liked)
[post](https://x.com/Simoon67/status/2079240431498563870) · ♥ 1,671 · 2026-07-20 · [[Assets/Reference-Captures/X/ui-anim/Simoon67-2079240431498563870/vid-1.mp4|▶ video 1]]
![[Assets/Reference-Captures/X/ui-anim/Simoon67-2079240431498563870/sheet-1.jpg|480]]
> WIP Inspired by Persona series
**Take:** Viewed. Persona-style 'Student Archive' menu (1.7k likes, the top #RobloxUI clip): an avatar profile card with an ID-card frame, a slanted list of options (Stats, Inventory, Playerlist, Restricted, Settings) and glitch scan-line transitions between screens. Strong art direction, but too heavy and mature-styled for a young-teen casual game; borrow the slanted-list and transition idea only.

#### acturko_ — Pokemon-inspired animated UI
[post](https://x.com/acturko_/status/2021344765082796289) · ♥ 1,193 · 2026-02-10 · [[Assets/Reference-Captures/X/ui-anim/acturko_-2021344765082796289/vid-1.mp4|▶ video 1]]
![[Assets/Reference-Captures/X/ui-anim/acturko_-2021344765082796289/sheet-1.jpg|480]]
> Pokemon Inspired Animated UI Heavily inspired by @EleonsOnline and Pocket Anime UI: Me and…
**Take:** Viewed (grid). Pokémon-inspired battle UI: HP bars with level chips top-left and bottom-right, and a four-wedge action wheel (Fight, Items, Switch, Catch) around a centre button. A radial command menu that suits thumbs on mobile.

#### SapopDev — anime card
[post](https://x.com/SapopDev/status/1979337222123065731) · ♥ 810 · 2025-10-18 · [[Assets/Reference-Captures/X/ui-anim/SapopDev-1979337222123065731/vid-1.mp4|▶ video 1]]
![[Assets/Reference-Captures/X/ui-anim/SapopDev-1979337222123065731/sheet-1.jpg|480]]
> Made this Anime Card as Practice ⭐ ❤️+ 🔃 are appreciated! 📌 Portfolio Server:
**Take:** Viewed (grid). A single anime trading card (Guts) with a holographic red frame tilting toward the cursor. Practice piece; card tilt reused in Zac1kio's TCG.

#### PunIsIntendeds — Live2D-style character in UI
[post](https://x.com/PunIsIntendeds/status/2105764992792551442) · ♥ 713 · 2026-10-01 · [[Assets/Reference-Captures/X/ui-anim/PunIsIntendeds-2105764992792551442/vid-1.mp4|▶ video 1]]
![[Assets/Reference-Captures/X/ui-anim/PunIsIntendeds-2105764992792551442/sheet-1.jpg|480]]
> Live2D style character running in Roblox UI the whole thing is one 1024×1024 texture…
**Take:** Viewed. A Live2D-style talking shopkeeper inside the UI (one 1024x1024 texture + a 70 KB ModuleScript for parameters and animation): she breathes, blinks and gestures beside the shop list and a character-select grid. A living NPC portrait makes a shop feel inhabited; expensive to produce.

#### Niki_Interface — 3D-like UI timelapse
[post](https://x.com/Niki_Interface/status/2093003442532810807) · ♥ 639 · 2026-08-27 · [[Assets/Reference-Captures/X/ui-anim/Niki_Interface-2093003442532810807/vid-1.mp4|▶ video 1]]
![[Assets/Reference-Captures/X/ui-anim/Niki_Interface-2093003442532810807/sheet-1.jpg|480]]
> A new 3D-like UI. Watch 2 hours of work in 35s.⌛️
**Take:** Viewed. 'Round 3 / Welcome to Arena 8' intro card displayed on a CRT-TV-shaped frame with scanlines and static, built in about 2 hours. A themed frame turns a plain text banner into a moment.

#### acturko_ — simple animated UI
[post](https://x.com/acturko_/status/1999590625365381379) · ♥ 534 · 2025-12-12 · [[Assets/Reference-Captures/X/ui-anim/acturko_-1999590625365381379/vid-1.mp4|▶ video 1]]
![[Assets/Reference-Captures/X/ui-anim/acturko_-1999590625365381379/sheet-1.jpg|480]]
> Simple Animated UI UI: Me and @d0garr Scripting/Animations: Me
**Take:** Viewed. Light-blue avatar editor: a floating panel with side category tabs (Clothing, Accessories, Body), search, an item grid and a colour wheel for skin tone; tabs pop out on hover. A clean template for an outfit or customisation screen.

#### Zac1kio — interactive card TCG
[post](https://x.com/Zac1kio/status/1892395478190334012) · ♥ 387 · 2025-02-20 · [[Assets/Reference-Captures/X/ui-anim/Zac1kio-1892395478190334012/vid-1.mp4|▶ video 1]]
![[Assets/Reference-Captures/X/ui-anim/Zac1kio-1892395478190334012/sheet-1.jpg|480]]
> 🔥 Mahoraga Interactive Card | Anime Pocket TCG illus. @T3Tech0 .gg/AnimePocket
**Take:** Viewed (grid). Anime Pocket TCG 'Mahoraga' card on a pink spotlight stage: the card tilts and shines; stats and abilities printed on the card face. Card-collection games treat the card itself as the reward screen.

#### s4rqwltys — animated profile
[post](https://x.com/s4rqwltys/status/2080954834895945803) · ♥ 246 · 2026-07-25 · [[Assets/Reference-Captures/X/ui-anim/s4rqwltys-2080954834895945803/vid-1.mp4|▶ video 1]]
![[Assets/Reference-Captures/X/ui-anim/s4rqwltys-2080954834895945803/sheet-1.jpg|480]]
> Animated Profile Ui Inspired By @ExpeditionsRBLX Ui by @Ang3lzUI
**Take:** Viewed. Green-framed profile panel (inspired by Expeditions) with a character render, an item grid and a stats column; the panel slides in and items pop in one by one.

#### unrooot — shop ui + animations hoarcekat
[post](https://x.com/unrooot/status/1361605675348975620) · ♥ 224 · 2021-02-16 · [[Assets/Reference-Captures/X/ui-anim/unrooot-1361605675348975620/vid-1.mp4|▶ video 1]]
![[Assets/Reference-Captures/X/ui-anim/unrooot-1361605675348975620/sheet-1.jpg|480]]
> shop ui + animations (ft. hoarcekat)
**Take:** Viewed. Dark minimal shop (2021, built with Hoarcekat for previewing UI in isolation): Home/Monsters/Tokens/Upgrades tabs, a 'Featured' row of items with Unlock buttons, and category cards (Accessories, Food, Toys, Weapons) that lift on hover. Shows that testing UI components outside the game speeds iteration.

#### acturko_ — cartoony animated UIs with SFX
[post](https://x.com/acturko_/status/2045563918672712121) · ♥ 213 · 2026-04-18 · [[Assets/Reference-Captures/X/ui-anim/acturko_-2045563918672712121/vid-1.mp4|▶ video 1]]
![[Assets/Reference-Captures/X/ui-anim/acturko_-2045563918672712121/sheet-1.jpg|480]]
> Cartoony Animated UIs (Has Sound/SFX) UI: Me and @d0garr Scripting/Animations: Me
**Take:** Viewed. Cartoony pastel UI set with sound: a bottom dock of 4 icons (Inventory, Store, Settings, Codes) opens panels that swing in rotated and settle with a bounce; a Store with 2x Luck tiles in four colours and Passes/Coins side tabs. The 'tossed card' open animation is a cheap way to add personality.

#### dearpureoni — juicy buttons
[post](https://x.com/dearpureoni/status/2046636127185158177) · ♥ 198 · 2026-04-21 · [[Assets/Reference-Captures/X/ui-anim/dearpureoni-2046636127185158177/vid-1.mp4|▶ video 1]]
![[Assets/Reference-Captures/X/ui-anim/dearpureoni-2046636127185158177/sheet-1.jpg|480]]
> Some juicy buttons 🫧
**Take:** Viewed. Top-bar pill buttons (Shop / Garage / Codes + cog) with checker-flag texture; on hover a diagonal white shine sweeps across and the button scales up slightly; Shop carries a red NEW badge. Cheap juice: one shine tween reused on every button.

#### AstralDefined — animated summon
[post](https://x.com/AstralDefined/status/1890833925070532784) · ♥ 193 · 2025-02-15 · [[Assets/Reference-Captures/X/ui-anim/AstralDefined-1890833925070532784/vid-1.mp4|▶ video 1]]
![[Assets/Reference-Captures/X/ui-anim/AstralDefined-1890833925070532784/sheet-1.jpg|480]]
> ✨ Animated Summon Interface! discord — astraldefined [ | | ]
**Take:** Viewed. 'Summon' banner: Summon 1/5/10 buttons (10 at '50% off offer'), Legendary and Mythic pity bars (115/120, 91/120), an Auto Sell rarity filter, and side cards for currency bags and x2 Luck. Pity counters make gacha odds feel fair; auto-sell reduces inventory clutter.

#### Zac1kio — traits re-roll animation
[post](https://x.com/Zac1kio/status/1970284042680443241) · ♥ 176 · 2025-09-23 · [[Assets/Reference-Captures/X/ui-anim/Zac1kio-1970284042680443241/vid-1.mp4|▶ video 1]]
![[Assets/Reference-Captures/X/ui-anim/Zac1kio-1970284042680443241/sheet-1.jpg|480]]
> Traits Re-Roll Animation @BlackCatEnter all ui yes...maby a lil overkill on this too
**Take:** Viewed. Traits re-roll: a crystal is consumed and a winged emblem spins with radial light rays, its colour changing with the rarity rolled (green, gold, red, blue, rainbow 'Ruler'); reroll-token packs priced on the left. The colour of the burst tells the result before the text does.

#### captideRBLX — satisfying buttons
[post](https://x.com/captideRBLX/status/1966507294998339640) · ♥ 161 · 2025-09-12 · [[Assets/Reference-Captures/X/ui-anim/captideRBLX-1966507294998339640/vid-1.mp4|▶ video 1]]
![[Assets/Reference-Captures/X/ui-anim/captideRBLX-1966507294998339640/sheet-1.jpg|480]]
> 🪄 Working on making buttons satisfying (Commissions Open)
**Take:** Viewed. A slanted purple button with a dot texture: hover shrinks it a little, press squashes to about 90% then springs back with overshoot. A spring tween is the whole trick.

#### Ang3lzUI — animated summon 2
[post](https://x.com/Ang3lzUI/status/2074879528745271684) · ♥ 159 · 2026-07-08 · [[Assets/Reference-Captures/X/ui-anim/Ang3lzUI-2074879528745271684/vid-1.mp4|▶ video 1]]
![[Assets/Reference-Captures/X/ui-anim/Ang3lzUI-2074879528745271684/sheet-1.jpg|480]]
> ✦ | Animted Summon UI turned out pretty sick
**Take:** Viewed. Dark anime summon screen: the screen fades through a signature card, then a 'Special Banner' with three featured units, Summon x1 / x10, a banner-end timer and two pity bars underneath.

#### reliskdev — purchase animation with random outcome text
[post](https://x.com/reliskdev/status/2030245855211782416) · ♥ 147 · 2026-03-07 · [[Assets/Reference-Captures/X/ui-anim/reliskdev-2030245855211782416/vid-1.mp4|▶ video 1]]
![[Assets/Reference-Captures/X/ui-anim/reliskdev-2030245855211782416/sheet-1.jpg|480]]
> Purchase animation, random text based on outcome ;) Commissions open Discord: reliskdev
**Take:** Viewed. The purchase prompt dims the world with a vignette; after buy or cancel a random one-liner appears under the character ('Leaving empty handed? Brave.', 'Drip!', 'Buy it, you deserve nice things'). ⚠️ For a young-teen audience, guilt or pressure copy around purchases is a dark pattern. Keep the personality only on the success line; see [[Pay-To-Win-Boundaries]] and [[Monetisation-Mistakes]].

#### mashdee_ — numbers go brrr counter
[post](https://x.com/mashdee_/status/2045182701884592285) · ♥ 144 · 2026-04-17 · [[Assets/Reference-Captures/X/ui-anim/mashdee_-2045182701884592285/vid-1.mp4|▶ video 1]]
![[Assets/Reference-Captures/X/ui-anim/mashdee_-2045182701884592285/sheet-1.jpg|480]]
> Numbers go brrrrr
**Take:** Viewed. A number counter tween: on change the old digit slides out and the new one slides in vertically (odometer roll) on a mint card. Use it on every currency and score display; 'numbers go brrr' is the dopamine.

### Designer lessons (5)

#### captideRBLX — 4 font pairs
[post](https://x.com/captideRBLX/status/2074552100923560231) · ♥ 378 · 2026-07-07
![[Assets/Reference-Captures/X/ui-lessons/captideRBLX-2074552100923560231/img-1.jpg|480]]
> Fonts can completely change the feel and style of your UI. Here's the 4…
**Take:** Thread read in full. The 4 pairs (title + body): #1 Barlow + Poppins (tall slender title with rounded wide body); #2 Fira Sans + Prompt (Fira is his favourite, versatile bold or thin); #3 Roboto Slab + Ubuntu (serif for a mythical/anime feel); #4 Barlow + Cairo (bold Barlow for FPS games, light Cairo for contrast). Principle: 'the best UI is no UI', meaning readable, style-matching and out of the way. ⚠️ verify each font exists in Roblox's Font library (Font.new / Creator Store fonts) before designing around it.

#### captideRBLX — 3 UI mistakes ruining revenue
[post](https://x.com/captideRBLX/status/1998821801690857577) · ♥ 371 · 2025-12-10
![[Assets/Reference-Captures/X/ui-lessons/captideRBLX-1998821801690857577/img-1.jpg|480]]
> ⚡️ - 3 UI mistakes ruining your game’s revenue. (🧵)
**Take:** Thread read in full. (1) Buttons don't look tappable: flat, low-contrast, too small, blending into the background; if a player can't instantly see what's clickable they won't click. (2) Confusion kills retention: annoying popups, confusing navigation, no visual order, unclear close buttons; players must instantly know 'where do I go / what do I tap next / how do I buy an upgrade'. (3) Cheap-looking UI reads as a rushed game, so players won't spend: unbalanced fonts, odd colours, inconsistent styles. A reply pushed back that Brookhaven and Blox Fruits succeed with plain UI; captide answered that their UI is deliberate. The cover image is the stitched-notebook frame.

#### httptotem — dark colours instead of black
[post](https://x.com/httptotem/status/1893368152198664530) · ♥ 236 · 2025-02-22 · [[Assets/Reference-Captures/X/ui-lessons/httptotem-1893368152198664530/vid-1.mp4|▶ video 1]]
![[Assets/Reference-Captures/X/ui-lessons/httptotem-1893368152198664530/sheet-1.jpg|480]]
> When designing UI, instead of using black, try using a color that's dark, but…
**Take:** Use a dark tinted colour (e.g. deep navy or purple) instead of pure black for panels and text; it looks softer and more premium.

#### captideRBLX — 3 UI mistakes in Roblox games
[post](https://x.com/captideRBLX/status/2000996132043039205) · ♥ 156 · 2025-12-16
![[Assets/Reference-Captures/X/ui-lessons/captideRBLX-2000996132043039205/img-1.jpg|480]]
> ❌ - 3 UI mistakes I keep seeing in Roblox games. (🧵)
**Take:** Thread read in full. (1) No visual hierarchy: when everything looks equally important nothing does; make the good-value item stand out. (2) Wrong control for the job: toggles for on/off, sliders for ranges, buttons for actions, key buttons for keybinds. (3) Styling before structure: spacing and layout first, fonts/colours/textures after ('you don't decorate a house before building it').

#### captideRBLX — what would you click - gamepass enticing UI
[post](https://x.com/captideRBLX/status/1935004090548772942) · ♥ 111 · 2025-06-17
![[Assets/Reference-Captures/X/ui-lessons/captideRBLX-1935004090548772942/img-1.jpg|480]]
> What would you click? 🪄 - Good enticing UI = More gamepass purchases
**Take:** Viewed. 'What would you click?' The same 500 R$ price as a chunky green button (Robux icon, white text with a dark outline, a darker bottom edge for depth) next to a flat grey box with red '500 robux' text. Price buttons should look pressable and use the Robux glyph, not the word.

### UI tools and plugins (6)

#### Zac1kio — Blob Canvas UI import plugin
[post](https://x.com/Zac1kio/status/1960429790973808735) · ♥ 865 · 2025-08-26 · [[Assets/Reference-Captures/X/ui-tools/Zac1kio-1960429790973808735/vid-1.mp4|▶ video 1]]
![[Assets/Reference-Captures/X/ui-tools/Zac1kio-1960429790973808735/sheet-1.jpg|480]]
> Blob. Canvas — UI Plugin Onboarding Roblox wouldn't do it so I did🫡 The…
**Take:** Tool: Blob Canvas, an all-in-one UI importing plugin built in Studio (Zac1kio). Unevaluated.

#### cloudbeppXD — UI blur module
[post](https://x.com/cloudbeppXD/status/2010445187869507857) · ♥ 711 · 2026-01-11 · [[Assets/Reference-Captures/X/ui-tools/cloudbeppXD-2010445187869507857/vid-1.mp4|▶ video 1]]
![[Assets/Reference-Captures/X/ui-tools/cloudbeppXD-2010445187869507857/sheet-1.jpg|480]]
> Working on a UI Blur Module (Otimized) [Tutorial Soon]
**Take:** Tool: an optimised UI blur module (cloudbeppXD). Blur behind panels is expensive on low-end phones; profile before using.

#### electrickflare — Sketch Figma-like editor in Studio
[post](https://x.com/electrickflare/status/2060613950086254740) · ♥ 690 · 2026-05-30 · [[Assets/Reference-Captures/X/ui-tools/electrickflare-2060613950086254740/vid-1.mp4|▶ video 1]]
![[Assets/Reference-Captures/X/ui-tools/electrickflare-2060613950086254740/sheet-1.jpg|480]]
> Tired of Roblox's annoying UI Editor? Sketch is here to solve that! It emulates…
**Take:** Tool: Sketch, a Figma-like UI editor inside Studio (690 likes). Unevaluated.

#### FigbloxDev — Figblox Figma to Studio
[post](https://x.com/FigbloxDev/status/2047405416749965803) · ♥ 513 · 2026-04-23 · [[Assets/Reference-Captures/X/ui-tools/FigbloxDev-2047405416749965803/vid-1.mp4|▶ video 1]]
![[Assets/Reference-Captures/X/ui-tools/FigbloxDev-2047405416749965803/sheet-1.jpg|480]]
> Figblox is a two-plugin system for moving UI from Figma into Roblox Studio. Here’s…
**Take:** Tool: Figblox, two plugins moving Figma UI into Studio (JSON export, ScrollingFrame/viewport support). Unevaluated.

#### baker_koda — viewport editor
[post](https://x.com/baker_koda/status/2081896909753520250) · ♥ 367 · 2026-07-28 · [[Assets/Reference-Captures/X/ui-tools/baker_koda-2081896909753520250/vid-1.mp4|▶ video 1]]
![[Assets/Reference-Captures/X/ui-tools/baker_koda-2081896909753520250/sheet-1.jpg|480]]
> Super simple viewport editor Get it for free:
**Take:** Tool: a free, simple ViewportFrame editor (Creator Store). Unevaluated.

#### Stuxfian — ui-resources.com
[post](https://x.com/Stuxfian/status/2099489902320898506) · ♥ 364 · 2026-09-14
> Hi if you want resources, you may go to Has over 300+ effects, 200+…
**Take:** Text post pointing to ui-resources.com (300+ effects, 200+ backgrounds, renders, icon packs, textures; free). Also recommended on TikTok by flayodev.
<!-- catalogue:end -->

## Pitfalls
- Several high-like anime UI clips (Persona-style, Pokemon-style, Live2D) are technically impressive but slow to build
  and off-style for a young-teen casual game. Take the motion ideas, not the look.
- UI blur and heavy ViewportFrames cost performance on low-end phones; profile first ([[Performance-And-Profiling]]).

## Related
[[X-Reference-Library]] · [[UI-Polish-And-Juice]] · [[X-Shop-And-Seasonal-UI]] · [[X-HUD-And-Menus-UI]] · [[UI-Architecture]]

## Sources
Per-post X links are in each catalogue entry (captured 2026-10-04).
