---
tags: [project/trap-your-friends, project/prompt]
status: draft
updated: 2026-10-05
confidence: medium
---
# Trap Your Friends: Claude Code Kickoff Prompt

## TL;DR
- Paste the block below into a **new** Claude Code session opened with the vault connected and the roblox-dev plugin enabled.
- It makes Claude Code read the vault notes (the single source of truth), restate what it understood, ask where the project folder goes, and present a plan. **The first thing it builds is a style test for Holden to approve.** No gameplay until the style is locked.
- Status: ready to paste (2026-10-05). Nothing is built.

## The prompt (copy everything in the block)

```text
You are helping me (Holden) build a new Roblox game, "Trap Your Friends", in Claude Code. My Obsidian vault is connected and is the source of truth. We planned the game in a separate chat; everything we decided is saved in the vault under Projects/Trap-Your-Friends/.

THE GAME IN FIVE LINES
A retro party game for young teens (mobile and PC first). Two teams each build a hidden trap lane out of classic studded Roblox bricks in about 90 seconds, prove they can beat it themselves, then swap and run each other's lane. The look is the classic/retro Roblox stud style (my reference: Jujutsu Shenanigans and similar retro-style games), and bricks break apart JJS-style when traps or players smash them, then rebuild. Small scope. This is a separate game from Rubber Tower: do not touch Rubber Tower's code or place.

STEP 1: READ (in this order, before replying)
1. CLAUDE.md in the vault root (vault rules and my working rules)
2. Projects/Trap-Your-Friends/Trap-Your-Friends.md (hub: my approved decisions and open questions)
3. Projects/Trap-Your-Friends/Trap-Your-Friends-Art-Style-Guide.md (NOT approved yet)
4. Projects/Trap-Your-Friends/Trap-Your-Friends-Reference-Board.md (look at the contact sheets in Assets/Reference-Captures/Retro-Stud/)
5. Projects/Trap-Your-Friends/Trap-Your-Friends-GDD.md
6. Visuals/Retro-Stud-Style-Guide.md, Visuals/Lighting-And-Atmosphere.md, Visuals/VFX-Particles-Beams-Trails.md
7. Then what each phase needs, found via Home.md: Project-Bootstrap-Checklist, Module-Architecture, Remotes-And-Networking, Anti-Exploit-And-Server-Authority, UI-Layout-And-Device-Scaling, Rojo Workflow Gotchas, Roblox Studio MCP Quirks.
Search the vault before assuming anything. Do not duplicate notes; update them.

SOURCE-OF-TRUTH RULES
- Only lines under "Decisions from Holden" in the hub and lines tagged (USER) in the GDD are approved. (DRAFT) and UNDECIDED lines are proposals. Never turn a suggestion into an approval, never silently invent mechanics or lore, and flag any disagreement between notes and code.
- ART EXCEPTION FOR THIS PROJECT: CLAUDE.md says "no final part-built props, use Blender low-poly". For Trap Your Friends I accept part-built classic bricks in principle, BUT the style and build method are not approved until I sign off on the style test below. Do not treat the art style guide as locked.
- Mark anything unverified or policy-dependent with "verify:" and say what to check. Never claim a test was run when it wasn't.
- This prompt does not authorize publishing, purchases, spending Robux, uploading assets, installing third-party modules or plugins, or messages to other people. I make the git commits unless I ask you to.
- If you list Studio instances for deletion, list the exact instances for me to delete.

STEP 2: REPLY WITH (no code yet)
a) A short summary of what you understood, split into approved, draft and undecided.
b) Anything in the notes that conflicts or is unclear.
c) The project folder already exists: C:\Users\holde\Documents\GameDev\TrapYourFriends (only a README so far). Ask me before creating the git repo there.
d) Ask me the open questions from the hub that block phases 0 and 1 (style direction A or B, avatars). Skip the ones that can wait.
e) Your plan and file list for phases 0 and 1 only, with the gate each phase must pass.
Then STOP and wait for my approval.

PHASE 0 (after I approve): Rojo scaffold with the roblox-dev setup skill, strict Luau, lint and format, empty client/server bootstraps, a shared Config module for every tunable number. Stop and report.

PHASE 1: STYLE TEST (this is how I approve the look and the build method)
Build a small test place, not the game:
- One lane segment (12 x 35 studs) built on the 1-stud grid from classic studded bricks, in BOTH style directions side by side: A "Modern Retro" and B "Authentic 2008" (lighting presets as separate modules so I can toggle them).
- Test both stud methods on the segment (legacy SurfaceType Studs/Inlet vs a stud MaterialVariant made by us, not downloaded) so I can compare.
- Six sample traps using the proposed colour language: Kill Brick, Disappearing Plate, Spinner Bar, Bounce Pad, Brick Wall (breakable) and TNT Brick.
- A destruction prototype: server keeps cell states and toggles collision; clients spawn pooled, client-only studded debris cubes that fly, shrink and fade; broken cells rebuild after about 6 seconds. Demo it with the Brick Wall, the TNT Brick and the Spinner Bar. Respect the debris caps in the GDD.
- A classic blocky noob NPC that walks the segment so we can see scale and kill/shatter feedback.
- Take screenshots from 3 angles per direction (and a phone-size view) and save them under Projects/Trap-Your-Friends/attachments/. Report part counts, debris counts and frame time honestly. I test on my phone myself.
Then STOP. I will pick a direction and comment, and we iterate until I say it's locked. Only then update the style guide to LOCKED with my quote.

LATER PHASES (do not start without my approval)
Phase 2: trap placement tool prototype (mobile + PC) on one segment, the biggest risk. Phase 3: round loop (build, proof run, swap run, scoring). Phase 4 onward: planned after phase 3.

ENGINEERING RULES
- Server-authoritative: the client sends intent only (place trap at cell X with rotation R; bash); the server validates phase, owner, budget, cell and cooldowns. Use the roblox-dev skills (security, architecture, strict typing, performance, testing).
- Debris and other pure visuals are client-side only. No unanchored server parts for destruction.
- Use the Roblox Studio MCP where it helps and note its quirks. Save the Studio place file; the map lives there, not in git.

END OF EVERY REPLY
- Update the matching vault notes (hub, GDD, style guide, Gap-Tracker; Verification-Log when you verify something) and end with "Vault: created/updated <note path>" or "Vault: nothing to save".
```

## Before pasting (Holden's checklist)
- [ ] Open a new Claude Code session with the vault connected and the roblox-dev plugin enabled.
- [ ] Have Roblox Studio open with the MCP connected (for the style test).
- [ ] Skim [[Trap-Your-Friends-Reference-Board]] so you know what A and B mean.
- [x] Project folder decided: `C:\Users\holde\Documents\GameDev\TrapYourFriends` (2026-10-05).
- Note (2026-10-05): this prompt was used on 2026-10-05. Holden's answers changed phase 1 to **direction A only** with two stud methods and a noob shatter demo (see the hub [[Trap-Your-Friends]]). The B parts of the PHASE 1 text above are historical.
- [ ] Say "go" only when you want building to start; the prompt stops for your approval first.

## Pitfalls
- Claude Code does not see this planning chat. Anything that matters must be in the vault.
- If decisions change, update the hub and GDD; the prompt points at them, so it needs no edits unless the process changes.

## Related
[[Trap-Your-Friends]] · [[Trap-Your-Friends-GDD]] · [[Trap-Your-Friends-Art-Style-Guide]] · [[Trap-Your-Friends-Reference-Board]] · [[Rubber-Tower-Claude-Code-Prompt]]

## Sources
- Vault CLAUDE.md working rules; planning conversation with Holden, 2026-10-05; structure follows [[Rubber-Tower-Claude-Code-Prompt]].
