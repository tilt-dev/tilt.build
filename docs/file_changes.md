---
title: "Debugging File Changes: Rebuilds and Ignores"
description: "What do you do when a file changes, but Tilt does the wrong thing?"
layout: docs
sidebar: guides
---

Tilt watches your file system, and rebuilds any resources that have changed.

But what do you do when a file changes, but Tilt does the wrong thing?

This page should help you understand when file changes trigger builds, and when
they don't.

## Basic Principles

1) When Tilt builds a resource, it should print which file changes triggered
that build.

2) When a file changes that you don't have control over, Tilt should not do a
rebuild.

3) We optimize the syntax so that it's easy to ignore spurious file changes,
and hard to watch too much.

## Where File Watches Come From

### Tiltfiles

Tilt will always watch the Tiltfile. If the Tiltfile changes, Tilt will re-execute it.
Most notably, this re-runs any `local()` calls.

When it's finished, it will diff all the `docker_build()` and `k8s_yaml()`
configurations, and only rebuild the ones that have changed.

### How Tilt watches new files

Most Tiltfile built-in functions will automatically set up watches
for the files they read. If those files change, they re-run the Tiltfile.

This includes `helm()`, `load()`, and `read_file()`.

If your Tiltfile contains a `local()` call that reads from a file,
Tilt has no way to know what file it reads. You can tell it to watch additional
files with the [`watch_file()` function](api.html#api.watch_file).

### Image Builds

When you include a `docker_build()` in your Tiltfile, you give Tilt
a directory to build. Tilt will watch the entire directory.

Whenever a file in that directory changes, Tilt will re-build the image,
then deploy any Kubernetes resources that depend on that image.

### Custom and Local Resource Builds

When you build other types of resources (like `custom_build()` and
`local_resource()`), you can specify a file system path or a list of paths as
`deps`.

Whenever a file under that path changes, Tilt will re-run the specified scripts.

## Where Ignores Come From

### .git

Tilt will always ignore changes under the `.git` directory, since watching the
directory may trigger unintended builds and impact performance.

When you use `docker_build()` in your `Tiltfile`, Tilt will remove `.git` from
the Docker context.

If you need to include the `.git` directory in a build, you can use
[`custom_build`](custom_build.html) instead of `docker_build`.

### Editor temp files

Tilt has a hard-coded list of temp files in common text editors (Emacs, Vim, etc.).

As devtools developers ourselves, we want to be able to add hidden files to the
repo, and not have those hidden files affect other devtools. For example, we
don't think Emacs developers wanted their temp files to break Docker
caching. Lots of users get confused when this happens, because it's not a file
they control.

If you find that temp files in your editor trigger builds, please
[file a bug](https://github.com/tilt-dev/tilt/issues/new)
and we will add it to the list.

These temp files are still included in Docker build contexts by default.

### .dockerignore

Any docker_build commands will respect the `.dockerignore` file
in their build directory. Learn more about `.dockerignore` in [the
Dockerfile reference](https://docs.docker.com/engine/reference/builder/#dockerignore-file).

For all `docker_build` commands in this directory, files that match these
patterns will not trigger rebuilds, and will be excluded from the Docker build
context.

### docker_build and ignore=

For large multi-service repos, you may have multiple `docker_build()`s in the
same directory. With the `ignore=` parameter, you can add image-specific ignore
patterns.

For this specific `docker_build()` call, files that match these patterns will
not trigger rebuilds, and will be excluded from the Docker build context.

The patterns are evaluated relative to the `context` argument passed to `docker_build`. For instance, given the call:
```python
docker_build(
    'image-foo',
    './foo',  # context
    ignore=['bar']
)
```
Tilt will ignore the file `foo/bar`.

### ignore= and other build types

Both `custom_build()` and `local_resource()` also support the `ignore=`
parameter.

They handle it a little differently than `docker_build` does. See our [Custom
Build Guide](custom_build.html#adjust-file-watching-with-ignore).

### docker_build and only=

The `docker_build()` call's `only=` parameter excludes everything *but* the 
paths specified in `only`.

For example,

```python
docker_build(
    'image-foo',
    './foo',
    only=['./src', './static-files'])
```

is equivalent to having a `.dockerignore` file that looks like:

```
**
!./src
!./static-files
```

The `only=` parameter accepts paths, not glob patterns.

Again, these paths are evaluated relative to the `context` passed to
`docker_build`; in the call above, the only directories included in the
resulting image are `foo/src` and `foo/static-files`.

### only= and other build types

Other build types don't have an `only=` parameter.


For `docker_build`, `only=` filters what files are available to the docker
build within the build context. Other types of builds are simply able to access
all files, and `deps=` specifies which paths trigger them.

### .tiltignore

The `.tiltignore` file tells Tilt about file changes that should not trigger rebuilds.

Tilt looks for a file named `.tiltignore` in the same directory as your
`Tiltfile`. The `.tiltignore` patterns have the same syntax as `.dockerignore`.
Learn more about `.dockerignore` in
[the Dockerfile reference](https://docs.docker.com/engine/reference/builder/#dockerignore-file).

Files that match these patterns will not trigger rebuilds.

`.tiltignore` does not affect whether a file is included in any Docker
build contexts.

### watch_settings(ignore=)

The Tiltfile can specify additional patterns that should not trigger rebuilds.

This is equivalent to adding these patterns to `.tiltignore` (correcting for any
differences in working directory). It's useful in Tilt extensions that download
files, but that don't want the downloaded files to trigger rebuilds as they're
being downloaded.

`watch_settings` does not affect whether a file is included in any Docker build
contexts.

## Inspecting File Watches Yourself

Tilt has a [FileWatch
API](https://api.tilt.dev/core/file-watch-v1alpha1.html). 
At any time, you can inspect exactly which files a running Tilt environment is running
with the `tilt get filewatches` and `tilt describe filewatches` commands.

Let's look at a few examples with the [Plain Old Static HTML](/example_static_html.html) example project.

```shell
$ tilt get filewatches
NAME                       CREATED AT
configs:singleton          2021-05-04T22:00:32Z
image:example-html-image   2021-05-04T22:00:32Z
```


In this example, Tilt has two filewatches: one for reloading the Tiltfile
("configs:singleton"), and one for rebuilding the Docker image
("image:example-html-image").

Let's unpack those filewatches in more detail.

```shell
$ tilt get filewatches configs:singleton -o yaml
apiVersion: tilt.dev/v1alpha1
kind: FileWatch
metadata:
  annotations:
    tilt.dev/target-id: configs:singleton
  creationTimestamp: "2021-05-04T22:00:32Z"
  name: configs:singleton
  resourceVersion: "1"
  uid: 86e69fd0-c2e0-41f1-99ab-2c307c8a9e27
spec:
  watchedPaths:
  - /home/nick/src/tilt-example-html/0-base/.dockerignore
  - /home/nick/src/tilt-example-html/0-base/.tiltignore
  - /home/nick/src/tilt-example-html/0-base/Dockerfile
  - /home/nick/src/tilt-example-html/0-base/Tiltfile
  - /home/nick/src/tilt-example-html/0-base/kubernetes.yaml
status:
  lastEventTime: null
  monitorStartTime: "2021-05-04T22:00:32.286554Z"
```

When I print the full specification, I can see that we're watching 5 files. But
we haven't seen any changes yet.

Let's touch one of the files and see what happens:

```shell
$ touch /home/nick/src/tilt-example-html/0-base/Tiltfile
$ tilt get filewatches configs:singleton -o yaml
apiVersion: tilt.dev/v1alpha1
kind: FileWatch
metadata:
  annotations:
    tilt.dev/target-id: configs:singleton
  creationTimestamp: "2021-05-04T22:00:32Z"
  name: configs:singleton
  resourceVersion: "4"
  uid: 86e69fd0-c2e0-41f1-99ab-2c307c8a9e27
spec:
  watchedPaths:
  - /home/nick/src/tilt-example-html/0-base/.dockerignore
  - /home/nick/src/tilt-example-html/0-base/.tiltignore
  - /home/nick/src/tilt-example-html/0-base/Dockerfile
  - /home/nick/src/tilt-example-html/0-base/Tiltfile
  - /home/nick/src/tilt-example-html/0-base/kubernetes.yaml
status:
  fileEvents:
  - seenFiles:
    - /home/nick/src/tilt-example-html/0-base/Tiltfile
    time: "2021-05-04T22:04:09.056840Z"
  lastEventTime: "2021-05-04T22:04:09.056840Z"
  monitorStartTime: "2021-05-04T22:00:32.286554Z"
```

The file watch status field is immediately updated with the file change. Other
objects in Tilt read this change to figure out whether to reload.


### Hacking FileWatches

Reading APIs is boring. Let's make some changes.

The `tilt edit` command lets us change file watches on the fly.

```
$ EDITOR=emacs tilt edit filewatch configs:singleton
```

I'm going to go ahead and remove all the files.

Now, when I touch the Tiltfile again, nothing reloads:

```
$ touch /home/nick/src/tilt-example-html/0-base/Tiltfile
$ tilt get filewatches configs:singleton -o yaml
apiVersion: tilt.dev/v1alpha1
kind: FileWatch
metadata:
  annotations:
    tilt.dev/target-id: configs:singleton
  creationTimestamp: "2021-05-04T22:00:32Z"
  name: configs:singleton
  resourceVersion: "5"
  uid: 86e69fd0-c2e0-41f1-99ab-2c307c8a9e27
spec:
  watchedPaths:
  - /home/nick/src/tilt-example-html/0-base/.dockerignore
status:
  lastEventTime: null
  monitorStartTime: "2021-05-04T22:08:23.820911Z"
```

`tilt edit` is a convenient way to debug file watch problems. I sometimes turn file watches
off if I don't want them to trigger reloads. Or I add new ignore patterns to test them.

When I reload the Tiltfile (e.g., by clicking the reload button in the Tilt UI),
Tilt will regenerate all the file watches from scratch, blowing any of my
temporary edits away.

## Try it Yourself

If you'd like to try out the APIs in this guide, see
[this example repo](https://github.com/tilt-dev/ignore-examples). You can:

- `git clone https://github.com/tilt-dev/ignore-examples`
- `tilt up` to run all the servers
- Try editing the files and see which servers reload.
- In a separate terminal, run `tilt get filewatches` and `tilt describe filewatches` to see how Tilt processes the edits.

## Future Work

If Tilt rebuilds an image, you should always be able to look at the logs
and see which file change triggered that rebuild.

But there are still cases that are hard to debug:

1) If Tilt ignored a file change, which rule blocked the file? Was it a
`.dockerignore` or a `.tiltignore`?

2) If a Docker image build wasn't cached correctly, which file change broke the
cache? Are there files in my Docker image that shouldn't be there?

We are open to thoughts and
[feature requests](https://github.com/tilt-dev/tilt/issues/new) on how to
help people answer these questions!
