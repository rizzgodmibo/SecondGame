---
tags: [resources/tooling, visuals/audio, meta/ai-workflow]
status: verified
updated: 2026-10-04
confidence: medium
---
# Roblox Sound Library Skill

A Claude Code skill (`roblox-sound-library`): measure sounds before approval, keep a tagged catalogue of approved Roblox ids to **reuse instead of re-uploading**, track the upload quota, and play layered sounds in game.
Built 2026-10-04 as the sixth skill from [[Video-SyphoDev-Claude-Code-Roblox-Workflow]] (§7.5).

## TL;DR
- **Where:** `C:\Users\holde\.claude\skills\roblox-sound-library\`. Catalogue: `AssetLibrary/audio/catalogue.json` (18 Paper Plane Toss sounds with ids and volumes).
- **Soundcheck** (Blender headless; Claude can't listen): lead silence, clipping, quiet files, the 7 min / 20 MB / format limits, and a **suggested Sound.Volume**.
- **Catalogue tool** (Lune): validate, find by tag, **quota** (30-day window; the cap is assumed 100/month ID-verified, ⚠️ confirm), export a Luau ids table.
- **SoundPlan / SoundPlayer:** layered recipes, pitch ranges, delays, throttling (min gap + max copies), PPT's pitch climb. The pure logic is unit-tested; the Studio glue isn't tested yet.
- **Status: self-test PASSED 2026-10-04.** Nothing uploaded. Paper Plane Toss only read.

## Calibrated loudness targets (from Paper Plane Toss's phone-approved mix)
In-game level = file level (soundcheck) + 20·log10(Sound.Volume). Medians, measured 2026-10-04:
| Kind | Target | From |
|---|---|---|
| SFX | **−19.7 dB** | 14 used SFX (range −31.9 to −16.5; UI click and purchase ~12 dB quieter on purpose) |
| Music | **−30.3 dB** | hub −30.3, flight −25.2, cutscene −31.9 (after "halved after the phone playtest") |
Player SoundGroup sliders (PPT defaults 0.8 SFX / 0.7 music) apply on top.

## Finding: Paper Plane Toss sounds start late (report only; PPT is frozen)
9 of 14 SFX have more than 50 ms of silence before the sound: **click 216 ms, sparkle 212, level-up 182, big-win 119, bonk 103**, drumroll 84, throw 79, glass 73, ninja 59.
That makes taps and rewards feel slightly behind. For a future update (Holden's call): trim the files, or start playback after the gap with `PlaybackRegion`, the same trick PPT uses to end the drumroll at 1.6 s.

## Pitfalls
- Tags for PPT sounds come from file names only. Holden to confirm by ear.
- Quota math only knows logged uploads. Always log a new upload in the catalogue.
- Reuse in another game: confirm on a live server (Studio is more lenient), per [[Roblox Audio Pipeline]].

## Related
- [[Roblox Audio Pipeline]] · [[Sound-Design]] · [[Video-SyphoDev-Claude-Code-Roblox-Workflow]] · [[Roblox Code Gate Skill]] · [[Paper Plane Toss]]

## Sources
- SyphoDev video, 20:12–20:58: https://www.youtube.com/watch?v=afuKhenJldY
- Open Cloud audio limits (100/month ID-verified, 10 unverified, 7 min, 20 MB): https://create.roblox.com/docs/cloud/guides/usage-assets (verified 2026-10-04)
- Paper Plane Toss `Config.Audio` and `audio/src`, read 2026-10-04 (no changes made).
