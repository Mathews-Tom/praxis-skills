# Scalability

**Dimension Weight: 18%**

Evaluates whether the system can grow to meet demand without architectural rework.

## Table of Contents

1. Sub-Criteria Checklist
2. Scaling Pattern Analysis
3. Bottleneck Identification Framework
4. Capacity Planning Guide
5. Evaluation Guidance by Mode

---

## 1. Sub-Criteria Checklist

### 1.1 Horizontal Scaling Capability

- Can the system scale out (add instances) rather than only scale up (bigger machines)?
- Are there components that inherently prevent horizontal scaling? (In-memory state, local
  file storage, singleton processes, machine-specific cron jobs.)
- Is the system designed for multiple instances from day one, or is horizontal scaling a
  future retrofit?

### 1.2 Statelessness

- Are application-tier services stateless?
- Is session state externalized (Redis, database, JWT) or stored in-process?
- Are there any in-memory caches that would cause inconsistency across instances?
- Can a request be served by any instance, or is session affinity required?
- **Test:** If you kill an instance mid-request, does the user lose state?

### 1.3 Database Scaling Strategy

- **Read scaling:** Read replicas configured? Query routing (writes to primary, reads to
  replicas)? Replica lag tolerance defined?
- **Write scaling:** Sharding strategy? Partition key selection? Cross-shard query handling?
- **Connection management:** Connection pooling (PgBouncer, ProxySQL)? Pool sizing relative
  to instance count? Connection limits per service?
- **Vertical limits:** What is the current database instance size? Is there a clear ceiling?
  What's the plan when you hit it?

### 1.4 Caching Architecture

- **Multi-layer caching:** CDN (static assets) → Application cache (Redis/Memcached) →
  Database query cache → Connection pooling. Which layers exist?
- **Cache invalidation strategy:** Time-based TTL, event-driven invalidation, or
  write-through? Is invalidation reliable?
- **Cache consistency:** What happens when cached data is stale? Is the staleness window
  acceptable for the use case?
- **Cache warming:** Is there a pre-warming strategy for cold starts or cache flushes?
- **Thundering herd:** Are cache stampede / thundering herd scenarios addressed? (Lock-based
  refresh, stale-while-revalidate, probabilistic early expiration.)

### 1.5 Asynchronous Processing

- Are long-running tasks offloaded to background workers / queues?
- Is there backpressure handling? What happens when the queue grows faster than consumers
  can process?
- Are there dead-letter queues for failed messages?
- Is message processing idempotent? (At-least-once delivery means duplicates are possible.)
- **Queue scaling:** Can consumers auto-scale based on queue depth?

### 1.6 Connection Management

- Are connection pools properly sized? (Too few → bottleneck; too many → resource exhaustion.)
- Are connections reused (keep-alive, multiplexing)?
- Are timeout configurations explicit for all external connections?
- **Connection math:** instances × connections_per_instance ≤ database max_connections.
  Does this hold at maximum scale?

### 1.7 Auto-Scaling Policies

- Are scaling triggers defined? (CPU, memory, request rate, queue depth, custom metrics.)
- Are scale-up and scale-down thresholds different? (Prevents flapping.)
- Are cool-down periods configured?
- Are minimum and maximum instance counts set?
- **Predictive scaling:** For known traffic patterns (daily peaks, events), is pre-scaling used?

### 1.8 CDN & Edge Strategy

- Are static assets served from a CDN?
- Are API responses cacheable at the CDN level where appropriate?
- Is geographic distribution addressed for global users?
- **Edge computing:** Are there computations that should run at the edge (auth validation,
  content personalization, A/B testing)?

### 1.9 Hot Spot Analysis

- Are there data partitions, keys, or services that will receive disproportionate traffic?
- **Database hot spots:** Is the partition key well-distributed? Are there "celebrity" rows
  with extreme read/write frequency?
- **Service hot spots:** Is there one service in the critical path of every request?
- **Time-based hot spots:** Do batch jobs, reports, or cron tasks compete with live traffic?

### 1.10 Load Distribution

- What load balancing algorithm is used? (Round-robin, least-connections, weighted, IP-hash.)
- Is session affinity used? If so, does it prevent effective distribution?
- For multi-region: is geographic load balancing in place?
- Is there a service mesh or API gateway handling inter-service traffic distribution?

### 1.11 Rate Limiting & Backpressure

- Are consumers protected from overwhelming producers?
- Are producers protected from slow consumers?
- Is there per-user/per-tenant rate limiting?
- Are rate limits applied at the edge (API gateway) before reaching backend services?
- What happens when limits are hit? (429 responses, queue buffering, graceful degradation.)

### 1.12 Capacity Planning

- Are throughput estimates documented? (Current, 6-month, 12-month, peak.)
- Is data volume growth projected?
- What is the theoretical ceiling of the current architecture?
- At what scale does the architecture require fundamental changes?
- **Cost scaling:** Does cost scale linearly or super-linearly with load?

---

## 2. Scaling Pattern Analysis

Evaluate which patterns are present and whether they're appropriate:

| Pattern                 | When Needed                                       | Red Flag If Missing                           |
| ----------------------- | ------------------------------------------------- | --------------------------------------------- |
| Horizontal app scaling  | >1 instance needed for availability or throughput | Always needed for production systems          |
| Read replicas           | Read-heavy workloads, reporting queries           | High read:write ratio without replicas        |
| Database sharding       | Single-node write capacity exceeded               | Premature if current load is manageable       |
| Message queues          | Async processing, workload buffering              | Synchronous long-running operations           |
| Caching layer           | Repeated expensive computations or queries        | Hot data queried repeatedly from source       |
| CDN                     | Static assets, global user base                   | Serving static files from application servers |
| CQRS                    | Read/write patterns diverge significantly         | Premature for simple CRUD                     |
| Event-driven decoupling | Multiple consumers, loose coupling needed         | Tight synchronous chains across services      |

---

## 3. Bottleneck Identification Framework

For each component in the critical path, evaluate:

```
Component → Throughput Limit → What Happens at Limit → Mitigation
```

Common bottleneck locations (in order of frequency):

1. **Database** — Connection limits, query throughput, lock contention, disk I/O
2. **External APIs** — Rate limits, latency, availability, no circuit breaker
3. **Network** — Bandwidth, cross-AZ latency, DNS resolution, TLS handshake overhead
4. **Compute** — CPU-bound processing, memory pressure, GC pauses
5. **Storage** — Disk I/O, file descriptor limits, storage IOPS limits
6. **Queues** — Consumer throughput, message size, queue depth limits

---

## 4. Capacity Planning Guide

When reviewing capacity, verify:

- **Current baseline:** What is the current load? (requests/sec, data volume, concurrent users)
- **Growth trajectory:** What is the growth rate? (Monthly, quarterly, annual projections)
- **Peak-to-average ratio:** How much does peak load exceed average? (2x? 10x? 100x?)
- **Headroom:** How much capacity headroom exists before the next scaling tier?
- **Breaking points:** At what scale does each component need redesign?
- **Cost model:** How does infrastructure cost grow relative to load?

---

## 5. Evaluation Guidance by Mode

### Mode A (Codebase)

- Check for in-memory state (session stores, local caches, singletons with state)
- Inspect database connection pool configurations
- Look for queue/worker implementations
- Check auto-scaling configs (HPA, ASG, Cloud Run settings)
- Review load balancer configurations
- Identify synchronous blocking calls in the critical path
- Check for file system dependencies (local uploads, temp files, logs written locally)

### Mode B (Document)

- Verify stated scale targets are realistic and specific (not "millions of users")
- Check if the design addresses database scaling beyond single node
- Look for caching strategy presence and specificity
- Verify async processing is planned for long-running operations
- Check if capacity planning is addressed with concrete numbers
- Identify any component described as "single instance" without justification

### Mode C (Hybrid)

- Compare stated scale targets against actual infrastructure sizing
- Check if documented scaling strategy matches implemented auto-scaling rules
- Verify caching strategy in docs matches caching code in implementation
- Look for implemented scaling patterns not mentioned in docs (and vice versa)
