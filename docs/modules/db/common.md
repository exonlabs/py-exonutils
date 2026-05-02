# db.common

`exonutils.db.common`

Utility functions used internally by the query builder and models.

## Functions

### `sql_identifier(name: str) -> str`

Validates that `name` contains only `[a-zA-Z0-9_]` and returns it
unchanged. Raises `ValueError` on invalid input.

```python
sql_identifier("user_name")   # "user_name"
sql_identifier("user; DROP")  # ValueError
```

### `data_mapping(mapper: dict, data: dict) -> dict`

Applies callable transformations from `mapper` to matching keys in `data`.
Used by `BaseModel.data_adapters()` and `data_converters()`.

```python
mapper = {"active": bool}
data_mapping(mapper, {"active": 1, "name": "Alice"})
# {"active": True, "name": "Alice"}
```

### `generate_guid() -> str`

Generates a 32-character hex GUID using `uuid.uuid5(uuid.uuid1(), uuid.uuid4().hex)`.
Used as the primary key for all model records.
