---
tags: [prompting/growth, growth/launch, growth/thumbnails]
status: draft
updated: 2026-10-04
confidence: medium
---
# Prompting: Launch, Store Page and Marketing Art (Icons, Thumbnails, Logos)

How to prompt image models and Claude for icons, thumbnails, logos, the store page and the launch plan. General rules: [[Prompting-Principles]].

## TL;DR
- **Image prompts: scene → subject → details → constraints, and give every input image a role** ("input 1 is the exact icon to improve; inputs 2 and 3 are style references only") (OpenAI image prompting guide; [[Paper Plane Toss Thumbnails and Game Icon]]).
- **For edits: "change only X", then repeat the keep list every time,** and fix a local defect with a focused follow-up instead of regenerating everything. Repeated edits drift (OpenAI; local).
- **Specify the geometry that tells the story** (where the flight path starts, which cloud it touches, where it ends) and then inspect it: requested geometry is not guaranteed (local, Paper Plane Toss trajectory repair).
- **Check outputs with numbers:** real pixel size (image tools ignore requested sizes), file size under the 3 MB limit, alpha on every border for logos ([[Blender 3D Logo Pipeline]]).
- **Marketing art must show the real game,** and AI-generated thumbnails carry a reputational risk. Ship one only as one arm of a personalization test against a non-AI version ([[Thumbnails-And-Icons]], [[X-Thumbnails-And-Icons]]).
- **Claude prepares; Holden publishes.** Uploading thumbnails, publishing the game, buying ads and posting are Holden's actions.

## What Claude needs from you
- The exact current assets to improve (attach them; say which file is "the" one), the reference icons/thumbnails you like and what to take from each.
- The game's real look: in-game renders or screenshots (the lane, the island, the avatar, the planes), so the art matches what players get.
- The one promise each image should make (progression, distance curiosity, instant item recognition).

## Vault notes to point Claude at
| Note | Gives Claude |
|---|---|
| [[Thumbnails-And-Icons]] · [[Icon-And-Thumbnail-Gallery]] · [[X-Thumbnails-And-Icons]] | Sizes (icon 512², thumbnail 1920×1080), small-size rules, personalization, AI-art risk |
| [[Paper Plane Toss Thumbnails and Game Icon]] · `Assets/Paper Plane Toss Refined v6 Prompts.txt` | Full working edit prompts, reusable production lessons, before/after files |
| [[Blender 3D Logo Pipeline]] · [[Art Direction Feedback]] | Logo lessons, alpha checks, Holden's icon critiques |
| [[Titles-Descriptions-And-Tags]] · [[Launch-Checklist]] · [[Discovery-Algorithm]] | Title ≤ 30 chars, first 160 chars of description, no hashtags, launch timing (Fri/Sat US), soft launch first |
| [[Sponsored-Ads-And-Paid-Acquisition]] · [[Roblox Ads Strategy]] · [[Influencer-Coverage]] | When ads make sense, credit conversion, measurement |

## Prompts

### 1. Refine an icon or thumbnail (image model, edit mode)
Structure taken from the working Paper Plane Toss v6 prompt (full text in the Prompts file):
```text
Use case: refine an existing Roblox [square icon / 16:9 thumbnail] for [Game].
INPUTS: input 1 is the EXACT image to improve. Inputs 2 and 3 are style references only: take their [rendering quality, expressive faces, dynamic camera, clean contours]; don't copy their objects, setting or text.
KEEP from input 1: [avatar identity and outfit, the item's exact look and colours, the hook text, the world's style].
CHANGE: [e.g. a livelier expression looking along the action; the item larger; one clear arc from the hand to one cloud and up behind the plane].
COMPOSITION: designed to read at [150 px]; one focal subject; [≤ 3] dominant colours; at most [one] short text element; nothing important in the bottom strip.
SETTING: [the game's real environment details]; keep scenery quieter than the subject.
DON'T ADD: [things from other games: cubes, studs, gems, chests, monsters, extra planes, logos, watermark].
OUTPUT: only the finished image, edge to edge, no comparison layout.
```
Then check: size and file size from the actual file, every path endpoint and contact point, the face, and the text spelling.

### 2. Fix one defect with a focused follow-up
```text
Edit the attached image. Change only [the crossed streaks behind the plane]: replace them with [one continuous white arc from the throwing hand down to the cloud puff and up behind the plane]. Keep everything else exactly the same: [avatar, face, plane, text, colours, framing, background].
```
Why: redesigning the whole image to fix one streak kept introducing new problems; the targeted edit fixed it ([[Paper Plane Toss Thumbnails and Game Icon]]).

### 3. Logo or title with transparency
```text
Make a transparent title logo for [Game]: [style references and what to take from each]. One integrated motif ([e.g. a folded plane and sweep]), tight lettering, dark contour plus a fine light keyline so it reads on both pale sky and a busy island.
After generating: load the PNG and check the alpha on all four borders is 0 and nothing touches an edge; report the canvas size and the % of fully transparent pixels. Preview it composited on [sky colour] and on [in-game screenshot].
```
Why: the approved Paper Plane Toss title first clipped its plane at the right edge; the numeric alpha check caught it ([[Blender 3D Logo Pipeline]]).

### 4. Store page copy
```text
Write the Roblox store page text for [Game]. READ FIRST: Growth/Titles-Descriptions-And-Tags.md.
Title: brand + genre keyword, about 30 characters, no emoji spam. Description: the first ~160 characters are the hook (what you do and why it's fun), then a short "latest update" line, 3–5 core-loop bullets, devices, and codes. Under 1,000 characters. No hashtags or keyword lists, no "free Robux"/giveaway framing, no claims the game can't back up.
Give me 3 options for the first 160 characters and say which you'd test first.
```

### 5. Launch plan
```text
Make a launch plan for [Game] from Growth/Launch-Checklist.md and Operations/Moderation-And-Policy-Compliance.md, as a checklist with dates. Mark which items are mine (publishing, Creator Hub settings, maturity questionnaire, ads, posts) and which you can prepare (copy, thumbnails for review, a smoke-test list, analytics checks). Include: soft launch first, the Fri/Sat US release window, the first-72-hours watch list (error rate, bounce, D1), and "don't change thumbnails, title or genre during the first test". Flag eligibility steps that need 2+ weeks.
```

## More examples (added 2026-10-04)
Shorter prompts for other common jobs. Same rules: fill every bracket, keep the check. Sourced patterns are credited in [[Community-Prompt-Examples]].

### Thumbnail concepts before generating
```text
Before any image generation, give me [3] thumbnail concepts for [Game], each making one different promise (progression, curiosity, the core action). For each: the focal subject, what the player avatar is doing, the 1–3 dominant colours, the text (≤ 3 words or none), and why it's true to the real game. I'll pick one or two to generate.
```
A one-line "high CTR thumbnail" request failed in Scuppy's video; a concept step first is the fix ([[Community-Prompt-Examples]] §6).

### Short-form clip scripts
```text
Write [5] TikTok/Shorts clip ideas for [Game] (Growth/Organic-Growth.md): each one shows a surprising real moment in the first second, is 9:16, under 20 s, with a caption line and an ending on the game name. Say exactly what to record in Studio or in game for each. No fake features.
```

### Update log
```text
Write the player-facing update notes for [Game]'s [date] update from this list of changes: [changes]. Lead with the exciting bit, 4–6 short lines with emoji, kid-friendly wording, no technical terms, no promises with dates. Also give a 60-character update announcement and the title tag to use while it's new.
```

### Creator outreach messages (for me to send)
```text
Draft personalised messages for these Roblox creators who cover [genre]: [names + one video of theirs each]. Each message references their specific video, offers [early access / a code / a named item], is short, and includes a disclosure line if anything is given in return (Growth/Influencer-Coverage.md). I send them; you don't contact anyone.
```

### Ad creative set
```text
Plan a Roblox Ads test for [Game] (Growth/Sponsored-Ads-And-Paid-Acquisition.md): [3–5] creatives from our real thumbnails, one Plays campaign, budget [$5–10/day] for [3–5] days, and what to read afterwards (cost per play, play-through, D1 of the ad cohort). Only if D1 and first-session are at or above P50; otherwise tell me to wait.
```

## How to check the result
- Image files: actual dimensions and bytes reported from the file, under 3 MB; the 150 px view checked; alpha borders 0 for logos.
- Art matches real in-game renders (no invented features or mechanics).
- Holden's pick and approval are recorded before anything is uploaded; candidates are never labelled "approved" or "winner" without data.
- Thumbnail tests: run personalization with 2–5 images and leave them to settle; judge by play-through and bounce, not clicks alone ([[Thumbnails-And-Icons]]).

## Pitfalls
- **Glossy close-up approval doesn't transfer.** Holden loved the glossy title but wanted a literal gameplay-style icon ([[Art Direction Feedback]]).
- **Old prompt bans go stale.** Earlier prompts banned a cloud road; real renders showed the game has one, so the ban was wrong ([[Paper Plane Toss Thumbnails and Game Icon]]).
- **Clickbait art** raises clicks and bounce together, which lowers recommendations ([[Discovery-Algorithm]]).
- **Ads before D1 works** waste money, and ad players don't count toward recommendation ranking ([[Sponsored-Ads-And-Paid-Acquisition]]).
- **Social links or Discord invites inside the game** are not allowed; only approved social links on the game page ([[Moderation-And-Policy-Compliance]]).

## Related
[[Prompting/_Index|Prompting]] · [[Prompting-Principles]] · [[Prompting-Analytics-And-Live-Ops]] · [[Growth/_Index|Growth index]] · [[Paper Plane Toss Thumbnails and Game Icon]]

## Sources
- OpenAI, Image prompting guide (structure, roles for inputs, "change only X" + preserve list, transparency checks), read 2026-10-04: <https://developers.openai.com/api/docs/guides/image-prompting>
- Local: [[Paper Plane Toss Thumbnails and Game Icon]], `Assets/Paper Plane Toss Refined v6 Prompts.txt`, [[Blender 3D Logo Pipeline]], [[Art Direction Feedback]].
