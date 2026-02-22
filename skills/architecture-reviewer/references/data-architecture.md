# Data Architecture

**Dimension Weight: 5%**

Evaluates the data layer's design, integrity, lifecycle management, and fitness for the
system's access patterns. The data layer is often the silent constraint.

## Table of Contents

1. Sub-Criteria Checklist
2. Data Model Fitness Evaluation
3. Event Architecture Patterns
4. Evaluation Guidance by Mode

---

## 1. Sub-Criteria Checklist

### 1.1 Schema Design Quality

- Is normalization level appropriate? (3NF for OLTP, denormalized for read-heavy/analytics.)
- Is denormalization intentional and documented, or accidental?
- Are naming conventions consistent? (snake_case, camelCase — pick one.)
- Are data types appropriate? (No VARCHAR for timestamps, no TEXT for booleans.)
- Are constraints enforced at the database level? (NOT NULL, UNIQUE, FOREIGN KEY, CHECK.)
- Is referential integrity maintained? Or is it "enforced by the application"? (Fragile.)

### 1.2 Data Model Fitness

- Is the database engine appropriate for the access patterns?

| Access Pattern                | Best Fit                                   | Poor Fit                             |
| ----------------------------- | ------------------------------------------ | ------------------------------------ |
| Transactional CRUD            | Relational (PostgreSQL, MySQL)             | Document DB for complex transactions |
| Hierarchical/nested documents | Document (MongoDB, DynamoDB)               | Relational with deep JOINs           |
| Relationship traversal        | Graph (Neo4j, Neptune)                     | Relational with recursive CTEs       |
| Time-series metrics           | Time-series (TimescaleDB, InfluxDB)        | Relational without partitioning      |
| Full-text search              | Search engine (Elasticsearch, Meilisearch) | LIKE queries on relational           |
| Key-value lookups             | KV store (Redis, DynamoDB)                 | Relational for simple lookups        |
| Wide-column analytics         | Columnar (ClickHouse, BigQuery)            | Row-oriented for OLAP                |
| Vector similarity             | Vector DB (Pinecone, pgvector, FAISS)      | Relational without extensions        |

- Is polyglot persistence justified? (Multiple databases for different access patterns is
  valid, but adds operational complexity. Is the trade-off worth it?)

### 1.3 Migration Strategy

- Is a schema migration tool in place? (Flyway, Alembic, Knex, Prisma Migrate, Atlas.)
- Are migrations version-controlled and sequential?
- Are migrations forward-only or reversible? (Forward-only is safer for production.)
- Can migrations run without downtime? (No exclusive locks on large tables.)
- Is there a strategy for blue-green data migrations?
- Are data migrations tested in staging with production-like data volumes?

### 1.4 Backup & Recovery

- Are automated backups configured? (Daily minimum for production.)
- Is point-in-time recovery (PITR) available?
- Are backup restores tested regularly? (Untested backups are not backups.)
- Is cross-region backup replication in place for DR?
- Are backups encrypted?
- What is the backup retention period? Is it compliant with regulatory requirements?
- **RTO/RPO alignment:** Can the backup strategy meet the stated RPO?

### 1.5 Data Lifecycle Management

- Are data retention policies defined per data type?
- Is there an automated archival strategy for old data?
- Is TTL configured for ephemeral data? (Sessions, caches, temporary tokens.)
- Is there a data purge mechanism for GDPR right-to-erasure compliance?
- Is data growth projected? What is the storage scaling plan?

### 1.6 Event Architecture

- **Event sourcing:** If used, are events the source of truth? Are projections
  well-defined? Is replay capability implemented?
- **CQRS:** If used, is the read model kept in sync reliably? What is the sync lag?
- **Event schema:** Are event schemas versioned? Is there a schema registry?
- **Dead letter queues:** What happens to unprocessable events?
- **Ordering guarantees:** Is event ordering guaranteed where needed? (Partition-based
  ordering in Kafka, FIFO queues in SQS.)
- **Idempotent consumers:** Can events be safely reprocessed?

### 1.7 Data Pipeline Reliability

- Is pipeline processing idempotent?
- What delivery semantics are used? (Exactly-once, at-least-once, at-most-once.)
- Is there replay capability for failed or corrupted pipeline runs?
- Are checkpoints/offsets managed reliably?
- Is there data validation at pipeline boundaries? (Schema validation on ingest.)
- Are pipeline failures alerted and automatically retried?

### 1.8 Schema Versioning & Compatibility

- Are schema changes backward-compatible? (Adding columns with defaults, not renaming.)
- Are forward-compatible changes planned? (New consumers can handle old data.)
- Is there contract testing between producers and consumers of shared data?
- For event schemas: is there a compatibility mode? (BACKWARD, FORWARD, FULL in
  schema registries.)
- Are breaking schema changes managed with a migration plan?

---

## 2. Data Model Fitness Evaluation

When evaluating data model fitness, consider:

**Read-to-write ratio:** High read ratios suggest caching, read replicas, or denormalized
read models. High write ratios suggest write-optimized storage, append-only patterns, or
event sourcing.

**Query patterns:** If most queries are by a single key → KV store. If queries involve
complex JOINs → relational. If queries traverse relationships → graph. If queries are
full-text search → search engine. If queries are aggregations over time → time-series.

**Data volume trajectory:** Current volume may fit in a single database, but projected
growth may require partitioning, sharding, or a different engine entirely. Flag this early.

**Consistency requirements:** Financial and transactional data typically needs strong
consistency (relational with ACID). Social feeds, analytics, and caching can tolerate
eventual consistency.

**Access locality:** Is data accessed together stored together? If a query always needs
user + orders + recent activity, a document model or denormalized relational model may be
more efficient than normalizing across 5 tables.

---

## 3. Event Architecture Patterns

| Pattern                      | Use When                                                  | Complexity  | Consistency                |
| ---------------------------- | --------------------------------------------------------- | ----------- | -------------------------- |
| Event Notification           | Loose coupling between services, eventual consistency OK  | Low         | Eventual                   |
| Event-Carried State Transfer | Consumers need data without calling back to source        | Medium      | Eventual                   |
| Event Sourcing               | Full audit trail needed, complex domain, temporal queries | High        | Strong (within aggregate)  |
| CQRS                         | Read and write models diverge significantly               | Medium-High | Eventual (read model)      |
| Saga (Orchestration)         | Distributed transactions with centralized coordinator     | High        | Eventual with compensation |
| Saga (Choreography)          | Distributed transactions with event-driven coordination   | High        | Eventual with compensation |

When event architecture is present, verify:

- Events are immutable (never modified after publishing)
- Event schemas are versioned
- Dead-letter handling exists
- Consumer idempotency is implemented
- Ordering guarantees match requirements

---

## 4. Evaluation Guidance by Mode

### Mode A (Codebase)

- Inspect database migration files for schema design quality
- Check ORM model definitions for constraint enforcement
- Look for multiple database configurations (polyglot persistence)
- Check for migration tools and their configuration
- Inspect backup configurations in IaC files
- Look for event schema definitions and versioning
- Check queue/event handler code for idempotency patterns
- Review database index definitions against query patterns

### Mode B (Document)

- Verify data model choice is justified against stated access patterns
- Check if migration strategy is addressed
- Look for backup/recovery strategy with specific RPO/RTO
- Verify data lifecycle policies are defined
- Check if event architecture (if planned) addresses ordering, idempotency, dead letters
- Look for data volume projections and storage scaling plan
- Identify any unstated assumptions about data model ("we'll use PostgreSQL" without
  justifying why)

### Mode C (Hybrid)

- Compare documented data model against actual schema definitions
- Check if stated backup strategy matches actual backup configurations
- Verify documented event schemas match actual event definitions in code
- Cross-reference data lifecycle policies against actual TTL/archival implementations
- Check if planned indexes exist in actual database schema
