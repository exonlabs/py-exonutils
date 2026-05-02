# SharedData / SharedBuffer / SharedQueueBuffer

`exonutils.buffers.shareddata`

Thread-safe in-memory containers for sharing state between threads.

---

## SharedData

Single thread-safe value container. Not a `BaseBuffer` subclass — simpler
than a key/value store.

```python
SharedData(default=None)
```

| Method | Description |
|---|---|
| `get()` | Returns the current value (under lock) |
| `set(value)` | Replaces the value (under lock) |

```python
from exonutils.buffers.shareddata import SharedData

flag = SharedData(default=False)
flag.set(True)
print(flag.get())  # True
```

---

## SharedBuffer

Thread-safe key/value buffer backed by a `dict`. All operations acquire a
`threading.Lock`.

Implements the full [BaseBuffer](common.md) interface.

```python
from exonutils.buffers.shareddata import SharedBuffer

buf = SharedBuffer()
buf.set("count", 0)
buf.set("count", buf.get("count") + 1)
```

---

## SharedQueueBuffer

Extends `SharedBuffer`. Each key holds a `SimpleQueue` instead of a plain
value. Used for passing messages between threads.

### Additional Methods

| Method | Description |
|---|---|
| `create(key)` | Creates an empty queue for the key |
| `set(key, value)` | Pushes `value` onto the key's queue; creates the queue if missing |
| `get(key, default=None)` | Pops a value from the key's queue (non-blocking); returns `default` if empty |
| `put(key, value)` | Pushes `value` only if the queue already exists; returns `True` on success |

```python
from exonutils.buffers.shareddata import SharedQueueBuffer

q = SharedQueueBuffer()
q.set("events", "started")
q.set("events", "running")
print(q.get("events"))  # started
print(q.get("events"))  # running
```
