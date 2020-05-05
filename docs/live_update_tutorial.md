---
title: Faster Development with Live Update (Tutorial)
layout: docs
---
This tutorial looks at a `Tiltfile` with build optimizations.
We explain what they do, and why you would want to use them.

##### (This is a tutorial that walks you through a sample project. If you're looking for technical specs and details, check out the [Live Update Reference](live_update_reference.html) docs.)

In the [Tutorial](tutorial.html), we introduced the `docker_build()` function.
This function builds a Docker image. Tilt will watch the inputs to the
image, and rebuild it every time they change.

This works well for interpreted languages like JavaScript and Python
where you can add the files and go. For servers that need to be compiled,
it would be too slow to recompile from scratch every time.

That's why Tilt has a feature called Live Update for lightning-fast local
Kubernetes development.

Let's look at an example in the [tiltdemo repo](https://github.com/windmilleng/tiltdemo):

```
git clone https://github.com/windmilleng/tiltdemo
cd tiltdemo
```

The `Tiltfile` at the root of the repo contains this example:

```python
# tiltdemo1
k8s_yaml('deployments/demoserver1.yaml')
dm1_img_name = 'gcr.io/windmill-test-containers/tiltdemo/demoserver1'
docker_build(dm1_img_name, '.', dockerfile='Dockerfile.server1',
  live_update=[
    sync('cmd/demoserver1', '/go/src/github.com/windmilleng/tiltdemo/cmd/demoserver1'),
    run('go install github.com/windmilleng/tiltdemo/cmd/demoserver1'),
    restart_container(),
  ]
)
```

This looks similar to the `Tiltfile` in previous tutorials, but when we specify
how to build the image with `docker_build()`, we pass an additional argument,
`live_update`, containing a list of steps for how to update the running container.
Let's zoom in on that part of the configuration.


```python
docker_build(...,
  live_update=[
    sync('cmd/demoserver1', '/go/src/github.com/windmilleng/tiltdemo/cmd/demoserver1'),
    run('go install github.com/windmilleng/tiltdemo/cmd/demoserver1'),
    restart_container(),
  ]
)
```

These lines configure `tilt` to do incremental updates to containers running the
image we're currently specifying (when possible). We'll step through it line by line.

* `sync('cmd/demoserver1', '/go/src/github.com/windmilleng/tiltdemo/cmd/demoserver1'),`

The `sync` method copies a file or directory from outside your container to inside of your container.

In this case, we copy the directory `./cmd/demoserver1` (relative to the Tiltfile) into
the container filesystem.

The normal `docker_build` behavior is to watch all files in the docker build context (`.`),
and any time one changes, to do an image build and redeploy. The `sync` here says that, if
the changed file matches `cmd/demoserver1`, to instead do a `live_update` - Tilt will copy
the changed files into the container and execute any appropriate `run` or `restart_container`
steps, without actually building or pushing a docker image or performing a k8s deploy.

* `run('go install github.com/windmilleng/tiltdemo/cmd/demoserver1')`

The `run` method runs shell commands inside your container.

Every time a `live_update` runs (i.e., when a file matching a `sync` changes), Tilt will run
this command again.

One of the major build optimizations here is that Tilt runs your command inside the existing
container, instead of building from scratch to create a fresh image. This is much closer to how
we normally run commands for local development. Real humans don't delete all their code and
re-clone it from git every time we need to do a new build! Instead, we re-run the command in
the same directory. Modern tools then take advantage of local caches; Tilt runs commands with
the same approach, but inside a container.

* `restart_container()`

This specifies that the container should be restarted after the other update steps have been
applied. Any changed files stay around and, in the case of k8s, the pod stays where it is. This is
effectively just re-starting the service in the existing container.

For languages/frameworks like Node or Flask that have hot reloading (i.e., they can pick up code
changes without restarting the process), this step is unnecessary.

In this guide, we explored just a few of the functions we can use in a `Tiltfile`
to keep your build fast. For even more functions and tricks,
read the complete [Tiltfile API reference](api.html).
