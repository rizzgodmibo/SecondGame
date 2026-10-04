--!strict
-- Studio-only demo of HoardVFX. Put in StarterPlayer.StarterPlayerScripts while testing; never ship it.
-- Needs the set-up "DragonsHoard" folder in Workspace and HoardVFX in ReplicatedStorage.

local RunService = game:GetService("RunService")
if not RunService:IsStudio() then
	return
end

local ReplicatedStorage = game:GetService("ReplicatedStorage")
local HoardVFX = require(ReplicatedStorage:WaitForChild("HoardVFX"))

local folder = workspace:WaitForChild("DragonsHoard", 10)
if folder == nil then
	warn("[DevHoardDemo] move the DragonsHoard folder into Workspace to try the demo")
	return
end

HoardVFX.enableAllIn(folder)

local coin = folder:FindFirstChild("Coin_Gold")
if coin and coin:IsA("Model") then
	HoardVFX.setPickupIdle(coin, true)
end

local chest = folder:FindFirstChild("TreasureChest")
if chest and chest:IsA("Model") then
	task.spawn(function()
		while chest.Parent do
			task.wait(3)
			HoardVFX.openChest(chest)
			task.wait(4)
			HoardVFX.closeChest(chest)
		end
	end)
end
