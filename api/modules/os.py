from typing import Dict

environ = Dict[str, str]
"""A dictionary of your environment variables.

For example, ``os.environ['HOME']`` is usually your home directory.

Captured each time the Tiltfile begins execution.

Tiltfile dictionaries support many of the same methods
as Python dictionaries, including:

- dict.get(key, default)
- dict.items()

See the `Starlark spec <https://github.com/bazelbuild/starlark/blob/master/spec.md#built-in-methods>`_ for more.
"""
