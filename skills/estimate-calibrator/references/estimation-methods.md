# Estimation Methods

PERT formula, three-point estimation, and aggregation techniques.

---

## Three-Point Estimation

### The Three Scenarios

| Scenario | Definition | Probability |
|----------|-----------|-------------|
| Optimistic (O) | Best realistic case — minimal friction | ~10th percentile |
| Most Likely (M) | Normal friction, typical obstacles | ~50th percentile |
| Pessimistic (P) | Significant problems, but not catastrophic | ~90th percentile |

### Key Rules

1. **O is not zero.** Even the simplest task takes some time.
2. **P is not infinity.** It's the realistic bad case, not the apocalypse.
3. **M is not the average of O and P.** It's the mode (most common outcome).
4. **All three must be estimated independently.** Don't calculate one from the others.

---

## PERT Formula

PERT (Program Evaluation and Review Technique) weights the most likely estimate:

```
Expected = (O + 4M + P) / 6
Standard Deviation = (P - O) / 6
Variance = ((P - O) / 6)²
```

### Example

```
Task: Implement user search
O = 2 days
M = 4 days
P = 10 days

Expected = (2 + 4×4 + 10) / 6 = 28 / 6 = 4.67 days
Std Dev = (10 - 2) / 6 = 1.33 days
```

### Confidence Intervals

| Confidence | Range |
|-----------|-------|
| 68% | Expected ± 1 std dev |
| 95% | Expected ± 2 std dev |
| 99.7% | Expected ± 3 std dev |

For the example:
- 68% confident: 3.3 to 6.0 days
- 95% confident: 2.0 to 7.3 days

---

## Aggregating Estimates

### Sum of Expected Values

For multiple tasks, the total expected duration:

```
Total Expected = Σ Expected_i
```

### Aggregate Uncertainty

Standard deviations do NOT sum linearly. Use root sum of squares:

```
Total Std Dev = √(Σ Variance_i) = √(Σ ((P_i - O_i) / 6)²)
```

### Example: 3-Task Project

| Task | O | M | P | Expected | Std Dev | Variance |
|------|---|---|---|----------|---------|----------|
| Task 1 | 1 | 2 | 5 | 2.3 | 0.67 | 0.44 |
| Task 2 | 2 | 4 | 10 | 4.7 | 1.33 | 1.78 |
| Task 3 | 1 | 3 | 7 | 3.3 | 1.00 | 1.00 |
| **Total** | | | | **10.3** | **1.80** | **3.22** |

Total Std Dev = √3.22 = 1.80 days

95% confident: 10.3 ± 3.6 = 6.7 to 13.9 days

---

## Simplified Three-Point (Quick Sizing)

When full PERT is overkill:

```
Quick Estimate = M + Buffer

Buffer:
  High confidence (done this before): +20%
  Medium confidence (some unknowns): +50%
  Low confidence (many unknowns): +100%
```

---

## Sequential vs Parallel Duration

### Sequential Tasks

```
Duration = Σ Expected_i
```

### Parallel Tasks

```
Duration = max(Expected_i)  for tasks running simultaneously
```

### Mixed (Critical Path)

```
Total = Σ (max of each parallel group on the critical path)
```

---

## Common Estimation Pitfalls

| Pitfall | Problem | Fix |
|---------|---------|-----|
| Single-point estimate | No uncertainty communicated | Always give ranges |
| Calendar time vs work time | 5 days of work ≠ 1 week (meetings, context switching) | Specify: "5 working days at 6 productive hours/day" |
| Forgetting testing time | Implementation estimate doesn't include tests | Add 20-40% for tests |
| Forgetting review time | Code review adds calendar time | Add 1-2 days per task for review cycle |
| Ignoring dependencies | Total = sum of individual estimates | Must account for blocking dependencies |
| Scope creep | Original estimate for original scope | Re-estimate when scope changes |
