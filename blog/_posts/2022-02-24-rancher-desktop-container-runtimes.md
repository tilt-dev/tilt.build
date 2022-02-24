---
slug: "rancher-desktop-container-runtimes"
date: 2022-02-24
author: milas
layout: blog
title: "Rancher Desktop: Should You Use containerd Or dockerd?"
image: "/assets/images/rancher-desktop-container-runtimes/title.jpg"
image_caption: 'Photo by <a rel="noopener noreferrer" href="https://unsplash.com/photos/u0vgcIOQG08">Jens Lelie</a> on Unsplash'
description: "Configure Tilt to build images with kim for use with Rancher Desktop"
tags:
- docker
- moby
- containerd
- rancher
- kubernetes
---

[Rancher Desktop][rancher-desktop], a lightweight and local Kubernetes cluster solution, has been evolving _fast_ over the past few months!

Early releases used [containerd][] behind-the-scenes with an experimental CLI tool, [`kim`][kim], to build images.
I wrote up a blog post about how easy it was to integrate with Tilt: [Writing Yet Another Custom Image Builder][blog-kim-extension].

Since then, however, Rancher Desktop has started also supporting Docker (aka `dockerd (moby)`) as an alternative to containerd.
Furthermore, [`kim`][kim] is no longer under active development.

While this might seem like a lot of churn, none of this is necessarily a bad thing!
In fact, when I was first writing about all this, our CTO, Nick, even predicted some of these changes.

If you're currently a Docker Desktop user who's interested in checking out Rancher Desktop, you're also in luck:
I've updated our [Switch from Docker Desktop to Rancher Desktop in 5 Minutes][blog-rancher-desktop-switch] blog post! 🎉

While that post is a great place to start, let's take a peek at the container runtime options in a bit more detail.
Why might you choose one over the other?
How do they work with Tilt?

### containerd
The default container runtime in Rancher Desktop is [containerd][].

These days, it's also the de facto standard container runtime used in production Kubernetes installs, so it's not surprising it's the default here!
In fact, it's also used by [kind][] and in some [minikube][minikube-runtime] configurations among others.

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

So, why are some reasons we would opt to use [containerd][] with Rancher Desktop?
* You're using containerd in prod and want your dev environment to mirror that
* [containerd][] and [nerdctl][] enable some features not possible with Docker (e.g. lazy-pulling with [stargz][])
* It's the default in Rancher Desktop, so it avoids extra set up steps
* You don't require Docker for other, non-Tilt parts your workflow

### dockerd (moby)
It's also possible to run Rancher Desktop with Docker/[moby][] as the container runtime.
([moby][] is the name of the OSS components used in Docker's commercial offerings.)

At this point, it's worth mentioning that Docker itself is actually built on containerd.
containerd originated by [being spun out of Docker and donated to CNCF][docker-containerd].
Docker, as a developer-centric tool, adds a lot of convenience on top to provide a great end-user experience.
(As a result, Docker does not support all possible options from containerd and vice-versa.)

If we're running Rancher Desktop with the `dockerd (moby)` container runtime, we can use the built-in [`docker_build`][tiltfile-docker-build] function:
```python
docker_build(
    ref='registry.example.com/my-image',
    context='.',
)
```
Take a look at our [Switch to Docker Desktop in 5 Minutes][blog-rancher-desktop-switch] post for a more detailed walkthrough.

Why might you use Rancher Desktop with the Docker runtime?
* Parts of your workflow rely on the `docker` CLI or API directly
* Support other Docker-based, local cluster solutions easily
* Experimenting/toying with Rancher Desktop

### Conclusion
Personally, I think the `dockerd (moby)` option is the better option for teams that are not reliant on containerd-only features.
It works with Tilt out-of-the-box without `Tiltfile` changes and enables straightforward interoperability with tools that only support Docker.

However, in practice, Docker and containerd are often trivially interchangeable.
Additionally, Tilt's support for non-Docker image builds means you don't lose out on features like [immutable tags][immutable-tags] or [Live Update][live-update] regardless of how you build your images.

There's really no wrong answer here - they're both great options! 🙌

[blog-kim-extension]: /2021/09/05/kim-extension.html
[blog-rancher-desktop-switch]: /2021/09/07/rancher-desktop.html
[containerd]: https://containerd.io/
[docker-containerd]: https://www.docker.com/blog/containerd-joins-cncf/
[ext-nerdctl]: https://github.com/tilt-dev/tilt-extensions/tree/master/nerdctl
[immutable-tags]: https://docs.tilt.dev/custom_build.html#why-tilt-uses-immutable-tags
[kim]: https://github.com/rancher/kim
[kind]: https://kind.sigs.k8s.io/
[live-update]: https://docs.tilt.dev/live_update_reference.html
[minikube-runtime]: https://minikube.sigs.k8s.io/docs/handbook/config/#runtime-configuration
[moby]: https://github.com/moby/moby
[nerdctl]: https://github.com/containerd/nerdctl
[rancher-desktop]: https://rancherdesktop.io/
[stargz]: https://github.com/containerd/nerdctl/blob/master/docs/stargz.md
[tiltfile-custom-build]: https://docs.tilt.dev/api.html#api.custom_build
[tiltfile-docker-build]: https://docs.tilt.dev/api.html#api.docker_build
