---
tags: [meta/ai-workflow, meta/agents]
status: draft
updated: 2026-10-04
confidence: medium
---
# The Gauntlet Loop (Matt Shumer)

An agent prompting method named by Matt Shumer on 2026-07-27, after his "Claude of Duty" run: one short prompt in
Claude Code (Opus 5) ran for many hours, fanned out subagents and produced a ~55,000-line Three.js Call of Duty-style FPS
with every texture, mesh, animation and sound generated in code. The idea: the agent splits the goal into pieces, each
piece gets a **builder** and a separate **blind, harsh critic**, and work only passes when it **beats a real-world
reference** in a side-by-side comparison. It loops until it wins or you stop it.

## TL;DR
- **Four rules:** (1) give the goal, not your implementation; (2) give a *concrete, inspectable* bar (real screenshots,
  a named site, a test suite, a benchmark); (3) let the lead agent decide the split into the smallest independently judgeable
  pieces; (4) never let the builder grade itself: a fresh-context critic compares the real output with the reference,
  ideally blind and unlabeled, picks a winner, and names the biggest gap.
- **No fixed round count.** The exit is "ours wins" or "you stop it". Claude of Duty never actually beat Call of Duty; the
  bar's job is direction and refusing to stop at "pretty good for AI".
- **Pick, don't score.** A 1–10 score drifts upward each round; a forced A/B pick doesn't (robonuggets skill README).
- **The reference corpus is everything.** A tester's four runs found that output quality tracked reference quality directly;
  without a named, fetchable bar the critic invents one and approves everything ([wotai](https://wotai.co/blog/gauntlet-loop-playbook)).
- **It sharpens; it doesn't discover.** On a new design with no anchor it polishes generic "premium" output at full token cost.
  Anchor the direction first (design doc, references), then loop.
- **Expensive.** Shumer burned through Anthropic subscriptions running three loops at once (2026-09-01). Community reports of
  $1,200–1,700 runs and a 1.7B-token run exist (⚠️ verify: seen only in a search summary, not at source).

## The original prompt (verbatim, from the Claude-of-Duty repo)
```
I want you to build a first-person shooter at the level of the most recent Call of Duty games. It should be utterly
perfect, visually beautiful, with every single thing done at AAA quality—from textures to physics to anything you could
think of.

Fan out sub-agents and have sub-agents tackle each one individually so that the game is utterly perfect. You should /loop
on each item and have a separate sub-agent check it visually to ensure it looks triple A. That separate sub-agent should be
a really harsh critic, and if it doesn't look triple A, it should keep going.

Don't stop until each sub-agent is utterly wowed with the quality when compared with the actual Call of Duty game. It
should literally compare them side by side blind and say which one looks better. Do this in ThreeJS. /loop until it's
utterly perfect. Fan out sub-agents and ultracode.
```
Repo: <https://github.com/mshumer/Claude-of-Duty> (created 2026-07-25, about 3.4k stars on 2026-10-04).

## How Shumer says to run it (from his guide, 2026-07-27)
- **Use a real agent harness** (Claude Code or Codex) that can open files, run code, render and screenshot, and spawn
  subagents with clean context. Plain chat won't work. His default is Claude Code with Opus; Codex is good for backend
  and critiquing visuals, weaker at creating them. He recommends `/effort` → ultracode for big runs.
- **When no real equivalent exists**, make finding a bar part of the task ("find a comparison that plays the role Call of
  Duty screenshots played"). Later (2026-08-28) he suggested generating reference images with an image model when there
  is no real-world complement.
- **Watch without interrupting:** have the lead agent maintain a live HTML page or `workbench.md` with screenshots and
  progress, so you check from your phone instead of pinging the agent.
- **Optional smoothing pass:** after each wave, a fresh agent checks the whole artifact for consistency between
  separately improved parts. It fixes conflicts but doesn't redesign.
- **Meta-prompt:** his guide gives a prompt that turns any goal into a Gauntlet Loop prompt (choose the bar, write a
  short Matt-style prompt, don't prescribe architecture or round counts). There is also a web generator and a packaged
  Claude Code skill (robonuggets/gauntlet-loop, CC BY 4.0) that offers 2–3 named, fetchable bars and outputs a ~150-word prompt.
- **Model notes:** he had little success with GPT-6 Astra (it "got really stuck on over-optimizing and never moving on",
  2026-09-04); he ran the first Opus 5.5 loop on 2026-09-22.

## Where it's been used
Games (Claude of Duty; community Kart Royale, Der Koloss, Pastel Nuketown, an NYC open world), website redesigns
(somethingbig.ai), Claude Code skills folders, SEO/structured data. The tester's four runs (timing fixes against Google
Snake's 140–145 ms cadence, Doodle Jump physics against period footage, a new 3D board game anchored by an architecture
contract, SEO against official crawler docs) each converged within a day. Its origin is Anthropic's evaluator-optimizer
pattern ([Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)).

## How it could apply to Holden's work (recommendations, not approvals)
- **The X/YouTube/TikTok libraries are ready-made bars.** E.g. a shop frame judged blind against the DevionUI or Steal An Egg
  captures in [[X-Shop-And-Seasonal-UI]]; a HUD against the '+1' HUD references in [[X-HUD-And-Menus-UI]].
- **The critic needs real pixels.** In Roblox that means Studio screenshots (Roblox Studio MCP `screen_capture`) at phone and PC
  sizes, not the builder's description. Pair with the existing checkers (UI layout checker, code gate) as hard gates and
  use the blind critic only for taste.
- **Keep Holden's rules inside the loop:** plan approval before game code, no AI meshes or part-built props (the loop's
  "generate everything in code" style conflicts with the art rules in [[Art-Direction]]), Holden makes commits.
- **Start small and capped.** One piece (a single shop frame, one button set) with a token or time budget, not a whole game.
- Compare with the one-checker-per-discipline workflow in [[Video-SyphoDev-Claude-Code-Roblox-Workflow]], which is the
  same evaluator idea with automated checks instead of a blind taste critic.

## Pitfalls
- Vague bar ("AAA", "award-winning") → the critic hallucinates the comparison. The bar must be **named, fetchable and
  comparable** (robonuggets).
- The critic seeing the builder's reasoning or a summary instead of the artifact.
- Soft critics (scores), fixed round counts, and starting without a design anchor.
- Compute cost; budget before starting.

## Related
[[AI-Assisted-Workflow]] · [[Prompt-Library]] · [[Video-SyphoDev-Claude-Code-Roblox-Workflow]] · [[Third Party Claude Tools Evaluated]] ·
[[X-Reference-Library]]

## Sources
- Matt Shumer, X post naming the loop (2026-07-27, 801 likes on 2026-10-04): <https://x.com/mattshumer_/status/2081830214384886228>; "Say hello to the Gauntlet Loop": <https://x.com/mattshumer_/status/2081830741436928208>
- Shumer's guide, "How to Run a Gauntlet Loop" (2026-07-27): <https://somethingbig.ai/gauntlet-loop> · generator: <https://somethingbig.ai/gauntlet-loop/generator>
- Original prompt: <https://github.com/mshumer/Claude-of-Duty/blob/main/prompt.md>
- Shumer's follow-up posts read on X 2026-10-04 (bar via generated images 2026-08-28; Astra results 2026-09-04; compute 2026-09-01; Opus 5.5 run 2026-09-22): <https://x.com/search?q=from%3Amattshumer_%20gauntlet>
- robonuggets skill: <https://github.com/robonuggets/gauntlet-loop>
- Four test runs: <https://wotai.co/blog/gauntlet-loop-playbook>
- Summary: <https://rogerwong.me/2026/08/the-gauntlet-loop-method>
- Cost and limitations (search summary only; article bodies not readable): <https://helloskip.com/b/crazystack-typescript-1/blog/gauntlet-loop-in-claude-code-strengths-costs-and-real-uses>, <https://daily.dev/posts/the-new-gauntlet-loop-has-a-flaw-this-claude-skill-just-fixed-it-2u5yvngy5>
- Other explainers: <https://explainx.ai/blog/gauntlet-loop-matt-shumer-builder-critic-agent-technique-2026>, <https://www.thepromptindex.com/ai-loop-engineering-gauntlet-loop-guide.html>
