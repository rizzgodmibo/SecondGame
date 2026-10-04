---
tags: [reference/ui, design/onboarding]
status: draft
updated: 2026-10-04
confidence: medium
---
# UI and First-Minute Gameplay Reference: 10 Top Games

How ten top games lay out their HUD, where the shop is, how the first reward arrives, how often pop-ups fire, and what
feedback they use. Compiled from beginner guides, wikis and press (linked per game) on 2026-10-04. Live screenshots could not
be captured (Roblox and wiki hosts were blocked by egress). Wiki pages are linked so they can be viewed directly.
Owner-supplied clip breakdowns with frame grabs are in [[Community-Showcase-Breakdowns]].

## TL;DR
- **The first reward lands within 30–60 s and costs nothing.** Examples: a free starter egg (Adopt Me), a cheap conveyor brainrot (Steal a Brainrot), starter seeds (Grow a Garden), breakables right at spawn (PS99).
- **Use a passive income ticker to keep players watching.** Steal a Brainrot, Steal An Egg and Grow a Garden all have income that ticks while you wait. Pair it with a visible `+$/s`.
- **Make shops physical NPC stands in the world, plus a HUD button.** Players walk to Sam or Steven (Grow a Garden) or to the conveyor (Steal a Brainrot), but a button opens the same UI. The world teaches, the button speeds things up.
- **Time-boxed loops create pop-up cadence.** Restock timers, lock timers (60 s), round timers (DTI 6 min, MM2 rounds) and the DOORS pre-run shop (30 s) give the HUD a heartbeat without spam.
- **Put "needs" in a left-side task list** (Adopt Me orange tasks). One glance tells the player what to do next.
- **Social proof is in the world, not the UI.** Other players' bases, gardens and outfits are the advertisement for the next purchase.

## Layout conventions observed across top games
| Zone | What usually goes there | Examples |
|---|---|---|
| Top-centre | Objective, timer, theme or round info | DTI theme + timer; MM2 role reveal; Steal a Brainrot lock timer at base |
| Top-left/left edge | Currency, task list, menu buttons (Shop, Inventory, Pets) | Adopt Me tasks (left); PS99 left-side buttons (house icon returns to spawn) |
| Bottom-centre | Hotbar/tools | Grow a Garden tools; 99 Nights inventory sack |
| Bottom-right | Big contextual action (mobile thumb zone) | Hatch, Claim, Steal, Sprint |
| World-space | Shops as NPC stands, billboards over bases with owner and income | Grow a Garden stands; Steal a Brainrot base signs |

Roblox's own HUD tutorial shows safe-area insets. Keep HUD inside **CoreUISafeInsets** so the Roblox top-bar and device notches never cover it:

![Core UI safe insets](https://raw.githubusercontent.com/Roblox/creator-docs/9f840b170b3e472c705e035126b45e3e050daed2/content/en-us/assets/tutorials/creating-hud-meters/Meter-CoreUISafeInsets.png)
![Device safe insets](https://raw.githubusercontent.com/Roblox/creator-docs/9f840b170b3e472c705e035126b45e3e050daed2/content/en-us/assets/tutorials/creating-hud-meters/Meter-DeviceSafeInsets.png)
*(Roblox Creator Docs, CC-BY-4.0, from the "Create HUD meters" tutorial.)*

---

## 1. Grow a Garden (tycoon/idle)
- **First minute:** spawn at your own plot → plant starter seeds → crops grow in real time → harvest → walk to **Steven's stand to sell** for Sheckles → buy more seeds at **Sam's seed shop** ([GameSpot guide](https://www.gamespot.com/articles/grow-a-garden-beginners-guide-and-tips/1100-6535055/)).
- **Shop entry points:** NPC stands in a central row (seeds, gear, sell). A gear shop sells watering cans, sprinklers and sprays. Rotating event merchants appear.
- **Cadence:** seed and gear stock **restocks on a timer** (⚠️ verify the interval, commonly reported as about 5 min). Weather and events (mutations) arrive as server-wide announcements. This is the main "pop-up" pressure, and it is *opportunity*, not nagging.
- **Feedback:** crops visibly grow. Rare mutations glow and change colour. Sell price pops as text.
- **Steal this:** a **server-wide event announcement** turns a solo idle loop into a shared moment ("everyone check your garden").

## 2. Steal a Brainrot (tycoon + PvP heist)
- **First minute:** a free or cheap **Noobini Pizzanini from the red conveyor** in the map centre → place it in your base → it earns **cash per second** → buy better ones off the conveyor ([guide](https://gameanomaly.com/steal-a-brainrot-guide/)).
- **Shop entry point:** the **conveyor belt itself is the shop**. Items scroll past with price and rarity labels, creating scarcity and FOMO without any UI.
- **Cadence:** base **Lock button: locked for 60 s**. Unlocked windows are 30 s (+10 s per rebirth). The lock timer creates a natural "go back to base" rhythm. **Rebirth** needs 1M cash plus specific brainrots and grants multipliers ([Beebom](https://beebom.com/steal-a-brainrot-rebirth-guide-levels-and-rewards/)).
- **Feedback:** cash floats up from each unit. Rarity colours on labels. Being robbed is loud and visible.
- **Steal this:** a **moving storefront** (conveyor) plus **a timed vulnerability window** (lock) gives tension in a tycoon.

## 3. Steal An Egg (2026 #1)
- **First minute:** pick an egg your **Speed** can handle → grab it → run home before the guardian catches you → place it on your grass → a **hatch timer** runs → press **Hatch** on screen → the pet earns money per second → upgrade the **treadmill** to gain Speed ([TechWiser](https://techwiser.com/steal-an-egg-beginner-guide/), [guide](https://stealanegg.app/guides/how-to-play/)).
- **Gating:** biomes are gated by Speed, not money. It is a physical progression check.
- **Feedback:** a chase (guardian) gives adrenaline. The hatch reveal is a gacha moment.
- **Steal this:** **a skill-light chase plus a gacha reveal plus idle income** in one loop. Each step has a different emotion: tension, surprise, satisfaction.

## 4. Adopt Me! (pet RPG/roleplay)
- **First minute:** spawn → choose **Parent or Baby** at the Age-O-Matic (Baby earns 2× Bucks on tasks) → collect the **free Starter Egg** at the Nursery (Cat or Dog) ([guide](https://games.gg/adopt-me/guides/adopt-me-beginners-guide/)).
- **HUD:** **needs and tasks appear as icons on the left**. Orange tasks pay more than blue. Each task sends you to a location (Salon, Pizza Shop, School, Campsite). The **Task Board** gives daily Bucks and eggs. The **Guide** (achievement rewards) was added on 2025-12-16 ([Fandom](https://adoptme.fandom.com/wiki/Guide)).
- **Steal this:** a **needs list as the onboarding**. It never explains; it just asks ("Your pet is hungry"), and the answer moves you around the map.

## 5. Pet Simulator 99 (clicker/collector)
- **First minute:** break objects at spawn for coins → **first egg costs 100 coins** → each pet speeds up breaking → push into the next zone ([guide](https://playpatch.org/roblox/pet-simulator-99/guide/)).
- **HUD:** left-side buttons, with a house icon to return to spawn and upgrades. Auto-hatch unlocks at Rebirth 2.
- **Cadence:** constant number pops and coin magnet. Zone purchase gates come every few minutes early on.
- **Steal this:** **the first currency source is visible at spawn**, needing zero instruction.

## 6. Dress To Impress (round-based social)
- **First minute:** lobby/intermission → **theme revealed** → **about 5–6 min dressing timer** (sources say 325–360 s) → runway → everyone votes **1–5 stars** → stars raise your rank (New Model → Fashion Goddess at 25,000+) ([PixelTwelve](https://pixeltwelve.com/articles/dress-to-impress-beginner-guide), [guide](https://dresstoimpresscodes.wiki/guides/how-to-play/)).
- **HUD:** theme plus timer always visible at the top. Wardrobe and stations are physical areas (hair, makeup, colour wall). There is an item cap of 18, or 24 with a gamepass.
- **Monetisation entry point:** the **limit itself** (item cap → gamepass) and premium items in the wardrobe.
- **Steal this:** **peer voting as the reward**. Players generate each other's rewards, so there's no content treadmill.

## 7. DOORS (co-op horror roguelite)
- **First minute:** lobby with **12 elevators** (1–4 player parties) → enter → **Pre-Run Shop in the elevator for 30 s** (Vitamins 100, Lockpicks 50, Lighter 50, Flashlight 100 Knobs) → run starts ([Wiki: Shops](https://doors-game.fandom.com/wiki/Shops), [Lobby](https://doors-game.fandom.com/wiki/Lobby)).
- **Currency:** **Knobs** earned at run end (escape *or* death screen) or bought with Robux ([Knobs](https://doors-game.fandom.com/wiki/Knobs)).
- **Steal this:** **put the shop in dead time**. The elevator wait becomes a purchase moment. Rewards are paid even on death, so failure still progresses.

## 8. 99 Nights in the Forest (co-op survival)
- **First minute:** lobby with a class showcase (classes cost Diamonds) → spawn at a campfire → **night 1 is the only safe night**: chop 5–6 logs to reach **Campfire Level 2**, which expands the map and keeps the Deer away ([PC Gamer tips](https://www.pcgamer.com/games/roblox/99-nights-in-the-forest-tips/), [The Click](https://www.theclick.gg/99-nights-in-the-forest-beginners-guide/)).
- **Monetisation entry point:** **classes shown off in the lobby** (Scavenger 40 Diamonds, Camper 10). Diamonds come from badges, achievements, rare chests and codes.
- **Steal this:** **the lobby is a showroom.** Players see the premium tools before the run, and the first night is a safe tutorial disguised as a deadline.

## 9. Murder Mystery 2 (social deduction rounds)
- **First minute:** lobby → map vote → **secret role reveal** (Innocent, Sheriff, Murderer) → round → coins collected during play → back to lobby ([MM2 guide](https://mm2guide.com/guides/beginner-guide/)).
- **Economy:** **1,000 coins opens a crate**. Godly-tier drops are about 1 in 500. All weapons are cosmetic.
- **Steal this:** **a dramatic role reveal** (full-screen, sound sting) as the start-of-round hook. Collectibles earned *during* rounds give losers progress too.

## 10. Animal Hospital (anomaly horror)
- **First minute:** start a shift at reception → inspect the patient → **take a photo → check CCTV while it develops → compare** → admit, or slam the **red shutter button** if anomalous. Keep **Sanity** above 0 ([Destructoid](https://www.destructoid.com/animal-hospital-walkthrough-guide/), [how-to](https://animalhospitalroblox.wiki/guides/how-to-play/)).
- **HUD:** mostly diegetic. The desk *is* the UI (stamps, PC, printer, CCTV monitors, shutter). The HUD shows only Sanity and shift progress.
- **Steal this:** **diegetic interfaces** (in-world screens and buttons) make a simple check-in loop feel physical and tense.

---

## Cross-game rules
1. **Reward #1 must come in ≤ 60 s with zero reading.** Put the first currency source or free item at spawn.
2. **Two entry points per shop:** a world stand (teaches location and fantasy) plus a HUD button (speed).
3. **Make timers the pop-up system.** Use restock, lock, round, pre-run and night timers instead of modal "BUY NOW" pop-ups. Reserve modals for purchases the player started.
4. **Pay out on failure.** DOORS knobs on death and MM2 coins mid-round keep losers returning.
5. **Use dead time for shopping** (elevator, intermission, lobby).
6. **Make others' progress visible** (bases, gardens, outfits, pets). It is the best upsell and costs no UI.
7. **Mobile first:** the big action button goes bottom-right. Nothing important sits under the top-bar inset.

See [[Onboarding-And-First-60-Seconds]] for the design theory and [[UI-Architecture]] for implementation.

## Checklist
- [ ] Capture 1 screenshot per game (first spawn, shop open, first reward) by URL from the wikis and embed it here.
- [ ] Time first-reward latency yourself in each game (stopwatch) and replace the estimates.
- [ ] Verify the Grow a Garden restock interval.

## Pitfalls
- Guides describe the *current* version. Onboarding in these games changes often (e.g. the Adopt Me Guide was added in Dec 2025). Date your observations.
- Copying the HUD without the loop fails. The conveyor works because scarcity and stealing exist.

## Related
- [[Reference/_Index|Reference index]] · [[Community-Showcase-Breakdowns]] · [[Onboarding-And-First-60-Seconds]] · [[UI-Architecture]]
- [[UI-Layout-And-Device-Scaling]] · [[UI-Polish-And-Juice]] · [[Core-Loops]] · [[Reward-Schedules]] · [[Prestige-And-Rebirth]] · [[Idle-And-Offline-Earning]]

## Sources
(web search, 2026-10-04)
- Grow a Garden: [GameSpot beginner guide](https://www.gamespot.com/articles/grow-a-garden-beginners-guide-and-tips/1100-6535055/)
- Steal a Brainrot: [GameAnomaly guide](https://gameanomaly.com/steal-a-brainrot-guide/), [Beebom rebirth](https://beebom.com/steal-a-brainrot-rebirth-guide-levels-and-rewards/)
- Steal An Egg: [TechWiser](https://techwiser.com/steal-an-egg-beginner-guide/), [stealanegg.app](https://stealanegg.app/guides/how-to-play/)
- Adopt Me: [games.gg](https://games.gg/adopt-me/guides/adopt-me-beginners-guide/), [Fandom Guide](https://adoptme.fandom.com/wiki/Guide)
- PS99: [playpatch](https://playpatch.org/roblox/pet-simulator-99/guide/) · DTI: [PixelTwelve](https://pixeltwelve.com/articles/dress-to-impress-beginner-guide)
- DOORS: [Wiki Shops](https://doors-game.fandom.com/wiki/Shops), [Lobby](https://doors-game.fandom.com/wiki/Lobby), [Knobs](https://doors-game.fandom.com/wiki/Knobs)
- 99 Nights: [PC Gamer](https://www.pcgamer.com/games/roblox/99-nights-in-the-forest-tips/) · MM2: [mm2guide](https://mm2guide.com/guides/beginner-guide/)
- Animal Hospital: [Destructoid](https://www.destructoid.com/animal-hospital-walkthrough-guide/)
- Roblox Creator Docs "Create HUD meters" images (CC-BY-4.0) @ `9f840b1`.
