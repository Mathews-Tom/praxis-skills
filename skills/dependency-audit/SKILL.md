---
name: dependency-audit
description: >
  Audits project dependencies for license compliance, maintenance health, security
  vulnerabilities, and bloat. Analyzes both direct and transitive dependency trees,
  detects abandoned packages, identifies license conflicts (copyleft, unknown), checks
  for known CVEs, and finds unused or duplicate dependencies.
  Triggers on: "audit dependencies", "dependency check", "license check",
  "dependency health", "abandoned packages", "bloat check", "unused dependencies",
  "security audit dependencies", "dependency review", "license compliance",
  "package audit", "supply chain", "dependency risk".
  Use this skill when reviewing project dependencies for risk.
metadata:
  version: 1.1.0
---

# Dependency Audit

Comprehensive dependency risk assessment: license compatibility analysis, maintenance
health scoring, CVE detection, bloat identification, and transitive dependency risk
mapping. Produces an actionable report with prioritized remediation steps organized by
urgency (security → license → maintenance → bloat).

## Reference Files

| File                                  | Contents                                                                   | Load When                |
| ------------------------------------- | -------------------------------------------------------------------------- | ------------------------ |
| `references/license-compatibility.md` | License compatibility matrix, copyleft detection, commercial-safe licenses | Always                   |
| `references/health-metrics.md`        | Maintenance health indicators, scoring criteria, abandonment detection     | Always                   |
| `references/bloat-detection.md`       | Identifying unused deps, duplicate functionality, heavy transitive trees   | Bloat analysis requested |
| `references/cve-sources.md`           | CVE databases, advisory sources, vulnerability severity interpretation     | Security audit requested |

## Prerequisites

- Access to the project's dependency files (`pyproject.toml`, `requirements.txt`,
  `package.json`, `Cargo.toml`, `go.mod`)
- Lock file (for exact versions and transitive dependencies)
- Project license (to determine compatibility requirements)

## Workflow

### Phase 1: Parse Dependency Tree

1. **Direct dependencies** — Packages explicitly declared in the project.
2. **Transitive dependencies** — Dependencies of dependencies. Often 10-50x the
   direct count.
3. **Version constraints** — Pinned (`==1.2.3`), ranged (`>=1.0,<2.0`), or floating (`*`).
4. **Development vs production** — Separate dev/test dependencies from production.

Tools:

- Python: `uv pip list`, `pip-audit`, `pipdeptree`
- Node.js: `npm list --all`, `npm audit`
- Rust: `cargo tree`, `cargo audit`

### Phase 2: Audit Licenses

For each dependency:

1. **Identify the license** — Check package metadata, LICENSE file, pyproject.toml.
2. **Classify compatibility** — Against the project's own license:

   | License                   | Commercial OK            | Copyleft         | Risk Level |
   | ------------------------- | ------------------------ | ---------------- | ---------- |
   | MIT, BSD, ISC, Apache 2.0 | Yes                      | No               | Low        |
   | LGPL                      | With care                | Weak             | Medium     |
   | GPL-2.0, GPL-3.0          | No (unless GPL project)  | Strong           | High       |
   | AGPL                      | No (unless AGPL project) | Strong + network | Critical   |
   | Unknown                   | Cannot determine         | Unknown          | Critical   |

3. **Flag issues** — Copyleft licenses in proprietary projects, unknown licenses,
   license changes between versions.

### Phase 3: Assess Maintenance Health

For each dependency, evaluate maintenance signals:

| Indicator            | Healthy        | Warning     | Abandoned                |
| -------------------- | -------------- | ----------- | ------------------------ |
| Last release         | < 6 months     | 6-18 months | > 18 months              |
| Commits (90 days)    | 10+            | 1-9         | 0                        |
| Open issues response | < 2 weeks      | 2-8 weeks   | > 8 weeks or no response |
| Bus factor           | 3+ maintainers | 2           | 1                        |
| CI status            | Passing        | Flaky       | Failing or absent        |

### Phase 4: Check Security

1. **Known CVEs** — Check against advisory databases:
   - Python: `pip-audit`, PyPI advisory database
   - Node.js: `npm audit`, GitHub Advisory Database
   - General: NVD (National Vulnerability Database)

2. **Severity classification** — CVSS score interpretation:

   | CVSS Score | Severity | Action                 |
   | ---------- | -------- | ---------------------- |
   | 9.0-10.0   | Critical | Upgrade immediately    |
   | 7.0-8.9    | High     | Upgrade within days    |
   | 4.0-6.9    | Medium   | Upgrade within weeks   |
   | 0.1-3.9    | Low      | Upgrade at convenience |

3. **Fix availability** — Is there a patched version? If not, what's the workaround?

### Phase 5: Detect Bloat

1. **Unused dependencies** — Dependencies imported nowhere in the codebase.
2. **Duplicate functionality** — Multiple packages doing the same thing (2 HTTP clients,
   2 JSON parsers).
3. **Heavy transitive trees** — Packages that pull in dozens of sub-dependencies for
   a simple feature.
4. **Size analysis** — Large packages used for small functionality.

### Phase 6: Report

Produce a prioritized report with action items.

## Output Format

```text
## Dependency Audit: {Project Name}

### Summary
| Metric | Count |
|--------|-------|
| Direct dependencies | {N} |
| Transitive dependencies | {N} |
| License issues | {N} |
| Maintenance concerns | {N} |
| Security vulnerabilities | {N} |
| Bloat candidates | {N} |

### License Compliance

| Package | Version | License | Compatible | Issue |
|---------|---------|---------|------------|-------|
| {pkg} | {ver} | MIT | Yes | None |
| {pkg} | {ver} | GPL-3.0 | No | Copyleft in proprietary project |
| {pkg} | {ver} | Unknown | Unknown | License not identifiable |

### Maintenance Health

| Package | Last Release | Commits (90d) | Maintainers | Status |
|---------|-------------|---------------|-------------|--------|
| {pkg} | {date} | {N} | {N} | {Healthy/Warning/Abandoned} |

### Security Vulnerabilities

| Package | Version | CVE | Severity | Fix Available | Fixed In |
|---------|---------|-----|----------|---------------|----------|
| {pkg} | {ver} | {CVE-ID} | {severity} | {Yes/No} | {version} |

### Bloat Analysis

| Package | Install Size | Used By | Recommendation |
|---------|-------------|---------|----------------|
| {pkg} | {size} | {usage description} | {Remove/Replace/Keep} |

### Action Items

#### Immediate (Security)
1. Upgrade {pkg} to {version} — fixes {CVE-ID} ({severity})

#### Short-term (License)
1. Review {pkg} GPL usage — may require license change or removal

#### Medium-term (Maintenance)
1. Find alternative to {pkg} — abandoned since {date}

#### Long-term (Bloat)
1. Remove {pkg} — unused in codebase
2. Replace {pkg} with lighter alternative

### Transitive Risk
- {direct-dep} depends on {transitive-dep} which has {issue}
```

## Calibration Rules

1. **Production dependencies first.** Dev/test dependencies have lower risk since they
   don't ship to users. Audit production dependencies with higher scrutiny.
2. **Transitive risk is real.** A direct dependency with MIT license may pull in a GPL
   transitive dependency. Always check the full tree.
3. **Abandoned is not broken.** A mature, stable library that hasn't been updated in a
   year may be perfectly fine. Evaluate based on whether the library is "done" vs "neglected."
4. **Security is non-negotiable.** Critical and High CVEs must be addressed immediately.
   Medium CVEs should be tracked. Low CVEs can wait for the next dependency update cycle.

## Error Handling

| Problem                                 | Resolution                                                                                             |
| --------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| No lock file available                  | Audit based on declared dependencies. Note that transitive analysis is incomplete without a lock file. |
| License metadata missing                | Check the package's repository for LICENSE file. Note packages where license cannot be determined.     |
| Package registry unavailable            | Work from cached metadata and local lockfile data.                                                     |
| Too many dependencies to audit manually | Prioritize: production deps first, then direct deps, then transitive deps with known issues.           |

## When NOT to Audit

Push back if:

- The project is a prototype that won't ship — defer audit until production decision
- The user wants dependency updates, not audit — different task (dependabot, renovate)
- The project has no dependencies (pure standard library) — nothing to audit
