---
title: Roblox Audio Pipeline
date: 2026-10-03
tags: [roblox, audio, pipeline, how-to]
---
# Roblox Audio Pipeline (Pixabay → Open Cloud → game)

How sound and music were added to Paper Plane Toss (Phase 11), so the same steps can be reused.

## Picking sounds
- **Source:** [Pixabay](https://pixabay.com/) music and sound effects. The Pixabay Content License covers games and needs no credit.
- **Zapsplat needs a logged-in account** (and credit on the free tier), so Holden has to download those himself.
- **Claude can't listen to audio.** It shortlists 3 options per sound by genre, length and tags, and Holden picks by ear.
- Holden's call: avoid AI-generated tracks, like with art.
- **Getting the file:** each Pixabay page has the real file URL in its HTML (`cdn.pixabay.com/download/audio/...mp3`). Download it with curl and a browser user agent.

## Uploading
- **Script:** `AssetLibrary/tools/upload_audio.sh <file.mp3> "<name>"`. It's the same Open Cloud flow as `upload_model.sh`, with `assetType: Audio` and `audio/mpeg`.
- **Quota (verified 2026-10-04, Open Cloud usage guide):** audio uploads through the Assets API are capped at **100/month if ID-verified, 10 total/month if not**. Max 7 min, mp3/ogg/wav/flac, 20 MB per request. Generate-Speech uploads count too. Keep a tagged local library and combine sounds rather than uploading per iteration ([[Video-SyphoDev-Claude-Code-Roblox-Workflow]] §7.5).
- **Moderation check:** `GET https://apis.roblox.com/assets/v1/assets/<id>` with the API key returns `moderationResult.moderationState`. All 17 Paper Plane sounds were "Approved" within minutes.
- **Keep the originals in the repo** (`audio/src`) and the ids in `audio/ids.txt`.

## In game
- **One client module plays everything** (`client/Audio/Sound`). It has two SoundGroups, Music and SFX, so the player's sliders scale whole groups.
- **The mix lives in Config** (`Config.Audio`): id, volume and an optional `length`.
- **No ffmpeg on this PC:** long files are trimmed in game with `Sound.PlaybackRegionsEnabled` + `PlaybackRegion = NumberRange.new(0, length)`.
- **The "+1" bounce pop climbs in pitch** per bounce through `PlaybackSpeed`. That's the satisfying feel of +1 games.
- **Throttle one-shots** with a minimum gap and a cap on copies. A phone hitch can fire dozens of bounces in one frame.
- **Music crossfades** use a per-track fade counter. A fade-out that finishes late must never stop a track that has since faded back in.
- **Start both groups at volume 0** until the saved settings arrive, so a player who muted music never hears a burst on join.
- **Volume sliders on touch:**
  - track the InputObject that started the drag;
  - release on `WindowFocusReleased`;
  - save the final value about 0.35 s after the last change, so the rate limiter can't drop it.

## Mix lessons
- **The first music mix was "very very loud" on a phone** (hub 0.32). The halved mix (hub 0.16, flight 0.19, cutscene 0.22) is the new baseline.
- **A constant wind ambience loop sounded like a plane engine.** It was removed.
- **Training-pad trampoline "boing":** Pixabay option 2, `rbxassetid://135392770352262` at volume 0.5, pitch randomised 0.95–1.1 per bounce.

## Moving an experience to a group
Paper Plane Toss went from Holden's account to his group on 2026-10-03. The audio was uploaded under his user account, but **all music and SFX still played on a live server** in the Roblox app afterwards, and no permission changes were needed. Check on a real live server, not Studio: Studio can be more lenient when you own the sounds.

Related: [[Game Dev Resource Sites]], [[Keeping API Keys Out of Git]], [[2026-10-03 Paper Plane Toss Phone Playtest]] · [[Roblox Sound Library Skill]] (soundcheck, catalogue at AssetLibrary/audio/catalogue.json, quota, calibrated volume targets)
