---
tags: [systems/luau, systems/typing]
status: draft
updated: 2026-10-04
confidence: high
---
# Luau Strict Typing

## TL;DR
- Put `--!strict` on line 1 of **every** script and ModuleScript. New code that does not type-check in strict mode does not ship.
- Annotate **module boundaries** (function params/returns, exported tables, remote payloads); let inference handle locals.
- Define shared shapes once in `ReplicatedStorage/Shared/Types.luau` with `export type` and import them with `require(...)` + `Types.Name`.
- Treat every value from the network, DataStore or `Instance:GetAttribute()` as `unknown` and **narrow** it with `typeof()` checks — static types are not runtime validation.
- Use `--!native` / `@native` only on hot, numeric, server-side code and **measure** with the Script Profiler; never blanket-apply it.
- Escape hatches (`:: any`, `--!nonstrict`) need a comment explaining why; treat them as tech debt.

## Details

### Modes
| Directive | Meaning | Use |
|---|---|---|
| `--!strict` | Every inferred/annotated type is checked | Default for all code |
| `--!nonstrict` | Only explicitly annotated vars are checked; unannotated → `any` | Legacy/imported code only |
| `--!nocheck` | No type checking | Generated code, vendored libs |
| `--!native` | Compile script's functions to machine code (if profitable) | Hot server math (see below) |
| `--!optimize 2` | Already the default in live games; mostly irrelevant ⚠️ verify: whether Studio defaults to O1 | Rarely needed |

### Annotation cheat sheet
```lua
--!strict
-- ReplicatedStorage/Shared/Types.luau
export type ItemId = string
export type Rarity = "Common" | "Rare" | "Epic" | "Legendary"   -- string singleton union

export type Item = {
	id: ItemId,
	rarity: Rarity,
	level: number,
	tags: { string },             -- array
	stats: { [string]: number },  -- dictionary
	owner: Player?,               -- optional (Player | nil)
}

export type Result<T> = { ok: true, value: T } | { ok: false, err: string }  -- tagged union

export type Callback = (player: Player, amount: number) -> ()
export type Variadic = (...number) -> number

return {}
```
```lua
--!strict
-- Usage elsewhere
local Types = require(game:GetService("ReplicatedStorage").Shared.Types)

local function rollRarity(weights: { [Types.Rarity]: number }): Types.Rarity
	local total = 0
	for _, w in weights do total += w end
	local r = math.random() * total
	for rarity, w in weights do
		r -= w
		if r <= 0 then return rarity end
	end
	return "Common"
end
```

### Generics
```lua
--!strict
local function map<T, U>(list: { T }, fn: (T) -> U): { U }
	local out = table.create(#list)
	for i, v in list do out[i] = fn(v) end
	return out
end

local function find<T>(list: { T }, pred: (T) -> boolean): T?
	for _, v in list do
		if pred(v) then return v end
	end
	return nil
end

export type Pool<T> = { acquire: () -> T, release: (T) -> () }
```

### Classes (metatable OOP) that type-check
```lua
--!strict
-- ReplicatedStorage/Shared/Timer.luau
local Timer = {}
Timer.__index = Timer

type TimerData = { duration: number, startedAt: number? }
export type Timer = typeof(setmetatable({} :: TimerData, Timer))

function Timer.new(duration: number): Timer
	return setmetatable({ duration = duration, startedAt = nil } :: TimerData, Timer)
end

function Timer.start(self: Timer)
	self.startedAt = os.clock()
end

function Timer.remaining(self: Timer): number
	local s = self.startedAt
	if s == nil then return self.duration end
	return math.max(0, self.duration - (os.clock() - s))
end

return Timer
```
Rule: declare methods as `function Timer.method(self: Timer, ...)` (dot + explicit `self`) — `:` sugar gives `self` an inferred type that often fails in strict mode.

### `typeof` (two meanings)
- **Type-level** `typeof(expr)` — gives the inferred type of an expression: `type Config = typeof(DEFAULT_CONFIG)`. Use this to derive the profile data type from the ProfileStore template.
- **Runtime** `typeof(v)` — returns a string, `"Instance"`, `"Vector3"`, `"CFrame"`, etc. (prefer over `type()`, which returns `"userdata"` for Roblox types). Use for narrowing:
```lua
--!strict
local function readNumber(v: unknown): number?
	if typeof(v) == "number" and v == v and v ~= math.huge and v ~= -math.huge then
		return v -- narrowed to number; rejects NaN and ±inf
	end
	return nil
end
```
- `v:IsA("BasePart")` narrows `Instance` → `BasePart` in strict mode.

### Casts
- `expr :: T` — assertion; only allowed when types are compatible. `x :: any :: T` forces it (avoid).
- Prefer narrowing (`if typeof(x) == ...`, `assert(x, ...)`, `if x then`) over casting.

### Common strict-mode errors and fixes
| Error (paraphrased) | Cause | Fix |
|---|---|---|
| `Key 'Foo' not found in table 'Instance'` | `workspace.Map.Foo` — children aren't typed | `workspace:WaitForChild("Map"):FindFirstChild("Foo")` then `:IsA()` narrow, or `:: Model` cast once at a typed boundary |
| `Value of type 'X?' could be nil` | optional not narrowed | `if x then … end`, `assert(x)`, or early return |
| `Type 'unknown' could not be converted into 'number'` | remote/attribute payload | `typeof(v) == "number"` guard |
| `Unknown require: unsupported path` | dynamic require path | Require via a static expression (`script.Parent.Foo`, `ReplicatedStorage.Shared.Foo`); `luau-lsp` with a Rojo sourcemap resolves them |
| `Cannot add property 'x' to table` | sealed table literal | Declare the field in the type / initial literal, or annotate the table type up front |
| `Type 'Player' could not be converted into 'Instance?'` style mismatches in `FindFirstChildOfClass` | API returns base `Instance` | Narrow with `:IsA()` |
| Recursive type errors in OOP | `:` methods on metatables | Use the `typeof(setmetatable(...))` pattern above |
| `Generic function does not satisfy...` | mismatched generic variance | Annotate the call site: `map(list, function(x: number): string ... end)` |

### Native code generation (`--!native`, `@native`)
- Compiles a script's **functions** to machine code; the top-level scope gains little. Docs describe it for **server-side scripts**. ⚠️ verify: whether client-side native codegen is now enabled.
- There is a **game-wide limit on total natively compiled code** and extra memory cost → prefer `@native` on specific hot functions over `--!native` on whole files.
- Wins: tight numeric loops, buffer manipulation, custom serialisers, noise/terrain gen, pathfinding grids. No win: code dominated by Roblox API calls.
- Type annotations help native codegen choose fast paths (e.g. annotate `vector`/`Vector3`/`number` params).
```lua
--!strict
@native
local function sumSquares(values: { number }): number
	local total = 0
	for _, v in values do total += v * v end
	return total
end
```

### New type solver
Roblox has been rolling out a new Luau type solver (better generics, `read`/`write` property modifiers, type functions). ⚠️ verify: current Studio default solver and whether user-defined type functions are enabled in production. Code written against the patterns above works on both.

## Checklist
- [ ] `--!strict` first line of every Luau file (enforce with a CI grep or `luau-lsp analyze`).
- [ ] Shared types in `ReplicatedStorage/Shared/Types.luau`.
- [ ] All `OnServerEvent` / `OnServerInvoke` params typed as `unknown` and narrowed.
- [ ] Profile data type derived with `typeof(TEMPLATE)`.
- [ ] Zero type errors in `luau-lsp analyze` in CI.
- [ ] `@native` only where Script Profiler shows a hot function, with before/after numbers recorded.

## Pitfalls
- Typing a remote handler param as `number` gives **zero** runtime safety — exploiters send anything. Validate at runtime.
- `type(v)` vs `typeof(v)`: `type(Vector3.zero)` is `"userdata"`; always use `typeof`.
- NaN passes `typeof(v) == "number"` and breaks comparisons (`NaN ~= NaN`). Check `v == v`.
- `table.freeze` makes tables read-only at runtime but the type system won't stop writes in all solver versions — don't rely on it for type safety.
- Overusing `:: any` silently disables checking downstream.
- `--!native` everywhere can exhaust the native code budget so later scripts silently fall back to the interpreter.

## Related
- [[Module-Architecture]]
- [[Remotes-And-Networking]]
- [[Performance-And-Profiling]]
- [[Tooling-Rojo-Wally-And-Studio-MCP]]
- [[_Index]]

## Sources
- https://create.roblox.com/docs/luau/type-checking (read via github.com/Roblox/creator-docs mirror, 2026-10-04)
- https://create.roblox.com/docs/luau/native-code-gen (same mirror, 2026-10-04)
- https://luau.org/typecheck
