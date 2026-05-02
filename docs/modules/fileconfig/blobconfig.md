# BlobFileConfig

`exonutils.fileconfig.common.BlobFileConfig`

Stores configuration as an encoded binary file. The contents are not
human-readable, providing basic obfuscation for sensitive config data.

## Constructor

```python
BlobFileConfig(file_path: str, defaults: dict = None)
```

## Behaviour

- `load()` — reads the binary file, decodes it via `_decode()`, merges with
  `defaults`
- `save()` — encodes the buffer via `_encode()` and writes binary
- `dump()` — returns the raw binary file contents as `bytes`

## Encoding

The default encoding is base64 + byte-pair inversion (via `_mangle`). To
strengthen the encoding for production use, subclass and override
`_mangle()` and `_demangle()`.

## Example

```python
from exonutils.fileconfig.blobconfig import BlobFileConfig

cfg = BlobFileConfig("/etc/myapp/config.bin", defaults={"secret": ""})
cfg.set("secret", "s3cr3t", encode=True)
cfg.save()

print(cfg.get("secret", decode=True))  # s3cr3t
```
