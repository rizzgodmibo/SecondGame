--[[
	HoardSetup — run ONCE in the Studio COMMAND BAR (View > Command Bar), in Edit mode, after importing
	the 11 OBJs into a Folder named "DragonsHoard" (in Workspace, ServerStorage or ReplicatedStorage).
	The command bar is needed because CollisionFidelity can't be set from game scripts.

	What it does, per item:
	  • wraps the MeshPart in a Model named after the item (PrimaryPart = the MeshPart)
	  • Anchored, CanTouch off, SmoothPlastic, CollisionFidelity (Box; Hull for the chest)
	  • PivotOffset = base centre (the lid: its hinge; the sword: its tip)
	  • "HoardVFXPreset" attribute on the MeshPart (read by HoardVFX.enableDefault / enableAllIn)
	  • attachments: CoinPile_Large.SwordSocket, Chest_Base.LidHinge
	  • points every item at one shared atlas TextureID
	Then it builds two ready-made examples next to the items: "TreasureChest" and "PileWithSword".
	Safe to re-run. Numbers come from build_report.json (Blender build).
]]

local FOLDER_NAME = "DragonsHoard"
local Box, Hull = Enum.CollisionFidelity.Box, Enum.CollisionFidelity.Hull

-- size = expected MeshPart.Size; pivot = pivot offset from the MeshPart centre (studs, part space)
local ITEMS = {
	Egg_Ember = {
		size = Vector3.new(1.135, 1.6, 1.129),
		pivot = Vector3.new(0, -0.8, 0),
		preset = "Ember",
		fidelity = Box,
	},
	Egg_Frost = {
		size = Vector3.new(1.135, 1.6, 1.131),
		pivot = Vector3.new(0, -0.8, 0),
		preset = "Frost",
		fidelity = Box,
	},
	Egg_Venom = {
		size = Vector3.new(1.135, 1.6, 1.131),
		pivot = Vector3.new(0, -0.8, 0.0009),
		preset = "Venom",
		fidelity = Box,
	},
	Coin_Gold = {
		size = Vector3.new(0.5, 0.086, 0.475),
		pivot = Vector3.new(0, -0.043, 0),
		preset = "Sparkle",
		fidelity = Box,
	},
	CoinPile_Small = {
		size = Vector3.new(1.524, 0.575, 1.579),
		pivot = Vector3.new(0.1617, -0.2355, 0.1512),
		preset = "Sparkle",
		fidelity = Box,
	},
	CoinPile_Large = {
		size = Vector3.new(3.415, 1.295, 3.394),
		pivot = Vector3.new(-0.0461, -0.5121, 0.0734),
		preset = "Sparkle",
		fidelity = Box,
		attachments = { SwordSocket = Vector3.new(-0.0461, 0.6379, 0.0734) },
	},
	Goblet_Jewelled = {
		size = Vector3.new(0.638, 1.0, 0.66),
		pivot = Vector3.new(-0.0053, -0.5, 0),
		preset = "Sparkle",
		fidelity = Box,
	},
	Crown_Gold = {
		size = Vector3.new(1.2, 0.654, 1.2),
		pivot = Vector3.new(0, -0.3271, 0),
		preset = "Sparkle",
		fidelity = Box,
	},
	Chest_Base = {
		size = Vector3.new(3.06, 1.35, 2.125),
		pivot = Vector3.new(0, -0.675, -0.0075),
		fidelity = Hull,
		attachments = { LidHinge = Vector3.new(0, 0.625, 0.9925) },
	},
	Chest_Lid = { size = Vector3.new(3.06, 0.972, 2.11), pivot = Vector3.new(0, -0.3258, 1.02), fidelity = Hull },
	Sword_Ornate = {
		size = Vector3.new(1.56, 4.44, 0.292),
		pivot = Vector3.new(0, -2.22, 0),
		preset = "Blade",
		fidelity = Box,
	},
}

local folder = workspace:FindFirstChild(FOLDER_NAME)
	or game:GetService("ServerStorage"):FindFirstChild(FOLDER_NAME)
	or game:GetService("ReplicatedStorage"):FindFirstChild(FOLDER_NAME)
assert(folder, "[HoardSetup] put the imported items in a Folder named " .. FOLDER_NAME)

local done = {}
local textureId = nil

for name, info in ITEMS do
	local found = nil
	for _, child in folder:GetChildren() do
		if child.Name == name then
			found = child
			break
		end
	end
	found = found or folder:FindFirstChild(name, true)
	if not found then
		warn("[HoardSetup] missing " .. name .. " — import " .. name .. ".obj into the folder")
		continue
	end
	local part = if found:IsA("BasePart") then found else found:FindFirstChildWhichIsA("BasePart", true)
	if not part then
		warn("[HoardSetup] no MeshPart inside " .. found:GetFullName())
		continue
	end

	local model = found
	if not found:IsA("Model") then
		model = Instance.new("Model")
		model.Parent = found.Parent
		part.Parent = model
	end
	model.Name = name
	part.Name = name
	model.PrimaryPart = part

	local ratio = part.Size.Y / info.size.Y
	if math.abs(ratio - 1) > 0.02 then
		warn(
			("[HoardSetup] %s is %.3fx the expected size (check the importer's file units are studs); offsets scaled to match"):format(
				name,
				ratio
			)
		)
	end

	part.Anchored = true
	part.CanTouch = false
	part.CanCollide = true
	part.CanQuery = true
	part.CastShadow = true
	part.Material = Enum.Material.SmoothPlastic
	local ok, err = pcall(function()
		part.CollisionFidelity = info.fidelity
	end)
	if not ok then
		warn(
			"[HoardSetup] could not set CollisionFidelity on "
				.. name
				.. " (run this in the command bar): "
				.. tostring(err)
		)
	end
	part.PivotOffset = CFrame.new(info.pivot * ratio)
	part:SetAttribute("HoardVFXPreset", info.preset)

	for attName, pos in info.attachments or {} do
		local old = part:FindFirstChild(attName)
		if old then
			old:Destroy()
		end
		local att = Instance.new("Attachment")
		att.Name = attName
		att.Position = pos * ratio
		att.Parent = part
	end

	if part:IsA("MeshPart") and part.TextureID ~= "" then
		textureId = textureId or part.TextureID
	end
	done[name] = model
end

-- one shared atlas instead of 11 identical uploads
if textureId then
	for _, model in done do
		local p = model.PrimaryPart
		if p:IsA("MeshPart") and p.TextureID ~= "" and p.TextureID ~= textureId then
			p.TextureID = textureId
		end
	end
else
	warn(
		"[HoardSetup] no TextureID found — if the importer made SurfaceAppearances, keep those (they hold the atlas)"
	)
end

-- example: assembled chest (base + lid on its hinge)
local base, lid = done.Chest_Base, done.Chest_Lid
local old = folder:FindFirstChild("TreasureChest")
if old then
	old:Destroy()
end
if base and lid then
	local chest = Instance.new("Model")
	chest.Name = "TreasureChest"
	local b = base.PrimaryPart:Clone()
	b.Parent = chest
	local l = lid.PrimaryPart:Clone()
	l.Parent = chest
	chest.PrimaryPart = b
	l:PivotTo(b.LidHinge.WorldCFrame)
	chest:SetAttribute("OpenAngle", 105)
	chest.Parent = folder
	chest:PivotTo(base:GetPivot() * CFrame.new(0, 0, 6))
end

-- example: sword standing in the large pile (same numbers as HoardVFX.placeSword defaults)
local pile, sword = done.CoinPile_Large, done.Sword_Ornate
old = folder:FindFirstChild("PileWithSword")
if old then
	old:Destroy()
end
if pile and sword then
	local display = Instance.new("Model")
	display.Name = "PileWithSword"
	local p = pile.PrimaryPart:Clone()
	p.Parent = display
	local s = sword.PrimaryPart:Clone()
	s.Parent = display
	display.PrimaryPart = p
	s:PivotTo(p.SwordSocket.WorldCFrame * CFrame.Angles(math.rad(8), 0, 0) * CFrame.new(0, -0.9, 0))
	display.Parent = folder
	display:PivotTo(pile:GetPivot() * CFrame.new(6, 0, 0))
end

local count = 0
for _ in done do
	count += 1
end
print(("[HoardSetup] set up %d / 11 items in %s"):format(count, folder:GetFullName()))
