# Context Capture

Techniques for eliciting and documenting the context around an architectural decision.
The Context section is the most valuable part of an ADR — without it, a decision is
just an assertion.

---

## Elicitation Questions

### Problem Space

| Question | What It Reveals |
|----------|----------------|
| What problem are we solving? | Core motivation |
| Who is affected by this problem? | Stakeholders |
| How are we handling this today? | Current state, existing workarounds |
| What happens if we do nothing? | Urgency, cost of inaction |
| What triggered this decision now? | Immediate catalyst |

### Constraint Space

| Question | What It Reveals |
|----------|----------------|
| What is the budget/timeline? | Resource constraints |
| What technology must we keep? | Integration constraints |
| What skills does the team have? | Expertise constraints |
| What compliance requirements apply? | Regulatory constraints |
| What does our SLA require? | Performance constraints |
| What can we NOT change? | Hard boundaries |

### Force Space

| Question | What It Reveals |
|----------|----------------|
| What are the performance requirements? | Non-functional requirements |
| How will this scale? | Growth expectations |
| How many people will maintain this? | Team size, bus factor |
| What is the expected lifetime? | Longevity expectations |
| What other systems interact with this? | Integration surface |

---

## Writing Effective Context

### Structure Pattern

```
1. SITUATION: What exists today (1-2 sentences)
2. PROBLEM: What's wrong or missing (1-2 sentences)
3. CONSTRAINTS: What limits our options (bullet list)
4. TRIGGER: Why we're deciding now (1 sentence)
```

### Example: Good Context

```markdown
## Context

Our order management service uses a PostgreSQL database for all reads and writes.
Daily order volume has grown from 5K to 50K over the past year, and peak write
latency now exceeds 500ms during flash sales, causing timeout errors for users.

The current architecture uses a single primary with two read replicas. Vertical
scaling is maxed at the largest available RDS instance (db.r6g.16xlarge).

Constraints:
- Cannot change the order service's API contract (50+ downstream consumers)
- Budget allows for 2x current infrastructure cost, not 10x
- Team has PostgreSQL expertise but limited NoSQL experience
- SOC2 compliance requires encryption at rest and audit logging

This decision is triggered by the upcoming Black Friday sale, which is projected
to hit 100K orders/day based on marketing campaign reach.
```

### Example: Bad Context

```markdown
## Context

We need a new database.
```

This is insufficient. It doesn't explain why, what constraints exist, or what
triggered the decision.

---

## Context Reconstruction

When documenting a decision that was already made without an ADR:

### Sources of Context

| Source | What to Extract |
|--------|----------------|
| Git history | When the change was made, who made it, PR description |
| Slack/chat archives | Discussion threads around the decision |
| Issue tracker | Related issues, feature requests |
| Meeting notes | Decision meetings, architecture reviews |
| Code comments | Inline rationale ("we use X because Y") |
| Team interviews | Ask the people who were there |

### Reconstruction Template

```markdown
## Context

> **Note:** This ADR was written after the fact to document a decision made
> approximately {date}. Context has been reconstructed from {sources}.

{Best available reconstruction of the context at decision time.}
```

Always mark reconstructed context explicitly. It may be incomplete or slightly
inaccurate — future readers should know this.

---

## Common Context Pitfalls

| Pitfall | Problem | Fix |
|---------|---------|-----|
| Solution in context | Context describes the solution, not the problem | Rewrite to describe the situation without mentioning the chosen technology |
| Missing constraints | Context doesn't explain why alternatives were rejected | Add constraint list |
| Too brief | "We need better performance" — not actionable | Quantify: "Write latency exceeds 500ms at 50K ops/day" |
| Too verbose | Multi-page context with tangential details | Cut to 2-5 focused paragraphs |
| Past tense | "We were having problems with..." | Write in present tense — capture the world at decision time |
| Missing trigger | Why now? What changed? | Add the immediate catalyst |
