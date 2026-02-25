# Diagnostic Queries

Designing evaluation query sets for RAG pipeline assessment.

---

## Query Types

### Factoid (Known-Answer)

Single-fact questions with unambiguous answers directly in the corpus.

```
Query: "What is the maximum file upload size?"
Expected: "100MB" (from docs/configuration.md)
Source chunk: "The maximum file upload size is 100MB by default..."
```

**Purpose:** Baseline retrieval and generation accuracy.
**Minimum count:** 10 queries.

### Multi-Hop

Questions requiring information from multiple chunks to answer.

```
Query: "Can admin users upload files larger than the default limit?"
Expected: "Yes, admin users can set custom limits up to 1GB"
Source chunks:
  - "Admin users have elevated permissions..." (users.md)
  - "Custom upload limits can be set per role, up to 1GB" (configuration.md)
```

**Purpose:** Tests chunk retrieval breadth and generation reasoning.
**Minimum count:** 5 queries.

### Unanswerable

Questions whose answers are NOT in the corpus.

```
Query: "What is the pricing for the enterprise tier?"
Expected: "This information is not available in the documentation."
Source: No relevant chunk exists
```

**Purpose:** Tests abstention capability and hallucination tendency.
**Minimum count:** 3 queries.

### Ambiguous

Questions with multiple valid interpretations.

```
Query: "How do I reset?"
Could mean: Reset password, reset configuration, factory reset
```

**Purpose:** Tests retrieval robustness and generation disambiguation.
**Minimum count:** 3 queries.

### Temporal / Updated

Questions about information that may have changed.

```
Query: "What version of Python is required?"
Expected: "3.12+" (updated from "3.10+" in older docs)
```

**Purpose:** Tests freshness and correct version retrieval.
**Minimum count:** 2 queries.

---

## Query Design Guidelines

### Good Queries

| Characteristic | Example |
|---------------|---------|
| Specific | "What HTTP status code does /api/users return for invalid email?" |
| Verifiable | Answer can be checked against source |
| Realistic | Represents actual user questions |
| Varied vocabulary | Uses different words than the source document |

### Bad Queries

| Characteristic | Example | Problem |
|---------------|---------|---------|
| Too broad | "Tell me about the system" | No clear expected answer |
| Uses exact source text | "What is the maximum file upload size of 100MB?" | Tests keyword matching, not understanding |
| Subjective | "Is the API well-designed?" | No objective answer |
| Multiple questions | "What are the limits and how do I change them?" | Unclear evaluation criteria |

---

## Query Generation from Corpus

### Method 1: Fact Extraction

1. Read a document section
2. Identify key facts (numbers, names, procedures, rules)
3. Formulate a question for each fact
4. Rephrase using different vocabulary

```
Source: "Rate limiting is set to 100 requests per minute per API key."
Query: "How many API calls can I make per minute?"
Expected: "100 requests per minute per API key"
```

### Method 2: Scenario-Based

1. Imagine a user scenario
2. Formulate the question they would ask
3. Locate the answer in the corpus

```
Scenario: User wants to deploy to production
Query: "What are the prerequisites for production deployment?"
Expected: (from deployment guide)
```

### Method 3: Cross-Document

1. Find information split across documents
2. Design a question requiring both pieces

```
Doc A: "OAuth tokens expire after 1 hour"
Doc B: "Use refresh tokens to get new access tokens"
Query: "What happens when my OAuth token expires?"
Expected: "It expires after 1 hour; use a refresh token to get a new one"
```

---

## Evaluation Dataset Template

```markdown
| # | Query | Type | Expected Answer | Source Chunks | Difficulty |
|---|-------|------|-----------------|---------------|------------|
| 1 | {query} | Factoid | {answer} | {doc:section} | Easy |
| 2 | {query} | Factoid | {answer} | {doc:section} | Easy |
| 3 | {query} | Multi-hop | {answer} | {doc1, doc2} | Medium |
| 4 | {query} | Ambiguous | {answer(s)} | {docs} | Hard |
| 5 | {query} | Unanswerable | "Not in docs" | None | Medium |
```

---

## Difficulty Calibration

| Difficulty | Characteristics |
|-----------|----------------|
| Easy | Single chunk, exact phrasing match, common topic |
| Medium | Single chunk but vocabulary differs, or multi-chunk with obvious connection |
| Hard | Multi-hop, ambiguous, requires inference, rare topic, or paraphrased heavily |

Aim for distribution: 40% Easy, 40% Medium, 20% Hard.
