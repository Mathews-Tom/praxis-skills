# Failure Taxonomy

Categories of RAG pipeline failures with diagnostic indicators and root causes.

---

## Failure Classification

### Level 1: Retrieval Failures

The retriever fails to find the relevant information.

| Failure             | Indicator                               | Root Cause                          | Fix                                                |
| ------------------- | --------------------------------------- | ----------------------------------- | -------------------------------------------------- |
| Total miss          | Relevant chunk not in top-K at all      | Embedding mismatch, vocabulary gap  | Try different embedding model, add query expansion |
| Rank failure        | Relevant chunk retrieved but ranked low | Similarity score not discriminating | Add reranking stage, increase K                    |
| Partial miss        | Part of answer retrieved, part missing  | Chunk boundary split the answer     | Increase overlap, try semantic chunking            |
| Duplicate retrieval | Same info retrieved multiple times      | Overlapping chunks, dedup needed    | Deduplicate by content similarity                  |

### Level 2: Chunking Failures

The chunking strategy corrupts the information.

| Failure      | Indicator                             | Root Cause                            | Fix                                        |
| ------------ | ------------------------------------- | ------------------------------------- | ------------------------------------------ |
| Split entity | Named entity split across chunks      | Fixed-size chunking ignores semantics | Use semantic chunking, sentence boundaries |
| Lost context | Chunk lacks necessary context         | No overlap, no metadata               | Add overlap, prepend section headers       |
| Too large    | Chunk contains irrelevant information | Chunk size too big                    | Reduce chunk size                          |
| Too small    | Chunk lacks sufficient context        | Chunk size too small                  | Increase chunk size                        |

### Level 3: Embedding Failures

The embedding model fails to capture the right semantics.

| Failure            | Indicator                           | Root Cause                  | Fix                                 |
| ------------------ | ----------------------------------- | --------------------------- | ----------------------------------- |
| Vocabulary gap     | Domain terms not embedded well      | Model not trained on domain | Use domain-specific embedding model |
| Synonym miss       | Query uses different words than doc | Lexical mismatch            | Add hybrid search (BM25 + semantic) |
| Negation blindness | "Not X" retrieves docs about X      | Embeddings poor at negation | Add keyword filter, reranking       |

### Level 4: Generation Failures

The generator produces incorrect output despite correct retrieval.

| Failure           | Indicator                               | Root Cause                           | Fix                                                |
| ----------------- | --------------------------------------- | ------------------------------------ | -------------------------------------------------- |
| Hallucination     | Claims not in context                   | Model relies on parametric knowledge | Strengthen grounding instruction                   |
| Incomplete answer | Misses relevant context                 | Model doesn't process all chunks     | Reduce context length, highlight relevant sections |
| Wrong emphasis    | Focuses on irrelevant detail            | No guidance on what matters          | Add focus instruction: "Focus on X"                |
| Refusal           | Won't answer despite sufficient context | Over-cautious prompt                 | Soften abstention criteria                         |
| Contradiction     | Answer contradicts context              | Conflicting information in chunks    | Add conflict resolution instruction                |

---

## Diagnostic Flowchart

```text
Query → Correct Answer?
  ├── Yes → Pipeline working (for this query)
  └── No → Was relevant info retrieved?
        ├── No → RETRIEVAL FAILURE
        │    └── Was it in the corpus at all?
        │         ├── No → CORPUS GAP (need more documents)
        │         └── Yes → Was the chunk well-formed?
        │              ├── No → CHUNKING FAILURE
        │              └── Yes → EMBEDDING/RANKING FAILURE
        └── Yes → GENERATION FAILURE
             └── Was the answer hallucinated?
                  ├── Yes → HALLUCINATION
                  └── No → Was it incomplete?
                       ├── Yes → CONTEXT UTILIZATION FAILURE
                       └── No → REASONING FAILURE
```

---

## Failure Distribution (Typical RAG Pipelines)

Based on common patterns across RAG audits:

| Failure Category    | Typical Prevalence | Priority   |
| ------------------- | ------------------ | ---------- |
| Retrieval failures  | 40-60% of errors   | Fix first  |
| Chunking issues     | 15-25%             | Fix second |
| Generation failures | 15-25%             | Fix third  |
| Corpus gaps         | 10-20%             | Ongoing    |

**Key insight:** Most RAG failures are retrieval failures, not generation failures.
Improving retrieval has the highest ROI.

---

## Per-Query Failure Report Template

```markdown
### Query #{N}: "{query text}"

**Expected answer:** {correct answer}
**Generated answer:** {model output}
**Verdict:** {Correct | Incorrect}

**Retrieval analysis:**

- Chunk 1 (score: 0.85): {chunk summary} — Relevant: {Yes/Partial/No}
- Chunk 2 (score: 0.72): {chunk summary} — Relevant: {Yes/Partial/No}
- Chunk 3 (score: 0.65): {chunk summary} — Relevant: {Yes/Partial/No}

**Failure classification:** {Retrieval | Chunking | Generation | Hallucination}
**Root cause:** {specific diagnosis}
**Recommendation:** {specific fix for this failure type}
```
