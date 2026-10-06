# Roblox Development Vault — Conventions

This vault (canonical location `E:\Vault`; `C:\Vault` is an old copy, don't edit it; mirrored in git repo `rizzgodmibo/SecondGame`) exists so Claude can
design, build, launch, monetise and grow a successful Roblox game with minimal correction.
It is never "done": every session should close a gap, verify a claim, or refresh a stale note.

## Working rules from Holden
- Holden makes Roblox games for young teens, mobile and PC first. Roblox: MiboRBX, user ID 2599876233.
- Before game code, present a plan and file list and wait for approval. Never silently invent mechanics or lore. Holden makes commits unless asked otherwise.
- Before 3D/map work read `C:\Users\holde\Documents\GameDev\AssetLibrary\README.md`. Use clean, flat-shaded low-poly Blender assets with crisp zone colours, model colour variation and varied trees. No Roblox AI meshes or final part-built props. Be honest about weak art.
- For Paper Plane Toss, project planning USER lines, ROADMAP and actual code/place are distinct sources of truth; flag disagreements. Do not convert research suggestions into approvals.
- Studio deletions: list exact instances for Holden to delete.
- The ongoing vault mandate authorizes research and vault edits. It does not authorize game changes, purchases, publishing or messages to others. Never represent a complete checklist as a guarantee of commercial success.
- End replies with "Vault: created/updated <note path>" or "Vault: nothing to save".

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
| `Assets/` | Binary assets the owner supplies (icon packs, reference captures), asset IDs and provenance + a catalogue note per pack |
| `Projects/<name>/` | Game-specific decisions, specs, asset IDs |
| `Bugs/` | Bugs and their fixes |
| `Playtests/` | Observed playtest logs |
| `Resources/` | Reusable how-tos and guidance |
| `Prompting/` | How to prompt Claude and other AIs for each part of Roblox development (principles, copy-paste prompts, checks) |
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
  Older local notes may use `title/date/source/project/verified/review_after` — keep those fields when updating them.
- Sections: **TL;DR** (3–6 bullets an agent can act on) → body → **Checklist** (if actionable) → **Pitfalls** → **Related** (`[[wikilinks]]`) → **Sources**.
- Code is Luau with `--!strict` in ```lua fences, runnable, and states where it lives (ServerScriptService / ReplicatedStorage / StarterPlayerScripts).
- Mark anything unverified, time-sensitive or platform-policy-dependent with `⚠️ verify:` plus what to check.
  Numbers (prices, revenue shares, rates, limits) must cite a source and a date.
- Keep evidence types separate: verified platform facts, documented library behaviour, local observations, user-approved decisions, recommendations/hypotheses, open questions. Never claim a test was run when only a checklist was written.
- Prefer concrete numbers, defaults and decision rules over vague advice ("do X when Y").

## Linking
- Use Obsidian wikilinks `[[Note-Name]]` (no folder prefix needed; names are unique).
- Every new note must be linked from `Home.md` or its folder's `_Index.md`.

## Maintenance
- When you verify a claim, update `updated:` and log it in `Meta/Verification-Log.md`.
- Notes older than 180 days with time-sensitive claims → set `status: stale` and add to Gap-Tracker.
- At the end of a session, update `Meta/Gap-Tracker.md` (what was done, what is next).
