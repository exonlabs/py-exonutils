# webapp

Flask/Gunicorn web server wrappers providing a structured application
lifecycle, view routing, and multi-worker production serving.

**Requires:** `flask`, `jinja2`; `gunicorn` for `ExtWebServer`.

## Classes

| Class | Module | Description |
|---|---|---|
| [BaseWebView](view.md) | `webapp.view` | Base class for URL-routed view handlers |
| [SimpleWebServer](server.md) | `webapp.server` | Single-process Flask server |
| [ExtWebServer](extserver.md) | `webapp.extserver` | Gunicorn multi-worker server |
| [WebArbiter](extserver.md) | `webapp.extserver` | Gunicorn arbiter with custom signal handling |
| [ThreadWebArbiter](extserver.md) | `webapp.extserver` | `WebArbiter` runnable from a thread |

## Architecture

```
SimpleWebServer          ExtWebServer
  .app (Flask)    →        (Gunicorn BaseApplication)
  .add_view(...)           WebArbiter / ThreadWebArbiter
  .start(host, port)         manages worker processes
```
