# FTPClient (shell)

`exonutils.services.ftp_shell.FTPClient`

Shell-based FTP client that delegates file operations to `curl`. Supports
the same TLS options as the native client but relies on the system `curl`
binary instead of `ftplib`.

## Constructor

```python
FTPClient(options: dict, logger=None)
```

Same options dict as [FTPClient (native)](ftp.md).

!!! note
    `transfer_blksize` is not supported in this implementation.

## Methods

### `download(remote_file, local_dir, **kwargs) -> bool`

Downloads a remote file using `curl`. Kwargs:

| kwarg | Default | Description |
|---|---|---|
| `retries` | `0` | Retry attempts on failure |
| `retry_delay` | `5` | Seconds between retries |
| `timeout` | `300` | Total operation timeout in seconds |

### `upload(local_file, remote_dir, **kwargs) -> bool`

Uploads a local file using `curl`. Same kwargs as `download`.

### `cancel()`

Sets `term_event` to abort the running operation.

## When to Use

Use this client when:

- The `ftplib` TLS implementation has compatibility issues with the server
- You need `curl`-specific features (e.g. progress, proxy, certificates)
- The target environment has `curl` available and `ftplib` is insufficient

## Example

```python
from exonutils.services.ftp_shell import FTPClient

client = FTPClient({
    "host": "ftp.example.com",
    "port": 21,
    "username": "user",
    "password": "pass",
    "tls_enable": True,
    "tls_version": "TLSv1_2",
}, logger=my_logger)

client.upload("/data/export.zip", "/backups", retries=2, timeout=120)
```
