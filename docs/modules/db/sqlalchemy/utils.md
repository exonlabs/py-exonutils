# db.sqlalchemy.utils

`exonutils.db.sqlalchemy.utils`

Interactive console helpers for configuring and initialising a database
backend. Delegates to the corresponding `db.backends.<backend>.utils`
module.

## Functions

### `interactive_config(backend: str, defaults: dict = {}) -> dict`

Prompts the user for connection parameters for `backend`. Returns a complete
options dict with `backend` set.

Supported backends: `"sqlite"`, `"pgsql"`, `"mysql"`, `"mssql"`.

```python
from exonutils.db.sqlalchemy.utils import interactive_config

options = interactive_config("pgsql", defaults={"host": "localhost"})
# prompts: host, port, database, username, password
```

### `interactive_setup(backend: str, options: dict) -> bool`

Runs one-time database setup (e.g. create the SQLite file, verify
connectivity for server backends). Returns `True` on success.

```python
from exonutils.db.sqlalchemy.utils import interactive_setup

interactive_setup("sqlite", {"database": "/var/db/app.db"})
```
