# Fixture Design

Patterns for designing pytest fixtures that are reusable, composable, and properly
scoped. Covers factory fixtures, yield teardown, scope selection, autouse, and
conftest organization.

---

## Factory Fixture Pattern

When tests need similar but slightly different objects, use a factory fixture instead
of creating multiple fixtures with minor variations.

```python
@pytest.fixture
def make_user():
    """Factory that creates User instances with sensible defaults."""
    def _make_user(
        name: str = "Alice Smith",
        email: str = "alice@example.com",
        role: str = "member",
        active: bool = True,
    ) -> User:
        return User(name=name, email=email, role=role, active=active)
    return _make_user


def test_admin_permissions(make_user):
    admin = make_user(role="admin")
    assert admin.can_delete_users() is True


def test_inactive_user(make_user):
    inactive = make_user(active=False)
    assert inactive.can_login() is False
```

**When to use:** 3+ tests need objects with the same structure but different values.

---

## Yield Fixtures (Setup + Teardown)

`yield` fixtures provide both setup and cleanup in a single function.

```python
@pytest.fixture
def temp_database():
    """Create a test database and clean up after."""
    db = create_database("test_db")
    db.migrate()
    yield db
    db.drop_all_tables()
    db.close()
```

**Execution order:**

1. Everything before `yield` runs during setup
2. The yielded value is injected into the test
3. Everything after `yield` runs during teardown — even if the test fails

### Teardown Guarantees

Code after `yield` always runs, equivalent to a `finally` block. Use this for:

- Closing connections
- Deleting temp files
- Reverting configuration changes
- Stopping background processes

```python
@pytest.fixture
def mock_server():
    server = start_mock_server(port=8080)
    yield server
    server.shutdown()  # Guaranteed to run
```

---

## Scope Selection Criteria

| Scope      | Fixture Runs   | State Isolation     | Use When                                |
| ---------- | -------------- | ------------------- | --------------------------------------- |
| `function` | Every test     | Full isolation      | Default. Stateful objects, mutable data |
| `class`    | Once per class | Shared within class | Read-only resources, expensive parse    |
| `module`   | Once per file  | Shared within file  | Config loading, file parsing            |
| `session`  | Once per run   | Shared globally     | Docker start, external service init     |

### Decision Flow

1. **Does the fixture modify state?** → `function` scope (prevent cross-test contamination)
2. **Is setup expensive (>100ms)?** → Consider wider scope
3. **Are tests read-only against the fixture?** → Wider scope is safe
4. **Can tests run in parallel?** → `function` scope or ensure thread safety

### Scope Mismatch Error

A lower-scoped fixture cannot depend on a higher-scoped fixture. This fails:

```python
@pytest.fixture(scope="session")
def db_pool():
    return create_pool()

@pytest.fixture  # function scope (default)
def db_connection(db_pool):
    return db_pool.acquire()  # OK: function can use session
```

This fails:

```python
@pytest.fixture(scope="session")
def expensive_thing(function_scoped_fixture):  # ERROR: session cannot use function
    ...
```

---

## Autouse Fixtures

`autouse=True` fixtures apply to every test in their scope without explicit request.

```python
@pytest.fixture(autouse=True)
def reset_global_state():
    """Reset global cache before every test."""
    global_cache.clear()
    yield
    global_cache.clear()
```

### When to Use Autouse

- Resetting global state (singletons, caches, module-level variables)
- Setting environment variables for all tests
- Recording test timing or logging

### When NOT to Use Autouse

- When only some tests need the fixture — use explicit fixture names instead
- When the fixture has expensive setup — autouse runs for every test
- When the fixture produces a value tests need to reference — explicit is clearer

---

## Fixture Composition

Fixtures can depend on other fixtures, building complex setups from simple parts.

```python
@pytest.fixture
def db_connection():
    conn = create_connection()
    yield conn
    conn.close()


@pytest.fixture
def user_repo(db_connection):
    """Depends on db_connection — runs after it, tears down before it."""
    return UserRepository(db_connection)


@pytest.fixture
def populated_repo(user_repo, make_user):
    """Depends on both user_repo and make_user factory."""
    user_repo.add(make_user(name="Alice"))
    user_repo.add(make_user(name="Bob"))
    return user_repo
```

**Teardown order:** Fixtures tear down in reverse dependency order. `populated_repo`
tears down first, then `user_repo`, then `db_connection`.

---

## conftest.py Organization

### Single conftest.py (Small Projects)

```text
tests/
├── conftest.py       # All shared fixtures
├── test_api.py
├── test_models.py
└── test_utils.py
```

### Hierarchical conftest.py (Large Projects)

```text
tests/
├── conftest.py              # Session fixtures: DB pool, test config
├── unit/
│   ├── conftest.py          # Unit fixtures: mocks, factories
│   ├── test_validators.py
│   └── test_parsers.py
└── integration/
    ├── conftest.py          # Integration fixtures: real DB, API stubs
    ├── test_endpoints.py
    └── test_workflows.py
```

### conftest.py Rules

1. **No test functions in conftest.py** — only fixtures and hooks
2. **No imports of conftest.py** — pytest discovers it automatically
3. **Inner conftest overrides outer** — a fixture in `tests/unit/conftest.py` shadows
   the same name in `tests/conftest.py`
4. **Keep it focused** — if a conftest grows past 200 lines, split into helper modules
   and import into conftest

---

## Request Object

The `request` fixture provides metadata about the test requesting the fixture.

```python
@pytest.fixture
def db_connection(request):
    conn = create_connection()
    def cleanup():
        conn.rollback()
        conn.close()
    request.addfinalizer(cleanup)  # Alternative to yield
    return conn
```

### Accessing Test Info

```python
@pytest.fixture
def log_test_name(request):
    print(f"Starting: {request.node.name}")
    yield
    print(f"Finished: {request.node.name}")
```

### Parameterized Fixtures

```python
@pytest.fixture(params=["json", "yaml", "toml"])
def config_format(request):
    """Run the test once for each config format."""
    return request.param


def test_parse_config(config_format):
    # Runs 3 times: once for json, yaml, toml
    config = parse_config(f"test.{config_format}")
    assert config is not None
```
