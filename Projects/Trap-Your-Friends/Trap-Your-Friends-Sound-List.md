---
tags: [project/trap-your-friends, visuals/audio]
status: draft
updated: 2026-10-06
confidence: medium
---
# Trap Your Friends: Sound List

## TL;DR
- (USER, 2026-10-06) New, **original** SFX only: our own synthesis or free licensed Creator Store audio. Nothing ripped, no commercial audio. Uploads are private and within the monthly quota. Every sound and its source is listed here.
- **18 candidates made** (9 sounds × variants a/b) by procedural synthesis in `TrapYourFriends/art/sfx/make_sfx.py`: oscillators, filtered noise and pitch sweeps written from scratch in numpy. **No samples, no downloads, no AI audio model.**
- All 18 **pass the roblox-sound-library soundcheck** (no lead silence over 50 ms, no clipping, nothing too quiet, under the size/length limits) and the profile end check. The two "tell" sounds end at their peak on purpose (30 ms fade), because the trap fires right then.
- **Uploaded by Holden via Creator Hub** (ids below). Earlier, Studio's Asset Manager wouldn't open for him. Alternative steps: `art/sfx/export/IMPORT-SOUNDS.md` (Creator Hub upload → Toolbox Inventory insert). **Wired 2026-10-06:** `Audio/Sfx.luau` holds both sets (`Default` = a, `Alternate` = b); all 18 load in Studio (IsLoaded + TimeLength checked). Holden picks a/b by ear: in Studio press **4** on the dev Trapper panel to switch. Holden picks a/b by ear; Claude can't listen.
- **Upload formats (2026-10-06):** the same 18 sounds also exist as MP3 (192 kbps) and WAV (16-bit, 44.1 kHz) in `art/sfx/export/mp3/` and `wav/`, plus zips. All pass the soundcheck, and MP3 encoding added no lead silence.
- Quota (AssetLibrary catalogue log): 18 of 100 used in the last 30 days; importing all 18 → 36.

## Uploaded asset ids (Holden, Creator Hub, shows "Oct 5, 2026"; read from his screenshots 2026-10-06)
| Sound | a | b |
|---|---|---|
| bonk | 124071009984663 | 92805793527879 |
| crunch | 116778509545794 | 114305981838194 |
| glass | 129785947725971 | 95290214832067 |
| spring | 109301023538056 | 128616531739496 |
| chomp | 117461220222021 | 89261539504112 |
| whoosh | 99906691688147 | 122278482696370 |
| explosion | 100782410882499 | 83510099443178 |
| tell | 79351746212505 | 98109706768877 |
| catch | 106131538887973 | 73423256061730 |
- Logged in the AssetLibrary audio catalogue (36 sounds, validated; quota 36/100 in 30 days).
- **Not wired into the game yet** (the 2026-10-06 step was planning only). Wiring = put the ids in `src/shared/Audio/Sfx.luau` (step 1 of [[Trap-Your-Friends-v3-Plan]]). Default: the "a" variants until Holden picks by ear.

## The sounds
| Sound | Used for (TrapFx kind) | a | b | Source | Status |
|---|---|---|---|---|---|
| bonk | Hammer, Glove, Wrecking Ball, dodgeball hits | 0.30 s, woody damped sine 430→300 Hz + click | 0.30 s, lower/hollower (300→210 Hz + 3rd harmonic) | synthesis | file ready, not imported |
| crunch | Brick smashes ("Smash"), Spike Pop | 0.40 s, 14 band-passed noise grains + 95 Hz thud | 0.60 s, 24 grains + 70 Hz thud | synthesis | file ready |
| glass | Glass Floor shatter (and quiet for "Crack") | 0.70 s, 22 resonant pings 2.2–6.5 kHz + crack + hiss tail | 0.90 s, 38 brighter pings | synthesis | file ready |
| spring | Bounce Pad | 0.55 s, triangle boing 220→400 Hz with wobble | 0.55 s, square/sine twang | synthesis | file ready |
| chomp | Chomper bite | 0.32 s, two teeth clacks + squelch | 0.38 s, one big chomp + growl + squelch | synthesis | file ready |
| whoosh | Swings, punches, trapdoor, turret shots | 0.50 s, band-pass noise sweep | 0.32 s, faster sweep | synthesis | file ready |
| explosion | TNT | 1.6 s, 30–75 Hz boom + rumble + crack + crackle (soft clip) | 1.1 s, punchier, more mid crack | synthesis | file ready |
| tell | Every trap's 0.4 s warning | 0.4 s, accelerating ratchet ticks + rising tone | 0.4 s, two-tone beep "bee-boop" | synthesis | file ready |
| catch | "Caught!" sting | 0.95 s, original 4-note marimba drop + slide whistle | 0.8 s, boing + pop + major chord | synthesis | file ready |

Soundcheck `volume=` (Sound.Volume at the catalogue SFX target −19.7 dB), a/b, final files: bonk 0.80/0.72, crunch 0.57/0.74, glass 0.72/0.64, spring 0.48/0.36, chomp 0.57/0.33, whoosh 0.61/0.57, explosion 0.30/0.31, tell 0.54/0.21, catch 0.43/0.49. Full output: `art/sfx/soundcheck.txt`; waveform/spectrogram sheets: `art/sfx/profile/`.

## Creator Store audio
- None picked yet. When an original sound loses to a Creator Store one by ear, record its asset id, title, creator and licence note here (⚠️ verify the store's licence wording at that time).

## Wiring
- `src/shared/Audio/Sfx.luau` holds id + volume + pitch jitter + cooldown per sound (empty ids are skipped). `SfxController` plays them as 3D sounds at the event position.

## Related
[[Trap-Your-Friends]] · [[Sound-Design]] · [[Roblox Sound Library Skill]] · [[Roblox Audio Pipeline]] · [[2026-10-06-Trap-Your-Friends-Style-Test-v2]]

## Sources
- Generated locally 2026-10-06 (`make_sfx.py`); checks with the roblox-sound-library `soundcheck.py` / `sfxprofile.py`.
