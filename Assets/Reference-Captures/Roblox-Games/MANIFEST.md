---
tags: [reference/captures, project/rubber-tower]
status: draft
updated: 2026-10-04
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
