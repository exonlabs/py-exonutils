# services

FTP client implementations with TLS support and retry logic.

## Classes

| Class | Module | Description |
|---|---|---|
| [FTPClient](ftp.md) | `services.ftp` | Native Python FTP client using `ftplib` |
| [FTPClient](ftp_shell.md) | `services.ftp_shell` | Shell-based FTP client using `curl` |

Both classes expose the same public interface (`download`, `upload`,
`cancel`) and accept the same options dict.

## Options Dict

```python
options = {
    "host": "192.168.1.10",
    "port": 21,
    "username": "user",
    "password": "pass",
    "transfer_mode": "Passive",    # Passive | Active
    "tls_enable": True,
    "tls_protocol": "Explicit",    # Explicit | Implicit
    "tls_version": "Auto",         # Auto | TLSv1_2 | TLSv1_3
}
```
