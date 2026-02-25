# Safe Patterns

Online DDL patterns and zero-downtime migration techniques for PostgreSQL and MySQL.

---

## PostgreSQL Safe Patterns

### Add Nullable Column (Safe)

```sql
-- Safe: Instant, no table rewrite, no lock contention
ALTER TABLE users ADD COLUMN middle_name TEXT;
```

### Add Column with Default (PG 11+, Safe)

```sql
-- Safe in PG 11+: Instant, stores default in catalog
ALTER TABLE users ADD COLUMN status TEXT DEFAULT 'active';
```

### Add NOT NULL Constraint (Multi-Step, Safe)

```sql
-- Step 1: Add CHECK constraint as NOT VALID (instant, no scan)
ALTER TABLE users ADD CONSTRAINT users_email_not_null
  CHECK (email IS NOT NULL) NOT VALID;

-- Step 2: Validate in background (scans table, but allows concurrent access)
ALTER TABLE users VALIDATE CONSTRAINT users_email_not_null;

-- Step 3: Set NOT NULL using the validated constraint (instant)
ALTER TABLE users ALTER COLUMN email SET NOT NULL;

-- Step 4: Drop the redundant CHECK constraint
ALTER TABLE users DROP CONSTRAINT users_email_not_null;
```

### Create Index (Concurrently)

```sql
-- Safe: No lock contention, but slower and must be in its own transaction
CREATE INDEX CONCURRENTLY idx_users_email ON users(email);

-- IMPORTANT: Cannot be inside a transaction block
-- IMPORTANT: If it fails, it leaves an INVALID index. Clean up:
DROP INDEX CONCURRENTLY idx_users_email;
-- Then retry
```

### Add Foreign Key (Multi-Step)

```sql
-- Step 1: Add constraint NOT VALID (instant, no scan)
ALTER TABLE orders ADD CONSTRAINT fk_orders_user
  FOREIGN KEY (user_id) REFERENCES users(id) NOT VALID;

-- Step 2: Validate (scans table, allows concurrent access)
ALTER TABLE orders VALIDATE CONSTRAINT fk_orders_user;
```

### Rename Column

```sql
-- Safe but may break application code. Coordinate with deploy.
ALTER TABLE users RENAME COLUMN name TO full_name;
```

---

## MySQL Safe Patterns

### Add Column (INSTANT, MySQL 8.0.12+)

```sql
-- Safe: INSTANT, no table copy
ALTER TABLE users ADD COLUMN middle_name VARCHAR(100), ALGORITHM=INSTANT;
```

### Add Index (INPLACE)

```sql
-- Safe: INPLACE algorithm, allows concurrent DML
ALTER TABLE users ADD INDEX idx_email (email), ALGORITHM=INPLACE, LOCK=NONE;
```

### Online Schema Change Tools

For operations MySQL doesn't support online:

**pt-online-schema-change (Percona Toolkit):**
```bash
pt-online-schema-change --alter "MODIFY COLUMN name VARCHAR(500)" \
  --host=localhost --user=root D=mydb,t=users --execute
```

Process:
1. Creates shadow table with new schema
2. Copies data in chunks
3. Captures changes via triggers
4. Swaps tables atomically

**gh-ost (GitHub):**
```bash
gh-ost --alter="ADD COLUMN new_col INT" \
  --database=mydb --table=users \
  --host=localhost --execute
```

Process:
1. Creates ghost table with new schema
2. Copies data in chunks
3. Captures changes via binlog (no triggers)
4. Swaps tables atomically

---

## Multi-Step Migration Patterns

### Expand-Contract Pattern

For column renames or type changes without downtime:

```
Phase 1: EXPAND — Add new column, dual-write
Phase 2: MIGRATE — Backfill old data to new column
Phase 3: SWITCH — Application reads from new column
Phase 4: CONTRACT — Drop old column
```

```sql
-- Phase 1
ALTER TABLE users ADD COLUMN display_name TEXT;
-- Deploy: application writes to both `name` and `display_name`

-- Phase 2
UPDATE users SET display_name = name WHERE display_name IS NULL;
-- Do this in batches for large tables

-- Phase 3
-- Deploy: application reads from `display_name`

-- Phase 4
ALTER TABLE users DROP COLUMN name;
```

### Backfill in Batches

Never UPDATE entire table at once for large tables:

```sql
-- BAD: Locks entire table, long transaction
UPDATE users SET status = 'active' WHERE status IS NULL;

-- GOOD: Batch update
DO $$
DECLARE
  batch_size INT := 10000;
  updated INT := 1;
BEGIN
  WHILE updated > 0 LOOP
    UPDATE users SET status = 'active'
    WHERE id IN (
      SELECT id FROM users WHERE status IS NULL LIMIT batch_size
    );
    GET DIAGNOSTICS updated = ROW_COUNT;
    COMMIT;
    PERFORM pg_sleep(0.1);  -- Brief pause between batches
  END LOOP;
END $$;
```

---

## General Safety Rules

1. **Never run DDL in the same transaction as DML** in production
2. **Set lock timeout** to prevent indefinite blocking:
   ```sql
   SET lock_timeout = '5s';  -- Fail fast instead of blocking
   ```
3. **Run migrations during low-traffic periods** for any exclusive lock operation
4. **Test in staging with production-sized data** before production
5. **Always have a rollback plan** tested before executing
6. **Monitor connections** during migration — watch for connection pool exhaustion
