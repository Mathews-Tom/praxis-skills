# Async Testing

Patterns for testing asynchronous Python code with pytest. Covers pytest-asyncio
configuration, event loop management, coroutine mocking, and async fixture design.

---

## pytest-asyncio Configuration

### Installation

```bash
pip install pytest-asyncio
```

### Mode Selection

Configure in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
asyncio_mode = "auto"  # or "strict"
```

| Mode     | Behavior                                                                  | When to Use                                         |
| -------- | ------------------------------------------------------------------------- | --------------------------------------------------- |
| `auto`   | All `async def test_*` functions are treated as async tests automatically | Most projects — reduces boilerplate                 |
| `strict` | Only tests decorated with `@pytest.mark.asyncio` are async                | Mixed sync/async codebases needing explicit control |

In `strict` mode, every async test needs the marker:

```python
@pytest.mark.asyncio
async def test_fetch_data():
    result = await fetch_data("https://api.example.com")
    assert result["status"] == "ok"
```

In `auto` mode, the marker is optional.

---

## Basic Async Tests

```python
import pytest

async def test_async_function():
    """Auto mode: no marker needed."""
    result = await my_async_function("input")
    assert result == "expected"


@pytest.mark.asyncio
async def test_async_explicit():
    """Strict mode: marker required."""
    result = await my_async_function("input")
    assert result == "expected"
```

---

## Async Fixtures

```python
@pytest.fixture
async def async_client():
    """Async fixture with setup and teardown."""
    client = await create_client()
    yield client
    await client.close()


@pytest.fixture(scope="module")
async def shared_connection():
    """Module-scoped async fixture."""
    conn = await connect_to_database()
    yield conn
    await conn.disconnect()
```

### Fixture Scope with Async

Session and module-scoped async fixtures require `pytest-asyncio >= 0.23`. Earlier
versions only support function-scoped async fixtures.

```python
# Requires pytest-asyncio >= 0.23
@pytest.fixture(scope="session")
async def db_pool():
    pool = await create_pool()
    yield pool
    await pool.close()
```

---

## Mocking Coroutines

### AsyncMock (Python 3.8+)

```python
from unittest.mock import AsyncMock, patch

async def test_async_dependency():
    mock_fetch = AsyncMock(return_value={"key": "value"})
    with patch("mymodule.fetch_data", mock_fetch):
        result = await process_data()
    assert result == "processed: value"
    mock_fetch.assert_awaited_once()
```

### AsyncMock Assertions

```python
mock.assert_awaited()              # Was awaited at least once
mock.assert_awaited_once()         # Exactly once
mock.assert_awaited_with("arg")    # With specific arguments
mock.assert_awaited_once_with("arg")
mock.assert_not_awaited()          # Never awaited
assert mock.await_count == 3       # Specific count
```

### Side Effects for Async Mocks

```python
# Sequence of return values
mock_api = AsyncMock(side_effect=[
    {"page": 1, "data": [1, 2, 3]},
    {"page": 2, "data": [4, 5, 6]},
    {"page": 3, "data": []},
])

# Exception on specific call
mock_api = AsyncMock(side_effect=ConnectionError("timeout"))

# Conditional return
async def conditional_return(url):
    if "users" in url:
        return {"users": []}
    return {"error": "not found"}

mock_api = AsyncMock(side_effect=conditional_return)
```

---

## Async Context Managers

### Testing Code That Uses `async with`

```python
from unittest.mock import AsyncMock, MagicMock

async def test_async_context_manager():
    mock_session = MagicMock()
    mock_session.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = AsyncMock(return_value=False)

    with patch("mymodule.create_session", return_value=mock_session):
        result = await my_function()
    assert result == "expected"
```

### Testing Async Iterators

```python
async def test_async_iterator():
    async def mock_stream():
        for item in [1, 2, 3]:
            yield item

    with patch("mymodule.data_stream", mock_stream):
        result = await collect_stream()
    assert result == [1, 2, 3]
```

---

## Event Loop Management

### Default Behavior

pytest-asyncio creates a new event loop per test function by default. This ensures
test isolation but can be slow for setup-heavy tests.

### Shared Event Loop (Module Scope)

```python
@pytest.fixture(scope="module")
def event_loop():
    """Override the default event loop for module-scoped async fixtures."""
    import asyncio
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()
```

### Common Pitfall: Loop Already Running

```text
RuntimeError: This event loop is already running
```

This occurs when calling `asyncio.run()` inside an already-running loop (common in
Jupyter notebooks or nested async). In tests, use `await` directly — pytest-asyncio
manages the loop.

---

## anyio Multi-Backend Testing

For code that should work with both asyncio and trio:

```bash
pip install anyio pytest-anyio
```

```python
import pytest

@pytest.mark.anyio
async def test_with_anyio():
    """Runs on both asyncio and trio backends."""
    result = await my_function()
    assert result == "expected"
```

Configure backends in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
anyio_backends = ["asyncio", "trio"]
```

---

## Timeout Handling

Async tests can hang indefinitely. Add timeouts:

```python
@pytest.mark.asyncio
@pytest.mark.timeout(5)  # pytest-timeout
async def test_with_timeout():
    result = await potentially_slow_operation()
    assert result is not None
```

Or configure globally:

```toml
[tool.pytest.ini_options]
timeout = 30
```

---

## Common Async Test Patterns

### Testing Concurrent Operations

```python
import asyncio

async def test_concurrent_tasks():
    results = await asyncio.gather(
        fetch_user(1),
        fetch_user(2),
        fetch_user(3),
    )
    assert len(results) == 3
    assert all(r["status"] == "ok" for r in results)
```

### Testing Task Cancellation

```python
async def test_cancellation_handling():
    task = asyncio.create_task(long_running_operation())
    await asyncio.sleep(0.1)
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task
```

### Testing Retry Logic

```python
async def test_retry_on_failure():
    mock_api = AsyncMock(side_effect=[
        ConnectionError("attempt 1"),
        ConnectionError("attempt 2"),
        {"status": "ok"},  # Third attempt succeeds
    ])
    with patch("mymodule.api_call", mock_api):
        result = await fetch_with_retry(max_retries=3)
    assert result == {"status": "ok"}
    assert mock_api.await_count == 3
```
