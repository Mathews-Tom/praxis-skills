# Statistical Rigor

Sample sizing, variance measurement, significance testing, and outlier handling
for benchmark results.

---

## Why Statistics Matter in Benchmarks

A single measurement tells nothing. Performance varies due to:
- CPU scheduling, context switches
- Cache state (hot vs cold)
- Background processes
- GC pauses
- Thermal throttling

Without statistical analysis, you cannot distinguish real differences from noise.

---

## Sample Size

### Minimum Samples

| Confidence Level | Minimum Samples |
|-----------------|-----------------|
| Basic comparison | 30 |
| Percentile reporting (P95) | 100 |
| Percentile reporting (P99) | 1,000 |
| Publication-quality | 1,000+ |

### Rule of Thumb

For percentile P_k, collect at least `100 / (100 - k)` × 10 samples:
- P50 → 20 samples minimum
- P95 → 200 samples minimum
- P99 → 1,000 samples minimum

---

## Variance Measurement

### Standard Deviation

```python
import statistics

times = [measure() for _ in range(100)]
mean = statistics.mean(times)
stdev = statistics.stdev(times)
print(f"{mean:.2f} ± {stdev:.2f} ms")
```

### Coefficient of Variation (CV)

```
CV = stdev / mean × 100%
```

| CV | Interpretation |
|----|----------------|
| < 5% | Low variance — results are stable |
| 5-15% | Moderate variance — acceptable for most comparisons |
| 15-30% | High variance — increase iterations or improve isolation |
| > 30% | Very high variance — results are unreliable, fix the measurement setup |

### Inter-Quartile Range (IQR)

More robust than standard deviation for skewed distributions:

```python
import numpy as np

times = [measure() for _ in range(100)]
q25, q50, q75 = np.percentile(times, [25, 50, 75])
iqr = q75 - q25
print(f"Median: {q50:.2f} ms, IQR: {iqr:.2f} ms")
```

---

## Significance Testing

### When Two Candidates Are "Close"

If Candidate A has mean 50ms and B has mean 52ms, is A really faster? It depends
on variance.

### Mann-Whitney U Test

Non-parametric test — does not assume normal distribution (benchmark times are
often skewed). Tests whether one distribution tends to have larger values.

```python
from scipy import stats

times_a = [measure_a() for _ in range(100)]
times_b = [measure_b() for _ in range(100)]

statistic, p_value = stats.mannwhitneyu(times_a, times_b, alternative='two-sided')

if p_value < 0.05:
    print(f"Significant difference (p={p_value:.4f})")
else:
    print(f"No significant difference (p={p_value:.4f})")
```

### Effect Size

Statistical significance alone is insufficient. A 0.1ms difference might be
statistically significant with enough samples but practically irrelevant.

Report effect size alongside significance:

```python
# Relative difference
effect = (mean_b - mean_a) / mean_a * 100
print(f"B is {effect:.1f}% {'slower' if effect > 0 else 'faster'} than A")
```

| Effect Size | Interpretation |
|-------------|----------------|
| < 1% | Negligible — practically identical |
| 1-5% | Small — may matter at scale |
| 5-20% | Medium — meaningful difference |
| > 20% | Large — clear winner |

---

## Outlier Handling

### Detection

```python
import numpy as np

times = np.array([measure() for _ in range(100)])
q25, q75 = np.percentile(times, [25, 75])
iqr = q75 - q25
lower_bound = q25 - 1.5 * iqr
upper_bound = q75 + 1.5 * iqr

outliers = times[(times < lower_bound) | (times > upper_bound)]
print(f"Found {len(outliers)} outliers out of {len(times)} measurements")
```

### What to Do with Outliers

| Approach | When to Use |
|----------|-------------|
| Keep all data | Default — outliers represent real-world behavior |
| Report with and without | When outliers significantly affect mean |
| Remove and document | Only if outliers have a known, irrelevant cause (e.g., GC pause during unrelated operation) |
| Use robust statistics | Report median + IQR instead of mean + stdev |

**Never silently remove outliers.** Always report what was removed and why.

---

## Reporting Format

### Compact Table Format

```markdown
| Candidate | P50 | P95 | P99 | Mean ± StdDev | N |
|-----------|-----|-----|-----|---------------|---|
| A | 12ms | 18ms | 25ms | 13.2 ± 3.1ms | 1000 |
| B | 15ms | 22ms | 35ms | 16.8 ± 5.2ms | 1000 |
| Difference | -20% | -18% | -29% | p < 0.001 | |
```

### Interpretation Template

```markdown
**Candidate A is {X}% faster than B** (P50: 12ms vs 15ms, p < 0.001, N=1000).
The difference is statistically significant and practically meaningful (>5% effect
size). A also shows lower variance (CV=23% vs 31%), indicating more consistent
performance.
```

### What to Include

- [ ] Sample size (N)
- [ ] Central tendency (median or mean)
- [ ] Spread (stdev, IQR, or CV)
- [ ] Percentiles (P50, P95, P99 as appropriate)
- [ ] Statistical significance (p-value)
- [ ] Effect size (relative difference)
- [ ] Outlier count and handling
