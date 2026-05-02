# fileconfig

File-backed configuration with dot-notation key access, nested dict support,
and optional value encoding.

## Classes

| Class | Module | Description |
|---|---|---|
| [BaseFileConfig](common.md) | `fileconfig.common` | Abstract base — defines the config interface |
| [JsonFileConfig](jsonconfig.md) | `fileconfig.jsonconfig` | Human-readable JSON storage |
| [BlobFileConfig](blobconfig.md) | `fileconfig.blobconfig` | Binary blob storage with encoding |

## Common Interface

```python
cfg.keys()                       # top-level keys
cfg.get("key")                   # read key (supports dot notation)
cfg.get("section.key")           # nested read
cfg.set("section.key", value)    # nested write (merges into existing dict)
cfg.delete("key")                # delete key
cfg.load(defaults=None)          # reload from file, merge with defaults
cfg.save()                       # persist buffer to file
cfg.dump()                       # return raw file contents
cfg.purge()                      # clear buffer and delete file
```

### Encoded Values

`get()` and `set()` accept `decode=True` / `encode=True` for storing
opaque values (passwords, secrets) via the internal `_encode`/`_decode`
mechanism. Override `_mangle`/`_demangle` in subclasses for custom encoding.
