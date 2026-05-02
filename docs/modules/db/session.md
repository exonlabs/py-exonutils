# Session

`exonutils.db.session.Session`

Manages a single database connection and transaction lifecycle. Obtained
via `DBHandler.session()`. Supports use as a context manager.

## Constructor

```python
Session(dbh: DBHandler)
```

## Context Manager

```python
with dbh.session() as dbs:
    dbs.begin()
    dbs.execute("INSERT INTO ...")
    dbs.commit()
# connection closed automatically on exit
```

## Query Shorthand

```python
# These are equivalent:
dbs.query(MyModel)
dbs(MyModel)
```

Both return a [Query](query.md) instance.

## Connection Methods

| Method | Description |
|---|---|
| `connect()` | Opens connection if not already open |
| `close()` | Closes the connection and resets state |
| `is_connected()` | Returns `True` if connected |

## Transaction Methods

| Method | Description |
|---|---|
| `begin()` | Begins a transaction (`BEGIN;` or `BEGIN TRAN;` for MSSQL) |
| `commit()` | Commits the current transaction |
| `rollback()` | Rolls back the current transaction |
| `in_transaction()` | Returns `True` if inside a transaction |

## Execution Methods

| Method | Description |
|---|---|
| `execute(sql, params=None)` | Executes SQL with retry logic; raises `RuntimeError` on failure |
| `fetchall(sql, params=None)` | Executes SQL and returns all rows as `list[dict]` |
| `rowsaffected()` | Returns the row count from the last statement |

## SQL Placeholder

The session translates the application-level placeholder (`$?` by default)
to the backend's native placeholder (`?` for SQLite, `%s` for others) at
execution time.
