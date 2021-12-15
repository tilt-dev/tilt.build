---
title: Resource Dependencies
description: "Control the startup order of Tilt resources"
layout: docs
sidebar: guides
---

Tilt defines your dev environment as a list of resources.

## How Tilt Brings up Resources

While a Tilt environment is running, you can use the CLI to explore the list of
resources that Tilt is aware of. This command will print all the resources in the UI:

```
tilt get uiresources
```

Here's example output of what this might look like:

```shell
$ tilt get uiresources
NAME         CREATED AT
docs-site    2021-10-19T19:51:21Z
make-api     2021-10-19T19:51:21Z
(Tiltfile)   2021-10-19T19:51:21Z
```

Tilt will try to start up the resources as fast as it's safe to do so. Here's
the heuristic it uses by default:

- Run the Tiltfile to create resources.

- Run `local_resource` definitions first.

- Run one `local_resource` at a time (so that they can't step on each others'
  local output).

- Run up to 3 image build and deploys at a time in parallel (for both Kubernetes
  resources and Docker Compose resources). Make educated guesses about the
  correct order of resources and which can be run in parallel based on the YAML.

- Continue until all resources have been built. 

Sometimes the right startup order depends on application logic that Tilt can't guess!
For example, you might have a resource `frontend` that requires a running `database`
before it starts.

This can lead to distracting errors on startup (especially, e.g., if you have 5
services all depending on the same backend!)

That's why Tilt gives you a way to specify startup order manually.

## Adding `resource_deps` for Startup Order

Tilt has 3 built-in functions for configuring a resource:

- `local_resource` (for local jobs and servers)

- `dc_resource` (for docker compose services)

- `k8s_resource` (for Kubernetes workloads - see [Tiltfile concepts](tiltfile_concepts.html) for more details about how YAML is divided into workloads)

All 3 functions have a `resource_deps` argument. To specify that `frontend` depends on `database`:

```python
k8s_resource('frontend', resource_deps=['database'])
```

This has two effects:

1. `frontend` will not be deployed until `database` has been ready at least once
    since Tilt was started.
    
2. If you run `tilt up frontend` to run only the `frontend` resource,
    that also implicitly brings up all of `frontend`'s transitive dependencies.

## Adding Readiness Checks for Startup Waiting

Once a resource is ready, Tilt will start building the resources that depend on it.

By default, a resource is "ready" when:

- For `k8s_resource`: the pod is running and Kubernetes considers all of its containers ready. A job is considered ready when it has completed.

- For `dc_resource`: the container is started (NB: Tilt doesn't currently observe docker-compose health checks).

- For `local_resource`: the command has succeeded at least once.

But Tilt also has ways to customize the definition of readiness. This will change both
when dependent servers start building, and how the servers show up in the UI.

### Kubernetes Readiness Checks

Kubernetes has a built-in notion of
[readiness](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/#define-readiness-probes).
Tilt will use the built-in readiness probe when it's available.

For any Kubernetes object type, including built-ins and CRDs, that creates pods,
Tilt will consider it ready when the pod is running and all of its containers
are ready. The exception to this rule is jobs, which are considered ready by Tilt when
the job has completed.

If an object does not create pods, there isn't a way for Tilt to determine readiness.
Instead, you'll want to configure the resource to let Tilt know that it shouldn't
try to use pods to determine readiness. Resources configured to [ignore pods
for readiness](api.html#api.k8s_resource) will appear as ready in the Tilt UI 
as soon as they are applied to the Kubernetes cluster.

To ignore pod readiness:

```python
k8s_resource('frontend', pod_readiness='ignore')
```

If you're using custom Kubernetes resources, you can also specify the default
readiness settings for a particular API Kind. See the [Custom Resource
Definition](custom_resource.html) guide for more info.

### Local Resource Readiness Checks

`local_resource` allows you to define readiness probes for servers running locally.

The API borrows liberally from the Kubernetes readiness probe API.

Read the guide to [Local Resource Readiness Probes](local_resource.html#readiness_probe) for more info.

## Parallelism

By default, image build and deploys can run 3 at a time (for both `k8s_resource` and `dc_resource`). To change this setting, you can set the `max_parallel_updates` option in `update_settings`.

To allow 10 in parallel:

```python
update_settings(max_parallel_updates=10)
```

To force all deploys to happen in serial:

```python
update_settings(max_parallel_updates=1)
```

To run `local_resource` commands in parallel, you will need to manually mark the resource
as parallelizable:

```python
local_resource(name, cmd, allow_parallel=True)
```

See the [`local_resource` guide](local_resource.html) for more info.

## Other Types of Dependencies

Resource dependencies are designed to help when different versions
of services are broadly compatible with each other.

They focus on ensuring that *some* instance of a resource's dependencies exist.
They are not concerned with whether it's a *current* version. 

For this reason, `resource_deps` currently only affects the first build after a
`tilt up`.  Once any version of `database` has been running at least once, its
dependencies are unblocked to build for the rest of Tilt's lifetime.

For discussions on other types of dependencies in Tilt that could exist in the future, see these issues:

- [https://github.com/tilt-dev/tilt/issues/3048](https://github.com/tilt-dev/tilt/issues/3048)

- [https://github.com/tilt-dev/tilt/issues/3667](https://github.com/tilt-dev/tilt/issues/3667)
