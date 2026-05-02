# MySQL Backend

`exonutils.db.backends.mysql`

MySQL backend using the `mysqldb` driver.

**Requires:** `mysqlclient` (`pip install mysqlclient`)

## Engine

```python
from exonutils.db.backends.mysql.engine import Engine
engine = Engine()
```

### Options

| Key | Required | Description |
|---|---|---|
| `database` | yes | Database name |
| `host` | yes | Server hostname or IP |
| `port` | yes | Server port (typically `3306`) |
| `username` | yes | Login user |
| `password` | yes | Login password |
| `connect_timeout` | no | Default: `30` |

### Notes

- Connection charset: `utf8mb4`
- Default table engine: `InnoDB` (set via `table_args()`)

## interactive_config / interactive_setup

```python
from exonutils.db.backends.mysql.utils import interactive_config, interactive_setup

options = interactive_config(defaults={"host": "localhost", "port": 3306})
interactive_setup(options)
```
