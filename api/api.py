from typing import Dict, Union, List, Callable, Any

class Blob:
  """The result of executing a command on your local system.

   Under the hood, a `Blob` is just a string, but we wrap it this way so Tilt knows the difference between a string meant to convey content and a string indicating, say, a filepath.

   To wrap a string as a blob, call ``blob(my_str)``"""

def docker_build(ref: str, context: str, build_args: Dict[str, str] = {}, dockerfile: str = "Dockerfile", dockerfile_contents: Union[str, Blob] = "") -> None:
  """Builds a docker image.

  Note that you can't set both the `dockerfile` and `dockerfile_contents` arguments (will throw an error).

  Example: ``docker_build('myregistry/myproj/backend', '/path/to/code')`` is roughly equivalent to the call ``docker build /path/to/code -t myregistry/myproj/backend``

  Args:
    ref: name for this image (e.g. 'myproj/backend' or 'myregistry/myproj/backend'). If this image will be used in a k8s resource(s), this ref must match the ``spec.container.image`` param for that resource(s).
    context: path to use as the Docker build context.
    build_args: build-time variables that are accessed like regular environment variables in the ``RUN`` instruction of the Dockerfile. See `the Docker Build Arg documentation <https://docs.docker.com/engine/reference/commandline/build/#set-build-time-variables---build-arg>`_
    dockerfile: path to the Dockerfile to build
    dockerfile_contents: raw contents of the Dockerfile to use for this build
  """
  pass

class k8sObjectID:
  """
  Attributes:
      name (str): The object's name (e.g., `"my-service"`)
      kind (str): The object's kind (e.g., `"deployment"`)
      namespace (str): The object's namespace (e.g., `"default"`)
      group (str): The object's group (e.g., `"apps"`)
  """
  pass

class FastBuild:
  """An image that was created with ``fast_build``"""
  def add(self, src: str, dest: str) -> 'FastBuild':
    """Adds the content from ``src`` into the image at path ``dest``.

    Args:
      src: The path to content to be added to the image (absolute, or relative to the location of the Tiltfile).
      dest: The path in the image where the content should be added.

    """
    pass

  def run(self, cmd: str, trigger: Union[List[str], str] = []) -> None:
    """Runs ``cmd`` as a build step in the image.

    Args:
      cmd: A shell command.
      trigger: If the ``trigger`` argument is specified, the build step is only run on changes to the given file(s).
    """
    pass

  def hot_reload() -> None:
    """Setting this on a ``FastBuild`` image tells Tilt that this container knows how to automatically reload any changes in the container. As a result there is no need to restart it.

    This is useful for containers that run something like nodemon or webpack Hot Module Replacement to update running processes quickly."""
    pass


def fast_build(img_name: str, dockerfile_path: str, entrypoint: str = "") -> FastBuild:
  """Initiates a docker image build that supports ``add`` s and ``run`` s, and that uses a cache for subsequent builds.

    See the `fast build documentation <https://docs.tilt.dev/fast_build.html>`_.
  """
  pass

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

def k8s_resource(workload: str, new_name: str = "",
                 port_forwards: Union[str, int, List[int]] = [],
                 extra_pod_selectors: Union[Dict[str, str], List[Dict[str, str]]] = []) -> None:
  """Configures a kubernetes resources

  This description apply to `k8s_resource_assembly_version` 2.
  If you are running Tilt version < 0.8.0 and/or do not call `k8s_resource_assembly_version(2)`, see
  :meth:`k8s_resource_v1_DEPRECATED` instead.

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
    port_forwards: Local ports to connect to the pod. If no
      target port is specified, will use the first container port.
      Example values: 9000 (connect localhost:9000 to the default container port),
      '9000:8000' (connect localhost:9000 to the container port 8000),
      ['9000:8000', '9001:8001'] (connect localhost:9000 and :9001 to the
      container ports 8000 and 8001, respectively).
    extra_pod_selectors: In addition to relying on Tilt's heuristics to automatically
      find K8S resources associated with this resource, a user may specify extra
      labelsets to force entities to be associated with this resource. An entity
      will be associated with this resource if it has all of the labels in at
      least one of the entries specified (but still also if it meets any of
      Tilt's usual mechanisms).
  """

  pass

def k8s_resource_assembly_version(version: int) -> None:
  """
  Specifies which version of k8s resource assembly loading to use.

  This function is deprecated and will be removed.
  See `Resource Assembly Migration </resource_assembly_migration.html>`_ for information.

  Changes the behavior of :meth:`k8s_resource`.
  """

def k8s_resource_v1_DEPRECATED(name: str, yaml: Union[str, Blob] = "", image: Union[str, FastBuild] = "",
    port_forwards: Union[str, int, List[int]] = [], extra_pod_selectors: Union[Dict[str, str], List[Dict[str, str]]] = []) -> None:
  """NOTE: This is actually named :meth:`k8s_resource`. This documents
  the behavior of this method after a call to :meth:`k8s_resource_assembly_version` with value `1`.
  This behavior is deprecated and will be removed.
  See `Resource Assembly Migration </resource_assembly_migration.html>`_ for information.

  Creates a kubernetes resource that tilt can deploy using the specified image.

  Args:
    name: What call this resource in the UI. If ``image`` is not specified ``name`` will be used as the image to group by.
    yaml: Optional YAML. If this arg is not passed, we
      expect to be able to extract it from an existing resource
      (by looking for a k8s container running the specified ``image``).
    image: An optional Image. If the image is not passed,
      we expect to be able to extract it from an existing resource.
    port_forwards: Local ports to connect to the pod. If no
      target port is specified, will use the first container port.
      Example values: 9000 (connect localhost:9000 to the default container port),
      '9000:8000' (connect localhost:9000 to the container port 8000),
      ['9000:8000', '9001:8001'] (connect localhost:9000 and :9001 to the
      container ports 8000 and 8001, respectively).
    extra_pod_selectors: In addition to relying on Tilt's heuristics to automatically
      find K8S resources associated with this resource, a user may specify extra
      labelsets to force entities to be associated with this resource. An entity
      will be associated with this resource if it has all of the labels in at
      least one of the entries specified (but still also if it meets any of
      Tilt's usual mechanisms).
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

def helm(pathToChartDir: str) -> Blob:
  """Run `helm template <https://docs.helm.sh/helm/#helm-template>`_ on a given directory that contains a chart and return the fully rendered YAML as a Blob
  Chart directory is watched (See ``watch_file``).

  Args:
    pathToChartDir: Path to the directory locally (absolute, or relative to the location of the Tiltfile)."""
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

def k8s_kind(kind: str, api_version: str=None, *, image_json_path: Union[str, List[str]]):
  """Tells Tilt about a k8s kind. Primarily intended for defining where your CRD specifies image names.

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

JSONType = Union[
    Dict[str, Any],
    List[Any],
]

def decode_json(json: str) -> JSONType:
  """Deserializes a given string from JSON to Starlark. Fails if the string can't be parsed as JSON."""
  pass

def read_json(path: str, default: str = None) -> JSONType:
  """
  Reads the file at `path` and deserializes its contents as JSON

  If the `path` does not exist and `default` is not `None`, `default` will be returned.
  In any other case, an error reading `path` will be a Tiltfile load error.

  Args:
    path: Path to the file locally (absolute, or relative to the location of the Tiltfile).
    default: If not `None` and the file at `path` does not exist, this value will be returned."""
  pass

def default_registry(registry: str) -> None:
  """Specifies that any images that Tilt builds should be renamed so that they have the specified docker registry.

  This is useful if, e.g., a repo is configured to push to Google Container Registry, but you want to use Elastic Container Registry instead, without having to edit a bunch of configs. For example, `default_registry("gcr.io/myrepo")` would cause `docker.io/alpine` to be rewritten to `gcr.io/myrepo/docker.io_alpine`

  Args:
    registry: The registry that all built images should be renamed to use.

  Images are renamed following these rules:
  1. Replace `/` and `@` with `_`.
  2. Prepend the value of `registry` and a `/`.

  e.g., with `default_registry('gcr.io/myorg')`, `user-service` becomes `gcr.io/myorg/user-service`.

  (Note: this logic is currently crude, on the assumption that development image names are ephemeral and unimportant. `Please let us know <https://github.com/windmilleng/tilt/issues>`_ if they don't suit you!)

  Cf. our `using a personal registry guide <https://docs.tilt.dev/personal_registry.html>`_
  """
  pass

class CustomBuild:
  """An image that was created with ``custom_build``"""
  def add_fast_build() -> FastBuild:
    """Returns a FastBuild that is associated with the image that was built from a ``custom_build``. When the container needs to be rebuilt it will be built using the ``CustomBuild``. Otherwise update will be done with the ``FastBuild`` instructions. """
    pass

def custom_build(ref: str, command: str, deps: List[str], tag: str = "", disable_push: bool = False) -> CustomBuild:
  """Provide a custom command that will build an image.

  Returns an object which can be used to create a FastBuild.

  It will raise an error if the specified ref is not published in the registry with the name+tag that is provided via the ``$EXPECTED_REF`` environment variable.

  Example ::

    k8s_yaml('deploy/fission.yaml')
    k8s_kind('Environment', image_json_path='{.spec.runtime.image}')
    custom_build(
      'gcr.io/foo',
      'docker build -t $EXPECTED_REF .',
      ['.'],
    )

  Args:
    ref: name for this image (e.g. 'myproj/backend' or 'myregistry/myproj/backend'). If this image will be used in a k8s resource(s), this ref must match the ``spec.container.image`` param for that resource(s).
    command: a command that, when run in the shell, builds an image puts it in the registry as ``ref``. Must produce an image named ``$EXPECTED_REF``
    deps: a list of files or directories to be added as dependencies to this image. Tilt will watch those files and will rebuild the image when they change.
    tag: the tag you expect the resulting image to have; we set ``$EXPECTED_REF=imagename:tag`` and use this value to verify that the command produced the correct image. (If ``tag`` is not specified, Tilt will set the expected ref to ``imagename:<tilt-generated temporary tag>``.)
    disable_push: whether Tilt should push the image in to the registry that the Kubernetes cluster has access to. Set this to true if your command handles pushing as well.
  """
  pass

def workload_to_resource_function(fn: Callable[[k8sObjectID], str]) -> None:
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
      fn: A function that takes a :class:`k8sObjectID` and returns a `str`.
          Tilt will call this function once for each workload to determine that workload's resource's name.
    """

    pass
