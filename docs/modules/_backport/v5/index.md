# _backport.v5

`exonutils._backport.v5`

Compatibility layer preserving the v5 public API. Use this when migrating
from exonutils v5 to v6+ without rewriting all import paths immediately.

!!! warning
    This backport is provided for migration only. New code should import
    from the main subpackages. The v5 API may be removed in a future major
    version.

## Modules

| v5 Module | Equivalent v6+ Module |
|---|---|
| [buffers](buffers.md) | `exonutils.buffers.*` |
| [config](config.md) | `exonutils.fileconfig.*` |
| [console](console.md) | `exonutils.utils.console` |
| [daemon](daemon.md) | `exonutils.process.daemon` |
| [dbutils](dbutils.md) | `exonutils.db.backends.*.utils` |
| [misc](misc.md) | `exonutils.utils.pkgtools` |
| [service](service.md) | `exonutils.process.service` |
| [sqlalchemydb](sqlalchemydb.md) | `exonutils.db.sqlalchemy.*` |
| [sqlitedb](sqlitedb.md) | `exonutils.db.backends.sqlite.*` |
| [webapp](webapp.md) | `exonutils.webapp.*` |
