# Shell

`exonutils.utils.shell.Shell`

Thin wrapper around `subprocess.Popen` for synchronous shell command
execution via `/bin/bash`.

## Method

### `Shell.run(commands, inputs=None, timeout=None)`

Classmethod. Executes one or more shell commands.

| Parameter | Type | Description |
|---|---|---|
| `commands` | `str` or `list[str]` | Single command string or list joined with `"; "` |
| `inputs` | `str` or `None` | Data passed to stdin |
| `timeout` | `float` or `None` | Seconds before raising `subprocess.TimeoutExpired` |

**Returns:** `(returncode, stdout, stderr)` tuple.

- `returncode` — exit code; negative means terminated by signal
- `stdout` / `stderr` — captured text output

**Raises:** `RuntimeError` on any execution failure.

## Example

```python
from exonutils.utils.shell import Shell

rc, out, err = Shell.run("uname -r")
print(rc, out.strip())

rc, out, err = Shell.run(["echo hello", "echo world"])
print(out)  # hello\nworld\n
```
