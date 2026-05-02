# DBHandler

`exonutils.db.handlers.DBHandler`

Top-level database handle. Holds the engine and connection options, creates
sessions, and orchestrates database initialisation.

## Constructor

```python
DBHandler(engine: BaseEngine, options: dict = {})
```

### Options

| Key | Default | Description |
|---|---|---|
| `database` | — | Database name or file path |
| `host` | — | Server host (non-SQLite backends) |
| `port` | — | Server port |
| `username` | — | Login username |
| `password` | — | Login password |
| `connect_timeout` | `30` | Connection timeout in seconds |
| `retries` | `10` | Execution retry attempts |
| `retry_delay` | `0.5` | Seconds between retries |
| `sql_placeholder` | `"$?"` | Application-level SQL placeholder |

## Methods

### `session() -> Session`

Returns a new [Session](session.md) instance bound to this handler.

### `init_database(models, **kwargs)`

Creates all tables from the model list and runs data initialisation:

1. Opens a session and begins a transaction
2. For each model: runs `engine.table_schema()` DDL statements, then
   `model.upgrade_schema(dbs)`
3. Commits
4. For each model: runs `model.initialize_data(dbs)`

## Example

```python
from exonutils.db.handlers import DBHandler
from exonutils.db.backends.pgsql.engine import Engine

engine = Engine()
dbh = DBHandler(engine, options={
    "database": "myapp",
    "host": "localhost",
    "port": 5432,
    "username": "app",
    "password": "secret",
})
dbh.init_database([UserModel, OrderModel])
```
