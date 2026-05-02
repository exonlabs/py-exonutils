# validation

`exonutils.utils.validation`

Lightweight predicate functions for input validation. All functions return
`True` on valid input and `False` otherwise — no exceptions raised.

## Functions

| Function | Description |
|---|---|
| `is_alpha(data)` | Letters only (`str.isalpha()`) |
| `is_alphanum(data)` | Letters and digits only (`str.isalnum()`) |
| `is_digit(data)` | Digits only (`str(data).isdigit()`) |
| `is_number(data)` | Positive or negative integer string (`^[0-9-]+$`) |
| `is_decimal(data)` | Positive or negative decimal string (`^[0-9-]+(.[0-9]+)?$`) |
| `is_tcp_ipv4(data)` | Valid IPv4 address (four octets, each 0–255) |
| `is_tcp_port(data)` | Valid TCP port (integer 1–65535) |

## Example

```python
from exonutils.utils.validation import (
    is_alpha, is_digit, is_tcp_ipv4, is_tcp_port
)

is_alpha("hello")        # True
is_alpha("hello123")     # False
is_digit("42")           # True
is_digit("-42")          # False
is_tcp_ipv4("10.0.0.1")  # True
is_tcp_ipv4("999.0.0.1") # False
is_tcp_port(8080)        # True
is_tcp_port(0)           # False
is_tcp_port(99999)       # False
```
