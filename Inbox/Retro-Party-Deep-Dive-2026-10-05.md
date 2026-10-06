---
tags: [design/concepts, inbox]
status: draft
updated: 2026-10-05
confidence: low
---
# Retro Party Deep Dive: Trap Builders, Brick Telephone, Super Toppler

## TL;DR
- **Update 2026-10-05:** Holden chose Trap Builders and named it **Trap Your Friends** → [[Trap-Your-Friends]].
- Holden asked for more detail on three concepts from [[Retro-Party-Game-Concepts-2026-10-05]], plus alternate names.
- Each section covers: the fantasy, players, round flow with timings, the content list, scoring, controls (mobile + PC), modes, first session, progression, monetisation, how it works without chat, safety, tech outline, the MVP cut, risks, open questions and names.
- **Trap Builders and Brick Telephone can share one grid/stud placement tool.** Building it once covers two games, or two modes of one game (see the end).
- All numbers (timers, budgets, part caps) are **starting guesses to playtest, not decisions**. Nothing here is approved or tested.
- Style rules for all three: [[Retro-Stud-Style-Guide]]. All three need Holden's part-built exception.

---

## 1. Trap Builders

### Fantasy
"I built the meanest kill-brick lane, and I watched my friends fall into it." You're the prankster and the victim in the same round.

### Players
- 2 teams × 2–4 players (server cap 8). Solo queue fills with simple bot runners.
- Each team member **owns one segment** of the team's lane. That gives every kid their own space, avoids teammates fighting over parts, and lets a 2-player team build 2 segments each.

### Lane
- A 12-stud-wide, ~140-stud-long stud baseplate split into 4 segments. Fixed start pad, finish pad, and a checkpoint plate between segments.
- Height cap 20 studs. Build only on a 1-stud grid, rotating in 90° steps.

### Round flow (~4 min; a match = best of 3, ~12 min)
| Phase | Time | What happens |
|---|---|---|
| Theme vote | 10 s | Pick a lane skin (Classic Baseplate, Castle, Lava Factory, Candy) on pads |
| Draft | 15 s | Each player sees 5 random trap cards and keeps 3. Common traps are always available |
| Build | 90 s | Place traps in your segment with a **brick budget** (~40 points) |
| Proof run | 30 s | One builder must clear the team's lane. **Fail = all kill bricks in that segment go harmless (grey)**, and the other team gets +2 |
| Swap run | 75 s | Both teams run the other lane at the same time. Unlimited respawns at the last checkpoint |
| Fail cam | 10 s | Replay of the funniest fall + the "Meanest Trap" award |

The proof-run rule stops unwinnable walls without complex path-checking code. If your trap is unfair, you pay for it.

### Trap catalogue (launch 12, unlock to ~24)
| Trap | Cost | Notes |
|---|---|---|
| Kill Brick (Really red) | 2 | The classic. Reserved colour, never used for decoration |
| Disappearing Plate | 2 | Fades 0.6 s after touch, back after 3 s |
| Conveyor | 3 | Pushes sideways or backwards |
| Bounce Pad | 2 | Big launch. Good or bad depending on placement |
| Spinner Bar | 4 | Hinge bar, knockback |
| Push Wall | 4 | Piston on a 2 s timer |
| Ice Plate | 2 | No friction |
| Glue Plate | 2 | Walk speed ×0.3 |
| Swinging Ball | 5 | A ball on a rope across the lane |
| Falling Brick | 3 | Drops when someone is under it |
| Fan | 3 | Wind zone |
| Fake Floor | 4 | No collision. **Faint shimmer so it's readable**, which keeps it fair |
| Mystery Crate | 3 | Random each round: rubber chicken launcher, gravity patch, slow-mo pad, banana floor |
| Teleporter | 4 | Sends you back one checkpoint (max 1 per segment) |
| Truss | 1 | Builders need climbable routes too |

### Scoring
- **Runners:** +1 per segment cleared, +3 for finishing, +1 time bonus for finishing first.
- **Builders:** +1 per trap kill, **capped at 3 per trap**, so camping one trap can't farm points.
- Team score = run points + trap points. Match MVP = the player with most points.

### Controls
- **Build camera:** fixed angled top-down view of your segment (no 3D orbiting, so it's easy on phones).
- **Mobile:** tap a card → a ghost preview snaps where you tap → big **Rotate** / **Place** / **Undo** / **Delete** buttons in the thumb zone ([[UI-Layout-And-Device-Scaling]]).
- **PC:** click to place, R to rotate, Ctrl+Z to undo (classic Studio joke, and it works).
- **Run phase:** normal character controls.

### Modes
- **Classic** 2v2 / 4v4.
- **King of Traps** (free-for-all, 4–8): each player builds one segment of a single shared lane; everyone else runs it; most kills + best run wins.
- **Daily Gauntlet** (v2): a lane stitched from the meanest segments of the day. Needs saved player builds → moderation (see Safety).
- **Private server rules:** more build time, all cards unlocked, a budget slider.

### First session (first 60 s)
1. Spawn on a tiny tutorial segment with 3 kill-brick cards.
2. Place them; a bot noob runs and trips into them → "+3 Trap Kills!" with confetti and a goofy sound.
3. Then run a pre-built lane, and hit the queue.

### Progression
- XP → unlock trap cards (start 8, up to ~24) and lane themes. Unlocks come from **play only, never purchase**.
- Trap mastery stats ("Your Spinner has 412 kills"). Titles: "Kill Brick Connoisseur".
- Weekly featured card that's free for everyone.

### Monetisation (all cosmetic)
- Trap skins that everyone sees: gold kill brick, disco spinner, rainbow conveyor. Showing them off is the selling point.
- Runner trails and fail-cam emotes.
- Private servers.
- ⚠️ Never sell trap power or cards. Paying to win in a build-versus game kills it fast ([[Monetisation-Design-Checklist]]).

### Without chat
- Team pings on the lane ("Trap here!", "Go left"), segment ownership (no need to coordinate), and votes on pads.

### Safety
- Builds use **fixed trap pieces on a grid**, so the risk of drawing shapes is low but not zero. Cap ~25 pieces per segment, add a report button on the fail cam, and keep builds visible only to the current server in v1.

### Tech outline
- `ReplicatedStorage/Traps/<TrapName>`: template model + a behaviour module tagged via CollectionService.
- Client sends `PlaceTrap(cardId, cellX, cellZ, rot)`. The server validates the phase, segment owner, budget, free cell and height, then clones the template ([[Anti-Exploit-And-Server-Authority]]: rate limit, validate everything).
- Kill detection is server-side (touch → reset to checkpoint, credit the trap owner).
- Lanes rebuild every round from an empty template, so few parts stay in the world.

### MVP cut (first playable)
1 lane theme, 8 traps, fixed budget (no draft), proof run, Classic 2v2/4v4, scoring, fail cam. Leave out: modes, saved lanes, unlocks.

### Risks
- **Mobile build UX** is the make-or-break part. Prototype it first.
- Builders who don't place anything (auto-fill the empty segment with 3 basic traps so runners still have fun).
- Rounds feeling samey (Mystery Crate + weekly cards + themes).

### Open questions
- Should segments be private (surprise traps) or visible to the other team during build (counter-building)?
- Bots: allowed in public servers, or only to fill tiny servers?

### Name ideas
**Trap Swap** · **Kill Brick Clash** · **Build to Break** · **Prank Lane** · **Trap Trade** · **Brick Traps!** · **Spike Your Friends** · **Death by Brick** · **Trapsmiths** · **Lane Pranks**
*My pick: **Kill Brick Clash** (the classic hook is in the title) or **Trap Swap** (explains the game in two words).*

---

## 2. Brick Telephone

### Fantasy
The telephone game, but with bricks. "A sleepy shark driving a bus" turns into "a blue sofa on fire" after three builders. The reveal is the joke.

### Players
- 4–10 players, best at 6–8. Server cap 10.
- Small servers fill with **dev-made bot builds**: a hand-built library of builds for common prompts, so there's no moderation risk.

### Prompts: no free text
- Players **build prompts from word tiles**: [adjective] + [thing] + [doing] ("a *sleepy* *shark* *driving a bus*"), or pick 1 of 3 ready-made prompt cards.
- Every word comes from curated lists, so there's no chat, no typing on mobile and no filter fights. Roblox requires filtering of player-typed text shown to others, and this avoids typed text entirely (Roblox safety docs).
- Target: ~150 adjectives × ~200 things × ~100 actions, curated for funny and buildable.

### Round flow (8 players ≈ 12 min)
| Phase | Time | What happens |
|---|---|---|
| Prompt | 20 s | Make a prompt from tiles (or take a card) |
| Build | 75 s | Build it on your personal 16×16 stud plot (cap 60 parts) |
| Guess | 25 s | The previous player's build spins on a turntable. Assemble a guess from a tile bank (the right words mixed with close decoys) |
| Build | 75 s | Build what the previous player *guessed* |
| … | | Alternate build/guess until each chain is ~6 steps |
| **Reveal Show** | ~40 s per chain | Prompt → build (turntable) → guess → build … plays back with drumrolls and sound effects; the audience hits reaction buttons |
| Awards | 15 s | "Best Build", "Biggest Plot Twist", "Most Accurate" voted on pads |

### Build kit
- Parts: Brick, Plate, Wedge, Cylinder, Ball, Truss, plus a few **special pieces** (wheel, crown, flag, fire).
- The 20-colour palette from the style guide.
- **Sticker faces:** classic-style eyes and mouths you can slap on any brick. This is where the comedy comes from: a cylinder with a face is a character.
- Part cap 60, so builds stay quick and readable.

### Scoring
- **Guessers:** +1 per tile matching the previous prompt, +2 for a perfect match.
- **Builders:** +2 if the next guesser gets ≥ 2 tiles right (rewards readable building).
- **Reactions:** +1 per 😂 or 🔥 from other players (capped).
- Points matter less than the reveal. Keep the scoreboard light.

### Controls
- **Face-placement building** (Minecraft-style): tap any face to put the selected part against it; stud snap means no fiddly positioning. This is the best fit for phones.
- Buttons: Part picker, Colour, Sticker, Rotate 90°, Undo, Erase. Orbit the camera with a one-finger drag.
- PC: click to place, R to rotate, Ctrl+Z to undo, number keys for parts.

### Modes
- **Classic Chain** (above).
- **Speed Chain:** 40 s builds, 3-step chains. Better for short mobile sessions.
- **Copycat:** see a build for 10 s, rebuild it from memory, and score on similarity (auto-scored by part type and colour per grid cell).
- **Masterpiece:** 3 players add 20 parts each to one build in turn, without knowing the prompt.
- **Team Telephone:** two teams race to keep a message intact down their chain.

### First session (first 60 s)
1. Prompt: "a tree" (fixed for the tutorial).
2. Five green bricks and one brown cylinder, done in ~20 s → "Nice build!" with a sticker-face tip.
3. A bot guesses "a green tower" → mini reveal → into the lobby.

### Progression
- XP → unlock prompt packs (Animals, Food, Space, Memes), sticker faces and special pieces, all earned through play.
- **Album:** your chains are saved privately (visible only to you) so you can rewatch them. Sharing in v2 (see Safety).
- Titles: "Brickasso", "Master Misunderstander".

### Monetisation (cosmetic)
- Sticker-face packs, turntable stands, reveal-show sound packs (airhorn, sitcom laugh).
- Extra prompt packs are a grey area: they change content, not power, so it's acceptable, but keep the base set large.
- Private servers (choose packs and timer lengths).

### Without chat
Built in from the start: tile prompts, tile guesses, reaction buttons, pad votes. Voice chat just makes the reveal louder.

### Safety (the hardest part of this concept)
- Players can build inappropriate shapes with any building tool. Developers are expected to manage this risk (Roblox safety docs).
- v1 mitigations:
  - 60-part cap and small plots.
  - Builds exist only inside the current server and are deleted at round end.
  - A **report button + "hide this player's builds"** in the reveal.
  - Kick and Ban APIs for confirmed abuse.
  - No public gallery.
- v2 (shareable albums, "featured builds"): only once Roblox's developer moderation API for player-made content is available. A Roblox AMA said an alpha was coming (as of Sep 2025). ⚠️ verify its current status.

### Tech outline
- Plot = a model with a grid map `{[cell]: {part, colour, rot, sticker}}` stored on the server. The client sends `PlacePart(cell, face, partId, colour, rot)`, and the server validates it.
- Saving a build = serialising that small table. The reveal re-spawns builds from the table onto turntables (cheap, no instance cloning across servers).
- Chain logic is a pure module (easy to unit test, see unit tests).
- Copycat scoring = compare the grid maps.

### MVP cut
Classic Chain, 4–8 players, tile prompts and guesses, 6 basic parts + palette + 10 stickers, reveal show, awards, report button. Leave out: modes, album, unlocks.

### Risks
- **Needs a full lobby.** Empty or tiny servers are dead (bots + a 4-player minimum + Speed Chain for small groups).
- The reveal drags when chains are long (cap 6 steps; allow skipping a chain by majority vote).
- Prompt quality decides whether it's funny, so it needs lots of writing and curation.
- Moderation, as above.

### Open questions
- Free-text guessing for age-checked players, or always tiles? (Tiles are simpler and safer, and I'd suggest tiles only.)
- Reveal in one big theatre, or each player's own camera?

### Name ideas
**Brick Telephone** · **Telebrick** · **What Did You Build?!** · **Mis-Brick-Communication** · **Build It Back** · **Brick Whispers** · **Lost in Building** · **Stud Telephone** · **Broken Bricks** · **Block Rumors**
*My pick: **What Did You Build?!** (it reads as a joke on a thumbnail) or **Telebrick** (short and memorable).*

---

## 3. Super Toppler

### Fantasy
Classic brickbattle (four brick towers, explosions, chaos), except every round hands out ridiculous gear. The goal is to **knock their tower over**, not to rack up kills.

### Players
4 teams × 1–4 (server cap 16), or 2 teams × up to 8.

### Map and towers
- Four brick towers on a classic baseplate over the void, plus a central island with a gear pickup.
- Towers are ~400–800 classic parts, **joined by welds/surfaces that explosions break**. Each team's spawn plates sit at the top. Knock them into the void and that team is out.
- Tower variants, picked by vote: Classic Spire, Castle, **Giant Noob Statue** (topple the noob!), Pizza Tower, Upside-Down Pyramid, Jelly Tower (bouncy).

### Round flow (~5 min)
| Phase | Time | What happens |
|---|---|---|
| Deck reveal | 10 s | A slot-machine spin shows this round's **Silly Deck**: 4 gears + 1–2 modifiers |
| Fortify | 30 s | Builders' trowel time: patch and add walls |
| Battle | ~4 min | Topple towers. Respawn in 3 s while your spawns still exist |
| Sudden Death | 30 s | Baseplate shrinks / lava rises if more than one team survives |
| Results | 10 s | Slow-mo replay of the biggest topple |

### Silly Deck: gear pool (4 per round, everyone on a team gets the same)
| Gear | What it does |
|---|---|
| Rubber Duck Rocket | Rocket launcher; big knockback, quacks, breaks bricks |
| Mega Superball | House-sized bouncy ball that wrecks walls |
| Friend Slingshot | Launch a teammate as the projectile; they smash bricks on impact |
| Confetti Timebomb | Explodes into 200 loose 1×1 bricks that bury a tower top |
| Wrong Trowel | Builds a wall… of jelly, or a wall facing the wrong way 20% of the time |
| Bonk Sword | Barely any damage, huge knockback |
| Magnet Glove | Rips loose bricks off enemy towers |
| Plunger Grapple | Swing between towers |
| Paint Bucket | Paints enemy bricks your colour. Painted bricks don't hurt your team (an area-denial tactic) |
| Classic Rocket / Bomb / Superball / Sword | The "normal" deck that sometimes appears for nostalgia |

### Modifiers (1–2 per round)
Low Gravity · Giant Mode (everyone 3×) · Tiny Mode · Everything Is Bouncy · Rockets Only · Lights Out (neon-only night) · **Tower Swap** (at 2:00 every team teleports to another team's tower) · Earthquake · Rain of 2×4s.

### Combat tuning for a nonsense game
- Lots of knockback, low damage, 3 s respawn. Falling into the void is the main way to die, and that's funny, not frustrating.
- Score = **towers toppled + spawns destroyed**, not kills. A sweaty sword player can't carry the round alone.
- The random decks stop the strongest players from mastering one loadout.

### Controls
- **Mobile:** gear hotbar (max 4 slots), aim with the camera, one big fire button. Tune auto-aim assist for projectile gear. ⚠️ playtest on a phone early.
- **PC:** classic 1–4 hotbar, click to fire.
- **Console** later: radial gear wheel.

### Modes
- **Classic Four** (4 teams), **Two Towers** (2 big teams).
- **Topple the Noob** (co-op PvE): everyone vs one giant noob tower that throws bricks back. Good for small servers and new players.
- **Lone Towers** (free-for-all): every player gets a tiny tower.
- **Custom Deck** (private servers): pick gears and modifiers.

### First session (first 60 s)
1. Spawn in a short "Topple the Noob" tutorial: one gear (Rubber Duck Rocket), a small noob tower.
2. Three shots → the tower collapses in slow-mo → "TOPPLED!" banner.
3. Queue into Classic Four.

### Progression
- XP → gear skins, kill/knockback effects (cartoon stars, a "bonk" text pop), team flags for your tower, emotes.
- **Gear Index:** a collection page of every silly gear and modifier you've played with, which gives a reason to keep queueing.
- Weekly "Featured Gear" (a new silly gear every week, cheap content: [[Content-Cadence]]).

### Monetisation (cosmetic)
- Gear skins, impact effects, tower flags, victory dances, private servers with Custom Deck.
- ⚠️ Never sell gear power. Classic gear existed as Roblox catalog items, so **build our own models and names**. Don't reuse Roblox's catalog assets or the "Doomspire" name.

### Without chat
- Ping wheel ("Attack Red!", "Defend!", "Need trowel!"), team-colour arrows pointing at the weakest enemy tower.

### Tech outline
- Towers are templates cloned each round; parts start anchored with welds. An explosion or impact breaks joints in a radius on the server, and broken bricks become unanchored debris.
- **Performance budget:** ~3k tower parts total; cap live debris at ~1,000–1,500 unanchored parts; fade and delete debris after 8–10 s; test on a low-end phone early.
- **Anti-exploit:** physics parts can be flung by exploiters when clients own them. Give tower debris to the server (`SetNetworkOwner(nil)`) at the cost of server load. Damage and knockback are computed on the server ([[Anti-Exploit-And-Server-Authority]]).
- Gears are modules sharing one projectile system; a modifier is a function applied at round start.

### MVP cut
One tower type, Classic Four, a 6-gear pool (4 silly + 2 classic), 3 modifiers, toppling + void elimination, Sudden Death. Leave out: Topple the Noob, Custom Deck, the index.

### Risks
- **A crowded niche:** Super Doomspire (Polyhex) and Crossroads-style remakes already serve classic brickbattle players. The silly deck must be the reason to choose this one.
- Physics cost on mobile; exploiters with physics.
- PvP can feel bad for young players (fix with knockback-first tuning, co-op mode, bots in small servers).

### Open questions
- Should toppled teams spectate, or rejoin as "ghost saboteurs" with one silly ability?
- Fortify phase: keep it, or let the trowel be just a gear?

### Name ideas
**Super Toppler** · **Topple Town** · **Tower Tumble** · **Bonk Towers** · **Kaboom Castles** · **Brick Brawl** · **Knock Your Block Off** · **Timber Towers** · **Wobble Wars** · **Topple Trouble**
*My pick: **Knock Your Block Off** (funny, says exactly what you do) or **Tower Tumble** (short and clean for an icon).*

---

## Comparison of the three (judgement, not tested)
| | Trap Builders | Brick Telephone | Super Toppler |
|---|---|---|---|
| Hardest part | Mobile build UX | Moderation + needing a full lobby | Physics performance + crowded niche |
| Fun with 2 players | Yes (1v1) | Weak | OK (co-op noob mode) |
| Session fit | 12-min matches | 10–15-min games | 5-min rounds (best for drop-in) |
| Content cadence | New trap card weekly | New prompt pack weekly | New silly gear weekly |
| Scope (solo dev + Claude) | Medium | Medium | Medium–high |

## Idea: one game, three modes?
Trap Builders and Brick Telephone use the **same grid + stud placement tool**. A "Brick Party" hub with *Trap Swap* and *Telebrick* as two queues shares one build system, one palette, one UI kit and one player base. **Ship one mode first and prove it's fun before adding the second.** Super Toppler shares less (physics and combat) and works best as its own game.

## Pitfalls
- No ranking guarantees success. Pick the one whose 2-minute prototype makes you laugh in a playtest.
- Don't use Roblox's own brand names or assets (Doomspire, Tix, Builderman, classic catalog gear). ⚠️ verify Roblox brand rules before using any classic references.
- Party games die in empty servers. Bots and small server caps are not optional.

## Related
[[Retro-Party-Game-Concepts-2026-10-05]] · [[Retro-Stud-Style-Guide]] · [[Friend-And-Group-Play]] · [[Session-Length-And-Pacing]] · [[Onboarding-And-First-60-Seconds]] · [[Content-Cadence]]

## Sources
- Roblox Wiki, Super Doomspire (team elimination by destroying spawns/towers, Sudden Death, gear: rocket, sword, superball, bomb, trowel; modes) — https://roblox.fandom.com/wiki/Doomsquires/Super_Doomspire
- Mechanics of Magic, "MDA: Gartic Phone" (prompt/draw/guess chain, timers, sequential reveal, imperfection as the fun) — https://mechanicsofmagic.com/2024/04/07/mda-garticphone/
- Roblox Creator Docs, Safety (manage player content: pre-moderation, temporary content, limits; text filtering required; Ban/Kick APIs) — https://create.roblox.com/docs/safety
- Devforum, "Detecting inappropriate builds and UGC by players in-game" (moderation tactics; Roblox AMA on a moderation API alpha) — https://devforum.roblox.com/t/detecting-inappropriate-builds-and-ugc-by-players-in-game/3930427
- All fetched 2026-10-05. Brainstorm with Holden, 2026-10-05.
