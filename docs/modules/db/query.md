# Query

`exonutils.db.query.Query`

Fluent query builder returned by `Session.query(model)` or `Model(dbs)`.
All filter/order/limit methods return `self` for chaining.

## Constructor

```python
Query(dbs: Session, model: BaseModel, table_name: str = None)
```

`table_name` overrides `model.table_name()`, allowing one model to map to
multiple tables.

## Builder Methods (chainable)

| Method | Description |
|---|---|
| `columns(*cols)` | Restrict SELECT to named columns |
| `filter(expr, *params)` | Append a raw WHERE clause fragment with positional params |
| `filterby(column, value)` | Append `AND column=$?` with the given value |
| `groupby(*cols)` | Set GROUP BY columns |
| `orderby(*exprs)` | Set ORDER BY — each expr must be `"col ASC"` or `"col DESC"` |
| `having(expr, param)` | Set HAVING clause |
| `limit(n)` | Limit result count |
| `offset(n)` | Skip first N rows |

## Execution Methods

| Method | Returns | Description |
|---|---|---|
| `all()` | `list[dict]` | All matching rows, with converters applied |
| `first()` | `dict` or `None` | First matching row (sets `LIMIT 1`) |
| `one()` | `dict` or `None` | Exactly one row; raises `ValueError` if multiple found |
| `get(guid)` | `dict` or `None` | Row by primary key `guid` |
| `count()` | `int` | Row count matching filters |
| `insert(data: dict)` | `str` (guid) | Inserts a row; auto-generates `guid` if missing; commits unless in transaction |
| `update(data: dict)` | `int` (rows affected) | Updates matching rows; commits unless in transaction |
| `delete()` | `int` (rows affected) | Deletes matching rows; commits unless in transaction |

## Example

```python
with dbh.session() as dbs:
    # fetch all active users ordered by name
    users = UserModel(dbs)\
        .filterby("active", 1)\
        .orderby("name ASC")\
        .all()

    # paginate
    page = UserModel(dbs).limit(20).offset(40).all()

    # insert inside transaction
    dbs.begin()
    guid = UserModel(dbs).insert({"name": "Bob", "email": "bob@example.com", "active": True})
    OrderModel(dbs).insert({"user_guid": guid, "total": 99.99})
    dbs.commit()

    # delete
    UserModel(dbs).filterby("active", 0).delete()
```
