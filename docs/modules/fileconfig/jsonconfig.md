# JsonFileConfig

`exonutils.fileconfig.jsonconfig.JsonFileConfig`

Stores configuration as a human-readable, indented JSON file.

## Constructor

```python
JsonFileConfig(file_path: str, defaults: dict = None)
```

## Behaviour

- `load()` — reads and parses the JSON file; merges with `defaults`; creates
  an empty buffer if the file does not exist
- `save()` — writes the buffer as pretty-printed JSON (`indent=2`)
- `dump()` — returns the raw JSON file contents as a string

## Example

```python
from exonutils.fileconfig.jsonconfig import JsonFileConfig

cfg = JsonFileConfig("/etc/myapp/config.json", defaults={
    "host": "localhost",
    "port": 8080,
    "db": {"backend": "sqlite"},
})

cfg.set("port", 9090)
cfg.set("db.backend", "pgsql")
cfg.save()

print(cfg.get("db.backend"))  # pgsql
```
