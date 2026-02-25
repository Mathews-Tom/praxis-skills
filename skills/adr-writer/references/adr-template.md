# ADR Template

Standard Architecture Decision Record template with field explanations and guidance
for each section.

---

## Complete Template

```markdown
# ADR-{NNN}: {Title — descriptive, starts with a noun or verb}

**Status:** {Proposed | Accepted | Deprecated | Superseded by ADR-XXX}
**Date:** {YYYY-MM-DD}
**Author:** {name or team}
**Supersedes:** {ADR-XXX, if this replaces a previous decision}

## Context

{Describe the situation that requires a decision.

- What problem are we solving?
- What constraints exist (technical, organizational, time, budget)?
- What forces are at play (scalability, team expertise, compliance)?

Write in present tense — capture the world AS IT IS when the decision is made.
This section is the most important: without context, a decision is just an assertion.

Length: 2-5 paragraphs. Enough to understand WHY, not a novel.}

## Decision

{State the decision clearly in 1-3 sentences.

"We will use PostgreSQL as the primary database for the order management service."

The reader should understand the decision without reading the rest of the document.
Use "We will..." phrasing.}

## Alternatives Considered

### {Alternative 1: Concrete Name}
- **Pros:** {Specific, measurable benefits}
- **Cons:** {Specific, measurable drawbacks}
- **Rejected because:** {Concrete reason tied to context — not "not suitable"}

### {Alternative 2: Concrete Name}
- **Pros:** {Specific, measurable benefits}
- **Cons:** {Specific, measurable drawbacks}
- **Rejected because:** {Concrete reason tied to context}

{Include at least 2 alternatives. If there was truly only one option, question
whether an ADR is needed — decisions without alternatives are constraints.}

## Consequences

### Positive
- {Concrete benefit that follows from this decision}
- {Another concrete benefit}

### Negative
- {Concrete tradeoff accepted — be honest}
- {Technical debt incurred, with plan to address if applicable}

### Neutral
- {Side effect that is neither positive nor negative}
- {Change in workflow or process}

## References

- {Link to issue, PR, discussion, or related ADR}
- {Link to external documentation or comparison}
```

---

## Field Guidance

### Title

| Good | Bad |
|------|-----|
| "Use PostgreSQL for Order Management" | "Database Decision" |
| "Adopt gRPC for Service Communication" | "ADR about APIs" |
| "Replace Celery with Temporal for Workflows" | "New Architecture" |

The title should be specific enough that you can understand the decision from it alone.

### Status Values

| Status | Meaning | When to Use |
|--------|---------|-------------|
| Proposed | Under discussion, not yet agreed | New ADR, pending team review |
| Accepted | Team has agreed, this is the active decision | After review and approval |
| Deprecated | Still valid but no longer the preferred approach | Newer alternatives exist |
| Superseded by ADR-XXX | Replaced by a newer decision | New ADR explicitly replaces this |

### Context Section Checklist

- [ ] States the problem clearly
- [ ] Lists relevant constraints
- [ ] Mentions the trigger (what prompted this decision now)
- [ ] Written in present tense
- [ ] Does NOT include the solution (that's the Decision section)

### Alternatives Section Checklist

- [ ] At least 2 alternatives listed
- [ ] Each has specific pros and cons (not generic)
- [ ] Rejection reason is tied to the context, not generic
- [ ] "Do nothing" is included as an alternative when applicable

### Consequences Section Checklist

- [ ] At least 1 negative consequence listed (if empty, analysis is incomplete)
- [ ] Consequences follow logically from the decision
- [ ] Technical debt is acknowledged, not hidden
- [ ] Timeline for addressing negative consequences (if applicable)

---

## Numbering Convention

### Sequential Numbering

```
docs/adr/
├── 001-use-postgresql.md
├── 002-adopt-grpc.md
├── 003-replace-celery-with-temporal.md
└── 004-use-s3-for-file-storage.md
```

### Padding

Use 3-digit padding (001-999) for projects expecting fewer than 1000 decisions.
Use 4-digit padding (0001-9999) for large organizations.

### Finding Next Number

```bash
# Find the highest existing ADR number
ls docs/adr/ | sort -n | tail -1
```
