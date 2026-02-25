# Alternatives Analysis

Framework for evaluating and documenting rejected alternatives in ADRs.

---

## Analysis Framework

### Evaluation Criteria

Define criteria BEFORE evaluating alternatives. Common criteria:

| Criterion | What It Measures | Typical Weight |
|-----------|-----------------|---------------|
| Meets requirements | Does it solve the stated problem? | Must-have |
| Team expertise | Can the team build and maintain it? | High |
| Operational complexity | How hard is it to run in production? | High |
| Cost | Total cost of ownership (license, infra, people) | Medium-High |
| Community/support | Is there help when things break? | Medium |
| Migration effort | How hard is the transition? | Medium |
| Lock-in risk | How hard is it to switch away later? | Medium |
| Performance | Does it meet performance requirements? | Depends on context |
| Security | Does it meet security requirements? | Must-have |
| Maturity | Is it production-proven? | Medium |

### Scoring

For complex decisions with 3+ alternatives and 4+ criteria, use a decision matrix:

```markdown
| Criterion | Weight | Alternative A | Alternative B | Alternative C |
|-----------|--------|--------------|--------------|--------------|
| Performance | 30% | 4/5 | 5/5 | 3/5 |
| Team expertise | 25% | 5/5 | 2/5 | 4/5 |
| Operational cost | 20% | 3/5 | 4/5 | 4/5 |
| Migration effort | 15% | 5/5 | 2/5 | 3/5 |
| Lock-in risk | 10% | 4/5 | 3/5 | 5/5 |
| **Weighted Score** | | **4.15** | **3.35** | **3.65** |
```

For simpler decisions (2 alternatives, clear winner), a prose comparison is sufficient.

---

## Writing Rejection Reasons

### Good Rejection Reasons

Specific, tied to context, measurable:

```markdown
### Alternative: MongoDB
- **Pros:** Flexible schema, horizontal scaling, JSON-native
- **Cons:** No ACID transactions across collections, eventual consistency
- **Rejected because:** Our order processing requires ACID transactions across
  the orders and inventory tables. MongoDB's multi-document transactions (added
  in 4.0) have 2-3x latency overhead compared to PostgreSQL for our write pattern
  of 50K transactions/day.
```

### Bad Rejection Reasons

Vague, generic, not tied to context:

```markdown
### Alternative: MongoDB
- **Pros:** Good
- **Cons:** Bad
- **Rejected because:** Not suitable for our needs
```

### Rejection Reason Patterns

| Pattern | Example |
|---------|---------|
| Performance gap | "Benchmark showed 3x slower read latency at our expected scale" |
| Missing capability | "Does not support X, which is required for Y" |
| Expertise gap | "Team has no experience with X; learning curve estimated at 3 months" |
| Cost prohibitive | "License cost of $X/year exceeds budget by 2x" |
| Risk too high | "Only used in production by 3 companies; insufficient maturity for our SLA" |
| Migration effort | "Requires rewriting 50K lines of SQL; estimated 6 months of work" |

---

## The "Do Nothing" Alternative

Always consider "do nothing" as an alternative:

```markdown
### Alternative: Do Nothing (Status Quo)
- **Pros:** No migration effort, no new technology to learn, zero risk
- **Cons:** Current pain continues (500ms latency, timeout errors during peaks)
- **Rejected because:** Projected Black Friday volume will cause 30% of orders
  to fail. The cost of inaction ($X in lost revenue) exceeds migration cost.
```

If "do nothing" is not clearly worse than the proposed solution, the decision may
be premature.

---

## Number of Alternatives

| Scenario | Recommended Count |
|----------|------------------|
| Clear winner, one obvious alternative | 2 (chosen + alternative) |
| Several viable options | 3-4 (chosen + 2-3 alternatives) |
| Complex decision, many options | 3-5 (chosen + top alternatives). Don't list every option — only those seriously considered |

If there is truly only one option, question whether an ADR is needed. Decisions
without alternatives are constraints, not decisions — document them differently.

---

## Bias Awareness

### Common Biases in Alternative Evaluation

| Bias | Description | Mitigation |
|------|-------------|------------|
| Familiarity bias | Preferring what we already know | Evaluate expertise separately from capability |
| Anchoring | First option considered becomes the default | Evaluate all options independently first |
| Sunk cost | "We already invested in X" | Evaluate future cost only, not past investment |
| Hype bias | Choosing the newest/trendiest option | Require production evidence at comparable scale |
| Confirmation bias | Seeking evidence for preferred option | Assign someone to argue for each alternative |

### Debiasing Checklist

- [ ] Could a reasonable person choose differently given the same context?
- [ ] Are rejection reasons specific and verifiable, not vague feelings?
- [ ] Has someone argued the case for each rejected alternative?
- [ ] Would the decision change if the team had different expertise?
