# Test Coverage Analysis Methodology

Analyze behavioral test coverage — not line coverage. Focus on tests that prevent real
bugs, not academic completeness.

## Analysis Process

1. Examine the diff to identify new functionality and modifications
2. Map existing tests to changed code paths
3. Identify critical paths that could cause production issues if broken
4. Check for implementation-coupled tests that break on refactoring
5. Find missing negative cases and error scenarios
6. Evaluate integration points and their coverage

## Critical Gap Identification

Look for:

- Untested error handling paths that could cause silent failures
- Missing boundary condition tests (zero, one, max, overflow)
- Uncovered business logic branches
- Absent negative test cases for validation logic
- Missing async/concurrent behavior tests where relevant
- Integration points tested only in isolation

## Test Quality Evaluation

Tests should:

- Test behavior and contracts, not implementation details
- Catch meaningful regressions from future code changes
- Be resilient to reasonable refactoring
- Follow DAMP principles (Descriptive and Meaningful Phrases)
- Avoid mocking what they're testing

## Criticality Rating

| Rating | Criteria                                     | Example                   |
| ------ | -------------------------------------------- | ------------------------- |
| 9-10   | Data loss, security issues, system failures  | Auth bypass with no test  |
| 7-8    | User-facing errors in business logic         | Payment rounding untested |
| 5-6    | Edge cases causing confusion or minor issues | Empty input not tested    |
| 3-4    | Nice-to-have for completeness                | Redundant enum variant    |
| 1-2    | Optional minor improvements                  | Trivial getter            |

## Output Format

```text
## Test Coverage Analysis

### Summary
Brief overview of coverage quality.

### Critical Gaps (rating 8-10)
- [file:line] What's untested, what failure it would catch, criticality rating

### Important Improvements (rating 5-7)
- [file:line] What's weakly tested, suggested improvement, rating

### Test Quality Issues
- Tests coupled to implementation rather than behavior
- Brittle assertions that break on valid refactoring

### Positive Observations
- Well-tested areas that follow best practices
```

Do not suggest tests for trivial getters/setters unless they contain logic. Consider
whether existing integration tests already cover a scenario before flagging it.
