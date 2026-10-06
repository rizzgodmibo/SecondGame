---
tags: [project/rubber-tower, design/level]
status: final
updated: 2026-10-05
---
# Rubber Tower: map plan answers + finish the test (prompt)

Paste the block into Claude Code (after the phone emulator shots finish).

```
Answers to your 4 map questions (record as USER in [[Rubber-Tower]] and [[Rubber-Tower-Map-Build-Plan]]):
1. Footprint: keep 240×240 and 100 studs per segment for now (my "for now" from the v2 answers). If the dev timer shows S1 is under the 5–8 minute target, make the ROUTE longer (more zigzag, wall runs, more height per jump section), not the valley wider. Tell me if you think a segment needs more than 100 studs of height.
2. Leap landing: next to the start plaza so replays are fast (Squishmaster), but in its own "splash zone": land in the pond, with soft jelly/cushion pads around it, so players never land on someone spawning. Make the splash a fun moment (a big splash/boing). Keep the full lane clear from the summit to the pond at every height.
3. Shops: YES, place them on the ground floor now (placement only, not wired), so we can judge the hub as a whole: the cosmetics hat shack, the Caravan gamepass shop, and the other hub structures. Leave space for the halfway shop at CP2 later.
4. Player hats: while a game hat is equipped, hide the player's own HAT accessories only (keep hair and everything else), and restore them when the game hat comes off. Hats perching on big hair is normal Roblox behaviour, so that's fine.

Before the map build, finish the test items:
- Finish the 16-dummy phone emulator shots at ~30 studs and get real client FPS with Studio visible. I'll do the 2-player test and a real /e dance for Disco Duck myself; give me a short checklist of what to look for.
- Fix the weak spots from the playtest:
  - TP_Top_Hat: swing the paper streamer to the side/back so it doesn't cover the face.
  - Leap pad: make it bigger and clearly readable on the summit, and tune it so a standing player gets a proper launch too (not just a hop on the tip).
  - The TexturePack 429 upload errors: check the textures still load after the rate limit resets.
- Small titles: leave TitleUI.BaseScale as is until my phone test.

Then GO on the map build: follow [[Rubber-Tower-Map-Build-Plan]] (layout sketch first, and stop if I want changes, then ground floor + S1 + CP1, audit, timer, 4 angles, before/after, honest self-critique, stop for my review). Delete Workspace.TestPlace.LeapTest only once the real leap lane works. Keep the vault updated, with today's real date.
```
