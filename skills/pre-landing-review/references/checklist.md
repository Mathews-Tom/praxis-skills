# Pre-Landing Review Checklist

## Pass 1 — CRITICAL (blocking)

### SQL & Data Safety
- [ ] No raw SQL without parameterized queries
- [ ] Schema migrations use lock timeouts and are reversible
- [ ] Bulk updates/deletes have verified WHERE clauses
- [ ] Column updates go through model validations, not direct DB writes
- [ ] No N+1 queries introduced in hot paths
- [ ] Indexes exist for new query patterns

### Race Conditions & Concurrency
- [ ] No read-then-write without optimistic locking or database locks
- [ ] Unique constraints enforced at database level, not just application
- [ ] Shared mutable state properly synchronized
- [ ] Background jobs are idempotent (safe to retry)
- [ ] No TOCTOU (time-of-check-to-time-of-use) vulnerabilities

### Trust Boundaries
- [ ] LLM/AI output sanitized before use in SQL, shell, or HTML
- [ ] User input validated before reaching privileged operations
- [ ] External API responses validated against expected schema
- [ ] No deserialization of untrusted data without schema validation
- [ ] Authentication/authorization checks on all new endpoints
- [ ] Secrets not hardcoded or logged

## Pass 2 — INFORMATIONAL (non-blocking)

### Conditional Side Effects
- [ ] Side effects not hidden in conditional branches
- [ ] State-change callbacks documented and intentional
- [ ] Error handlers don't silently swallow failures

### Magic Numbers
- [ ] Numeric literals extracted to named constants
- [ ] Thresholds and limits documented with rationale
- [ ] Timeout values appropriate and configurable

### Dead Code
- [ ] No unreachable branches
- [ ] No unused imports or variables
- [ ] No commented-out code without explanation

### Test Gaps
- [ ] New code paths have test coverage
- [ ] Modified behavior has updated tests
- [ ] Edge cases and error paths tested
- [ ] Integration points have contract tests

### Crypto & Entropy
- [ ] Cryptographically secure random for security contexts
- [ ] No hardcoded secrets or API keys
- [ ] TLS/encryption for sensitive data in transit

### Time Window Safety
- [ ] Timezone-aware datetime comparisons
- [ ] Daylight saving transitions handled
- [ ] Cron expressions account for clock skew

### Type Coercion
- [ ] No implicit type conversions that lose data
- [ ] Numeric precision maintained across boundaries
- [ ] String encoding explicit at I/O boundaries

## Gate Classification

| Category | Severity | Blocking? |
|----------|----------|-----------|
| SQL & Data Safety | CRITICAL | Yes |
| Race Conditions | CRITICAL | Yes |
| Trust Boundaries | CRITICAL | Yes |
| All Pass 2 categories | INFORMATIONAL | No |

## Suppressions

Do NOT flag:
- Test files using test fixtures or factories
- Migration files following framework conventions
- Code with inline comments explaining why a flagged pattern is intentional
- Configuration files with documented values
- Type stubs or interface definitions
