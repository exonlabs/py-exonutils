# utils

General-purpose utilities: interactive console I/O, subprocess execution,
named pipe IPC, input validation, and package introspection.

## Modules

| Module | Contents |
|---|---|
| [console](console.md) | `Console` — interactive prompted input with validation |
| [shell](shell.md) | `Shell` — synchronous subprocess execution |
| [pipe](pipe.md) | `NamedPipe` — POSIX named pipe IPC |
| [validation](validation.md) | `is_alpha`, `is_digit`, `is_tcp_ipv4`, `is_tcp_port`, ... |
| [pkgtools](pkgtools.md) | `get_pkgs`, `get_mods`, `get_classes` |
