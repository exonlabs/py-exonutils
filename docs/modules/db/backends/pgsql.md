# PostgreSQL Backend

`exonutils.db.backends.pgsql`

PostgreSQL backend using the `psycopg2` driver.

**Requires:** `psycopg2` (`pip install psycopg2-binary`)

## Engine

```python
from exonutils.db.backends.pgsql.engine import Engine
engine = Engine()
```

### Options

| Key | Required | Description |
|---|---|---|
| `database` | yes | Database name |
| `host` | yes | Server hostname or IP |
| `port` | yes | Server port (typically `5432`) |
| `username` | yes | Login user |
| `password` | yes | Login password |
| `connect_timeout` | no | Default: `30` |

### Notes

- Connection charset: `utf8`
- SQL placeholder: `%s`

## interactive_config / interactive_setup

```python
from exonutils.db.backends.pgsql.utils import interactive_config, interactive_setup

options = interactive_config(defaults={"host": "localhost", "port": 5432})
interactive_setup(options)
```
