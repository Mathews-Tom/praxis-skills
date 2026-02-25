# Validation Queries

Pre and post-migration validation SQL templates for verifying migration success
and data integrity.

---

## Pre-Migration Checks

### Table Size and Row Count

```sql
-- PostgreSQL: Table size and estimated row count
SELECT
  relname AS table_name,
  pg_size_pretty(pg_total_relation_size(relid)) AS total_size,
  n_live_tup AS estimated_rows
FROM pg_stat_user_tables
WHERE relname IN ('users', 'orders')
ORDER BY pg_total_relation_size(relid) DESC;

-- MySQL: Table size and row count
SELECT
  TABLE_NAME,
  ROUND(DATA_LENGTH / 1024 / 1024, 2) AS data_mb,
  TABLE_ROWS AS estimated_rows
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA = DATABASE()
  AND TABLE_NAME IN ('users', 'orders');
```

### Active Connections and Locks

```sql
-- PostgreSQL: Check for active locks on target tables
SELECT
  pid,
  usename,
  query_start,
  state,
  LEFT(query, 100) AS query
FROM pg_stat_activity
WHERE state != 'idle'
  AND query ILIKE '%users%'
ORDER BY query_start;

-- PostgreSQL: Check for blocking locks
SELECT
  blocked.pid AS blocked_pid,
  blocking.pid AS blocking_pid,
  blocked.query AS blocked_query,
  blocking.query AS blocking_query
FROM pg_stat_activity blocked
JOIN pg_locks bl ON bl.pid = blocked.pid
JOIN pg_locks bkl ON bkl.locktype = bl.locktype
  AND bkl.database IS NOT DISTINCT FROM bl.database
  AND bkl.relation IS NOT DISTINCT FROM bl.relation
  AND bkl.pid != bl.pid
JOIN pg_stat_activity blocking ON blocking.pid = bkl.pid
WHERE NOT bl.granted;
```

### Current Schema Snapshot

```sql
-- PostgreSQL: Capture current column definitions
SELECT
  column_name,
  data_type,
  is_nullable,
  column_default
FROM information_schema.columns
WHERE table_name = 'users'
ORDER BY ordinal_position;

-- Capture current indexes
SELECT
  indexname,
  indexdef
FROM pg_indexes
WHERE tablename = 'users';

-- Capture current constraints
SELECT
  conname AS constraint_name,
  contype AS constraint_type,
  pg_get_constraintdef(oid) AS definition
FROM pg_constraint
WHERE conrelid = 'users'::regclass;
```

---

## Post-Migration Structural Checks

### Verify Column Exists/Removed

```sql
-- Verify new column exists
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'users'
  AND column_name = 'new_column';
-- Expected: 1 row

-- Verify old column removed
SELECT column_name
FROM information_schema.columns
WHERE table_name = 'users'
  AND column_name = 'removed_column';
-- Expected: 0 rows
```

### Verify Index Exists

```sql
-- PostgreSQL
SELECT indexname, indexdef
FROM pg_indexes
WHERE tablename = 'users'
  AND indexname = 'idx_users_email';
-- Expected: 1 row

-- Verify index is valid (not partial build failure)
SELECT indexrelid::regclass AS index_name, indisvalid
FROM pg_index
WHERE indexrelid = 'idx_users_email'::regclass;
-- Expected: indisvalid = true
```

### Verify Constraint

```sql
-- PostgreSQL
SELECT conname, pg_get_constraintdef(oid)
FROM pg_constraint
WHERE conrelid = 'users'::regclass
  AND conname = 'fk_users_org';
-- Expected: 1 row with correct definition
```

---

## Post-Migration Data Integrity Checks

### Row Count Verification

```sql
-- Compare row count before and after
-- (Record the "before" count pre-migration)
SELECT COUNT(*) AS row_count FROM users;
-- Expected: Same as pre-migration (for DDL-only migrations)
```

### NULL Check After NOT NULL Migration

```sql
-- Verify no NULLs exist after adding NOT NULL constraint
SELECT COUNT(*) AS null_count
FROM users
WHERE email IS NULL;
-- Expected: 0
```

### Data Backfill Verification

```sql
-- Verify backfill completed
SELECT
  COUNT(*) AS total,
  COUNT(new_column) AS populated,
  COUNT(*) - COUNT(new_column) AS remaining
FROM users;
-- Expected: remaining = 0
```

### Foreign Key Integrity

```sql
-- Verify no orphaned foreign keys
SELECT o.id, o.user_id
FROM orders o
LEFT JOIN users u ON u.id = o.user_id
WHERE u.id IS NULL;
-- Expected: 0 rows (no orphans)
```

### Constraint Validation

```sql
-- Verify CHECK constraint holds for all rows
SELECT COUNT(*) AS violations
FROM orders
WHERE total < 0;
-- Expected: 0 (if CHECK total >= 0 was added)
```

---

## Application-Level Checks

After migration, verify application behavior:

```sql
-- Verify a representative query still works
EXPLAIN ANALYZE
SELECT id, name, email FROM users WHERE email = 'test@example.com';
-- Check: Uses expected index, reasonable execution time

-- Verify write operations work
BEGIN;
INSERT INTO users (name, email) VALUES ('test', 'test@example.com');
ROLLBACK;
-- Expected: No errors
```

---

## Monitoring Queries (During Migration)

```sql
-- PostgreSQL: Monitor lock waits during migration
SELECT
  pid,
  wait_event_type,
  wait_event,
  state,
  LEFT(query, 80) AS query,
  NOW() - query_start AS duration
FROM pg_stat_activity
WHERE wait_event_type = 'Lock'
ORDER BY duration DESC;

-- Monitor table access during migration
SELECT
  relname,
  seq_scan,
  idx_scan,
  n_tup_ins,
  n_tup_upd,
  n_tup_del
FROM pg_stat_user_tables
WHERE relname = 'users';
```
