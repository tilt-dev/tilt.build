---
title: Optimizing a Tiltfile
layout: docs
---

This tutorial looks at a `Tiltfile` with build optimizations.
We explain what they do, and why you would want to use them.

In the [Tutorial](tutorial.html), we introduced the `docker_build()` function.
This function builds a Docker image. Tilt will watch the inputs to the
image, and rebuild it every time they change.

This works well for interpreted languages like JavaScript and Python
where you can add the files and go. For servers that need to be compiled,
it would be too slow to recompile from scratch every time.

That's why Tilt has a function `live_update()` for lightning-fast local
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
docker_build(dm1_img_name, '.', dockerfile='Dockerfile.server1')
live_update(dm1_img_name,
  [
    sync('cmd/demoserver1', '/go/src/github.com/windmilleng/tiltdemo/cmd/demoserver1'),
    run('go install github.com/windmilleng/tiltdemo/cmd/demoserver1'),
    restart_container(),
  ])
```

This looks similar to the `Tiltfile` in previous tutorials, but in addition to specifying
how to build the image with `docker_build()`, it specifies how to update the running
image with `live_update()`. Let's zoom in on that part of the configuration.


```python
live_update(dm1_img_name,
  [
    sync('cmd/demoserver1', '/go/src/github.com/windmilleng/tiltdemo/cmd/demoserver1'),
    run('go install github.com/windmilleng/tiltdemo/cmd/demoserver1'),
    restart_container(),
  ])
```

These lines configure `tilt` to do incremental image builds. We'll step through it line-by-line.

* `live_update(dm1_img_name,`

This specifies we're configuring live updates for any container running `dm1_img_name`.

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

One of the major build optimizations that Tilt does is to keep the container around, and
start the command inside the running container.

This is much closer to how we normally run commands for local development. Real humans
don't delete all their code and re-clone it from git every time we need to do a new build!
Instead, we re-run the command in the same directory. Modern tools then take advantage of local caches;
Tilt runs commands with the same approach, but inside a container.

* `restart_container()`

This specifies that the container should be restarted after the other update steps have been
applied. Any changed files stay around and, in the case of k8s, the pod stays where it is. This is
effectively just re-starting the service in the existing container.

For languages/frameworks with hot reloading (i.e., they can pick up code changes without
restarting the process), like node or flask, this step is unnecessary.

In this guide, we explored just a few of the functions we can use in a `Tiltfile`
to keep your build fast. For even more functions and tricks,
read the complete [Tiltfile API reference](api.html).
