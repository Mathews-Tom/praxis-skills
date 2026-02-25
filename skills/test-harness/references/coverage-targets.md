# Coverage Targets

Test coverage thresholds, measurement strategies, and pytest-cov configuration.
Coverage is a hygiene metric, not a quality metric — 100% coverage does not guarantee
correct code, but low coverage guarantees untested code paths.

---

## Threshold Table

| Code Category | Minimum Coverage | Rationale |
|---------------|-----------------|-----------|
| Overall project | 80% | General baseline — catches major gaps |
| New or modified code | 90% | Higher bar for fresh code with no legacy excuse |
| Critical paths | 95% | Auth, payments, public API, security — failure is expensive |
| Generated code | Exempt | Protobuf, OpenAPI clients — test the generator instead |
| Configuration / constants | Exempt | No logic to cover |

These thresholds align with the project-level testing standards. Enforce them in CI
to prevent coverage regression.

---

## Branch vs Line Coverage

| Metric | What It Measures | Catches |
|--------|-----------------|---------|
| **Line coverage** | Which lines executed | Dead code, untouched functions |
| **Branch coverage** | Which branches taken (if/else, match arms) | Missing else handling, untested error paths |

**Branch coverage is the stronger metric.** A function can have 100% line coverage
but 50% branch coverage if only the `if` branch is tested and the `else` is never hit.

```python
def process(value):
    if value > 0:       # Branch 1: True
        return "positive"
    return "non-positive"  # Branch 2: False

# Line coverage: 100% with test_process(1) alone
# Branch coverage: 50% — the else branch is untested
```

Always measure branch coverage. Use line coverage as a secondary indicator.

---

## pytest-cov Configuration

### Installation

```bash
pip install pytest-cov
```

### pyproject.toml Configuration

```toml
[tool.pytest.ini_options]
addopts = "--cov=src --cov-branch --cov-report=term-missing --cov-fail-under=80"

[tool.coverage.run]
branch = true
source = ["src"]
omit = [
    "*/tests/*",
    "*/migrations/*",
    "*/__main__.py",
    "*/conftest.py",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "if TYPE_CHECKING:",
    "if __name__ == .__main__.:",
    "raise NotImplementedError",
    "pass",
    "\\.\\.\\.",
]
fail_under = 80
show_missing = true
skip_covered = false
```

### Running Coverage

```bash
# Basic coverage report
pytest --cov=src --cov-branch

# With HTML report
pytest --cov=src --cov-branch --cov-report=html

# Fail if below threshold
pytest --cov=src --cov-branch --cov-fail-under=80

# Coverage for specific module
pytest --cov=src/auth tests/test_auth.py
```

---

## Identifying Critical Paths

Not all code is equally important. Prioritize coverage for code where bugs
have the highest cost.

### Critical Path Indicators

| Indicator | Examples | Target |
|-----------|----------|--------|
| Handles money | Payment processing, billing, refunds | 95% |
| Handles authentication | Login, token validation, password reset | 95% |
| Public API surface | REST endpoints, GraphQL resolvers | 95% |
| Security boundaries | Input validation, authorization checks | 95% |
| Data integrity | Database writes, migrations, serialization | 90% |
| Error handling | Exception handlers, fallback logic | 90% |

### Finding Low-Coverage Critical Code

```bash
# Generate detailed report showing uncovered lines
pytest --cov=src --cov-branch --cov-report=term-missing

# HTML report for visual inspection
pytest --cov=src --cov-branch --cov-report=html
# Open htmlcov/index.html — red lines are uncovered
```

---

## Coverage Exclusion Patterns

Some code legitimately does not need test coverage. Use `# pragma: no cover` sparingly
and only for these categories:

### Acceptable Exclusions

```python
# Type checking imports — never executed at runtime
if TYPE_CHECKING:  # pragma: no cover
    from expensive_module import HeavyType

# Abstract methods — tested through concrete implementations
def process(self, data):  # pragma: no cover
    raise NotImplementedError

# Debug/development helpers
def __repr__(self):  # pragma: no cover
    return f"User(name={self.name!r})"

# Platform-specific code not testable in CI
if sys.platform == "win32":  # pragma: no cover
    ...
```

### Unacceptable Exclusions

Do NOT exclude:
- Error handling code — this is exactly what needs testing
- Complex conditional logic — branches are where bugs hide
- "Obvious" code — obvious code can still be wrong
- Code that is "too hard to test" — refactor for testability instead

---

## Coverage in CI

### GitHub Actions Example

```yaml
- name: Run tests with coverage
  run: |
    pytest --cov=src --cov-branch --cov-fail-under=80 --cov-report=xml

- name: Upload coverage report
  uses: codecov/codecov-action@v4
  with:
    file: coverage.xml
```

### Coverage Ratchet

Prevent coverage from decreasing over time:

1. Record current coverage percentage
2. Set `--cov-fail-under` to that value
3. After each PR that increases coverage, update the threshold
4. Coverage can only go up, never down

```toml
# Start at current level, ratchet up over time
[tool.coverage.report]
fail_under = 82.5  # Was 80, increased after auth module tests
```

---

## Common Pitfalls

### 1. Testing Coverage Instead of Behavior

```python
# BAD: Achieves coverage but tests nothing useful
def test_process():
    process(valid_input)  # No assertions — just runs the code
```

### 2. Mocking Away the Code Under Test

If a test mocks the function it's supposed to test, coverage shows the mock was called,
not the real function. This inflates coverage without testing anything.

### 3. Import-Time Coverage

Code executed at import time (module-level assignments, decorators, class body) is
counted as covered even without explicit tests. This can mask gaps.

### 4. Coverage ≠ Correctness

100% coverage means every line ran during tests. It does not mean:
- Every edge case was tested
- Assertions were meaningful
- Concurrent behavior was verified
- Performance was adequate

Coverage is necessary but not sufficient. Pair it with assertion quality, mutation
testing, and review.
