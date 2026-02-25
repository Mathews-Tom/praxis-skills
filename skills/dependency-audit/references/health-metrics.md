# Health Metrics

Maintenance health indicators, scoring criteria, and abandonment detection for
dependency risk assessment.

---

## Health Indicator Definitions

### Release Cadence

How frequently the package publishes new versions.

| Signal | Healthy | Warning | Abandoned |
|--------|---------|---------|-----------|
| Last release | < 6 months ago | 6-18 months ago | > 18 months ago |
| Release frequency | Regular (monthly/quarterly) | Sporadic | None in 18+ months |
| Pre-release versions | Stable releases available | Only pre-releases | N/A |

**Nuance:** Some packages are "done" — stable, feature-complete, and intentionally not
updated. Evaluate whether the domain requires ongoing updates:
- Crypto libraries: must update (new vulnerabilities) → stale = risky
- String utilities: rarely need updates → stale = acceptable
- Web frameworks: must track ecosystem → stale = risky

### Commit Activity

Recent development activity in the source repository.

| Signal | Healthy | Warning | Abandoned |
|--------|---------|---------|-----------|
| Commits (90 days) | 10+ | 1-9 | 0 |
| Commits (1 year) | 50+ | 10-49 | < 10 |
| Unique contributors (1 year) | 5+ | 2-4 | 0-1 |
| Branch activity | Active feature/fix branches | Only main | No activity |

### Issue Responsiveness

How maintainers handle bug reports and feature requests.

| Signal | Healthy | Warning | Abandoned |
|--------|---------|---------|-----------|
| Median response time | < 2 weeks | 2-8 weeks | > 8 weeks or no response |
| Open/closed ratio | More closed than open | Balanced | Growing backlog |
| Stale issues (no activity 90d) | < 20% | 20-50% | > 50% |
| Maintainer engagement | Active in discussions | Occasional | Absent |

### Bus Factor

Number of people who could maintain the project if others left.

| Signal | Healthy | Warning | Critical |
|--------|---------|---------|----------|
| Maintainers with merge access | 3+ | 2 | 1 |
| Active contributors (90d) | 5+ | 2-4 | 1 |
| Organization backing | Yes (company/foundation) | Community only | Solo developer |
| Documentation of internals | Good | Partial | None |

### CI/CD Health

Automated testing and build status.

| Signal | Healthy | Warning | Abandoned |
|--------|---------|---------|-----------|
| CI status | Passing | Flaky (intermittent failures) | Failing or absent |
| Test coverage | Reported and stable | Reported but declining | Not reported |
| CI configuration | Current (up-to-date actions/images) | Slightly outdated | Uses deprecated tools |

### Downstream Adoption

Community usage and trust signals.

| Signal | Healthy | Warning | Risky |
|--------|---------|---------|-------|
| Weekly downloads | Growing or stable | Declining | Minimal |
| Dependent packages | Many | Some | Few/none |
| GitHub stars | Trending or stable | Stagnant | N/A (not a health signal alone) |
| Stack Overflow activity | Recent Q&A | Old Q&A only | None |

---

## Health Score Calculation

### Per-Indicator Scoring

Rate each indicator on a 0-3 scale:

| Score | Meaning |
|-------|---------|
| 3 | Healthy — no concerns |
| 2 | Acceptable — minor concerns |
| 1 | Warning — monitor closely |
| 0 | Critical — action needed |

### Weighted Score

Not all indicators are equally important. Weights depend on context:

| Indicator | Production Weight | Dev-Only Weight |
|-----------|------------------|----------------|
| Release cadence | 0.15 | 0.10 |
| Commit activity | 0.15 | 0.10 |
| Issue responsiveness | 0.15 | 0.10 |
| Bus factor | 0.15 | 0.05 |
| CI health | 0.10 | 0.05 |
| Downstream adoption | 0.10 | 0.10 |
| Security track record | 0.20 | 0.10 |

```
Health Score = Σ (indicator_score × weight) / (3 × Σ weights) × 100

Example:
  Release cadence:     2 × 0.15 = 0.30
  Commit activity:     3 × 0.15 = 0.45
  Issue responsiveness: 1 × 0.15 = 0.15
  Bus factor:          2 × 0.15 = 0.30
  CI health:           3 × 0.10 = 0.30
  Adoption:            3 × 0.10 = 0.30
  Security:            2 × 0.20 = 0.40

  Score = (0.30+0.45+0.15+0.30+0.30+0.30+0.40) / (3 × 1.00) × 100
        = 2.20 / 3.00 × 100
        = 73%
```

### Score Interpretation

| Score Range | Status | Action |
|-------------|--------|--------|
| 80-100% | Healthy | No action needed |
| 60-79% | Acceptable | Monitor; note in report |
| 40-59% | Warning | Investigate alternatives; add to watch list |
| 0-39% | Critical | Plan migration away; assess immediate risk |

---

## Abandonment Detection

### Definite Abandonment Signals

Any single signal is sufficient to flag as abandoned:

- Repository archived on GitHub/GitLab
- README states "no longer maintained" or "deprecated"
- Last commit > 2 years ago AND open security issues
- Package marked as deprecated in registry (`npm deprecate`, PyPI yanked)
- Maintainer account deleted or inactive > 2 years

### Probable Abandonment Signals

Two or more signals together indicate likely abandonment:

- Last release > 18 months ago
- No commits in 12+ months
- No issue responses in 6+ months
- CI failing for 6+ months
- Only bot commits (dependency updates) for 12+ months

### False Positive: "Done" Packages

Some packages are stable and intentionally not updated. Characteristics:

- Small scope (single purpose, few features)
- No open bugs (or bugs are feature requests)
- API surface is stable and well-documented
- Dependencies are minimal or zero
- The domain doesn't change (math, string processing, data structures)

Examples of legitimately "done" packages:
- `is-odd` — determines if a number is odd. What more could it do?
- `left-pad` — pads strings. Complete.
- `semver` — follows a stable specification

### "Done" vs "Neglected" Decision Tree

```
Has open security vulnerabilities?
├── Yes → NEGLECTED (must update for security)
└── No
    Has open bugs (not feature requests)?
    ├── Yes → NEGLECTED (bugs should be fixed)
    └── No
        Does the domain require ongoing updates?
        ├── Yes (crypto, web framework, API client) → NEGLECTED
        └── No (math, string utils, data structures)
            Has stable API and documentation?
            ├── Yes → DONE (acceptable)
            └── No → NEGLECTED (incomplete)
```

---

## Data Sources for Health Assessment

### Package Registries

| Registry | API Endpoint | Key Fields |
|----------|-------------|------------|
| PyPI | `https://pypi.org/pypi/{pkg}/json` | `info.version`, `releases` (dates), `info.license` |
| npm | `https://registry.npmjs.org/{pkg}` | `dist-tags.latest`, `time` (version dates), `license` |
| crates.io | `https://crates.io/api/v1/crates/{pkg}` | `crate.max_version`, `crate.updated_at` |
| RubyGems | `https://rubygems.org/api/v1/gems/{pkg}.json` | `version`, `version_created_at` |

### Repository Platforms

| Platform | API | Key Endpoints |
|----------|-----|--------------|
| GitHub | REST/GraphQL | `/repos/{owner}/{repo}` (stars, forks), `/commits` (activity), `/issues` (responsiveness) |
| GitLab | REST | `/projects/{id}` (similar data) |

### Aggregate Services

| Service | URL | Provides |
|---------|-----|----------|
| Libraries.io | libraries.io | SourceRank score, dependency info, version history |
| Snyk Advisor | snyk.io/advisor | Health score, maintenance, community, security |
| Socket.dev | socket.dev | Supply chain risk analysis |
| Scorecard | securityscorecards.dev | OpenSSF security scorecard |

---

## Reporting Health Findings

### Per-Dependency Health Summary

```
### {package-name} v{version}

**Health Score:** {score}% ({status})

| Indicator | Value | Score |
|-----------|-------|-------|
| Last release | {date} ({N} months ago) | {0-3} |
| Commits (90d) | {N} | {0-3} |
| Issue response | {N} days median | {0-3} |
| Bus factor | {N} maintainers | {0-3} |
| CI status | {Passing/Failing/None} | {0-3} |
| Downloads (weekly) | {N} | {0-3} |

**Concerns:** {list specific concerns or "None"}
**Recommendation:** {Keep / Monitor / Plan migration / Migrate immediately}
```

### Aggregated Health Report

```
### Dependency Health Overview

| Status | Count | Packages |
|--------|-------|----------|
| Healthy (80%+) | {N} | {list} |
| Acceptable (60-79%) | {N} | {list} |
| Warning (40-59%) | {N} | {list} |
| Critical (0-39%) | {N} | {list} |
```
