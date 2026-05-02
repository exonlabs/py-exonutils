# SimpleService / ManagedService

`exonutils.process.service`

---

## SimpleService

`exonutils.process.service.SimpleService`

Extends [BaseDaemon](daemon.md). Manages a collection of
[BaseRoutine](routine.md) threads, monitoring their health and restarting
dead routines on each `monitor_interval` cycle.

### Constructor

```python
SimpleService(name, proctitle='', logger=None, debug=0)
```

Inherits all `BaseDaemon` constructor parameters.

### Configuration Attributes

| Attribute | Default | Description |
|---|---|---|
| `monitor_interval` | `5` | Seconds between routine health checks |
| `exit_delay` | `3` | Seconds to wait for routines to stop on shutdown |

### Routine Management

| Method | Description |
|---|---|
| `add_routine(rthnd)` | Registers a `BaseRoutine`; sets its `parent` to this service |
| `del_routine(name)` | Cancels and removes a routine by name |
| `start_routine(name)` | Starts a registered routine |
| `stop_routine(name, suspend=False, wait_exit=True)` | Stops a routine; optionally suspends it |
| `check_routines()` | Health-check loop body — restarts dead, removes cancelled |

### Example

```python
from exonutils.process.service import SimpleService
from exonutils.process.routine import BaseRoutine

class Worker(BaseRoutine):
    def execute(self):
        self.log.info("working")
        self.sleep(5)

svc = SimpleService("mysvc")
svc.add_routine(Worker("worker1"))
svc.add_routine(Worker("worker2", auto_start=False))
svc.start()
```

---

## ManagedService

`exonutils.process.service.ManagedService`

Extends `SimpleService` with a named-pipe command interface for runtime
management.

### Class Attributes

| Attribute | Description |
|---|---|
| `manage_pipe` | Base path for named pipes; e.g. `/run/myapp/manage` |
| `cmdhandler_callback` | `callable(service, command) -> str` — handles commands, returns reply string |

Two pipes are created: `<manage_pipe>.in` (receive) and `<manage_pipe>.out`
(send). The service reads commands with a timeout of `monitor_interval / 2`
seconds.

### Example

```python
from exonutils.process.service import ManagedService

def handle_cmd(svc, cmd):
    if cmd == "status":
        return "OK"
    return "UNKNOWN"

class MyService(ManagedService):
    manage_pipe = "/run/myapp/manage"
    cmdhandler_callback = staticmethod(handle_cmd)
```
