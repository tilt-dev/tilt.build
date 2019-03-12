---
title: Tiltfile Concepts 2
layout: docs
---

A Tiltfile is a Starlark program that Tilt runs to generate a configuration. This doc describes how the concepts in a Tiltfile, to let you better understand what Tilt is doing. You should have already looked at a simple Tiltfile, like in the [tutorial](tutorial.html).

You'll learn about Resources (Tilt's low-level configuration), Directives (high-level configuration), Assembly (the process that compiles Directives into Resources), and how to debug a Tiltfile.

## Resources
A Resource is the unit of organization for Tilt's engine and UI. It's identified by a name and contains information on how to build container images and how to deploy objects to Kubernetes or Docker Compose. It also contains what to watch in the local filesystem and cluster and how to interact with these systems. In the UI, each resource is one row that combines status from across the phases.

This grouping makes Tilt more useful: it's easier to see what's going on when related errors are in the same place. A Resource should contain objects that are related in the mind of the user.

Resources are low-level and having to list them fully would be tedious and error-prone. For example, an image that's used in a sidecar in every deployment would have to be listed in each Resource. A Tiltfile doesn't create a Resource directly, but instead creates high-level Directives that guide Tilt to create Resources.

## Directives
Tiltfile functions like `docker_build` and `k8s_yaml` are useful for their side effect: telling Tilt about your project. This information is called a Directive, which is recorded by calling the function.

Examples of functions that register Directives, and a description of the Directive:
*) `docker_build`, `custom_build`: how to build an image (and watch the filesystem for when to rebuild)
*) `k8s_yaml`: yaml for Kubernetes objects
*) `k8s_kind`: how Tilt should treat a CRD

Examples of functions that don't register Directives:
*) `read_file` and `listdir`: return the contents of a file or directory
*) `kustomize`: return the result of running Kustomize

Directives are the input to Assembly.

## Assembly
Assembly is the step that compiles Directives into Resources. Assembly applies a series of rules to group related objects and images into Resources. Let's go through each step of Assembly.

### Images
Tilt supports images that depend on other images. If image `bar` depends on image `foo`, and Tilt knows how to build each, then when you change a file in `bar`, Tilt will rebuild `bar` and then rebuild `foo`, using the new `bar`. To assemble an image, Tilt looks for dependencies it knows how to build and adds a link. Tilt creates this link automatically, without any extra configuration:

```python
docker_build('bar', './bar')
docker_build('foo', './foo')
```

### Workloads
Tilt then looks for Kubernetes objects that are workloads: objects that contain an image and create pods. For example, deployments, pods, or CRDs that run pods, but not secrets. Assembly then iterates over each workload and puts it into a resource.

For each workload object, find the right Resource. By default, Tilt will auto-assign a Resource name equal to the name of the workload object. (For historical reasons, you can use the function `assemble_group_by_image(true)` to use the basename of the first Tilt-built image, instead.) You can override this default Resource using `k8s_resource`. `k8s_resource` lets you define a new Resource and define which objects will be placed in the Resource.

```python
# create a resource foo with workload objects that use the specified image
k8s_resource('foo', image='gcr.io/companyname/foo')

# create a resource bar with workload objects that match the labels
k8s_resource('bar', labels={'app': 'bar'})

# create a resource baz even though the deployment is named app-baz
k8s_resource('baz', k8s_name='app-baz')
```

Assembly adds Kubernetes services that match the workload to the Resource.

### Remaining objects
After putting each workload object into a Resource, there may be objects leftover. E.g. secrets or ConfigMaps; they don't require building but need to be deployed. Assembly adds these into a special Resource called `k8s_yaml`.

## Debugging
The Assembly phase can make a Tiltfile feel like magic. This is good when it works like you want, but infuriating if it means you can't understand why it's not working as you expect.

The Tilt UI also includes a special Resource called "Tiltfile". When you select it, it shows you a log of running the Tiltfile that lets you see each Directive being registered during Execution and the decisions Tilt makes at each step of Assembly.
