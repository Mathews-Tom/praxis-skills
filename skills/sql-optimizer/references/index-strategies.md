# Index Strategies

Index type selection, composite index column ordering, covering indexes, and
maintenance considerations.

---

## Index Types

| Type | Supports | Use When |
|------|---------|----------|
| B-tree (default) | `=`, `<`, `>`, `<=`, `>=`, `BETWEEN`, `LIKE 'prefix%'` | Default for most columns |
| Hash | `=` only | Equality lookups only (PostgreSQL) |
| GIN | Array containment, full-text search, JSONB | `@>`, `@@`, `?` operators |
| GiST | Range types, geometric, full-text | Overlaps, nearest-neighbor |
| BRIN | Range queries on naturally ordered data | Timestamp columns in append-only tables |

### B-tree (Default Choice)

```sql
CREATE INDEX idx_users_email ON users(email);
```

Appropriate for 90%+ of indexes. Supports equality and range queries.

### Composite (Multi-Column) Index

```sql
CREATE INDEX idx_orders_user_status ON orders(user_id, status);
```

**Column order matters.** The index is usable for queries that filter on:
- `user_id` alone ✅
- `user_id` AND `status` ✅
- `status` alone ❌ (leftmost prefix rule)

**Rule:** Put the most selective column first. If `user_id` has higher cardinality
(more distinct values) than `status`, put `user_id` first.

**Exception:** If one column is always `=` and another is a range (`<`, `>`), put
the `=` column first regardless of cardinality.

```sql
-- Query: WHERE status = 'active' AND created_at > '2026-01-01'
-- Best index: (status, created_at) — equality first, range second
CREATE INDEX idx_orders_status_created ON orders(status, created_at);
```

---

## Covering Indexes

A covering index includes all columns the query needs, avoiding a table lookup.

```sql
-- Query only needs email and name
SELECT email, name FROM users WHERE email = 'alice@example.com';

-- Covering index — no table access needed
CREATE INDEX idx_users_email_name ON users(email) INCLUDE (name);  -- PostgreSQL
CREATE INDEX idx_users_email_name ON users(email, name);            -- MySQL
```

**When to use:** High-frequency queries that read few columns. The INCLUDE clause
(PostgreSQL) adds columns to the index leaf without affecting index ordering.

---

## Partial Indexes

Index only a subset of rows. Smaller index = faster scans + less storage.

```sql
-- Only index active users (80% of queries filter on active users)
CREATE INDEX idx_users_active_email ON users(email) WHERE active = true;
```

**When to use:** A significant portion of queries filter on a common condition.

---

## Index Selection Guide

### From WHERE Clause

| WHERE Pattern | Index Recommendation |
|--------------|---------------------|
| `WHERE col = value` | Single-column index on `col` |
| `WHERE col1 = v1 AND col2 = v2` | Composite index `(col1, col2)` |
| `WHERE col1 = v1 AND col2 > v2` | Composite `(col1, col2)` — equality first |
| `WHERE col IN (v1, v2, v3)` | Single-column index on `col` |
| `WHERE col LIKE 'prefix%'` | B-tree index on `col` |
| `WHERE col IS NOT NULL` | Partial index `WHERE col IS NOT NULL` |

### From JOIN Clause

```sql
-- Always index the foreign key column used in JOINs
SELECT * FROM orders o JOIN users u ON u.id = o.user_id;
-- Index needed: orders(user_id)
```

### From ORDER BY Clause

```sql
-- Index matching ORDER BY avoids sort operation
SELECT * FROM logs ORDER BY created_at DESC LIMIT 100;
-- Index needed: logs(created_at DESC)
```

### From GROUP BY Clause

```sql
-- Index on GROUP BY columns enables streaming aggregation
SELECT status, COUNT(*) FROM orders GROUP BY status;
-- Index: orders(status)
```

---

## When NOT to Index

| Scenario | Why |
|----------|-----|
| Small tables (< 1000 rows) | Full scan is faster than index lookup |
| Columns with very low cardinality | Boolean columns (true/false) — index doesn't help much |
| Columns rarely queried in WHERE | Index overhead without benefit |
| Tables with heavy write load | Each write updates every index |
| Temporary/staging tables | Short-lived data doesn't benefit |

---

## Index Maintenance

### Monitoring Index Usage

```sql
-- PostgreSQL: Find unused indexes
SELECT schemaname, tablename, indexname, idx_scan
FROM pg_stat_user_indexes
WHERE idx_scan = 0
ORDER BY pg_relation_size(indexrelid) DESC;
```

### Index Bloat

Over time, B-tree indexes accumulate dead tuples. Rebuild periodically:

```sql
-- PostgreSQL: Non-blocking rebuild
REINDEX INDEX CONCURRENTLY idx_users_email;

-- MySQL: Rebuild
ALTER TABLE users DROP INDEX idx_email, ADD INDEX idx_email(email);
```

### Index Size

```sql
-- PostgreSQL: Index sizes
SELECT indexname, pg_size_pretty(pg_relation_size(indexname::regclass))
FROM pg_indexes WHERE tablename = 'users';
```

Keep total index size reasonable. Rule of thumb: index storage should not exceed
2-3x the table data storage.
