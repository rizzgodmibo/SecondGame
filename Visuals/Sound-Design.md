---
tags: [visuals/audio]
status: draft
updated: 2026-10-04
confidence: medium
---
# Sound Design

Two coexisting audio systems: legacy **`Sound` + `SoundGroup`** (simple, still fully supported) and the modular **audio API** (`AudioPlayer` → `Wire` → effects → `AudioEmitter`/`AudioListener` → `AudioDeviceOutput`). New projects should use the audio API for mixing/buses/effects; `Sound` is fine for quick one-shots.

## TL;DR
- **Mix with buses**: Music, SFX, UI, Ambience, Voice. Legacy: one `SoundGroup` per bus under `SoundService` (set `Sound.SoundGroup`). Audio API: one `AudioFader` per bus wired to `AudioDeviceOutput`. Expose Music/SFX sliders in settings — players mute bad music, not the game.
- **Default levels** (relative): music −14 to −18 dB below SFX peaks; UI clicks quiet and short (≤ 150 ms); reward stingers loudest UI event. In numbers: Music bus 0.3–0.5, SFX 0.7–1, UI 0.5. Normalise source files to about **−16 LUFS integrated / −1 dBTP** before upload so in-engine volumes stay consistent.
- **Spatial**: 3D sounds = `Sound` parented to a part/attachment (`RollOffMode = InverseTapered`, `RollOffMinDistance` 5–10, `RollOffMaxDistance` 60–150) or `AudioEmitter` + `DistanceAttenuation` curve. UI/music = 2D (parent to `SoundService`, or AudioPlayer → AudioDeviceOutput).
- **Upload rules**: you must own the rights; `.mp3/.ogg/.wav/.flac`, < 20 MB, < 7 min, ≤ 48 kHz, mono/stereo/3.0/5.1; 100 uploads per 30 days unverified, 2,000 ID-verified. Uploaded audio is private to you until you grant experience/collaborator permission.
- **Licensed music**: use the Creator Store's free library (100,000+ professionally produced SFX and tracks from Roblox audio partners) — never upload commercial songs; they get removed and risk account strikes.
- Every player action gets a sound; vary pitch ±5–10% and keep a per-sound cooldown (≥ 50 ms) to prevent stacking.

## Legacy Sound essentials
- `Sound.Volume` 0–10 (default 0.5); `PlaybackSpeed` (pitch); `Looped`; `PlaybackRegion`/`LoopRegion` (with `PlaybackRegionsEnabled`); `RollOffMode` (`Inverse`, `Linear`, `LinearSquare`, `InverseTapered`); `RollOffMinDistance`/`RollOffMaxDistance`; `PlaybackLoudness` (0–1000, for visualisers); `SoundGroup`.
- `SoundService:PlayLocalSound(sound)` — plays a 2D sound locally without parenting; good for UI.
- `SoundService.RespectFilteringEnabled = true` (default) — client-played sounds don't replicate; play local feedback on the client, world sounds others must hear on the server (or broadcast a remote and play on each client — preferred, lower latency).
- Effects as children of Sound/SoundGroup: `EqualizerSoundEffect`, `ReverbSoundEffect`, `CompressorSoundEffect`, `ChorusSoundEffect`, `DistortionSoundEffect`, `EchoSoundEffect`, `FlangeSoundEffect`, `PitchShiftSoundEffect`, `TremoloSoundEffect`.
- `SoundService.AmbientReverb` for global reverb presets (caves, halls).

## Audio API (modular)

| Instance | Role | Key properties |
|---|---|---|
| `AudioPlayer` | Plays an asset | `Asset` (ContentId), `Volume` 0–10, `Looping`, `PlaybackSpeed`, `TimePosition`, `PlaybackRegion`, `LoopRegion`, `AutoLoad`, `IsReady`; `:Play()`, `:Stop()`, `.Ended` |
| `Wire` | Connects streams | `SourceInstance`, `TargetInstance`, `SourceName` (default `Output`), `TargetName` (`Input`; `AudioCompressor` also has `Sidechain`), `Connected` |
| `AudioFader` | Bus/volume | `Volume` 0–3, `Bypass` |
| `AudioEmitter` | Virtual speaker in 3D | `DistanceAttenuation` curve (`SetDistanceAttenuation({[distance]=volume})`), `AngleAttenuation`, `AudioInteractionGroup`, `AcousticSimulationEnabled` |
| `AudioListener` | Virtual microphone | `AudioInteractionGroup`, attenuation curves; auto-created by `SoundService.DefaultListenerLocation` (`Default`/`None`/`Character`/`Camera`) |
| `AudioDeviceOutput` | Player's speakers | `Player` (nil = local) |
| Effects | `AudioEqualizer`, `AudioReverb`, `AudioCompressor` (sidechain ducking), `AudioFilter` (`FilterType` Lowpass/Highpass/Peak…), `AudioEcho`, `AudioChorus`, `AudioDistortion`, `AudioFlanger`, `AudioPitchShifter`, `AudioTremolo`, `AudioLimiter`, `AudioGate`, plus `AudioChannelMixer`/`AudioChannelSplitter`, `AudioRecorder` (verified against API class list 2026-10-04) | `Bypass` on each |
| `AudioAnalyzer` | Metering | `RmsLevel`, `PeakLevel`, spectrum |
| `AudioTextToSpeech` / `AudioSpeechToText` | TTS / STT | see docs |

2D chain: `AudioPlayer → Wire → AudioFader(bus) → Wire → AudioDeviceOutput`.
3D chain: `AudioPlayer → Wire → AudioEmitter` (parented to a part) … `AudioListener → Wire → AudioDeviceOutput` (auto-created if `DefaultListenerLocation` is `Character` or `Camera`).

### Bus setup + UI sound player (client)

```lua
--!strict
-- ReplicatedStorage/Shared/Audio/Mixer.luau (required from a LocalScript)
local SoundService = game:GetService("SoundService")

export type BusName = "Music" | "SFX" | "UI" | "Ambience"

local Mixer = {}
local buses: { [string]: AudioFader } = {}

local output = Instance.new("AudioDeviceOutput")
output.Name = "MixerOutput"
output.Parent = SoundService

local function wire(source: Instance, target: Instance, parent: Instance): Wire
	local w = Instance.new("Wire")
	w.SourceInstance = source
	w.TargetInstance = target
	w.Parent = parent
	return w
end

local DEFAULT_VOLUMES: { [string]: number } = { Music = 0.4, SFX = 1, UI = 0.6, Ambience = 0.5 }

for name, volume in DEFAULT_VOLUMES do
	local fader = Instance.new("AudioFader")
	fader.Name = name .. "Bus"
	fader.Volume = volume
	fader.Parent = SoundService
	wire(fader, output, fader)
	buses[name] = fader
end

function Mixer.setBusVolume(bus: BusName, volume: number)
	buses[bus].Volume = math.clamp(volume, 0, 3)
end

local rng = Random.new()

-- Fire-and-forget 2D sound on a bus (UI clicks, stingers).
function Mixer.play2D(assetId: string, bus: BusName, volume: number?, pitchJitter: number?)
	local player = Instance.new("AudioPlayer")
	player.Asset = assetId
	player.Volume = volume or 1
	local jitter = pitchJitter or 0
	player.PlaybackSpeed = 1 + rng:NextNumber(-jitter, jitter)
	player.Parent = buses[bus]
	wire(player, buses[bus], player)
	player.Ended:Once(function()
		player:Destroy()
	end)
	player:Play()
end

-- Looping music track with crossfade-ready fader per track.
function Mixer.playMusic(assetId: string): AudioPlayer
	local player = Instance.new("AudioPlayer")
	player.Asset = assetId
	player.Looping = true
	player.Parent = buses.Music
	wire(player, buses.Music, player)
	player:Play()
	return player
end

return Mixer
```

Notes: preload frequently used one-shots by keeping a template `AudioPlayer` with `AutoLoad = true` and cloning it (first play of an unloaded asset is delayed). ⚠️ verify: whether `:Play()` before `IsReady` queues playback or drops it on slow connections — wait on `IsReady` for stingers that must sync with visuals.

Music ducking: wire the SFX/voice bus into an `AudioCompressor`'s **Sidechain** pin placed on the Music bus chain — music dips automatically when big SFX play.

## UI sound feedback map

| Event | Sound | Length | Notes |
|---|---|---|---|
| Hover (PC only) | soft tick | 30–60 ms | very quiet; skip on touch |
| Click / confirm | pop/click | 60–150 ms | ±6% pitch jitter |
| Back / close | lower-pitched click | 60–120 ms | |
| Error / can't afford | dull buzz | 150–250 ms | pair with shake of the button |
| Currency gain | coin tick, rising pitch per tick | 50 ms each | cap rate 15/s |
| Reward / level-up | stinger | 0.8–2 s | loudest UI sound; duck music |
| Purchase success | "cha-ching" + sparkle | 0.5–1 s | reinforce spending (ethically) |
| Notification / quest complete | chime | 0.3–0.6 s | |

See [[UI-Polish-And-Juice]] for pairing with motion.

## Music strategy
- 2–4 tracks minimum: lobby/menu, main gameplay, intense (boss/event), shop (optional). Crossfade 1–2 s between states.
- Loop points: use `LoopRegion` to skip intros on repeat.
- Silence is a tool: drop music in horror; reduce music volume while tutorials speak.
- Music shown on the game details page requires: passes moderation/copyright, meets duration/plays/age thresholds, meaningful title, uploader ID verified, Audio Upload License Agreement accepted.

## Licensing & asset privacy
- Only upload audio you own or have licensed for Roblox use. Roblox runs copyright detection; infringing audio is rejected/removed (account moderation risk).
- Free, cleared library: Creator Store → Audio (Roblox + partner tracks). Prefer these for commercial games.
- Uploaded audio is restricted to you; grant use to groups/experiences via Creator Dashboard → Development Items → Audio → Permissions. **Upload audio under the group** that owns the game to avoid permission errors.
- Limits (2026-10-04): 100 audio uploads / 30 days (unverified), 2,000 / 30 days (ID-verified); < 20 MB, < 7 min, ≤ 48 kHz.

## Volume normalisation workflow
1. Master all music to ~−16 LUFS integrated, SFX peaks at −1 dBTP, UI SFX ~−20 LUFS short-term (quieter).
2. Upload; set per-asset `Volume` only for corrections, and do mixing on buses.
3. In game, measure with `AudioAnalyzer` (`RmsLevel`, `PeakLevel`) on each bus during a loud scene; keep the Master path from clipping (add an `AudioCompressor`/limiter on the output chain).
4. Test on phone speakers (no bass) and headphones.

## Checklist
- [ ] Buses for Music/SFX/UI/Ambience; settings sliders persist (save in player data)
- [ ] All game audio uploaded under the owning group (or permissions granted)
- [ ] UI events all mapped to sounds; pitch jitter + cooldown
- [ ] 3D sounds have sensible rolloff (no map-wide audible footsteps)
- [ ] Music loops cleanly; crossfades between states
- [ ] Checked on phone speakers

## Pitfalls
- Server-side `Sound:Play()` for UI clicks → latency and everyone hears it.
- Inserting audio by clicking in Toolbox creates a legacy `Sound`, not an `AudioPlayer`.
- Overlapping identical sounds (100 coins at once) → phasing and clipping; throttle.
- Commercial music uploads → removal, wasted upload quota, possible strikes.
- Forgetting Wires → AudioPlayer "plays" silently (`Wire.Connected` false).
- Default `Sound.RollOffMaxDistance` (10000) on loud world sounds → heard everywhere.

## Related
- [[Visuals/_Index]] · [[UI-Polish-And-Juice]] · [[Animation-Rigging-And-IK]] · [[Asset-Creation-Workflow-And-Marketplace]] · [[Remotes-And-Networking]]

## Sources
- Audio objects (AudioPlayer/Emitter/Listener/DeviceOutput/Wire, 2D vs 3D setup, ListenerLocation) — https://create.roblox.com/docs/audio/objects
- Audio effects — https://create.roblox.com/docs/audio/effects
- Audio assets (upload requirements, 100/2,000 per 30 days, visibility rules, Creator Store 100k+ licensed tracks) — https://create.roblox.com/docs/audio/assets
- Legacy sound objects & groups — https://create.roblox.com/docs/sound/objects , https://create.roblox.com/docs/sound/groups
- API: Sound (Volume 0–10 default 0.5), AudioPlayer (Volume 0–10, AutoLoad), AudioFader (Volume 0–3), Wire (Output/Input/Sidechain pins), SoundService — https://create.roblox.com/docs/reference/engine/classes/Wire
- Asset privacy / permissions — https://create.roblox.com/docs/projects/assets/privacy
- All checked via Roblox/creator-docs GitHub source (2026-10-02 commit) on 2026-10-04. LUFS targets are industry convention (streaming/game audio), not Roblox requirements.
