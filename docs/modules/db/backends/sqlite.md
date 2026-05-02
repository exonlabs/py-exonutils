# SQLite Backend

`exonutils.db.backends.sqlite`

SQLite backend using the stdlib `sqlite3` module. No additional driver
required.

## Engine

```python
from exonutils.db.backends.sqlite.engine import Engine
engine = Engine()
```

Calling `Engine()` registers all type adapters (see below).

### Options

| Key | Required | Description |
|---|---|---|
| `database` | yes | Absolute path to the `.db` file |
| `connect_timeout` | no | Default: `30` |
| `isolation_level` | no | SQLite isolation level; `None` for autocommit |
| `foreign_keys_constraints` | no | Default: `True` — enables `PRAGMA foreign_keys=ON` |

### Table Schema

- Adds `guid VARCHAR(32) NOT NULL PRIMARY KEY` if not present in `table_columns()`
- Supports `sqlite_without_rowid: True` (default) via `table_args()`
- Auto-creates `UNIQUE INDEX` for `PRIMARY` and `INDEX` constraint tokens
- Adds `CHECK (col IN (0,1))` for `BOOLEAN` columns

## Type Adapters

Registered automatically on `Engine()`:

| Python type | SQLite type | Notes |
|---|---|---|
| `bool` | `BOOLEAN` | Stored as `0`/`1` |
| `datetime` | `DATETIME` | ISO format `%Y-%m-%d %H:%M:%S.%f` |
| `date` | `DATE` | `%Y-%m-%d` |
| `time` | `TIME` | `%H:%M:%S.%f` |

`datetime_converter` handles multiple incoming formats flexibly.

## interactive_config / interactive_setup

```python
from exonutils.db.backends.sqlite.utils import interactive_config, interactive_setup

options = interactive_config(defaults={"database": "/var/db/app.db"})
# prompts: db path

interactive_setup(options)
# creates parent directories and touches the db file
```
