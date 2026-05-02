# db.backends

Backend-specific engine implementations for the native DB abstraction layer.

## Available Backends

| Backend | Module | Driver |
|---|---|---|
| [SQLite](sqlite.md) | `db.backends.sqlite` | stdlib `sqlite3` |
| [MySQL](mysql.md) | `db.backends.mysql` | `mysqldb` |
| [PostgreSQL](pgsql.md) | `db.backends.pgsql` | `psycopg2` |
| [MS SQL Server](mssql.md) | `db.backends.mssql` | `pymssql` |

Each backend exposes:

- `Engine` — implements [BaseEngine](../engine.md)
- `interactive_config(defaults={})` — prompts for connection parameters
- `interactive_setup(options)` — one-time DB setup (create file, test connection)
