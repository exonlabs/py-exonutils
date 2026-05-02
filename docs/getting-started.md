# Getting Started

## Requirements

- Python 3.9+
- No mandatory external dependencies

Optional extras install additional packages for specific subpackages:

```bash
# SQLAlchemy ORM integration
pip install sqlalchemy

# Flask/Gunicorn web server
pip install flask jinja2 gunicorn

# colorama for colored console output
pip install colorama
```

## Installation

```bash
pip install exonutils
```

## Import Conventions

All classes and functions are imported directly from their leaf module:

```python
from exonutils.buffers.shareddata import SharedBuffer
from exonutils.db.handlers import DBHandler
from exonutils.fileconfig.jsonconfig import JsonFileConfig
from exonutils.process.service import SimpleService
from exonutils.utils.console import Console
from exonutils.utils.validation import is_tcp_ipv4, is_tcp_port
```

The subpackage `__init__.py` files are empty — there are no top-level
re-exports.
