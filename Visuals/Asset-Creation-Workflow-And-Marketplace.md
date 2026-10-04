---
tags: [visuals/assets, systems/security]
status: draft
updated: 2026-10-04
confidence: high
---
# Asset Creation Workflow and Creator Store

How assets get into the game safely: sourcing (make / Creator Store / commission), upload & ownership, packages, moderation, and keeping free models from backdooring your game.

## TL;DR
- **Upload everything under the group that owns the game** (Importer/Asset Manager "Creator" = group). Personal-account assets used in a group game cause permission failures for restricted asset types (images, decals, meshes, animations, audio).
- **Treat every Creator Store model as hostile until audited**: insert into an empty baseplate, **Disable Scripts** on insert (right-click → Disable Scripts), search for `require(`, `getfenv`, `setfenv`, `loadstring`, `InsertService`, `LoadAsset`, `LinkedSource`, `HttpService`, `MarketplaceService`, obfuscated strings, and delete every script you don't need. Prefer **mesh/art-only** assets.
- Keep `ServerScriptService.LoadStringEnabled = false`, Game Settings → Security → **Allow HTTP Requests** off unless needed, and **Allow Third-Party Teleports/Sales** off unless needed.
- Use **packages** (with `PackageLink.AutoUpdate`) for anything reused across places (UI kits, NPCs, building modules); never delete/move the `PackageLink`.
- **Moderation**: imported assets are invisible in live games until approved — upload well before release; keep originals; text/images that look like contact info, logos, real brands or off-platform links get rejected.
- Install plugins only from verified creators with many installs; review plugin **script-injection** permission prompts — malicious plugins are the main backdoor vector.

## Sourcing decision table
| Need | Source | Notes |
|---|---|---|
| Unique hero assets (mascot, main pets, key props) | Make in-house or commission | Owns the art identity; needed for thumbnails |
| Generic props (crates, fences, rocks) | Creator Store (Roblox-made or verified creators), restyled | Recolour/re-material to your palette ([[Art-Direction]]) |
| Materials | Roblox materials + MaterialVariants (make or Creator Store) | Check map sizes |
| Audio | Creator Store licensed library | See [[Sound-Design]] |
| Systems/scripts | Write your own or audited open-source (GitHub, Wally) | Avoid Creator Store scripts in production |
| Commissions | Contracts specifying full rights transfer; pay via escrow/milestones; artist uploads to **your** group or sends source files | ⚠️ verify: Talent Hub / commission marketplace terms on Roblox if using it |

## Creator Store (facts, 2026-10-04)
- Marketplace of models, meshes, images, audio, plugins, fonts, video; access via Creator Hub (create.roblox.com/store) and Studio Toolbox. Details page shows triangle, vertex and **script count** — check before inserting.
- Sellers can price models/plugins in **USD and keep 100% of net proceeds** (no DevEx). Requires ID/age-check verified account (not phone), account ≥ 2 days old, not recently banned, plus a seller account.
- Distribution limits per 30 days: verified — 200 meshes, 200 images, 200 models, 100 audio, 10 plugins; unverified — 10, 10, 10, 10, 2.
- Store policy **restricts** in distributed assets: obscuring engine features (`getfenv`/`setfenv`, Lua VMs), requiring remote assets (`require(assetId)`, `loadstring`, `InsertService:LoadAsset`, `AssetService:LoadAssetAsync`, `ModuleScript.LinkedSource`), obfuscated code, extremely large scripts. Any asset containing these is a red flag — report via **Report Item**.
- Composite assets may include **Open Use** dependencies made by others; not **Restricted** dependencies you didn't upload.

## Licensing & IP
- Creator Store assets are licensed for use in Roblox experiences; you don't get ownership or rights to use them off-platform (e.g. in ads outside Roblox or merch). ⚠️ verify: current Creator Store / Terms of Use wording for off-platform use before using store assets in YouTube/TikTok ads or merchandise.
- Don't use real brands, logos, celebrity likeness, or copyrighted characters (moderation + DMCA). Follow Roblox IP guidelines.
- Track provenance: keep a sheet (asset ID, source, creator, licence, date) in `Projects/<game>/` — needed for takedown disputes and audits.

## Upload paths
| Tool | Best for | Notes |
|---|---|---|
| **3D Importer** (File → Import) | Meshes with rigs/skinning/animation/cages, PBR textures | Settings & presets in [[Blender-To-Roblox-Pipeline]] |
| **Asset Manager** (Window → Asset Manager) | Bulk images, audio, decals, simple meshes, video; folders; insert | No rigged/skinned/animated meshes; imported assets go to moderation then to the game owner's inventory |
| **Creator Dashboard** (Development Items) | Single uploads, permissions, configuring/distributing | Permissions tab grants access to collaborators/experiences |
| **Open Cloud Assets API** | CI pipelines, batch uploads from scripts (`POST https://apis.roblox.com/assets/v1/assets` with `x-api-key`) | Group or user creator; good for Rojo/asset-sync workflows |

Upload limits to know: audio 100 / 30 days unverified, 2,000 ID-verified (see [[Sound-Design]]); video upload requires 13+ ID-verified.

## Asset privacy & permissions
- Two access types: **Open Use** (anyone may use) and **Restricted** (owner must grant). The **Asset Privacy** setting controls the default only for newly created **Images, Decals, Meshes**; audio, video, models, MeshParts, animations and packages have their own defaults.
- Your own assets always work in your own games. For other creators/experiences: Creator Dashboard → Development Items → (type) → asset → **Permissions** → add collaborators (friends/groups) or experiences.
- Importer's **Add to Workspace** from a published place also grants that game permission to use the restricted asset.

## Packages
- Select instances → right-click → **Convert to Package** (choose group ownership). A `PackageLink` child marks it; enable `PackageLink.AutoUpdate` to keep all copies synced; publish changes → mass-update copies; version history and diff/restore available.
- Permissions: collaborators get **Edit** or **Use**.
- Use for: shared UI kits, NPC rigs, building kits across places of one universe, lobby ↔ match places.
- Don't package things that need per-copy edits (each edit diverges the copy until updated).

## Moderation of assets
- Human + automated, proactive and reactive. Unapproved assets don't render in live games (still visible to you in Studio).
- Common rejections: text in images that reads as off-platform contact/links, logos/brands, sexual/violent/gory imagery beyond the experience's maturity label, real-money/gambling imagery, copyrighted audio.
- Keep originals locally/in Git LFS; re-uploading creates new IDs — update references via constants module.
- Moderated assets can trigger account warnings; repeated violations affect the account and potentially the game.

## Free-model / plugin backdoor defence

Audit command-bar script (Studio Command Bar, run on suspicious model selection):

```lua
--!strict
-- Studio Command Bar / plugin helper: scans selected instances for red-flag patterns.
local Selection = game:GetService("Selection")

local PATTERNS = {
	"require%s*%(", "getfenv", "setfenv", "loadstring", "LoadAsset", "LinkedSource",
	"HttpService", "MarketplaceService", "TeleportService", "\\%d%d%d", -- escaped bytes (obfuscation)
	"string%.reverse", "eriuqer", "_G%.", "shared%.",
}

for _, root in Selection:Get() do
	local candidates = root:GetDescendants()
	table.insert(candidates, root)
	for _, inst in candidates do
		if inst:IsA("LuaSourceContainer") then
			local ok, source = pcall(function()
				return (inst :: any).Source :: string
			end)
			if ok then
				for _, pattern in PATTERNS do
					if string.find(source, pattern) then
						warn(`[AUDIT] {inst:GetFullName()} matches '{pattern}'`)
					end
				end
				if #source > 50000 then
					warn(`[AUDIT] {inst:GetFullName()} is very large ({#source} chars)`)
				end
			end
		end
	end
end
```

(`Source` is readable from the Command Bar/plugins only.) Also check: scripts hidden in odd places (inside `Decal`s or deeply nested in meshes), names mimicking services ("Chat", "Animate"), `Weld` scripts in decorative models, `RemoteEvent`s created by models, and **Toolbox insert plugins** you didn't install.

Ongoing hygiene:
- After using any new plugin, Ctrl+Shift+F the whole game for `require(` and `getfenv`.
- Use version control (Rojo + Git) so unexpected script additions show in diffs — see [[Module-Architecture]].
- Server-authoritative design means even a compromised client script can't grant currency; a server backdoor can do anything — see [[Anti-Exploit-And-Server-Authority]].

## Checklist
- [ ] Game owned by a group; all assets uploaded to that group
- [ ] Provenance sheet for third-party assets
- [ ] Every inserted model audited; scripts disabled/removed
- [ ] `LoadStringEnabled` false; HTTP off unless needed
- [ ] Plugins limited to a vetted list
- [ ] Assets uploaded ≥ 48 h before launch to clear moderation ⚠️ verify typical moderation turnaround
- [ ] Shared systems converted to packages with AutoUpdate

## Pitfalls
- "Free admin"/"anti-exploit" models — classic backdoor carriers.
- Inserting a model with a `require(1234567)` hidden 8 levels deep — gives a remote attacker server-side code execution.
- Re-uploading the same image many times → inventory clutter; use Asset Manager folders.
- Assets in moderation at launch → invisible shop items/icons on day one.
- Using personal-account animations/audio in a group game → silent failures in live servers.

## Related
- [[Visuals/_Index]] · [[Blender-To-Roblox-Pipeline]] · [[Sound-Design]] · [[Art-Direction]] · [[Anti-Exploit-And-Server-Authority]] · [[Module-Architecture]]

## Sources
- Creator Store (limits table, restricted practices, seller requirements, 100% USD proceeds, Disable Scripts) — https://create.roblox.com/docs/production/creator-store
- Asset privacy (Open Use vs Restricted, scope, permissions) — https://create.roblox.com/docs/projects/assets/privacy
- Packages — https://create.roblox.com/docs/projects/assets/packages
- Asset Manager — https://create.roblox.com/docs/projects/assets/manager ; Assets overview & moderation — https://create.roblox.com/docs/projects/assets
- Importer — https://create.roblox.com/docs/studio/importer ; Open Cloud assets usage — https://create.roblox.com/docs/cloud/guides/usage-assets
- Audio upload limits — https://create.roblox.com/docs/audio/assets
- DevForum: Removing Backdoors 101 — https://devforum.roblox.com/t/removing-backdoors-101/545574 ; Is getfenv dangerous — https://devforum.roblox.com/t/is-getfenv-dangerous/2420643 ; free model/plugin virus removal — https://devforum.roblox.com/t/how-to-remove-free-model-plugin-viruses-from-your-game-on-roblox/1258483
- Docs checked via Roblox/creator-docs GitHub source (2026-10-02 commit) on 2026-10-04.
