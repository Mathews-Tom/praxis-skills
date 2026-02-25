# Metric Selection

Catalog of benchmark metrics organized by category, with guidance on which metrics
to select for different comparison types.

---

## Latency Metrics

| Metric | What It Measures | When to Use |
|--------|-----------------|-------------|
| P50 (median) | Typical latency | Always — baseline user experience |
| P95 | Tail latency affecting 5% of requests | User-facing services |
| P99 | Worst-case latency for 1% | SLA-sensitive services |
| Mean | Average across all measurements | General comparison (but hides outliers) |
| Std deviation | Consistency of latency | When consistency matters more than raw speed |
| Min/Max | Absolute best/worst case | Identifying outliers, warmup effects |

### Latency Guidelines

- **Always report P50 + P95 at minimum.** Mean alone hides bimodal distributions.
- **Report P99 for user-facing systems.** 1% of 10M requests = 100K affected users.
- **Report std deviation when comparing similar candidates.** If P50 is close, the
  more consistent candidate may be preferable.

### Measurement Units

| Scale | Unit | Context |
|-------|------|---------|
| < 1ms | microseconds (μs) | In-memory operations, cache lookups |
| 1ms - 1000ms | milliseconds (ms) | API calls, database queries |
| > 1s | seconds (s) | Batch processing, file operations |

---

## Throughput Metrics

| Metric | What It Measures | When to Use |
|--------|-----------------|-------------|
| Operations/second (ops/s) | Discrete operation throughput | API endpoints, DB queries |
| Tokens/second (tok/s) | LLM generation speed | Language model comparison |
| MB/second | Data transfer rate | File processing, streaming |
| Requests/second (RPS) | HTTP request handling capacity | Web server comparison |
| Items/second | Processing pipeline throughput | ETL, data pipeline |

### Throughput Guidelines

- **Measure at saturation.** Throughput at 10% load tells nothing. Measure at the
  point where adding more load doesn't increase throughput.
- **Report with concurrency level.** "10K ops/s at 100 concurrent connections" is
  meaningful. "10K ops/s" alone is not.

---

## Memory Metrics

| Metric | What It Measures | When to Use |
|--------|-----------------|-------------|
| Peak RSS | Maximum resident memory | Resource-constrained environments |
| Average RSS | Typical memory usage | Long-running processes |
| Allocation rate | Memory allocations per second | GC pressure comparison |
| Peak heap | Maximum heap usage | JVM/managed runtime comparison |
| Memory growth rate | Memory increase over time | Leak detection |

### Memory Guidelines

- **Peak RSS is the most actionable metric.** It determines if the process fits in
  available memory.
- **Measure under realistic load.** Idle memory usage is irrelevant.

---

## Accuracy Metrics

| Metric | What It Measures | When to Use |
|--------|-----------------|-------------|
| F1 score | Harmonic mean of precision/recall | Classification tasks |
| Precision | Fraction of positives that are correct | When false positives are costly |
| Recall | Fraction of actual positives found | When false negatives are costly |
| Exact match | Binary correct/incorrect | QA tasks, code generation |
| BLEU | N-gram overlap with reference | Machine translation, text generation |
| ROUGE | Recall-oriented text overlap | Summarization |
| Accuracy | Fraction of correct predictions | Balanced classification |

---

## Cost Metrics

| Metric | What It Measures | When to Use |
|--------|-----------------|-------------|
| $/1K operations | Cost per unit of work | API service comparison |
| $/hour | Hourly infrastructure cost | Compute resource comparison |
| $/GB stored | Storage cost | Database, object storage comparison |
| $/GB transferred | Data transfer cost | CDN, API comparison |
| Total cost of ownership | All-in cost over time | Long-term infrastructure decisions |

---

## Metric Selection by Task Type

| Task Type | Primary Metrics | Secondary Metrics |
|-----------|----------------|-------------------|
| API endpoint comparison | Latency (P50, P95), RPS | Memory, cost |
| Database query | Latency (P50, P99), rows/sec | Memory, CPU |
| ML model inference | Latency, accuracy (F1 or task-specific) | Memory, cost |
| Data processing pipeline | Throughput (items/sec) | Memory, latency |
| File format comparison | Parse speed, serialize speed | File size, memory |
| Caching solution | Read latency, hit rate | Memory, write latency |
| Search engine | Latency (P50, P95), precision/recall | Index size, memory |

---

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Reporting only mean | Hides tail latency, bimodal distributions | Report P50 + P95 at minimum |
| Single measurement | No statistical confidence | Run N iterations, report mean ± std dev |
| Best-case input only | Misleading optimistic results | Test with representative + worst-case inputs |
| Ignoring warmup | First-run includes JIT, caching overhead | Discard first N iterations |
| Different hardware | Results not comparable | Run all candidates on same hardware |
| Throughput without concurrency | Unclear load conditions | State concurrency level with throughput |
