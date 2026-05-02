# Console

`exonutils.utils.console.Console`

Interactive console input with colored prompts (via `colorama` if installed),
retry logic, and built-in validators.

## Class Attribute

| Attribute | Default | Description |
|---|---|---|
| `prompt_caret` | `">>"` | Prefix shown before each prompt |

## Methods

### `get_value(msg, default=None, required=False, trials=3, hidden=False, regex=None, validator=None)`

Prompts for a string value.

| Parameter | Description |
|---|---|
| `msg` | Prompt label |
| `default` | Value used if input is empty |
| `required` | Raises `ValueError` after `trials` failed attempts if no value given |
| `trials` | Maximum number of input attempts |
| `hidden` | Masks input (password mode) |
| `regex` | Validates input against a regular expression |
| `validator` | Custom `callable(input_str, regex) -> True or error_str` |

### `get_password(msg, ...)`

Shorthand for `get_value(..., hidden=True)`.

### `confirm_password(msg, value, trials=3)`

Re-prompts and compares against `value`. Raises `ValueError` on mismatch
after `trials` attempts.

### `get_number(msg, default=None, required=False, trials=3, vmin=None, vmax=None)`

Prompts for an integer. Validates range if `vmin`/`vmax` are given.
Returns `int` or `None`.

### `get_decimal(msg, default=None, required=False, trials=3, vmin=None, vmax=None)`

Prompts for a float. Returns `float` or `None`.

### `select_value(msg, values, default=None, required=False, trials=3, case_sensitive=False)`

Prompts for a choice from `values` list. Displays choices as `{a|b|c}`.

### `select_yesno(msg, default=None, required=False, trials=3)`

Shorthand for `select_value(..., values=['y', 'n'])`. Returns `bool`.

## Example

```python
from exonutils.utils.console import Console

ch = Console()
host = ch.get_value("Enter host", default="localhost", required=True)
port = ch.get_number("Enter port", default=8080, vmin=1, vmax=65535)
confirm = ch.select_yesno("Save settings?", default="y")
```
