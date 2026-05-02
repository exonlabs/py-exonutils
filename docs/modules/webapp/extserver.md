# ExtWebServer / WebArbiter / ThreadWebArbiter

`exonutils.webapp.extserver`

Production-grade Gunicorn-based server wrappers. **Requires `gunicorn`.**

---

## ExtWebServer

`exonutils.webapp.extserver.ExtWebServer`

Wraps a `SimpleWebServer` as a Gunicorn `BaseApplication`. Manages worker
processes, logging integration, and process title.

### Constructor

```python
ExtWebServer(websrv: SimpleWebServer, options: dict = {})
```

### Gunicorn Options

| Key | Default | Description |
|---|---|---|
| `bind` | — | `"host:port"` or `"unix:/path/to.sock"` |
| `workers` | `2` | Number of worker processes |
| `worker_class` | `"sync"` | Gunicorn worker type |
| `timeout` | `0` | Worker timeout in seconds |
| `graceful_timeout` | `0` | Graceful shutdown timeout |
| `max_requests` | `0` | Requests per worker before restart |
| `max_requests_jitter` | `0` | Random jitter for `max_requests` |
| `reuse_port` | `True` | Enable `SO_REUSEPORT` (disabled for Unix sockets) |

### Example

```python
from exonutils.webapp.server import SimpleWebServer
from exonutils.webapp.extserver import ExtWebServer, ThreadWebArbiter

srv = SimpleWebServer("myapp")
srv.initialize()
srv.add_view(MyView)

app = ExtWebServer(srv, options={"bind": "0.0.0.0:8080", "workers": 4})
arbiter = ThreadWebArbiter(app)
arbiter.run()
```

---

## WebArbiter

`exonutils.webapp.extserver.WebArbiter`

Subclass of Gunicorn's `Arbiter` with a reduced signal set
(`HUP QUIT INT TERM USR1`) and stores the root PID in the Flask app config.

Handles socketd / systemd socket activation and `GUNICORN_FD` listener
inheritance for zero-downtime restarts.

---

## ThreadWebArbiter

`exonutils.webapp.extserver.ThreadWebArbiter`

Extends `WebArbiter` for running from a thread. Disables signal
initialisation (`init_signals` is a no-op) so the thread does not interfere
with the parent process signal handlers.

### Usage

```python
import threading
arbiter = ThreadWebArbiter(app)
t = threading.Thread(target=arbiter.run, daemon=True)
t.start()
```
