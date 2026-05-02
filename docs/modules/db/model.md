# BaseModel

`exonutils.db.model.BaseModel`

Base class for all database table models. Defines the schema, data
lifecycle hooks, and a shorthand for creating query instances.

## Constructor Shorthand

`BaseModel` uses `__new__` to return a [Query](query.md) instance directly:

```python
query = MyModel(dbs)            # equivalent to dbs.query(MyModel)
query = MyModel(dbs, table_name="alt_table")
```

## Class Methods to Override

### `table_name() -> str` *(required)*

Returns the SQL table name.

```python
@classmethod
def table_name(cls): return "users"
```

### `table_columns() -> list` *(required)*

Returns a list of column definitions. Each item is a tuple:
`(name, definition)` or `(name, definition, constraint)`.

```python
@classmethod
def table_columns(cls):
    return [
        ("name",  "TEXT NOT NULL"),
        ("email", "TEXT NOT NULL", "INDEX UNIQUE"),
        ("active","BOOLEAN NOT NULL"),
    ]
```

Valid constraint tokens: `PRIMARY`, `UNIQUE`, `INDEX`.

### `table_args() -> dict`

Backend-specific table options:

| Key | Description |
|---|---|
| `sqlite_without_rowid` | `True` — create WITHOUT ROWID (SQLite) |
| `mysql_engine` | `"InnoDB"` — storage engine (MySQL) |

### `table_constraints() -> list[str]`

Additional SQL constraint expressions appended to the CREATE TABLE.

### `default_orderby() -> list[str]`

Default ORDER BY applied to all queries on this model.

### `data_adapters() -> dict`

Callables applied to column values **before insert/update** (Python → DB).

### `data_converters() -> dict`

Callables applied to column values **after fetch** (DB → Python).

### `upgrade_schema(dbs, **kwargs)`

Called during `init_database` inside a transaction. Use for ALTER TABLE
migrations.

### `initialize_data(dbs, **kwargs)`

Called during `init_database` after commit. Use for seeding initial rows.

## Example

```python
from exonutils.db.model import BaseModel

class UserModel(BaseModel):

    @classmethod
    def table_name(cls): return "users"

    @classmethod
    def table_columns(cls):
        return [
            ("name",  "TEXT NOT NULL"),
            ("email", "TEXT NOT NULL", "INDEX UNIQUE"),
            ("active","BOOLEAN NOT NULL"),
        ]

    @classmethod
    def data_adapters(cls):
        return {"active": lambda v: 1 if v else 0}

    @classmethod
    def data_converters(cls):
        return {"active": lambda v: bool(v)}

    @classmethod
    def initialize_data(cls, dbs, **kwargs):
        cls(dbs).insert({"name": "admin", "email": "admin@localhost", "active": True})
```
