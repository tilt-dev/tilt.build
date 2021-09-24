---
slug: "docker-does-not-mean-slow"
date: 2021-09-13
author: milas
layout: blog
title: "Docker Does Not Mean Slow"
image: "/assets/images/docker-does-not-mean-slow/title.jpg"
image_caption: 'Photo by <a rel="noopener noreferrer" target="_blank" href="https://unsplash.com/@javier365">Javier Mazzeo</a>'
description: "Speed up your Docker builds with .dockerignore and cache mounts"
tags:
  - docker
---

There are _lots_ of guides out there about speeding up your Docker image builds.
(Some of them are even written by folks other than ourselves!)

This blog post isn't comprehensive but instead focuses on a couple of oft-neglected and lesser-known techniques.

First, we'll cover some common pitfalls that `.dockerignore` can help you avoid.
Then we'll look at `cache` mounts that let you re-use files between builds even after layers have been invalidated.

Now's a good time to grab a coffee: we're going to dive in head-first! ☕️

### Create & Tune Your `.dockerignore`
Docker supports a special [`.dockerignore`][dockerignore] file, which excludes files from the image build context based on file patterns.
For example, the pattern `**/*.tmp` will ignore any files with the `.tmp` extension at the root build context directory and any of its subdirectories, recursively.

You might be familiar with `.gitignore`, which excludes files from being committed to your repo.
A common misconception is that `.dockerignore` is **additive** with `.gitignore`, but Docker does NOT use `.gitignore`!
(Additionally, while they look very similar, the file glob pattern syntax differs between them.)

There are two big reasons an un-tuned `.dockerignore` file can result in performance woes: unnecessary layer cache invalidation and increased Docker context size.

#### Unnecessary Layer Cache Invalidation
Unnecessary layer cache invalidation can happen when **unused** files are added to an image.
For example, if your Dockerfile has `COPY . /app`, whenever `README.md` changes, the layer will be invalidated even though no source code changed!
This means the next image build will have to re-run that step and all subsequent ones.

There can be more insidious instances of this such as generated files that change with every build or locally compiled build artifacts (e.g. `target/` or `out/` directories).

One thing to consider is whether you run tests as part of your image build or from a container using the built image.
If not, you might consider excluding test source files (e.g. `*_test.go` for Go, `src/test` for Java).

#### Bloated Docker Context Size
At the start of the build, Docker creates a tar archive from the build context (e.g. your project directory) for the daemon to use.
**Even if you don't reference files as part of your build via `COPY`, you still pay the cost of archiving and transferring them to the Docker daemon!**
This can be particularly slow on Docker for Mac/Windows or if using a remote Docker context.

Perhaps the most common case of this is your repository's `.git/` directory, which can generally be excluded.
(If your builds embed Git metadata such as a commit reference, consider using [build arguments][build-args] to pass them in - most CI systems provide this metadata as environment variables and you can set defaults as placeholders for local builds.)

Large test/sample data files that aren't ever used by the build or resulting image can be another common culprit.
Similarly, some tools create Python virtual environments in the corresponding project directory.

Lastly, if you rely on installing npm/yarn dependencies from scratch in your Dockerfile for reproducibility, exclude `node_modules/`.
(As a bonus, this helps avoid platform & architecture mismatch issues that can result from transferring binaries meant for your host platform, like Windows or macOS, into a Linux container image!)

#### Explore Your Context
If you want to inspect your build context, you can use Docker to export a copy to `/tmp/docker-context`:
```sh
printf 'FROM scratch\nCOPY . /' | DOCKER_BUILDKIT=1 docker build -f - -o /tmp/docker-context .
```
You can then browse `/tmp/docker-context` via CLI or file manager to ensure that irrelevant files are not present.

For more information on `.dockerignore`, read the [official docs][dockerignore].

### Leverage `cache` Mounts to Avoid Re-downloading Artifacts
You might be familiar with Docker volume mounts when _running_ containers.
For example, these are commonly used to share a local directory with commands like `docker run -v $(pwd)/awesome:/app/awesome my-image`.

Docker also supports [_build_ mounts][build-mounts] via the underlying BuildKit engine.
These are very powerful; for example, the `ssh` mount type allows sharing SSH keys in the build to access private resources.

Of interest for performance is the `cache` mount type.
Files in a `cache` mount persist between builds but are NOT included in the resulting images.
We can use this for package manager and compiler caches to speed up subsequent builds without bloating the final image.

For example, imagine we have a Java project:
```dockerfile
FROM mvn

COPY pom.xml ./
RUN mvn dependency:resolve

COPY src/java ./src/java
RUN mvn package
```

We've already separated out our dependency download from copying in source files and compilation to optimize the layer cache, which is great!

However, if we change _anything_ in `pom.xml`, because the layer cache is invalid, we will have to re-download **all** dependencies from scratch.

We can prevent this with a `cache` mount on `/root/.m2` which is where Maven stores its package cache:
```dockerfile
FROM mvn

COPY pom.xml .
RUN --mount=type=cache,target=/root/.m2 \
    mvn dependency:resolve

COPY src/java ./src/java
RUN  --mount=type=cache,target=/root/.m2 \
    mvn package
```

Note that we _also_ need to attach the mount to the actual compilation step!

Now, when `pom.xml` changes, even though the layer cache has been invalidated, when dependencies are resolved, the `/root/.m2` cache mount can help prevent the need to download everything from scratch.

While the path(s) to cache can vary by language, the process remains the same.
For example, [npm maintains a cache][npm-cache] at `~/.npm` and Yarn allows [customizing the cache location][yarn-cache] with the `YARN_CACHE_FOLDER` environment variable.

Some languages, like Go, make it easy to share the compiler cache as well:
```dockerfile
FROM golang

ENV GOMODCACHE=/cache/gomod
ENV GOCACHE=/cache/gobuild

COPY go.mod go.sum ./
RUN --mount=type=cache,target=/cache/gomod \
    go mod download

COPY main.go .
RUN --mount=type=cache,target=/cache/gomod \
    --mount=type=cache,target=/cache/gobuild,sharing=locked \
    go build -o /my-app main.go
```

Here, we created two caches: one for the package manager and one for the compiler.
We've additionally marked the compiler cache as `sharing=locked` to prevent multiple concurrent builds from using it simultaneously.
Before caching compiler output, be sure to consider the potential impact on image build reproducibility, which might depend on your particular language/compiler!

You can also use this technique to [cache OS package manager packages][apt-cache] (e.g. those installed with `apt` for Debian/Ubuntu-based images).

### What Else?
There are many other tricks to speed up your Docker builds while keeping your images small, but a lot of it comes down to profiling your specific setup and iterating.

While optimizing your `Dockerfile`, try building with `--progress=plain` and/or `--no-cache` to get a more traditional, linear log output to help identify slow steps.
Try changing different types of files (source code, package manager manifest, README, etc.) and observe the effect on a re-build.

Finally, a popular technique, particularly for compiled languages, is to use [multi-stage builds][multi-stage-builds].
You can use this in some creative ways: stay tuned for the next entry in this series that will focus on that!

[apt-cache]: https://github.com/moby/buildkit/blob/master/frontend/dockerfile/docs/syntax.md#example-cache-apt-packages
[build-args]: https://docs.docker.com/engine/reference/builder/#arg
[build-mounts]: https://github.com/moby/buildkit/blob/master/frontend/dockerfile/docs/syntax.md#build-mounts-run---mount
[dockerignore]: https://docs.docker.com/engine/reference/builder/#dockerignore-file
[multi-stage-builds]: https://docs.docker.com/develop/develop-images/multistage-build/
[npm-cache]: https://docs.npmjs.com/cli/v7/commands/npm-cache#cache
[yarn-cache]: https://classic.yarnpkg.com/en/docs/cli/cache/#toc-change-the-cache-path-for-yarn
