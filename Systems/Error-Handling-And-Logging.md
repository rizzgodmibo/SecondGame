---
tags: [systems/reliability, systems/logging]
status: draft
updated: 2026-10-04
confidence: high
---
# Error Handling and Logging

## TL;DR
- Wrap every **web-backed call** in `pcall` with retry + exponential backoff + jitter: DataStore, MemoryStore, MessagingService, HttpService, MarketplaceService `GetProductInfoAsync`/`UserOwnsGamePassAsync`, TeleportService, `Players:GetUserThumbnailAsync`, `TextService:FilterStringAsync`, BadgeService.
- Use `xpcall(fn, debug.traceback)` (or a handler that adds `debug.traceback()`) where you need the stack.
- Use the **`task` library** only: `task.spawn`, `task.defer`, `task.delay`, `task.wait`, `task.cancel`. Never `spawn`, `delay`, `wait` (deprecated, throttled).
- Capture all uncaught server errors with `ScriptContext.Error` and send aggregated counts to analytics; watch the Creator Hub **Error Report** after each release.
- Structured log lines: `[Area] event key=value …`, with UserId (never usernames in analytics), place version (`game.PlaceVersion`), JobId.
- Promise libraries are optional; with strict typing and `task`, plain functions + Result tables are usually clearer.

## Details

### Retry with backoff
```lua
--!strict
-- ReplicatedStorage/Shared/Util/Retry.luau
local Retry = {}

export type Options = {
	attempts: number?,   -- default 5
	baseDelay: number?,  -- default 0.5 s
	maxDelay: number?,   -- default 8 s
	label: string?,
}

-- Calls fn until it succeeds. Returns (true, value) or (false, lastError).
function Retry.call<T>(fn: () -> T, opts: Options?): (boolean, T | string)
	local o = opts or {}
	local attempts = o.attempts or 5
	local base = o.baseDelay or 0.5
	local maxDelay = o.maxDelay or 8
	local lastErr = "unknown"
	for i = 1, attempts do
		local ok, result = pcall(fn)
		if ok then
			return true, result
		end
		lastErr = tostring(result)
		if i < attempts then
			local delay = math.min(maxDelay, base * 2 ^ (i - 1))
			delay *= 0.5 + math.random() -- jitter 50–150%
			warn(`[Retry] {o.label or "call"} attempt {i}/{attempts} failed: {lastErr}; retrying in {string.format("%.2f", delay)}s`)
			task.wait(delay)
		end
	end
	return false, lastErr
end

return Retry
```
Usage:
```lua
--!strict
local DataStoreService = game:GetService("DataStoreService")
local Retry = require(game:GetService("ReplicatedStorage").Shared.Util.Retry)
local store = DataStoreService:GetDataStore("Config_v1")

local ok, value = Retry.call(function(): any
	local v = store:GetAsync("LiveConfig") -- drop the 2nd return (DataStoreKeyInfo)
	return v
end, { label = "LoadConfig", attempts = 4 })
if not ok then
	warn("Using default config:", value)
end
```
Rules: don't retry non-transient errors (key too long, value too large 105, invalid args 10x) — check the error string/code and bail. Don't retry inside `UpdateAsync` transform functions. Respect `BindToClose` 30 s total — use fewer attempts during shutdown.

### pcall / xpcall / error
```lua
--!strict
local function risky(n: number): number
	if n < 0 then error("negative input", 2) end -- level 2 blames the caller
	return math.sqrt(n)
end

local ok, res = xpcall(risky, function(err)
	return `{err}\n{debug.traceback(nil, 2)}`
end, -1)
if not ok then warn(res) end
```
- `error({code = "NoFunds"})` — tables can be thrown for typed error handling; convert at module boundaries.
- `assert(cond, msg)` for programmer errors (invariants), not for user input — user input gets graceful rejection.

### task library cheatsheet
| Function | Behaviour | Use |
|---|---|---|
| `task.spawn(fn, ...)` | Runs now until first yield | Fire-and-forget that should start immediately |
| `task.defer(fn, ...)` | Runs at next resumption point (end of current step) | Avoid re-entrancy in signal handlers |
| `task.delay(t, fn, ...)` | After `t` s | Timers; store the thread to cancel |
| `task.wait(t?)` | Yields ≥ t (min 1 frame) | Loops; returns actual elapsed |
| `task.cancel(thread)` | Cancels a spawned/delayed thread | Cleanup of timers |
| `task.desynchronize/synchronize` | Parallel phases | [[Parallel-Luau]] |
Errors inside `task.spawn` don't propagate to the caller; they go to output/ScriptContext.Error. Wrap the body if the caller needs to know.

### Global error capture (server)
```lua
--!strict
-- ServerScriptService/Server/Services/ErrorReporter.luau
local ScriptContext = game:GetService("ScriptContext")

local ErrorReporter = {}
local counts: { [string]: number } = {}
local FLUSH_INTERVAL = 60

local function signature(message: string, trace: string): string
	-- strip numbers/addresses so similar errors aggregate
	local first = string.split(trace, "\n")[1] or ""
	return (string.gsub(message, "%d+", "N")) .. " @ " .. first
end

function ErrorReporter.Start(self: typeof(ErrorReporter))
	ScriptContext.Error:Connect(function(message: string, trace: string, _script: Instance?)
		local sig = string.sub(signature(message, trace), 1, 200)
		counts[sig] = (counts[sig] or 0) + 1
	end)
	task.spawn(function()
		while true do
			task.wait(FLUSH_INTERVAL)
			for sig, n in counts do
				print(`[Error] count={n} v={game.PlaceVersion} job={game.JobId} sig={sig}`)
				-- Optional: forward to an external sink via HttpService (batched, rate-limited).
				-- AnalyticsService custom events are per-player; ⚠️ verify: an API for server-wide (non-player) events.
			end
			table.clear(counts)
		end
	end)
end

return ErrorReporter
```
Client errors: Roblox collects client script errors into the Creator Hub Error Report automatically ⚠️ verify: whether client errors appear in the Error Report or only server errors. For custom client error telemetry, forward rate-limited summaries to the server via a remote (max ~1 per 10 s per player, truncated to 200 chars).

### Structured logging
```lua
--!strict
-- ReplicatedStorage/Shared/Util/Log.luau
local RunService = game:GetService("RunService")
local Log = {}
local SIDE = if RunService:IsServer() then "S" else "C"
local DEBUG_ENABLED = RunService:IsStudio()

local function fmt(area: string, event: string, fields: { [string]: any }?): string
	local parts = { `[{SIDE}][{area}] {event}` }
	if fields then
		for k, v in fields do table.insert(parts, `{k}={tostring(v)}`) end
	end
	return table.concat(parts, " ")
end

function Log.debug(area: string, event: string, fields: { [string]: any }?)
	if DEBUG_ENABLED then print(fmt(area, event, fields)) end
end
function Log.info(area: string, event: string, fields: { [string]: any }?)
	print(fmt(area, event, fields))
end
function Log.warn(area: string, event: string, fields: { [string]: any }?)
	warn(fmt(area, event, fields))
end

return Log
```
Usage: `Log.info("Shop", "purchase", { userId = player.UserId, item = id, price = cost })`.
Server output from live servers is visible in Dev Console (F9 → Server tab) for developers; for persistent logs use AnalyticsService custom/economy/funnel events (see the Operations folder) or an external HTTP sink with batching (HttpService: 500 requests/min per server for external URLs; Open Cloud calls from HttpService have a separate 2,500/min per server — docs, 2026-10-04).

### Promise libraries
- `evaera/roblox-lua-promise` (v4.0.0-rc.3 tag, 2026-10-04) — mature, chaining/cancellation/`Promise.retryWithDelay`. Typed poorly in strict mode.
- Use when: complex async orchestration with cancellation (cutscenes, sequential loading with timeouts). Skip when: simple retries — use `Retry.call`.

## Checklist
- [ ] `Retry.call` around every web-backed API.
- [ ] No `wait(`, `spawn(`, `delay(` in codebase (CI grep / Selene `deprecated` lint).
- [ ] ErrorReporter running on server; Error Report checked after each publish.
- [ ] Logs include UserId, PlaceVersion, JobId; no usernames/PII in external sinks.
- [ ] Debug logs off in live servers.

## Pitfalls
- Retrying instantly in a tight loop → throttling cascades (DataStore queue full errors 301–306).
- Swallowing errors with bare `pcall(fn)` and ignoring the result.
- Yielding inside `ProcessReceipt` for too long without a timeout.
- `warn` spam in hot paths (every frame) tanks performance and floods output.
- Sending raw error messages to clients (leaks internals).

## Related
- [[Data-Persistence-DataStores-And-ProfileStore]]
- [[Common-Libraries]]
- [[Module-Architecture]]
- [[Anti-Exploit-And-Server-Authority]]

## Sources
- https://create.roblox.com/docs/reference/engine/libraries/task (via github.com/Roblox/creator-docs, 2026-10-04)
- https://create.roblox.com/docs/reference/engine/classes/ScriptContext#Error
- https://create.roblox.com/docs/cloud-services/data-stores/error-codes-and-limits
- https://create.roblox.com/docs/cloud-services/http-service (HTTP limits)
- https://github.com/evaera/roblox-lua-promise (tag checked 2026-10-04)
