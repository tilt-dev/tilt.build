---
title: With CI
description: "Test that your images build and your servers start"
layout: docs
sidebar: guides
---

Once you've bought into container-based development,
you'll want to set up CI to ensure your servers don't break.

The Tilt team has this problem too! For every change, we create a real
single-use cluster and verify that all our services and example projects still
work. So we have a lot of experience with best practices.

There are two tools you'll need to configure:

1) How to use `tilt ci` to build and deploy servers.

2) How to run a Kubernetes cluster in CI that `tilt ci` can deploy to.

Let's dig into examples of each one.

## The `tilt ci` command

The [`tilt ci` command](/cli/tilt_ci.html) is made for CI jobs.

### How it Works

Under the hood, `tilt ci`:

1) Executes your Tiltfile.

2) Runs all `local_resource` commands.

3) Builds all images.

4) Deploys all Kubernetes resources.

5) Waits until all servers and other resources are healthy.

`tilt ci` defaults to log-streaming mode. The web UI is still accessible,
but the terminal will be a simple log stream.

If any step fails, Tilt will exit immediately with an error code.

If any resource crashes or looks like it will never succeed (e.g., a pod that
takes too long to schedule), Tilt will also exit with an error code.

Once all services are healthy, it will exit with status code 0.

Any portforwards will not be active after `tilt ci` has exited.

### Examples

Most of our example projects use CircleCI to run `tilt ci`:

<ul>
  {% for page in site.data.examples %}
     <li><a href="/{{page.href | escape}}#ci">{{page.title | escape}}</a></li>
  {% endfor %}
</ul>

Each example invokes [`ctlptl`](https://github.com/tilt-dev/ctlptl) to set up a single-use
cluster. But the `ctlptl` tool has many options for setting up clusters,
depending on what you need.

### Debugging

Sometimes `tilt ci` will be waiting on a server to come up. But it can be hard to tell
what it's waiting on. Tilt has tools to help debug this!

First, `tilt ci` still runs the normal web dashboard at `http://localhost:10350/`. That should
be familiar, so use that first.

But maybe the dashboard doesn't help. The next step is to inspect the `Session` object.

The `Session` object is the Tilt API that drives `tilt ci`. 

For human-readable output, run:

```
tilt describe session
```

For machine-readable output, run:

```
tilt get session -o yaml
tilt get session -o json
```

The status of the session reflects:
- The current Tilt PID.
- The time Tilt started at.
- Each target that Tilt is waiting on, and its current state (waiting, running, or terminated).

We also pair with teams on how to integrate this status reporting with their own
in-house tools, like in [the tilt-status VSCode
extension](https://marketplace.visualstudio.com/items?itemName=tilt-dev.tilt-status).

For more info, here's the [complete API
reference](https://api.tilt.dev/core/session-v1alpha1.html) of the Session
object.

## Single-use Kubernetes clusters

Running a Kubernetes cluster in CI can be harder than running one locally.

Here are some options, with the pros and cons of each:

### Easiest: Cluster on VM-based CI

[`kind`](https://kind.sigs.k8s.io/) is currently the gold standard for running
Kubernetes in CI. The Kubernetes project itself uses it for testing. `kind` can
create clusters inside Docker.

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

Tilt-team maintains [`ctlptl`](https://github.com/tilt-dev/ctlptl), a CLI for declaratively
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
