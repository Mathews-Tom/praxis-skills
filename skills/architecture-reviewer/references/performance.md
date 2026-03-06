# Performance

**Dimension Weight: 17%**

Evaluates whether the system will meet latency, throughput, and resource efficiency targets
under expected and peak conditions.

## Table of Contents

1. Sub-Criteria Checklist
2. Critical Path Analysis Framework
3. Common Performance Anti-Patterns
4. Evaluation Guidance by Mode

---

## 1. Sub-Criteria Checklist

### 1.1 Latency Targets

- Are P50, P95, and P99 latency targets defined for critical endpoints?
- Is the critical path (request → response) mapped with per-hop latency budgets?
- Are latency targets realistic given the architecture? (e.g., 3 synchronous service calls
  plus a database query cannot achieve <50ms P99.)
- Is tail latency (P99.9) considered for user-facing paths?

### 1.2 Throughput Bottlenecks

- Where are the narrowest pipes in the system?
- For each component in the critical path: what is its throughput ceiling?
- Are throughput requirements stated in specific terms? (requests/sec, messages/sec,
  MB/sec, transactions/sec.)
- Under load, which component will saturate first?

### 1.3 Query Efficiency

- **N+1 query detection:** Are there loops that execute one query per iteration instead of
  batch/join queries?
- **Index coverage:** Do frequent queries have supporting indexes? Are there full table scans
  on large tables?
- **Unbounded result sets:** Are queries always paginated/limited? Can a single query return
  millions of rows?
- **Query complexity:** Are there expensive JOINs, subqueries, or aggregations in the
  hot path?
- **ORM overhead:** Is the ORM generating efficient queries? Are there cases where raw queries
  would be significantly better?

### 1.4 Payload Optimization

- Are response payloads sized appropriately? (No returning 100 fields when 5 are needed.)
- Is compression enabled? (gzip, Brotli for HTTP; compression for message queues.)
- Is field selection / sparse fieldsets supported? (GraphQL fields, REST field parameters.)
- Is pagination implemented for all list endpoints? (Cursor-based preferred over offset for
  large datasets.)
- Are large binary payloads (images, files) served via CDN/object storage, not through the
  application?

### 1.5 Connection Efficiency

- Are connection pools configured for all external dependencies? (Database, Redis, HTTP clients.)
- Is HTTP/2 or gRPC used for multiplexed connections between services?
- Are TCP keep-alive settings appropriate?
- Is connection establishment overhead minimized? (Pre-warming, connection reuse.)
- Are TLS session resumption / 0-RTT configured where applicable?

### 1.6 Resource Utilization

- Are compute resources right-sized? (Not 8 vCPUs for a service using 0.5.)
- Are memory limits set appropriately? (Headroom for GC, but not wasting 80% of allocation.)
- Is I/O the bottleneck? (Disk IOPS, network bandwidth.)
- Is there resource contention between co-located workloads?
- Are resource requests and limits defined? (Kubernetes resource specs, Cloud Run limits.)

### 1.7 Cold Start Impact

- **Serverless:** What is the cold start latency? Is it acceptable for the use case?
  Provisioned concurrency used for critical paths?
- **JVM-based services:** Is JVM warm-up accounted for? GraalVM native image considered?
- **Container startup:** How long from container start to serving traffic? Are readiness
  probes configured correctly?
- **Cache cold starts:** After a deployment or cache flush, what is the performance impact?
  Is there a warming strategy?

### 1.8 Caching Effectiveness

- What is the expected cache hit rate? Is it measured?
- Are TTL values appropriate? (Too short → low hit rate; too long → stale data.)
- Is the caching strategy appropriate? (Cache-aside, read-through, write-through,
  write-behind.)
- Are cache keys well-designed? (Avoiding collisions, supporting invalidation patterns.)
- Is cache size bounded? What happens when the cache is full?

### 1.9 Async vs Sync Decisions

- Are synchronous calls used where async would be more appropriate?
- **Candidates for async:** email sending, webhook delivery, report generation, image
  processing, notification dispatch, third-party API calls not in critical path.
- Are fire-and-forget patterns used safely? (With durability guarantees from a queue.)
- For async operations: is there a way for users to check status?

### 1.10 Batch Processing Efficiency

- Are batch jobs optimized with appropriate chunk sizing?
- Is parallelism used for independent batch operations?
- Is progress tracking implemented for long-running batches?
- Do batch jobs compete with live traffic for resources?
- Is there backfill capability? Can failed batches be retried partially?

### 1.11 Network Hops

- How many network hops are in the critical request path?
- Are there cross-AZ or cross-region calls in the critical path? (Each adds 1-5ms minimum.)
- Is DNS resolution cached? Are DNS TTLs appropriate?
- Is TLS handshake overhead minimized? (Session resumption, 0-RTT.)
- Are service-to-service calls within the same network segment where possible?

### 1.12 Database Performance

- Is the database engine appropriate for the access patterns? (OLTP vs OLAP, relational vs
  document vs graph vs time-series.)
- Are read replicas used for read-heavy workloads?
- Is read/write splitting implemented? Are queries routed correctly?
- Are materialized views used for expensive aggregations?
- Is database connection overhead managed? (Connection pooling, persistent connections.)
- Are slow query logs enabled and monitored?

---

## 2. Critical Path Analysis Framework

For each critical user flow, trace the request path:

```text
User Request
  → CDN / Edge (static content, edge rules)
    → Load Balancer (TLS termination, routing)
      → API Gateway (auth, rate limiting)
        → Service A (business logic)
          → Cache Check (Redis/Memcached)
          → Database Query (if cache miss)
          → External API Call (if needed)
        → Service B (if needed, additional hop)
      → Response Assembly
    → Load Balancer
  → CDN
→ User Response
```

For each hop, document:

- Expected latency (P50 and P99)
- Whether the call is synchronous or async
- What happens on failure (retry, fallback, error)
- Can this hop be eliminated or parallelized?

**Latency budget:** The sum of per-hop P99 latencies must not exceed the overall P99 target.
Account for serialization/deserialization, network overhead, and queue wait times.

---

## 3. Common Performance Anti-Patterns

| Anti-Pattern             | Description                                        | Severity |
| ------------------------ | -------------------------------------------------- | -------- |
| N+1 Queries              | Loop executing one query per item instead of batch | S2       |
| Synchronous Waterfalls   | Serial calls that could be parallel                | S2       |
| Missing Indexes          | Frequent queries without supporting indexes        | S2       |
| Unbounded Queries        | No LIMIT/pagination on list queries                | S2       |
| Over-fetching            | Returning far more data than needed                | S3       |
| In-process Heavy Compute | CPU-intensive work blocking request threads        | S2       |
| Cross-region in Hot Path | Synchronous cross-region calls in critical path    | S2       |
| GC Pressure              | Excessive object allocation causing GC pauses      | S3       |
| Connection Churn         | Creating new connections per request               | S2       |
| Logging in Hot Path      | Synchronous verbose logging in critical path       | S3       |
| Uncompressed Payloads    | Large responses without compression                | S4       |
| Missing Cache            | Repeatedly computing/fetching identical data       | S3       |
| Lock Contention          | Coarse-grained locks serializing concurrent work   | S2       |
| Chatty Protocols         | Many small requests instead of batched requests    | S3       |

---

## 4. Evaluation Guidance by Mode

### Mode A (Codebase)

- Trace the critical request path through the code
- Check ORM query patterns for N+1 and unbounded results
- Inspect database schemas for index definitions
- Look for synchronous external API calls in the request path
- Check connection pool configurations (size, timeout, idle settings)
- Review caching implementations (TTL, invalidation, key design)
- Look for async patterns (queue producers, workers, event handlers)
- Check response payload construction (field selection, serialization)
- Inspect resource configurations (CPU/memory limits, instance sizing)

### Mode B (Document)

- Verify latency and throughput targets are stated with specific numbers
- Check if the critical path is mapped and analyzed
- Look for caching strategy specifics (not just "we'll add caching")
- Verify async processing is planned for identifiable long-running operations
- Check if database choice is justified against access patterns
- Look for performance testing plans
- Identify any "TBD" or "will optimize later" notes — these are findings

### Mode C (Hybrid)

- Compare stated performance targets against actual implementation evidence
- Check if documented caching strategy is actually implemented
- Verify async patterns in docs match queue/worker implementations in code
- Cross-reference planned indexes against actual database schema
- Check if performance monitoring (documented) is actually instrumented in code
