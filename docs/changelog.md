# Changelog

## v6.8

**Released:** 2026-04-23

### Tooling

- Replaced `scripts/common.sh` with a new `environ` shell script — centralises
  virtualenv paths, package metadata, and colour helper functions used by all
  Makefile targets
- Rewrote Makefile targets to source `environ` directly; removed dependency on
  `scripts/common.sh`
- Updated `scripts/build.sh`, `scripts/release.sh`, `scripts/setup_dev.sh`,
  and `scripts/host_update.sh` to use the new `environ` conventions
- Updated `pyproject.toml` dependency versions

---

## v6.7

**Released:** 2025-12-16

### Package

- Replaced module-level `__version__`, `__author__`, `__license__`,
  `__copyright__` constants in `__init__.py` with a `get_version()` function
  backed by `importlib.metadata`
- Migrated package configuration from `setup.cfg` / `setup.py` to
  `pyproject.toml`

### Bug Fixes

- `services.ftp.FTPClient` — fixed `download()` and `upload()` success paths
  logging at `error` level instead of `info`
- `services.ftp_shell.FTPClient` — same fix for the shell-based client

### webapp

- `ExtWebServer` — `reuse_port` now reads from the options dict (default
  `True`) and is automatically disabled when a Unix socket bind path is
  configured; default worker count changed from `os.cpu_count()` to `2`
- `SimpleWebServer.create_app()` — refactored options initialisation to use
  a single `dict.update()` call
- `BaseWebView.is_jsrequest()` — replaced `request.is_json` with an explicit
  `Content-Type` header check for more reliable JSON request detection across
  Flask versions
