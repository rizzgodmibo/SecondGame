---
tags: [prompting/moc, meta/ai-workflow]
status: reviewed
updated: 2026-10-04
confidence: medium
---
# Prompting: How to Prompt Claude (and Other AIs) for Roblox Games

The hub for prompting. One page per part of Roblox game development, each with: what Claude needs from you, which vault notes to point it at, copy-paste prompts, how to check the result, and pitfalls. Built on 2026-10-04 from everything already in the vault, plus Anthropic's, Roblox's and OpenAI's current prompting docs.

## TL;DR
- **Read [[Prompting-Principles]] once.** Everything else applies it: give Claude a check it can run, plan before building, name exact targets and the proof, use references, link vault notes, and get a fresh-context review.
- **Copy the prompt from the page for the job,** fill or delete every `[bracket]`, and attach references for anything visual.
- **Claude proposes; Holden decides.** Prompts ask for `USER` / `PROPOSAL` tags, plan + file list before code, and no publishing, uploads, purchases, commits or messages without Holden's OK.
- **Each page ends with "How to check the result".** If a prompt has no check Claude can run itself, add one before sending.

## The skeleton (details in [[Prompting-Principles]] §1)
```text
GOAL / READ FIRST / CONTEXT / TARGET / CONSTRAINTS / DONE WHEN / PROCESS / REPORT
```

## Pages by part of game development
| Part | Page | Prompts on the page | Main check |
|---|---|---|---|
| All | [[Prompting-Principles]] | Skeleton, 14 rules, model/effort table, reusable lines | — |
| Concept, GDD, economy | [[Prompting-Concept-And-Design]] | Brainstorm grid · interview → GDD · first-60-seconds check · economy sim · design red-team | Lune economy spec, tagged GDD |
| New project, Claude Code setup | [[Prompting-Project-Setup]] | Kickoff · scaffold · repo CLAUDE.md · Studio + secrets · repeated correction → skill/hook | `gate.sh --scaffold` GATE PASS |
| Gameplay systems, data, security | [[Prompting-Gameplay-Systems]] | Plan a system · build with DevTest exploit script · saves and migrations · security review · physics | Code gate + DevTest PASS lines |
| Bugs, playtests, review, performance | [[Prompting-Debugging-And-Testing]] | Bug report · Claude playtests · phone video review · code review · phone performance | Failing repro → passing run |
| UI | [[Prompting-UI]] | Analyse reference · build in 3 passes · precise correction · phone check · blind critic loop · juice | UI checker at 4 sizes + phone |
| 3D assets, characters, maps | [[Prompting-3D-Assets-And-Maps]] | Prop set · creature anatomy-first · map plan + audit · critique → fix · upload batch | Preflight 0 FAIL, map audit PASS |
| VFX, animation, sound, lighting | [[Prompting-Game-Feel]] | VFX from blocks · retune · animation via contact sheets · sound shortlist + soundcheck · lighting pass | Phase-freeze frames, soundcheck |
| Monetisation | [[Prompting-Monetisation]] | Plan · receipt handler with failure scenarios · paid random items · compliance audit | Receipt scenarios PASS, 100k-roll odds |
| Onboarding and retention | [[Prompting-Onboarding-And-Retention]] | First 3 minutes · tutorial · daily rewards · social/invites · timed event | Fresh-save timings, DevTest day tests |
| Launch, store page, marketing art | [[Prompting-Launch-And-Marketing-Art]] | Refine icon/thumbnail · focused fix · transparent logo · store copy · launch plan | Real size/alpha checks, Holden's pick |
| Analytics, experiments, live-ops, policy | [[Prompting-Analytics-And-Live-Ops]] | Instrument · diagnose numbers · experiment plan · weekly update · incident · policy question | Funnel-order diagnosis, smoke test |
| Research and vault upkeep | [[Prompting-Research-And-References]] | Research into vault · collect references · video breakdown · verify a claim · maintenance pass | No duplicates, sourced numbers |
| Big one-shot specs, session bootstraps, Discord "master prompts" | [[One-Shot-Spec-Prompts]] | Steal an Egg spec anatomy + Holden spec skeleton, fresh-context verifier JSON prompt, Studio session bootstrap, VFX / map / polish master prompts with stop rules | Verifier total ≥ 85 and no blockers |
| What other devs actually use | [[Community-Prompt-Examples]] | 11 sourced patterns from X, TikTok, YouTube, DevForum, GitHub and Roblox docs, each rewritten for this setup | — |

Every aspect page also has a **More examples** section (4–7 shorter prompts each, about 60 in total, added 2026-10-04).

## Find a prompt by task
| I want to… | Go to |
|---|---|
| Pick or brainstorm a game | [[Prompting-Concept-And-Design]] P1, "Competitor teardown", "Names and theme options" |
| Turn an idea into a GDD / cut scope | [[Prompting-Concept-And-Design]] P2, "Cut list for a first release" |
| Set the economy, rebirth, pacing | [[Prompting-Concept-And-Design]] P4, "Rebirth / prestige numbers", "Session beats" |
| Start a project / resume / hand off | [[Prompting-Project-Setup]] P1–P2, "Resume in a fresh session", "End-of-session handoff" |
| Build combat, inventory, NPCs, quests, rounds, pets, trading | [[Prompting-Gameplay-Systems]] "More examples" |
| Save data, migrations, security review | [[Prompting-Gameplay-Systems]] P3–P4 |
| Report a bug / test / review code | [[Prompting-Debugging-And-Testing]] P1–P4, "Deprecated API sweep", "Works in Studio, broken live" |
| Build or fix a screen (HUD, shop, inventory, settings) | [[Prompting-UI]] P1–P3 and "More examples" |
| Props, trees, building kits, creatures, maps, obby stages | [[Prompting-3D-Assets-And-Maps]] + [[Community-Prompt-Examples]] §1 (spec-style item prompt) |
| VFX, animation, sounds, camera, game feel | [[Prompting-Game-Feel]] |
| Passes, products, eggs, offers, gifting | [[Prompting-Monetisation]] |
| Tutorial, dailies, codes, quests, invites | [[Prompting-Onboarding-And-Retention]] |
| Thumbnails, icons, logo, store text, clips, ads | [[Prompting-Launch-And-Marketing-Art]] |
| Read numbers, plan a test, ship an update, handle an incident | [[Prompting-Analytics-And-Live-Ops]] |
| Research, trends, tool evaluation | [[Prompting-Research-And-References]] |

## A new game, prompt by prompt
1. Brainstorm → pick ([[Prompting-Concept-And-Design]] P1).
2. Interview → GDD → red-team (P2, P3, P5).
3. Kickoff in a fresh Claude Code session ([[Prompting-Project-Setup]] P1), then the scaffold (P2).
4. One system at a time ([[Prompting-Gameplay-Systems]] P1 → P2), with bug and playtest prompts as needed.
5. Economy numbers + sim ([[Prompting-Concept-And-Design]] P4).
6. UI, art, game feel ([[Prompting-UI]], [[Prompting-3D-Assets-And-Maps]], [[Prompting-Game-Feel]]).
7. Monetisation, onboarding, analytics ([[Prompting-Monetisation]], [[Prompting-Onboarding-And-Retention]], [[Prompting-Analytics-And-Live-Ops]] P1).
8. Launch plan and store art ([[Prompting-Launch-And-Marketing-Art]]), then weekly updates ([[Prompting-Analytics-And-Live-Ops]] P4).
The [[Roblox Game Manager Skill]] runs this same order with gates and evidence in `Build-Status.md`.

## Other prompting material in the vault
- [[Prompt-Library]]: saved asset prompts (2D → 3D props, creatures, UI polish) with what worked.
- [[AI-Assisted-Workflow]]: community advice (reference-first multi-pass, model table, animation tips).
- [[Gauntlet-Loop]] and [[Shop Gauntlet Workbench]]: the builder + blind critic method and a real run.
- [[Video-SyphoDev-Claude-Code-Roblox-Workflow]] and the skill notes it produced: [[Roblox Code Gate Skill]], [[Roblox UI Checker Skill]], [[Roblox Map Audit Skill]], [[Roblox VFX Review Skill]], [[Roblox Asset Pipeline Skill]], [[Roblox Sound Library Skill]].
- Real prompts used on projects: [[Rubber-Tower-Claude-Code-Prompt]], [[Rubber-Tower-Map-v3-Critique]], `Assets/Paper Plane Toss Refined v6 Prompts.txt`.

## Pitfalls
- **Copying a prompt without filling the brackets.** Claude then invents the missing parts.
- **Using these pages as approvals.** The prompts are tools; game changes still need Holden's go-ahead.
- **Model details go out of date.** The model and effort notes are from Anthropic's docs as of 2026-10-04; re-check them when a new model ships.

## Related
[[Home]] · [[Prompting-Principles]] · [[Prompt-Library]] · [[AI-Assisted-Workflow]] · [[Game-Building-Playbook]]

## Sources
See [[Prompting-Principles]] (Anthropic, Roblox, OpenAI docs read 2026-10-04) and the Sources section on each page.
