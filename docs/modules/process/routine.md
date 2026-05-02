# BaseRoutine

`exonutils.process.routine.BaseRoutine`

Base class for thread-based recurring tasks managed by a
[SimpleService](service.md). Each routine runs in its own daemon thread.

## Constructor

```python
BaseRoutine(name: str, logger=None, debug: int = 0, auto_start: bool = True)
```

| Parameter | Description |
|---|---|
| `name` | Routine identifier |
| `logger` | Python logger; inherits from parent service if not set |
| `debug` | Debug level; inherits from parent service |
| `auto_start` | If `False`, routine starts in suspended state |

## Lifecycle Methods

Override in subclasses:

| Method | When called |
|---|---|
| `initialize()` | Once before the run loop |
| `execute()` | Every loop iteration — **must override** |
| `terminate()` | Once after loop exits |

## Control Methods

| Method | Description |
|---|---|
| `start()` | Spawns the daemon thread; requires `parent` to be set |
| `stop(suspend=False, cancel=False)` | Signals the routine to stop |
| `is_alive()` | Returns `True` if the thread is running |
| `sleep(timeout)` | Interruptible sleep |

## State Flags

| Flag | Description |
|---|---|
| `is_suspended` | Routine is paused; parent will not auto-restart it |
| `is_cancelled` | Routine is marked for removal by the parent |
| `initial_run` | Set to `True` after first `run()` call |

## Example

```python
from exonutils.process.routine import BaseRoutine

class PollRoutine(BaseRoutine):
    def execute(self):
        self.log.info("polling...")
        self.sleep(30)
```
