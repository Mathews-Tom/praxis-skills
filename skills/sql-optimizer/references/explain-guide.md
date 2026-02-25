# EXPLAIN Guide

Reading and interpreting EXPLAIN output for PostgreSQL, MySQL, and SQLite.

---

## PostgreSQL EXPLAIN

### Running EXPLAIN

```sql
-- Plan only (no execution)
EXPLAIN SELECT * FROM users WHERE email = 'alice@example.com';

-- Plan with actual execution statistics
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'alice@example.com';

-- Verbose with all details
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT) SELECT ...;
```

### Reading the Output

```
Seq Scan on users  (cost=0.00..1234.00 rows=1 width=64) (actual time=0.015..8.234 rows=1 loops=1)
  Filter: (email = 'alice@example.com'::text)
  Rows Removed by Filter: 99999
```

| Field | Meaning |
|-------|---------|
| `Seq Scan` | Scan type (see below) |
| `cost=0.00..1234.00` | Estimated startup..total cost (arbitrary units) |
| `rows=1` | Estimated result rows |
| `width=64` | Estimated row width in bytes |
| `actual time=0.015..8.234` | Real time in ms (with ANALYZE) |
| `rows=1` | Actual rows returned (with ANALYZE) |
| `loops=1` | How many times this node executed |
| `Rows Removed by Filter: 99999` | Rows scanned but not returned |

### Scan Types (Best to Worst)

| Scan Type | Performance | Meaning |
|-----------|-------------|---------|
| Index Only Scan | Best | All data from index, no table access |
| Index Scan | Good | Index finds rows, fetches from table |
| Bitmap Index Scan | Good | Multiple index conditions combined |
| Seq Scan | Bad (on large tables) | Reads every row in the table |

### Join Types

| Join Type | When Used | Performance |
|-----------|-----------|-------------|
| Nested Loop | Small tables, indexed inner | Best for small result sets |
| Hash Join | Equi-joins, unindexed | Good for medium result sets |
| Merge Join | Pre-sorted data, equi-joins | Good for large sorted sets |

### Red Flags in EXPLAIN

| Red Flag | Meaning | Fix |
|----------|---------|-----|
| Seq Scan on large table | No useful index | Add index for WHERE/JOIN columns |
| `rows=1` estimated, `rows=100000` actual | Stale statistics | Run `ANALYZE tablename` |
| Sort with large cost | No index for ORDER BY | Add index matching sort order |
| Hash/Merge with `Batches > 1` | Insufficient `work_mem` | Increase `work_mem` or add index |
| Nested Loop with large outer table | Missing index on inner table | Add index on join column |

---

## MySQL EXPLAIN

### Running EXPLAIN

```sql
EXPLAIN SELECT * FROM users WHERE email = 'alice@example.com';
EXPLAIN FORMAT=JSON SELECT ...;  -- Detailed JSON output
EXPLAIN ANALYZE SELECT ...;      -- MySQL 8.0.18+, actual execution
```

### Key Columns

| Column | Meaning | Watch For |
|--------|---------|-----------|
| `type` | Access type | `ALL` = full scan (bad) |
| `possible_keys` | Indexes that might be used | `NULL` = no index available |
| `key` | Index actually used | `NULL` = no index used |
| `rows` | Estimated rows to examine | Large number on filtered query |
| `Extra` | Additional info | `Using filesort`, `Using temporary` |

### Access Types (Best to Worst)

| Type | Meaning | Performance |
|------|---------|-------------|
| `system` | Table has one row | Best |
| `const` | Primary key or unique index lookup | Excellent |
| `eq_ref` | One row per join (unique key) | Excellent |
| `ref` | Non-unique index lookup | Good |
| `range` | Index range scan | Good |
| `index` | Full index scan | Fair |
| `ALL` | Full table scan | Bad |

### Red Flags

| Extra Value | Meaning | Fix |
|-------------|---------|-----|
| `Using filesort` | Sort without index | Add index matching ORDER BY |
| `Using temporary` | Temporary table created | Optimize GROUP BY or DISTINCT |
| `Using where` with `type=ALL` | Full scan with filter | Add index for WHERE condition |
| `Using join buffer` | No index for join | Add index on join column |

---

## SQLite EXPLAIN

### Running EXPLAIN

```sql
EXPLAIN QUERY PLAN SELECT * FROM users WHERE email = 'alice@example.com';
```

### Output Format

```
QUERY PLAN
|--SCAN users
```

vs.

```
QUERY PLAN
|--SEARCH users USING INDEX idx_users_email (email=?)
```

| Keyword | Meaning |
|---------|---------|
| `SCAN` | Full table scan — no index used |
| `SEARCH ... USING INDEX` | Index lookup — good |
| `USING COVERING INDEX` | Index-only scan — best |
| `USE TEMP B-TREE` | Sort without index |

---

## Common EXPLAIN Patterns

### Pattern: Index Not Used Despite Existing

```sql
-- Index exists on users(email) but this does Seq Scan:
SELECT * FROM users WHERE LOWER(email) = 'alice@example.com';
```

The function `LOWER()` prevents index use. Create a functional index or rewrite.

### Pattern: Estimated vs Actual Row Mismatch

```
Index Scan (rows=10) (actual rows=50000)
```

Statistics are stale. Run `ANALYZE` (PostgreSQL) or `ANALYZE TABLE` (MySQL).

### Pattern: Nested Loop with High Cost

```
Nested Loop (cost=0..500000)
  -> Seq Scan on orders (rows=100000)
  -> Index Scan on users (rows=1)
```

The outer table (orders) has no filter. The nested loop runs 100K index lookups.
Add a filter on orders or restructure the query.
