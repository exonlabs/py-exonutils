# DBHandler (SQLAlchemy)

`exonutils.db.sqlalchemy.handlers.DBHandler`

SQLAlchemy-backed database handler. Builds a SQLAlchemy engine URL from the
options dict and manages a `scoped_session` factory.

## Constructor

```python
DBHandler(options: dict = {})
```

### Options

| Key | Description |
|---|---|
| `backend` | `"sqlite"`, `"pgsql"`, `"mysql"`, or `"mssql"` |
| `database` | Database name or file path |
| `host` | Server host |
| `port` | Server port |
| `username` | Login user |
| `password` | Login password |
| `connect_timeout` | Connection timeout (default: `30`) |
| `retries` | Retry count (default: `10`) |
| `retry_delay` | Seconds between retries (default: `0.5`) |

## Methods

### `init_engine(**kwargs)`

Creates the SQLAlchemy engine. Call this before the first `session()` if
you need custom pool settings.

| kwarg | Description |
|---|---|
| `pool` | Dict with `size`, `overflow`, `timeout`, `recycle` |
| `connect_timeout` | Override connect timeout |
| `query_timeout` | Statement timeout (PostgreSQL/MySQL/MSSQL) |

### `session() -> scoped_session`

Returns a SQLAlchemy session. Engine is initialised with `NullPool` on
first call if `init_engine()` was not called explicitly.

### `init_database(models, **kwargs)`

Creates all tables via `BaseModel.metadata.create_all()`, then calls
`model.upgrade_schema(dbs)` and `model.initialize_data(dbs)` for each model.

### `init_logging(level)`

Sets SQLAlchemy's log level. Defaults to `ERROR` to suppress query noise.

## Example

```python
from exonutils.db.sqlalchemy.handlers import DBHandler

dbh = DBHandler({
    "backend": "pgsql",
    "database": "myapp",
    "host": "localhost",
    "port": 5432,
    "username": "app",
    "password": "secret",
})
dbh.init_engine(pool={"size": 5, "overflow": 10})
dbh.init_database([UserModel])

with dbh.session() as dbs:
    users = dbs.query(UserModel).filter_by(active=True).all()
```
