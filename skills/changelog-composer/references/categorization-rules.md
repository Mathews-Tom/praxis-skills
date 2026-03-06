# Categorization Rules

Logic for classifying changes into changelog categories and ordering entries by
significance within each category.

---

## Classification Decision Tree

For each change (commit or PR), follow this sequence:

```text
1. Is it a breaking change?
   → Yes: Category = "Breaking Changes" (regardless of type)
   → No: continue

2. Does it add new user-facing capability?
   → Yes: Category = "Features"
   → No: continue

3. Does it fix a bug or incorrect behavior?
   → Yes: Category = "Fixes"
   → No: continue

4. Does it improve performance (speed, memory, cost)?
   → Yes: Category = "Performance"
   → No: continue

5. Does it modify documentation only?
   → Yes: Category = "Documentation"
   → No: continue

6. Does it modify security-relevant dependencies?
   → Yes: Category = "Security"
   → No: Category = "Internal" (excluded from user-facing changelog)
```

---

## Category Definitions

### Breaking Changes

Any change that requires users to modify their code, configuration, or workflow.

| Breaking Change Type | Example                   | Required in Entry       |
| -------------------- | ------------------------- | ----------------------- |
| API removal          | Function deleted          | Migration path          |
| Signature change     | Parameter renamed/removed | Before/after example    |
| Behavior change      | Default value changed     | What changed and why    |
| Configuration change | Config key renamed        | Old → new mapping       |
| Minimum version bump | Python 3.9 → 3.10         | New minimum requirement |
| Output format change | JSON schema changed       | Schema diff             |

### Features

New capabilities that didn't exist before.

| Feature Type             | Entry Style                                |
| ------------------------ | ------------------------------------------ |
| New function/method      | "Added `function_name` for {purpose}"      |
| New CLI command          | "New `command` to {what it does}"          |
| New configuration option | "Added `config.key` to control {behavior}" |
| New file format support  | "Support for {format} files"               |

### Fixes

Corrections to existing behavior.

| Fix Type       | Entry Style                                     |
| -------------- | ----------------------------------------------- |
| Crash fix      | "Fixed crash when {condition}"                  |
| Logic fix      | "Fixed {incorrect behavior} when {condition}"   |
| Regression fix | "Fixed regression in {version} where {symptom}" |
| Data fix       | "Fixed incorrect {data} in {context}"           |

### Performance

Measurable improvements to speed, memory, or resource usage.

| Performance Type    | Entry Style                                    |
| ------------------- | ---------------------------------------------- |
| Speed improvement   | "{Operation} is {X}x faster"                   |
| Memory reduction    | "Reduced memory usage by {X}% for {operation}" |
| Startup improvement | "Startup time reduced from {X}s to {Y}s"       |

---

## Ordering Within Categories

Within each category, order entries by impact:

1. **High impact** — Affects most users or core functionality
2. **Medium impact** — Affects specific use cases or features
3. **Low impact** — Affects edge cases or minor features

For breaking changes specifically, order by:

1. Most disruptive (API removal) first
2. Least disruptive (default value change) last

---

## Grouping by Component

For large releases (20+ changes), group within categories by component:

```markdown
### Features

#### Authentication

- Added OAuth2 support (#123)
- Added MFA via TOTP (#124)

#### API

- Added pagination to /users endpoint (#125)
- Added rate limiting headers (#126)
```

Use component grouping when there are 5+ entries in a single category.

---

## Ambiguous Cases

| Scenario                                      | Resolution                             |
| --------------------------------------------- | -------------------------------------- |
| Refactoring that changes public API           | Breaking change, not internal          |
| Bug fix that changes behavior users depend on | Breaking change with migration         |
| Dependency update with security fix           | Security category if CVE exists        |
| Performance fix that changes output precision | Breaking if output is part of contract |
| Documentation fix in code comments            | Internal (not user documentation)      |
| Test that reveals undocumented behavior       | Internal unless behavior is changed    |
