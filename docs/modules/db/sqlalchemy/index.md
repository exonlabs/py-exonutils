# db.sqlalchemy

`exonutils.db.sqlalchemy`

SQLAlchemy ORM integration. Provides an alternative `DBHandler` and
`BaseModel` built on top of SQLAlchemy's declarative system and
`scoped_session`. Supports SQLite, PostgreSQL, MySQL, and MS SQL Server.

**Requires:** `sqlalchemy`

## Modules

| Module | Contents |
|---|---|
| [handlers](handlers.md) | `DBHandler` — SQLAlchemy engine and session factory |
| [model](model.md) | `BaseModel` — SQLAlchemy declarative base with helpers |
| [utils](utils.md) | `interactive_config`, `interactive_setup` |
