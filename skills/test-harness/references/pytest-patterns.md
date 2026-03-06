# Pytest Patterns

Core pytest patterns for test organization, fixture management, parametrization, and
built-in utilities. Load this reference for every test generation task.

---

## Fixture Scopes

Fixtures control setup and teardown. Scope determines how often the fixture runs.

| Scope      | Runs                             | Typical Use                       |
| ---------- | -------------------------------- | --------------------------------- |
| `function` | Once per test function (default) | Fresh state per test              |
| `class`    | Once per test class              | Shared DB connection across class |
| `module`   | Once per test file               | Loaded config, parsed data        |
| `session`  | Once per entire test run         | Docker container, server process  |

```python
@pytest.fixture(scope="module")
def loaded_config():
    """Parse config once for the entire module."""
    return parse_config("test_config.toml")
```

**Scope selection rule:** Use the narrowest scope that avoids redundant expensive setup.
When in doubt, use `function` scope — it is the safest default.

---

## Parametrize

`@pytest.mark.parametrize` runs a test with multiple input sets.

### Basic Usage

```python
@pytest.mark.parametrize(
    "input_val, expected",
    [
        ("hello", 5),
        ("", 0),
        ("a" * 1000, 1000),
    ],
    ids=["normal", "empty", "long"],
)
def test_string_length(input_val, expected):
    assert len(input_val) == expected
```

### Multiple Parameters

```python
@pytest.mark.parametrize("x", [1, 2, 3])
@pytest.mark.parametrize("y", [10, 20])
def test_multiply(x, y):
    """Runs 6 combinations: (1,10), (1,20), (2,10), (2,20), (3,10), (3,20)."""
    assert x * y == x * y
```

### IDs for Readability

Always provide `ids` when parametrizing. Without IDs, pytest generates `test_func[0]`,
`test_func[1]`, etc. which are uninformative on failure.

```python
# Good: ids describe the scenario
ids=["empty_string", "single_char", "unicode", "with_spaces"]

# Bad: no ids, failures show test_func[0-3]
```

### Parametrize with Fixtures

Cannot directly parametrize fixture values. Use `pytest.fixture(params=...)` instead:

```python
@pytest.fixture(params=["sqlite", "postgres", "mysql"], ids=lambda p: f"db-{p}")
def db_engine(request):
    return create_engine(request.param)
```

---

## Markers

Built-in and custom markers for test classification.

| Marker                                         | Purpose                     | Usage                         |
| ---------------------------------------------- | --------------------------- | ----------------------------- |
| `@pytest.mark.skip(reason="...")`              | Skip unconditionally        | Broken test, known issue      |
| `@pytest.mark.skipif(condition, reason="...")` | Skip on condition           | OS-specific, version-specific |
| `@pytest.mark.xfail(reason="...")`             | Expected failure            | Known bug, pending fix        |
| `@pytest.mark.parametrize(...)`                | Multi-input test            | See above                     |
| `@pytest.mark.asyncio`                         | Async test (pytest-asyncio) | Coroutine tests               |
| `@pytest.mark.slow`                            | Custom: slow tests          | Filter with `-m "not slow"`   |

### Registering Custom Markers

In `pyproject.toml` or `pytest.ini`:

```toml
[tool.pytest.ini_options]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks integration tests",
]
```

---

## conftest.py

Shared fixtures and hooks live in `conftest.py`. Pytest discovers these automatically.

### Layout Pattern

```text
tests/
├── conftest.py          # Session and module-level fixtures
├── unit/
│   ├── conftest.py      # Unit-test specific fixtures
│   ├── test_models.py
│   └── test_utils.py
└── integration/
    ├── conftest.py      # Integration fixtures (DB, API)
    ├── test_api.py
    └── test_db.py
```

### What Goes in conftest.py

- Fixtures used by **multiple** test files
- Pytest plugins and hooks
- Shared test data factories

### What Stays in the Test File

- Fixtures used by **one** test file only
- Test-specific helpers and data

---

## Built-in Fixtures

Pytest provides several built-in fixtures. Use these instead of reinventing.

### `tmp_path` / `tmp_path_factory`

```python
def test_write_file(tmp_path):
    """tmp_path provides a unique temporary directory per test."""
    file = tmp_path / "output.txt"
    file.write_text("hello")
    assert file.read_text() == "hello"
    # Directory is cleaned up after the test session
```

### `capsys` — Capture stdout/stderr

```python
def test_print_output(capsys):
    print("hello world")
    captured = capsys.readouterr()
    assert captured.out == "hello world\n"
    assert captured.err == ""
```

### `monkeypatch` — Temporary Modifications

```python
def test_with_env_var(monkeypatch):
    monkeypatch.setenv("API_KEY", "test-key-123")
    monkeypatch.setattr("mymodule.CONFIG_PATH", "/tmp/test.toml")
    # Changes are reverted after the test
```

**monkeypatch vs unittest.mock.patch:** Use `monkeypatch` for simple attribute/env changes.
Use `patch` when you need to assert the mock was called with specific arguments.

### `caplog` — Capture Log Output

```python
def test_logging(caplog):
    with caplog.at_level(logging.WARNING):
        my_function()
    assert "expected warning" in caplog.text
```

### `request` — Test Metadata

```python
@pytest.fixture
def db_connection(request):
    conn = create_connection()
    request.addfinalizer(conn.close)  # Alternative to yield
    return conn
```

---

## Test Organization Patterns

### Function-based (flat)

```python
def test_create_user_happy_path():
    ...

def test_create_user_duplicate_email():
    ...
```

Best for: small test files, simple functions.

### Class-based (grouped)

```python
class TestCreateUser:
    def test_happy_path(self):
        ...

    def test_duplicate_email(self):
        ...

    def test_missing_required_field(self):
        ...
```

Best for: grouping tests for a single function or class under test. Allows class-scoped fixtures.

### Test Naming Convention

```python
# Pattern: test_{function}_{scenario}
def test_parse_config_valid_toml():
    ...

def test_parse_config_missing_file_raises():
    ...

def test_parse_config_empty_file_returns_defaults():
    ...
```

The name should describe the scenario, not repeat the function name verbatim.

---

## Assertion Patterns

### Value Assertions

```python
assert result == expected
assert result != unexpected
assert result is None
assert result is not None
assert item in collection
assert len(result) == 3
```

### Approximate Comparison (floats)

```python
assert result == pytest.approx(3.14, abs=1e-2)
assert result == pytest.approx(expected, rel=1e-3)
```

### Exception Assertions

```python
with pytest.raises(ValueError, match="invalid email"):
    validate_email("not-an-email")

# Capture exception for inspection
with pytest.raises(ValueError) as exc_info:
    validate_email("")
assert "required" in str(exc_info.value)
```

### Warning Assertions

```python
with pytest.warns(DeprecationWarning, match="use new_func"):
    old_func()
```
