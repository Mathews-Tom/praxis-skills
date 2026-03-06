# Type Design Analysis Methodology

Evaluate type designs for invariant strength, encapsulation quality, and practical
usefulness. Well-designed types are the foundation of maintainable, bug-resistant systems.

## Analysis Framework

### 1. Identify Invariants

Examine the type for all implicit and explicit invariants:

- Data consistency requirements (field A implies field B)
- Valid state transitions (status can only go DRAFT → PUBLISHED → ARCHIVED)
- Relationship constraints between fields (end_date > start_date)
- Business logic rules encoded in the type
- Preconditions and postconditions on methods

### 2. Rate Encapsulation (1-10)

- Are internal implementation details hidden?
- Can invariants be violated from outside the type?
- Are access modifiers appropriate?
- Is the interface minimal and complete?

### 3. Rate Invariant Expression (1-10)

- How clearly are invariants communicated through the type's structure?
- Are constraints enforced at compile-time where possible?
- Is the type self-documenting through its design?
- Are edge cases obvious from the type definition?

### 4. Rate Invariant Usefulness (1-10)

- Do the invariants prevent real bugs?
- Are they aligned with business requirements?
- Do they make the code easier to reason about?
- Are they neither too restrictive nor too permissive?

### 5. Rate Invariant Enforcement (1-10)

- Are invariants checked at construction time?
- Are all mutation points guarded?
- Is it impossible to create invalid instances?
- Are runtime checks appropriate and comprehensive?

## Anti-Patterns to Flag

- **Anemic domain models** — types with no behavior, just data bags
- **Exposed mutable internals** — returning references to internal collections
- **Documentation-only invariants** — constraints described in comments but not enforced
- **Too many responsibilities** — type doing multiple unrelated things
- **Missing construction validation** — no checks in constructor/factory
- **Inconsistent enforcement** — some mutation methods check, others don't
- **External invariant maintenance** — relying on callers to maintain type's constraints

## Key Principles

- Prefer compile-time guarantees over runtime checks when feasible
- Make illegal states unrepresentable
- Constructor validation is crucial for maintaining invariants
- Immutability simplifies invariant maintenance
- Value clarity over cleverness
- Consider the maintenance burden of suggestions

## Output Format

```text
## Type: UserAccount

### Invariants Identified
- Email must be non-empty and valid format
- Role must be one of ADMIN, MEMBER, VIEWER
- Created date is immutable after construction

### Ratings
- **Encapsulation**: 7/10 — Role field is publicly settable, bypassing validation
- **Invariant Expression**: 8/10 — Role enum makes valid values clear
- **Invariant Usefulness**: 9/10 — Prevents invalid role assignment bugs
- **Invariant Enforcement**: 5/10 — No validation on role setter

### Strengths
- Email validated at construction via factory method

### Concerns
- Role can be set to any value after construction

### Recommended Improvements
- Make role setter private, add changeRole() method with validation
```
