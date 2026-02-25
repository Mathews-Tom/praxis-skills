# Log Analysis

Patterns for extracting debugging information from log output: temporal analysis,
anomaly detection, correlation, and structured filtering.

---

## Log Anatomy

### Standard Log Format

```
2026-02-25 14:30:01.123 [ERROR] auth.handler:45 - Failed to validate token: expired
│                        │       │              │   └─ Message
│                        │       │              └─ Line number
│                        │       └─ Module/function
│                        └─ Level
└─ Timestamp
```

### Key Fields for Debugging

| Field | What It Tells You | Red Flags |
|-------|-------------------|-----------|
| Timestamp | When the event occurred | Gaps, clustering, wrong timezone |
| Level | Severity (DEBUG, INFO, WARN, ERROR, CRITICAL) | ERROR/CRITICAL entries |
| Module | Where in the code | Unexpected modules in error path |
| Message | What happened | Exception text, unexpected values |
| Request ID | Which request failed | Correlate across services |
| User/Session | Who was affected | Single user vs. all users |

---

## Temporal Analysis

### Timeline Construction

Build a timeline of events around the failure:

```bash
# Extract ERROR and CRITICAL entries around the failure time
grep -E '(ERROR|CRITICAL)' app.log | grep '2026-02-25 14:3'

# Get all log entries in a 5-minute window
awk '/2026-02-25 14:28/,/2026-02-25 14:33/' app.log
```

### What to Look For in the Timeline

1. **First occurrence** — The first error in a burst is the root cause; subsequent
   errors are cascading failures.
2. **Preceding events** — What happened in the 30 seconds before the first error?
   Look for warnings, unusual state changes, or external events.
3. **Gaps** — Missing log entries (silence) can indicate:
   - Process crash (no graceful shutdown log)
   - Deadlock (process hung, no new entries)
   - Log rotation issue
4. **Periodicity** — Errors occurring at regular intervals suggest:
   - Cron job failure
   - Health check failure
   - Connection pool cycling

### Timestamp Anomalies

| Anomaly | Possible Cause |
|---------|----------------|
| Out-of-order timestamps | Multi-threaded logging, clock skew |
| Large gap followed by burst | Process was blocked, then recovered |
| Microsecond-level clustering | Single request cascading through multiple components |
| Regular intervals (30s, 60s) | Retry mechanism, health check, cron |

---

## Pattern Extraction

### Filtering Techniques

```bash
# Count errors by type
grep 'ERROR' app.log | sed 's/.*ERROR.*- //' | sort | uniq -c | sort -rn

# Find most common error messages
grep 'ERROR' app.log | awk -F'- ' '{print $NF}' | sort | uniq -c | sort -rn | head -20

# Extract unique stack traces
grep -A 5 'Traceback' app.log | grep -v '^--$' | sort -u

# Filter by request ID
grep 'req_abc123' app.log
```

### Error Clustering

Group errors to distinguish root causes from symptoms:

1. **Same error, same location** → Single bug, multiple triggers
2. **Different errors, same time** → Cascading failure from one root cause
3. **Same error, different locations** → Systemic issue (e.g., DB down)
4. **Same error, same schedule** → Triggered by recurring event

### State Transition Tracking

For bugs involving state machines or workflows:

```bash
# Track state changes for a specific entity
grep 'order_id=12345' app.log | grep -E '(state|status)'
```

Look for:
- Missing transitions (jumped from state A to state C, skipping B)
- Repeated transitions (state oscillation)
- Terminal state reached prematurely

---

## Correlation

### Cross-Service Correlation

When debugging distributed systems, correlate logs across services:

1. **Request ID** — Trace a single request across services
2. **Timestamp alignment** — Ensure clocks are synchronized (NTP)
3. **Causation chain** — Service A calls B calls C; error in C may originate in A

```bash
# Find all log entries for a request across services
grep 'request_id=abc123' service_a.log service_b.log service_c.log
```

### External Event Correlation

Check if the error coincides with:

| External Event | How to Check |
|----------------|--------------|
| Deployment | `git log --oneline --since="2026-02-25 14:00"`, CI/CD logs |
| Config change | Config management audit log |
| Load spike | Metrics dashboard, request rate graphs |
| Dependency outage | Status pages, external service logs |
| Certificate expiry | `openssl s_client -connect host:443` |
| DNS change | `dig` results, TTL expiry |

---

## Structured Logging Queries

### JSON Logs

Modern applications use structured (JSON) logging:

```bash
# Parse JSON logs with jq
cat app.log | jq 'select(.level == "ERROR") | {time: .timestamp, msg: .message}'

# Filter by field
cat app.log | jq 'select(.user_id == "12345")'

# Count by error type
cat app.log | jq 'select(.level == "ERROR") | .error_type' | sort | uniq -c | sort -rn

# Time range filter
cat app.log | jq 'select(.timestamp >= "2026-02-25T14:28:00" and .timestamp <= "2026-02-25T14:33:00")'
```

### Key-Value Logs

```bash
# Extract specific fields from key=value format
grep 'ERROR' app.log | grep -oP 'user_id=\K[^ ]+'

# Build a frequency table
grep 'ERROR' app.log | grep -oP 'error_code=\K[^ ]+' | sort | uniq -c | sort -rn
```

---

## What Logs Won't Tell You

Logs have blind spots. Be aware of what they cannot show:

| Blind Spot | Alternative |
|------------|-------------|
| What DIDN'T happen (missing log = no evidence) | Add instrumentation |
| Performance timing between log entries | Add duration metrics |
| Memory state at time of error | Add memory profiling or dumps |
| Thread interleaving | Add thread ID to log format |
| Values of variables not logged | Add targeted debug logging |
| Events in third-party code | Enable library debug logging |

When logs are insufficient, add instrumentation (see `instrumentation-points.md`).
