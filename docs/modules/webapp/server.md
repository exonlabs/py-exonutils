# SimpleWebServer

`exonutils.webapp.server.SimpleWebServer`

Single-process Flask application server. Suitable for development or
lightweight deployments. Use [ExtWebServer](extserver.md) for production
multi-worker deployments.

## Constructor

```python
SimpleWebServer(name, proctitle='', options={}, logger=None,
                reqlogger=None, debug=0)
```

| Parameter | Description |
|---|---|
| `name` | Application name |
| `proctitle` | OS process title (requires `setproctitle`) |
| `options` | Flask config options (see below) |
| `logger` | Application logger |
| `reqlogger` | Separate logger for HTTP requests |
| `debug` | Debug level |

## Flask Options

Passed as lowercase keys in `options`; stored in `app.config` as uppercase:

| Key | Default | Description |
|---|---|---|
| `secret_key` | auto-generated UUID | Flask secret key |
| `max_content_length` | `10485760` (10 MiB) | Max request body size |
| `templates_auto_reload` | — | Reload templates on change |

## Methods

| Method | Description |
|---|---|
| `initialize()` | Creates the Flask app and configures loggers |
| `add_view(view_hnd)` | Registers a `BaseWebView` class or instance |
| `create_app()` | Internal — creates and configures the Flask app |
| `start(host, port, **kwargs)` | Runs the Flask dev server |
| `stop()` | Sends `SIGTERM` to the root process |

## Example

```python
from exonutils.webapp.server import SimpleWebServer
from exonutils.webapp.view import BaseWebView

class HelloView(BaseWebView):
    routes = [("/", "hello")]
    def get(self):
        return "Hello", 200

srv = SimpleWebServer("myapp", options={"debug": True})
srv.initialize()
srv.add_view(HelloView)
srv.start("0.0.0.0", 8080)
```
