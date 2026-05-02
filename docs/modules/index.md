# Modules

All public classes and functions are accessed by importing directly from the
leaf module. The subpackage `__init__.py` files are intentionally empty.

## Subpackages

| Module | Import path | Contents |
|---|---|---|
| [buffers](buffers/index.md) | `exonutils.buffers.*` | BaseBuffer, SimpleFileBuffer, SharedData, SharedBuffer, SharedQueueBuffer |
| [db](db/index.md) | `exonutils.db.*` | SQL abstraction, ORM, 4 backends |
| [fileconfig](fileconfig/index.md) | `exonutils.fileconfig.*` | JsonFileConfig, BlobFileConfig |
| [process](process/index.md) | `exonutils.process.*` | BaseDaemon, BaseRoutine, SimpleService, ManagedService |
| [services](services/index.md) | `exonutils.services.*` | FTPClient (native + shell) |
| [utils](utils/index.md) | `exonutils.utils.*` | Console, Shell, NamedPipe, validation, pkgtools |
| [webapp](webapp/index.md) | `exonutils.webapp.*` | SimpleWebServer, ExtWebServer, BaseWebView |
| [_backport.v5](_backport/v5/index.md) | `exonutils._backport.v5.*` | Legacy v5 compatibility layer |
