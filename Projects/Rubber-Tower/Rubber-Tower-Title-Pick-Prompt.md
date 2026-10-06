---
tags: [project/rubber-tower, visuals/ui]
status: final
updated: 2026-10-05
---
# Rubber Tower: title style pick → fixes → move on (prompt)

Paste the block into Claude Code.

```
Title decisions (record as USER in [[Rubber-Tower]] and [[Rubber-Tower-Title-UI]]):
1. Style: C Clean Text, but make it slightly smaller overall (about 10–15% smaller than the mockup).
2. My own title: YES, it shows above my head (keep it a bit smaller than other players' like the mockup).
3. Legendary price: DON'T raise it. Keep the economy as it is.
4. Title list: you come up with the final names, rarities and how to get each one. Use your name ideas plus the current 27, keep the ones that work, replace weak names, keep the approved ones (summit without checkpoints, push 5+ players, invite friends / 3 friends in the server, first cosmetic, Millionaire / False Conqueror joke titles). Same 6 rarities and the locked payouts (Common 25, Uncommon 75, Rare 75, Epic 150, Legendary 300, Mythic 300). Short names (max ~16 characters), funny and goofy for young teens. Anything cheatable is checked on the server. Put the final list in Config and the vault. If I want more titles later, I'll ask.

FIX THE WEAK POINTS FIRST
- Style C's own weak points (from your honest read):
  - Common and Rare look plain. Give every tier something besides colour: e.g. a small rarity gem/dot or a thin underline bar next to the text, a subtle shine on Rare, so it still reads at a glance. Keep it light; C's strength is that it's clean in crowds.
  - Gradient text needs a thick stroke: make sure every tier stays readable over grass, sky, cliffs and snow (test it on all 4 segment backgrounds in the mockup).
  - Keep the category badge small so C stays light.
- Any other weak points still open from your last self-critique (batch h fixes, mockups): fix them too, or tell me why one can't be fixed yet.
- Render ONE updated style C mockup (smaller, fixed) with the final title list on the rarity ladder, over a crowd of 4–5 players, and show me. If it's good, I'll say go.

THEN MOVE ON
1. Write the plan + file list for the title system (TitleService on the server, TitleController on the client, the Titles menu with locked / unlocked / equipped states), following my rules: plan first, I approve, then code. Use the spec already in [[Rubber-Tower-Title-UI]] (distance LOD, declutter, offset above tall hats, StudsOffsetWorldSpace for ragdoll, server-validated EquippedTitle).
2. After that, the next big step is the test place: upload the kit and check the hats on real avatars, the hats + titles during ragdoll, and the titles with 16 dummies on a phone. Ask me before uploading anything.
3. Keep the vault updated ([[Rubber-Tower]], [[Rubber-Tower-Build-Status]], [[Rubber-Tower-Title-UI]], [[Rubber-Tower-Squishies-Economy]]). Use today's real date in notes.
```
