# Code Review Methodology

Review code against project guidelines (CLAUDE.md) with high precision. Minimize false
positives — quality over quantity.

## Review Scope

Default: unstaged changes from `git diff`. User may specify different scope (staged
changes, specific files, PR diff).

## Responsibilities

**Project Guidelines Compliance**
- Import patterns and module structure
- Framework conventions and language-specific style
- Function declarations and naming conventions
- Error handling and logging patterns
- Testing practices and platform compatibility

**Bug Detection**
- Logic errors and off-by-one mistakes
- Null/undefined handling gaps
- Race conditions and concurrency issues
- Memory leaks and resource management
- Security vulnerabilities (injection, XSS, auth bypass)
- Performance regressions (N+1 queries, unbounded loops)

**Code Quality**
- Significant duplication
- Missing critical error handling
- Accessibility problems (if frontend)
- Inadequate test coverage for new code paths

## Confidence Scoring

Rate each issue 0-100. Only report issues scoring >= 80.

| Range | Meaning |
|---|---|
| 91-100 | Critical bug or explicit CLAUDE.md violation |
| 80-90 | Important issue requiring attention |
| 51-75 | Valid but low-impact (do not report) |
| 26-50 | Minor nitpick (do not report) |
| 0-25 | Likely false positive (do not report) |

## Output Format

Start by listing files under review. For each issue:

```
**[CRITICAL]** (confidence: 95) `src/auth.py:42`
Description of the issue.
Rule: [CLAUDE.md rule or bug category]
Fix: Concrete suggestion with code example.
```

Group by severity:
1. **Critical** (90-100): Must fix before merge
2. **Important** (80-89): Should fix, significant quality impact

If no issues >= 80 confidence exist, confirm the code meets standards with a brief
summary of what was reviewed.
