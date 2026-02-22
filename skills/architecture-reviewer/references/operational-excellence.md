# Operational Excellence

**Dimension Weight: 7%**

Evaluates whether the system is operable, observable, and maintainable in production.
An architecturally sound system can still fail operationally.

## Table of Contents

1. Sub-Criteria Checklist
2. Observability Maturity Model
3. CI/CD Maturity Assessment
4. Evaluation Guidance by Mode

---

## 1. Sub-Criteria Checklist

### 1.1 CI/CD Maturity

- Is there an automated build pipeline? (Triggered on commit, not manual.)
- Are tests run automatically in the pipeline? (Unit, integration, and/or E2E.)
- Is deployment automated to at least staging/pre-production?
- Are there staged environments? (dev → staging → production, minimum.)
- Is there artifact management? (Versioned build artifacts, container registry.)
- Is the pipeline fast enough for team productivity? (<15 min is good, >30 min is a finding.)
- Are pipeline failures blocking? (Broken builds prevent deployment.)
- Is there branch protection? (PR reviews required, status checks must pass.)

### 1.2 Infrastructure as Code (IaC)

- Is all infrastructure defined in code? (Terraform, CloudFormation, Pulumi, CDK.)
- Can the entire environment be reproduced from code? (No manual console changes.)
- Is IaC version-controlled and reviewed?
- Is there drift detection? (Alerts when actual infra diverges from defined state.)
- Are infrastructure changes applied through the same CI/CD pipeline?
- Is state management handled securely? (Remote state, state locking, encrypted state.)

### 1.3 Observability — Three Pillars

**Logging:**

- Is structured logging used? (JSON, not plain text.)
- Are log levels used appropriately? (DEBUG, INFO, WARN, ERROR — not all INFO.)
- Is there a centralized log aggregation platform? (ELK, Loki, CloudWatch, Datadog.)
- Are logs correlated with request/trace IDs?
- Is log volume managed? (Sampling, level configuration, retention policies.)

**Metrics:**

- Are RED metrics captured for every service? (Rate, Errors, Duration.)
- Are USE metrics captured for infrastructure? (Utilization, Saturation, Errors.)
- Are business metrics captured? (Orders/min, signups, revenue-impacting metrics.)
- Are custom application metrics exposed? (Prometheus, StatsD, CloudWatch custom metrics.)
- Are metric dashboards defined and maintained?

**Distributed Tracing:**

- Is distributed tracing implemented? (OpenTelemetry, Jaeger, Zipkin, X-Ray.)
- Is trace context propagated across service boundaries?
- Are trace IDs included in error responses for debugging?
- Is sampling configured appropriately? (100% for errors, 1-10% for normal traffic.)
- Can a single user request be traced end-to-end across all services?

### 1.4 Alerting Strategy

- Are alerts defined for critical failures? (Service down, error rate spike, latency spike.)
- Are alerts actionable? (Each alert has a clear response action.)
- Are severity tiers defined? (P1-Critical, P2-High, P3-Medium — not everything is critical.)
- Are escalation paths defined? (Who gets paged, when does it escalate.)
- Is there alert fatigue management? (Deduplication, suppression, aggregation.)
- Are alerts based on SLO burn rates rather than raw thresholds where appropriate?

### 1.5 Runbooks & Playbooks

- Are there documented procedures for common incidents?
- Are runbooks linked from alerts? (Alert fires → runbook link in notification.)
- Are runbooks tested and updated? (Not 2 years stale.)
- Do runbooks include: symptoms, diagnosis steps, resolution steps, escalation criteria?
- Are emergency procedures documented? (Database restore, service rollback, incident
  communication.)

### 1.6 Incident Response

- Is there a defined incident response process?
- Are on-call rotations established?
- Is there a post-mortem/retrospective culture? (Blameless post-mortems for every P1/P2.)
- Are Mean-Time-To-Detect (MTTD) and Mean-Time-To-Recovery (MTTR) tracked?
- Is there an incident communication plan? (Status page, stakeholder notifications.)

### 1.7 Chaos Engineering Readiness

- Is graceful degradation tested? (What happens when dependencies fail?)
- Is there capability for failure injection? (Chaos Monkey, Litmus, Gremlin.)
- Have game day exercises been conducted?
- Are circuit breakers and fallbacks verified under actual failure conditions?
- Is there a blast radius understanding for each component failure?

### 1.8 Feature Management

- Are feature flags used for progressive rollout?
- Can features be disabled in production without a deployment?
- Is there A/B testing infrastructure?
- Are feature flags cleaned up after full rollout? (Flag debt management.)
- Is there per-tenant or per-user feature targeting?

### 1.9 Documentation

- Are Architecture Decision Records (ADRs) maintained?
- Is system documentation up-to-date? (Architecture diagrams, data flows, API docs.)
- Are onboarding guides available for new team members?
- Is there operational documentation? (Runbooks, deployment guides, troubleshooting.)
- Is documentation co-located with code or in a discoverable location?

### 1.10 Developer Experience

- Is local development setup documented and functional? (<30 min to first local run.)
- Is the feedback loop fast? (Local test → result in under 5 minutes.)
- Are contribution guidelines clear?
- Is there a consistent development environment? (Docker, devcontainers, Nix.)
- Are code quality tools in place? (Linting, formatting, type checking.)

---

## 2. Observability Maturity Model

| Level         | Description                    | Indicators                                          |
| ------------- | ------------------------------ | --------------------------------------------------- |
| 0 — None      | No observability               | No logging, no metrics, no tracing                  |
| 1 — Basic     | Logs exist but unstructured    | Plain text logs, no centralization, no metrics      |
| 2 — Reactive  | Can investigate known issues   | Centralized logs, basic metrics, no tracing         |
| 3 — Proactive | Alerts for known failure modes | Structured logging, RED/USE metrics, basic alerting |
| 4 — Advanced  | End-to-end visibility          | Distributed tracing, SLO-based alerting, dashboards |
| 5 — Exemplary | Predictive and self-healing    | Anomaly detection, auto-remediation, chaos testing  |

Target level depends on system stage:

- Greenfield design: Plan for Level 3+
- Early development: Implement Level 2-3
- Growth: Achieve Level 3-4
- Mature production: Target Level 4-5

---

## 3. CI/CD Maturity Assessment

| Level                    | Description                          | Indicators                                             |
| ------------------------ | ------------------------------------ | ------------------------------------------------------ |
| 0 — Manual               | Everything is manual                 | Manual builds, FTP deployments, no version control     |
| 1 — Basic                | Version control, some automation     | Git, manual builds, scripted deployment                |
| 2 — CI                   | Automated build and test             | CI pipeline, automated tests, manual deployment        |
| 3 — CD to Staging        | Automated deploy to staging          | Pipeline deploys to staging, manual prod promotion     |
| 4 — CD to Production     | Automated deploy to production       | Full pipeline with staged rollout, rollback capability |
| 5 — Progressive Delivery | Canary, feature flags, auto-rollback | Canary deployments, automated rollback on error spike  |

---

## 4. Evaluation Guidance by Mode

### Mode A (Codebase)

- Check for CI/CD configuration files (.github/workflows, Jenkinsfile, .gitlab-ci.yml)
- Inspect pipeline stages (build, test, lint, security scan, deploy)
- Look for IaC files (Terraform, CloudFormation, Pulumi)
- Check logging patterns in code (structured vs unstructured, log levels)
- Look for metrics instrumentation (Prometheus client, StatsD, custom metrics)
- Check for tracing instrumentation (OpenTelemetry, middleware)
- Look for health check endpoints (/health, /ready, /live)
- Check for feature flag implementations
- Inspect Dockerfiles for best practices (multi-stage builds, non-root, small images)
- Look for ADR directories or decision documentation

### Mode B (Document)

- Check if CI/CD strategy is described
- Look for observability architecture (logging, metrics, tracing strategy)
- Verify alerting and incident response processes are documented
- Check if DR procedures are described
- Look for deployment strategy (blue-green, canary, rolling)
- Verify operational responsibilities are assigned

### Mode C (Hybrid)

- Compare documented operational procedures against actual pipeline implementations
- Check if stated observability strategy matches actual instrumentation
- Verify documented alerting strategy has corresponding alert definitions
- Cross-reference stated deployment strategy against actual pipeline configuration
