# Calibration Tips

Cognitive biases in estimation, historical calibration, and buffer strategies.

---

## Cognitive Biases

### Planning Fallacy

**What:** People systematically underestimate how long tasks will take, even when
they know they've underestimated in the past.

**Magnitude:** 25-50% underestimation is typical.

**Counteraction:**

- Reference class forecasting: "How long did similar tasks take last time?"
- Multiply your gut estimate by 1.5x
- Ask: "If I had to bet money on finishing by this date, would I?"

### Anchoring

**What:** The first number heard becomes the reference point, even if irrelevant.

**Counteraction:**

- Estimate independently before hearing others' estimates
- Use bottom-up estimation (sum of parts) instead of top-down
- Avoid leading with a number: "How long do you think?" not "Would 3 days be enough?"

### Optimism Bias

**What:** "It'll be straightforward" — imagining the happy path only.

**Counteraction:**

- Pre-mortem: "Imagine it took twice as long. What went wrong?"
- List specific things that could go wrong for each task
- Review past estimates: were you usually optimistic?

### Dunning-Kruger Effect

**What:** Low familiarity leads to confidence ("How hard can it be?").

**Counteraction:**

- For unfamiliar technology, assume L or XL until proven otherwise
- Spike before estimating
- Add "unfamiliarity tax" to estimate

### Sunk Cost Fallacy

**What:** "We've already spent 3 days, it must be almost done."

**Counteraction:**

- Re-estimate remaining work from scratch, ignoring time already spent
- Ask: "If we were starting today, how long would the remaining work take?"

---

## Historical Calibration

### Track Actuals

For every estimate, record:

1. Original estimate (best/likely/worst)
2. Actual time taken
3. What was different from expectations

### Calibration Ratio

```text
Calibration Ratio = Actual / Estimated (Likely)

If ratio > 1.0: You underestimate (most people)
If ratio < 1.0: You overestimate
If ratio = 1.0: You're calibrated (rare)
```

### Apply Your Ratio

If your historical calibration ratio is 1.4:

```text
Adjusted Estimate = Raw Estimate × 1.4
```

### Team Calibration

Track the ratio per team member. Some people are consistent 2x underestimators;
others are well-calibrated. Use individual ratios for accuracy.

---

## Buffer Strategies

### Fixed Buffer

Add a flat percentage based on confidence:

| Confidence | Buffer | Use When                                            |
| ---------- | ------ | --------------------------------------------------- |
| High       | +20%   | Familiar task, clear requirements, done it before   |
| Medium     | +50%   | Some unknowns, new elements, moderate familiarity   |
| Low        | +100%  | Many unknowns, new technology, unclear requirements |

### Per-Task Buffer

Add buffer at the task level based on individual uncertainty, then aggregate.
This is more accurate than a flat project-level buffer.

### Risk-Based Buffer

Add buffer for specific identified risks:

```text
Risk buffer = Σ (probability × impact) for each risk

Example:
- External API delay: 30% chance × 3 days = 0.9 days
- Unclear requirements: 50% chance × 2 days = 1.0 day
- Total risk buffer: 1.9 days
```

---

## Communication Strategies

### For Stakeholders

| Bad                 | Good                                                                                                     |
| ------------------- | -------------------------------------------------------------------------------------------------------- |
| "It'll take 5 days" | "Likely 5 days, could range from 3 to 10 depending on X"                                                 |
| "I'm not sure"      | "3-10 days. The range is wide because we haven't validated X yet. A 2-day spike would narrow it to 4-6." |
| "Done by Friday"    | "80% confident it's done by Friday. 95% by next Wednesday."                                              |

### When Asked for a Single Number

If forced to give one number:

- Use PERT expected + buffer matching confidence level
- State the confidence explicitly: "5 days, assuming X and Y. If those don't hold, up to 10."

### When the Estimate Is "Too High"

Do NOT reduce the estimate to match expectations. Instead:

1. Identify which tasks could be descoped
2. Identify which unknowns could be spiked first
3. Offer a smaller scope with a smaller estimate
4. "We can do X by Friday or X+Y+Z by next Wednesday"
