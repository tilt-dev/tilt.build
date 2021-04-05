---
title: With CI
description: "Test that your images build and your servers start"
layout: docs
---

Once you've bought into container-based development,
you'll want to set up CI to ensure your servers don't break.

We think of this in two pieces:

1) Run Tilt in CI to deploy to a single-use cluster.

2) Run a single-use Kubernetes in CI that you can immediately throw away.

Let's dig into examples of each one.

## The `tilt ci` command

The [`tilt ci` command](/cli/tilt_ci.html) is made for CI jobs.

### How it Works

Under the hood, `tilt ci`:

1) Executes your Tiltfile.

2) Runs all `local_resource` commands.

3) Builds all images.

4) Deploys all Kubernetes resources.

5) Waits until all servers and other Kubernetes resources are healthy.

`tilt ci` defaults to log-streaming mode. The web UI is still accessible,
but the terminal will be a simple log stream.

If any step fails, Tilt will exit immediately with an error code.

If any resource crashes or looks like it will never succeed (e.g., a pod that
takes too long to schedule), Tilt will also exit with an error code.

Once all services are healthy, it will exit with status code 0.

### Examples

Most of our example projects use CircleCI to run `tilt ci`:

<ul>
  {% for page in site.data.examples %}
     <li><a href="/{{page.href | escape}}#ci">{{page.title | escape}}</a></li>
  {% endfor %}
</ul>

These each use [`ctlptl`](https://ctlptl.dev/) to set up a single-use
cluster. But if you're considering other options, read on.

## Single-use Kubernetes clusters

If you're using Kubernetes for dev, you'll likely also want to use Kubernetes in CI.

Tilt-team has this problem as well! Our integration test suite uses the latest
version of Tilt to deploy real sample projects against a real cluster.  So we
have a lot of experiences with best practices.

Here are some options, with the pros and cons of each:

### Easiest: Cluster on VM-based CI

[`kind`](https://kind.sigs.k8s.io/) is currently the gold standard for running
Kubernetes in CI. The Kubernetes project itself uses it for testing.

`kind` comes with the ability to run a local registry, so you can push images to
the registry on `localhost:5000` and pull them from inside `kind`.

Set up a CI pipeline that:
 
1. Creates a VM.

2. Installs all our dependencies, including Docker.

3. Creates a `kind` cluster with a local registry
   at `localhost:5000`, using [their
   script](https://kind.sigs.k8s.io/docs/user/local-registry/).

This is the approach we use to test `ctlptl` with both
`minikube` and `kind`. Here's [the CI
config](https://github.com/tilt-dev/ctlptl/blob/b6f808a09b05b6cf7aa0b3365e4781d2c23e4851/.circleci/config.yml#L30).

Tilt will auto-detect that the registry is running on `localhost:5000` and push
images there instead of your prod image registry.

The downside is that most teams are more comfortable managing container
images than managing VMs. VMs are slower. Upgrading dependencies is more
heavyweight.

### Recommended: Cluster in Remote Docker-based CI

Many CI environments offer a remote Docker environment outside the container.
You can run test code in a container that talks to Docker, without the pitfalls
of running Docker inside Docker.

Set up a CI pipeline that:

1. Create a container with your code.

2. Create [a remote Docker environment](https://circleci.com/docs/2.0/building-docker-images).

3. Start a `kind` cluster with a local registry inside the remote Docker environment.

4. Use `socat` to expose the remote registry and Kubernetes
   cluster inside the local container.

The `socat` element makes this a bit tricky.

Tilt-team maintains [`ctlptl`](https://ctlptl.dev/), a CLI for declaratively
setting up local Kubernetes clusters. If you're using `ctlptl`, it will try to
detect when you have a remote docker environment and set up the `socat`
forwarding automatically.

If you want to wire it up yourself, check out
[this Bash script](https://github.com/tilt-dev/kind-local/blob/master/.circleci/with-kind-cluster.sh).

### Not Recommended: Remote Registry

You may already have a container image registry that you prefer for development,
like Quay.io or Google Cloud Registry.

If you want to use this registry in CI, you need to set up permissions so
that your CI job can write to this registry.

1. Create a dedicated image registry for CI.

2. Create a service account or access token with a secret in your CI build.

3. Use [`kind`](https://kind.sigs.k8s.io) to create the cluster.
  
This is an approach a lot of teams try. We usually don't recommend it. The downsides:

- Managing secrets and permissions for the remote registry can be a pain.
  You'll want to set it up so that anyone who can send a pull request to your repository
  can also write to the remote registry. This may look different depending on your
  org structure.
  
- It's hard to guarantee that images aren't leaking between tests. For example,
  if image pushing failed, you'll want to be sure we weren't picking up a cached
  image from a previous test. One solution is to reset the whole registry at
  regular intervals.

But it might be the best option if you're not able to easily modify where
your tools are pushing images to and pulling images from.
