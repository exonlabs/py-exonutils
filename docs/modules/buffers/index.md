# buffers

Key/value buffer abstractions backed by files or shared memory.

## Classes

| Class | Module | Description |
|---|---|---|
| [BaseBuffer](common.md) | `buffers.common` | Abstract base class for all buffers |
| [SimpleFileBuffer](filebuffer.md) | `buffers.filebuffer` | File-backed persistent buffer |
| [SharedData](shareddata.md) | `buffers.shareddata` | Thread-safe single-value container |
| [SharedBuffer](shareddata.md) | `buffers.shareddata` | Thread-safe key/value buffer |
| [SharedQueueBuffer](shareddata.md) | `buffers.shareddata` | Thread-safe per-key queue buffer |

## Common Interface

All buffer classes implement the `BaseBuffer` interface:

```python
buf.keys()             # list all keys
buf.items()            # list all (key, value) pairs
buf.get(key)           # read a key, returns None if missing
buf.set(key, value)    # write a key
buf.delete(key)        # delete a key
buf.purge()            # delete all keys
buf.reset(defaults)    # purge then load defaults
```
