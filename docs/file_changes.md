---
title: "Debugging File Changes: Rebuilds and Ignores"
layout: docs
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

## Watching Files

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

## Ignoring Files

### .git

Tilt will always ignore changes under the `.git` directory.

When you use `docker_build()` in your `Tiltfile`, Tilt will remove `.git` from
the Docker context.

### Editor temp files

Tilt has a hard-coded list of temp files in common text editors (Emacs, Vim, etc.).

As devtools developers ourselves, we want to be able to add hidden files to the
repo, and not have those hidden files affect other devtools. For example, we
don't think Emacs developers wanted their temp files to break Docker
caching. Lots of users get confused when this happens, because it's not a file
they control.

If you find that temp files in your editor trigger builds, please
[file a bug](https://github.com/windmilleng/tilt/issues/new)
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

### docker_build and only=

The `docker_build()` call's `only=` parameter excludes everything *but* the file
paths specified in `only`.

For example,

```
docker_build('image-name', '.', only=['./src', './static-files'])
```

is equivalent to having a `.dockerignore` file that looks like:

```
**
!./src
!./static-files
```

The `only=` parameter accepts paths, not glob patterns.

### .tiltignore

The `.tiltignore` file tells Tilt about file changes that should not trigger rebuilds.

Tilt looks for a file named `.tiltignore` in the same directory as your
`Tiltfile`. The `.tiltignore` patterns have the same syntax as `.dockerignore`.
Learn more about `.dockerignore` in
[the Dockerfile reference](https://docs.docker.com/engine/reference/builder/#dockerignore-file).

Files that match these patterns will not trigger rebuilds.

`.tiltignore` does not affect whether a file is included in any Docker
build contexts.

## Try it Yourself

If you'd like to try out the APIs in this guide, see
[this example repo](https://github.com/windmilleng/ignore-examples). You can:

- `git clone https://github.com/windmilleng/ignore-examples`
- `tilt up` to run all the servers
- Try editing the files and see which servers reload.

## Future Work

If Tilt rebuilds an image, you should always be able to look at the logs
and see which file change triggered that rebuild.

But there are still cases that are hard to debug:

1) If Tilt ignored a file change, which rule blocked the file? Was it a
`.dockerignore` or a `.tiltignore`?

2) If a Docker image build wasn't cached correctly, which file change broke the
cache? Are there files in my Docker image that shouldn't be there?

We are open to thoughts and
[feature requests](https://github.com/windmilleng/tilt/issues/new) on how to
help people answer these questions!
