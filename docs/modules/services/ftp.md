# FTPClient (native)

`exonutils.services.ftp.FTPClient`

Native Python FTP client built on `ftplib`. Supports explicit and implicit
TLS (v1.2 / v1.3), passive/active transfer modes, and configurable retries.

## Constructor

```python
FTPClient(options: dict, logger=None)
```

## Methods

### `download(remote_file, local_dir, **kwargs) -> bool`

Downloads `remote_file` from the FTP server into `local_dir`.

| kwarg | Description |
|---|---|
| `retries` | Number of retry attempts on failure (default: `0`) |
| `retry_delay` | Seconds between retries (default: `5`) |

Returns `True` on success, `False` on failure.

### `upload(local_file, remote_dir, **kwargs) -> bool`

Uploads `local_file` to `remote_dir` on the FTP server.

Same `retries` / `retry_delay` kwargs as `download`.

### `cancel()`

Sets the internal `term_event` to abort the current in-progress operation.

## TLS Notes

- **Explicit TLS** — standard FTPS over port 21 using `STARTTLS`; uses
  `_ExplicitFtpTls` (subclass of `ftplib.FTP_TLS`)
- **Implicit TLS** — FTPS over port 990 with SSL from the first byte; uses
  `_ImplicitFtpTls`
- `tls_version: "TLSv1_2"` restricts to TLS 1.2; `"Auto"` allows 1.2+

## Example

```python
from exonutils.services.ftp import FTPClient

client = FTPClient({
    "host": "ftp.example.com",
    "port": 21,
    "username": "user",
    "password": "pass",
    "tls_enable": True,
    "tls_protocol": "Explicit",
})

client.upload("/data/report.csv", "/uploads", retries=3)
client.download("/uploads/report.csv", "/tmp", retries=2, retry_delay=10)
```
