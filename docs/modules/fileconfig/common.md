# BaseFileConfig

`exonutils.fileconfig.common.BaseFileConfig`

Abstract base providing the full key/value config interface. Subclasses
implement only `load()`, `save()`, and `dump()`.

## Constructor

```python
BaseFileConfig(file_path: str, defaults: dict = None)
```

Immediately calls `load(defaults=defaults)` on construction.

## Methods

| Method | Description |
|---|---|
| `keys()` | Returns top-level keys from the buffer |
| `get(key, default=None, decode=False)` | Read key; dot notation for nesting (`"a.b.c"`) |
| `set(key, value, encode=False)` | Write key; merges nested dicts for dotted keys |
| `delete(key)` | Deletes key; dot notation supported |
| `load(defaults=None)` | **Abstract** — reload buffer from file, merge with defaults |
| `save()` | **Abstract** — persist buffer to file |
| `dump()` | **Abstract** — return raw file contents |
| `purge()` | Clears buffer dict and deletes the file |

## Encoding

Values stored with `encode=True` are run through `_encode()` (base64 +
byte mangling) before writing. Read them back with `decode=True`.

Override `_mangle()` / `_demangle()` in a subclass for stronger obfuscation.

## Subclasses

- [JsonFileConfig](jsonconfig.md)
- [BlobFileConfig](blobconfig.md)
