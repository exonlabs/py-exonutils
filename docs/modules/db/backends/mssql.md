# MS SQL Server Backend

`exonutils.db.backends.mssql`

Microsoft SQL Server backend using the `pymssql` driver.

**Requires:** `pymssql` (`pip install pymssql`)

## Engine

```python
from exonutils.db.backends.mssql.engine import Engine
engine = Engine()
```

### Options

| Key | Required | Description |
|---|---|---|
| `database` | yes | Database name |
| `host` | yes | Server hostname or IP |
| `port` | yes | Server port (typically `1433`) |
| `username` | yes | Login user |
| `password` | yes | Login password |
| `connect_timeout` | no | Default: `30` |

### Notes

- Connection charset: `utf8`
- Transactions use `BEGIN TRAN` / `COMMIT TRAN` / `ROLLBACK TRAN`
- `LIMIT`/`OFFSET` translated to `TOP(n)` / `OFFSET n ROWS FETCH NEXT n ROWS ONLY`
- SQL placeholder: `%s`

## interactive_config / interactive_setup

```python
from exonutils.db.backends.mssql.utils import interactive_config, interactive_setup

options = interactive_config(defaults={"host": "localhost", "port": 1433})
interactive_setup(options)
```
