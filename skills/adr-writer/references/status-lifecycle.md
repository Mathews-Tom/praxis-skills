# Status Lifecycle

Rules for ADR status transitions, supersession, and deprecation.

---

## Status State Machine

```text
Proposed → Accepted → Deprecated
                   → Superseded by ADR-XXX

Proposed → Rejected (rare — most rejected proposals are just not written)
```

### Transition Rules

| From     | To                    | Trigger                                          | Action                                         |
| -------- | --------------------- | ------------------------------------------------ | ---------------------------------------------- |
| Proposed | Accepted              | Team agrees                                      | Update status, set acceptance date             |
| Proposed | Rejected              | Team disagrees                                   | Add rejection reason, or simply delete the ADR |
| Accepted | Deprecated            | Better approach exists but no formal replacement | Add deprecation note                           |
| Accepted | Superseded by ADR-XXX | New ADR explicitly replaces this decision        | Update status, link to new ADR                 |

### Immutability Rule

**Once accepted, an ADR is never edited.** If the decision changes:

1. Write a NEW ADR
2. The new ADR's Context section explains why the original decision is being revisited
3. The new ADR references the original: "Supersedes ADR-003"
4. Update the original ADR's status: "Superseded by ADR-007"

This preserves the historical record. Editing old ADRs destroys context.

---

## Supersession

### When to Supersede

Supersede an ADR when:

- The original decision is being reversed
- The technology is being replaced
- The constraints that drove the original decision have fundamentally changed

### How to Supersede

**In the new ADR:**

```markdown
**Supersedes:** ADR-003

## Context

ADR-003 chose PostgreSQL for order management. Since then, our write volume has
grown to 50K TPS, exceeding PostgreSQL's capacity with our current architecture.
We need to revisit the database choice for the orders table.
```

**In the original ADR:**

```markdown
**Status:** Superseded by ADR-007
```

Only the status line is updated. The rest of the original ADR remains unchanged.

### Chain of Supersession

When an ADR supersedes another that itself superseded an earlier one:

```text
ADR-001: Use MySQL        ← Superseded by ADR-003
ADR-003: Use PostgreSQL   ← Superseded by ADR-007
ADR-007: Use CockroachDB  ← Current (Accepted)
```

Each ADR links only to its immediate predecessor and successor. Reading the chain
provides the full evolution of the decision.

---

## Deprecation

### When to Deprecate

Deprecate an ADR when:

- The decision is still technically valid but no longer recommended
- A better approach exists but no one has formally decided to switch
- The context has changed enough that the decision should be revisited

### How to Deprecate

```markdown
**Status:** Deprecated

> **Note (2026-02-25):** This decision predates our adoption of Kubernetes.
> While the decision is still technically correct, new services should follow
> ADR-012 instead. This ADR will be formally superseded when the remaining
> services are migrated.
```

---

## Review Cadence

ADRs should be reviewed periodically:

| Review Trigger             | Action                                       |
| -------------------------- | -------------------------------------------- |
| Annual architecture review | Check if accepted ADRs are still valid       |
| Major technology change    | Check which ADRs are affected                |
| New team member onboarding | Use ADRs as architecture documentation       |
| Post-incident review       | Check if any ADR's consequences materialized |

### Stale ADR Indicators

- Accepted ADR references technology no longer in use
- Context describes constraints that no longer apply
- No one on the team remembers why the decision was made (ADR exists but context is insufficient)
