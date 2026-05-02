# NamedPipe

`exonutils.utils.pipe.NamedPipe`

POSIX named pipe (FIFO) wrapper for inter-process communication. Supports
non-blocking send/receive with timeout and cancellation.

## Constructor

```python
NamedPipe(path: str)
```

## Configuration Attributes

| Attribute | Default | Description |
|---|---|---|
| `polling_delay` | `0.2` | Seconds between poll attempts |
| `send_delay` | `0.1` | Delay after send to allow the reader to finish |
| `recv_delay` | `0.1` | Select timeout while reading chunks |
| `recv_size` | `1024` | Bytes per read chunk |
| `cancel_event` | `threading.Event()` | Set this to abort blocking operations |

## Methods

| Method | Description |
|---|---|
| `open(perm=0o666)` | Creates the FIFO at `path`; removes any existing FIFO first |
| `close()` | Removes the FIFO file |
| `cancel()` | Sets `cancel_event` to abort ongoing send/recv |
| `send(data, timeout=0)` | Sends `bytes` to the pipe; returns `True` on success, `False` if no peer or cancelled |
| `recv(timeout=0)` | Waits for and reads `bytes` from the pipe; returns empty `bytes` on timeout or cancel |
| `send_wait(data, timeout=0)` | Sends data then waits for a reply; raises `RuntimeError` on failure or timeout |

## Example

```python
from exonutils.utils.pipe import NamedPipe

# writer process
pipe = NamedPipe("/run/myapp/cmd.in")
pipe.open()
pipe.send(b"status", timeout=3)
pipe.close()

# reader process
pipe = NamedPipe("/run/myapp/cmd.in")
pipe.open()
data = pipe.recv(timeout=5)
print(data.decode())  # status
pipe.close()
```
