# Document Review Guide

Reference for Mode B (Document Review) and Mode C (Hybrid). Provides completeness checklists,
common gaps in architecture documents, and questions to surface unstated assumptions.

## Table of Contents

1. Architecture Document Completeness Checklist
2. Common Gaps & Missing Concerns
3. Questions to Ask for Greenfield Projects
4. Questions to Ask for Existing Systems
5. Document Quality Assessment

---

## 1. Architecture Document Completeness Checklist

Rate each section as: ✅ Addressed, ⚠️ Partially Addressed, ❌ Missing, N/A Not Applicable.

### System Overview

- [ ] System purpose and business context
- [ ] Target users and personas
- [ ] Key use cases / user flows
- [ ] System scope (what's included and excluded)
- [ ] Key assumptions and constraints
- [ ] Success metrics / KPIs

### Functional Architecture

- [ ] Component inventory with responsibilities
- [ ] Component interaction diagram
- [ ] Data flows between components
- [ ] API contracts (at least interface-level)
- [ ] External system integrations
- [ ] Asynchronous workflows identified

### Non-Functional Requirements

- [ ] Performance targets (latency, throughput)
- [ ] Availability target (SLA / uptime percentage)
- [ ] Scalability requirements (current + projected)
- [ ] Security requirements
- [ ] Compliance requirements
- [ ] Data retention and privacy requirements

### Infrastructure Architecture

- [ ] Deployment topology (cloud, region, AZ)
- [ ] Compute strategy (containers, serverless, VMs)
- [ ] Networking (VPC, subnets, load balancers)
- [ ] Storage strategy (databases, object storage, caches)
- [ ] CDN / edge strategy
- [ ] Environment strategy (dev, staging, production)

### Data Architecture

- [ ] Data model (at least ER diagram level)
- [ ] Database technology selection with justification
- [ ] Data lifecycle (retention, archival, deletion)
- [ ] Backup and recovery strategy
- [ ] Migration strategy

### Security Architecture

- [ ] Authentication mechanism
- [ ] Authorization model
- [ ] Encryption (transit + rest)
- [ ] Secret management
- [ ] Network security
- [ ] Threat model or security considerations

### Operational Architecture

- [ ] CI/CD pipeline design
- [ ] Monitoring and alerting strategy
- [ ] Logging strategy
- [ ] Incident response process
- [ ] Deployment strategy (rollout, rollback)
- [ ] Disaster recovery plan

### Decision Records

- [ ] Technology choices justified
- [ ] Trade-offs documented
- [ ] Alternatives considered and reasons for rejection
- [ ] Known risks acknowledged

---

## 2. Common Gaps & Missing Concerns

These are the concerns most frequently absent from architecture documents. Each missing
concern is a potential finding.

### Frequently Missing (High Impact)

1. **Error handling strategy** — What happens when things fail? Most docs describe the
   happy path only.
2. **Data consistency model** — Is it strong or eventual? Most docs never state this
   explicitly, leading to incorrect assumptions.
3. **Capacity planning** — "Millions of users" is not a plan. Specific numbers for current,
   6-month, 12-month, and peak scenarios are needed.
4. **Cache invalidation** — "We'll cache it" appears often. How the cache is invalidated
   appears rarely.
5. **Secret management** — Where do credentials live? How are they rotated?
6. **Migration path** — For existing systems: how do you get from here to there? For new
   systems: what's the schema migration strategy?
7. **Backup restore testing** — Backups are mentioned, testing restores is not.
8. **Cost model** — What does this architecture cost at 1x, 10x, 100x scale?

### Frequently Understated (Medium Impact)

9. **Cross-cutting concerns** — Logging, tracing, metrics are "assumed" but not designed.
10. **API versioning** — Mentioned as "we'll version the API" without specifying how.
11. **Database connection management** — Pool sizes, connection limits, failover.
12. **Rate limiting** — Often absent for internal APIs between services.
13. **Idempotency** — Retry behavior is undefined for state-changing operations.
14. **Feature flagging** — Progressive rollout capability is assumed but not designed.

### Frequently Overlooked (Lower Impact but Important)

15. **Team topology alignment** — Architecture designed without considering who builds/owns it.
16. **Vendor lock-in** — Cloud-specific services used without abstraction layer discussion.
17. **Developer experience** — Local development, onboarding, contribution workflow.
18. **Data sovereignty** — Where is data stored? Does it cross borders?
19. **Composite SLA** — Individual component SLAs stated but composite SLA not calculated.

---

## 3. Questions to Ask for Greenfield Projects

When reviewing a design that has not yet been built:

**Viability Questions:**

- Has the team built systems of this complexity before?
- Is the timeline realistic for the proposed architecture complexity?
- Are there simpler alternatives that would meet the same requirements?
- What is the minimum viable architecture? Can complexity be added iteratively?

**Assumption Challenges:**

- What are the three things most likely to be wrong in this design?
- What happens if the scale estimate is 10x higher? 10x lower?
- What happens if a key technology choice turns out to be wrong? How expensive is the pivot?
- Which components are the team least experienced with?

**Prioritization Questions:**

- If you could only build 3 of the 10 planned components, which 3 would you build?
- What is the simplest possible version that could go to production?
- Which non-functional requirements are day-1 must-haves vs can-be-added-later?

**Risk Questions:**

- What is the single most likely cause of project failure?
- What is the single most likely cause of production incident?
- Which external dependency poses the biggest risk? (Vendor, API, library.)

---

## 4. Questions to Ask for Existing Systems

When reviewing an architecture document for a system already in production:

**Reality Check Questions:**

- How closely does this document match the actual running system?
- What has been built but is not documented here?
- What is documented here but has not been built?
- When was this document last updated?

**Operational History Questions:**

- What are the most frequent production incidents?
- What is the most common developer complaint about the architecture?
- Which component is the most fragile?
- Where does the team spend the most unplanned maintenance time?

**Evolution Questions:**

- What architectural decisions would you reverse if you could?
- What is the biggest scaling concern in the next 12 months?
- What technical debt is actively causing problems?

---

## 5. Document Quality Assessment

Beyond content completeness, assess document quality:

**Specificity:** Replace vague statements with specific questions.

- ❌ "The system will be scalable" → What does "scalable" mean specifically?
- ❌ "We will use caching" → What caching strategy? What data? What TTL?
- ❌ "The API will be secure" → What authentication? What authorization model?
- ❌ "High availability" → What availability percentage? What's the failover strategy?

**Consistency:** Check for internal contradictions.

- Does the stated consistency model match the database choice?
- Does the stated availability target match the infrastructure design?
- Do stated scale targets match the infrastructure sizing?

**Completeness of Trade-offs:** Every architectural decision should acknowledge what was
given up. If a document presents only benefits, the trade-offs are unstated, not absent.

**Diagram Quality:** Architecture diagrams should show:

- Component boundaries (what's inside vs outside)
- Data flows (arrows with labels, not just boxes)
- Synchronous vs asynchronous communication
- External system boundaries
- Network boundaries (public, private, data tier)
