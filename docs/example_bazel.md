---
title: "Example: Bazel"
description: "Best practices for developing Bazel projects with Tilt"
layout: docs
---

The best indicator of a healthy development workflow is a short feedback loop.

Kubernetes is a huge wrench in the works.

Let's fix this.

In this example, we're going to look at a project that uses Bazel to build images and
Kubernetes resources. We'll show you how to use Tilt to speed up iterative development.
Our simple server uses Go templates to serve HTML.

We'll use Tilt to:

- Run the server on Kubernetes
- Measure the time from a code change to a new process
- Optimize that time for faster feedback

All the code is in this repo:

[tilt-example-bazel](https://github.com/tilt-dev/tilt-example-bazel){:.attached-above}

To skip straight to the fully optimized setup, go to this Tiltfile:

[Recommended Setup](https://github.com/tilt-dev/tilt-example-bazel/blob/main/3-recommended/Tiltfile){:.attached-above}

For now, we've posted the code so that teams can copy it and adapt it to their own Bazel builds.

We're workshopping this approach with partner teams and tweaking it to make sure
it works well.  We'll add a longer write-up to the doc on how it works once
we're happy with it.

Stay tuned!

## Further Reading

### CI

Once you're done configuring your project, set up a CI test to ensure
your setup doesn't break! In the example repo, CircleCI uses
[`ctlptl`](https://github.com/tilt-dev/ctlptl) to create a single-use Kubernetes
cluster. The test script invokes `tilt ci`.  The `tilt ci` command deploys all
services in a Tiltfile and exits successfully if they're healthy.

- [CircleCI config](https://github.com/tilt-dev/tilt-example-bazel/blob/master/.circleci/config.yml)
- [Test script](https://github.com/tilt-dev/tilt-example-bazel/blob/master/test/test.sh)

