---
tilt: Integrating Bazel with Tilt
layout: docs
---

# Integrating Bazel with Tilt
Bazel provides a deterministic build process that, coupled with [rules_docker](https://github.com/bazelbuild/rules_docker) maximizes container layer caching and can even deploy to Kubernetes with [rules_k8s](https://github.com/bazelbuild/rules_k8s). In this guide we'll walk through how to use `local` and `custom_build` to integrate such a Bazel setup with your Tiltfile.

_Note: Before diving in to this guide you should have run through [Tilt's Getting Started Guide](tutorial.html) and the deep dive in to [Tiltfile concepts](tiltfile_concepts.html). A familiarity with the Bazel build system will also clear a lot of things up but isn't necessary. Ready? Let's get started!_

## Building Microservices with Bazel
Here's an [example repository](https://github.com/tilt-dev/bazel_example) that contains two services (snack and vigoda) that are built with Bazel. The current development workflow is to make some changes to the code (contained in the `snack` or `vigoda` directories) then run the appopriate bazel rule to put the service in to my Kubernetes cluster. For example if I made a change to `snack/main.go` I would then run `bazel run //:snack-server.apply`. This command will build my Go code, put it in to an image, put that image in to my YAML, and run `kubectl apply` to update my Kubernetes cluster with the new YAML. Bazel handles it all by understanding the transitive dependencies of `snack-server`.

## Writing the Tiltfile
Tiltfiles only need two things: Kubernetes YAML and Docker Images. To get started we just need to figure out how to ask Bazel for those two things.

### Getting YAML
So when we run `bazel run //:snack-server.apply` what does Bazel actually do? Let's look at the `:snack-server` rule definition.

```python
k8s_object(
  name = "snack-server",
  kind = "deployment",

  template = ":deploy/snack.yaml",

  cluster = "docker-for-desktop-cluster",
)
```

If I want to get just the YAML, a quick [glance at the rules_k8s documentation](https://github.com/bazelbuild/rules_k8s#resolve) tells me that can be done by just running the target without the `.apply`.

```
$ > bazel run //:snack-server
apiVersion: apps/v1
kind: Deployment
metadata:
  labels: {app: snack, owner: varowner}
  name: varowner-snack
spec:
  selector:
    matchLabels: {app: snack, owner: varowner}
  template:
    metadata:
      labels: {app: snack, owner: varowner, tier: web}
    spec:
      containers:
      - image: bazel/snack@sha256:5a7e2fd3bd39a841cad0f009d605e7f5337a50d2cf641c50ebc03148d8257a0b
        name: snack
        ports:
        - {containerPort: 8083}
        resources:
          requests: {cpu: 10m}
```

 Now we have enough to begin writing our Tiltfile. We'll use `local` to call Bazel and `k8s_yaml` to tell Tilt about the YAML that Bazel generates. Here's a function that given a Bazel target name returns the YAML for that target:

```python
def bazel_k8s(target):
  return local("bazel run %s" % target)
```

In the main body of our Tiltfile we can call it like so:

```python
k8s_yaml(bazel_k8s(":snack-server"))
```

And if we `tilt up` we should see that Tilt calls Bazel to build the YAML and then Tilt takes that YAML and deploys it to the cluster. If the image exists in the registry Kubernetes should schedule the resource

### Building Images
Let's follow the same strategy and figure out the Bazel command that will just build an image and then integrate that in to the Tiltfile.

"rules_k8s" uses "rules_docker" under the hood for building images. [Reading through rules_docker's documentation](https://github.com/bazelbuild/rules_docker#using-with-docker-locally) reveals that `bazel run //:targetname` will load the image in to the configured Docker daemon. That's all we need thanks to `custom_build`. Custom build takes an image name and a command that should produce that image. After the command is executed Tilt asserts that it exists, and retags it so it can track it.

```python
custom_build(
  'bazel/snack',
  'bazel run //snack:image',
  [],
  tag="image",
)
```

In this case Tilt runs `bazel run //snack:image` and asserts that an image named "bazel/snack" exists with the tag "image". If it doesn't exist then the build will fail.

Thanks to Bazel's deterministic nature we know in advance what the image name will be. Bazel uses a formula for determining the name of the image that it pushes:

```
"bazel/" + directory that the build file is in + ":" + the name of the rule
```
Hence for us: "bazel/snack:image".

The third argument, the empty list, is a list of dependencies. We'll fill that in later. For now let's wrap this in a function called `bazel_build` and add it to the main section of our Tiltfile:

```python
def bazel_build(image, target):
  custom_build(
    image,
    'bazel run ' + target,
    [],
    tag="image",
  )

k8s_yaml(bazel_k8s(":snack-server"))
bazel_build('bazel/snack', '//snack:image')
```

Now Tilt can get YAML from Bazel, get an image from Bazel, insert the image into the YAML and track the resource's status in the Kubernetes cluster.

## Dealing with Dependencies
If you started Tilt now, it would appear to work! Run `tilt up` and all the images get deployed to your cluster.

Then you make a change to `snack/main.go`. Nothing gets updated. Why not?

It's not enough for Tilt to know how to build & deploy an image. It needs to know what files should trigger a new build and deploy.

Luckily for us Bazel makes it easy to ask for those files and Tilt makes it easy to tell it about those files.

[`bazel query`](https://docs.bazel.build/versions/master/query-how-to.html) is the functionality that we'll use to ask Bazel about the various dependencies of certain targets. Before we do that there are two types of dependencies that Tilt cares about: dependencies for the Tiltfile and dependencies for images.

Dependencies for the Tiltfile are files that you read during Tiltfile execution. For example, if you had a JSON file that you read to tell you which services Tilt should start that JSON file would be marked as a dependency of the Tiltfile. Tilt will watch that file and, if it changes, re-execute the Tiltfile.

Dependencies for images are files that are included in a build context or running container. If they change Tilt doesn't necessarily re-execute the Tiltfile but it will update a container.

### YAML Dependenices
For the YAML case the only question we need to ask is "Under what circumstances should the Tiltfile re-execute to get the new YAML"? To fully answer this question from Bazel we need to run two queries: one for Bazel's build dependencies, and one for the source dependencies of the YAML target:

```python
# build dependencies: what dependencies does Bazel need to execute this target?
BAZEL_SOURCES_CMD = """
  bazel query 'filter("^//", kind("source file", deps(set(%s))))' --order_output=no
  """.strip()

# source dependencies: What are the target's dependencies?
BAZEL_BUILDFILES_CMD = """
  bazel query 'filter("^//", buildfiles(deps(set(%s))))' --order_output=no
  """.strip()
```

For `:snack-server` we get 1 build dependency: `BUILD`

Okay that makes sense: if the Bazel build files themselves change we will want to re-execute the Tiltfile so that it can re-execute the Bazel rules and potentially get new YAML. There's also a source file dependency: `deploy/snack.yaml`. As the actual YAML itself that makes total sense too.

Let's wire up these query calls in to `bazel_k8s`:

```python
def watch_labels(labels):
  watched_files = []
  for l in labels:
    if l.startswith("@"):
      continue
    elif l.startswith("//external/") or l.startswith("//external:"):
      continue
    elif l.startswith("//"):
      l = l[2:]

    path = l.replace(":", "/")
    if path.startswith("/"):
      path = path[1:]

    watch_file(path)
    watched_files.append(path)

  return watched_files

def bazel_k8s(target):
  build_deps = str(local(BAZEL_BUILDFILES_CMD % target)).splitlines()
  source_deps = str(local(BAZEL_SOURCES_CMD % target)).splitlines()
  watch_labels(build_deps)
  watch_labels(source_deps)

  return local("bazel run %s" % target)
```

Now if we change a dependency of the YAML, the Tiltfile re-executes.

### Image Dependencies
We can reuse our build and source file queries for the image target `//snack:image`. There's one build dep (`snack/BUILD`) and one source dep (`snack/main.go`). That looks right, now to use these queries in our `bazel_build` function:

```python
def bazel_build(image, target):
  build_deps = str(local(BAZEL_BUILDFILES_CMD % target)).splitlines()
  watch_labels(build_deps)

  source_deps = str(local(BAZEL_SOURCES_CMD % target)).splitlines()
  source_deps_files = bazel_labels_to_files(source_deps)

  custom_build(
    image,
    BAZEL_RUN_CMD % target,
    source_deps_files,
    tag="image",
  )
```
_(`bazel_labels_to_files` is some boring code that parses Bazel output that is omitted here but is included in the full example linked to at the end of this guide)_

Now we're passing the dependencies to our `custom_build`. If any of those paths change we will build a new image and update the YAML with the new image. Same as above: if any of the dependencies of the image rule itself change Tilt will now re-execute the Tiltfile.

Now we have a [Tiltfile that fully integrates with Bazel](https://github.com/tilt-dev/bazel_example/blob/master/Tiltfile) and responds to changes from the filesystem.

## Putting it all together
And that's that! Take a look at the [full example code](https://github.com/tilt-dev/bazel_example) and let us know if you have any questions.
