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

def getcwd() -> str:
  """Returns a string representation of the current working directory.

  The current working directory is the directory containing the currently executing Tiltfile.
  If your Tiltfile runs any commands, they run from this directory.

  While calling :meth:load or :meth:include to execute another Tiltfile,
  returns the directory of the loaded/included Tiltfile.
  """
  pass

def realpath(path: str) -> str:
  """Return the canonical path of the specified filename, eliminating any symbolic links encountered in the path (if they are supported by the operating system)."""
  pass
