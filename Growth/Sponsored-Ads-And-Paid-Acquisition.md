---
tags: [growth/ads]
status: draft
updated: 2026-10-04
confidence: medium
---
# Sponsored Ads and Paid Acquisition (Roblox Ads Manager)

## TL;DR
- **Ads buy reach, not rank.** Ad-acquired players are **excluded from RFY ranking signals** (official). Use ads to (a) seed the *retrieval* pool at launch or after an update, (b) test thumbnails quickly, and (c) make money directly via the **Earnings/ROAS** objective once monetisation is proven.
- **Don't advertise until D1 retention and the first session are fixed.** Paying for players who bounce wastes money and teaches you nothing. Gate: D1 ≥ genre benchmark, first-play bounce at or below benchmark, and payer conversion > 0 measured on organic traffic. See [[Growth-Metrics-And-Benchmarks]].
- Campaign = **Goal** (Plays / Earnings (limited) / Engagement) + **Audience** (All / New / Recent ≥10k / Lapsed ≥20k) + targeting (location, age, gender, genre, device) + daily or lifetime budget + **≤10 creatives**. Auto-bidding, second-price auction. Ads show on Home *and* Search automatically.
- Money: **1 ad credit = US$1**. Credits can be bought by card (18+) or converted from Robux at **263 Robux per credit** (since RDC 2025; was 285). Conversion is irreversible. Unused campaign credits are refunded.
- Measure by **CPP (cost per play)** for Plays campaigns and **ROAS** for Earnings campaigns. Attribution windows: new users 30 days, resurrected 7 or 30 days. Data lags up to 48 h. Roblox's own 2026 incrementality studies found a **median +14% incremental play sessions** and **+10% D7 retained users** for exposed users.
- **Clones can't buy traffic**: non-unique games may get "no ad spend and no conversions" (official).

## Details

### Products (official, 2026-10)
| Product | Where | Notes |
|---|---|---|
| **Sponsored games** | "Sponsored" tiles on Home, blended through RFY and labelled | Main product. Plays/Earnings/Engagement goals |
| **Search ads** | Top of search results; after the exact-match hero tile | Up to 10 exact-match keywords per Ad Set. Relevance-adjusted auction. **No audience targeting** (all regions, 13+, all devices). Reported combined with Sponsored in acquisition analytics |
| **Portal ads / immersive ads** | Inside other games' ad units | Shows as "Portal ads" source |
| **Rewarded video ads** | *Monetisation* inside your own game, not acquisition | See below |
| Sponsored items | Marketplace | UGC only |

### Campaign settings
| Setting | Options / rules |
|---|---|
| Goal | **Plays**: broad reach, "help recommendation systems learn… qualify your game for RFY". **Earnings** (limited beta May 2026, about 30k games eligible by Oct 2026): players likely to spend, measured by ROAS. **Engagement**: age-checked highly engaged players, for reaching the Kids & Select threshold. Higher CPP; doesn't auto-pause. |
| Audience | All · **New** (never played, or 180+ days ago) · **Recent** (played ≤30 d; needs ≥10,000 recent players) · **Lapsed** (30–180 d; needs ≥20,000 lapsed) |
| Advanced targeting | Location, age, gender, genre, device type |
| Budget | Daily or lifetime. Payment method is fixed after publishing. Auto-reload buys 1 day of credits. Unused credits refunded at the end |
| Creatives | ≤10 thumbnails at 16:9, evenly rotated, toggle any time. "AI generate" makes 3 variants. Asset library (moderation ≤48 h) |
| Editable after publishing | Name, budget amount, schedule, creatives. **Fixed**: goal, audience, budget type |
| Join options | Start place plus **LaunchData**, read via `player:GetJoinData().LaunchData` → ad-only onboarding/reward. Launch data is visible and shareable. |
| Moderation | Target ≤24 h. Cancel up to 6 h before start for a full refund |
| Learning | The first 24 h is the "Learning" status. Don't judge or edit during it |
| Fraud | Invalid traffic analysed 14 d after the end; refunds applied 16 d after the end |
| Billing (card) | $5 charge on first submit; threshold billing (e.g. charged at $100) or monthly |

### Attribution (official)
| Reporting view | Credit rule |
|---|---|
| New Users | All plays and earnings for **30 days** after the first ad join |
| Recent Users (<7 d since last play) | Only the session started by the ad click |
| Resurrected (7–29 d) | **7 days** after return |
| Resurrected (30 d+) | **30 days** after return |

### What it costs (no official rate card; ranges are community data, treat as indicative)
| Metric | Reported range | Source / date |
|---|---|---|
| CPP (Plays), small/mid games | ~0.009–0.011 credits (~$0.01) per play after the 2024 migration, vs ~0.004 earlier | DevForum "Sponsored Experiences moving to Ads Manager" thread, 2024–25 ⚠️ verify |
| CPP blended "benchmark" | ~$0.45 average per play | bloxg.com "Roblox Advertising Benchmarks 2026" (third-party, 850+ games) ⚠️ verify: methodology unknown, conflicts with the forum data |
| Cost per visit | 4–12 Robux (~$0.015–0.046 at 263 R$ per credit) | rowatcher.com 2026 ⚠️ verify |
| Min. bid (old Ads Manager) | 0.01 credit per play | DevForum 2024 ⚠️ verify: manual bids replaced by auto-bidding |
| Engagement goal | Higher CPP than Plays (official, no number) | Ads Manager docs |

**Decision math (use your own numbers):** break-even CPP = **30-day revenue per new user (USD at DevEx rate)**. From Acquisition analytics, 30D revenue per user (Robux) × DevEx rate (⚠️ verify: current DevEx rate in the `Monetisation/` notes) gives USD per user. If CPP < that value, ads pay back within 30 days. "Earnings" campaigns show ROAS directly. Roblox reported that roughly 2 of 3 games that reinvested saw positive returns (RDC 2026 recap).
Remember the second-order effect: ads also lift Creator Rewards and push CCU into Charts. Ad users do **not** improve RFY ranking.

### When ads are worth it vs not
| Situation | Do ads? | How |
|---|---|---|
| Pre-launch / soft launch, need data | **Yes, small** | Plays goal, $20–50/day for 3–5 days, target core country and age. Read D1 and bounce on the ad cohort as a proxy ⚠️ verify the budget heuristic |
| Launch or update day, seeding retrieval | **Yes** | Plays, New Players, 2–5 days. Stack with influencers and socials to hit Charts sorts |
| D1 below benchmark / high bounce | **No** | Fix [[Onboarding-And-First-60-Seconds]] first |
| Proven monetisation (30D ARPU > CPP) | **Yes, scale** | Earnings goal (if eligible), scale +20–30% per day while ROAS holds |
| Big lapsed base after an update | **Yes** | Lapsed audience (needs ≥20k), LaunchData "welcome back" gift |
| Clone or reskin | **No** | Ads may not even spend |
| Reaching Kids & Select threshold (250 highly engaged players since 2026-08-19) | Optional | Engagement goal with a separate budget; pause manually |

### Search ads tactics
- Bid on your **genre nouns plus your own brand** (defend it). Bidding on unrelated hot terms ("obby" for a horror game) is down-weighted by the relevance score.
- Use one keyword per Ad Set to measure per-keyword performance (no keyword-level reporting otherwise).

### Rewarded video ads (monetisation, for completeness)
- Full-screen, 6–30 s, opt-in. The reward **must be a developer product** (not Robux, not randomised). Roblox recommends rewards worth **3–10 Robux**.
- Eligibility: 13+, **ID-verified**, public game with **≥2,000 unique monthly visitors**. Opened to all ads-eligible creators in late 2025.
- Earnings = EPM × impressions. Place in lobbies or natural breaks with a 1–2-click prompt ("Watch for 2× coins"). Pause damage while the ad plays.
- API: `AdService:GetAdAvailabilityNowAsync(Enum.AdFormat.RewardedVideo)` (client) → `AdService:CreateAdRewardFromDevProductId` + `ShowRewardedVideoAdAsync` (server) → grant in `ProcessReceipt`.

### Launch-data hook (ServerScriptService)
```lua
--!strict
-- ServerScriptService/AdJoinHandler.server.lua
-- Tags players who joined via an Ads Manager campaign or share link that sets LaunchData.
local Players = game:GetService("Players")

local AD_TAGS: {[string]: string} = {
	ad_launch_new = "NewPlayerAd",
	ad_lapsed = "LapsedAd",
}

local function onPlayerAdded(player: Player)
	local joinData = player:GetJoinData()
	local launchData = joinData.LaunchData
	if typeof(launchData) == "string" and AD_TAGS[launchData] then
		player:SetAttribute("AcqSource", AD_TAGS[launchData])
		-- e.g. fire an analytics custom event and grant a small cosmetic welcome gift
	end
end

Players.PlayerAdded:Connect(onPlayerAdded)
```

## Checklist
- [ ] D1, bounce and payer conversion measured on organic traffic first.
- [ ] Ad account in the **group** (if the game is group-owned); permissions set.
- [ ] 4–10 creatives (reuse personalization winners) plus one honest gameplay variant.
- [ ] LaunchData per campaign wired to analytics ([[Analytics-And-Instrumentation]]).
- [ ] Don't touch the campaign for the first 24 h (Learning).
- [ ] Judge Plays on CPP and the D1 of the ad cohort. Judge Earnings on ROAS after the attribution window closes (up to 30 d).
- [ ] Expect a dip in RFY impressions during and after campaigns. Compare **total** new users.

## Pitfalls
- Using ads to "fix" a weak algorithm placement. The ranking ignores ad users.
- Converting Robux to credits without needing to (irreversible).
- Reading All Users ROAS for a resurrection campaign. Switch to the Resurrected view.
- Editing mid-learning or spreading a tiny budget over too many audiences.
- Mismatched creatives (exciting art, dull game) give cheap clicks and expensive bounces.

## Related
- [[Growth/_Index]] · [[Discovery-Algorithm]] · [[Launch-Checklist]] · [[Growth-Metrics-And-Benchmarks]] · [[Influencer-Coverage]]
- [[Analytics-And-Instrumentation]] · [[AB-Testing]] · [[Onboarding-And-First-60-Seconds]]

## Sources
- Roblox Creator Docs, *Ads Manager*: https://create.roblox.com/docs/production/promotion/ads-manager (GitHub mirror 2026-10-02)
- Roblox Creator Docs, *Search ads*: https://create.roblox.com/docs/production/promotion/search-ads
- Roblox Creator Docs, *Advertise on Roblox*: https://create.roblox.com/docs/production/promotion/advertise-on-roblox
- Roblox Creator Docs, *Rewarded video ads*: https://create.roblox.com/docs/production/promotion/rewarded-video-ads
- Roblox Creator Docs, *Discovery FAQ* (ads vs RFY): https://create.roblox.com/docs/discovery-faq
- DevForum, "Ads for Creators: RDC Recap and What's Next" (2025-09; 263 R$/credit): https://devforum.roblox.com/t/3929106
- DevForum, "Ads Manager RDC Recap: Earnings, ROAS Reporting, & Incrementality" (2026-10-02): https://devforum.roblox.com/t/4909790
- DevForum, "Rewarded Video ads are now available to all ads eligible creators" (2025): https://devforum.roblox.com/t/4063278
- DevForum, "Highly Engaged Player Threshold Drops to 250" (2026-08-19): https://devforum.roblox.com/t/4820164
- DevForum, "Sponsored Experiences moving to Ads Manager" (community CPP reports): https://devforum.roblox.com/t/2661756
- Third-party: https://bloxg.com/statistics/roblox-advertising-benchmarks ; https://rowatcher.com/news/roblox-ads-in-2026-the-break-even-math-small-devs-ignore
