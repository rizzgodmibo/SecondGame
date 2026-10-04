---
tags: [systems/networking]
status: draft
updated: 2026-10-04
confidence: high
---
# Remotes and Networking

## TL;DR
- **RemoteEvent** (reliable, ordered) for anything that must arrive. **UnreliableRemoteEvent** for high-frequency, replaceable data (aim direction, cosmetic positions, VFX) — payload > **1,000 bytes is dropped**. **RemoteFunction** only client→server (`InvokeServer`) for request/response.
- **Never `InvokeClient`**: the client can yield forever or error, hanging or breaking the server thread.
- Every `OnServerEvent`/`OnServerInvoke` handler: (1) rate-limit per player, (2) type-check every arg as `unknown`, (3) validate ranges/ownership/state, (4) act. Reject silently; log suspicious patterns.
- Client→server rate limit is **~500 requests/s per client, shared across all remotes of the same type** (2026-10-04, RemoteEvent docs). Excess reliable events are queued (latency), excess unreliable ones dropped. Your own limiter should be far lower (typically 5–30/s per action).
- Batch: send one remote per frame/tick with an array of changes, not one per change. Budget ~**50 KB/s per player** outbound total ⚠️ verify: current recommended per-client bandwidth ceiling.
- For bandwidth-heavy games use a schema-based serializer (**Blink** or **Zap** IDL compilers, or ByteNet) which pack to `buffer`s.

## Details

### Choosing a remote
| Need | Use |
|---|---|
| Player action intent (buy, equip, attack) | RemoteEvent client→server |
| Server state push (inventory delta, notifications) | RemoteEvent server→client |
| Client asks for data and needs answer (open shop → prices) | RemoteFunction `InvokeServer` (or RemoteEvent request + reply event) |
| 10–60 Hz streams (look direction, vehicle input, projectile cosmetics) | UnreliableRemoteEvent |
| Server→client "ask the client something" | **Don't.** Fire a RemoteEvent and have the client reply with another RemoteEvent; server times out |

Delivery semantics (docs, 2026-10-04): RemoteEvents are reliable and ordered; if nothing is connected, messages queue until a handler connects (bounded queue, overflow discarded with "Remote event invocation" error). UnreliableRemoteEvents: no delivery/order guarantee, no ordering relative to RemoteEvents, dropped if >1,000 bytes, if over throttle, or if nothing is connected.

### Argument rules
- Passing tables: **mixed tables** (array + dict keys) lose data; non-string dictionary keys are converted to strings; metatables are stripped; functions are not sent; `nil` holes truncate arrays.
- Instances arrive as `nil` if the receiver can't see them (server-only container or not streamed in).
- Exploiters can pass **any** type: tables in place of numbers, `NaN`, `math.huge`, huge strings, deeply nested tables, Instances they don't own.

### Validation helpers (shared)
```lua
--!strict
-- ServerScriptService/Server/Net/Guard.luau
local Guard = {}

function Guard.number(v: unknown, min: number, max: number): number?
	if typeof(v) ~= "number" then return nil end
	if v ~= v or v < min or v > max then return nil end -- NaN fails v ~= v; inf fails range
	return v
end

function Guard.integer(v: unknown, min: number, max: number): number?
	local n = Guard.number(v, min, max)
	if n == nil or n % 1 ~= 0 then return nil end
	return n
end

function Guard.string(v: unknown, maxLen: number): string?
	if typeof(v) ~= "string" or #v > maxLen or not utf8.len(v) then return nil end
	return v
end

-- Returns the key if it exists in `allowed` (use for item ids, enums-as-strings).
function Guard.key(v: unknown, allowed: { [string]: any }): string?
	if typeof(v) ~= "string" or #v > 64 or allowed[v] == nil then return nil end
	return v
end

function Guard.vector3(v: unknown, maxMagnitude: number): Vector3?
	if typeof(v) ~= "Vector3" then return nil end
	if v ~= v or v.Magnitude > maxMagnitude then return nil end -- v ~= v catches NaN components
	return v
end

function Guard.instanceOf(v: unknown, className: string, ancestor: Instance?): Instance?
	if typeof(v) ~= "Instance" or not v:IsA(className) then return nil end
	if ancestor and not v:IsDescendantOf(ancestor) then return nil end
	return v
end

return Guard
```

### Token-bucket rate limiter
```lua
--!strict
-- ServerScriptService/Server/Net/RateLimiter.luau
-- capacity = burst size, refillPerSec = sustained rate.
local Players = game:GetService("Players")

export type Limiter = {
	consume: (player: Player, cost: number?) -> boolean,
}

type Bucket = { tokens: number, last: number }

local RateLimiter = {}

function RateLimiter.new(capacity: number, refillPerSec: number): Limiter
	local buckets: { [Player]: Bucket } = {}

	Players.PlayerRemoving:Connect(function(player)
		buckets[player] = nil
	end)

	local function consume(player: Player, cost: number?): boolean
		local c = cost or 1
		local now = os.clock()
		local b = buckets[player]
		if b == nil then
			b = { tokens = capacity, last = now }
			buckets[player] = b
		end
		b.tokens = math.min(capacity, b.tokens + (now - b.last) * refillPerSec)
		b.last = now
		if b.tokens < c then
			return false
		end
		b.tokens -= c
		return true
	end

	return { consume = consume }
end

return RateLimiter
```

### Hardened handler pattern
```lua
--!strict
-- ServerScriptService/Server/Services/ShopService.luau (excerpt)
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Guard = require(script.Parent.Parent.Net.Guard)
local RateLimiter = require(script.Parent.Parent.Net.RateLimiter)

local ITEMS: { [string]: { price: number } } = {
	Sword = { price = 100 },
	Shield = { price = 250 },
}

local remotes = Instance.new("Folder")
remotes.Name = "Remotes"
local buyRemote = Instance.new("RemoteEvent")
buyRemote.Name = "BuyItem"
buyRemote.Parent = remotes
remotes.Parent = ReplicatedStorage

local buyLimiter = RateLimiter.new(5, 2) -- burst 5, then 2/s
local strikes: { [Player]: number } = {}

local function flag(player: Player, reason: string)
	strikes[player] = (strikes[player] or 0) + 1
	warn(`[Net] {player.UserId} {reason} strikes={strikes[player]}`)
	-- Don't auto-kick on a single strike: lag causes false positives.
end

buyRemote.OnServerEvent:Connect(function(player: Player, rawItem: unknown, rawQty: unknown)
	if not buyLimiter.consume(player) then return end
	local itemId = Guard.key(rawItem, ITEMS)
	local qty = Guard.integer(rawQty, 1, 10)
	if not itemId or not qty then
		flag(player, "BuyItem bad args")
		return
	end
	-- state checks: owns data, near shop, enough coins … (server-side only)
	local cost = ITEMS[itemId].price * qty
	-- CurrencyService:TrySpend(player, cost) then grant item
	print(player.Name, "buys", qty, itemId, "for", cost)
end)
```

### RemoteFunction safely
```lua
--!strict
-- Server: always return quickly; never yield on client-provided state.
local getShop = Instance.new("RemoteFunction")
getShop.Name = "GetShop"
getShop.Parent = game:GetService("ReplicatedStorage")
getShop.OnServerInvoke = function(player: Player): { [string]: number }
	return { Sword = 100, Shield = 250 }
end
```
Client side: wrap `InvokeServer` in `pcall` — it errors if the server handler errors.

### Bandwidth and batching rules
- Send **deltas** after an initial snapshot; never resend the full inventory on each change.
- Coalesce: accumulate changes in a table and flush once per `Heartbeat` (or every 0.1–0.2 s for non-urgent UI).
- Quantise: positions to 1/100 stud or int16, angles to 1 byte/2 bytes, booleans packed into bitfields — what Blink/Zap generate for you.
- Strings are costly; send numeric ids, map to names client-side.
- Don't replicate per-frame positions of server-owned NPCs via remotes — physics replication already does it; use remotes only for state changes (animation state, target).
- Check **Network** stats in the Developer Console (Ctrl/Cmd+F9 → Network) and the MicroProfiler to find chatty remotes.

### Networking libraries (2026-10-04)
| Lib | Type | Latest tag | Use |
|---|---|---|---|
| Blink | IDL → generated Luau, buffer-packed, built-in validation of types | v0.18.9 (1.0 pre-releases exist) | Default for bandwidth-sensitive games |
| Zap | IDL → generated Luau, similar to Blink | v0.6.29 | Alternative to Blink |
| ByteNet | Runtime-defined packets, buffer serialisation | v0.4.3 | No codegen step wanted |
| Plain RemoteEvents + Guard | none | – | Small/casual games; fine up to moderate traffic |
Generated serializers validate **types** but not **game rules** — still rate-limit and check state.

## Checklist
- [ ] All remotes created by server code (or generated) in one place (`ReplicatedStorage.Remotes` or lib).
- [ ] Every server handler: limiter → type guard → state check → act.
- [ ] No `InvokeClient` anywhere (`grep -r InvokeClient src/` returns nothing).
- [ ] High-frequency streams moved to UnreliableRemoteEvent and kept < 1,000 bytes.
- [ ] Per-player strike counter + logging feeding analytics, not instant kicks.
- [ ] Network tab checked with 10+ players in a test server.

## Pitfalls
- Validating `typeof(x) == "number"` but not NaN/inf → `NaN` comparisons are always false, bypassing `if coins < price`.
- Trusting a client-supplied `Player` or `UserId` argument — the first param of `OnServerEvent` is the only trustworthy player.
- Long strings (chat-like input) without length caps → memory/DataStore bloat; filter user text with `TextService:FilterStringAsync` before showing to others.
- Remote spam DOS: unrate-limited remotes that do DataStore or heavy work per call.
- Creating remotes on the client — they won't exist on the server.
- Relying on ordering between an UnreliableRemoteEvent and a RemoteEvent.

## Related
- [[Client-Server-Boundary-And-Replication]]
- [[Anti-Exploit-And-Server-Authority]]
- [[Common-Libraries]]
- [[Performance-And-Profiling]]
- [[Luau-Strict-Typing]]

## Sources
- https://create.roblox.com/docs/scripting/events/remote (via github.com/Roblox/creator-docs, read 2026-10-04)
- https://create.roblox.com/docs/reference/engine/classes/RemoteEvent ("approximately 500 requests per second, per client … shared among all remote events of the same type", read 2026-10-04)
- https://create.roblox.com/docs/reference/engine/classes/UnreliableRemoteEvent (1,000-byte payload limit, read 2026-10-04)
- https://github.com/1Axen/blink, https://github.com/red-blox/zap, https://github.com/ffrostfall/ByteNet (tags checked 2026-10-04)
