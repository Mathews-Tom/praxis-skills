# Structural Integrity & Design Principles

**Dimension Weight: 20%**

Evaluates whether the system's foundational design is sound — its bones, not its skin.

## Table of Contents

1. Sub-Criteria Checklist
2. Anti-Pattern Catalog
3. Architecture Pattern Fitness Evaluation
4. Evaluation Guidance by Mode

---

## 1. Sub-Criteria Checklist

### 1.1 Separation of Concerns

- Are responsibilities clearly divided across modules/services/layers?
- Does each component have a single, well-defined purpose?
- Are cross-cutting concerns (logging, auth, config) handled via shared infrastructure,
  not duplicated in every component?
- **Red flag:** A single module handling user auth, business logic, database queries, and
  external API calls.

### 1.2 Coupling & Cohesion

- **Coupling (want: LOW):** Can you change component A without cascading changes to B, C, D?
  Are interfaces narrow and well-defined? Are components communicating through contracts, not
  internals?
- **Cohesion (want: HIGH):** Are related functions grouped together? Does each module contain
  only things that change for the same reason?
- **Measure:** Count the number of files that must change for a typical feature addition. More
  than 3-4 modules for a simple feature signals high coupling.

### 1.3 Dependency Direction

- Do dependencies point inward (toward domain/business logic), not outward (toward infra)?
- Is the domain layer free from framework imports, HTTP concepts, database specifics?
- Can you swap the database, queue, or API framework without touching business logic?
- **Architectural principle:** Clean Architecture / Hexagonal / Ports-and-Adapters — the
  domain should be the center, infrastructure on the periphery.

### 1.4 Single Points of Failure (SPOF)

- Is there ANY component whose failure brings down the entire system?
- Common SPOFs: single database instance, single load balancer, single DNS, single auth
  service, single queue, hardcoded external service endpoints.
- For each SPOF found: what is the blast radius? Is there a fallback path?

### 1.5 Fault Tolerance Patterns

- **Circuit breakers:** Are external dependencies wrapped in circuit breakers to prevent
  cascading failures?
- **Bulkheads:** Are failure domains isolated? Can a failing component be contained?
- **Retries with exponential backoff:** Are transient failures retried with backoff and jitter?
  Are there retry limits?
- **Timeouts:** Are all external calls configured with explicit timeouts? Are there no
  infinite-wait patterns?
- **Graceful degradation:** Can the system operate in a reduced-functionality mode when
  dependencies are unavailable?

### 1.6 Service Boundary Correctness

- Are service boundaries aligned with business domains / bounded contexts?
- **Distributed monolith test:** Do services deploy independently? Can you deploy service A
  without deploying service B? Do services share a database? Do they require coordinated
  releases?
- **Chatty services test:** Are there high-frequency synchronous calls between services that
  suggest they should be one service?
- **Data ownership:** Does each service own its data, or do multiple services write to the
  same tables?

### 1.7 Data Consistency Model

- Is the consistency model (strong / eventual / causal) explicitly chosen?
- Is the choice appropriate for the domain? (Financial transactions need stronger guarantees
  than social media feeds.)
- Are CAP theorem trade-offs acknowledged and designed for?
- For eventual consistency: is the window of inconsistency acceptable? Are compensating
  transactions defined?
- **Saga pattern assessment:** For distributed transactions, are sagas implemented? Are
  compensation steps defined for each step?

### 1.8 Idempotency

- Are state-changing operations (payments, writes, external API calls) idempotent?
- Is there an idempotency key mechanism?
- What happens on retry? On duplicate submission? On network partition recovery?
- **Critical for:** payment processing, order placement, email sending, external webhooks.

### 1.9 Error Handling Strategy

- Is there a coherent error classification? (Retryable vs non-retryable, user-facing vs
  internal, expected vs unexpected.)
- Are errors handled at the appropriate level? (Not caught-and-swallowed at the bottom,
  not all bubbled to the top.)
- Is error propagation across service boundaries well-defined?
- Are error responses consistent in format and information disclosure?
- **Dead letter handling:** What happens to unprocessable messages/events?

### 1.10 API Contract Quality

- Are APIs designed contract-first (schema defined before implementation)?
- Is versioning present? (URL path, header, or content-type based)
- Are APIs paginated for list endpoints?
- Are request/response schemas documented (OpenAPI, GraphQL schema, proto files)?
- Are error responses standardized?
- **Breaking change management:** Is there a deprecation policy? Consumer notification?

### 1.11 Technology Fitness

- Are technology choices appropriate for the problem domain and scale?
- **Over-engineering signs:** Kubernetes for a single-service app, microservices for a team
  of 2, event sourcing for a CRUD app, Kafka for 10 messages/minute.
- **Under-engineering signs:** SQLite for a multi-user production API, no queue for
  long-running tasks, polling where webhooks/events are needed.
- Is there technology sprawl? (5 different languages, 3 databases, 2 queue systems without
  clear justification.)

### 1.12 Abstraction Quality

- Are abstractions at the right level? Too high (everything is generic, nothing is clear)?
  Too low (implementation details leak through interfaces)?
- Are there leaky abstractions? (ORM that requires raw SQL knowledge, "REST" API that
  exposes database structure.)
- Are there missing abstractions? (Duplicate patterns that should be extracted.)
- Are there premature abstractions? (Generic frameworks for one use case.)

---

## 2. Anti-Pattern Catalog

Flag these patterns with at minimum S3 severity:

| Anti-Pattern               | Description                                                                              | Typical Severity |
| -------------------------- | ---------------------------------------------------------------------------------------- | ---------------- |
| Distributed Monolith       | Microservices that must deploy together, share databases, or require coordinated changes | S2               |
| Big Ball of Mud            | No discernible architecture; everything depends on everything                            | S1               |
| Golden Hammer              | One technology used for everything regardless of fit                                     | S3               |
| God Service/Class          | One component does everything; too many responsibilities                                 | S2               |
| Circular Dependencies      | A depends on B depends on C depends on A                                                 | S2               |
| Shared Database            | Multiple services writing to the same database tables                                    | S2               |
| Chatty Interfaces          | Excessive fine-grained calls between components                                          | S3               |
| Anemic Domain Model        | Business logic scattered outside domain objects                                          | S4               |
| Spaghetti Integration      | Point-to-point connections without standardized patterns                                 | S2               |
| Config in Code             | Hardcoded values that should be externalized                                             | S3               |
| Implicit Dependencies      | Hidden runtime dependencies not visible in interface contracts                           | S3               |
| Vendor Lock-in by Accident | Deep coupling to vendor APIs without abstraction layers                                  | S3               |

---

## 3. Architecture Pattern Fitness Evaluation

When evaluating whether the chosen architecture pattern fits, consider:

**Monolith** — Good fit when: small team (<8), early stage, domain boundaries unclear, low
operational complexity budget. Bad fit when: multiple teams needing independent deployments,
different scaling requirements per component, polyglot requirements.

**Microservices** — Good fit when: multiple teams, independent deployment needed, different
scaling profiles per service, clear domain boundaries. Bad fit when: small team, shared
database, coordinated deployments required, domain boundaries still unclear.

**Serverless / FaaS** — Good fit when: event-driven workloads, variable/spiky traffic,
cost-sensitive low-traffic services, rapid prototyping. Bad fit when: long-running processes,
latency-sensitive critical paths, high sustained throughput, complex stateful workflows.

**Event-Driven / EDA** — Good fit when: loose coupling needed, eventual consistency acceptable,
complex workflows with multiple consumers, audit requirements. Bad fit when: strong consistency
required, simple request-response patterns, small team without event infrastructure experience.

**CQRS** — Good fit when: read and write patterns diverge significantly, complex domain with
rich queries, event sourcing desired. Bad fit when: simple CRUD, read/write patterns similar,
small data volume.

**Modular Monolith** — Good fit when: need monolith simplicity with service-like boundaries,
preparing for future decomposition, moderate team size. Bad fit when: truly independent
scaling is needed now, polyglot requirements.

Do not recommend a pattern switch lightly. Include effort/risk assessment and suggest phased
migration when applicable.

---

## 4. Evaluation Guidance by Mode

### Mode A (Codebase)

- Map the actual dependency graph (import analysis)
- Check for circular dependencies between top-level modules
- Identify the largest files/classes (likely god objects)
- Check configuration patterns (hardcoded vs externalized)
- Look for interface/contract definitions at module boundaries
- Count cross-module imports to assess coupling

### Mode B (Document)

- Check if component responsibilities are clearly stated
- Look for overlapping responsibilities between components
- Verify data ownership is defined per component
- Check if failure scenarios are addressed
- Look for stated consistency model
- Identify any assumed infrastructure not explicitly designed

### Mode C (Hybrid)

- Cross-reference stated boundaries against actual code structure
- Check if documented APIs match implementation
- Verify stated patterns (e.g., "we use CQRS") against actual code
- Identify undocumented components that exist in code
- Flag documented components not yet implemented
