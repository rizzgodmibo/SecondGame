# Roblox Development Vault — Conventions

This vault (canonical location `C:\Vault`, mirrored in git repo `rizzgodmibo/SecondGame`) exists so Claude can
design, build, launch, monetise and grow a successful Roblox game with minimal correction.
It is never "done": every session should close a gap, verify a claim, or refresh a stale note.

## Before you write anything
1. Search the vault first (`grep -ri "<topic>" .`) — **never duplicate**. If a note exists, update it.
2. Check `Meta/Gap-Tracker.md` for the next area due in the rotation.
3. Start from `Home.md` (map of content) to find the right folder.

## Folders
| Folder | Holds |
|---|---|
| `Systems/` | Engineering: Luau, architecture, networking, data, security, performance, tooling |
| `Visuals/` | UI, VFX, animation, 3D/Blender pipeline, lighting, audio, art direction |
| `Design/` | Core loops, progression, economy, onboarding, pacing, balancing |
| `Monetisation/` | Gamepasses, dev products, pricing, receipts, DevEx, ethics |
| `Growth/` | Discovery algorithm, thumbnails/icons, ads, launch, influencers |
| `Retention/` | D1/D7/D30, dailies, events, social, community |
| `Operations/` | Analytics, A/B testing, live-ops, moderation/policy, post-mortems |
| `Reference/` | Real-game and community examples: icons, thumbnails, videos, UI/VFX breakdowns |
| `Assets/` | Binary assets the owner supplies (icon packs, reference captures) + a catalogue note per pack |
| `Projects/<name>/` | Game-specific decisions, specs, asset IDs |
| `Inbox/` | Unsorted findings — triage into a folder later |
| `Meta/` | Gap tracker, verification log, sources list |
| `Templates/` | Note templates |

## Note format
- File names: `Title-Case-With-Hyphens.md`. One topic per note; split when a note passes ~400 lines.
- Every note starts with YAML frontmatter:
  ```yaml
  ---
  tags: [area/subarea]
  status: draft | reviewed | verified | stale
  updated: YYYY-MM-DD
  confidence: high | medium | low
  ---
  ```
- Sections: **TL;DR** (3–6 bullets an agent can act on) → body → **Checklist** (if actionable) → **Pitfalls** → **Related** (`[[wikilinks]]`) → **Sources**.
- Code is Luau with `--!strict`, runnable, and states where it lives (ServerScriptService / ReplicatedStorage / StarterPlayerScripts).
- Mark anything unverified, time-sensitive or platform-policy-dependent with `⚠️ verify:` plus what to check.
  Numbers (prices, revenue shares, rates, limits) must cite a source and a date.
- Prefer concrete numbers, defaults and decision rules over vague advice ("do X when Y").

## Linking
- Use Obsidian wikilinks `[[Note-Name]]` (no folder prefix needed; names are unique).
- Every new note must be linked from `Home.md` or its folder's `_Index.md`.

## Maintenance
- When you verify a claim, update `updated:` and log it in `Meta/Verification-Log.md`.
- Notes older than 180 days with time-sensitive claims → set `status: stale` and add to Gap-Tracker.
- At the end of a session, update `Meta/Gap-Tracker.md` (what was done, what is next).
