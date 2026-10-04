---
tags: [growth/store-page, visuals/marketing]
status: draft
updated: 2026-10-04
confidence: medium
---
# Thumbnails and Icons

## TL;DR
- **Icon (512×512, square)** is the brand mark. It appears in most Home sorts, Continue Playing, search and the friend list, and is often shown at about 150×150. **Thumbnail (16:9, 1920×1080)** is the scene. It appears in Home's large tiles, Sponsored tiles and the top of the details page. Design both to be read at phone size.
- Turn on **thumbnail personalization** and keep **2–5 thumbnails active** at all times. Roblox reported **+8.5% average QPTR** in testing (some games +50%), and over 8,000 games were using it by Feb 2025 with about **+12% avg** QPTR. Always include your current winner when starting a new test.
- Click-through only counts if players stay. Since June 2026, RFY ranks on **play-through rate plus first-play bounce rate**, so a misleading thumbnail costs you twice. The rule is "true and exciting": show real gameplay, the real hook and real characters.
- Small-size rules: **1 focal subject, ≤3 colours dominant, strong value contrast, a big readable face or emotion, ≤3 words of text (or none on the icon)**, and nothing important in the **bottom strip** (player-count overlay).
- Refresh the thumbnail set **with every major update**. Roblox recommends leaving the set stable between updates; this is guidance, not a prohibition on correcting inaccurate assets. Upload an **authentic gameplay video**: it autoplays on Home hover/scroll (2026) and plays first on the details page.

## Details

### Roles and specs (official, create.roblox.com docs, 2026-10)
| Asset | Spec | Where shown | Limits |
|---|---|---|---|
| **Icon** | Square, ≥512×512; preview at 150×150 | Most Home sorts, search, Continue, Charts, friend activity | 1 per locale; moderated |
| **Home-page thumbnails** | 16:9, ideally 1920×1080, <3 MB for personalization uploads; jpg/gif/png/tga/bmp | Home large tiles; personalised per user | 2–5 active for personalization |
| **Details-page media** | Up to **10** images/videos | Details page carousel | Free |
| **Video** | Authentic gameplay | First on details page; can show on Home | **3 uploads/month quota**; rejected videos still count; not shown on Xbox/PlayStation/VR |
| **Ad creatives** | 16:9, up to 10 per campaign; AI-generate gives 3 variants | Sponsored tiles and search ads | Moderated (~24–48 h) |

### Thumbnail personalization (official)
- Starts when **≥2** thumbnails are active (Home Page tab → Edit active thumbnails → 2–5 → Start).
- It explores randomly per user group, then sends most traffic to each group's winner while keeping minimal exploration traffic.
- The table shows Impressions, Qualified Plays, Avg Playtime, **QPTR** and Winning Segment, and populates "after a few hours".
- **2025 update ("remembers winners")**: a new test that includes the existing winner keeps most traffic on that winner, while challengers get enough impressions to be measured. Roblox reported +0.19% QPTR and 21% fewer impressions wasted on losers. **Always include the incumbent winner.**
- Roblox advice: keep multiple active rather than choosing one winner, because preferences drift and a loser can become #2 later. Test new sets at each major update, then leave them alone until the next one.
- **Verified 2026-10-04:** the live Thumbnails documentation still names QPTR as the personalization objective. Do not infer thumbnail allocation changes from Home ranking changes; these are different systems. This check does not verify every historical statistic or policy claim in this note.

### Video policy (official, rejected if broken)
| Allowed | Not allowed |
|---|---|
| Cinematic camera (Studio freecam: **Left Shift+P** in solo playtest) | Mechanics, UI or genre not in the game |
| Minor colour/contrast; logo overlay | Graphics enhanced beyond in-game reality |
| Highlight-reel cuts of real gameplay | Real-life footage or external content |
| In-game UI text; Roblox catalog music | Voice-over, narration, voice chat, **music with lyrics** |
| Sparse descriptive overlay ("Collect coins to boost jumps") | Ads or claims ("50% off", "Free UGC!") |

### Design rules for small sizes (practitioner consensus plus Roblox guidance)
| Rule | Why / how |
|---|---|
| **One focal point** | The tile is seen for <1 s while scrolling. One hero character or object, not a collage. |
| **Readable at 150 px (icon) / ~300 px wide (thumbnail on phone)** | Test by downscaling. If you cannot tell the genre, redo it. |
| **Faces with exaggerated emotion** | Shock, joy and fear read at tiny sizes. Use a Roblox avatar or game character, looking toward the action or at the camera. |
| **Value contrast first, hue second** | Dark subject on light background or the reverse. Add a rim light or outline (white or black 4–8 px stroke) to separate the subject from the background. |
| **Saturated, genre-coded palette** | Bright and high saturation for fantasy/simulator; muted for somber; heavy contrast for horror (official examples). Match [[Art-Direction]]. |
| **Text: 0 words on the icon, ≤3 big words on the thumbnail** | Text must survive localisation and size. Never use "FREE", "ROBUX", "GIVEAWAY" (giveaway-led metadata gets reduced exposure). Update badges ("NEW WORLD!") are fine if true. |
| **Keep bottom clear** | Metadata can obscure essential elements. A 15% margin is a design heuristic, not a documented platform safe area; inspect actual previews. |
| **Stand out from the sort's neighbours** | Look at the current Home and Charts row for your genre. If everyone uses yellow, use blue. Unique imagery is also an official requirement (copied visuals trigger "non-unique" de-prioritisation). |
| **Icon consistency for brand** | Keep a recognisable icon character or logo across updates so returning users find you in Continue. Swap seasonal variants (Halloween hat, etc.). |
| **Deliver the promise early (recommendation)** | Introduce the advertised hook early. Progression imagery need not be reachable within one minute; avoid implying immediate access when it requires progression. See [[Onboarding-And-First-60-Seconds]]. |

### Iteration process (repeat each major update)
1. **Brief**: the update's hook in one sentence, and the target segment (new players vs returning).
2. **Produce 4–5 variants** that differ by *concept* (character vs environment vs action moment vs social/group shot), not small tweaks. Use real in-game renders plus paint-over. Keep it honest.
3. **Downscale test**: 150 px icon / 320 px thumbnail; glance test with 3–5 target-age testers.
4. **Choose a stable review window before activation**, including comparable traffic periods. The inspected Thumbnails page specifies neither a universal minimum sample nor test duration. Treat 1,000 impressions and 3–7 days as unvalidated planning guesses, never significance thresholds. Choose evidence requirements around baseline rate, useful effect size and available traffic; see [[AB-Testing]].
5. **Read QPTR and Avg Playtime together.** QPTR uses Home recommendation qualified plays divided by impressions; Avg Playtime is minutes per qualified play. Low playtime is a diagnostic clue, not proof of mis-selling. Investigate expectation mismatch, audience mix, loading failures and onboarding. This conditional average does not describe every joining player.
6. **Review before retiring a variant.** Adaptive allocation and different audiences make aggregate differences insufficient evidence of causal creative lift. Preserve potentially useful segment coverage; if evidence is sparse, record inconclusive instead of naming a loser. Recommendation: retire inaccurate assets promptly and document the intervention.
7. Treat reuse in paid ads as a separate hypothesis: paid CTR cannot establish a Home QPTR winner. Keep placement, audience, attribution and metric definitions separate. See [[Sponsored-Ads-And-Paid-Acquisition]] and [[Roblox Acquisition Experiments and Ad Measurement]].
8. Log the results in the project notes. For general method see [[AB-Testing]].

### Policy limits
- Everything is moderated against Community Standards. Uploading thousands of near-duplicate assets or copying another game's art reduces discoverability.
- **Reusing your own old thumbnails or icons is explicitly fine** (Discovery FAQ).
- No misleading imagery (mismatched metadata gets reduced exposure). Example from the docs: a dinosaur thumbnail on an obby with no dinosaurs.
- Content shown must fit the game's maturity label. See also the content-maturity docs.

### Evidence acceptance checks (maintenance procedure, 2026-10-04)
These are proposed checks, not completed analytics tests. No Creator Hub account data, campaign or player experiment was accessed in this pass.
- [ ] Record asset IDs, build/version, active set, dates/timezone and concurrent game or acquisition changes.
- [ ] Preserve counts and metric definitions alongside rates; distinguish new/returning audiences where the report supports them.
- [ ] Record whether the decision is an operational choice, an association or a causal experiment result. Do not claim incremental lift from adaptive aggregate rankings alone.
- [ ] Record low-traffic results as inconclusive, with the next review condition; do not manufacture a universal success threshold.
- [ ] Check the advertised gameplay against the actual build and phone previews. Link evidence and record remaining corrections.

## Checklist
- [ ] Icon 512×512, readable at 150 px, no text or one short logo word, unique silhouette.
- [ ] 4–5 home thumbnails at 1920×1080, <3 MB, with essential elements clear of overlays in actual previews.
- [ ] Personalization started; incumbent winner included.
- [ ] Authentic gameplay video uploaded (no voice, no lyrics, no claims).
- [ ] Details page: 5–10 media items covering core loop, social, progression and update.
- [ ] Alt text added to thumbnails (accessibility).
- [ ] Seasonal icon variant scheduled for the next event.

## Pitfalls
- "Clickbait" (fake features, Robux imagery). High CTR becomes high bounce, which lowers RFY impressions and risks reduced-exposure status.
- Choosing one "winner" and deactivating the rest. You lose adaptation to segment and seasonal shifts.
- Restarting tests mid-update cycle or every day. The data never settles.
- Using AI-generated art that looks nothing like the game. This breaks the "authentic" rule and causes bounce.
- Using AI-generated art at all is now a reputational risk: on X, posts rejecting AI thumbnails reach 46k+ likes, and studios advertise "artists contractually bound not to use generative AI" (captured 2026-10-04 in [[X-Thumbnails-And-Icons]]). This is community sentiment, not measured CTR. Test against in-engine renders or human art.
- Spending the video quota (3/month) on uploads that get rejected.

## Related
- [[Growth/_Index]] · [[Discovery-Algorithm]] · [[Titles-Descriptions-And-Tags]] · [[Growth-Metrics-And-Benchmarks]]
- [[Art-Direction]] · [[AB-Testing]] · [[Onboarding-And-First-60-Seconds]] · [[Sponsored-Ads-And-Paid-Acquisition]]

## Sources
- Roblox Creator Docs, *Thumbnails*: https://create.roblox.com/docs/production/publishing/thumbnails (live page inspected 2026-10-04: personalization objective, metric definitions, update guidance and overlay placement; other sections not fully reverified)
- Roblox Creator Docs, *Icons*: https://create.roblox.com/docs/production/publishing/experience-icons (2026-10-02)
- Roblox Creator Docs, *Discovery* and *Discovery FAQ* (reuse of thumbnails; reduced exposure): https://create.roblox.com/docs/discovery
- DevForum, "[Live now] Personalize your thumbnails to attract more users" (2024-11): https://devforum.roblox.com/t/3257233
- DevForum, "Thumbnail personalization now remembers your existing winning thumbnails" (2025): https://devforum.roblox.com/t/3793665
- Bloxy News on X (2025-02-13): "over 8,000 experiences… average lift of +12% qPTR": https://x.com/Bloxy_News/status/1890113378766704674
- DevForum, "How we are improving Home this year" (2026, video autoplay): https://devforum.roblox.com/t/4502571
