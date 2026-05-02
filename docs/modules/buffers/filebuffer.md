# SimpleFileBuffer

`exonutils.buffers.filebuffer.SimpleFileBuffer`

File-backed key/value buffer. Each key is stored as a JSON file inside a
directory. Defaults to the system temp directory when no base path is given.

## Constructor

```python
SimpleFileBuffer(name: str, base_path: str = '')
```

- `name` — buffer directory name
- `base_path` — parent directory; defaults to `tempfile.gettempdir()`

The buffer directory is created on first `set()` call.

## Methods

Inherits the full [BaseBuffer](common.md) interface.

| Method | Notes |
|---|---|
| `keys()` | Returns filenames in the buffer directory |
| `get(key, default=None)` | Reads and JSON-decodes the key file; raises `ValueError` on invalid key |
| `set(key, value)` | JSON-encodes and writes the key file; creates directory if needed |
| `delete(key)` | Removes the key file if it exists |
| `purge()` | Removes the entire buffer directory |

## Example

```python
from exonutils.buffers.filebuffer import SimpleFileBuffer

buf = SimpleFileBuffer("myapp-buf", base_path="/var/run")
buf.set("status", {"running": True, "pid": 1234})
print(buf.get("status"))   # {'running': True, 'pid': 1234}
buf.delete("status")
buf.purge()
```
