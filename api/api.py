from typing import Dict, Union, List, Callable, Any

class Blob:
  """The result of executing a command on your local system.

   Under the hood, a `Blob` is just a string, but we wrap it this way so Tilt knows the difference between a string meant to convey content and a string indicating, say, a filepath.

   To wrap a string as a blob, call ``blob(my_str)``"""

class LiveUpdateStep:
  """A step in the process of performing a LiveUpdate on an image's container.

  For details, see the `Live Update documentation <live_update_reference.html>`_.
  """
  pass

def fall_back_on(files: Union[str, List[str]]) -> LiveUpdateStep:
  """Specify that any changes to the given files will cause Tilt to *fall back* to a
  full image build (rather than performing a live update).

  ``fall_back_on`` step(s) may only go at the beginning of your list of steps.

  (Files must be a subset of the files that we're already watching for this image;
  that is, if any files fall outside of DockerBuild.context or CustomBuild.deps,
  an error will be raised.)

  For more info, see the `Live Update Reference <live_update_reference.html>`_.

  Args:
      files: a string or list of strings of files. If relative, will be evaluated relative to the Tiltfile. Tilt compares these to the local paths of edited files when determining whether to fall back to a full image build.
  """
  pass

def set_team(team_id: str) -> None:
  """Associates this Tiltfile with the `team <teams.html>`_ identified by `team_id`.

  Sends usage information to Tilt Cloud periodically.
  """
  pass

def sync(local_path: str, remote_path: str) -> LiveUpdateStep:
  """Specify that any changes to `localPath` should be synced to `remotePath`

  May not follow any `run` steps in a `live_update`.

  For more info, see the `Live Update Reference <live_update_reference.html>`_.

  Args:
      localPath: A path relative to the Tiltfile's directory. Changes to files matching this path will be synced to `remotePath`.
          Can be a file (in which case just that file will be synced) or directory (in which case any files recursively under that directory will be synced).
      remotePath: container path to which changes will be synced. Must be absolute.
  """
  pass

def run(cmd: str, trigger: Union[List[str], str] = []) -> LiveUpdateStep:
  """Specify that the given `cmd` should be executed when updating an image's container

  May not precede any `sync` steps in a `live_update`.

  For more info, see the `Live Update Reference <live_update_reference.html>`_.

  Args:
    cmd: A shell command.
    trigger: If the ``trigger`` argument is specified, the build step is only run when there are changes to the given file(s). Paths relative to Tiltfile. (Note that in addition to matching the trigger, file changes must also match at least one of this Live Update's syncs in order to trigger this run. File changes that do not match any syncs will be ignored.)
  """
  pass

def restart_container() -> LiveUpdateStep:
  """**For use with Docker Compose resources only.**

  Specify that a container should be restarted when it is live-updated. In
  practice, this means that the container re-executes its `ENTRYPOINT` within
  the changed filesystem.

  May only be included in a `live_update` once, and only as the last step.

  For more info (and for the equivalent functionality for Kubernetes resources),
  see the `Live Update Reference <live_update_reference.html#restarting-your-process>`__.
  """
  pass

def docker_build(ref: str, context: str, build_args: Dict[str, str] = {}, dockerfile: str = "Dockerfile", dockerfile_contents: Union[str, Blob] = "", live_update: List[LiveUpdateStep]=[], match_in_env_vars: bool = False, ignore: Union[str, List[str]] = [], only: Union[str, List[str]] = [], entrypoint: Union[str, List[str]] = [], target: str = "", ssh: Union[str, List[str]] = "", network: str = "", secret: Union[str, List[str]] = "", extra_tag: Union[str, List[str]] = "", container_args: List[str] = None) -> None:
  """Builds a docker image.

  The invocation

  .. code-block:: python

    docker_build('myregistry/myproj/backend', '/path/to/code')

  is roughly equivalent to the shell call

  .. code-block:: bash

    docker build /path/to/code -t myregistry/myproj/backend

  For more information on the `ignore` and `only` parameters, see our `Guide to File Changes </file_changes.html>`_.

  Note that you can't set both the `dockerfile` and `dockerfile_contents` arguments (will throw an error).

  Note also that the `entrypoint` parameter is not supported for Docker Compose resources. If you need it for your use case, let us know.

  Args:
    ref: name for this image (e.g. 'myproj/backend' or 'myregistry/myproj/backend'). If this image will be used in a k8s resource(s), this ref must match the ``spec.container.image`` param for that resource(s).
    context: path to use as the Docker build context.
    build_args: build-time variables that are accessed like regular environment variables in the ``RUN`` instruction of the Dockerfile. See `the Docker Build Arg documentation <https://docs.docker.com/engine/reference/commandline/build/#set-build-time-variables---build-arg>`_.
    dockerfile: path to the Dockerfile to build.
    dockerfile_contents: raw contents of the Dockerfile to use for this build.
    live_update: set of steps for updating a running container (see `Live Update documentation <live_update_reference.html>`_).
    match_in_env_vars: specifies that k8s objects can reference this image in their environment variables, and Tilt will handle those variables the same as it usually handles a k8s container spec's ``image`` s.
    ignore: set of file patterns that will be ignored. Ignored files will not trigger builds and will not be included in images. Follows the `dockerignore syntax <https://docs.docker.com/engine/reference/builder/#dockerignore-file>`_. Patterns will be evaluated relative to the ``context`` parameter.
    only: set of file paths that should be considered for the build. All other changes will not trigger a build and will not be included in images. Inverse of ignore parameter. Only accepts real paths, not file globs. Patterns will be evaluated relative to the ``context`` parameter.
    entrypoint: command to run when this container starts. Takes precedence over the container's ``CMD`` or ``ENTRYPOINT``, and over a `container command specified in k8s YAML <https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/>`_. If specified as a string, will be evaluated in a shell context (e.g. ``entrypoint="foo.sh bar"`` will be executed in the container as ``/bin/sh -c 'foo.sh bar'``); if specifed as a list, will be passed to the operating system as program name and args.
    target: Specify a build stage in the Dockerfile. Equivalent to the ``docker build --target`` flag.
    ssh: Include SSH secrets in your build. Use ssh='default' to clone private repositories inside a Dockerfile. Uses the syntax in the `docker build --ssh flag <https://docs.docker.com/develop/develop-images/build_enhancements/#using-ssh-to-access-private-data-in-builds>`_.
    network: Set the networking mode for RUN instructions. Equivalent to the ``docker build --network`` flag.
    secret: Include secrets in your build in a way that won't show up in the image. Uses the same syntax as the `docker build --secret flag <https://docs.docker.com/develop/develop-images/build_enhancements/#new-docker-build-secret-information>`_.
    extra_tag: Tag an image with one or more extra references after each build. Useful when running Tilt in a CI pipeline, where you want each image to be tagged with the pipeline ID so you can find it later. Uses the same syntax as the ``docker build --tag`` flag.
    container_args: args to run when this container starts. Takes precedence over a `container args specified in k8s YAML <https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/>`_.
  """
  pass

def docker_compose(configPaths: Union[str, List[str]]) -> None:
  """Run containers with Docker Compose.

  Tilt will read your Docker Compose YAML and separate out the services.
  We will infer which services defined in your YAML
  correspond to images defined elsewhere in your ``Tiltfile`` (matching based on
  the DockerImage ref).

  Tilt will watch your Docker Compose YAML and reload if it changes.

  For more info, see `the guide to Tilt with Docker Compose <docker_compose.html>`_.

  Examples:

  .. code-block:: python

    # Path to file
    docker_compose('./docker-compose.yml')

    # List of files
    docker_compose(['./docker-compose.yml', './docker-compose.override.yml'])

  Args:
    configPaths: Path(s) to Docker Compose yaml files.
  """



def k8s_yaml(yaml: Union[str, List[str], Blob]) -> None:
  """Call this with a path to a file that contains YAML, or with a ``Blob`` of YAML.

  We will infer what (if any) of the k8s resources defined in your YAML
  correspond to Images defined elsewhere in your ``Tiltfile`` (matching based on
  the DockerImage ref and on pod selectors). Any remaining YAML is YAML that Tilt
  applies to your k8s cluster independently.

  Any YAML files are watched (See ``watch_file``).

  Examples:

  .. code-block:: python

    # path to file
    k8s_yaml('foo.yaml')

    # list of paths
    k8s_yaml(['foo.yaml', 'bar.yaml'])

    # Blob, i.e. `local` output (in this case, script output)
    templated_yaml = local('./template_yaml.sh')
    k8s_yaml(templated_yaml)

  Args:
    yaml: Path(s) to YAML, or YAML as a ``Blob``.
  """
  pass


class TriggerMode:
  """A set of constants that describe how Tilt triggers an update for a resource.
  Possible values are:

  - ``TRIGGER_MODE_AUTO``: the default. When Tilt detects a change to files or config files associated with this resource, it triggers an update.

  - ``TRIGGER_MODE_MANUAL``: user manually triggers update for dirty resources (i.e. resources with pending changes) via a button in the UI. (Note that the initial build always occurs automatically.)

  The default trigger mode for all manifests may be set with the top-level function :meth:`trigger_mode`
  (if not set, defaults to ``TRIGGER_MODE_AUTO``), and per-resource with :meth:`k8s_resource` / :meth:`dc_resource`.

  See also: `Manual Update Control documentation <manual_update_control.html>`_
  """
  def __init__(self):
    pass

def trigger_mode(trigger_mode: TriggerMode):
  """Sets the default :class:`TriggerMode` for resources in this Tiltfile.
  (Trigger mode may still be adjusted per-resource with :meth:`k8s_resource`.)

  If this function is not invoked, the default trigger mode for all resources is ``TRIGGER MODE AUTO``.

  See also: `Manual Update Control documentation <manual_update_control.html>`_

  Args:
    trigger_mode: may be one of ``TRIGGER_MODE_AUTO`` or ``TRIGGER_MODE_MANUAL``

  """

# Hack so this appears correctly in the function signature: https://stackoverflow.com/a/50193319/4628866
TRIGGER_MODE_AUTO = type('_sentinel', (TriggerMode,),
                 {'__repr__': lambda self: 'TRIGGER_MODE_AUTO'})()

def dc_resource(name: str, trigger_mode: TriggerMode = TRIGGER_MODE_AUTO, resource_deps: List[str] = []) -> None:
  """Configures the Docker Compose resource of the given name. Note: Tilt does an amount of resource configuration
  for you(for more info, see `Tiltfile Concepts: Resources <tiltfile_concepts.html#resources>`_); you only need
  to invoke this function if you want to configure your resource beyond what Tilt does automatically.

  Args:
    trigger_mode: one of ``TRIGGER_MODE_AUTO`` or ``TRIGGER_MODE_MANUAL``. For more info, see the
      `Manual Update Control docs <manual_update_control.html>`_.
    resource_deps: a list of resources on which this resource depends.
      See the `Resource Dependencies docs <resource_dependencies.html>`_.
  """

  pass

def k8s_resource(workload: str = "", new_name: str = "",
                 port_forwards: Union[str, int, List[int]] = [],
                 extra_pod_selectors: Union[Dict[str, str], List[Dict[str, str]]] = [],
                 trigger_mode: TriggerMode = TRIGGER_MODE_AUTO,
                 resource_deps: List[str] = [], objects: List[str] = [],
                 auto_init: bool = True) -> None:
  """

  Configures or creates the specified Kubernetes resource.

  A "resource" is a bundle of work managed by Tilt: a Kubernetes resource consists
  of one or more Kubernetes objects to deploy, and zero or more image build directives
  for the images referenced therein.

  Tilt assembles Kubernetes resources automatically, as described in
  `Tiltfile Concepts: Resources <tiltfile_concepts.html#resources>`_. You may call
  ``k8s_resource`` to configure an automatically created Kubernetes resource, or to
  create and configure a new one:

  - If configuring an automatically created resource: the ``workload`` parameter must be specified.
  - If creating a new resource: both the ``objects`` and ``new_name`` parameters must be specified.

  Calling ``k8s_resource`` is *optional*; you can use this function to configure port forwarding for
  your resource, to rename it, or to adjust any of the other settings specified below, but in many cases,
  Tilt's default behavior is sufficient.

  Examples:

  .. code-block:: python

    # load Deployment foo
    k8s_yaml('foo.yaml')

    # modify the resource called "foo" (auto-assembled by Tilt)
    # to forward container port 8080 to localhost:8080
    k8s_resource(workload='foo', port_forwards=8080)

  .. code-block:: python

    # load CRD "bar", Service "bar", and Secret "bar-password"
    k8s_yaml('bar.yaml')

    # create a new resource called "bar" which contains the objects
    # loaded above (none of which are workloads, so none of which
    # would be automatically assigned to a resource). Note that the
    # first two object selectors specify both 'name' and 'kind',
    # since just the string "bar" does not uniquely specify a single object.
    # As the object name "bar-password" is unique, "bar-password" suffices as
    # an object selector (though a more more qualified object selector
    # like "bar-password:secret" or "bar-password:secret:default" would
    # be accepted as well).
    k8s_resource(
      objects=['bar:crd', 'bar:service', 'bar-password'],
      new_name='bar'
    )

  For more examples, see `Tiltfile Concepts: Resources <tiltfile_concepts.html#resources>`_.

  Args:
    workload: The name of an existing auto-assembled resource to configure
      (Tilt generates resource names when it `assembles resources by workload <tiltfile_concepts.html#resources>`_).
      (If you instead want to create/configure a _new_ resource, use the ``objects`` parameter
      in conjunction with ``new_name``.)
    new_name: If non-empty, will be used as the new name for this resource. (To
      programmatically rename all resources, see :meth:`workload_to_resource_function`.)
    port_forwards: Local ports to connect to the pod. If a target port is
      specified, that will be used. Otherwise, if the container exposes a port
      with the same number as the local port, that will be used. Otherwise,
      the default container port will be used.
      Example values: 9000 (connect localhost:9000 to the container's port 9000,
      if it is exposed, otherwise connect to the container's default port),
      '9000:8000' (connect localhost:9000 to the container port 8000),
      ['9000:8000', '9001:8001'] (connect localhost:9000 and :9001 to the
      container ports 8000 and 8001, respectively).
      [8000, 8001] (assuming the container exposes both 8000 and 8001, connect
      localhost:8000 and localhost:8001 to the container's ports 8000 and 8001,
      respectively).
    extra_pod_selectors: In addition to relying on Tilt's heuristics to automatically
      find Kubernetes resources associated with this resource, a user may specify extra
      labelsets to force pods to be associated with this resource. An pod
      will be associated with this resource if it has all of the labels in at
      least one of the entries specified (but still also if it meets any of
      Tilt's usual mechanisms).
    trigger_mode: One of ``TRIGGER_MODE_AUTO`` or ``TRIGGER_MODE_MANUAL``. For more info, see the
      `Manual Update Control docs <manual_update_control.html>`_.
    resource_deps: A list of resources on which this resource depends.
      See the `Resource Dependencies docs <resource_dependencies.html>`_.
    objects: A list of Kubernetes objects to be added to this resource, specified via
      Tilt's `Kubernetes Object Selector <tiltfile_concepts.html#kubernetes-object-selectors>`_
      syntax. If the ``workload`` parameter is specified, these objects will be
      added to the existing resource; otherwise, these objects will form a new
      resource with name ``new_name``. If an object selector matches more than
      one Kubernetes object, or matches an object already associated with a
      resource, ``k8s_resource`` raises an error.
    auto_init: whether this resource runs on ``tilt up``. Defaults to ``True``.
      Note that ``auto_init=False`` is only compatible with
      ``trigger_mode=TRIGGER_MODE_MANUAL``.
  """
  pass

def filter_yaml(yaml: Union[str, List[str], Blob], labels: dict=None, name: str=None, namespace: str=None, kind: str=None, api_version: str=None):
  """Call this with a path to a file that contains YAML, or with a ``Blob`` of YAML.
  (E.g. it can be called on the output of ``kustomize`` or ``helm``.)

  Captures the YAML entities that meet the filter criteria and returns them as a blob;
  returns the non-matching YAML as the second return value.

  For example, if you have a file of *all* your YAML, but only want to pass a few elements to Tilt: ::

    # extract all YAMLs matching labels "app=foobar"
    foobar_yaml, rest = filter_yaml('all.yaml', labels={'app': 'foobar'})
    k8s_yaml(foobar_yaml)

    # extract YAMLs of kind "deployment" with metadata.name regex-matching "baz", also matching "bazzoo" and "bar-baz"
    baz_yaml, rest = filter_yaml(rest, name='baz', kind='deployment')
    k8s_yaml(baz_yaml)

    # extract YAMLs of kind "deployment" exactly matching metadata.name "foo"
    foo_yaml, rest = filter_yaml(rest, name='^foo$', kind='deployment')
    k8s_yaml(foo_yaml)

  Args:
    yaml: Path(s) to YAML, or YAML as a ``Blob``.
    labels: return only entities matching these labels. (Matching entities
      must satisfy all of the specified label constraints, though they may have additional
      labels as well: see the `Kubernetes docs <https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/>`_
      for more info.)
    name: Case-insensitive regexp specifying the ``metadata.name`` property of entities to match
    namespace: Case-insensitive regexp specifying the ``metadata.namespace`` property of entities to match
    kind: Case-insensitive regexp specifying the kind of entities to match (e.g. "Service", "Deployment", etc.).
    api_version: Case-insensitive regexp specifying the apiVersion for `kind`, (e.g., "apps/v1")

  Returns:
    2-element tuple containing

    - **matching** (:class:`~api.Blob`): blob of YAML entities matching given filters
    - **rest** (:class:`~api.Blob`): the rest of the YAML entities
  """
  pass

def include(path: str):
  """Include another Tiltfile.

  Loads any builds or resources defined in that Tiltfile.

  If you want to define common functions or constants and
  import them into another Tiltfile, see the `load()` function.

  Example ::

    include('./frontend/Tiltfile')
    include('./backend/Tiltfile')
  """

def load(path: str, *args):
  """Include another Tiltfile.

  Similar to `include(path)`, but binds variables in the global scope.

  Used when you want to define common functions or constants
  to share across Tiltfiles.

  Example ::

    load('./lib/Tiltfile', 'create_namespace')
    create_namespace('frontend')

  If ``path`` starts with ``"ext://"`` the path will be treated as a `Tilt Extension <extensions.html>`_.

  Example ::

    load('ext://hello_world', 'hi') # Resolves to https://github.com/tilt-dev/tilt-extensions/blob/master/hello_world/Tiltfile
    hi() # prints "Hello world!"
  """

def local(command: Union[str, List[str]], quiet: bool = False, command_bat: str = "", echo_off: bool = False) -> Blob:
  """Runs a command on the *host* machine, waits for it to finish, and returns its stdout as a ``Blob``

  Args:
    command: Command to run. If a string, executed with ``sh -c`` on macOS/Linux, or ``cmd /S /C`` on Windows; if a list, will be passed to the operating system as program name and args.
    quiet: If set to True, skips printing output to log.
    command_bat: The command to run, expressed as a Windows batch command executed
      with ``cmd /S /C``. Takes precedence over the ``command`` parameter on Windows. Ignored on macOS/Linux.
    echo_off: If set to True, skips printing command to log. 
  """
  pass

def read_file(file_path: str, default: str = None) -> Blob:
  """
  Reads file and returns its contents.

  If the `file_path` does not exist and `default` is not `None`, `default` will be returned.
  In any other case, an error reading `file_path` will be a Tiltfile load error.

  Args:
    file_path: Path to the file locally (absolute, or relative to the location of the Tiltfile).
    default: If not `None` and the file at `file_path` does not exist, this value will be returned."""
  pass

def watch_file(file_path: str) -> None:
  """Watches a file. If the file is changed a re-exectution of the Tiltfile is triggered.

  Args:
    file_path: Path to the file locally (absolute, or relative to the location of the Tiltfile)."""


def kustomize(pathToDir: str) -> Blob:
  """Run `kustomize <https://github.com/kubernetes-sigs/kustomize>`_ on a given directory and return the resulting YAML as a Blob
  Directory is watched (see ``watch_file``). Checks for and uses separately installed kustomize first, if it exists. Otherwise,
  uses kubectl's kustomize. See `blog post <https://blog.tilt.dev/2020/02/04/are-you-my-kustomize.html>`_.

  Args:
    pathToDir: Path to the directory locally (absolute, or relative to the location of the Tiltfile)."""
  pass

def helm(pathToChartDir: str, name: str = "", namespace: str = "", values: Union[str, List[str]]=[], set: Union[str, List[str]]=[]) -> Blob:
  """Run `helm template <https://docs.helm.sh/helm/#helm-template>`_ on a given directory that contains a chart and return the fully rendered YAML as a Blob
  Chart directory is watched (See ``watch_file``).

  For more examples, see the `Helm Cookbook <helm.html>`_.

  Args:
    pathToChartDir: Path to the directory locally (absolute, or relative to the location of the Tiltfile).
    name: The release name. Equivalent to the helm `--name` flag
    namespace: The namespace to deploy the chart to. Equivalent to the helm `--namespace` flag
    values: Specify one or more values files (in addition to the `values.yaml` file in the chart). Equivalent to the Helm ``--values`` or ``-f`` flags (`see docs <https://helm.sh/docs/chart_template_guide/#values-files>`_).
    set: Specify one or more values. Equivalent to the Helm ``--set`` flag.
"""
  pass

def fail(msg: str) -> None:
  """Raises an error that cannot be intercepted. Can be used anywhere in a Tiltfile."""
  pass

def blob(contents: str) -> Blob:
  """Creates a Blob object that wraps the provided string. Useful for passing strings in to functions that expect a `Blob`, e.g. ``k8s_yaml``."""
  pass

def listdir(directory: str, recursive: bool = False) -> List[str]:
  """Returns all the files at the top level of the provided directory. If ``recursive`` is set to True, returns all files that are inside of the provided directory, recursively.

  Directory is watched (See ``watch_file``)."""
  pass

def k8s_kind(kind: str, api_version: str=None, *, image_json_path: Union[str, List[str]]=[], image_object_json_path: Dict=None):
  """Tells Tilt about a k8s kind.

  For CRDs that use images built by Tilt: call this with `image_json_path` or
  `image_object` to tell Tilt where in the CRD's spec the image is specified.

  For CRDs that do not use images built by Tilt, but have pods you want in a Tilt resource: call this without `image_json_path`, simply to specify that this type is a Tilt workload. Then call :meth:`k8s_resource` with `extra_pod_selectors` to specify which pods Tilt should associate with this resource.

  (Note the `*` in the signature means `image_json_path` must be passed as a keyword, e.g., `image_json_path="{.spec.image}"`)

  Example ::

    # Fission has a CRD named "Environment"
    k8s_yaml('deploy/fission.yaml')
    k8s_kind('Environment', image_json_path='{.spec.runtime.image}')

  Here's an example that specifies the image location in `a UselessMachine
  Custom Resource
  <https://github.com/tilt-dev/tilt/blob/master/integration/crd/Tiltfile#L8>`_.

  Args:
    kind: Case-insensitive regexp specifying he value of the `kind` field in the k8s object definition (e.g., `"Deployment"`)
    api_version: Case-insensitive regexp specifying the apiVersion for `kind`, (e.g., "apps/v1")
    image_json_path: Either a string or a list of string containing json path(s) within that kind's definition
      specifying images deployed with k8s objects of that type.
      This uses the k8s json path template syntax, described `here <https://kubernetes.io/docs/reference/kubectl/jsonpath/>`_.
    image_object: A specifier of the form `image_object={'json_path': '{.path.to.field}', 'repo_field': 'repo', 'tag_field': 'tag'}`.
      Used to tell Tilt how to inject images into Custom Resources that express the image repo and tag as separate fields.

  """
  pass

StructuredDataType = Union[
    Dict[str, Any],
    List[Any],
]

def decode_json(json: Union[str, Blob]) -> StructuredDataType:
  """
  Deserializes the given JSON into a starlark object

  Args:
    json: the JSON to deserialize
  """
  pass

def encode_json(obj: StructuredDataType) -> Blob:
  """
  Serializes the given starlark object into JSON.

  Only supports maps with string keys, lists, strings, ints, and bools.

  Args:
    obj: the object to serialize
  """
  pass

def read_json(path: str, default: str = None) -> StructuredDataType:
  """
  Reads the file at `path` and deserializes its contents as JSON

  If the `path` does not exist and `default` is not `None`, `default` will be returned.
  In any other case, an error reading `path` will be a Tiltfile load error.

  Args:
    path: Path to the file locally (absolute, or relative to the location of the Tiltfile).
    default: If not `None` and the file at `path` does not exist, this value will be returned."""
  pass

def read_yaml(path: str, default: StructuredDataType = None) -> StructuredDataType:
  """
  Reads the file at `path` and deserializes its contents into a starlark object

  If the `path` does not exist and `default` is not `None`, `default` will be returned.
  In any other case, an error reading `path` will be a Tiltfile load error.

  Args:
    path: Path to the file locally (absolute, or relative to the location of the Tiltfile).
    default: If not `None` and the file at `path` does not exist, this value will be returned."""
  pass

def read_yaml_stream(path: str, default: List[StructuredDataType] = None) -> List[StructuredDataType]:
  """
  Reads a yaml stream (i.e., yaml documents separated by ``"\\n---\\n"``) from the
  file at `path` and deserializes its contents into a starlark object

  If the `path` does not exist and `default` is not `None`, `default` will be returned.
  In any other case, an error reading `path` will be a Tiltfile load error.

  Args:
    path: Path to the file locally (absolute, or relative to the location of the Tiltfile).
    default: If not `None` and the file at `path` does not exist, this value will be returned."""
  pass

def decode_yaml(yaml: Union[str, Blob]) -> StructuredDataType:
  """
  Deserializes the given yaml document into a starlark object

  Args:
    yaml: the yaml to deserialize
  """
  pass

def decode_yaml_stream(yaml: Union[str, Blob]) -> List[StructuredDataType]:
  """
  Deserializes the given yaml stream (i.e., any number of yaml
  documents, separated by ``"\\n---\\n"``) into a list of starlark objects.

  Args:
    yaml: the yaml to deserialize
  """
  pass

def encode_yaml(obj: StructuredDataType) -> Blob:
  """
  Serializes the given starlark object into YAML.

  Only supports maps with string keys, lists, strings, ints, and bools.

  Args:
    obj: the object to serialize
  """
  pass

def encode_yaml_stream(objs: List[StructuredDataType]) -> Blob:
  """
  Serializes the given starlark objects into a YAML stream (i.e.,
  multiple YAML documents, separated by ``"\\n---\\n"``).

  Only supports maps with string keys, lists, strings, ints, and bools.

  Args:
    objs: the object to serialize
  """
  pass

def default_registry(host: str, host_from_cluster: str = None) -> None:
  """Specifies that any images that Tilt builds should be renamed so that they have the specified Docker registry.

  This is useful if, e.g., a repo is configured to push to Google Container Registry, but you want to use Elastic Container Registry instead, without having to edit a bunch of configs. For example, ``default_registry("gcr.io/myrepo")`` would cause ``docker.io/alpine`` to be rewritten to ``gcr.io/myrepo/docker.io_alpine``

  For more info, see our `Using a Personal Registry Guide <personal_registry.html>`_.

  Args:
    host: host of the registry that all built images should be renamed to use.
    host_from_cluster: registry host to use when referencing images from inside the cluster (i.e. in Kubernetes YAML). Only include this arg if it is different from ``host``. For more on this use case, `see this guide <personal_registry.html#different-urls-from-inside-your-cluster>`_.

  Images are renamed following these rules:

  1. Replace ``/`` and ``@`` with ``_``.

  2. Prepend the value of ``host`` and a ``/``.

  e.g., with ``default_registry('gcr.io/myorg')``, an image called ``user-service`` becomes ``gcr.io/myorg/user-service``.

  (Note: this logic is currently crude, on the assumption that development image names are ephemeral and unimportant. `Please let us know <https://github.com/tilt-dev/tilt/issues>`_ if they don't suit you!)
  """
  pass

def custom_build(ref: str, command: str, deps: List[str], tag: str = "", disable_push: bool = False, skips_local_docker: bool = False, live_update: List[LiveUpdateStep]=[], match_in_env_vars: bool = False, ignore: Union[str, List[str]] = [], entrypoint: Union[str, List[str]] = [], command_bat: str = ""):
  """Provide a custom command that will build an image.

  For examples on how to use this to integrate your own build scripts with Tilt,
  see the `Custom Build Script How-to <custom_build.html>`_.

  The command *must* publish an image with the name & tag ``$EXPECTED_REF``.

  Tilt will raise an error if the command exits successfully, but the registry does not contain
  an image with the ref ``$EXPECTED_REF``, unless you specify ``skips_local_docker=True``

  Example ::

    custom_build(
      'gcr.io/foo',
      'docker build -t $EXPECTED_REF .',
      ['.'],
    )

  Note: the ``entrypoint`` parameter is not supported for Docker Compose resources. If you need it for your use case, let us know.

  Args:
    ref: name for this image (e.g. 'myproj/backend' or 'myregistry/myproj/backend'). If this image will be used in a k8s resource(s), this ref must match the ``spec.container.image`` param for that resource(s).
    command: a command that, when run in the shell, builds an image puts it in the registry as ``ref``. Must produce an image named ``$EXPECTED_REF``  Executed with ``sh -c`` on macOS/Linux, or ``cmd /S /C`` on Windows.
    deps: a list of files or directories to be added as dependencies to this image. Tilt will watch those files and will rebuild the image when they change. Only accepts real paths, not file globs.
    tag: Some tools can't change the image tag at runtime. They need a pre-specified tag. Tilt will set ``$EXPECTED_REF = image_name:tag``,
       then re-tag it with its own tag before pushing to your cluster. See `the bazel guide <integrating_bazel_with_tilt.html>`_ for an example.
    disable_push: whether Tilt should push the image in to the registry that the Kubernetes cluster has access to. Set this to true if your command handles pushing as well.
    skips_local_docker: Whether your build command writes the image to your local Docker image store. Set this to true if you're using a cloud-based builder or independent image builder like ``buildah``.
    live_update: set of steps for updating a running container (see `Live Update documentation <live_update_reference.html>`_).
    match_in_env_vars: specifies that k8s objects can reference this image in their environment variables, and Tilt will handle those variables the same as it usually handles a k8s container spec's ``image`` s.
    ignore: set of file patterns that will be ignored. Ignored files will not trigger builds and will not be included in images. Follows the `dockerignore syntax <https://docs.docker.com/engine/reference/builder/#dockerignore-file>`_. Patterns/filepaths will be evaluated relative to each ``dep`` (e.g. if you specify ``deps=['dep1', 'dep2']`` and ``ignores=['foobar']``, Tilt will ignore both ``deps1/foobar`` and ``dep2/foobar``).
    entrypoint: command to run when this container starts. Takes precedence over the container's ``CMD`` or ``ENTRYPOINT``, and over a `container command specified in k8s YAML <https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/>`_. If specified as a string, will be evaluated in a shell context (e.g. ``entrypoint="foo.sh bar"`` will be executed in the container as ``/bin/sh -c 'foo.sh bar'``); if specifed as a list, will be passed to the operating system as program name and args.
    command_bat: The command to run, expressed as a Windows batch command executed
      with ``cmd /S /C``. Takes precedence over the ``command`` parameter on Windows. Ignored on macOS/Linux.
  """
  pass


class K8sObjectID:
  """
  Attributes:
    name (str): The object's name (e.g., `"my-service"`)
    kind (str): The object's kind (e.g., `"deployment"`)
    namespace (str): The object's namespace (e.g., `"default"`)
    group (str): The object's group (e.g., `"apps"`)
  """
  pass


def workload_to_resource_function(fn: Callable[[K8sObjectID], str]) -> None:
    """
    Provide a function that will be used to name `Tilt resources <tiltfile_concepts.html#resources>`_.

    Tilt will auto-generate resource names for you. If you do not like the names
    it generates, you can use this to customize how Tilt generates names.

    Example ::

      # name all tilt resources after the k8s object namespace + name
      def resource_name(id):
        return id.namespace + '-' + id.name
      workload_to_resource_function(resource_name)

    The names it generates must be unique (i.e., two workloads can't map to the
    same resource name).

    Args:
      fn: A function that takes a :class:`K8sObjectID` and returns a `str`.
          Tilt will call this function once for each workload to determine that workload's resource's name.
    """

    pass

def k8s_context() -> str:
  """Returns the name of the Kubernetes context Tilt is connecting to.

  Example ::

    if k8s_context() == 'prod':
      fail("failing early to avoid overwriting prod")
  """
  pass

def allow_k8s_contexts(contexts: Union[str, List[str]]) -> None:
  """Specifies that Tilt is allowed to run against the specified k8s context names.

  To help reduce the chances you accidentally use Tilt to deploy to your
  production cluster, Tilt will only push to clusters that have been whitelisted
  for local development.

  By default, Tilt whitelists Minikube, Docker for Desktop, Microk8s, Red Hat CodeReady Containers, Kind, K3D, and Krucible.

  To whitelist your development cluster, add a line in your Tiltfile:

  `allow_k8s_contexts('context-name')`

  where 'context-name' is the name returned by `kubectl config current-context`.

  For more on which cluster context is right for you, see `Choosing a Local Dev Cluster <choosing_clusters.html>`_.

  Args:
    contexts: a string or list of strings, specifying one or more k8s context
        names that Tilt is allowed to run in. This list is in addition to
        the default of all known-local clusters.

  Example ::

    allow_k8s_contexts('my-staging-cluster')

    allow_k8s_contexts(['my-staging-cluster', 'gke_some-project-123456_us-central1-b_windmill'])
  """
  pass

def enable_feature(feature_name: str) -> None:
  """Configures Tilt to enable non-default features (e.g., experimental or deprecated).

  The Tilt features controlled by this are generally in an unfinished state, and
  not yet documented.

  As a Tiltfile author, you don't need to worry about this function unless something
  else directs you to (e.g., an experimental feature doc, or a conversation with a
  Tilt contributor).

  As a Tiltfile reader, you can probably ignore this, or you can ask the person
  who added it to the Tiltfile what it's doing there.

  Args:
    feature_name: name of the feature to enable
  """
  pass

def local_resource(name: str, cmd: Union[str, List[str]],
                   deps: Union[str, List[str]] = None,
                   trigger_mode: TriggerMode = TRIGGER_MODE_AUTO,
                   resource_deps: List[str] = [], ignore: Union[str, List[str]] = [],
                   auto_init: bool=True, serve_cmd: str = "", cmd_bat: str = "",
                   serve_cmd_bat: str = "") -> None:
  """Configures one or more commands to run on the *host* machine (not in a remote cluster).

  By default, Tilt performs an update on local resources on ``tilt up`` and whenever any of their ``deps`` change.

  When Tilt performs an update on a local resource:

  - if `cmd` is non-empty, it is executed
  - if `cmd` succeeds:
    - Tilt kills any extant `serve_cmd` process from previous updates of this resource
    - if `serve_cmd` is non-empty, it is executed

  For more info, see the `Local Resource docs <local_resource.html>`_.

  Args:
    name: will be used as the new name for this resource
    cmd: command to be executed on host machine.  If a string, executed with ``sh -c`` on macOS/Linux, or ``cmd /S /C`` on Windows; if a list, will be passed to the operating system as program name and args.
    deps: a list of files or directories to be added as dependencies to this cmd. Tilt will watch those files and will run the cmd when they change. Only accepts real paths, not file globs.
    trigger_mode: one of ``TRIGGER_MODE_AUTO`` or ``TRIGGER_MODE_MANUAL``. For more info, see the
      `Manual Update Control docs <manual_update_control.html>`_.
    resource_deps: a list of resources on which this resource depends.
      See the `Resource Dependencies docs <resource_dependencies.html>`_.
    ignore: set of file patterns that will be ignored. Ignored files will not trigger runs. Follows the `dockerignore syntax <https://docs.docker.com/engine/reference/builder/#dockerignore-file>`_. Patterns will be evaluated relative to the Tiltfile.
    auto_init: whether this resource runs on ``tilt up``. Defaults to ``True``. Note that ``auto_init=False`` is only compatible with ``trigger_mode=TRIGGER_MODE_MANUAL``.
    serve_cmd: Tilt will run this command on update and expect it to not exit.
      Executed with ``sh -c`` on macOS/Linux, or ``cmd /S /C`` on Windows.
    cmd_bat: The command to run, expressed as a Windows batch command executed
      with ``cmd /S /C``. Takes precedence over the ``cmd`` parameter on Windows. Ignored on macOS/Linux.
    serve_cmd_bat: The command to run, expressed as a Windows batch command executed
      with ``cmd /S /C``. Takes precedence over the ``serve_cmd`` parameter on Windows. Ignored on macOS/Linux.
  """
  pass

def disable_snapshots() -> None:
    """Disables Tilt's `snapshots <snapshots.html>`_ feature, hiding it from the UI.

    This is intended for use in projects where there might be some kind of
    data policy that does not allow developers to upload snapshots to TiltCloud.

    Note that this directive does not provide any real security, since a
    developer can always simply edit it out of the Tiltfile, but it at least
    ensures a pretty high bar of intent.
    """

def docker_prune_settings(disable: bool=True, max_age_mins: int=360,
                          num_builds: int=0, interval_hrs: int=1, keep_recent: int=2) -> None:
  """
  Configures Tilt's Docker Pruner, which runs occasionally in the background and prunes Docker images associated
  with your current project.

  The pruner runs soon after startup (as soon as at least some resources are declared, and there are no pending builds).
  Subsequently, it runs after every ``num_builds`` Docker builds, or, if ``num_builds`` is not set, every ``interval_hrs`` hours.

  The pruner will prune:
    - stopped containers built by Tilt that are at least ``max_age_mins`` mins old
    - images built by Tilt and associated with this Tilt run that are at least ``max_age_mins`` mins old,
      and not in the ``keep_recent`` most recent builds for that image name
    - dangling build caches that are at least ``max_age_mins`` mins old

  Args:
    disable: if true, disable the Docker Pruner
    max_age_mins: maximum age, in minutes, of images/containers to retain. Defaults to 360 mins., i.e. 6 hours
    num_builds: number of Docker builds after which to run a prune. (If unset, the pruner instead runs every ``interval_hrs`` hours)
    interval_hrs: run a Docker Prune every ``interval_hrs`` hours (unless ``num_builds`` is set, in which case use the "prune every X builds" logic). Defaults to 1 hour
    keep_recent: when pruning, retain at least the ``keep_recent`` most recent images for each image name. Defaults to 2
  """
  pass

def analytics_settings(enable: bool) -> None:
  """Overrides Tilt telemetry.

  By default, Tilt does not send telemetry. After you successfully run a Tiltfile,
  the Tilt web UI will nudge you to opt in or opt out of telemetry.

  The Tiltfile can override these telemetry settings, for teams
  that always want telemetry enabled or disabled.

  Args:
    enable: if true, telemetry will be turned on. If false, telemetry will be turned off.
  """
  pass

def version_settings(check_updates: bool = True, constraint: str = "") -> None:
  """Controls Tilt's behavior with regard to its own version.

  Args:
    check_updates: If true, Tilt will check GitHub for new versions of itself
                   and display a notification in the web UI when an upgrade is
                   available.
    constraint: If non-empty, Tilt will check its currently running version against
                this constraint and generate an error if it doesn't match.
                Examples:

                - `<0.13.0` - less than 0.13.0
                - `>=0.12.0` - at least 0.12.0

                See more at the `constraint syntax documentation <https://github.com/blang/semver#ranges>`_.
  """

def struct(**kwargs) -> Any:
  """Creates an object with arbitrary fields.

  Examples:

  .. code-block:: python

    x = struct(a="foo", b=6)
    print("%s %d" % (x.a, x.b)) # prints "foo 6"
  """


def secret_settings(disable_scrub: bool = False) -> None:
  """Configures Tilt's handling of Kubernetes Secrets. By default, Tilt scrubs
  the text of any Secrets from the logs; e.g. if Tilt applies a Secret with contents
  'mysecurepassword', Tilt redacts this string if ever it appears in the logs,
  to prevent users from accidentally sharing sensitive information in snapshots etc.

  If you need other configuration options, `let us know <https://github.com/tilt-dev/tilt/issues>`_.

  Args:
    disable_scrub: if True, Tilt will *not* scrub secrets from logs.
"""


def update_settings(max_parallel_updates: int=3, k8s_upsert_timeout_secs: int=30) -> None:
  """Configures Tilt's updates to your resources. (An update is any execution of or
  change to a resource. Examples of updates include: doing a docker build + deploy to
  Kubernetes; running a live update on an existing container; and executing
  a local resource command).

  If you need other configuration options, `let us know <https://github.com/tilt-dev/tilt/issues>`_.

  Args:
    max_parallel_updates: maximum number of updates Tilt will execute in parallel. Default is 3. Must be a positive integer.
    k8s_upsert_timeout_secs: timeout (in seconds) for Kubernetes upserts (i.e. ``create``/``apply`` calls). Minimum value is 1.
"""
