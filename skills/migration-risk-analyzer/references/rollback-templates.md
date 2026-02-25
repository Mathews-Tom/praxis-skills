# Rollback Templates

Rollback scripts for common DDL operations and data migration patterns.

---

## DDL Rollback Templates

### ADD COLUMN → DROP COLUMN

```sql
-- Forward
ALTER TABLE users ADD COLUMN middle_name TEXT;

-- Rollback
ALTER TABLE users DROP COLUMN middle_name;
```

**Risk:** If application code has already written data to the new column, that data
is lost on rollback.

### DROP COLUMN (IRREVERSIBLE)

```sql
-- Forward
ALTER TABLE users DROP COLUMN legacy_field;

-- Rollback: IMPOSSIBLE — data is destroyed
-- Mitigation: Backup before dropping
CREATE TABLE users_backup_legacy_field AS
  SELECT id, legacy_field FROM users;

-- After drop, if rollback needed:
ALTER TABLE users ADD COLUMN legacy_field TEXT;
UPDATE users u SET legacy_field = b.legacy_field
  FROM users_backup_legacy_field b WHERE b.id = u.id;
```

### ADD INDEX → DROP INDEX

```sql
-- Forward
CREATE INDEX CONCURRENTLY idx_users_email ON users(email);

-- Rollback
DROP INDEX CONCURRENTLY idx_users_email;
```

**Risk:** None — indexes don't affect data correctness.

### DROP INDEX (Reversible)

```sql
-- Forward
DROP INDEX idx_users_email;

-- Rollback
CREATE INDEX CONCURRENTLY idx_users_email ON users(email);
```

**Risk:** Recreating the index takes time. Queries may be slow during rebuild.

### DROP TABLE (IRREVERSIBLE)

```sql
-- Forward
DROP TABLE legacy_table;

-- Rollback: IMPOSSIBLE — table and data destroyed
-- Mitigation: Rename instead of drop
ALTER TABLE legacy_table RENAME TO legacy_table_deprecated;
-- Wait 30 days, then DROP if no issues

-- Or backup first
CREATE TABLE legacy_table_backup AS SELECT * FROM legacy_table;
DROP TABLE legacy_table;
```

### RENAME TABLE

```sql
-- Forward
ALTER TABLE old_name RENAME TO new_name;

-- Rollback
ALTER TABLE new_name RENAME TO old_name;
```

### RENAME COLUMN

```sql
-- Forward
ALTER TABLE users RENAME COLUMN name TO full_name;

-- Rollback
ALTER TABLE users RENAME COLUMN full_name TO name;
```

**Risk:** Application code referencing the old column name will break between
forward and rollback.

### ALTER COLUMN TYPE

```sql
-- Forward: Widen from VARCHAR(50) to VARCHAR(200)
ALTER TABLE users ALTER COLUMN name TYPE VARCHAR(200);

-- Rollback: Narrow back (may fail if data exceeds 50 chars)
ALTER TABLE users ALTER COLUMN name TYPE VARCHAR(50);
```

**Risk:** Narrowing may fail if data now exceeds the old limit. Test rollback
with production data.

### ADD NOT NULL CONSTRAINT

```sql
-- Forward
ALTER TABLE users ALTER COLUMN email SET NOT NULL;

-- Rollback
ALTER TABLE users ALTER COLUMN email DROP NOT NULL;
```

### ADD FOREIGN KEY

```sql
-- Forward
ALTER TABLE orders ADD CONSTRAINT fk_orders_user
  FOREIGN KEY (user_id) REFERENCES users(id);

-- Rollback
ALTER TABLE orders DROP CONSTRAINT fk_orders_user;
```

### ADD CHECK CONSTRAINT

```sql
-- Forward
ALTER TABLE orders ADD CONSTRAINT chk_positive_total
  CHECK (total >= 0);

-- Rollback
ALTER TABLE orders DROP CONSTRAINT chk_positive_total;
```

---

## Data Migration Rollback

### UPDATE with Backup

```sql
-- Before migration: save old values
CREATE TABLE users_backup_status AS
  SELECT id, status FROM users;

-- Forward
UPDATE users SET status = 'active' WHERE status = 'enabled';

-- Rollback
UPDATE users u SET status = b.status
  FROM users_backup_status b WHERE b.id = u.id;

-- Cleanup (after confirmed success)
DROP TABLE users_backup_status;
```

### INSERT Rollback

```sql
-- Forward: Insert new default rows
INSERT INTO settings (key, value, created_at)
VALUES ('feature_x', 'true', NOW());

-- Rollback: Delete inserted rows
DELETE FROM settings WHERE key = 'feature_x';
```

### DELETE with Backup (IRREVERSIBLE without backup)

```sql
-- Before migration: backup
CREATE TABLE deleted_users_backup AS
  SELECT * FROM users WHERE status = 'deleted';

-- Forward
DELETE FROM users WHERE status = 'deleted';

-- Rollback
INSERT INTO users SELECT * FROM deleted_users_backup;
```

---

## Rollback Testing Protocol

1. **Run forward migration in staging**
2. **Verify application works with new schema**
3. **Run rollback script in staging**
4. **Verify application works with original schema**
5. **Run forward migration again** to confirm it's idempotent
6. **Document rollback time** — how long does rollback take on staging-sized data?

If rollback takes longer than your acceptable downtime window, consider alternative
migration strategies (expand-contract, blue-green).
