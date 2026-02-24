# Python Refinement Patterns

## Table of Contents
1. [Structural Patterns](#structural-patterns)
2. [Anti-Patterns to Eliminate](#anti-patterns-to-eliminate)
3. [Stdlib Replacements](#stdlib-replacements)
4. [Type Annotation Guidance](#type-annotation-guidance)
5. [Modern Python (3.10+)](#modern-python)

---

## Structural Patterns

### Guard Clauses over Nested Conditionals

```python
# Before
def process_order(order):
    if order is not None:
        if order.is_valid():
            if order.has_inventory():
                return fulfill(order)
            else:
                return "out of stock"
        else:
            return "invalid order"
    else:
        return "no order"

# After
def process_order(order):
    if order is None:
        return "no order"
    if not order.is_valid():
        return "invalid order"
    if not order.has_inventory():
        return "out of stock"
    return fulfill(order)
```

### Comprehensions over Accumulator Loops

Replace manual append loops with comprehensions when the logic is a straightforward
filter-map. Do NOT use comprehensions for complex multi-step logic or side effects.

```python
# Replace: filter + transform
results = []
for item in items:
    if item.is_active():
        results.append(item.name.lower())
# With:
results = [item.name.lower() for item in items if item.is_active()]

# Do NOT replace: complex logic with side effects
for item in items:
    validated = validate(item)  # may raise
    cache.store(validated)
    results.append(validated.id)
```

### Context Managers for Resource Cleanup

Any open/close, acquire/release, setup/teardown pair should use a context manager.

```python
# Before
f = open(path)
try:
    data = f.read()
finally:
    f.close()

# After
with open(path) as f:
    data = f.read()
```

For custom resources, prefer `contextlib.contextmanager` over writing `__enter__`/`__exit__`
for simple cases.

### Dataclasses over Raw Dicts/Tuples

When a dict has a fixed schema, replace with a dataclass. This gives you type checking,
immutability options, and readable attribute access.

```python
# Before
config = {"host": "localhost", "port": 8080, "debug": True}

# After
@dataclass(frozen=True)
class Config:
    host: str
    port: int
    debug: bool = False
```

---

## Anti-Patterns to Eliminate

### Bare `except`
Always catch specific exceptions. `except Exception` is acceptable as a last resort
with logging; bare `except:` catches SystemExit and KeyboardInterrupt.

### Mutable Default Arguments
```python
# Bug: shared mutable default
def append_to(item, target=[]):  # WRONG
    target.append(item)
    return target

# Fix:
def append_to(item, target=None):
    if target is None:
        target = []
    target.append(item)
    return target
```

### Type Checking with `type()` instead of `isinstance()`
`isinstance()` respects inheritance and supports union checks.

### String Concatenation in Loops
Use `"".join()` or f-strings. Repeated `+=` on strings creates O(n²) behavior.

### Redundant Boolean Comparisons
```python
# Before
if is_valid == True:
if len(items) > 0:
if result is not None:

# After
if is_valid:
if items:
if result is not None:  # Keep this one — explicit None check is intentional
```
Note: `if x is not None` is NOT the same as `if x`. Keep explicit None checks.

---

## Stdlib Replacements

| Pattern | Replace With |
|---------|-------------|
| Manual dict grouping loop | `collections.defaultdict` or `itertools.groupby` |
| `dict.get(k)` then check None | `dict.setdefault(k, default)` or `collections.defaultdict` |
| Manual counter loop | `collections.Counter` |
| Nested dict access with KeyError handling | `dict.get(k, {}).get(k2, default)` or a helper |
| Manual LRU cache | `functools.lru_cache` or `functools.cache` (3.9+) |
| Manual partial application | `functools.partial` |
| Manual chain of iterables | `itertools.chain` |
| `os.path.join` + `os.path.exists` | `pathlib.Path` |
| `subprocess.Popen` for simple commands | `subprocess.run` |
| Manual retry loops | Consider `tenacity` if already a dependency, otherwise a small helper |

---

## Type Annotation Guidance

- Annotate all public function signatures (parameters + return)
- Use `X | None` (3.10+) instead of `Optional[X]`
- Use `list[str]` (3.9+) instead of `List[str]`
- Use `TypeAlias` for complex types used more than once
- Use `Protocol` over ABC when you only need structural typing
- Use `@overload` when return type depends on input type

---

## Modern Python

### Structural Pattern Matching (3.10+)
Replace complex if/elif chains on type/structure with `match`:

```python
# Before
if isinstance(event, ClickEvent):
    handle_click(event.x, event.y)
elif isinstance(event, KeyEvent) and event.key == "enter":
    handle_submit()
elif isinstance(event, KeyEvent):
    handle_key(event.key)

# After
match event:
    case ClickEvent(x=x, y=y):
        handle_click(x, y)
    case KeyEvent(key="enter"):
        handle_submit()
    case KeyEvent(key=key):
        handle_key(key)
```

Only use when there are 3+ branches and the pattern destructuring adds clarity.

### Exception Groups (3.11+)
For concurrent error collection, use `ExceptionGroup` and `except*`.

### `tomllib` (3.11+)
Don't use third-party TOML parsers if you only need reading.
