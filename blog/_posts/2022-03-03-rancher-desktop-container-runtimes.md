---
slug: "rancher-desktop-container-runtimes"
date: 2022-03-03
author: milas
layout: blog
title: "Rancher Desktop: Should You Use containerd Or dockerd?"
image: "/assets/images/rancher-desktop-container-runtimes/title.jpg"
image_caption: 'Photo by <a rel="noopener noreferrer" href="https://unsplash.com/photos/u0vgcIOQG08">Jens Lelie</a> on Unsplash'
description: "Pick a container runtime, any container runtime"
tags:
- docker
- containerd
- rancher
- kubernetes
---

[Rancher Desktop][rancher-desktop], a lightweight and local Kubernetes cluster solution, has been evolving _fast_ over the past few months!

Early releases used [containerd][] behind-the-scenes with an experimental CLI tool, [kim][], to build images.
I wrote up a blog post about how easy it was to integrate with Tilt: [Writing Yet Another Custom Image Builder][blog-kim-extension].

Since then, however, Rancher Desktop has started also supporting Docker as an alternative to containerd.
Furthermore, [kim][] is no longer under active development, and [nerdctl][] is now the recommended way to build images when using Rancher Desktop with containerd.

While this might seem like a lot of churn, none of this is necessarily a bad thing!
[nerdctl][] is a project that uses a lot of the same architecture + components as [kim][].
By focusing all the community energy on a single project, we'll get a better, more well-maintained tool overall, and both kim and nerdctl users will benefit.

If you're currently a Docker Desktop user who's interested in checking out Rancher Desktop, you're also in luck:
I've updated our [Switch from Docker Desktop to Rancher Desktop in 5 Minutes][blog-rancher-desktop-switch] blog post! 🎉

While that post is a great place to start, let's take a peek at the container runtime options in a bit more detail.
Why might you choose one over the other?
How do they work with Tilt?

### containerd
The default container runtime in Rancher Desktop is [containerd][].

If you haven't heard of containerd, it's the de facto standard container runtime used in production Kubernetes installs.

This might come as a surprise!
At this point, it's worth mentioning that Docker itself is actually built on containerd.
containerd originated by [being spun out of Docker and donated to CNCF][docker-containerd].
While this has led to some confusion in the past, the official Kubernetes blog post [Don't Panic: Kubernetes and Docker][k8s-blog-dockershim] does a great job explaining things.
And, like the title says, Don't Panic!

Within the local cluster space, containerd is also used by [kind][] and in some [minikube][minikube-runtime] configurations among others.

A popular option for building images with containerd is [nerdctl][] (a non-core subproject of containerd).
As a bonus, `nerdctl` is drop-in compatible for the `docker` command.
Luckily for us, Rancher Desktop even bundles a version of `nerdctl` already configured to build to its containerd instance.

Be sure it's enabled by opening the Rancher Desktop preferences, navigating to **Supporting Utilities**, and checking the box for `nerdctl`.

![Rancher Desktop preferences pane showing the nerdctl option](/assets/images/rancher-desktop-container-runtimes/nerdctl.png)

Once that's done, we can use it with Tilt via the [`nerdctl` extension][ext-nerdctl].
For example:
```python
# docker_build(
#     ref='registry.example.com/my-image',
#     context='.',
# )
# ⬇️ ⬇️ ⬇️ ⬇️
load('ext://nerdctl', 'nerdctl_build')
nerdctl_build(
    ref='registry.example.com/my-image',
    context='.',
)
```

Now that we know _how_ to use containerd with Tilt, **why** might we opt to use it as our container runtime?

Simplicity!

Docker, as a developer-centric tech stack, adds a lot of convenience on top to provide a great end-user experience.
These higher-level abstractions are invaluable for humans but often add additional complexity for software.

In fact, to use Docker as the container runtime for Kubernetes, a translation component named [cri-dockerd][] (formerly `dockershim`) is necessary.

Furthermore, Docker does not support all possible options from containerd (and vice-versa).
For example, lazy-pulling (and building) [eStargz][stargz] images is supported by containerd/nerdctl, but not Docker ([containerd/stargz-snapshotter#258][stargz-snapshotter-support]).
However, this really only applies to bleeding-edge features, so don't sweat it unless you rely on these.

### Docker
More recently, it's also possible to run Rancher Desktop with Docker as the container runtime.

This allows Rancher Desktop to function as a drop-in replacement for Docker Desktop in many cases.

---
#### ⚠️ Watch Out!
You cannot run both Docker Desktop and Rancher Desktop (in `dockerd` mode) simultaneously!
See [rancher-desktop#1081][rd-issues-1081] for details.

---

If we've configured Rancher Desktop to use `dockerd (moby)` as the container runtime, we can use the built-in [`docker_build`][tiltfile-docker-build] function:
```python
docker_build(
    ref='registry.example.com/my-image',
    context='.',
)
```
💁‍♀️ Take a look at our [Switch to Docker Desktop in 5 Minutes][blog-rancher-desktop-switch] post for a more detailed walkthrough.

If containerd is already used under the hood by Docker, why might you use Rancher Desktop with the Docker runtime?

Compatibility!

Docker has been around for longer than containerd and has an entire ecosystem of tools built directly around it.
Many repos also have helper shell scripts or `Makefile` tasks that use the Docker CLI.

Additionally, it's a great way to try out Rancher Desktop if you're curious and currently use Docker, as no `Tiltfile` changes are needed.
This also makes it easier to support if not everyone on your team (or contributor to your project) uses the same cluster solution.

### Conclusion
Personally, I think Docker is the better option for teams that are not reliant on containerd-only features.
It works with Tilt out-of-the-box without `Tiltfile` changes and enables straightforward interoperability with tools that only support Docker.

However, in practice, Docker and containerd are often trivially interchangeable.
Additionally, Tilt's support for non-Docker image builds means you don't lose out on features like [immutable tags][immutable-tags] or [Live Update][live-update] regardless of how you build your images.

There's really no wrong answer here - they're both great options! 🙌

[blog-kim-extension]: /2021/09/05/kim-extension.html
[blog-rancher-desktop-switch]: /2021/09/07/rancher-desktop.html
[containerd]: https://containerd.io/
[cri-dockerd]: https://github.com/Mirantis/cri-dockerd
[docker-containerd]: https://www.docker.com/blog/containerd-joins-cncf/
[ext-nerdctl]: https://github.com/tilt-dev/tilt-extensions/tree/master/nerdctl
[immutable-tags]: https://docs.tilt.dev/custom_build.html#why-tilt-uses-immutable-tags
[k8s-blog-dockershim]: https://kubernetes.io/blog/2020/12/02/dont-panic-kubernetes-and-docker/
[kim]: https://github.com/rancher/kim
[kind]: https://kind.sigs.k8s.io/
[live-update]: https://docs.tilt.dev/live_update_reference.html
[minikube-runtime]: https://minikube.sigs.k8s.io/docs/handbook/config/#runtime-configuration
[moby]: https://github.com/moby/moby
[nerdctl]: https://github.com/containerd/nerdctl
[rancher-desktop]: https://rancherdesktop.io/
[rd-issues-1081]: https://github.com/rancher-sandbox/rancher-desktop/issues/1081
[stargz]: https://github.com/containerd/nerdctl/blob/master/docs/stargz.md
[stargz-snapshotter-support]: https://github.com/containerd/stargz-snapshotter/issues/258
[tiltfile-custom-build]: https://docs.tilt.dev/api.html#api.custom_build
[tiltfile-docker-build]: https://docs.tilt.dev/api.html#api.docker_build
