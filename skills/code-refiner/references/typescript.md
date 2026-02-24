# TypeScript / JavaScript Refinement Patterns

## Table of Contents
1. [Type System Leverage](#type-system-leverage)
2. [Structural Patterns](#structural-patterns)
3. [Module Design](#module-design)
4. [Anti-Patterns](#anti-patterns)
5. [React Specific](#react-specific)

---

## Type System Leverage

### Discriminated Unions over Type Guards
```typescript
// Before — stringly typed, easy to miss a case
type Event = { type: string; payload: unknown };

function handle(event: Event) {
    if (event.type === "click") { ... }
    else if (event.type === "key") { ... }
}

// After — exhaustive, compiler-checked
type Event =
    | { type: "click"; x: number; y: number }
    | { type: "key"; key: string };

function handle(event: Event) {
    switch (event.type) {
        case "click": return handleClick(event.x, event.y);
        case "key": return handleKey(event.key);
    }
    // Exhaustiveness: event is `never` here
    const _exhaustive: never = event;
}
```

### `satisfies` for Validated Object Literals
```typescript
const config = {
    port: 8080,
    host: "localhost",
} satisfies ServerConfig;
// Type is inferred precisely (literal types), but validated against ServerConfig
```

### Branded Types for Domain Identifiers
```typescript
type UserId = string & { readonly __brand: "UserId" };
type OrderId = string & { readonly __brand: "OrderId" };

// Prevents accidentally passing a UserId where OrderId is expected
function getOrder(id: OrderId): Order { ... }
```

### `const` Assertions for Immutable Literals
```typescript
const DIRECTIONS = ["north", "south", "east", "west"] as const;
type Direction = typeof DIRECTIONS[number]; // "north" | "south" | "east" | "west"
```

---

## Structural Patterns

### Early Returns / Guard Clauses
Same principle as all languages. Flatten the happy path:
```typescript
// Before — deeply nested
async function processRequest(req: Request): Promise<Response> {
    if (req.body) {
        const parsed = JSON.parse(req.body);
        if (parsed.userId) {
            const user = await getUser(parsed.userId);
            if (user) {
                return buildResponse(user);
            }
        }
    }
    return errorResponse(400);
}

// After
async function processRequest(req: Request): Promise<Response> {
    if (!req.body) return errorResponse(400);
    const parsed = JSON.parse(req.body);
    if (!parsed.userId) return errorResponse(400);
    const user = await getUser(parsed.userId);
    if (!user) return errorResponse(400);
    return buildResponse(user);
}
```

### Object Destructuring for Clarity
```typescript
// Before
function render(props: Props) {
    return h("div", null, props.title, props.description, props.author.name);
}

// After
function render({ title, description, author: { name } }: Props) {
    return h("div", null, title, description, name);
}
```

### `Map` / `Set` over Object Lookup
When keys are dynamic or non-string, use `Map`/`Set`. They have proper iteration
order, `.size`, and don't conflict with prototype properties.

---

## Module Design

### Named Exports over Default
Named exports enable better tree-shaking, refactoring support, and import consistency.

### Barrel Files — Use Sparingly
`index.ts` re-exports are convenient but can break tree-shaking and create circular
dependency issues. Use for public API surfaces, not internal organization.

### Explicit Extensions in Imports
For ESM projects, include `.js` extensions in import paths (even for `.ts` source files
when targeting Node ESM).

---

## Anti-Patterns

| Anti-Pattern | Fix |
|-------------|-----|
| `any` type annotations | Narrow to specific types; use `unknown` + type guards if truly dynamic |
| Nested ternaries | `switch`, if/else chain, or extracted function |
| `== null` vs `=== null` | Use `== null` to catch both null and undefined (this is intentional) |
| `Promise` constructor for async/await wrapping | Just use `async`/`await` directly |
| `setTimeout(fn, 0)` for ordering | Use `queueMicrotask` or restructure logic |
| `for...in` on arrays | Use `for...of`, `.forEach()`, or array methods |
| Throwing strings | Throw `Error` instances (preserves stack traces) |
| Enum with string values for simple union | Use string literal union type instead |

---

## React Specific

### Component Extraction Signals
Extract a component when:
- A JSX block has its own state or effects
- The same markup pattern appears 3+ times
- A section has a distinct responsibility (form, list, header)

### Hook Composition
Extract custom hooks when:
- Multiple state/effect pairs work together
- The same hook combination appears in multiple components
- Business logic can be separated from presentation

### Avoid Inline Object/Array Literals in JSX Props
```tsx
// Before — creates new reference every render, breaks memoization
<Chart options={{ animate: true }} data={[1, 2, 3]} />

// After
const chartOptions = useMemo(() => ({ animate: true }), []);
const data = useMemo(() => [1, 2, 3], []);
<Chart options={chartOptions} data={data} />
```

### Prefer `key` on List Items from Stable Identifiers
Never use array index as key for lists that can reorder.
