---
title: Custom Build Scripts
description: "Docker is the most common way to build container images, but there are others. Tilt supports these other tools with the function 'custom_build' instead of 'docker_build'."
layout: docs
sidebar: guides
---

`docker build` is the common way to build container images, but there are others.

Tilt supports these other tools with the function [`custom_build`](api.html#api.custom_build)
instead of `docker_build`.

## Usage

All `custom_build` calls require:

* A name of the image to build (as a ref, e.g. `frontend` or `gcr.io/company-name/frontend')

* A command to run (e.g. `bazel build //frontend:image` or `build_frontend.sh`)

* Files to watch (e.g. `['frontend']` or `['frontend', 'util', 'data.txt']`). When a dependency changes, Tilt starts an update to build the image then apply the YAML.

There are a couple different image-building patterns.

### The Easiest Way: Get Someone Else to Write it For You

Before you write your own custom builder, check out the [Tilt
Extensions](https://github.com/tilt-dev/tilt-extensions) repo to see if someone
has already written a `custom_build` wrapper for your tool.

Tilt Extensions can be simple. Here's an example that uses Ko, the Go image builder.

[Ko Tilt extension](https://github.com/tilt-dev/tilt-extensions/tree/master/ko){:.attached-above}

### Custom Docker Builds

Suppose you have a script that wraps `docker build`, but adds some application-specific abstractions.

Here's a simple example that invokes `docker build` to build an image named `frontend` from the directory `frontend`:

```python
custom_build(
  'frontend',
  'docker build -t $EXPECTED_REF frontend',
  ['./frontend'],
)
```

Tilt will run this command to build the image, verify that the image is in the
Docker image store, then push the image to the appropriate image registry.

You can also use this pattern to use `docker` flags that the `docker_build()`
function doesn't support.

### Jib, Bazel, or any other builder that interoperates with Docker

Many tools can create Docker images, then write them to the local Docker image
store.

For example, [Jib](https://github.com/GoogleContainerTools/jib) has plugins that integrate
with your existing Java tooling and create Java-based images.

The [tilt-example-java](https://github.com/tilt-dev/tilt-example-java) repo has an example
[Tiltfile](https://github.com/tilt-dev/tilt-example-java/blob/master/101-jib/Tiltfile)
that uses `custom_build` to generate images with Gradle and Jib:

```
custom_build(
  'example-java-image',
  './gradlew jibDockerBuild --image $EXPECTED_REF',
  deps=['src'])
```

[Bazel](https://github.com/google/bazel), the general-purpose build system, also
takes this approach. Bazel's
[rules_docker](https://github.com/bazelbuild/rules_docker) extension assembles
Docker images and writes them to the local Docker image store.

See the tutorial on how to use `custom_build` to [build images with
Bazel](integrating_bazel_with_tilt.html).

### Buildah (or any image builder indepdendent of Docker)

[Buildah](https://buildah.io/) is an independent Docker image builder.

Buildah has its own API and own image store. A `custom_build()` call needs to
both build and push the image.

```python
custom_build(
  'frontend',
  'buildah bud -t $EXPECTED_REF frontend && buildah push $EXPECTED_REF $EXPECTED_REF',
  ['./frontend'],
  skips_local_docker=True,
)
```

The `skips_local_docker` parameter indicates that we don't expect the image to
ever show up in the local Docker image store. Tilt shouldn't try to verify the
image locally.

There are a couple of caveats you should be aware of with `buildah` (and similar builders):

- They often require privileged access. You may need to run Tilt with `sudo` or
  inside an appropriate sandbox

- If you're using Tilt to push to an insecure registry, you will need to
  configure your builder for that registry. For example, to use `buildah` with
  Microk8s, you need to add `localhost:32000` to
  [registries.insecure](https://github.com/containers/buildah/blob/master/install.md#registriesconf).

## How to Write Your Own

We've looked at a couple simple recipes for how to write a custom build script.

To write more complex ones, we need to understand in more detail how they work.

All the commands above contain `$EXPECTED_REF`. What is that?

Tilt always pushes a content-based, immutable tag, not a bare ref. (Instead of `gcr.io/company-name/frontend`, Tilt injects `gcr.io/company-name/frontend:tilt-ffd9c2013b5bf5d4`, where the `ffd9c2013b5bf5d4` part is based on the contents of your image). Before explaining why (see [below](#why-tilt-uses-immutable-tags)), let's describe what this means for your Tiltfile and build script.

There are two ways for Tilt and your build script to coordinate image builds.

### The Good Way

Most tools take a destination of the image as an argument (e.g. `docker build`).

* Before running your build script, Tilt sets the environment variable
  `$EXPECTED_REF` with a randomized tag
  (e.g. `EXPECTED_REF=gcr.io/company-name/frontend:tilt-12345`).

* The custom build script builds the image and tags it with `$EXPECTED_REF`.

* After the build script exits, Tilt reads the new image at `$EXPECTED_REF`,
  re-tags it with a content-based tag, and pushes it to the image registry.

### The Hacky Way

Other tools have an image ref hard-coded in configuration. They'll build
to the same tag each time.

Instead of writing a wrapper script around your tool, tell Tilt what tag the
build image will have with `custom_build(...,
tag='gcr.io/company-name/frontend:dev')`.

After Tilt runs your build command, it will find this image and retag and push
it with a content-based tag.

This method is generally less robust, because the script is building to a
mutable tag instead of an immutable tag.

### An Improvement on the Hacky Way

If you're willing to invest more into your custom build script,
you should use content-based tags!

`custom_build(outputs_image_ref_to='ref.txt')` will tell Tilt that your custom
build script intends to write a tagged image reference to the file `ref.txt`.

Tilt will then inject that image into your deployments.

If Tilt has detected a local registry, it will populate the environment variable
`REGISTRY_HOST` (e.g., `REGISTRY_HOST=localhost:5000`) before calling the build script.

### Determining the Content-based Tag

In rare cases, another script in your build system may need to know what tag
Tilt is going to deploy. This typically only comes up if your team has
written their own artisanal image build system that's closely coupled with Kubernetes.

Tilt has a special command to help with this. After you build the image, run:

```
tilt dump image-deploy-ref $EXPECTED_REF
```

Tilt will read the image, determine the hash of the context, and print out the
full name and content-based tag.

**NOTE:** This is not a common use-case. Usually, when teams ask about this, they're
writing a workflow engine that creates its own pods (like Airflow), and need a
way to get the deploy tag at runtime. So they hack custom_build to grab the
deploy tag at build-time, and plumb it through to their runtime pods. There's a
better way to do this. Use [this
guide](custom_resource.html#advanced-pod-creation) instead.

## Live Update and Other Features
Tilt's `docker_build` supports other options. The most impactful is `live_update`, which lets you update code in Kubernetes without doing a full image build.  `custom_build` supports this as well, using the same syntax.

`custom_build` supports most other options of `docker_build`, and a few specific to non-Docker container builders.

### Adjust File Watching with `ignore`
While most of the points in our [Debugging File Changes](/file_changes.html) guide hold true for `custom_build`, the `ignore` parameter (which adjusts the set of files watched for a given build) works a bit differently, and is worth discussing briefly.

The `ignore` parameter takes a pattern or list of patterns (following [`.dockerignore` syntax](https://docs.docker.com/engine/reference/builder/#dockerignore-file); files matching any of these patterns will _not_ trigger a build.

Of note, these patterns are evaluated relative to each ``dep``. E.g. given the following call:
```python
custom_build(
    'image-foo',
    'docker build -t $EXPECTED_REF .',
    deps=['dep1', 'dep2'],
    ignore=['baz']
)
```
Tilt will ignore `dep1/baz` and `dep2/baz`.

## Why Tilt uses Immutable Tags

Immutable tags have a long history in the Kubernetes community.

The Knative team has this presentation that gives a good overview: 
[Why we resolve tags in Knative](https://docs.google.com/presentation/d/1gjcVniYD95H1DmGM_n7dYJ69vD9d6KgJiA-D9dydWGU/edit?usp=sharing)
(join
[`knative-users@googlegroups.com`](https://groups.google.com/d/forum/knative-users)
for access).

Mutable tags have good usability and security properties. For example, a
`registry:v2` image that has the latest, most secure minor version of the v2
major version.

Immutable tags have good reliability and caching properties. For example, if
you're rolling out 3 pods of `registry:v2`, you want to be sure all pods have
the exact same version. Deploying with a mutable reference creates a race
condition. Pods created at different times from the same definition may end up
running different code as the reference is overwritten.

Tilt only deploys immutable tags. Instead of pushing to
`gcr.io/company-name/frontend`, Tilt re-tags the image as
`gcr.io/company-name/frontend:tilt-ffd9c2013b5bf5d4`. The unique bit is a
[Nonce](https://en.wikipedia.org/wiki/Cryptographic_nonce) or a digest of the
contents. (Technically the tag isn't write-protected in any way, but the
improbability of collisions means we can pretend it's immutable.)

Tilt then injects the new tag into the container spec. This makes the Tilt
experience faster and more reliable, because we can instruct Kubernetes to cache
the tag aggressively as if it's immutable.

Knative uses [a similar strategy](https://knative.dev/docs/serving/tag-resolution/), but the immutability is enforced by a
Kuberentes operator, instead of by client-side tooling.

## When You're Done

If you have a more complex build script that you're not sure how to integrate
with Tilt, we'd love to hear about it. Come find us in the `#tilt` channel in
[Kubernetes Slack](http://slack.k8s.io) or
[file an issue](https://github.com/tilt-dev/tilt/issues) on GitHub.

We'll love you even more if you share it with other Tilt users as an [extension](extensions.html)!
