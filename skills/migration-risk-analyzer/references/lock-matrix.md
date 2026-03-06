# Lock Matrix

Operation-to-lock-type mapping for PostgreSQL and MySQL. Understanding which
operations acquire which locks determines migration risk.

---

## PostgreSQL Lock Types

### Table-Level Locks

| Lock Level          | Blocks                                     | Allowed Concurrent          |
| ------------------- | ------------------------------------------ | --------------------------- |
| ACCESS SHARE        | Nothing                                    | All except ACCESS EXCLUSIVE |
| ROW SHARE           | Nothing practical                          | Most operations             |
| ROW EXCLUSIVE       | Nothing practical                          | Most operations             |
| SHARE               | ROW EXCLUSIVE, EXCLUSIVE, ACCESS EXCLUSIVE | SELECT, ACCESS SHARE        |
| SHARE ROW EXCLUSIVE | ROW EXCLUSIVE and above                    | SELECT                      |
| EXCLUSIVE           | ROW SHARE and above                        | SELECT only                 |
| ACCESS EXCLUSIVE    | Everything                                 | Nothing                     |

### DDL Operations → Lock Types

| Operation                        | Lock Acquired           | Blocks Reads | Blocks Writes  | Duration                                   |
| -------------------------------- | ----------------------- | ------------ | -------------- | ------------------------------------------ |
| `SELECT`                         | ACCESS SHARE            | No           | No             | Query duration                             |
| `INSERT/UPDATE/DELETE`           | ROW EXCLUSIVE           | No           | No (row-level) | Transaction                                |
| `CREATE TABLE`                   | None on existing tables | No           | No             | Instant                                    |
| `CREATE INDEX`                   | SHARE                   | No           | Yes            | Full index build                           |
| `CREATE INDEX CONCURRENTLY`      | None effectively        | No           | No             | Full index build (slower)                  |
| `DROP TABLE`                     | ACCESS EXCLUSIVE        | Yes          | Yes            | Instant                                    |
| `DROP INDEX`                     | ACCESS EXCLUSIVE        | Yes          | Yes            | Instant                                    |
| `DROP INDEX CONCURRENTLY`        | None effectively        | No           | No             | Instant                                    |
| `ALTER TABLE ADD COLUMN`         | ACCESS EXCLUSIVE        | Yes          | Yes            | Instant (if nullable, no default rewrite)  |
| `ALTER TABLE ADD COLUMN DEFAULT` | ACCESS EXCLUSIVE        | Yes          | Yes            | Instant (PG 11+) or table rewrite (PG <11) |
| `ALTER TABLE DROP COLUMN`        | ACCESS EXCLUSIVE        | Yes          | Yes            | Instant (marks column as dropped)          |
| `ALTER TABLE ALTER TYPE`         | ACCESS EXCLUSIVE        | Yes          | Yes            | Table rewrite                              |
| `ALTER TABLE SET NOT NULL`       | ACCESS EXCLUSIVE        | Yes          | Yes            | Full table scan                            |
| `ALTER TABLE ADD CONSTRAINT`     | SHARE ROW EXCLUSIVE     | No           | Yes            | Full table scan                            |
| `VACUUM`                         | SHARE UPDATE EXCLUSIVE  | No           | No             | Duration varies                            |
| `REINDEX`                        | ACCESS EXCLUSIVE        | Yes          | Yes            | Full rebuild                               |
| `REINDEX CONCURRENTLY`           | None effectively        | No           | No             | Full rebuild (slower)                      |

### Key PostgreSQL Behaviors

1. **ADD COLUMN (nullable, no default):** Instant in all versions. Only updates catalog.
2. **ADD COLUMN WITH DEFAULT:** Instant in PG 11+. Table rewrite in PG 10-.
3. **ALTER TYPE:** Almost always rewrites the table. Very expensive on large tables.
4. **SET NOT NULL:** Requires scanning all rows to verify no NULLs. Can use `CHECK`
   constraint with `NOT VALID` + `VALIDATE` as a faster alternative.

---

## MySQL Lock Types (InnoDB)

### DDL Lock Behavior

MySQL DDL behavior depends on the version and operation:

| Operation            | MySQL 5.7                      | MySQL 8.0+                     | Lock Duration |
| -------------------- | ------------------------------ | ------------------------------ | ------------- |
| `ADD COLUMN`         | Table copy, blocks writes      | INSTANT or INPLACE             | Varies        |
| `DROP COLUMN`        | Table copy, blocks writes      | INPLACE, blocks writes         | Table copy    |
| `ADD INDEX`          | INPLACE, allows concurrent DML | INPLACE, allows concurrent DML | Full build    |
| `DROP INDEX`         | INPLACE, allows concurrent DML | INPLACE, allows concurrent DML | Instant       |
| `CHANGE COLUMN TYPE` | Table copy, blocks all         | Table copy, blocks all         | Table copy    |
| `RENAME COLUMN`      | INSTANT (8.0+)                 | INSTANT                        | Instant       |
| `ADD FOREIGN KEY`    | INPLACE, blocks writes briefly | INPLACE, blocks writes briefly | Full scan     |

### MySQL 8.0 INSTANT DDL

MySQL 8.0.12+ supports INSTANT for some operations:

```sql
-- Check if INSTANT is supported
ALTER TABLE users ADD COLUMN new_col INT, ALGORITHM=INSTANT;
-- If not supported, MySQL will error rather than falling back
```

| Operation                  | INSTANT Support (8.0) |
| -------------------------- | --------------------- |
| ADD COLUMN (at end)        | Yes                   |
| ADD COLUMN (at position)   | 8.0.29+               |
| DROP COLUMN                | 8.0.29+               |
| RENAME COLUMN              | Yes                   |
| SET DEFAULT                | Yes                   |
| MODIFY COLUMN (order only) | 8.0.29+               |

---

## Lock Duration Estimation

### Instant Operations (< 1 second)

- PostgreSQL: ADD nullable column, DROP column, RENAME
- MySQL 8.0: ADD COLUMN (INSTANT), RENAME, SET DEFAULT

### Table Scan Operations

Duration proportional to table size:

| Table Size | Estimated Duration |
| ---------- | ------------------ |
| < 10K rows | < 1 second         |
| 10K - 100K | 1-10 seconds       |
| 100K - 1M  | 10-60 seconds      |
| 1M - 10M   | 1-10 minutes       |
| 10M - 100M | 10-60 minutes      |
| > 100M     | Hours              |

Factors: disk speed, CPU, concurrent load, row width.

### Table Rewrite Operations

Full table copy — 2x the storage during operation:

| Table Size | Estimated Duration | Extra Storage |
| ---------- | ------------------ | ------------- |
| < 1M       | < 1 minute         | < 1 GB        |
| 1M - 10M   | 1-15 minutes       | 1-10 GB       |
| 10M - 100M | 15-120 minutes     | 10-100 GB     |
| > 100M     | Hours              | 100+ GB       |

---

## Lock Wait Impact

When an exclusive lock is acquired, concurrent queries queue behind it:

```text
Time:  0s     5s     10s    15s    20s
Lock:  |----EXCLUSIVE LOCK----|
Query: |----blocked-----------|---runs----|
Query:     |----blocked-------|---runs----|
Query:         |--blocked-----|---runs----|
```

Impact depends on:

- Lock duration (seconds vs minutes)
- Query rate (100/sec vs 10/sec)
- Connection pool size (blocked connections fill the pool)
- Client timeout settings (connections may timeout and retry, amplifying load)
