# BaseWebView

`exonutils.webapp.view.BaseWebView`

Base class for view handlers. Each subclass represents one URL endpoint,
with HTTP method dispatch handled automatically.

## Class Attributes

| Attribute | Default | Description |
|---|---|---|
| `routes` | `[]` | List of `(url, endpoint)` tuples to register |
| `methods` | `['GET', 'POST']` | Allowed HTTP methods |

## Constructor

```python
BaseWebView(name=None, logger=None, debug=0)
```

`name` defaults to the class name.

## Override Points

| Method | Description |
|---|---|
| `initialize()` | Called by the server after registering routes |
| `get(**kwargs)` | Handles GET requests |
| `post(**kwargs)` | Handles POST requests |
| `before_request(**kwargs)` | Pre-handler hook; return a response to short-circuit |
| `after_request(response, **kwargs)` | Post-handler hook; must return the (possibly modified) response |

## Request Helpers

| Method | Returns |
|---|---|
| `is_xhrequest()` | `True` if `X-Requested-With: XMLHttpRequest` |
| `is_jsrequest()` | `True` if JSON content-type or XHR |

## Example

```python
from exonutils.webapp.view import BaseWebView

class StatusView(BaseWebView):
    routes = [("/status", "status")]
    methods = ["GET"]

    def get(self):
        return {"status": "ok"}, 200
```
