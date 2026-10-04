---
title: Roblox Texture Upload Failures
date: 2026-10-03
tags: [roblox, assets, bug, workaround]
---
# Roblox Texture Upload Failures (grey meshes)

**Symptom:** a GLB uploaded through Open Cloud (see [[Blender to Roblox Asset Pipeline]]) shows up **grey in game**. It happened to the Paper Plane Toss group chest.

## What was checked
- **The MeshPart has a `TextureID`,** so the upload did attach a texture.
- **`ContentProvider:PreloadAsync`** reported `Failure` for the texture, both from the GLB upload and from a re-upload through Studio's `upload_image`.
- **The Open Cloud asset API** said the image was `"moderationState":"Approved"`.
- **`AssetService:CreateEditableImageAsync`** loaded the image fine.
- **`PreloadAsync` also said Failure for UI icons that displayed perfectly in game.** So `PreloadAsync` in Studio is not a reliable check for brand-new assets. Only a visual check is.

## Workaround that worked
Rebuild the mesh using an **atlas palette that's already approved and loading**: the same colour names in the same order. Then point its `TextureID` at that existing texture.

The chest now uses the rebirth atlas (`rbxassetid://91036935402412`). It looks identical apart from one swapped colour (a blue gem became purple).

Related: [[Roblox Studio MCP Quirks]], [[Paper Plane Toss]]
