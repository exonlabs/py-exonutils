# BaseEngine

`exonutils.db.engine.BaseEngine`

Abstract contract that all backend engine implementations must satisfy.

## Class Attributes

| Attribute | Default | Description |
|---|---|---|
| `backend` | `""` | Backend identifier string (`"sqlite"`, `"pgsql"`, etc.) |
| `sql_placeholder` | `"?"` | SQL parameter placeholder |
| `Error` ... `NotSupportedError` | `Exception` | DB-API 2 exception classes, mapped per backend |

## Methods

| Method | Description |
|---|---|
| `connection(options) -> conn` | **Abstract** — returns a DB-API 2 connection |
| `post_connect(conn, options)` | Optional hook called after `connection()`; e.g. `PRAGMA` setup |
| `table_schema(model, **kwargs) -> list[str]` | **Abstract** — returns DDL statements for the model |

## Implementations

- [SQLite](backends/sqlite.md)
- [MySQL](backends/mysql.md)
- [PostgreSQL](backends/pgsql.md)
- [MS SQL Server](backends/mssql.md)
