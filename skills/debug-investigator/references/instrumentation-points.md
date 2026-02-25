# Instrumentation Points

Strategic placement of logging, breakpoints, and state inspection to maximize
diagnostic information with minimal code changes.

---

## Placement Strategy

### Where to Instrument

Add diagnostic output at these categories of locations, ordered by priority:

| Location | What to Log | Why |
|----------|------------|-----|
| Function entry | Arguments received | Verify inputs are what you expect |
| Function exit | Return value | Verify output is correct |
| Decision points | Branch taken, condition values | Understand which path executed |
| State mutations | Before and after values | Detect unexpected changes |
| External call boundaries | Request sent, response received | Isolate integration failures |
| Loop iterations | Counter, current element | Detect off-by-one, infinite loops |
| Exception handlers | Exception type, message, context | Understand what was caught and why |

### Minimum Effective Instrumentation

For a given function, the minimum useful instrumentation is:

```python
import logging
logger = logging.getLogger(__name__)

def process_order(order_id: int, items: list[dict]) -> str:
    logger.debug("process_order called: order_id=%s, item_count=%d", order_id, len(items))

    # ... function body ...

    if status == "invalid":
        logger.warning("Order %s invalid: reason=%s, items=%s", order_id, reason, items)

    logger.debug("process_order returning: order_id=%s, result=%s", order_id, result)
    return result
```

Three points: entry, anomaly, exit. This covers most debugging needs.

---

## Logging Patterns

### Structured Debug Logging

```python
# BAD: Unstructured, hard to grep
print(f"Something happened with {user}")

# GOOD: Structured, greppable, includes context
logger.debug(
    "token_validation: user_id=%s valid=%s expires=%s",
    user_id, is_valid, expiry_time,
)
```

### Conditional Debug Logging

For expensive-to-compute debug info, guard with level check:

```python
if logger.isEnabledFor(logging.DEBUG):
    logger.debug("Large object state: %s", expensive_serialize(obj))
```

### Temporary Instrumentation Pattern

When adding temporary debug logging, mark it clearly for removal:

```python
# DEBUG-TEMP: investigating issue #1234 — remove after resolution
logger.debug("DEBUG-TEMP: cache state at lookup: key=%s, cache_size=%d, hit=%s",
             key, len(cache), key in cache)
```

Search for `DEBUG-TEMP` to find and remove all temporary instrumentation after
the bug is resolved.

---

## Breakpoint Strategy

### Python Breakpoints

```python
# Built-in breakpoint (Python 3.7+)
breakpoint()  # Drops into pdb

# Conditional breakpoint
if order_id == 12345:
    breakpoint()

# Remote debugging (for servers)
import debugpy
debugpy.listen(5678)
debugpy.wait_for_client()  # Pauses until debugger attaches
```

### Breakpoint Placement

| Placement | Use When |
|-----------|----------|
| Before the failing line | Inspect state just before the crash |
| At function entry | Verify arguments are correct |
| Inside a condition body | Verify the condition was reached |
| In exception handler | Inspect the exception object |
| At the return statement | Verify the computed result |

### Post-Mortem Debugging

Instead of placing breakpoints before the error, let it crash and inspect:

```python
# Run with post-mortem debugging
python -m pdb -c continue script.py
# When it crashes, pdb activates at the crash point

# In pytest
pytest --pdb tests/test_failing.py
# Drops into pdb on the first failure
```

This is often faster than guessing where to place breakpoints.

---

## State Inspection Techniques

### Snapshot Pattern

Capture full state at a point in time:

```python
import json
import copy

def snapshot_state(label: str, **variables):
    """Log a snapshot of multiple variables for debugging."""
    state = {k: repr(v) for k, v in variables.items()}
    logger.debug("SNAPSHOT [%s]: %s", label, json.dumps(state, indent=2))

# Usage
snapshot_state("before_transform",
    input_data=data,
    config=config,
    cache_size=len(cache),
)
```

### Diff Pattern

Compare state before and after an operation:

```python
import copy

def debug_diff(label: str, obj: dict, operation):
    """Run an operation and log what changed in the object."""
    before = copy.deepcopy(obj)
    result = operation()
    after = obj

    changes = {
        k: {"before": before.get(k), "after": after.get(k)}
        for k in set(before) | set(after)
        if before.get(k) != after.get(k)
    }

    if changes:
        logger.debug("DIFF [%s]: %s", label, changes)
    else:
        logger.debug("DIFF [%s]: no changes", label)

    return result
```

### Watch Pattern

Monitor a value across multiple calls:

```python
class ValueWatch:
    """Track how a value changes across calls."""

    def __init__(self, name: str):
        self.name = name
        self.history: list = []

    def record(self, value, context: str = ""):
        self.history.append({"value": repr(value), "context": context})
        if len(self.history) >= 2:
            prev = self.history[-2]["value"]
            curr = self.history[-1]["value"]
            if prev != curr:
                logger.debug(
                    "WATCH [%s] changed: %s → %s (at %s)",
                    self.name, prev, curr, context,
                )

# Usage
watcher = ValueWatch("user_status")
watcher.record(user.status, "after_load")
# ... operations ...
watcher.record(user.status, "after_process")
```

---

## Choosing Between Logging and Breakpoints

| Use Logging When | Use Breakpoints When |
|------------------|---------------------|
| Bug is in production or CI | Bug is reproducible locally |
| Need to see execution flow across time | Need to inspect complex objects interactively |
| Bug is intermittent (need many data points) | Bug is deterministic |
| Multiple developers need to see output | Solo debugging session |
| Need to preserve evidence for documentation | Quick exploration |

---

## Instrumentation Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Logging inside tight loops | Floods logs, hides useful entries | Log summary after loop, or sample every Nth iteration |
| Logging sensitive data | Security risk (passwords, tokens) | Mask sensitive fields: `token=***{last4}` |
| Leaving debug logging permanently | Performance overhead, log noise | Use `DEBUG-TEMP` marker, clean up after resolution |
| Logging without context | "Error occurred" tells nothing | Always include identifiers: user_id, request_id, entity_id |
| `print()` instead of `logging` | Cannot control output, no levels | Use `logging` module with appropriate levels |
| Catching and logging without re-raising | Swallows the error | `logger.exception("...")` then `raise` |
