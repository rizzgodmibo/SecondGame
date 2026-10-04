# Dragon's Hoard — import guide

11 separate models, a 512 px shared colour atlas, 7 particle textures and 3 scripts.
Built by `build_hoard.py` (Blender 5.2, headless). Front of every model = the part's front (−Z / LookVector).

## 1. What to import, and where it goes

| File(s) | How | Where it ends up |
|---|---|---|
| `models/<Item>/<Item>.obj` (+ `.mtl`, `HoardAtlas.png` beside it) ×11 | Studio **3D Importer** (File → Import 3D), one OBJ at a time | Workspace, inside a Folder named **`DragonsHoard`**; after setup, move the folder to **ServerStorage** (templates your server clones). Use **ReplicatedStorage** instead if clients need the templates (e.g. ViewportFrames). |
| `vfx/*.png` ×7 (Sparkle, Ember, FrostFlake, Bubble, Glow, CoinGlint, Shine) | **Asset Manager → Bulk Import** (uploads as Images) | Copy each **Image** id into `HoardVFX.Textures` at the top of the module. Not uploaded yet = built-in fallback textures. |
| `scripts/HoardVFX.luau` | New ModuleScript, paste contents | **ReplicatedStorage.HoardVFX** |
| `scripts/HoardSetup.luau` | Paste into the **Command Bar** once (Edit mode) | Not kept in the game |
| `scripts/DevHoardDemo.client.luau` | New LocalScript, paste contents | **StarterPlayer.StarterPlayerScripts**, Studio testing only; delete before publishing |

The 11 OBJs, in import order: `Egg_Ember`, `Egg_Frost`, `Egg_Venom`, `Coin_Gold`, `CoinPile_Small`,
`CoinPile_Large`, `Goblet_Jewelled`, `Crown_Gold`, `Chest_Base`, `Chest_Lid`, `Sword_Ornate`.

### 3D Importer settings
- **Units/file dimensions: studs.** The files are authored 1 unit = 1 stud. HoardSetup warns if a part arrives at a different size.
- **No rig / no avatar.** Import as a plain model (no "Rig General" / R15 options).
- **Anchored:** on (HoardSetup also sets it).
- **Insert using scene position:** off. Pivots are fixed by HoardSetup either way.
- **Upload to Roblox / textures:** on, so the MTL's `HoardAtlas.png` becomes the MeshPart's texture.
- ⚠️ verify: the importer's option names change between Studio releases; the intent above is what matters.
  Check after importing: each MeshPart shows colours (not grey). If one is grey, set its `TextureID` to the same atlas id as the others.

## 2. Run the setup (once)
1. Put all 11 imported items in a Folder named `DragonsHoard` (Workspace is easiest).
2. Paste `HoardSetup.luau` into the Command Bar and press Enter. Output: `[HoardSetup] set up 11 / 11 items`.
3. It sets per item: Model wrapper with PrimaryPart, Anchored, CanTouch off, SmoothPlastic, **CollisionFidelity**
   (Box for everything except the chest base and lid, which get Hull), **PivotOffset** (base centre; the lid's is its hinge; the sword's is its tip),
   the `HoardVFXPreset` attribute, the `SwordSocket` / `LidHinge` attachments, and one shared atlas TextureID.
4. It also builds two examples in the folder: **TreasureChest** and **PileWithSword**.
5. Move the folder to ServerStorage (or keep it in Workspace while testing the demo).

## 3. Sizes (studs) and triangle counts
| Item | Size X × Y × Z | Tris | VFX preset |
|---|---|---|---|
| Egg_Ember / Egg_Frost / Egg_Venom | 1.14 × 1.60 × 1.13 | 1,476 each | Ember / Frost / Venom |
| Coin_Gold | 0.50 × 0.09 × 0.48 | 92 | Sparkle |
| CoinPile_Small | 1.52 × 0.58 × 1.58 | 530 | Sparkle |
| CoinPile_Large (with gems) | 3.42 × 1.30 × 3.39 | 1,900 | Sparkle |
| Goblet_Jewelled | 0.64 × 1.00 × 0.66 | 390 | Sparkle |
| Crown_Gold | 1.20 × 0.65 × 1.20 | 842 | Sparkle |
| Chest_Base | 3.06 × 1.35 × 2.13 | 746 | (chest functions) |
| Chest_Lid | 3.06 × 0.97 × 2.11 | 206 | (chest functions) |
| Sword_Ornate | 1.56 × 4.44 × 0.29 | 342 | Blade |

Avatar ≈ 5 studs tall. Scale a whole item with `model:ScaleTo(n)`; the VFX scale with the part size.

## 4. Assembling the chest (base + lid)
Easiest: use the **TreasureChest** model HoardSetup builds. By hand:
1. Put `Chest_Base` and `Chest_Lid` MeshParts in one Model (e.g. `TreasureChest`), PrimaryPart = `Chest_Base`.
2. Snap the lid to the hinge: `lid:PivotTo(base.LidHinge.WorldCFrame)` (the lid's pivot *is* its hinge line).
3. Optional attribute `OpenAngle` (number, default 105) on the chest model.
4. Open/close from a LocalScript: `HoardVFX.openChest(chest)` / `HoardVFX.closeChest(chest)`.
   The lid swings about its hinge (Back easing), then a gold light flash, a coin-glint fountain, sparks and a soft shimmer play while it stays open.
   The swing is client-side, so the server's lid stays closed (fine for visuals; collisions use the closed lid).

## 5. Standing the sword in the large coin pile
Easiest: use the **PileWithSword** model. In code (server or client):
```lua
HoardVFX.placeSword(swordModel, largePileModel)                       -- defaults: sink 0.9, lean 8°
HoardVFX.placeSword(swordModel, largePileModel, { depth = 1.1, tilt = 12, yaw = 30 })
```
`CoinPile_Large` carries a `SwordSocket` attachment on the top of the mound; the sword's pivot is its tip,
so it's pushed `depth` studs into the pile along its own leaning axis. Only the server's call replicates.

## 6. Using the VFX from your code
```lua
--!strict
-- StarterPlayerScripts (LocalScript)
local HoardVFX = require(game:GetService("ReplicatedStorage"):WaitForChild("HoardVFX"))

HoardVFX.enable(egg, "Ember")            -- pulse glow + embers
HoardVFX.enable(goblet, "Sparkle")       -- occasional gold twinkle
HoardVFX.enableDefault(anyHoardItem)     -- uses the preset HoardSetup stored on it
HoardVFX.enableAllIn(workspace.Treasure) -- every hoard item in a container
HoardVFX.setPickupIdle(coin, true)       -- bob + spin + shine (anchored items); false restores the pivot
HoardVFX.disable(egg)                    -- removes everything it added
```
Your server decides *when* (pickup, chest opened, …) and fires a RemoteEvent; each client calls HoardVFX.

## Pitfalls
- Eggs use one `Highlight` each for the pulse. The client limit is 255, but each Highlight costs an extra render pass, so set `HoardVFX.UseHighlightGlow = false` when more than about 10 eggs are on screen (see [[VFX-Particles-Beams-Trails]]).
- Pickup idle moves the item locally every frame; turn it off before your code moves the item.
- Use either the Model or its MeshPart as the target for a given item, not both (they get separate effects).
- Unused atlas cells are grey on purpose; a grey patch on a model means a bad UV, so report it.
