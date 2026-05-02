# BaseBuffer

`exonutils.buffers.common.BaseBuffer`

Abstract base class defining the interface all buffer implementations must
satisfy.

## Interface

```python
class BaseBuffer:
    def keys(self) -> list: ...
    def items(self) -> list: ...
    def get(self, key, default=None): ...
    def set(self, key, value): ...
    def delete(self, key): ...
    def purge(self): ...
    def reset(self, defaults=None, clean=True): ...
```

### `reset(defaults=None, clean=True)`

Reinitialises the buffer. If `clean=True` (default), calls `purge()` first.
Then loads each `(key, value)` pair from `defaults` via `set()`.

## Subclasses

- [SimpleFileBuffer](filebuffer.md) — file-backed storage
- [SharedBuffer](shareddata.md) — thread-safe in-memory dict
- [SharedQueueBuffer](shareddata.md) — thread-safe per-key queues
