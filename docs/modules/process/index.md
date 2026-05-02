# process

Daemon and service process management with signal handling, routine
lifecycle management, and optional IPC via named pipes.

## Classes

| Class | Module | Description |
|---|---|---|
| [BaseDaemon](daemon.md) | `process.daemon` | Base class for long-running daemon processes |
| [BaseRoutine](routine.md) | `process.routine` | Base class for thread-based recurring tasks |
| [SimpleService](service.md) | `process.service` | Daemon that manages a set of routines |
| [ManagedService](service.md) | `process.service` | SimpleService with named-pipe command interface |

## Relationship

```
BaseDaemon
└── SimpleService       manages → BaseRoutine threads
    └── ManagedService  adds IPC via NamedPipe
```
