# Mock Strategies

Decision framework for when, what, and how to mock in pytest test suites. Mocks are
a necessary tool for isolating units under test from external dependencies — but
over-mocking creates brittle tests that pass when the code is broken.

---

## The Mock Decision Tree

Before adding a mock, answer these questions in order:

1. **Is the dependency external?** (network, DB, filesystem, clock, random)
   - Yes → mock it
   - No → proceed to question 2

2. **Is the dependency slow or non-deterministic?**
   - Yes → mock it
   - No → proceed to question 3

3. **Does the dependency have side effects you want to prevent?**
   - Yes → mock it
   - No → **do not mock** — test through the real implementation

---

## What to Mock

| Dependency Type | Mock Strategy | Example |
|----------------|---------------|---------|
| HTTP API calls | `patch("module.requests.get")` | Third-party REST API |
| Database queries | `patch("module.db.execute")` or use test DB | SQL queries, ORM calls |
| Filesystem I/O | `tmp_path` fixture or `patch("builtins.open")` | File reads/writes |
| Current time | `patch("module.datetime")` with fixed return | Time-dependent logic |
| Random values | `patch("module.random.randint")` with fixed return | Non-deterministic logic |
| Email/SMS sending | `patch("module.send_email")` | Side-effect-only operations |
| External processes | `patch("module.subprocess.run")` | Shell commands |

## What NOT to Mock

| Do Not Mock | Why | Test Instead |
|-------------|-----|--------------|
| The function under test | Defeats the purpose of testing | Call the real function |
| Pure helper functions | Testing through the caller covers them | Call the caller with real helpers |
| Data classes / value objects | No side effects to isolate | Use real instances |
| Standard library operations | They are tested; you are not testing Python | Use real operations |
| Simple constructors | No benefit to mocking `__init__` | Create real objects |

**Anti-pattern: mock cascade.** If you find yourself mocking 5+ things for a single test,
the code under test likely has too many dependencies. Flag this as a design issue rather
than adding more mocks.

---

## Patch Boundaries

### Patch at the Import Site, Not the Definition Site

```python
# mymodule.py
from requests import get

def fetch_data(url):
    return get(url).json()

# test_mymodule.py
# CORRECT — patch where it is imported
@patch("mymodule.get")
def test_fetch_data(mock_get):
    mock_get.return_value.json.return_value = {"key": "value"}
    result = fetch_data("https://api.example.com")
    assert result == {"key": "value"}

# WRONG — patching the source module has no effect
@patch("requests.get")  # This won't intercept mymodule.get
def test_fetch_data_wrong(mock_get):
    ...
```

### Context Manager vs Decorator

```python
# Decorator — cleaner for entire test function
@patch("mymodule.external_call")
def test_with_decorator(mock_call):
    mock_call.return_value = "mocked"
    assert my_function() == "mocked"

# Context manager — when mock needed for part of the test
def test_with_context():
    setup_real_state()
    with patch("mymodule.external_call") as mock_call:
        mock_call.return_value = "mocked"
        assert my_function() == "mocked"
    # mock_call is unpatched here
```

### pytest-mock's `mocker` Fixture

```python
def test_with_mocker(mocker):
    mock_call = mocker.patch("mymodule.external_call")
    mock_call.return_value = "mocked"
    assert my_function() == "mocked"
    # Automatically unpatched after test
```

Advantage over `@patch`: no decorator stacking for multiple patches, cleaner with fixtures.

---

## Mock Assertions

Every mock must have at least one assertion. A mock without assertions is invisible
to the test — the code could skip the call entirely and the test would still pass.

### Call Assertions

```python
# Called exactly once
mock_db.query.assert_called_once()

# Called with specific arguments
mock_db.query.assert_called_once_with("SELECT * FROM users WHERE id = %s", (42,))

# Called at least once
mock_db.query.assert_called()

# Never called
mock_db.query.assert_not_called()

# Call count
assert mock_db.query.call_count == 3

# Inspect all calls
assert mock_db.query.call_args_list == [
    call("query1"),
    call("query2"),
    call("query3"),
]
```

### Return Value Configuration

```python
# Single return value
mock_api.get.return_value = {"status": "ok"}

# Different returns per call
mock_api.get.side_effect = [
    {"status": "ok"},
    {"status": "error"},
    ConnectionError("timeout"),
]

# Conditional return based on input
def selective_return(key):
    return {"a": 1, "b": 2}.get(key)
mock_db.lookup.side_effect = selective_return
```

### Exception Simulation

```python
mock_api.get.side_effect = ConnectionError("network unreachable")

with pytest.raises(ConnectionError):
    fetch_data("https://api.example.com")
```

---

## Anti-Patterns

### 1. Over-Mocking

```python
# BAD: Mocking everything, testing nothing
@patch("module.validate")
@patch("module.transform")
@patch("module.save")
def test_process(mock_save, mock_transform, mock_validate):
    mock_validate.return_value = True
    mock_transform.return_value = "transformed"
    process("input")
    mock_save.assert_called_once()
    # This test verifies call order, not behavior
```

### 2. Mocking the Subject Under Test

```python
# BAD: You are testing the mock, not the code
@patch("module.my_function")
def test_my_function(mock_fn):
    mock_fn.return_value = 42
    assert my_function() == 42  # Always passes, proves nothing
```

### 3. No Assertions on Mocks

```python
# BAD: Mock exists but is never verified
@patch("module.send_email")
def test_register_user(mock_email):
    register_user("alice@example.com")
    # mock_email is never asserted — email could be skipped silently
```

### 4. Patch Leaking Across Tests

```python
# BAD: Manual patch without cleanup
def test_something():
    patcher = patch("module.thing")
    mock_thing = patcher.start()
    # Missing patcher.stop() — leaks into subsequent tests
```

Use `@patch` decorator, `with` statement, or `mocker` fixture to auto-cleanup.

---

## Mock Types Reference

| Type | Import | Use When |
|------|--------|----------|
| `Mock` | `unittest.mock.Mock` | General-purpose mock object |
| `MagicMock` | `unittest.mock.MagicMock` | Mock with magic methods (`__len__`, `__iter__`, etc.) |
| `AsyncMock` | `unittest.mock.AsyncMock` | Mock for coroutines and async methods |
| `PropertyMock` | `unittest.mock.PropertyMock` | Mock a `@property` |
| `patch` | `unittest.mock.patch` | Replace an attribute with a mock during a test |
| `patch.object` | `unittest.mock.patch.object` | Patch attribute on an object instance |
| `patch.dict` | `unittest.mock.patch.dict` | Temporarily modify a dictionary |
| `create_autospec` | `unittest.mock.create_autospec` | Mock that enforces the original's signature |

`create_autospec` is the safest choice for complex interfaces — it raises `TypeError`
if the mock is called with the wrong number of arguments.
