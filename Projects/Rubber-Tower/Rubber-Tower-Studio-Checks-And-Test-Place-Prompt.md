---
tags: [project/rubber-tower]
status: final
updated: 2026-10-05
---
# Rubber Tower: finish the title system gaps → Studio checks → test place (prompt)

Paste the block into Claude Code.

```
Good work on the title system. Next steps, in order:

1. CLOSE THE GAPS YOU CAN NOW
- Pay the checkpoint Squishies (CP1 50 / CP2 75 / CP3 100 / Summit 200, once each) and the +20 replay reward (once per day), session-only like the titles. Log them to Output and show the total in the dev panel, same as the title payouts.
- Squishmaster (climb again after the summit), my decision:
  - At the summit, add a goofy way back down: a "Leap of Faith" edge/launch pad where you jump off the top and ragdoll-fall all the way down to the ground floor (it also triggers Long Way Down). Add a soft landing zone at the bottom.
  - A new run starts when you leave the ground floor. A run only counts toward Squishmaster (and the +20 replay reward) if the server's climb trace shows you climbed it, with no teleport up the tower during that run (teleporting DOWN is fine).
  - If this needs a model (a summit launch pad / diving board, a landing pad), add it to the kit in the v5 style.
- The other hooks (shop, skip pass, dailies, hand-up, shove, banana peel titles) stay as one-line hooks until those features are built. That's fine.

2. STUDIO CHECKS (before any upload)
- Check the 3 unconfirmed things: the Nunito Heavy font loads, the server sees the first-jump state (Wobbly Beginner), and the real emote animation names for Disco Duck. Fix whatever fails.
- Run a 2-player test (like the ragdoll test) to check titles show for other players, LOD and declutter work, and payouts happen once.
- Tell me what passed and failed.

3. TEST PLACE UPLOAD
- You have my OK to upload to the PRIVATE test place only: the kit (batches a–h), the 39 hats and the 12 title icons. Nothing public. Swap the emoji/text placeholders for the real icon images once they're uploaded.
- Then test and screenshot:
  - Hats on real avatars, R6 and R15, a few head shapes and big hair: nothing floating or badly clipping.
  - Hats + titles during ragdoll: the hats stay on, the wobble parts jiggle, the title stays above the hat without spinning.
  - Titles above the tallest hats (tower, castle, planet).
  - 16 dummies with titles + hats on the phone emulator at ~30 studs, plus FPS/memory numbers. Then I'll do a real phone test myself.
- Show me the screenshots and an honest pass/fail list, then stop for my review.

4. AFTER MY REVIEW (just plan it, don't start)
- The next big step is building the map with the kit: ground floor + segment 1 first (as I asked in the v3 critique), using the obby pieces, then stop for review. Write a short plan for that.

Keep the vault updated ([[Rubber-Tower]], [[Rubber-Tower-Build-Status]], [[Rubber-Tower-Title-UI]], [[Rubber-Tower-Squishies-Economy]], [[Rubber-Tower-Valley-Kit]]), with today's real date.
```
