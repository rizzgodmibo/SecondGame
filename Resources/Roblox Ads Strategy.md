---
title: Roblox Ads Strategy
date: 2026-10-03
tags: [roblox, marketing, ads, launch, research]
project: Paper Plane Toss
---
# Roblox Ads Strategy (Sponsored Experiences / Ads Manager)

Research done for the [[Paper Plane Toss Release Prep|Paper Plane Toss launch]].

## How it works
- **Where ads show:** "Sponsored experiences" on the Home page and in search, using your thumbnails. A campaign can hold up to 10 creatives, and Roblox reports results per creative.
- **Pricing:** you pay **per play**, i.e. a player who joins after landing on the game page. Roblox bids automatically. Winning bids are usually **$0.04–0.07 per play**, and very low bids barely deliver.
- **Paying:** with ad credits (converted from Robux) or a card.
  - One source says the new system needs **at least 10 credits** (5/day for 2 days); the official docs state no minimum.
  - On a group-owned experience, run ads from the group's ad account.
- **Targeting:** All / New / Recent / Lapsed players, plus location, age, gender, genre and device. You must be 13+ to use Ads Manager. Roblox says to give a campaign **3–5 days** before judging it.

## Recommended plan for a small new simulator
1. **Test, 3–5 days:** about $5–10 a day, objective **Plays**, broad audience. Run **one campaign with 2–3 thumbnails** so Roblox finds the best one.
2. **Judge it:**
   - Ad click-through rate: aim for **1%+**; above 4% is great.
   - Cost per play.
   - D1 / D7 retention: **20%+** D7 minimum, **35%+** to grow.
   - Session length.
3. **Scale only if the numbers are good:** $15–25 a day for 1–3 weeks, continuously. Roblox needs time to notice the game. Returns drop after about 50K Home impressions.
4. **Low click-through means a thumbnail problem. Low retention means a game problem.** More money fixes neither.

DevForum ranges for simulators: start at 200–1,000 R$ to test, and spend 3K–10K R$ a day for 2–4 weeks if it works. Big studios spend 30–40K R$ a day.

The ranking algorithm rewards player behaviour (retention, playtime, repeat visits), not ad spend. Ads only buy the first wave of players, to create that data.

## Sources
- [Ads Manager docs](https://create.roblox.com/docs/production/promotion/ads-manager)
- [Sponsored Experiences moving to Ads Manager (DevForum)](https://devforum.roblox.com/t/sponsored-experiences-moving-to-ads-manager/2661756)
- [How much to spend to get into the algorithm (DevForum)](https://devforum.roblox.com/t/how-much-money-should-i-spent-to-get-into-the-algorithm/4551439)
- [How much should I spend for my simulator (DevForum)](https://devforum.roblox.com/t/how-much-robux-should-i-spend-on-sponsors-or-ads-for-my-simulator/703628)
- [BLOXG: Roblox marketing cost 2026](https://bloxg.com/how-much-does-roblox-marketing-cost)

## Paper Plane Toss results
### Day 1 (2026-10-04, campaign still "Learning")
| Creative | Spent | Impressions | Click rate | Clicks |
|---|---|---|---|---|
| NOOB → PRO | $2.63 | 45,900 | 0.5% | 219 |
| HOW FAR? | $2.48 | 45,017 | 0.5% | 208 |

- **Reach is cheap:** about $0.012 per click.
- **Click rate is half the 1% target.** Both creatives get the same click rate, which suggests players see them as the same idea: the same noob, sky and blocky grass.
- **Plan:**
  - Keep the budget flat until learning ends (about Wednesday).
  - Get cost per play, D1 retention and session time.
  - Add 1–2 creatives with a different idea (a big distance number, pets + Taco Jet, ghost racing), using the real pastel island look.
  - Scale only after a creative reaches 1%+.

### Day 2 (2026-10-05): "GHOST RACE" creative
| Creative | Spent | Impressions | Click rate | Clicks |
|---|---|---|---|---|
| **GHOST RACE** (ChatGPT, added a few hours earlier) | $1.28 | 9,732 | **2%** | 191 |
| NOOB → PRO | $3.04 | 51,287 | 0.5% | 241 |
| HOW FAR? | $3.09 | 53,640 | 0.5% | 246 |

- **About 4× the click rate, at half the cost per click.** At 0.5% it would have got ~49 clicks, not 191, so this isn't luck.
- **Why it works:**
  - The paper plane is the hero, with no noob avatar.
  - It uses the game's real pastel sky and clouds.
  - A 2-word hook about what makes the game different (ghost racing).
  - Clean and readable at phone size.
- **Next:** 3 more in the same style with different hooks ("+1 BOUNCE!", "FLY FAR!", "SKY PETS!"). Pause the two 0.5% creatives once the new ones have ~5K impressions each.
- **Lesson:** test *different ideas*, not variations of one idea. Show the real game's look and its unique hook, not a generic avatar.

### Day 3 (2026-10-05)
- **Ghost Race:** 2.7% click rate over 20,048 impressions ($5.50).
- **New creatives, hours old and too small to judge:** Sky Pets 2.8% (143 impressions), Fly Far 2.6% (234), +1 Bounce 1.8% (607).
- **Old creatives paused** at 0.5%.
- **Why the old ones show more impressions:** they're lifetime totals, and the old ones ran alone for about a day and a half. New creatives start with a small test batch, and auto-bidding then moves spend toward the best click rate. Ghost Race already outspends each old one.
- **Rule:** judge a creative at 3–5K impressions, not at a few hundred.
- **"Plays" still shows "—"** while learning. Check it after learning ends.

Related: [[Paper Plane Toss Release Prep]], [[Paper Plane Toss Thumbnails and Game Icon]]
