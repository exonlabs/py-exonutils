# exonutils

General tools and utilities for modern Python applications.

## Overview

`exonutils` is a lightweight, stdlib-only Python library providing common
utilities for application development. It covers process and service
management, database abstraction, file-based configuration, shared buffers,
FTP clients, web server integration, and more.

**No external runtime dependencies** — only optional extras for specific
subpackages (SQLAlchemy, Flask/Gunicorn, colorama).

## Installation

```bash
pip install exonutils
```

## Package Layout

| Subpackage | Description |
|---|---|
| [`buffers`](modules/buffers/index.md) | In-memory and file-based key/value buffers |
| [`db`](modules/db/index.md) | Multi-backend SQL abstraction layer |
| [`fileconfig`](modules/fileconfig/index.md) | File-based configuration (JSON, binary blob) |
| [`process`](modules/process/index.md) | Daemon and service process management |
| [`services`](modules/services/index.md) | FTP client with TLS support |
| [`utils`](modules/utils/index.md) | Console I/O, shell, pipes, validation, introspection |
| [`webapp`](modules/webapp/index.md) | Flask/Gunicorn web server wrappers |
| [`_backport.v5`](modules/_backport/v5/index.md) | Legacy v5 compatibility layer |

## Quick Links

- [Getting Started](getting-started.md)
- [API Modules](modules/index.md)
- [Repository](https://git.exonlabs.net/py-exonutils)
