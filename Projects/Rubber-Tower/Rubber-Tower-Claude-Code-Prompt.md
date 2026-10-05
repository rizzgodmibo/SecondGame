---
tags: [project/rubber-tower, project/prompt]
status: draft
updated: 2026-10-04
confidence: medium
---
# Rubber Tower: Claude Code Kickoff Prompt

## TL;DR
- Paste the block below into a new Claude Code session opened with the vault (`C:\Vault`) connected. It points Claude Code at the vault notes instead of repeating them, so the notes stay the single source of truth.
- It tells Claude Code to read first, restate what it understood, ask where to create the project, present the phase 0 to 1 plan and file list, and **wait for Holden's approval before writing game code**.
- Status: final draft (2026-10-04), ready for Holden to paste. Nothing in the game is built.
- Keep it current: when decisions change in [[Rubber-Tower]], the prompt needs no edits unless the process rules change.

## The prompt (copy everything in the block)

```text
You are helping me (Holden) build my third Roblox game, "Rubber Tower", in Claude Code. My Obsidian vault (C:\Vault) is connected and is the source of truth. We planned the game in a separate chat; everything we decided is saved in the vault.

THE GAME IN FIVE LINES
A very tall, fixed tower obby for young teens (mobile and PC first). Every player's own avatar is the ragdoll: mostly ragdolls on falls and shoves, plus some wobble/bounce areas. 3-4 big saved checkpoints with a teleport menu (teleport to any checkpoint you have claimed; it does not change your respawn point), free soft platforms between them, shared server, a close-range shove (30 s cooldown, about 10 studs, a few seconds of ragdoll; editable), a hand-up, a currency called Squishies (each payout earned once, also sold for Robux), unlockable titles above heads, and cosmetic/novelty passes. New worlds come later and unlock after beating the first.

STEP 1: READ (in this order, before replying)
1. C:\Vault\CLAUDE.md (vault rules and my working rules)
2. Projects/Rubber-Tower/Rubber-Tower.md (hub: my approved decisions and open questions)
3. Projects/Rubber-Tower/Rubber-Tower-GDD.md
4. Projects/Rubber-Tower/Rubber-Tower-Build-Plan.md
5. Projects/Rubber-Tower/Rubber-Tower-Reference-Obbies.md and Rubber-Tower-Ideas-Bank.md
6. Then the vault notes you need for each phase, found via Home.md, for example Project-Bootstrap-Checklist, Module-Architecture, Remotes-And-Networking, Anti-Exploit-And-Server-Authority, Data-Persistence-DataStores-And-ProfileStore, Difficulty-And-Mastery, Pay-To-Win-Boundaries, ProcessReceipt-Handling, Roblox Mobile UI Layout, Rojo Workflow Gotchas, Roblox Studio MCP Quirks.
Search the vault before assuming anything ("grep -ri"). Do not duplicate notes; update them.

SOURCE-OF-TRUTH RULES
- Only lines under "Decisions from Holden" in the hub and lines tagged (USER) in the GDD are approved. (DRAFT) and UNDECIDED lines are not. Never turn a suggestion into an approval, never silently invent mechanics or lore, and flag any disagreement between the hub, GDD, plan and code.
- Mark anything unverified, time-sensitive or policy-dependent with "verify:" and say what to check. Never claim a test was run when it wasn't.
- This prompt does not authorize publishing, purchases, spending Robux, uploading assets, or messages to other people. I make the git commits unless I ask you to.
- If you list Studio instances for deletion, list the exact instances for me to delete.
- Before any 3D or map work, read C:\Users\holde\Documents\GameDev\AssetLibrary\README.md. Art direction: clean flat-shaded low-poly Blender assets, crisp zone colours, colour variation, varied trees. No Roblox AI meshes and no final part-built props. Be honest when art is weak.

STEP 2: REPLY WITH (no code yet)
a) A short summary of what you understood, split into approved, draft, and undecided.
b) Anything in the notes that conflicts or is unclear.
c) Ask me where to create the project folder and git repo (I have not chosen yet).
d) Your plan and file list for phases 0 and 1 only (project scaffold, then the avatar ragdoll prototype), with the gate each phase must pass.
Then STOP and wait for my approval.

AFTER I APPROVE
- Build phase 0 (Rojo scaffold with the roblox-dev setup skill, strict Luau, lint and format, empty bootstraps), then phase 1 (avatar ragdoll prototype, a bounce area, and a flat test place). Build only those, then stop for my review.
- Phase 1 must be tested on a real phone, not only in Studio. Measure the ragdoll cost and report it honestly.
- Server-authoritative design: the client sends intent only; the server validates range, cooldown and force. Use the roblox-dev skills (security, architecture, strict typing, testing). Use the Roblox Studio MCP where it helps and note its quirks.
- Put tunable numbers (shove distance and cooldown, checkpoint list, rewards) in a shared Config module so I can tune them.
- Save the Studio place file; the map lives there, not in git.

END OF EVERY REPLY
- Update the matching vault notes (hub, GDD, plan, Gap-Tracker, Verification-Log when you verify something) and end with "Vault: created/updated <note path>" or "Vault: nothing to save".
```

## Before pasting (Holden's checklist)
- [ ] Open the Claude Code session with `C:\Vault` connected and the roblox-dev plugin enabled.
- [ ] Decide the project folder location (the prompt will ask).
- [ ] Reread the open questions in [[Rubber-Tower]]; none blocks phases 0 and 1, but currency name, shove distance and checkpoint-menu rules are needed by phases 3 and 4.
- [ ] Say "go" only when you want building to start; the prompt stops for your approval first.

## Pitfalls
- The prompt links to notes, so keep those notes current; stale notes mean stale instructions.
- Claude Code does not see this planning chat. Anything that matters must be in the vault.

## Related
- [[Rubber-Tower]] · [[Rubber-Tower-GDD]] · [[Rubber-Tower-Build-Plan]] · [[Rubber-Tower-Reference-Obbies]] · [[Game-Building-Playbook]]

## Sources
- Vault `CLAUDE.md` working rules and the planning conversation with Holden, 2026-10-04.
