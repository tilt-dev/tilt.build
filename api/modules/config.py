from typing import Dict, Union, List, Callable, Any

def define_string_list(name: str, args: bool=False, usage: str="") -> None:
    """
    Defines a config setting of type `List[str]` to be returned by
    :meth:`parse`.

    See the `Tiltfile config documentation <tiltfile_config.html>`_ for examples and more
    information.

    Args:
      name: The name of the config setting
      args: If true, this setting takes the value of any positional args (e.g.,
            in ``tilt up -- 1 2 3``, this setting would get ``["1" "2" "3"]``)
      usage: When arg parsing fails, what to print for this setting's description.
    """

def parse() -> Dict[str, Any]:
    """
    Loads config settings from tilt_config.json, overlays config settings from
    Tiltfile command-line args, validates them using the setting definitions
    specified in the Tiltfile, and returns a Dict of the resulting settings.

    Settings that are defined in the Tiltfile but not specified in the config
    file or command-line args will be absent from the dict. Access values via,
    e.g., `cfg.get('foo', ["hello"])` to have a default value.

    Note: by default, Tilt interprets the Tilt command-line args as the names of
    Tilt resources to run. When a Tiltfile calls :meth:`parse`, that behavior is
    suppressed, since those args are now managed by :meth:parse. If a
    Tiltfile uses :meth:`parse` and also needs to allow specifying a set
    of resources to run, it needs to call :meth:`set_enabled_resources`.

    See the `Tiltfile config documentation <tiltfile_config.html>`_ for examples
    and more information.

    Returns:
      A Dict where the keys are settings names and the values are their values.
    """

def set_enabled_resources(resources: List[str]) -> None:
    """
    Tells Tilt to only run the specified resources.
    (takes precedence over the default behavior of "run the resources specified
    on the command line")

    Calling this with an empty list results in all resources being run.

    See the `Tiltfile config documentation <tiltfile_config.html>`_ for examples
    and more information.

    Args:
      resources: The names of the resources to run, or an empty list to run them
                 all.
    """
