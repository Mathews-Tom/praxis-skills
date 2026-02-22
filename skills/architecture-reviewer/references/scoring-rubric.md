# Scoring Rubric

Detailed scoring criteria for each dimension, weight justification, grade boundaries,
and calibration rules.

## Table of Contents

1. Dimension Score Scale (1-5)
2. Per-Dimension Scoring Criteria
3. Weight Justification
4. Overall Score Calculation
5. Grade Boundaries
6. Calibration Rules

---

## 1. Dimension Score Scale

| Score | Label          | General Criteria                                                                                                                                               |
| ----- | -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 5     | **Exemplary**  | Best-in-class. All sub-criteria met or exceeded. Could serve as a reference architecture. No S1/S2 findings. At most a few S4/S5 findings.                     |
| 4     | **Strong**     | Well-designed. Most sub-criteria met. No S1 findings. At most 1-2 S2 findings. Minor improvements possible.                                                    |
| 3     | **Adequate**   | Meets basic requirements. Several sub-criteria partially met. No S1 findings. Multiple S2/S3 findings. Notable gaps exist but system can function.             |
| 2     | **Concerning** | Significant issues. Multiple sub-criteria unmet. May have S1 findings. Many S2/S3 findings. System will encounter serious problems under realistic conditions. |
| 1     | **Critical**   | Fundamentally flawed. Most sub-criteria unmet or absent. Multiple S1 findings. Requires significant redesign before production use.                            |

### Half-Score Policy

**Half-scores (e.g., 3.5) are permitted** when a dimension falls clearly between two levels.
Use half-scores when:

- The architecture meets most criteria for the higher score but has 1-2 notable gaps
- The architecture exceeds the lower score criteria but doesn't fully meet the higher level
- Evidence supports a nuanced assessment rather than forcing into a whole number

**Do not use half-scores** to avoid making a decision. If uncertain, gather more evidence or
document the uncertainty and round down (conservative scoring).

---

## 2. Per-Dimension Scoring Criteria

### Structural Integrity (20%)

| Score | Criteria                                                                                                                                                                                                                                    |
| ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 5     | Clear separation of concerns, loose coupling, clean dependency direction, no SPOFs, comprehensive fault tolerance, well-defined service boundaries, explicit consistency model, idempotent critical operations, high-quality API contracts. |
| 4     | Good separation with minor coupling issues. No SPOFs in critical path. Most fault tolerance patterns present. API contracts well-defined. 1-2 areas for improvement.                                                                        |
| 3     | Recognizable architecture but some tight coupling. 1-2 SPOFs identified. Basic error handling but inconsistent. API contracts exist but incomplete.                                                                                         |
| 2     | High coupling between components. Multiple SPOFs. No fault tolerance patterns. Inconsistent error handling. Unclear service boundaries.                                                                                                     |
| 1     | No discernible architecture. Circular dependencies. Everything is tightly coupled. No error handling strategy. God classes/services.                                                                                                        |

### Scalability (18%)

| Score | Criteria                                                                                                                                                                                                                |
| ----- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 5     | Stateless services, well-designed multi-layer caching, effective async processing, auto-scaling configured, load distribution optimized, capacity planning documented with projections, no scaling bottlenecks visible. |
| 4     | Services are mostly stateless. Caching layer present. Async processing for most long tasks. Auto-scaling configured. Minor bottleneck risks identified.                                                                 |
| 3     | Some stateful components identified. Basic caching present. Some async processing. Manual scaling or basic auto-scaling. Capacity planning absent or vague.                                                             |
| 2     | Significant stateful components. No or ineffective caching. Most processing synchronous. No auto-scaling. Multiple scaling bottlenecks.                                                                                 |
| 1     | Fundamentally cannot scale horizontally. In-memory state everywhere. No caching. No async processing. Single-instance design.                                                                                           |

### Enterprise Readiness (15%)

| Score | Criteria                                                                                                                                                                                                                                                       |
| ----- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 5     | Full multi-tenancy with isolation, comprehensive RBAC/ABAC, tamper-proof audit logging, compliance controls implemented and verified, HA with tested failover, DR with tested recovery, zero-downtime deployments, API versioning with backward compatibility. |
| 4     | Multi-tenancy with adequate isolation. Role-based access control. Audit logging present. Compliance addressed for applicable frameworks. HA configured. DR plan exists.                                                                                        |
| 3     | Basic multi-tenancy (shared everything with tenant ID filtering). Basic auth model. Some audit logging. Compliance partially addressed. HA planned but not fully implemented.                                                                                  |
| 2     | No multi-tenancy consideration. Minimal authorization. No audit logging. Compliance not addressed despite requirements. No HA/DR.                                                                                                                              |
| 1     | Single-tenant design for a multi-tenant requirement. No authorization model. No compliance consideration despite regulatory requirements. No deployment strategy.                                                                                              |

### Performance (17%)

| Score | Criteria                                                                                                                                                                                                                                             |
| ----- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 5     | P50/P95/P99 targets defined and achievable. Critical path optimized with latency budgets. Efficient queries with proper indexing. Multi-layer caching with proven invalidation. Async processing where appropriate. Connection management optimized. |
| 4     | Performance targets defined. Critical path identified. Most queries efficient. Caching present. Some async processing. Minor optimization opportunities.                                                                                             |
| 3     | Performance targets vague or absent. Some query efficiency issues (N+1, missing indexes). Basic caching. Mixed sync/async patterns. Performance acceptable but unoptimized.                                                                          |
| 2     | No performance targets. Multiple N+1 patterns. No caching. Synchronous heavy operations in critical path. Connection management issues.                                                                                                              |
| 1     | Fundamental performance problems. Unbounded queries. No caching. All processing synchronous. No connection pooling. System will be unacceptably slow under normal load.                                                                              |

### Security (18%)

| Score | Criteria                                                                                                                                                                                                                                                                              |
| ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 5     | Strong authentication (OAuth2/OIDC + MFA). Fine-grained authorization. TLS everywhere (including internal). KMS-managed encryption at rest. Secrets in vault with rotation. Input validation comprehensive. OWASP Top 10 mitigated. Dependency scanning automated. Network segmented. |
| 4     | Strong authentication. Role-based authorization. TLS for external, encryption at rest. Secrets managed (not hardcoded). Input validation present. Most OWASP concerns addressed. Dependency scanning in place.                                                                        |
| 3     | Authentication present but basic. Authorization coarse-grained. TLS for external only. Some encryption at rest. Secrets in environment variables (not committed). Input validation inconsistent. Some OWASP gaps.                                                                     |
| 2     | Weak authentication. Minimal authorization. No encryption at rest. Some secrets in code or config files. Input validation missing in places. Multiple OWASP vulnerabilities likely.                                                                                                   |
| 1     | No authentication or trivially bypassable. No authorization. No encryption. Hardcoded secrets in source code. No input validation. System is actively exploitable.                                                                                                                    |

### Operational Excellence (7%)

| Score | Criteria                                                                                                                                                                                                                                                               |
| ----- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 5     | Full CI/CD with progressive delivery. Complete IaC. Three-pillar observability (structured logs, RED/USE metrics, distributed tracing). SLO-based alerting. Tested runbooks. Incident response process with post-mortems. Feature flags. Chaos engineering capability. |
| 4     | Automated CI/CD to production. IaC for most infrastructure. Centralized logging + metrics. Alerting configured. Some runbooks. Incident response process defined.                                                                                                      |
| 3     | CI with automated tests. Some IaC. Centralized logging but limited metrics/tracing. Basic alerting. Minimal documentation. Informal incident response.                                                                                                                 |
| 2     | Basic CI (build only). Manual deployments. Local/scattered logging. No metrics. No alerting. No runbooks. No incident process.                                                                                                                                         |
| 1     | No CI/CD. No IaC. No centralized logging. No monitoring. Manual everything. No documentation.                                                                                                                                                                          |

### Data Architecture (5%)

| Score | Criteria                                                                                                                                                                                                                                                                            |
| ----- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 5     | Database choice justified by access patterns. Schema well-designed with constraints enforced. Migration tooling with tested rollback. Automated backups with tested restores. Data lifecycle managed. Event architecture (if used) with versioned schemas and dead-letter handling. |
| 4     | Database choice reasonable. Schema generally well-designed. Migration tool in use. Backups configured. Basic lifecycle management. Event handling mostly reliable.                                                                                                                  |
| 3     | Database choice adequate but not justified. Schema has some design issues. Migrations exist but untested. Backups configured but never tested. No lifecycle management.                                                                                                             |
| 2     | Database choice questionable for the access patterns. Schema issues (missing constraints, poor normalization). No migration strategy. Backups uncertain. No event schema management.                                                                                                |
| 1     | Database fundamentally wrong for the use case. No schema management. No migrations. No backups. No data lifecycle consideration.                                                                                                                                                    |

---

## 3. Weight Justification

| Dimension              | Weight | Rationale                                                                                                                     |
| ---------------------- | ------ | ----------------------------------------------------------------------------------------------------------------------------- |
| Structural Integrity   | 20%    | Foundation of everything. Bad structure affects all other dimensions. Highest blast radius for defects.                       |
| Security               | 18%    | A single security failure can be catastrophic (data breach, compliance violation). Cannot be retrofitted easily.              |
| Scalability            | 18%    | Scaling failures are expensive to fix after the fact. Architectural decisions constrain scaling options.                      |
| Performance            | 17%    | Directly impacts user experience and cost. Many performance issues are architectural, not just code-level.                    |
| Enterprise Readiness   | 15%    | Critical for B2B/enterprise but less universally applicable. Weight adjusts based on stated requirements.                     |
| Operational Excellence | 7%     | Important but lower blast radius. Operational gaps cause pain but rarely catastrophic failure. Can be improved incrementally. |
| Data Architecture      | 5%     | Critical when wrong but narrower in scope. Often a subset of structural integrity concerns.                                   |

**Dynamic weight adjustment:** If the system is purely internal tooling with no enterprise
customers, reduce Enterprise Readiness weight and redistribute to other dimensions. Document
any weight adjustments in the report.

---

## 4. Overall Score Calculation

### Formula

```
Overall Score (%) = Σ(dimension_score × weight) / 5 × 100
```

### Calculation Steps (MUST follow in report)

1. **Calculate each weighted contribution:**

   ```
   weighted_contribution = dimension_score × weight
   ```

2. **Sum all weighted contributions:**

   ```
   weighted_sum = Σ(weighted_contribution)
   ```

3. **Convert to percentage:**

   ```
   overall_percentage = weighted_sum / 5 × 100
   ```

4. **Assign grade** based on percentage (see Grade Boundaries below)

### Worked Example

| Dimension              | Score | Weight   | Calculation | Weighted  |
| ---------------------- | ----- | -------- | ----------- | --------- |
| Structural Integrity   | 4     | 20%      | 4 × 0.20    | 0.800     |
| Scalability            | 3     | 18%      | 3 × 0.18    | 0.540     |
| Security               | 3     | 18%      | 3 × 0.18    | 0.540     |
| Performance            | 4     | 17%      | 4 × 0.17    | 0.680     |
| Enterprise Readiness   | 2     | 15%      | 2 × 0.15    | 0.300     |
| Operational Excellence | 3     | 7%       | 3 × 0.07    | 0.210     |
| Data Architecture      | 3     | 5%       | 3 × 0.05    | 0.150     |
| **Total**              |       | **100%** |             | **3.220** |

```
Overall = 3.220 / 5 × 100 = 64.4%
Grade: D (60-69 range)
```

### Arithmetic Verification (REQUIRED)

Before finalizing the report, verify the calculation:

1. **Check weights sum to 100%:** 20 + 18 + 18 + 17 + 15 + 7 + 5 = 100% ✓
2. **Recalculate weighted sum:** Multiply each score × weight, sum results
3. **Verify grade matches range:** Cross-reference percentage with Grade Boundaries table
4. **Sanity check:** If all scores are 3, weighted sum = 3.0, percentage = 60% (D grade)
   If all scores are 4, weighted sum = 4.0, percentage = 80% (B grade)

**Common errors to avoid:**

- Rounding individual weighted contributions before summing (keep 3 decimal places)
- Using wrong weights (check for weight adjustments documented in report)
- Misreading the grade boundary (70-79 is C, not 60-69)

---

## 5. Grade Boundaries

| Range  | Grade | Interpretation                     | Recommended Action                                              |
| ------ | ----- | ---------------------------------- | --------------------------------------------------------------- |
| 90-100 | **A** | Production-ready, enterprise-grade | Maintain and iterate                                            |
| 80-89  | **B** | Solid architecture                 | Address S2 findings before scaling                              |
| 70-79  | **C** | Acceptable with improvement needed | Prioritize S1/S2 findings, create improvement roadmap           |
| 60-69  | **D** | Major rework required              | Address S1 findings immediately, significant refactoring needed |
| <60    | **F** | Fundamental redesign recommended   | Consider architecture reset for most problematic dimensions     |

---

## 6. Calibration Rules

### Stage-Based Expectations

| Stage             | Expected Minimum Grade | Scoring Adjustments                                                             |
| ----------------- | ---------------------- | ------------------------------------------------------------------------------- |
| Greenfield Design | C+                     | Don't penalize for missing implementation. Score the plan, not the code.        |
| Early Development | C                      | Expect foundations to be right. Operational gaps acceptable.                    |
| Growth            | B-                     | Most dimensions should be addressed. Operational excellence becoming important. |
| Mature Production | B+                     | All dimensions should be strong. S1/S2 findings are serious at this stage.      |

### Scale-Based Expectations

| Scale                   | Enterprise Readiness Expectation        | Operational Excellence Expectation |
| ----------------------- | --------------------------------------- | ---------------------------------- |
| Solo dev / side project | Basic auth and deployment sufficient    | CI and basic logging sufficient    |
| Small team (2-5)        | Standard auth, basic monitoring         | CI/CD, centralized logging         |
| Multiple teams (5-20)   | RBAC, audit logging, staged deployments | Full CI/CD, metrics, alerting      |
| Org-wide (20+)          | Full enterprise readiness expected      | Full operational maturity expected |

### Scoring Integrity Rules

1. **Never score N/A as zero.** If a sub-criterion is genuinely not applicable, exclude it
   from the dimension score calculation.
2. **Never inflate scores to be nice.** A 3 that should be a 2 helps no one.
3. **Ground every score in evidence.** "This feels like a 4" is not acceptable. Cite specific
   findings.
4. **Score the architecture, not the team.** Don't give a higher score because the team is
   talented. Score what's in front of you.
5. **Consistency check:** A dimension with multiple S2 findings cannot score above 3. A
   dimension with any S1 finding cannot score above 2.
6. **Minimum one strength per dimension.** Every dimension must have at least one positive
   finding (S5 strength) unless the dimension is truly catastrophic (score 1). Architecture
   reviews that are 100% negative are demoralizing and miss genuine strengths.
7. **Verify arithmetic before finalizing.** Recalculate the weighted sum and percentage
   independently. Grade must match the calculated percentage per Grade Boundaries table.
