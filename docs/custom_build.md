---
title: Non-Docker Builds
layout: docs
---

`docker build` is the common way to build container images, but there are others. [Bazel](https://github.com/google/bazel), [s2i](https://github.com/openshift/source-to-image), and [ko](https://github.com/google/ko) support building images. Tilt supports these other tools with the function [`custom_build`](https://docs.tilt.dev/api.html#api.custom_build) instead of `docker_build`.

## Usage
Building an image with a custom build tool requires:
* Name of the image to build (as a ref, e.g. `frontend` or `gcr.io/company-name/frontend')
* Command to run (e.g. `bazel build //frontend:image` or `build_frontend.sh`)
* Files to watch (e.g. `['frontend']` or `['frontend', 'util', 'data.txt']`). When a dependency changes, Tilt starts an update to build the image then apply the YAML.

A simple case (that just calls `docker build` to build an image named `frontend` from the directory `frontend`) would look like
```python
custom_build(
  'frontend',
  'docker build -t $EXPECTED_REF frontend',
  ['./frontend'],
)
```

One piece of this needs more explanation: `$EXPECTED_REF`.

## Tags
Tilt always deploys with a digest, not a bare ref. (Instead of `gcr.io/company-name/frontend`, Tilt injects `gcr.io/company-name/frontend:tilt-ffd9c2013b5bf5d4`). Before explaining why (at the bottom of this document), let's describe what this means for your Tiltfile and build script.

Because different build tools have different ergonomics, Tilt supports two modes:
* one-time tags via $EXPECTED_REF
* temporary refs

### One-time Tags
This mode is easy if your tool takes the destination of the image as an argument (e.g. `docker build`).
* Tiltfile sets a custom build command (e.g. `custom_build(..., 'docker build -t $EXPECTED_REF frontend')`).
* Tilt sets a one-time ref as environment variable before executing the custom build command. (e.g. `EXPECTED_REF=gcr.io/company-name/frontend:tilt-ffd9c2013b5bf5d4`)
* The custom build command builds the image and pushes to that ref (e.g. by reading `$EXPECTED_REF`).

### Temporary Refs
Other tools want to have an image ref hard-coded in configuration. They'll build and push to the same place each time. Instead of having to change your tool, tell Tilt what tag the build image will have with `custom_build(..., tag='frontend:s2i')`. After Tilt runs your build command, it will find this image and retag and push it with a unique ID.

## Live Update and Other Features
Tilt's `docker_build` supports other options. The most impactful is [Live Update](live_update_tutorial.html), which lets you update code in Kubernetes without doing a full image build.  `custom_build` supports this as well, using the same syntax.

`custom_build` supports most other options of `docker_build`, and a few specific to non-Docker container builders. If you find an option you think should exist but doesn't, let us know in the `#tilt` channel in [Kubernetes Slack](http://slack.k8s.io).

## Why Tilt uses One-Time Tags
This section describes for the curious why Tilt uses tags the way it does, instead of using a fixed reference.
Kubernetes (and the [OCI model](https://github.com/opencontainers/image-spec) generally) support multiple ways to reference an image:
* Tagged: `gcr.io/company-name/frontend:username-devel`. These tags can change as you upload new images to the same tag.
* Untagged: `gcr.io/company-name/frontend`. This is shorthand for the tag `latest`, and changes even more frequently.
* One-Time: `gcr.io/company-name/frontend:tilt-ffd9c2013b5bf5d4`. The unique bit may be a [Nonce](https://en.wikipedia.org/wiki/Cryptographic_nonce) or a digest of the contents. These don't change once set (though technically they're not write-protected).

Tilt only deploys One-Time references. Instead of pushing to `gcr.io/company-name/frontend` and leaving the YAML as-is, Tilt retags the image and rewrites the container spec. This makes the Tilt experience more reliable.  Deploying with a Tagged reference creates a race condition. Pods created at different times from the same definition may end up running different code as the reference is overwritten.

## Conclusion
Tilt supports any container image builder via `custom_build`. You can see details at the [API reference](https://docs.tilt.dev/api.html#api.custom_build). We hang out in the `#tilt` channel in [Kubernetes Slack](http://slack.k8s.io) and would love to hear about problems or successes you have with `custom_build`.
