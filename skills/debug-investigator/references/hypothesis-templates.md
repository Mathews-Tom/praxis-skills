# Hypothesis Templates

Common bug categories organized by symptom type. Use these as starting points when
generating hypotheses during debugging — adapt to the specific evidence.

---

## Bug Category Catalog

### 1. State Bugs

The system is in an unexpected state.

| Hypothesis Template | Symptoms | Confirming Test |
|---------------------|----------|-----------------|
| Variable was not initialized | `None`/`undefined` where value expected | Log variable at assignment point |
| Variable was overwritten | Correct value early, wrong value later | Log at each mutation point |
| Stale cache | Correct after restart, wrong during operation | Clear cache and retry |
| Race condition on shared state | Intermittent failures, order-dependent | Add locks or serialize access, observe if fixed |
| Global state modified by another test | Test passes alone, fails in suite | Run test in isolation: `pytest test.py::test_name -x` |
| Object reference shared when copy intended | Modifying A changes B | Check if `a is b` returns `True` |

### 2. Logic Bugs

The code does the wrong thing deterministically.

| Hypothesis Template | Symptoms | Confirming Test |
|---------------------|----------|-----------------|
| Off-by-one error | Boundary values wrong, middle values correct | Test with boundary inputs (0, 1, N-1, N, N+1) |
| Wrong comparison operator | `<` instead of `<=`, `==` instead of `is` | Test with the exact boundary value |
| Inverted condition | if/else branches swapped | Test with known-true and known-false inputs |
| Short-circuit evaluation skip | Second condition never evaluated | Add logging to both sides of `and`/`or` |
| Integer division truncation | Math results slightly wrong | Check for `/` vs `//` in Python 3, or `int()` casting |
| Incorrect regex | Pattern matches wrong strings | Test with positive AND negative examples |
| String encoding mismatch | Mojibake, length mismatches | Check `type()` and `encoding` of strings |

### 3. Integration Bugs

The interface between components is wrong.

| Hypothesis Template | Symptoms | Confirming Test |
|---------------------|----------|-----------------|
| API contract changed | Worked before, fails after update | Compare current API response with expected schema |
| Argument order swapped | Function called with correct values, wrong behavior | Check call site against function signature |
| Serialization/deserialization mismatch | Data corrupted across boundary | Log raw data on both sides of the boundary |
| HTTP status code not checked | Silent failure on 4xx/5xx | Log response status before parsing body |
| Timeout too short | Intermittent failures under load | Increase timeout and observe |
| Missing Content-Type header | Server rejects or misparses request | Log full request headers |
| Environment variable not set | Works locally, fails in CI/production | `echo $VAR` in the failing environment |

### 4. Concurrency Bugs

Timing-dependent failures that may not reproduce reliably.

| Hypothesis Template | Symptoms | Confirming Test |
|---------------------|----------|-----------------|
| Race condition | Intermittent, changes with timing | Add artificial delays to expose the race |
| Deadlock | System hangs, no error | Thread dump: `kill -QUIT <pid>` or debugger |
| Resource exhaustion | Gradually degrading performance | Monitor open file descriptors, connections, memory |
| Lost update | Concurrent writes overwrite each other | Check for read-modify-write without locks |
| Callback ordering assumption | Works sequentially, fails concurrently | Log callback invocation order |

### 5. Environment Bugs

The code is correct but the environment is wrong.

| Hypothesis Template | Symptoms | Confirming Test |
|---------------------|----------|-----------------|
| Wrong Python/Node version | Syntax error on valid code, missing stdlib | `python --version` / `node --version` |
| Missing dependency | `ImportError` / `ModuleNotFoundError` | `pip list` / `npm list` |
| Wrong dependency version | Changed behavior, no code change | `pip freeze | grep package` vs requirements |
| Different config in environments | Works locally, fails elsewhere | Diff config files / env vars |
| File path separator (OS) | Works on Linux, fails on Windows | Check for hardcoded `/` vs `os.path.join` |
| Permissions | `PermissionError` | `ls -la` on the file/directory |
| Docker volume mount | File exists locally, not in container | Check docker-compose volumes |

### 6. Data Bugs

The code is correct but the input data is unexpected.

| Hypothesis Template | Symptoms | Confirming Test |
|---------------------|----------|-----------------|
| Missing required field | `KeyError`, `AttributeError` | Validate input schema before processing |
| Unexpected data type | `TypeError` | Log `type(value)` at entry point |
| Unicode/encoding issues | Mojibake, `UnicodeDecodeError` | Check file encoding, add explicit `encoding=` |
| Null/empty where non-empty expected | `NoneType has no attribute` | Add null check, log where value originates |
| Data truncation | Values cut off at boundary | Check field/column lengths |
| Timezone mismatch | Times off by hours | Log timezone-aware vs naive datetime |

---

## Probability Ranking Guide

### Prior Probabilities (Before Evidence)

Rank hypotheses using these base rates — bugs are overwhelmingly mundane:

| Rank | Category | Base Rate | Reasoning |
|------|----------|-----------|-----------|
| 1 | Recent code change | ~40% | Most bugs are in the newest code |
| 2 | Data/input issue | ~20% | Unexpected inputs are the second most common cause |
| 3 | Configuration/environment | ~15% | "Works on my machine" is a real category |
| 4 | Logic error | ~10% | Inverted conditions, off-by-ones |
| 5 | Integration mismatch | ~8% | API contracts, serialization |
| 6 | Concurrency | ~4% | Race conditions, deadlocks |
| 7 | Framework/library bug | ~2% | Almost never the framework's fault |
| 8 | Hardware/OS issue | ~1% | Cosmic rays, kernel bugs — last resort |

### Updating Probabilities

After each investigation step, update rankings:

- **Evidence strongly supports H1:** Increase H1 to >80%, decrease others proportionally
- **Evidence contradicts H1:** Drop H1 to <10%, promote H2 to top
- **Evidence is ambiguous:** Keep rankings, design a more discriminating test
- **New evidence suggests a new category:** Add H_new, ranked by evidence fit

### When to Abandon a Hypothesis

Drop a hypothesis when:
1. A direct test contradicts it (you proved it wrong)
2. The fix for that hypothesis doesn't resolve the symptom
3. Three separate pieces of evidence are inconsistent with it

---

## Hypothesis Documentation Template

Use this format for each hypothesis in an investigation:

```markdown
### H{N}: {Specific claim about what is wrong}

**Likelihood:** {High | Medium | Low}
**Evidence for:**
- {Observation that supports this hypothesis}

**Evidence against:**
- {Observation that contradicts this hypothesis} (or "None yet")

**Confirming test:**
- {Specific action that would prove this hypothesis}

**Refuting test:**
- {Specific action that would disprove this hypothesis}

**Status:** {Untested | Confirmed | Refuted | Inconclusive}
```
