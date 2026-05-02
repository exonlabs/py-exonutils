# BaseDaemon

`exonutils.process.daemon.BaseDaemon`

Base class for long-running daemon processes with signal handling and a
structured run loop.

## Constructor

```python
BaseDaemon(name: str, proctitle: str = '', logger=None, debug: int = 0)
```

| Parameter | Description |
|---|---|
| `name` | Daemon identifier, used as logger name if none provided |
| `proctitle` | OS process title (requires `setproctitle`); defaults to `name` |
| `logger` | Python logger instance; created from `name` if not provided |
| `debug` | Debug level: `0` normal, `1` extra logging, `2` full tracebacks |

## Lifecycle Methods

Override these in subclasses:

| Method | When called | Notes |
|---|---|---|
| `initialize()` | Once before the run loop | Raise to abort startup |
| `execute()` | Every loop iteration | **Must override** — raises `NotImplementedError` by default |
| `terminate()` | Once after loop exits | Cleanup; errors are logged but not propagated |

## Control Methods

| Method | Description |
|---|---|
| `start()` | Sets up signals, process title, then calls `run()` |
| `stop()` | Sets `term_event`; triggers clean loop exit |
| `sleep(timeout)` | Interruptible sleep — exits early if `term_event` is set |
| `run()` | Runs the full lifecycle (init → loop → terminate) |

## Signal Handling

Default signals handled: `SIGINT`, `SIGTERM`, `SIGQUIT`, `SIGHUP`,
`SIGUSR1`, `SIGUSR2`.

`SIGINT`, `SIGTERM`, `SIGQUIT` call `stop()`. To handle others, define
`handle_sighup()`, `handle_sigusr1()`, etc. on the subclass.

## Example

```python
from exonutils.process.daemon import BaseDaemon

class MyDaemon(BaseDaemon):
    def execute(self):
        self.log.info("tick")
        self.sleep(10)

d = MyDaemon("mydaemon", debug=1)
d.start()
```
