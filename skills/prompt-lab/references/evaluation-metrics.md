# Evaluation Metrics

Metrics for measuring prompt quality, rubric design, and scoring methodology.

---

## Core Metrics

### Correctness

Does the output contain the right answer/information?

| Score | Meaning                         |
| ----- | ------------------------------- |
| 0     | Completely wrong or irrelevant  |
| 1     | Partially correct, major errors |
| 2     | Mostly correct, minor errors    |
| 3     | Fully correct                   |

### Format Compliance

Does the output follow the specified format?

| Score | Meaning                              |
| ----- | ------------------------------------ |
| 0     | Wrong format entirely                |
| 1     | Right format, significant deviations |
| 2     | Right format, minor deviations       |
| 3     | Perfect format compliance            |

### Completeness

Does the output include all required elements?

| Score | Meaning                         |
| ----- | ------------------------------- |
| 0     | Missing most required elements  |
| 1     | Includes some required elements |
| 2     | Includes most required elements |
| 3     | All required elements present   |

### Conciseness

Is the output free of unnecessary content?

| Score | Meaning                            |
| ----- | ---------------------------------- |
| 0     | Extremely verbose, mostly filler   |
| 1     | Significant unnecessary content    |
| 2     | Slightly verbose                   |
| 3     | Concise, every sentence adds value |

### Groundedness

Are all claims supported by provided context? (For RAG/grounded tasks)

| Score | Meaning                                         |
| ----- | ----------------------------------------------- |
| 0     | Mostly hallucinated                             |
| 1     | Mix of grounded and hallucinated claims         |
| 2     | Almost fully grounded, minor unsupported claims |
| 3     | Every claim traceable to context                |

---

## Rubric Design

### Weighting by Task Type

| Task Type      | Correctness | Format | Completeness | Conciseness |
| -------------- | ----------- | ------ | ------------ | ----------- |
| Classification | 50%         | 20%    | 10%          | 20%         |
| Extraction     | 40%         | 25%    | 25%          | 10%         |
| Analysis       | 35%         | 15%    | 30%          | 20%         |
| Summarization  | 30%         | 15%    | 25%          | 30%         |
| Generation     | 30%         | 20%    | 25%          | 25%         |

### Custom Criteria

Add task-specific criteria when core metrics are insufficient:

| Custom Criterion | When to Use                                |
| ---------------- | ------------------------------------------ |
| Tone/voice       | Brand-specific or audience-specific output |
| Specificity      | Answers should be concrete, not generic    |
| Actionability    | Recommendations should be actionable       |
| Safety           | Output must not contain harmful content    |
| Creativity       | Output should be novel or engaging         |

---

## Scoring Methodology

### Per-Query Scoring

For each test query × variant:

1. Score each criterion (0-3)
2. Apply weights
3. Calculate weighted sum
4. Normalize to 0-100%

```text
Score = Σ(criterion_score × weight) / (3 × Σ weights) × 100
```

### Aggregate Scoring

For each variant across all test queries:

- **Mean score** — Overall quality
- **Min score** — Worst-case performance (important for reliability)
- **Std deviation** — Consistency
- **Pass rate** — % of queries scoring above threshold

### Comparison

| Metric                | Variant A | Variant B | Winner |
| --------------------- | --------- | --------- | ------ |
| Mean score            | 85%       | 78%       | A      |
| Min score             | 60%       | 45%       | A      |
| Consistency (std dev) | 8%        | 15%       | A      |
| Pass rate (>70%)      | 95%       | 80%       | A      |

---

## Automated Evaluation

### LLM-as-Judge

Use a separate LLM call to evaluate outputs:

```text
You are an evaluation judge. Score the following output on a 0-3 scale for each criterion.

Criteria:
- Correctness: Does the output contain the right answer?
- Format: Does it follow the specified format?
- Completeness: Are all required elements present?

Expected output: {expected}
Actual output: {actual}

Provide scores as JSON:
{"correctness": N, "format": N, "completeness": N, "reasoning": "..."}
```

**Limitations:** LLM judges have their own biases. Use as a signal, not ground truth.
Human evaluation is more reliable for subjective criteria.

### Exact Match

For tasks with unambiguous correct answers:

```python
score = 1.0 if output.strip() == expected.strip() else 0.0
```

### Partial Match (Recall)

For extraction tasks:

```python
expected_items = set(expected)
output_items = set(output)
recall = len(expected_items & output_items) / len(expected_items)
```
