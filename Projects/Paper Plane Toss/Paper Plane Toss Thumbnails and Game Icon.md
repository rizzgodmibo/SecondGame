---
title: Paper Plane Toss Thumbnails and Game Icon
date: 2026-10-03
tags: [roblox, thumbnails, icon, marketing, research, art]
source: codex
project: Paper Plane Toss
status: draft
updated: 2026-10-04
confidence: medium
---
# Paper Plane Toss Thumbnails and Game Icon

## TL;DR

- **v8 winner-style variants:** +1 BOUNCE!, FLY FAR!, SKY PETS! made from Holden's exact Ghost Race reference. Final exports are exactly 1920×1080; upload JPGs are under 0.5 MB. Screenshot now shows Ghost Race at 2% CTR versus 0.5% for the older two; different traffic/time windows remain unknown.
- Additional campaign candidates **v7**: Ghost Race and Plus One Bounce, created 2026-10-04. Existing campaign creatives were not changed; Ads Manager was inaccessible from this browser. Files are ready for manual addition to the same campaign.
- Latest candidates are **Refined v6**, made 2026-10-04 from Holden's exact three pastel attachments and two new rendered Roblox style references. Earlier versions below are history.
- Keep the white starter plane and +1 on the icon; gold/red star plane on the banners; smooth pastel islands and the cloud lane throughout.
- Improve expression, pose, lighting, silhouette and flight-path clarity together. A material polish pass alone does not create stronger storytelling.
- Public competitor artwork supplies composition observations, not evidence that any creative choice increases conversion. No live asset upload or analytics experiment occurred.
- ⚠️ **Risk flagged 2026-10-04 (observation, not a decision):** the v1–v6 candidates come from ChatGPT image generation. On X, anti-AI-thumbnail sentiment is strong: the most-liked post in the [[X-Thumbnails-And-Icons]] capture (46.5k likes) says players won't play games with AI thumbnails, and people call out AI thumbnails in replies. That audience is mostly devs and older players and it isn't player conversion data. Options for Holden: (a) keep the AI candidates but A/B test them against an in-engine Roblox render or a human-painted version, (b) commission an artist, (c) re-stage the composition as a real in-engine render in Studio/Blender. Holden decides.
- Current +1 and +10K claims match Starter and GoldenTicket Glide per bounce in local Config.luau, checked 2026-10-04. Recheck after balancing.

## Ghost Race winner-style variants v8 (2026-10-04)

Holden identified Ghost Race as his best-performing creative and requested three close style variants. Used his exact reference as the primary image input for all three. Kept white/cyan folded plane, yellow rim, white/gold tilted chunky title with plum outline, bright blue sky, soft clouds and smooth pastel islands. Removed rival planes for these three hooks.

![[Paper Plane Toss Plus One Bounce v8.png|640]]
![[Paper Plane Toss Fly Far v8.png|640]]
![[Paper Plane Toss Sky Pets v8.png|640]]

- **+1 BOUNCE!:** three cloud contacts, three gold +1 labels and dotted gold bounce arcs; up-right white plane.
- **FLY FAR!:** long cloud road/rainbow arches and exact requested distance text 1,000,000 M. Distance reachability was not verified in this task; illustration is not evidence of a reachable distance.
- **SKY PETS!:** baby dragon and winged bunny perched on the plane as explicitly requested. Actual StormDragon and CloudBunny UI renders supplied as supporting references. Riding and tiny bunny wings are requested promotional staging, not verified live behavior; existing pet notes describe followers. No gameplay changes were made.
- Resolved contradictory wording by treating the specifically requested +1 bonus labels and distance number as exceptions to the general 'no other text besides title' rule. No unrelated text/UI was added.

### New screenshot evidence

![[Paper Plane Toss Ghost Race Results October 4.png|640]]

| Creative | Spend shown | Impressions | Clicks | Displayed CTR |
| --- | --- | --- | --- | --- |
| Ghost Race | USD 1.28 | 9,732 | 191 | 2% |
| Noob Pro | USD 3.04 | 51,287 | 241 | 0.5% |
| How Far | USD 3.09 | 53,640 | 246 | 0.5% |

All rows show Learning. This supports the user's observed CTR lead for Ghost Race; it does not isolate the style's causal effect or establish retention/paid-play quality. Screenshot received 2026-10-04; reporting range and traffic composition unseen. Preserve this newer evidence alongside the earlier baseline, not as a replacement for it.

### Deliverables and QA

`C:\Users\holde\Downloads\SecondGame\art\thumbnails\winner-v8\` contains final `Plus One Bounce`, `Fly Far`, and `Sky Pets` in PNG and JPG, native images, 320×180 phone-size previews and `Prompts.md`.

- Built-in image_gen created/edited all artwork; high-quality bicubic export resampled the native 1672×941 results to the requested exact 1920×1080. Native originals preserved.
- Final JPG bytes: Bounce 395,797; Fly Far 467,617; Sky Pets 426,657. Use these upload copies; full-resolution PNGs exceed 3 MB.
- Inspected all three 320×180 previews: titles, principal plane and pet silhouettes remain distinguishable; number has correct digits, three +1 labels present. Bottom-right carries background rather than faces/title. Actual platform-specific crop/overlay still requires upload-preview review.
- No campaign changes or uploads requested/performed this turn. New variants have no measured CTR yet.
- Exact prompts/provenance archived as `Assets/Paper Plane Toss Winner v8 Prompts.txt`.

Related: [[Paper Plane Toss Pets and Eggs]], [[Thumbnails-And-Icons]], [[AB-Testing]], [[Sky Island Hub and Throw Lane]].

## Additional campaign ideas v7 (2026-10-04)

Holden requested 1–2 distinct concepts alongside the existing campaign creatives, keeping the game's pastel look, one main subject and at most three words of headline text. Created two candidates using built-in image_gen; preserved all existing images.

### Ghost Race

![[Paper Plane Toss Ghost Race v7.png|640]]

- Competition concept: one opaque white/cyan starter plane with yellow outline, flanked by two quieter translucent replay planes, over the real-style cloud lane. Two-word headline: GHOST RACE.
- Verified in current local `src/client/Controllers/GhostController.luau`: recent/server-best flights replay in side lanes; Config specifies ghost transparency 0.6. This is promotional illustration of an implemented local feature, not a screenshot or a fresh live-server test.
- One clear hero plane; supporting rivals stay smaller. Actual lane render supplied as environment reference. No finish-line rewards or controllable aircraft mechanics invented.

### Plus One Bounce

![[Paper Plane Toss Plus One Bounce v7.png|640]]

- Numeric progression concept: one large white paper plane and a connected three-cloud bounce path, with exactly three +1 labels increasing in perspective size. No headline or avatar competes with the plane.
- Starter +1 Glide per bounce checked in current local Config.luau. Chose this suggested option instead of an unverified 1,000,000-metre claim. Pet/Taco Jet remains a possible later concept; no pet-riding feature was assumed.
- Both new images retain organic pastel grass islands, rounded foliage, beige undersides and cloud lane/rainbow scenery. They offer different creative hypotheses, not a promise of higher CTR.

### Screenshot baseline and campaign status

![[Paper Plane Toss Campaign Baseline October 4.png|640]]

User-supplied screenshot, received 2026-10-04; reporting date range, campaign ID, audience and spend window are not visible:

| Existing creative | Status | Spend shown | Impressions | Clicks | Displayed CTR |
| --- | --- | --- | --- | --- | --- |
| Noob Pro | Learning, enabled | USD 2.63 | 45,900 | 219 | 0.5% |
| How Far | Learning, enabled | USD 2.48 | 45,017 | 208 | 0.5% |

These rounded rates do not establish a winner. Neither the screenshot nor public reference artwork proves that large numbers or collecting imagery improve conversion. Record new creative activation times, counts, plays and retention context before comparing results; paid CTR and organic Home personalization QPTR are different metrics. See [[Thumbnails-And-Icons]] and [[AB-Testing]].

**Platform check:** live Ads Manager documentation states up to 10 thumbnails per campaign, creatives editable after publication, and independent enable/disable controls. Checked 2026-10-04; source at bottom. Two existing plus two new would make four, provided the unseen campaign has no additional creatives.

**Execution limitation:** navigation to `https://ads.roblox.com` was blocked by the browser (ERR_BLOCKED_BY_CLIENT). No campaign ID, live controls, uploads or mutations were accessible. No attempt was made to bypass the block. The two new files are prepared; they have **not** been added or activated. Existing creatives, budget and schedule were not touched. To finish: edit that same campaign's Creatives, add these two files, keep the existing two enabled, and preserve budget/schedule.

### Saved files and checks

Workspace: `C:\Users\holde\Downloads\SecondGame\art\thumbnails\campaign-v7\`.

- `Ghost Race.png`: 1672×941, 1,843,861 bytes.
- `Plus One Bounce.png`: 1672×941, 1,744,105 bytes.
- `Prompts.md`: exact prompts, inputs and publication limitation. Vault artifact copy: `Assets/Paper Plane Toss Campaign v7 Prompts.txt`.

Dimensions/file sizes verified from PNG headers; approximately 16:9, not exact 1920×1080 exports. Outputs visually inspected for ghost count, lettering, plane silhouette, cloud contacts and terrain. Actual phone/Ads Manager preview and campaign performance remain untested.

Related: [[Deterministic Flight Sim and Ghosts]], [[Paper Plane Toss Pets and Eggs]], [[Sky Island Hub and Throw Lane]].

## Refined v6 with new rendering references (2026-10-04)

**User direction:** Holden likes the existing pastel style but requested further refinement using two supplied sled/treasure artworks and other large Roblox games. The references inform expressive faces, depth, lighting and framing; their literal snow, coins, gems, sleds and treasure mechanics do not belong in Paper Plane Toss. Approval of the direction is not approval of these new outputs.

### Before and after

| Asset | Exact supplied before | Refined v6 candidate |
| --- | --- | --- |
| Square icon | ![[Paper Plane Toss Icon v6 Before.png]] | ![[Paper Plane Toss Icon Refined v6.png]] |
| How Far | ![[Paper Plane Toss How Far v6 Before.png]] | ![[Paper Plane Toss How Far Refined v6.png]] |
| Noob Pro | ![[Paper Plane Toss Noob Pro v6 Before.png]] | ![[Paper Plane Toss Noob Pro Refined v6.png]] |

### Changes and art judgment

- **Icon:** enlarged expressive face and stronger leaning throw; reduced cliff area; one large +1; preserved white/cyan paper folds and one prominent cloud contact. White edge contours and warm hair highlights separate the avatar from blue sky. This preserves the gameplay focus of the chosen icon instead of returning to the previously rejected isolated gold-plane concept.
- **How Far:** tighter face/torso framing, excited expression, smaller headline footprint, and stronger foreground depth. Gold plane, two cloud contacts and distant rainbow lane remain. The background is still comparatively detailed; it is a visual tradeoff, not a proven optimization.
- **Noob Pro:** worried brows/frown versus confident grin; cleaned rendering and maintained the two real upgrade values. The first generation retained intersecting motion streaks despite the prompt. A localized second edit removed the direct streak bundle and extra pro bounce, leaving a clear hand → cloud → plane route. Preserve the correction rather than the initial generated file.
- **World consistency:** smooth organic green grass, beige low-poly island undersides, rounded green/pink foliage and cloud lane retained. No voxel grass or cube trees were reintroduced. These are promotional illustrations, not screenshots or exact FlightSim traces.
- **Transferable lesson:** borrow the rendering and visual emphasis from a style reference without borrowing its unrelated mechanics. For expressive Roblox art, face decals, camera, form lighting and silhouette are as important as saturated colors.
- **Iteration lesson:** explicitly requesting a connected trajectory is insufficient. Inspect the actual result and use one targeted edit for the defect. Simplifying to one bounce can convey the mechanic better than adding another ambiguous curve.

### Research refreshed for this pass

Official game pages and their actual linked artwork were opened on 2026-10-04. The public artwork served here is only one presentation sample; personalized variants and per-image performance are unknown.

| Reference | Direct observation | Applied lesson |
| --- | --- | --- |
| +1 Stone Skipping | Small throwing avatar, large foreground stone, visible white bounce arcs and +1 labels | Keep the throw/contact/object relationship legible and retain our sky/cloud identity |
| Pet Simulator 99 | Large dark pet with red eyes against a violet burst | Strong silhouette and one primary visual object can carry a tile |
| Grow a Garden | Oversized fruit structure with a smaller avatar | Scale contrast helps communicate the featured object quickly |
| Fisch | Current linked artwork shows a red dragon-like fish beside an excited yellow avatar, rod, balloons and confetti | Character reaction and object scale create a clear story; do not import the creature or celebration into this game |
| Holden's two new attachments | Close expressive bacon avatar, large overlapping objects, clean white contours, shaped highlights and strong depth | Apply expressive decals and dimensional rendering while retaining paper-plane gameplay |

**Verified platform facts:** Roblox recommends square icons at least 512×512 and checking readability around 150×150. Thumbnail guidance recommends 16:9, ideally 1920×1080; personalization upload instructions specify under 3 MB. Relevant imagery should communicate what players can expect. Sources below, checked 2026-10-04. These constraints do not establish a winning composition.

### Files and inspection

Workspace: `C:\Users\holde\Downloads\SecondGame\art\thumbnails\refined-v6\`.

| Final file | Verified dimensions | Verified bytes |
| --- | --- | --- |
| Game Icon After.png | 1254×1254 | 1,985,198 |
| How Far After.png | 1672×941 | 2,148,661 |
| Noob Pro After.png | 1672×941 | 2,117,214 |

PNG headers and file lengths checked locally. Both banners are approximately 16:9, not exact 1920×1080 exports. All are below 3 MB. Inspected full-size outputs for lettering, paper-plane identity, environment and trail continuity. Actual Creator Hub/mobile previews and conversion testing remain pending; do not describe them as completed.

Matching `Before.png` files preserve exact attachments. `Prompts.md` records all four built-in image_gen edits, including the trajectory repair. `Before and After.md` provides a local comparison. A prompt artifact is preserved in the vault at `Assets/Paper Plane Toss Refined v6 Prompts.txt`. No game code, Studio instances, asset uploads, publication or commits were changed.

**Next:** Holden reviews expressions and framing; inspect actual upload previews at small size before activation. Compare engagement data with a documented baseline after approval, using [[Thumbnails-And-Icons]] and [[AB-Testing]]. No measured uplift or universal sample threshold is claimed.

## Summary

Holden requested substantial improvements to two existing thumbnails, then added a square game icon. Created a coordinated gold, cyan, and navy set using the built-in image_gen tool. The artwork emphasizes a folded paper plane, cloud bounces, and the familiar bacon-haired Roblox avatar. These are review candidates, not measured conversion winners. No upload, publication, or live test was performed in this task.

Related: [[Paper Plane Toss]], [[Paper Plane Toss References and Core Loop]], [[Art Direction Feedback]], [[Blender 3D Logo Pipeline]], [[Sky Island Hub and Throw Lane]], [[Paper Plane Toss Progression Numbers]], [[Roblox Game Development Research]].

## Deliverables

### Progression thumbnail

![[Paper Plane Toss Noob Pro v4.png|640]]

- Preserves the NOOB/PRO contrast, avatar identity, small white starter plane, and gold plane with red accents.
- Enlarges faces and planes, tightens the diagonal split, reduces the field of tiny islands, and replaces rainbow PRO lettering with gold to align with the approved logo.
- Keeps +1 and +10K: verified in `src/shared/Config.luau` as Starter and GoldenTicket `glidePerBounce` values. They are Glide per bounce, not currency or distance. Recheck these claims whenever balancing changes.
- A second edit corrected the disconnected gold trail into a continuous hand → cloud → cloud → plane sequence. The generator's first pass prioritized attractive streaks over causal clarity; explicit trajectory review is necessary.
- Remaining compromise: this is the busiest candidate, and the final flight path doubles back. It reads as progression more immediately than as a precise flight diagram.

### Curiosity thumbnail

![[Paper Plane Toss How Far v4.png|640]]

- Preserves HOW FAR? but makes the gold plane much larger and removes repeated +10K labels.
- Two clearly separated clouds and one connected path make the gameplay easier to read. Floating island undersides establish height; the background is open sky, never water.
- Strongest initial art recommendation: this communicates the distinguishing cloud-bounce mechanic fastest. This is visual judgment, not a prediction of measured qPTR.
- Remaining compromise: the headline still occupies a substantial part of the frame. A future near-textless variant could test whether the action alone is stronger.

### Square game icon v1 — superseded after feedback

![[Paper Plane Toss Game Icon v1.png|300]]

- Purpose-designed square composition, not a crop of either thumbnail.
- One dominant folded gold plane, an expressive avatar face, one bounce cloud, and a tiny distant island. No words, counters, or full logo competing at small size.
- The icon has a somewhat softer rendered finish than the outlined thumbnails. Shared plane design and palette hold the set together; consistency of outlines is a possible future refinement.

### Square game icon v2 — superseded after further feedback

![[Paper Plane Toss Game Icon v2.png|300]]

- Holden said the first icon needed work and supplied discovery-grid screenshots with Steal An Egg, +1 Loot To Forge, +1 Stone Skipping, Build the Pyramid, and Ride A Pet.
- His references emphasize visible Roblox characters performing actions, recognizable game items, and compact progression/reward cues. This is explicit user direction; any popularity counts in the supplied screenshots are not independently verified analytics or proof of effectiveness.
- Rebuilt the composition as a gameplay scene: near-full-body throwing avatar standing on a floating island, white folded starter plane in the foreground, two separated cloud bounces, and two +1 labels. The original oversized gold-plane close-up is retained only as a superseded experiment.
- The +1 labels now specifically match the Starter plane. The white plane and cyan folds distinguish paper from a metal jet; the green island and visible rock underside establish the sky setting.
- Main lesson: branding consistency should not force identical composition across logo, thumbnails, and icon. Holden approved the glossy title but wanted a clearer, more literal Roblox gameplay icon.
- Remaining review: the trail is a stylized perspective diagram, not a simulation trace. The foreground plane is still the strongest shape, while the avatar remains visible. No claim of improved conversion until tested.

### Square game icon v3 — historical review candidate

![[Paper Plane Toss Game Icon v3.png|350]]

Holden explicitly said the two big banners were fine and asked for the square icon to be remade again. The thumbnails were left unchanged. The previous icon was insufficient; simply showing the correct mechanics did not make its composition strong enough.

- Re-examined both user-supplied discovery-grid screenshots alongside v2. Diagnosis: too much empty sky and cliff, avatar too small, plane isolated at the lower-right, weak action grouping.
- Used all three images as image_gen inputs: v2 as the edit target, and the two screenshots as style/composition references only. Requested one square original icon, never a reproduction of the reference grid or UI.
- Enlarged the throwing avatar and moved the plane upward alongside it. Reduced the cliff, added concentrated blue motion rays, and used one prominent yellow +1 to match the visual language of the supplied simulator icons.
- A cleanup pass removed an extra disconnected bounce cloud and its small +1. Final image has one readable hand → foreground cloud → ascending paper plane trajectory. The gain is still the Starter plane's real +1 Glide per bounce.
- White/cyan folded plane, orange-haired black/blue avatar, bright green launch ledge, and deep blue background give separate readable shapes. Keep the aircraft identifiable as folded paper rather than a metallic jet.
- Lesson: a square icon needs a deliberately compressed composition. A logically correct scene can still be weak if the main subject, character, and feedback occupy separate distant areas. Fewer steps shown clearly can communicate more than a sparse multi-bounce diagram.
- User review still pending for v3; no performance data, upload or publication. Do not describe it as approved or a measured improvement.

Workspace output: `C:\Users\holde\Downloads\SecondGame\art\thumbnails\research-v4\Game Icon v3.png`. Built-in image_gen used; both exact prompts saved alongside it in `Icon v3 prompts.md`. Prior versions preserved.

## User-selected set and pastel environment correction (2026-10-03)

Holden supplied the exact icon and two thumbnails he picked and requested an environment-only correction. These selections take precedence over earlier candidate labels in this note. He then requested a before/after comparison of each. The new environment edits are ready for review; the prior layouts were selected, but the edited outputs are not yet separately approved.

### How Far

| Selected before | Pastel environment after |
| --- | --- |
| ![[Paper Plane Toss How Far Selected Before.png]] | ![[Paper Plane Toss How Far Pastel v5.png]] |

### Noob Pro

| Selected before | Pastel environment after |
| --- | --- |
| ![[Paper Plane Toss Noob Pro Selected Before.png]] | ![[Paper Plane Toss Noob Pro Pastel v5.png]] |

### Square icon

| Selected before | Pastel environment after |
| --- | --- |
| ![[Paper Plane Toss Icon Selected Before.png]] | ![[Paper Plane Toss Icon Pastel v5.png]] |

**Exact chosen sources:** `exec-46580d3d-35fe-409c-8267-eddccf72c629.png` (How Far), `exec-04151f56-7b68-4061-8423-7800116406db.png` (Noob Pro), and `ChatGPT Image Oct 3, 2026, 06_57_31 PM.png` (square icon). Used these exact attached files rather than silently substituting the latest generated versions. In particular, the selected icon has both the large and small +1, and the selected Noob Pro has its original trajectories.

**Changes:** Removed cube/stud grass and voxel foliage throughout all three scenes. Used continuous pastel green grass surfaces with organic edges, simple beige faceted island undersides, rounded layered tree canopies with green/pink/peach variation, and hanging vines. Added a quiet distant cloud lane and rainbow arch. Preserved the selected layouts, readable labels, avatars, plane designs, and main action, allowing the minor rendering variation inherent to generative editing. No claim of pixel-identical preservation outside the ground.

**Actual visual references:** Inspected `art/preview_island_34.png` and `art/preview_lane_start.png` and supplied both to every edit. Read [[Sky Island Hub and Throw Lane]] and the AssetLibrary README. The lane reference confirms the game has a continuous low-poly cloud road and rainbow arches. Earlier thumbnail prompts that categorically banned a continuous cloud lane were too restrictive and should not guide future artwork. Keep the foreground bounce contacts clear while allowing the actual lane in the background.

**Lessons:**

- A recognizable simulator composition is insufficient if the terrain promises the wrong visual style. Borrow composition from references while taking materials, foliage, and world shapes from this game.
- Interpret "soft pastel" as clean continuous shapes and controlled colors, not an overall blur or washed-out exposure. Strong sky, lettering, avatar, and plane contrast can coexist with softer ground colors.
- Use the explicitly selected source files as the edit targets. Do not fold in unrelated trajectory repairs or previous revisions during a focused environment pass.
- Check every background island as well as the foreground; leaving distant cube trees would retain the mismatch.
- The supplied art critique's claim that NOOB/PRO is "proven" is not performance evidence for this game. No qPTR or retention uplift was measured here.

**Outputs:** `art/thumbnails/pastel-v5/How Far After.png`, `Noob Pro After.png`, and `Game Icon After.png`. Matching Before files preserve the exact selections. Both banners remain 1672×941 and the square icon remains 1254×1254; all after PNGs are below 3 MB. Built-in image_gen used for each edit; full prompts saved in `art/thumbnails/pastel-v5/Prompts.md`. Before/after comparison is embedded above and shown in chat. No game code, Studio assets, or published discovery media changed.

Related: [[Art Direction Feedback]], [[Sky Island Hub and Throw Lane]], [[Blender to Roblox Asset Pipeline]].

## Evidence and interpretation

- **Published platform evidence:** Roblox reports an average +8.5% qualified play-through-rate improvement during thumbnail-personalization testing, with some games seeing +50%. This measures the personalization system; it does not prove that these images, a NOOB/PRO layout, or gold colors produce that lift.
- **What to measure:** qPTR is qualified plays divided by recommendation impressions. Judge relevant engagement, not clicks alone. Public competitor artwork does not expose its individual qPTR or establish that the artwork caused the game's popularity.
- **Platform guidance:** Roblox recommends relevant imagery, 16:9 thumbnails, ideally 1920×1080, and avoiding essential content along the bottom where metadata can overlap. Its personalization instructions specify files under 3 MB and 2–5 active thumbnails. Keep distinct concepts available rather than treating an early aggregate leader as a universal winner.
- **Icon guidance:** square, at least 512×512; preview at small sizes such as 150×150. The new square master exceeds the minimum resolution. Its simple silhouette is intended to survive reduction, but real-device review is still appropriate.

## Competitor artwork actually inspected

Viewed artwork linked directly from these four official Roblox game pages, at their served 497×280/500×280 size. These are a snapshot of public presentation, not a complete catalog of personalized variants. No private analytics or current player-count ranking was accessed.

- **+1 Stone Skipping:** an avatar, a clearly connected bounce path, and a large foreground stone explain the action without a huge headline. Adaptation: use a large paper plane and visually connected cloud contacts. Preserve Paper Plane Toss's sky setting; do not copy the water scene.
- **Pet Simulator 99:** the inspected image concentrates attention on one large dark pet against a violet burst. Adaptation: one strongly contrasted hero object rather than many equally detailed objects.
- **Grow a Garden:** the inspected image uses an oversized crop and a smaller avatar to make scale immediately visible. Adaptation: show the upgrade contrast through plane size and pose, not only text.
- **Fisch:** a huge blue creature dominates the frame beside a small fishing avatar. Adaptation: stronger perspective and subject scale, while retaining this game's actual paper-plane mechanic. Do not invent monsters for this game.

These observations informed composition; none is evidence of a specific thumbnail's conversion rate. Search also surfaced third-party resellers and unrelated game copies; those were not used as reliable competitor references.

## Reusable production lessons

- Give each asset one primary promise: progression, distance curiosity, or instant plane recognition. Three nearly identical images would provide less creative variety.
- Spend image area on recognizable objects and faces. Distant decorative islands should establish setting, not compete with the plane.
- Gold against cyan/cobalt connects the thumbnails to the approved logo. Navy contours and selective light rims separate the subjects from pale clouds.
- Keep the aircraft unmistakably folded paper: central crease, triangular sheet wings, visible folds, no cockpit, engine, or propeller.
- In prompts, specify every flight-path endpoint and cloud contact. Inspect the result: requested geometry is not guaranteed.
- Foreground sky bounce contacts need clear cloud puffs and open air. Avoid water and splash rings. The real continuous cloud lane is appropriate in the background; the earlier blanket ban on cloud roads was superseded by the game renders.
- Preserve strong identifying features from an existing successful direction rather than replacing everything with generic polish. Here those were the bacon avatar, gold/red plane, airborne islands, and two original hooks.
- Use targeted follow-up edits for a localized defect instead of redesigning the entire image repeatedly.
- Validate dimensions and file sizes from the actual output; image generation may not obey requested pixel dimensions. Never label a native export 1920×1080 without checking.
- Keep original files and earlier candidates. Do not treat generated output or visual preference as a user-approved publication.

## Files and verification

Workspace directory: `C:\Users\holde\Downloads\SecondGame\art\thumbnails\research-v4\`.

- `Noob Pro.png`: 1672×941, 2,128,802 bytes.
- `How Far.png`: 1672×941, 1,970,186 bytes.
- `Game Icon.png`: 1254×1254, 1,909,357 bytes.
- `Game Icon v2.png`: revised square master, current icon candidate; v1 preserved.
- `Prompts.md`: full generation/edit prompts, including the trajectory repair.
- `Preview.html`: local review page displaying thumbnails at 320 pixels and the icon at 150 and 64 pixels. The in-app browser blocked local file navigation, so this page was prepared but not visually verified there. Full-size outputs were inspected.

All PNG signatures/dimensions and file sizes were read locally. Thumbnail masters are approximately 16:9 (rounding differs slightly), not exact 1920×1080 exports. All three are under 3 MB. Original supplied files are unchanged. No game code or Studio instances were edited.

## Proposed measurement plan

After art approval, test the progression and curiosity thumbnails through Roblox personalization. Record impressions, qualified plays, qPTR, and average playtime with dates and update context. Do not declare a winner from tiny samples, confuse segmented allocation with a clean equal-traffic A/B test, or change the icon and onboarding simultaneously when trying to isolate thumbnail effects. Retain comparable baselines and check that the art accurately represents gameplay. No universal sample threshold or guaranteed uplift is claimed here.

## Sources

- V8: Holden's exact winning reference `codex-clipboard-d7a45445-835f-46c1-8ae0-a59c8f65889b.png` and screenshot `codex-clipboard-8679b444-b1d8-4831-94e6-98ff08eb1a7f.png`, supplied 2026-10-04. Local pet references: `art/ui/pet_StormDragon.png` and `art/ui/pet_CloudBunny.png`. Screenshot observations are user-supplied evidence, not independently accessed analytics.
- [Roblox Ads Manager: creative limits, editing and enable/disable controls](https://create.roblox.com/docs/production/promotion/ads-manager), checked 2026-10-04 for v7 campaign additions.
- V7 campaign baseline: Holden's supplied `codex-clipboard-3602b7cc-f7a4-4c89-b44d-4ecdedf64b21.png`, preserved in Assets. Current ghost implementation: `src/client/Controllers/GhostController.luau`; Starter gain and ghost transparency: `src/shared/Config.luau`. Environment source: `art/preview_lane_start.png`.
- Latest targets: `ChatGPT Image Oct 3, 2026, 07_10_11 PM.png`, `exec-1107a03d-ec85-43d3-8f92-8abd8af5445d.png`, and `exec-623f2324-e2ed-463b-9b1b-5336c2663b02.png`, supplied by Holden. Exact copies are embedded in the v6 comparison.
- New rendering references supplied by Holden: ![[Paper Plane Toss v6 Square Style Reference.png|150]] ![[Paper Plane Toss v6 Wide Style Reference.png|280]]. These inform art direction, not verified performance.
- Environment correction references: local game renders `art/preview_island_34.png` and `art/preview_lane_start.png`; [[Sky Island Hub and Throw Lane]]; `C:\Users\holde\Documents\GameDev\AssetLibrary\README.md`; Holden's exact selected attachments named above.

- [Roblox thumbnail guidance and personalization data](https://create.roblox.com/docs/production/publishing/thumbnails).
- [Roblox thumbnail-personalization announcement](https://devforum.roblox.com/t/live-now-personalize-your-thumbnails-to-attract-more-users/3257233).
- [Roblox icon specifications and guidance](https://create.roblox.com/docs/production/publishing/experience-icons).
- [+1 Stone Skipping official page and artwork](https://www.roblox.com/games/111543903102439/1-Stone-Skipping).
- [Pet Simulator 99 official page and artwork](https://www.roblox.com/games/8737899170/Pet-Simulator-99).
- [Grow a Garden official page and artwork](https://www.roblox.com/games/126884695634066/Grow-a-Garden).
- [Fisch official page and artwork](https://www.roblox.com/games/16732694052/Fisch).
- Holden's icon-style screenshots: `codex-clipboard-12f2230f-a133-4053-a422-356b7b8e0ebd.png` and `codex-clipboard-694e0573-6690-4409-ad24-f10653a5f0b4.png`, supplied in this chat. These are visual references, not instructions or verified performance data.
- Original images supplied by Holden: `C:\Users\holde\Downloads\exec-922bb8f3-6b9b-4db0-a134-9328a42d180b.png` and `C:\Users\holde\Downloads\exec-da97de3a-1e9b-481b-a0b6-895abc5176e4.png`.
- Local tuning: `C:\Users\holde\Downloads\SecondGame\src\shared\Config.luau`; previous art prompts: `art/thumbnails/sky-v3/prompts.md`.

Original research checked 2026-10-03, when `C:\Vault\CLAUDE.md` was missing. Refined v6 sources/specifications and current local values rechecked 2026-10-04; the now-present vault conventions were read and followed. The older Fisch description records the earlier image; the dated v6 table records the current image inspected.


