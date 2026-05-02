# BaseModel (SQLAlchemy)

`exonutils.db.sqlalchemy.model.BaseModel`

SQLAlchemy declarative base with a built-in `guid` primary key and
CRUD class methods.

## Columns

| Column | Type | Notes |
|---|---|---|
| `guid` | `String(32)` | Primary key, unique, non-autoincrement |

Define additional columns as `sa.Column(...)` class attributes in subclasses.

## Class Methods

### `create(dbs, data: dict) -> str`

Inserts a new record. Auto-generates `guid` if not in `data`. Commits
unless inside a nested transaction. Returns the `guid`.

### `update(query, data: dict) -> int`

Updates records matching `query`. Removes `guid` from `data` before update.
Commits unless in nested transaction. Returns rows affected.

### `delete(query) -> int`

Deletes records matching `query`. Returns rows affected.

### `upgrade_schema(dbs, **kwargs)`

Override for schema migration logic called during `init_database`.

### `initialize_data(dbs, **kwargs)`

Override for seeding initial rows called during `init_database`.

## Example

```python
import sqlalchemy as sa
from exonutils.db.sqlalchemy.model import BaseModel

class UserModel(BaseModel):
    __tablename__ = "users"

    name  = sa.Column(sa.String(128), nullable=False)
    email = sa.Column(sa.String(256), nullable=False, unique=True)
    active = sa.Column(sa.Boolean, nullable=False, default=True)

    @classmethod
    def initialize_data(cls, dbs, **kwargs):
        cls.create(dbs, {"name": "admin", "email": "admin@localhost", "active": True})
```
