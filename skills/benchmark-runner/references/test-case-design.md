# Test Case Design

Designing representative benchmark inputs that reveal meaningful performance
characteristics across candidates.

---

## Input Scale Matrix

Every benchmark should test at multiple scales. Performance characteristics often
change non-linearly with input size.

### Standard Scale Tiers

| Tier   | Purpose              | Typical Size   | Reveals                               |
| ------ | -------------------- | -------------- | ------------------------------------- |
| Tiny   | Overhead measurement | 1-10 items     | Startup cost, minimum latency         |
| Small  | Typical light load   | 100-1K items   | Normal operation performance          |
| Medium | Typical heavy load   | 10K-100K items | Scaling behavior                      |
| Large  | Stress test          | 1M+ items      | Algorithmic complexity, memory limits |

### Choosing Scales

1. **Anchor to production data.** If production handles 50K items, test at 5K, 50K, and 500K.
2. **Cross the threshold.** If a candidate claims "fast up to 100K items," test at
   50K, 100K, and 200K.
3. **Find the crossover.** Two candidates often trade positions at a certain scale.
   Finding that crossover point is valuable.

---

## Input Type Coverage

### Representative Data

Use inputs that resemble production workloads:

| If Testing       | Use                                     | Not                     |
| ---------------- | --------------------------------------- | ----------------------- |
| Text processing  | Real documents, varied lengths          | Single repeated word    |
| JSON parsing     | Real API responses, nested objects      | Flat `{"key": "value"}` |
| Database queries | Realistic table sizes and distributions | Empty tables            |
| ML inference     | Real-world samples from test set        | Random noise            |
| Image processing | Varied sizes, formats, content          | Single test image       |

### Worst-Case Inputs

Include inputs designed to expose weaknesses:

| Category     | Example                                             |
| ------------ | --------------------------------------------------- |
| Pathological | Sorted input for quicksort, all-hash-collision keys |
| Adversarial  | Deeply nested JSON, regex backtracking patterns     |
| Empty        | Zero-length input, null, missing fields             |
| Maximum      | Largest possible input, max integer, longest string |
| Unicode      | Multi-byte characters, emoji, RTL text              |

---

## Warmup Strategy

### Why Warmup Matters

First-run measurements include:

- JIT compilation (JVM, V8)
- Cache population (CPU cache, application cache)
- Connection establishment (database, HTTP)
- Module loading (Python imports, dynamic libraries)

These are one-time costs that don't reflect steady-state performance.

### Warmup Protocol

```python
# Standard warmup pattern
WARMUP_ITERATIONS = 10
MEASUREMENT_ITERATIONS = 100

# Warmup — discard results
for _ in range(WARMUP_ITERATIONS):
    run_benchmark(input_data)

# Measurement — record results
results = []
for _ in range(MEASUREMENT_ITERATIONS):
    start = time.perf_counter()
    run_benchmark(input_data)
    elapsed = time.perf_counter() - start
    results.append(elapsed)
```

### How Many Warmup Iterations

| Environment            | Recommended Warmup                 |
| ---------------------- | ---------------------------------- |
| Python (CPython)       | 3-5 iterations                     |
| JVM (Java, Kotlin)     | 50-100 iterations (JIT)            |
| JavaScript (V8)        | 10-20 iterations                   |
| Compiled (Rust, Go, C) | 1-3 iterations (cache only)        |
| Database queries       | 5-10 iterations (query plan cache) |

---

## Iteration Count

### Minimum Iterations

```text
Minimum = 30 (for basic statistical confidence)
Recommended = 100+ (for percentile accuracy)
For P99 accuracy = 1000+ (need 10x the percentile denominator)
```

### When to Increase Iterations

- High variance in results → increase iterations
- P99 measurement needed → at least 1000 iterations
- Candidates are close in performance → more iterations for discrimination

---

## Isolation Strategies

### Process Isolation

Run each candidate in a separate process to prevent:

- Shared memory pollution
- GC interference
- Thread contention

```bash
# Run candidates in separate processes
python benchmark_candidate_a.py > results_a.json
python benchmark_candidate_b.py > results_b.json
```

### Interleaved Execution

Alternate between candidates to control for system-level drift:

```python
# BAD: Run all of A, then all of B
# System temperature, background processes may differ

# GOOD: Interleave
for i in range(iterations):
    time_a = measure(candidate_a, input_data)
    time_b = measure(candidate_b, input_data)
    results_a.append(time_a)
    results_b.append(time_b)
```

### System Isolation

For rigorous benchmarks:

- Close unnecessary applications
- Disable CPU frequency scaling: `sudo cpupower frequency-set --governor performance`
- Pin processes to specific CPU cores: `taskset -c 0 python benchmark.py`
- Disable turbo boost for consistent results
