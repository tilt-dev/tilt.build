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
  """Specify that a container should be restarted when it is live-updated.

  May only be included in a `live_update` once, and only as the last step.

  Only works on containers managed by Docker. For non-Docker runtimes
  (e.g. containerd, CRI-O), please see the `wrapper script for simulating
  restart_container <https://github.com/windmilleng/rerun-process-wrapper>`_.

  For more info, see the `Live Update Reference <live_update_reference.html>`_.
  """
  pass

def docker_build(ref: str, context: str, build_args: Dict[str, str] = {}, dockerfile: str = "Dockerfile", dockerfile_contents: Union[str, Blob] = "", live_update: List[LiveUpdateStep]=[], match_in_env_vars: bool = False, ignore: Union[str, List[str]] = [], only: Union[str, List[str]] = [], entrypoint: str = "", target: str = "", ssh: Union[str, List[str]] = "") -> None:
  """Builds a docker image.

  Note that you can't set both the `dockerfile` and `dockerfile_contents` arguments (will throw an error).

  Example: ``docker_build('myregistry/myproj/backend', '/path/to/code')`` is roughly equivalent to the call ``docker build /path/to/code -t myregistry/myproj/backend``

  Note: If you're using the the `ignore` and `only` parameters to do context filtering and you have tricky cases, reach out to us. The implementation is complex and there might be edge cases.

  Note: the `entrypoint` parameter is not supported for Docker Compose resources. If you need it for your use case, let us know.

  Args:
    ref: name for this image (e.g. 'myproj/backend' or 'myregistry/myproj/backend'). If this image will be used in a k8s resource(s), this ref must match the ``spec.container.image`` param for that resource(s).
    context: path to use as the Docker build context.
    build_args: build-time variables that are accessed like regular environment variables in the ``RUN`` instruction of the Dockerfile. See `the Docker Build Arg documentation <https://docs.docker.com/engine/reference/commandline/build/#set-build-time-variables---build-arg>`_.
    dockerfile: path to the Dockerfile to build.
    dockerfile_contents: raw contents of the Dockerfile to use for this build.
    live_update: set of steps for updating a running container (see `Live Update documentation <live_update_reference.html>`_).
    match_in_env_vars: specifies that k8s objects can reference this image in their environment variables, and Tilt will handle those variables the same as it usually handles a k8s container spec's ``image`` s.
    ignore: set of file patterns that will be ignored. Ignored files will not trigger builds and will not be included in images. Follows the `dockerignore syntax <https://docs.docker.com/engine/reference/builder/#dockerignore-file>`_.
    only: set of file paths that should be considered for the build. All other changes will not trigger a build and will not be included in images. Inverse of ignore parameter. Only accepts real paths, not file globs.
    entrypoint: command to run when this container starts. Takes precedence over the container's ``CMD`` or ``ENTRYPOINT``, and over a `container command specified in k8s YAML <https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/>`_. Will be evaluated in a shell context: e.g. ``entrypoint="foo.sh bar"`` will be executed in the container as ``/bin/sh -c 'foo.sh bar'``.
    target: Specify a build stage in the Dockerfile. Equivalent to the ``docker build --target`` flag.
    ssh: Include SSH secrets in your build. Use ssh='default' to clone private repositories inside a Dockerfile. Uses the syntax in the `Docker build --ssh flag <https://docs.docker.com/develop/develop-images/build_enhancements/#using-ssh-to-access-private-data-in-builds>`_.
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

def k8s_resource(workload: str, new_name: str = "",
                 port_forwards: Union[str, int, List[int]] = [],
                 extra_pod_selectors: Union[Dict[str, str], List[Dict[str, str]]] = [],
                 trigger_mode: TriggerMode = TRIGGER_MODE_AUTO, resource_deps: List[str] = []) -> None:
  """Configures the Kubernetes resource of the given name. Tilt assembles Kubernetes resources
  automatically, as described in `Tiltfile Concepts: Resources <tiltfile_concepts.html#resources>`_).
  Calling ``k8s_resource`` is *optional*; you can use this function to configure port forwarding for
  your resource, to rename it, or to adjust any of the other settings specified below.

  Args:
    workload: which workload's resource to configure. This is a colon-separated
      string consisting of one or more of (name, kind, namespace, group), e.g.,
      "redis", "redis:deployment", or "redis:deployment:default".
      `k8s_resource` searches all loaded k8s workload objects for an object matching
      all given fields. If there's exactly one, `k8s_resource` configures options for
      that workload. If there's not exactly one, `k8s_resource` raises an error.
      (e.g., "redis" suffices if there's only one object named "redis", but if
      there's both a deployment and a cronjob named "redis", you'd need to specify
      "redis:deployment").
    new_name: if non-empty, will be used as the new name for this resource
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
      find K8S resources associated with this resource, a user may specify extra
      labelsets to force entities to be associated with this resource. An entity
      will be associated with this resource if it has all of the labels in at
      least one of the entries specified (but still also if it meets any of
      Tilt's usual mechanisms).
    trigger_mode: one of ``TRIGGER_MODE_AUTO`` or ``TRIGGER_MODE_MANUAL``. For more info, see the
      `Manual Update Control docs <manual_update_control.html>`_.
    resource_deps: a list of resources on which this resource depends.
      See the `Resource Dependencies docs <resource_dependencies.html>`_.
  """
  pass

def filter_yaml(yaml: Union[str, List[str], Blob], labels: dict=None, name: str=None, namespace: str=None, kind: str=None, api_version: str=None):
  """Call this with a path to a file that contains YAML, or with a ``Blob`` of YAML.
  (E.g. it can be called on the output of ``kustomize`` or ``helm``.)

  Captures the YAML entities that meet the filter criteria and returns them as a blob;
  returns the non-matching YAML as the second return value.

  For example, if you have a file of *all* your YAML, but only want to pass a few elements to Tilt: ::

    # extract all YAMLs matching labels "app=foobar"
    foobar_yaml, rest = filter_yaml('all.yaml', labels={'app': 'foobar'}
    k8s_yaml(foobar_yaml)

    # extract YAMLs of kind "deployment" with metadata.name "baz"
    baz_yaml, rest = filter_yaml(rest, name='baz', kind='deployment')
    k8s_yaml(baz_yaml)

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
  """

def local(cmd: str) -> Blob:
  """Runs cmd, waits for it to finish, and returns its stdout as a ``Blob``."""
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
  Directory is watched (See ``watch_file``).

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

def k8s_kind(kind: str, api_version: str=None, *, image_json_path: Union[str, List[str]]=[]):
  """Tells Tilt about a k8s kind.

  For CRDs that use images built by Tilt: call this with `image_json_path` to tell Tilt where in the CRD's spec the image is specified.

  For CRDs that do not use images built by Tilt, but have pods you want in a Tilt resource: call this without `image_json_path`, simply to specify that this type is a Tilt workload. Then call :meth:`k8s_resource` with `extra_pod_selectors` to specify which pods Tilt should associate with this resource.

  (Note the `*` in the signature means `image_json_path` must be passed as a keyword, e.g., `image_json_path="{.spec.image}"`)

  Example ::

    # Fission has a CRD named "Environment"
    k8s_yaml('deploy/fission.yaml')
    k8s_kind('Environment', image_json_path='{.spec.runtime.image}')

  Args:
    kind: Case-insensitive regexp specifying he value of the `kind` field in the k8s object definition (e.g., `"Deployment"`)
    api_version: Case-insensitive regexp specifying the apiVersion for `kind`, (e.g., "apps/v1")
    image_json_path: Either a string or a list of string containing json path(s) within that kind's definition
      specifying images deployed with k8s objects of that type.
      This uses the k8s json path template syntax, described `here <https://kubernetes.io/docs/reference/kubectl/jsonpath/>`_.
  """
  pass

StructuredDataType = Union[
    Dict[str, Any],
    List[Any],
]

def decode_json(json: str) -> StructuredDataType:
  """Deserializes a given string from JSON to Starlark. Fails if the string can't be parsed as JSON."""
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

def read_yaml(path: str, default: str = None) -> StructuredDataType:
  """
  Reads the file at `path` and deserializes its contents as YAML

  If the `path` does not exist and `default` is not `None`, `default` will be returned.
  In any other case, an error reading `path` will be a Tiltfile load error.

  Args:
    path: Path to the file locally (absolute, or relative to the location of the Tiltfile).
    default: If not `None` and the file at `path` does not exist, this value will be returned."""
  pass

def default_registry(registry: str) -> None:
  """Specifies that any images that Tilt builds should be renamed so that they have the specified Docker registry.

  This is useful if, e.g., a repo is configured to push to Google Container Registry, but you want to use Elastic Container Registry instead, without having to edit a bunch of configs. For example, ``default_registry("gcr.io/myrepo")`` would cause ``docker.io/alpine`` to be rewritten to ``gcr.io/myrepo/docker.io_alpine``

  For more info, see our `Using a Personal Registry Guide <personal_registry.html>`_.

  Args:
    registry: The registry that all built images should be renamed to use.

  Images are renamed following these rules:

  1. Replace ``/`` and ``@`` with ``_``.

  2. Prepend the value of ``registry`` and a ``/``.

  e.g., with ``default_registry('gcr.io/myorg')``, ``user-service`` becomes ``gcr.io/myorg/user-service``.

  (Note: this logic is currently crude, on the assumption that development image names are ephemeral and unimportant. `Please let us know <https://github.com/windmilleng/tilt/issues>`_ if they don't suit you!)
  """
  pass

def custom_build(ref: str, command: str, deps: List[str], tag: str = "", disable_push: bool = False, skips_local_docker: bool = False, live_update: List[LiveUpdateStep]=[], match_in_env_vars: bool = False, ignore: Union[str, List[str]] = [], entrypoint: str=""):
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
    command: a command that, when run in the shell, builds an image puts it in the registry as ``ref``. Must produce an image named ``$EXPECTED_REF``
    deps: a list of files or directories to be added as dependencies to this image. Tilt will watch those files and will rebuild the image when they change. Only accepts real paths, not file globs.
    tag: Some tools can't change the image tag at runtime. They need a pre-specified tag. Tilt will set ``$EXPECTED_REF = image_name:tag``,
       then re-tag it with its own tag before pushing to your cluster. See `the bazel guide <integrating_bazel_with_tilt.html>`_ for an example.
    disable_push: whether Tilt should push the image in to the registry that the Kubernetes cluster has access to. Set this to true if your command handles pushing as well.
    skips_local_docker: Whether your build command writes the image to your local Docker image store. Set this to true if you're using a cloud-based builder or independent image builder like ``buildah``.
    live_update: set of steps for updating a running container (see `Live Update documentation <live_update_reference.html>`_).
    match_in_env_vars: specifies that k8s objects can reference this image in their environment variables, and Tilt will handle those variables the same as it usually handles a k8s container spec's ``image`` s.
    ignore: set of file patterns that will be ignored. Ignored files will not trigger builds and will not be included in images. Follows the `dockerignore syntax <https://docs.docker.com/engine/reference/builder/#dockerignore-file>`_.
    entrypoint: command to run when this container starts. Takes precedence over the container's ``CMD`` or ``ENTRYPOINT``, and over a `container command specified in k8s YAML <https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/>`_. Will be evaluated in a shell context: e.g. ``entrypoint="foo.sh bar"`` will be executed in the container as ``/bin/sh -c 'foo.sh bar'``.
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
  production cluster, Tilt will error unless at least one of these is true of
  the active K8S context (i.e., what is returned by `kubectl config current-context`)

  1. The K8S API URL is on localhost.
  2. The context name is one of a few known local context names (e.g,. "minikube").
  3. The context name is explicitly passed to `allow_k8s_contexts` in the Tiltfile.

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

def local_resource(name: str, cmd: str, deps: Union[str, List[str]] = None,
                   trigger_mode: TriggerMode = TRIGGER_MODE_AUTO,
                   resource_deps: List[str] = [], ignore: Union[str, List[str]] = [],
                   auto_init: bool=True) -> None:
  """Configures `cmd` to run on the *host* machine (not in a remote cluster).

  If `deps` is set then `cmd` is run whenever one of the files specified changes.

  All local resources are executed on the first run of the Tiltfile.

  Args:
    name: will be used as the new name for this resource
    cmd: command to be executed on host machine
    deps: a list of files or directories to be added as dependencies to this cmd. Tilt will watch those files and will run the cmd when they change. Only accepts real paths, not file globs.
    trigger_mode: one of ``TRIGGER_MODE_AUTO`` or ``TRIGGER_MODE_MANUAL``. For more info, see the
      `Manual Update Control docs <manual_update_control.html>`_.
    resource_deps: a list of resources on which this resource depends.
      See the `Resource Dependencies docs <resource_dependencies.html>`_.
    ignore: set of file patterns that will be ignored. Ignored files will not trigger runs. Follows the `dockerignore syntax <https://docs.docker.com/engine/reference/builder/#dockerignore-file>`_.
    auto_init: whether this resource runs on ``tilt up``. Defaults to ``True``. Note that ``auto_init=False`` is only compatible with ``trigger_mode=TRIGGER_MODE_MANUAL``.

  For more info, see the `Local Resource docs <local_resource.html>`_.
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

def docker_prune_settings(disable: bool=True, max_age_mins: int=360, num_builds: int=0, interval_hrs: int=1) -> None:
  """
  Configures Tilt's Docker Pruner, which runs occasionally in the background and prunes Docker images associated
  with your current project.

  The pruner runs soon after startup (as soon as at least some resources are declared, and there are no pending builds).
  Subsequently, it runs after every ``num_builds`` Docker builds, or, if ``num_builds`` is not set, every ``interval_hrs`` hours.

  The pruner will prune:
    - stopped containers built by Tilt that are at least ``max_age_mins`` mins old
    - images built by Tilt and associated with this Tilt run that are at least ``max_age_mins`` mins old
    - dangling build caches that are at least ``max_age_mins`` mins old

  Args:
    disable: if true, disable the Docker Pruner
    max_age_mins: maximum age, in minutes, of images/containers to retain. Defaults to 360 mins., i.e. 6 hours
    num_builds: number of Docker builds after which to run a prune. (If unset, the pruner instead runs every ``interval_hrs`` hours)
    interval_hrs: run a Docker Prune every ``interval_hrs`` hours (unless ``num_builds`` is set, in which case use the "prune every X builds" logic). Defaults to 1 hour
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

def version_settings(check_updates: bool) -> None:
  """Controls whether Tilt will display a notification in the web UI when there is a new version available.
  By default this is set to True.

  Args:
    check_updates: whether or not to check for new versions of Tilt on GitHub.
  """

def struct(**kwargs) -> Any:
  """Creates an object with arbitrary fields.

  Examples:

  .. code-block:: python

    x = struct(a="foo", b=6)
    print("%s %d" % (x.a, x.b)) # prints "foo 6"
  """

def update_settings(max_parallel_updates: int) -> None:
  """Configures Tilt's updates to your resources. (An update is any execution of or
  change to a resource. Examples of updates include: doing a docker build + deploy to
  Kubernetes; running a live update on an existing container; and executing
  a local resource command).

  Expect more settings to be configurable from this function soon.

  Args:
    max_parallel_updates: maximum number of updates Tilt will execute in parallel. Default is 3. Must be a positive integer.
"""
