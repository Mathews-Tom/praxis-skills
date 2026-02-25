# Stacktrace Patterns

Common exception patterns across Python and JavaScript, how to read tracebacks
efficiently, and what each exception type reveals about the root cause.

---

## Reading Python Tracebacks

### Structure

```
Traceback (most recent call last):
  File "main.py", line 10, in <module>      ← Entry point (oldest frame)
    result = process(data)
  File "processor.py", line 25, in process   ← Intermediate frame
    return transform(validated)
  File "transform.py", line 8, in transform  ← Failure point (newest frame)
    return data["key"]
KeyError: 'key'                              ← Exception type + message
```

**Read bottom-up.** The last frame shows where the error manifested. The frames above
show how execution reached that point. The root cause is often NOT in the bottom frame —
it's in a frame that passed bad data downstream.

### Key Questions

1. **What is the exception type?** — This narrows the category immediately.
2. **What is the message?** — Often contains the specific value that caused the failure.
3. **Where did it originate?** — The bottom frame's file and line number.
4. **Where was the bad data introduced?** — Trace upward through frames to find where
   the problematic value was created or modified.

---

## Python Exception Taxonomy

### AttributeError

```python
AttributeError: 'NoneType' object has no attribute 'name'
```

| Cause | Frequency | Investigation |
|-------|-----------|---------------|
| Variable is `None` when expected to be an object | Very common | Find where the variable was assigned — a function returned `None` unexpectedly |
| Wrong variable name (typo) | Common | Check spelling against class definition |
| Method called on wrong type | Moderate | Check what type the object actually is with logging |
| Missing import or circular import | Rare | Check if the module loaded correctly |

**First check:** What assigned the value? Look one frame up for the source.

### KeyError

```python
KeyError: 'user_id'
```

| Cause | Frequency | Investigation |
|-------|-----------|---------------|
| Expected key missing from dict | Very common | Print the dict's actual keys |
| Key name typo | Common | Compare key string with source dict |
| Dict was populated conditionally | Moderate | Check if the populating code ran |
| Dict replaced by different structure | Rare | Check where dict was last assigned |

**First check:** Log `dict.keys()` at the failure point.

### TypeError

```python
TypeError: unsupported operand type(s) for +: 'int' and 'str'
TypeError: func() takes 2 positional arguments but 3 were given
TypeError: 'NoneType' object is not callable
```

| Pattern | Cause | Investigation |
|---------|-------|---------------|
| `unsupported operand` | Wrong types in operation | Check types of both operands |
| `takes N arguments but M given` | Wrong number of args | Check function signature vs call site |
| `not callable` | Calling a non-function | Variable shadowing a function name |
| `not subscriptable` | Indexing a non-sequence | Check actual type of the object |
| `not iterable` | Iterating over non-iterable | Check what the loop variable actually is |

### ValueError

```python
ValueError: invalid literal for int() with base 10: 'abc'
ValueError: too many values to unpack (expected 2)
```

| Pattern | Cause | Investigation |
|---------|-------|---------------|
| `invalid literal` | String→number conversion failure | Check the input data format |
| `too many/not enough values to unpack` | Tuple/list size mismatch | Check the actual length of the iterable |
| `is not in list` | `.index()` or `.remove()` on missing element | Verify element exists before operating |

### ImportError / ModuleNotFoundError

```python
ModuleNotFoundError: No module named 'mypackage'
ImportError: cannot import name 'func' from 'module'
```

| Cause | Investigation |
|-------|---------------|
| Package not installed | `pip list | grep package` or check requirements |
| Virtual environment not activated | Check `which python` |
| Circular import | A imports B which imports A — restructure |
| Name doesn't exist in module | Check actual exports: `dir(module)` |
| Relative import from wrong location | Check `__package__` and working directory |

### IndexError

```python
IndexError: list index out of range
```

| Cause | Investigation |
|-------|---------------|
| Off-by-one in loop | Check `range()` bounds vs list length |
| Empty list accessed | Check if list was populated |
| Hardcoded index on variable-length data | Use `len()` check or `try/except` |

### RuntimeError

```python
RuntimeError: dictionary changed size during iteration
RuntimeError: This event loop is already running
```

| Pattern | Cause | Fix |
|---------|-------|-----|
| `dictionary changed size` | Modifying dict while iterating | Iterate over `list(dict.keys())` copy |
| `event loop is already running` | Nested `asyncio.run()` | Use `await` directly in async context |
| `maximum recursion depth` | Infinite recursion | Find the cycle in call chain |

---

## JavaScript Error Patterns

### TypeError

```javascript
TypeError: Cannot read properties of undefined (reading 'name')
TypeError: x is not a function
```

| Pattern | Cause | Investigation |
|---------|-------|---------------|
| `Cannot read properties of undefined` | Accessing property on undefined | Check the full property chain — which part is undefined |
| `Cannot read properties of null` | Accessing property on null | API returned null, or DOM element not found |
| `x is not a function` | Calling non-function | Import error, wrong export, or variable shadowing |
| `x is not a constructor` | Using `new` on non-constructor | Check the imported value type |

### ReferenceError

```javascript
ReferenceError: x is not defined
```

Always a scope issue: variable not declared, or declared in a different scope.

### SyntaxError at Runtime

```javascript
SyntaxError: Unexpected token '<' (in JSON)
```

Almost always: server returned HTML (error page) instead of JSON. Check the response
body, not the parsing code.

---

## Multi-Frame Analysis

### Identifying the Real Cause

The error manifests at the bottom frame but the root cause is often higher:

```python
# Frame 3: Root cause — get_user returns None for missing users
def get_user(user_id):
    return db.query(User).filter_by(id=user_id).first()  # Returns None

# Frame 2: Passes None downstream without checking
def get_user_email(user_id):
    user = get_user(user_id)
    return user.email  # AttributeError here when user is None

# Frame 1: Entry point
def send_notification(user_id):
    email = get_user_email(user_id)
    send_email(email, "Hello")
```

**Pattern:** Look for the frame where an assumption was made (Frame 2 assumes `user`
is not `None`) and the frame that violated that assumption (Frame 3 returns `None`).

### Library Frames vs Application Frames

Tracebacks often include library internals. Focus on YOUR code first:

```
Traceback (most recent call last):
  File "myapp/views.py", line 15, in handler     ← YOUR CODE
    result = process(request.data)
  File "myapp/processor.py", line 8, in process   ← YOUR CODE (likely cause)
    return json.loads(raw)
  File "/usr/lib/python3.12/json/__init__.py"...   ← LIBRARY (symptom)
json.decoder.JSONDecodeError: ...
```

The bug is in `processor.py` (passing invalid data to `json.loads`), not in the JSON
library.

---

## Chained Exceptions

### Python's `raise ... from ...`

```python
ValueError: Invalid user data
  During handling of the above exception, another exception occurred:
ProcessingError: Failed to process user 42
```

Read the **original** exception (first one) for the root cause. The second exception
is a wrapper that adds context.

### `__cause__` vs `__context__`

- `raise X from Y` → `X.__cause__ = Y` (explicit chain)
- Exception during `except` handling → `X.__context__ = Y` (implicit chain)

Always trace to the original exception for the root cause.
