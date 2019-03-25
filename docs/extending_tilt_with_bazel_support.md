---
tilt: Extending Tilt With No Pull Requests
layout: docs
---

# Extending Tilt with No Pull Requests

There's nothing more frustrating than using a tool that works perfectly except for _one_ small thing. Even if the tool is open source it can be a daunting task to get a change accepted to it.

We recognize that everyone's set up is different and that we cannot foresee all possible features and use cases that folks will need. Software is complicated! As a result we designed Tilt to be customizable from the beginning. If there's functionality you wish Tilt had you can often add it yourself, right in your Tiltfile, no external pull requests necessary!

Let's explore this with a simple feature request: I want Tilt to support the [Bazel](https://bazel.build/) build system. I can hear you now: but that's not simple at all! It's actually a lot simpler than you'd think, let's see why.

_Note: Before diving in to this guide you should have run through [Tilt's Getting Started Guide](tutorial.html) and the deep dive in to [Tiltfile concepts](tiltfile_concepts.html). A familiarity with the Bazel build system will also clear a lot of things up but isn't necessary. Ready? Let's get started!_

## Building Microservices with Bazel
Here's an [example repository](https://github.com/windmilleng/bazel_example) that contains two services (snack and vigoda) that are built with Bazel. The current development workflow is to make some changes to the code (contained in the `snack` or `vigoda` directories) then run the appopriate bazel rule to put the service in to my Kubernetes cluster. For example if I made a change to `snack/main.go` I would then run `bazel run //:snack-server.apply`. This command will build my Go code, put it in to an image, put that image in to my YAML, and run `kubectl apply` to update my Kubernetes cluster with the new YAML. That's a lot of stuff but Bazel handles it all by understanding the transitive dependencies of `snack-server`.

## Writing the Tiltfile
So how can we take this sophisticated workflow and combine its reproducability and dependency tracking with Tilt's lightning fast updates and heads up display?

Let's remember that Tiltfiles only need two things in order to provide a great experience: Kubernetes YAML and Docker Images. To get our service up in running Tilt we just need to figure out how to ask Bazel for those two things separately.

### Getting YAML
So when we run `bazel run //:snack-server.apply` what does Bazel actually do? To find out let's look at the `:snack-server` rule definition.

```python
k8s_object(
  name = "snack-server",
  kind = "deployment",

  template = ":deploy/snack.yaml",

  cluster = "docker-for-desktop-cluster",

  images = {
    "bazel/snack": "//snack:image",
  }
)
```

If I want to get it to just print the YAML, a quick [glance at the rules_k8s documentation](https://github.com/bazelbuild/rules_k8s#resolve) shows me that that can be done by just running the target without the `.apply`.

```
$ > bazel run //:snack-server
DEBUG: Rule 'org_golang_x_tools' modified arguments {"sha256": "2384fa91351a7414b643c5230422ce45f5aa2be8a82727609afd4e64e6973a30"}
INFO: Analysed target //:snack-server (0 packages loaded, 0 targets configured).
INFO: Found 1 target...
Target //:snack-server up-to-date:
  bazel-bin/snack-server.substituted.yaml
  bazel-bin/snack-server
INFO: Elapsed time: 0.331s, Critical Path: 0.04s
INFO: 0 processes.
INFO: Build completed successfully, 3 total actions
INFO: Build completed successfully, 3 total actions
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

With just this we have enough to write our Tiltfile. We'll be using the `local` function to call Bazel and `k8s_yaml` to tell Tilt about the YAML that Bazel generates. Let's write a function that given a Bazel target name returns the YAML for that target.

```python
def bazel_k8s(target):
  return local("bazel run %s" % target)
```

Easy enough, now in the main body of our Tiltfile we can call it like so:

```python
k8s_yaml(bazel_k8s(":snack-server"))
```

And if we Tilt up we should see that Tilt calls Bazel to build the YAML, and by extension its image and then Tilt takes that YAML and deploys it to the cluster. We get all the awesomeness of the HUD with three lines of code in a Tiltfile.

### Building Images
Now for the second component: images. Let's follow the same strategy and figure out the Bazel command that will just build an image and then integrate it in to the Tiltfile.

From reading about rules_k8s I've learned that it uses rules_docker under the hood for building images. Another [quick glance at rules_docker's documentation](https://github.com/bazelbuild/rules_docker#using-with-docker-locally) reveals that `bazel run //:targetname` will load the image in to the configured docker daemon. Perfect, that's all we need!

To integrate this functionality in to the Tiltfile we will make use of just one function: `custom_build`. Custom build takes a command that produces a docker image and tells Tilt about it so it can track it and manage its insertion in to the YAML that we provided previously. Here's what it looks like:

```python
custom_build(
  'bazel/snack',
  'bazel run //snack:image',
  [],
  tag="image",
)
```

This tells Tilt to run the command (`bazel run //snack:image`) and to assert after it has completed that an image named bazel/snack will exist with the tag "image". If it doesn't then the build fails.

We know what the image will be ahead of time because of Bazel's deterministic nature. Bazel uses a formula for determining the name of the image that it will push: "bazel/" + the directory that the build file is in". This image is tagged with the name of the rule that created it, which in our case is "image".

The third argument, the empty list, is a list of dependencies. We'll fill that in later. For now let's wrap this in a function called `bazel_build` and add it to the main section of our Tiltfile

```python
k8s_yaml(bazel_k8s(":snack-server"))
bazel_image('bazel/snack', '//snack:image')
```

Now Tilt can get YAML from Bazel, get an image from Bazel, insert it into the YAML and track its status in the Kubernetes cluster.

## Dealing with Dependencies
There's a problem with our Tiltfile as it stands: it only picks up changes if the Tiltfile changes. It doesn't understand what dependencies go in to generating the YAML _or_ the code dependencies that go in to generating the docker image. Luckily for us Bazel makes it easy to ask for those dependencies and Tilt makes it easy to tell it about those dependencies. Let's start by getting the dependencies for the YAML and then move on to the dependencies for the docker image.

### YAML Dependenices
[`bazel query`](https://docs.bazel.build/versions/master/query-how-to.html) is the functionality that we'll use to ask Bazel about the various dependencies of certain targets. Before we do that there are two types of dependencies that Tilt cares about: dependencies for the Tiltfile and dependencies for images.

Dependencies for the Tiltfile are files that you read during Tiltfile execution. For example, if you had a JSON file that you read to tell you which services Tilt should start that JSON file would be marked as a dependency of the Tiltfile. Tilt will watch that file and, if it changes, re-execute the Tiltfile.

Dependencies for images are files that are included in a build context or running container. If they change Tilt doesn't necessarily re-execute the Tiltfile but it will update a running container.

For the YAML case the question we need to ask is "Under what circumstances should the Tiltfile re-execute to get the new YAML"? To fully answer this question from Bazel we need to run two queries: one for Bazel's build dependencies, and one for the source dependencies of the YAML target:

```python
# what dependencies does Bazel need to execute this target?
BAZEL_SOURCES_CMD = """
  bazel query 'filter("^//", kind("source file", deps(set(%s))))' --order_output=no
  """.strip()

# What are the target's dependencies?
BAZEL_BUILDFILES_CMD = """
  bazel query 'filter("^//", buildfiles(deps(set(%s))))' --order_output=no
  """.strip()
```

For `:snack-server` we get 2 build dependencies:
* `BUILD`
* `snack/BUILD`

Okay that makes sense: if the Bazel build files themselves change we will want to re-execute the Tiltfile so that it can re-execute the Bazel rules and potentially get new YAML. But why is `snack/BUILD` there? There are also source file dependencies for snack's YAML:
* `deploy/snack.yaml`
* `snack/main.go`

It makes total sense that the YAML file itself would be a dependency, but again why is `snack/main.go` a dependency of the YAML? It's because in the root BUILD file we reference `//snack:image`. The two targets are dependencies. This is not ideal because if we change `snack/BUILD` we will rebuild and redeploy the YAML even if nothing has changed. Let's worry about this later and in the meantime wire up these query calls in to `bazel_k8s`:

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

Now if we change a dependency of the YAML, the Tiltfile re-executes. It might be a bit overzealous due to those extraneous dependencies but we can deal with that later.

### Image Dependencies
We can reuse our build and source file queries for the image target `//snack:image`. There's one build dep (`snack/BUILD`) and one source dep (`snack/main.go`). That looks right, now to use these queries in our `bazel_image` function:

```python
def bazel_build(image, target):
  build_deps = str(local(BAZEL_BUILDFILES_CMD % target)).splitlines()
  watch_labels(build_deps)

  source_deps = str(local(BAZEL_SOURCES_CMD % target)).splitlines()
  source_deps_files = bazel_labels_to_files(source_deps)

  custom_build(
    image,
    BAZEL_RUN_CMD % target,
    source_deps,
    tag="image",
  )
```
(`bazel_labels_to_files` is some boring code that parses Bazel output that I omitted here but included in the full example linked to at the end of this guide)

Now we're passing the dependencies to our `custom_build`. If any of those change we will build a new image and update the YAML with the new image. Same as above: if any of the dependencies of the image rule itself change Tilt will now re-execute the Tiltfile.

Phew! This was a lot to learn but we ended up with a Tiltfile that is respnsive and fully integrates with Bazel with not that much code. It looks like this:

```python
BAZEL_RUN_CMD = "bazel run --platforms=@io_bazel_rules_go//go/toolchain:linux_amd64 %s"

BAZEL_SOURCES_CMD = """
  bazel query 'filter("^//", kind("source file", deps(set(%s))))' --order_output=no
  """.strip()

BAZEL_BUILDFILES_CMD = """
  bazel query 'filter("^//", buildfiles(deps(set(%s))))' --order_output=no
  """.strip()

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

def bazel_build(image, target):
  build_deps = str(local(BAZEL_BUILDFILES_CMD % target)).splitlines()
  watch_labels(build_deps)

  source_deps = str(local(BAZEL_SOURCES_CMD % target)).splitlines()
  source_deps_files =bazel_labels_to_files(source_deps)

  custom_build(
    image,
    BAZEL_RUN_CMD % target,
    source_deps,
    tag="image",
  )

k8s_yaml(bazel_k8s(":snack-server"))
k8s_yaml(bazel_k8s(":vigoda-server"))

bazel_build('bazel/snack', "//snack:image")
bazel_build('bazel/vigoda', "//vigoda:image")
```

## Optimizing
The one remaining problem is that `snack/BUILD` is a dependency of our YAML generation rule. What can we do to solve that?

In the current setup both Tilt and Bazel are managing the insertion of the built image in to the YAML. Tilt takes care of this in dev so we don't need to do it in Bazel. Let's make a new Bazel rule, that we will only use in dev with Tilt, that doesn't associate YAML with an image:


```python
k8s_object(
  name = "snack-server-dev",
  kind = "deployment",

  template = ":deploy/snack.yaml",

  cluster = "docker-for-desktop-cluster",
)
```

When we reference `:snack-server-dev` in place of `:snack-server` in our `bazel_k8s` invocation we now get dependencies for _just_ the Kubernetes YAML and not also the image.

## Putting it all together
And that's that! With only 50 lines of python code we added an entire feature to Tilt, no pull requests required. Take a look at the [full example code](github.com/windmilleng/bazel_example) and let us know if you have any questions.
