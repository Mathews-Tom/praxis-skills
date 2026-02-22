# Enterprise Readiness

**Dimension Weight: 15%**

Evaluates whether the system is fit for enterprise deployment, operations, and compliance.
Includes deep compliance framework checklists.

## Table of Contents

1. Sub-Criteria Checklist
2. Compliance Framework Deep Dives
3. Multi-Tenancy Patterns
4. HA/DR Patterns
5. Evaluation Guidance by Mode

---

## 1. Sub-Criteria Checklist

### 1.1 Multi-Tenancy

- Is tenant isolation implemented at the data layer? (Separate databases, schemas, or
  row-level security.)
- Is tenant isolation implemented at the compute layer? (Separate containers, namespaces,
  or resource quotas.)
- Is network isolation in place between tenants?
- **Noisy neighbor protection:** Can one tenant's workload degrade another's experience?
  Are resource limits enforced per tenant?
- Is tenant context propagated correctly through all layers (API → service → database → logs)?

### 1.2 Authorization Model

- What authorization model is used? RBAC / ABAC / ReBAC / custom?
- Is authorization enforced at every layer, or only at the API gateway?
- Is the principle of least privilege applied? Are default permissions minimal?
- Are authorization policies centralized or scattered across services?
- **Policy enforcement points:** Where are authorization checks performed? Can they be bypassed?

### 1.3 Audit Logging

- Are security-relevant events logged? (Login, logout, failed auth, permission changes,
  data access, data modifications, admin actions.)
- Are audit logs tamper-proof? (Append-only, signed, separate storage from application data.)
- Is there a retention policy compliant with regulatory requirements?
- Are logs searchable and correlatable across services?
- Is PII handled appropriately in audit logs? (Masked, encrypted, or excluded.)

### 1.4 Data Sovereignty & Residency

- Can data be stored and processed in required jurisdictions?
- Is cross-border data transfer addressed? (Standard contractual clauses, adequacy decisions.)
- Are data residency requirements configurable per tenant?
- Is data routing aware of geographic constraints?

### 1.5 SLA Architecture

- Are SLA targets defined? (Availability, latency, throughput, recovery time.)
- Are SLOs (Service Level Objectives) defined per service/endpoint?
- Are error budgets tracked?
- Is the architecture designed to meet stated SLAs? (Redundancy, failover, monitoring.)
- **Composite SLA:** Is the composite SLA calculated from individual component SLAs?
  (99.9% × 99.9% × 99.9% = 99.7%, not 99.9%.)

### 1.6 High Availability (HA)

- Is the deployment active-active or active-passive?
- Is there redundancy at every tier? (Load balancer, application, database, cache, queue.)
- Are health checks implemented and used for automatic failover?
- What is the expected failover time? Is it tested?
- Are there no single points of failure in the HA design?

### 1.7 Disaster Recovery (DR)

- Are RPO (Recovery Point Objective) and RTO (Recovery Time Objective) defined?
- Is there a backup strategy with verified restores?
- Is cross-region or cross-AZ replication in place?
- Are DR runbooks documented and tested? When was the last DR drill?
- Can the system be rebuilt from scratch using IaC?

### 1.8 Deployment Strategy

- Is zero-downtime deployment supported? (Blue-green, canary, rolling.)
- Is rollback automated and tested?
- Are database migrations forward-only and backward-compatible?
- Is there a deployment pipeline with staged environments?
- **Feature flags:** Can new features be deployed but disabled?

### 1.9 Configuration Management

- Are configurations externalized from code? (Environment variables, config services, vaults.)
- Are per-environment configurations managed?
- Is there config drift detection?
- Are feature flags used for runtime configuration changes?
- Can configuration changes be applied without restarts?

### 1.10 API Versioning & Compatibility

- Is API versioning in place? (Path-based, header-based, content-type-based.)
- Are breaking changes managed with a deprecation policy?
- Is backward compatibility maintained for at least one previous version?
- Is there a consumer migration path for breaking changes?
- **Contract testing:** Are consumer-driven contract tests in place?

### 1.11 Integration Patterns

- Is there an API gateway for external integrations?
- Are integration patterns standardized? (REST, GraphQL, gRPC, event-based.)
- Is there a partner/vendor integration strategy?
- Are integration retries, circuit breakers, and timeouts in place?
- **Event mesh:** For event-driven integrations, is there a schema registry and versioning?

### 1.12 Compliance Alignment

- Which compliance frameworks apply? (See Section 2 for deep dives.)
- Are compliance requirements mapped to architectural controls?
- Is there a compliance monitoring and reporting capability?
- Are compliance controls automated where possible?

### 1.13 Vendor Lock-in Assessment

- How portable is the system? Can it move to a different cloud provider?
- What are the switching costs for key dependencies?
- Are cloud-specific services abstracted behind interfaces?
- **Lock-in severity:** Categorize dependencies as (a) easily replaceable, (b) moderately
  coupled, or (c) deeply entrenched.

### 1.14 Team Topology Alignment

- Does the architecture respect Conway's Law? (System structure mirrors team structure.)
- Are service ownership boundaries clear? Does each service have a responsible team?
- Can teams deploy independently?
- Are shared services owned by a platform team?
- Are cross-team dependencies minimized?

---

## 2. Compliance Framework Deep Dives

Evaluate only the frameworks the user identifies as applicable. For each applicable framework,
check the architectural controls below.

### 2.1 SOC 2 Type II

SOC 2 is organized around five Trust Service Criteria. Architectural relevance:

**Security (Common Criteria — CC)**

- CC6.1: Logical access controls — role-based access, MFA, SSO integration
- CC6.2: Credentials management — password policies, API key rotation, secret management
- CC6.3: Encryption — TLS for transit, AES-256 for rest, KMS for key management
- CC6.6: System boundaries — network segmentation, firewall rules, ingress/egress controls
- CC6.7: Change management — deployment pipelines, approval gates, rollback capability
- CC6.8: Vulnerability management — dependency scanning, penetration testing, patch management
- CC7.1: Monitoring — intrusion detection, anomaly detection, real-time alerting
- CC7.2: Incident response — defined procedures, escalation paths, post-mortem process

**Availability (A)**

- A1.1: Capacity management — auto-scaling, capacity planning, performance baselines
- A1.2: Recovery — DR plan, backup strategy, tested failover, defined RTO/RPO

**Processing Integrity (PI)**

- PI1.1: Input validation — server-side validation, type checking, boundary checks
- PI1.2: Processing accuracy — idempotency, transaction integrity, reconciliation
- PI1.3: Output completeness — data validation, checksum verification

**Confidentiality (C)**

- C1.1: Data classification — PII identification, sensitivity levels, handling procedures
- C1.2: Data protection — encryption, tokenization, masking, access logging

**Privacy (P)**

- P1.1: Privacy notice — data collection disclosure, purpose limitation
- P3.1: Data collection — consent management, data minimization
- P4.1: Data use — purpose limitation enforcement, secondary use controls
- P6.1: Data retention — retention policies, automated deletion, archival

### 2.2 HIPAA (Health Insurance Portability and Accountability Act)

Applicable when the system processes Protected Health Information (PHI).

**Technical Safeguards (§ 164.312)**

- Access control: Unique user identification, emergency access procedure, automatic logoff,
  encryption/decryption of ePHI
- Audit controls: Hardware/software/procedural mechanisms to record and examine access to ePHI
- Integrity controls: Mechanisms to authenticate ePHI, protect from improper alteration
- Transmission security: Encryption for ePHI in transit, integrity controls for transmitted data

**Administrative Safeguards (§ 164.308) — Architectural Impact**

- Risk analysis: Documented threat model, vulnerability assessment
- Access management: Role-based access to ePHI, minimum necessary standard
- Contingency plan: Data backup, disaster recovery, emergency mode operation
- Audit logging: Audit trail of all ePHI access with 6-year retention minimum

**Physical Safeguards (§ 164.310) — Cloud Architecture Impact**

- Facility access: Data center security (verify cloud provider compliance)
- Workstation security: Endpoint controls for systems accessing ePHI
- Device controls: Media disposal procedures, encryption for portable devices

**Breach Notification (§ 164.404-410)**

- Detection capability: Automated breach detection, monitoring for unauthorized access
- Notification infrastructure: Ability to identify affected individuals, notification workflows

### 2.3 GDPR (General Data Protection Regulation)

Applicable when processing personal data of EU/EEA residents.

**Data Protection by Design and Default (Art. 25)**

- Data minimization: Collect only what's necessary
- Purpose limitation: Process data only for stated purposes
- Storage limitation: Automated retention enforcement
- Pseudonymization/encryption as default measures

**Lawful Basis & Consent (Art. 6, 7)**

- Consent management: Granular consent collection, withdrawal mechanism
- Lawful basis tracking: Record which legal basis applies per processing activity
- Purpose binding: Enforcement that data isn't used beyond consented purposes

**Data Subject Rights (Art. 15-22) — Architectural Requirements**

- Right of access (Art. 15): Ability to export all personal data for a data subject
- Right to rectification (Art. 16): Ability to update personal data across all stores
- Right to erasure (Art. 17): Cascade deletion across all data stores, backups, logs, caches
- Right to portability (Art. 20): Machine-readable data export capability
- Right to restrict processing (Art. 18): Ability to flag and restrict specific data processing
- Right to object (Art. 21): Opt-out mechanism for profiling and automated decisions

**Data Protection Impact Assessment (Art. 35)**

- Risk assessment capability for new processing activities
- Documentation of processing activities (Art. 30)

**International Transfers (Art. 44-49)**

- Adequacy decisions, Standard Contractual Clauses, Binding Corporate Rules
- Data routing controls to enforce geographic restrictions

**Data Breach Notification (Art. 33-34)**

- 72-hour notification capability to supervisory authority
- Breach detection, classification, and impact assessment mechanisms

### 2.4 PCI-DSS (Payment Card Industry Data Security Standard)

Applicable when storing, processing, or transmitting cardholder data.

**Network Security (Req. 1-2)**

- Firewall/security group rules between CDE (Cardholder Data Environment) and untrusted networks
- No default passwords or vendor-supplied security parameters
- Network segmentation to minimize CDE scope

**Data Protection (Req. 3-4)**

- Stored cardholder data encryption (AES-256), key management procedures
- PAN masking (show only last 4 digits), PAN truncation
- TLS 1.2+ for all transmissions of cardholder data

**Vulnerability Management (Req. 5-6)**

- Anti-malware on all CDE systems, secure development lifecycle
- Patch management (critical patches within 30 days)
- Web application firewall (WAF) for public-facing applications

**Access Control (Req. 7-9)**

- Restrict access to cardholder data by business need-to-know
- Unique ID for each person with computer access
- Multi-factor authentication for administrative access to CDE

**Monitoring & Testing (Req. 10-11)**

- Audit trails for all access to network resources and cardholder data
- Regular vulnerability scans and penetration testing
- Intrusion detection/prevention systems
- File integrity monitoring for critical system files

**Security Policy (Req. 12)**

- Information security policy, risk assessment process
- Incident response plan with defined roles and procedures

### 2.5 FedRAMP (Federal Risk and Authorization Management Program)

Applicable for cloud services used by US federal agencies.

**Architectural Controls (Selected High-Impact)**

- FIPS 140-2 validated cryptographic modules
- Continuous monitoring program (ConMon)
- Boundary protection (managed interfaces, deny by default)
- Multi-factor authentication for all privileged access
- Audit logging with centralized SIEM integration
- Incident response within 1 hour for high-impact systems
- Data sovereignty: US-only data storage and processing
- Background checks for personnel with system access
- Configuration baseline and deviation monitoring
- Vulnerability scanning monthly + after changes, annual penetration testing

---

## 3. Multi-Tenancy Patterns

Evaluate which pattern is in use and whether it's appropriate:

| Pattern                     | Isolation | Cost     | Complexity | When Appropriate                                               |
| --------------------------- | --------- | -------- | ---------- | -------------------------------------------------------------- |
| Shared everything           | Low       | Low      | Low        | Early-stage SaaS, low compliance requirements                  |
| Shared app, separate DB     | Medium    | Medium   | Medium     | Moderate compliance, data isolation required                   |
| Shared app, separate schema | Medium    | Low-Med  | Medium     | PostgreSQL/MySQL multi-schema approach                         |
| Separate deployments        | High      | High     | High       | Strict compliance (HIPAA, FedRAMP), large enterprise customers |
| Hybrid (pool + silo)        | Variable  | Variable | High       | Mix of SMB and enterprise customers                            |

---

## 4. HA/DR Patterns

| Pattern                     | Availability Target | RPO       | RTO             | Cost        |
| --------------------------- | ------------------- | --------- | --------------- | ----------- |
| Single AZ, no DR            | 99.0-99.5%          | Hours     | Hours-Days      | Low         |
| Multi-AZ active-passive     | 99.9%               | Minutes   | Minutes         | Medium      |
| Multi-AZ active-active      | 99.95%              | Near-zero | Seconds-Minutes | Medium-High |
| Multi-region active-passive | 99.95-99.99%        | Minutes   | Minutes         | High        |
| Multi-region active-active  | 99.99%+             | Near-zero | Seconds         | Very High   |

---

## 5. Evaluation Guidance by Mode

### Mode A (Codebase)

- Check for tenant ID propagation in middleware/interceptors
- Inspect database queries for tenant scoping (WHERE tenant_id = ?)
- Look for RBAC/ABAC middleware and policy definitions
- Check audit log implementations and what events are captured
- Inspect deployment manifests for HA configuration (replicas, anti-affinity)
- Review CI/CD pipeline for staged deployments and rollback capability
- Check for compliance-related code: encryption, data masking, consent tracking

### Mode B (Document)

- Verify multi-tenancy strategy is explicitly stated
- Check if compliance requirements are identified and mapped to controls
- Look for HA/DR architecture with specific RPO/RTO targets
- Verify deployment strategy addresses zero-downtime
- Check if data sovereignty requirements are addressed
- Look for API versioning and backward compatibility strategy

### Mode C (Hybrid)

- Compare stated compliance controls against actual implementation
- Verify documented HA/DR strategy matches infrastructure code
- Check if claimed multi-tenancy isolation is actually enforced in code
- Cross-reference stated SLAs against monitoring/alerting implementations
