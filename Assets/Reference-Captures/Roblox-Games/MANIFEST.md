---
tags: [reference/captures, project/rubber-tower]
status: draft
updated: 2026-10-05
confidence: high
---
# Roblox game-page screenshots (manifest)

**What this is:** the game-page media carousels for the obbies in [[Rubber-Tower-Reference-Obbies]], plus stylised climb games and Fisch (for surface detail). They were captured for the Rubber Tower v5 art test. The analysis is in [[Roblox-Obby-Surface-References]].

**Capture details (2026-10-04):**
- **Method:** the public endpoints `apis.roblox.com/universes/v1/places/<placeId>/universe` and `thumbnails.roblox.com/v1/games/multiget/thumbnails?universeIds=…&size=768x432&format=Png`.
- **Format:** PNG, 768×432 each.
- **Inspection:** stills inspected as contact sheets.
- **What they show:** the developers' own thumbnails. Some are in-game screenshots and some are edited marketing art (text, effects, posed avatars). They are not verified gameplay captures.
- **Rights:** third-party artwork, kept local (gitignored). Use for study only, never as game assets.
- **Search:** climb games were found with `apis.roblox.com/search-api/omni-search` for "only up", "fantasy obby" and "climb tower obby".

| Folder | Place id | Universe id | Files (SHA-256, first 12) |
|---|---|---|---|
| Chained-2-Player-Obby | 18334179599 | 6215464786 | screen-1.png `e0ef130cbf9d` |
| Chained-Together | 18152595062 | 6153964325 | screen-1.png `02fdeec090aa` |
| Dash-World | – | 7877723741 | screen-1 `1f0f315cbd38`; screen-2 `c6c210d80733` |
| Fisch | 16732694052 | 5750914919 | screen-1 `f8bff638bb5f`; 2 `020d7ce0bc28`; 3 `4ba6838d4406`; 4 `89d08577600f`; 5 `78e7b41262cc`; 6 `f8141567a364`; 7 `dd47761ecaae`; 8 `c48f7d2b930b`; 9 `92ba0c1d57c2` |
| Glide-Tower | – | 7658676858 | screen-1 `cb5d717d660e` |
| New-Only-Up | – | 4769153665 | screen-1 `8e4fa235be82`; 2 `f6a7986a2541` |
| ONLY-UP | – | 4767935649 | screen-1 `dbe3f41f8565`; 2 `a1fbf520b108`; 3 `f54187e141d7`; 4 `c6a252fb34ec` |
| Parkour-Spiral | – | 6709042729 | screen-1 `b2f9f7def16f`; 2 `d23f4bcde1cc`; 3 `48abab355d5c` |
| Phonk-Edit-Tower | 101480963912212 | 9296252245 | screen-1 `8b64464aca3b` |
| Ragdoll-Physics-Tower | 81823526068423 | 8490155346 | screen-1 `a7da0273edd6`; 2 `9263806f2443`; 3 `046c7950d6f4` |
| Squishy-Troll-Tower | 82648796375761 | 10704015784 | screen-1 `87414fddb565`; 2 `a17a6397a6a2`; 3 `a98111efa30e` |
| TROLL-Hug-Tower | 103037106396302 | 10460801145 | screen-1 `32509e89ad08`; 2 `32c6d98fabad`; 3 `6031afca226a`; 4 `6312301ee4f3`; 5 `afcd90576b71` |
| Tower-Of-Sky | – | 4703261723 | screen-1 `81fb2b66f8df`; 2 `fe496d8011f5`; 3 `60670e488fce`; 4 `57956a74d236`; 5 `0acf533b05ef` |
| Tower-of-Hell | 1962086868 | 703124385 | screen-1 `879453b18216`; 2 `507441de1f74`; 3 `53dbf010ec76` |
| Troll-Ragdoll-Tower | 139788637490504 | 7609824898 | screen-1 `c0ef695e58cf`; 2 `c6016164230a`; 3 `dc2311f96794`; 4 `453d0897b064`; 5 `c97acc8c0484`; 6 `5af6425863b3` |

The place ids marked "–" were not looked up: those games came from search results by universe id.

`../Holden-Picks/` is where Holden drops his own screenshots. **They outrank everything here.** That folder was empty on 2026-10-04.

**Added 2026-10-05: fantasy-shop references, for the Rubber Tower cosmetics shop redo** (Holden: "use references from other games"). Same capture method. The most useful are **Islands** screen-2/6/7 (half-timber + stone shops, purple door, lanterns, banners, an open counter) and Fisch screen-2.

| Folder | Place id | Universe id | Files (SHA-256, first 12) |
|---|---|---|---|
| Bee-Swarm-Simulator | 1537690962 | 601130232 | 1 `7f79b07cebcc`; 2 `f9c3b7f1c075`; 3 `7e0c837463e2`; |
| Grow-a-Garden | 126884695634066 | 7436755782 | 1 `c8789713ecab`; 10 `5a2a010d4a8d`; 2 `d1865c757f8b`; 3 `56fdc08e8491`; 4 `b2b2383e82a0`; 5 `10a67e3a900b`; 6 `2cdc8e90ca94`; 7 `08977cde1a7a`; 8 `eb820460172a`; 9 `69a4ad5956cb`; |
| Islands | 4872321990 | 1659645941 | 1 `fe789b452a55`; 2 `e713d4c50232`; 3 `e7cbfc53f4c2`; 4 `5c57def2680e`; 5 `4668f22e7a13`; 6 `9631ef209f6e`; 7 `578bc0eeb212`; 8 `c7ad9825ebcc`; 9 `30936d5891b0`; |
| World-Zero | 2727067538 | 985731078 | 1 `a8f8c9e77169`; 2 `85bd1c4ea3ad`; 3 `118d22af93eb`; 4 `7c11156c161a`; |
| Arcane-Odyssey | 3272915504 | 1180269832 | 1 `8a8b2d3be3e3`; 2 `6c008b5d0182`; 3 `2bbea90649b7`; 4 `464b82994b38`; 5 `7689f538677a`; 6 `4a48d46ee0e4`; 7 `55039da256d1`; 8 `d4e842b7765d`; 9 `1e0f8cd130c5`; |
| Adopt-Me | 920587237 | 383310974 | 1 `0de9b8af27d5`; 2 `80c8116b9dc1`; 3 `9b10a93059f2`; 4 `8de7a49d2f6d`; 5 `0bd460569340`; 6 `ab1ca512f38f`; |
| Dungeon-Quest | 2414851778 | 848145103 | 1 `b9518467fadf`; 2 `2cf5ead9b251`; 3 `b31a35664a5e`; 4 `892b63ec9a03`; 5 `aa7a577b4c05`; |
