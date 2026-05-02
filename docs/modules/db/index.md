# db

Multi-backend SQL abstraction layer with an ORM-style query builder,
session management, and an optional SQLAlchemy integration.

## Architecture

```
DBHandler
  └── session() → Session
        └── query(Model) → Query
                            .filter().orderby().limit()
                            .all() / .first() / .one()
                            .insert() / .update() / .delete()
                            .count()
```

## Modules

| Module | Contents |
|---|---|
| [engine](engine.md) | `BaseEngine` — backend connection contract |
| [session](session.md) | `Session` — connection and transaction management |
| [handlers](handlers.md) | `DBHandler` — top-level database handle |
| [model](model.md) | `BaseModel` — table schema and data lifecycle |
| [query](query.md) | `Query` — fluent query builder |
| [common](common.md) | `sql_identifier`, `data_mapping`, `generate_guid` |
| [sqlalchemy/](sqlalchemy/index.md) | SQLAlchemy ORM integration |
| [backends/](backends/index.md) | SQLite, MySQL, PostgreSQL, MS SQL Server engines |

## Quick Start

```python
from exonutils.db.handlers import DBHandler
from exonutils.db.backends.sqlite.engine import Engine
from exonutils.db.model import BaseModel

class UserModel(BaseModel):
    @classmethod
    def table_name(cls): return "users"

    @classmethod
    def table_columns(cls):
        return [
            ("name", "TEXT NOT NULL"),
            ("email", "TEXT NOT NULL", "INDEX UNIQUE"),
        ]

engine = Engine()
dbh = DBHandler(engine, options={"database": "/var/db/app.db"})
dbh.init_database([UserModel])

with dbh.session() as dbs:
    dbs.begin()
    guid = UserModel(dbs).insert({"name": "Alice", "email": "alice@example.com"})
    dbs.commit()

with dbh.session() as dbs:
    user = UserModel(dbs).filterby("email", "alice@example.com").one()
    print(user)
```
