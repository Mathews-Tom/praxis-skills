# Generation Metrics

Metrics for evaluating the generation stage of a RAG pipeline: groundedness,
completeness, hallucination detection, and abstention accuracy.

---

## Groundedness

**What it measures:** Is every claim in the generated response supported by the
retrieved context?

### Scoring

| Score | Meaning |
|-------|---------|
| 1.0 | Every claim is traceable to the retrieved context |
| 0.8 | Most claims grounded, minor unsupported details |
| 0.5 | Significant mixing of grounded and ungrounded claims |
| 0.2 | Mostly ungrounded — model relied on parametric knowledge |

### Evaluation Method

For each claim in the response:
1. Can it be directly found in the retrieved context? → Grounded
2. Can it be reasonably inferred from context? → Partially grounded
3. Is it not in the context at all? → Ungrounded (potential hallucination)

```
Groundedness = (grounded claims + 0.5 × partially grounded) / total claims
```

### LLM-as-Judge Template

```
Given the following context and response, evaluate whether each claim in the
response is supported by the context.

Context:
{retrieved chunks}

Response:
{generated response}

For each claim in the response, mark it as:
- SUPPORTED: Directly stated or clearly implied by the context
- PARTIAL: Loosely related to context but not directly stated
- UNSUPPORTED: Not found in the context

Output as JSON: {"claims": [{"text": "...", "status": "SUPPORTED/PARTIAL/UNSUPPORTED"}]}
```

---

## Completeness

**What it measures:** Does the response use all relevant information from the context?

### Scoring

| Score | Meaning |
|-------|---------|
| 1.0 | All relevant information from context is used |
| 0.7 | Most relevant information used, minor omissions |
| 0.5 | Significant relevant information missed |
| 0.2 | Response barely uses the provided context |

### Evaluation Method

1. Identify key facts in the retrieved context that are relevant to the query
2. Check which facts appear in the response
3. Score: facts_used / relevant_facts

---

## Hallucination Rate

**What it measures:** Fraction of claims in the response that are not supported
by any source.

```
Hallucination Rate = unsupported claims / total claims
```

### Types of Hallucination

| Type | Description | Example |
|------|-------------|---------|
| Factual fabrication | Inventing facts not in context | "The company was founded in 1998" (not in context) |
| Numerical fabrication | Inventing statistics | "95% of users prefer X" (no data in context) |
| Source fabrication | Citing non-existent sources | "According to Smith et al." (no such reference) |
| Extrapolation | Extending beyond context | Context says "revenue grew" → "revenue doubled" |

### Target Hallucination Rates

| Application | Target |
|-------------|--------|
| Medical/legal | < 1% |
| Financial | < 2% |
| Customer support | < 5% |
| General knowledge | < 10% |

---

## Abstention Accuracy

**What it measures:** When the answer is not in the context, does the model
correctly say "I don't know"?

### Evaluation

Test with queries whose answers are NOT in the corpus:

| Model Behavior | Correct? |
|---------------|----------|
| "I don't have information about X" | Yes (correct abstention) |
| Provides an answer from context | Yes (if answer was actually there — test design error) |
| Makes up an answer | No (false confidence — hallucination) |
| Refuses to answer when context IS sufficient | No (over-abstention) |

```
Abstention Accuracy = correct abstentions / (unanswerable queries)
Over-Abstention Rate = false abstentions / (answerable queries)
```

---

## End-to-End Quality

### Answer Correctness (for known-answer queries)

```
Correctness = correct answers / total queries
```

Combine with component metrics to diagnose WHERE failures occur:

| Retrieval | Generation | Diagnosis |
|-----------|-----------|-----------|
| Good chunks | Wrong answer | Generation failure |
| Bad chunks | Wrong answer | Retrieval failure (fix retrieval first) |
| Good chunks | Right answer | Working correctly |
| Bad chunks | Right answer | Lucky — model used parametric knowledge |

### F1 Token Overlap

For open-ended answers, measure token overlap with reference answer:

```python
def token_f1(prediction: str, reference: str) -> float:
    pred_tokens = set(prediction.lower().split())
    ref_tokens = set(reference.lower().split())

    common = pred_tokens & ref_tokens
    if not common:
        return 0.0

    precision = len(common) / len(pred_tokens)
    recall = len(common) / len(ref_tokens)
    return 2 * precision * recall / (precision + recall)
```
