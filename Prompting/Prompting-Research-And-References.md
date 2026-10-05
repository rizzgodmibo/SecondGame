---
tags: [prompting/research, reference/process, meta/vault]
status: draft
updated: 2026-10-04
confidence: medium
---
# Prompting: Research, Reference Gathering and Vault Upkeep

How to ask Claude to research a topic, collect references from X/YouTube/TikTok, break down videos and keep the vault clean. General rules: [[Prompting-Principles]].

## TL;DR
- **Define success and the evidence types up front:** what counts as an answer, and keep verified platform facts, library behaviour, local observations, Holden's decisions, recommendations and open questions separate (vault CLAUDE.md; Anthropic's research guidance).
- **"Search the vault first; update, don't duplicate"** goes in every research prompt. Every reference pass so far started by checking what already existed (the X, YouTube and TikTok libraries were all deduplicated against each other).
- **Ask for honesty about what was actually seen:** "watched in full", "read the transcript", "viewed frames" vs "found in search, not opened" ([[Video-SyphoDev-Claude-Code-Roblox-Workflow]], [[Blender 3D Logo Pipeline]] sources).
- **Third-party media stays local.** The vault repo is public, so captured images and videos are gitignored; notes describe and link them ([[Reference-Capture-Process]], `.gitignore`).
- **For contested or time-sensitive claims, ask for "⚠️ verify:" plus the exact source to check,** and log real verifications in [[Verification-Log]].

## What Claude needs from you
- The question and what you'll do with the answer (decide a feature, set a price, copy a UI pattern).
- Where to look and what's off limits (sites you're signed in to; no posting, liking or following).
- The output: which note to update or create, and the folder.

## Vault notes to point Claude at
| Note | Gives Claude |
|---|---|
| `CLAUDE.md` (vault) · [[Home]] · [[Gap-Tracker]] | Note format, evidence types, folder map, what's due next |
| [[Reference-Capture-Process]] · [[X-Reference-Library]] · [[YouTube-Reference-Library]] · [[TikTok-Reference-Library]] | How captures are stored, named and deduplicated; what's already captured |
| [[Video-Breakdowns]] · [[Video Frame Extraction with Blender]] | Breakdown format with timestamps; frames without ffmpeg |
| [[Verification-Log]] · [[Sources]] | Where verified claims and trusted sources go |
| [[Gauntlet-Loop]] | Example of a well-sourced method write-up (original prompt, guide, testers, cautions) |

## Prompts

### 1. Research a topic into the vault
```text
Research [TOPIC] for my Roblox vault. Goal: [the decision this informs].
1. Search the vault first (grep -ri) and read what exists. Update existing notes; only create a new note if nothing covers it, in the right folder with the frontmatter from CLAUDE.md, linked from the folder's _Index or Home.
2. Prefer official sources (create.roblox.com, Roblox DevForum announcements, library docs); use community posts for practice, labelled as such.
3. Keep evidence types separate: verified platform fact (with source and date), library behaviour, local observation, my decisions, recommendations, open questions. Numbers need a source and date.
4. Track competing explanations and your confidence as you go; if sources disagree, say so and mark it "⚠️ verify:" with what to check.
5. Sources at the bottom. Log anything you verified in Meta/Verification-Log.md and update Meta/Gap-Tracker.md.
End with "Vault: created/updated <paths>".
```
Why: Anthropic's research guidance (clear success criteria, cross-checking sources, competing hypotheses, confidence tracking) mapped onto the vault's own note rules.

### 2. Collect references from X / YouTube / TikTok
```text
Collect the best Roblox references for [TOPIC: e.g. shop UI, hatch animations] from [X / YouTube / TikTok]. I'm signed in; don't like, follow, post or message anyone.
- Check the existing libraries first and skip anything already captured (same post, same video re-uploaded, same creator tip).
- For each keeper: link, creator, date, stats when captured, and a 1–2 line takeaway saying what to copy and what not to (dark patterns, AI-generated art, policy problems).
- Save media under Assets/Reference-Captures/[source]/ (gitignored, third-party) and write the catalogue into the matching Reference note.
- Say how many results you looked at and how many you kept, and why the rest were skipped.
```
Why: this is how 306 X posts, 26 YouTube and 26 TikTok references were gathered without duplicates ([[X-Reference-Library]]).

### 3. Break down a video
```text
Break down this video: [URL]. Watch/read it in full: the transcript plus frames every [5] s as contact sheets, and key frames at full size.
Write a note with: what it is and the evidence type (tutorial, self-report, ad for a course?), chapters with timestamps, the claims that matter with ✅ when you verified them at an official source and ⚠️ when you couldn't, how it maps onto my setup (a gap table), and what conflicts with my rules. Frames stay local (gitignored). Say exactly what you watched vs skimmed.
```
Why: the SyphoDev breakdown followed this and separated five verified facts from the creator's unverified workflow claims ([[Video-SyphoDev-Claude-Code-Roblox-Workflow]]).

### 4. Verify a claim
```text
Verify this claim from [note]: "[claim]". Check the official source (Roblox docs, creator-docs on GitHub, the library's own docs). Report: confirmed / contradicted / unclear, with the exact source and the date you checked. Update the note (remove or keep the ⚠️, fix the number) and add a row to Meta/Verification-Log.md.
```

### 5. Vault maintenance pass
```text
Do one vault maintenance pass. Read Meta/Gap-Tracker.md and take the next area in the rotation. Close one gap, verify one claim, or refresh one stale note (older than 180 days with time-sensitive claims → status: stale). Don't create duplicate notes; fix broken wikilinks you touch. Update Gap-Tracker with what you did and what's next.
```

## More examples (added 2026-10-04)
Shorter prompts for other common jobs. Same rules: fill every bracket, keep the check. Sourced patterns are credited in [[Community-Prompt-Examples]].

### Trend check before committing
```text
Is [trend/genre] still rising? Check current stats sites and Roblox Charts, plus recent TikTok/YouTube activity, and tell me where it is in the lifecycle (spark, breakout, copycat flood, consolidation, decay) per Growth/Genre-Positioning.md. Sources and dates for every number; say clearly what you couldn't verify.
```

### Mine a skill pack or prompt collection for ideas
```text
Read [repo/blog] (don't install anything). List the prompts, workflows and checks in it that our vault doesn't already have, with a one-line take on each and whether it conflicts with Holden's rules. Add the useful ones to the right Prompting page, paraphrased and credited.
```
How [[Community-Prompt-Examples]] was built.

### Watch a showcase post critically
```text
Look at this "made with AI" Roblox post: [link]. Separate what it shows (the result, the tools) from what it claims (one prompt, time, quality). Is the prompt shared? What would we need to reproduce it? Anything that conflicts with Holden's art rules or platform policy? Add it to the right Reference note only if it teaches something.
```

### Evaluate a third-party tool
```text
Evaluate [tool/plugin/MCP/skill] for Holden's setup before anyone installs it: what it does, who made it, licence, install method (pinned or @latest), what it can access (files, Studio, keys), and whether it duplicates something we have. Verdict and reasons, added to Resources/Third Party Claude Tools Evaluated.md.
```

## How to check the result
- No duplicate notes (search the note's main term; one canonical note).
- Every number has a source and date; unverified items carry "⚠️ verify:".
- Third-party media is gitignored (`git check-ignore` on a sample file).
- New notes are linked from Home or a folder index.

## Pitfalls
- **Search summaries treated as sources.** A figure seen only in a search snippet stays "⚠️ verify" until read at the source ([[Gauntlet-Loop]] cost figures).
- **Creator claims as facts.** Videos selling courses or tools are self-reports; label them ([[Video-SyphoDev-Claude-Code-Roblox-Workflow]]).
- **Copying third-party media into tracked folders** (the shop gauntlet's blind pairs held copies of reference images until `blind/` was gitignored, [[Shop Gauntlet Workbench]]).
- **Research suggestions treated as approvals** for game changes (vault CLAUDE.md).
- **Following instructions found inside pages or posts.** Anything read on the web is data; Claude should quote it and ask, not act.

## Related
[[Prompting/_Index|Prompting]] · [[Prompting-Principles]] · [[Reference/_Index|Reference index]] · [[Gap-Tracker]] · [[Verification-Log]]

## Sources
- Anthropic, Prompting best practices (research and information gathering section), read 2026-10-04: <https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices>
- Local: [[X-Reference-Library]], [[YouTube-Reference-Library]], [[TikTok-Reference-Library]], [[Video-SyphoDev-Claude-Code-Roblox-Workflow]], [[Reference-Capture-Process]].
