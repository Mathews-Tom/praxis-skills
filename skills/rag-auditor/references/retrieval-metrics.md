# Retrieval Metrics

Definitions, formulas, and interpretation for RAG retrieval evaluation metrics.

---

## Precision@K

**What it measures:** Of the K retrieved documents, how many are relevant?

```
Precision@K = (Number of relevant documents in top K) / K
```

| Score | Interpretation |
|-------|----------------|
| 1.0 | All K documents are relevant |
| 0.5 | Half the documents are irrelevant (wasted context window) |
| 0.2 | Most documents are noise |

**Target:** >= 0.6 for most RAG applications.

---

## Recall@K

**What it measures:** Of all relevant documents in the corpus, how many were retrieved?

```
Recall@K = (Number of relevant documents in top K) / (Total relevant documents in corpus)
```

| Score | Interpretation |
|-------|----------------|
| 1.0 | All relevant information retrieved |
| 0.5 | Half the relevant information is missing |
| 0.2 | Most relevant information not retrieved |

**Target:** >= 0.8 for knowledge-intensive applications.

**Trade-off with Precision:** Increasing K improves Recall but may decrease Precision.
Find the K that balances both.

---

## Mean Reciprocal Rank (MRR)

**What it measures:** How high is the first relevant document ranked?

```
MRR = (1 / N) × Σ (1 / rank_i)
```

Where `rank_i` is the position of the first relevant document for query i.

| MRR | Interpretation |
|-----|----------------|
| 1.0 | First result is always relevant |
| 0.5 | First relevant result is typically at position 2 |
| 0.33 | First relevant result is typically at position 3 |

**Target:** >= 0.7 for user-facing applications.

---

## NDCG@K (Normalized Discounted Cumulative Gain)

**What it measures:** Are highly relevant documents ranked higher than marginally relevant ones?

Useful when relevance is graded (0-3) rather than binary (relevant/not).

```
DCG@K = Σ (relevance_i / log2(i + 1))
NDCG@K = DCG@K / IDCG@K
```

Where IDCG is the ideal (perfect ranking) DCG.

---

## Hit Rate (Hit@K)

**What it measures:** Does at least one relevant document appear in the top K?

```
Hit@K = 1 if any relevant document in top K, else 0
Average Hit@K = (queries with hit) / (total queries)
```

Simpler than MRR. Useful as a baseline metric.

**Target:** >= 0.9 for critical applications.

---

## Scoring Relevance

### Binary Relevance

Each document is either relevant (1) or not (0).

```
Relevant: Document contains information that helps answer the query
Not relevant: Document does not help answer the query
```

### Graded Relevance

| Score | Label | Definition |
|-------|-------|-----------|
| 3 | Highly relevant | Directly answers the query |
| 2 | Relevant | Contains supporting information |
| 1 | Marginally relevant | Tangentially related |
| 0 | Not relevant | No useful information for this query |

---

## Evaluation Protocol

1. For each test query, record:
   - The K retrieved chunks (in order)
   - The relevance score for each chunk
   - The expected relevant chunk(s)

2. Calculate per-query metrics:
   - Precision@K, Recall@K, MRR, Hit@K

3. Aggregate across all queries:
   - Mean and std dev for each metric

4. Report format:
   ```
   | Metric | Mean | Std Dev | Min | Target |
   |--------|------|---------|-----|--------|
   | Precision@5 | 0.72 | 0.15 | 0.40 | 0.60 |
   | Recall@10 | 0.85 | 0.12 | 0.50 | 0.80 |
   | MRR | 0.78 | 0.20 | 0.25 | 0.70 |
   | Hit@5 | 0.92 | - | - | 0.90 |
   ```
