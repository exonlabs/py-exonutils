# pkgtools

`exonutils.utils.pkgtools`

Utilities for runtime Python package and class introspection.

## Functions

### `get_pkgs(target: str) -> list[str]`

Returns the fully-qualified names of all sub-packages inside `target`.

```python
from exonutils.utils.pkgtools import get_pkgs
print(get_pkgs("exonutils"))
# ['exonutils.buffers', 'exonutils.db', ...]
```

### `get_mods(target: str) -> list`

Returns a list of imported module objects from `target` — the package
itself plus all non-package modules directly inside it.

```python
from exonutils.utils.pkgtools import get_mods
mods = get_mods("exonutils.utils")
```

### `get_classes(target, baseclass=None) -> list`

Returns classes exported via `target.__all__`. If `baseclass` is given,
only subclasses of it are returned.

```python
from exonutils.utils.pkgtools import get_classes
from exonutils.buffers import common
from exonutils.buffers.common import BaseBuffer

classes = get_classes(common, baseclass=BaseBuffer)
```

!!! note
    `get_classes` requires the target module to define `__all__`. Modules
    in `exonutils` set `__all__ = []` by default — populate it to expose
    classes via this function.
