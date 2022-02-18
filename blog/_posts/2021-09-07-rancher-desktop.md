---
slug: "rancher-desktop"
date: 2021-09-07
author: milas
layout: blog
title: "Switch from Docker Desktop to Rancher Desktop in 5 Minutes"
image: "/assets/images/rancher-desktop/title.jpg"
image_caption: 'Photo by <a rel="noopener noreferrer" target="_blank" href="https://unsplash.com/@timwilson7">Tim Wilson</a>'
description: "Tilt + Rancher Desktop = 🤘"
tags:
- docker
- rancher
- kubernetes
---

---
### 📣 Update (February 2022)
We've revamped this blog post to reflect recent changes to both Tilt and [Rancher Desktop][rancher-desktop].

The good news? It's easier than ever to use Tilt and [Rancher Desktop][rancher-desktop] together!

(There is no bad news.)

---

[Rancher Desktop][rancher-desktop] is a new way to run Kubernetes on macOS and Windows.

![Rancher Desktop interface on macOS](/assets/images/rancher-desktop/rancher-desktop.png)

As a user, there are many similarities with Docker Desktop: Rancher Desktop manages a transparent VM with a container runtime and a single-node development Kubernetes cluster.

However, behind the scenes, there's a couple notable differences:
 * By default, Rancher Desktop uses [containerd][] instead of Docker
 * Rancher Desktop uses [k3s][] as the Kubernetes cluster ([k3s][] is a a lightweight, certified Kubernetes distribution also maintained by Rancher)

As a Docker Desktop moving to Rancher Desktop, the quickest way (I did promise you could do this in 5 minutes after all!) is to configure Rancher Desktop to use Docker as the container runtime. 

---
#### ⚠️ Watch Out!
You cannot run both Docker Desktop and Rancher Desktop (in `dockerd` mode) simultaneously!
See [rancher-desktop#1081][rd-issues-1081] for details.

---

Go ahead and open the Rancher Desktop preferences and choose `dockerd (moby)` as the Container Runtime in the "Kubernetes Settings" section:
![Rancher Desktop open to the "Kubernetes Settings" section highlighting Container Runtime section](/assets/images/rancher-desktop/rancher-desktop-runtime.png)

Once selected, Rancher Desktop will prompt you to confirm before resetting the cluster.

After it's started back up...you're done!

Tilt (as of v0.25.1+) will automatically detect your Rancher Desktop with `dockerd` configuration and use it for any [`docker_build`][tiltfile-docker-build] calls.

Similar to using Docker Desktop with its built-in Kubernetes support, no local registry or image pushes are required.
This is possible because Tilt is building _directly_ to the container runtime (`dockerd`) used by the cluster node, so building the image also makes it available for use by Pods.
If this sounds a bit complex - we agree!
Hopefully, you never have to think about it because Tilt takes care of finding the optimal strategy based on your configuration **automatically**.

> ℹ️ If you use `docker` via the CLI, you might notice a bunch of running containers, including Kubernetes cluster components as well as any Pods you have deployed.
> You should avoid manipulating these directly via Docker to avoid conflicting with Rancher Desktop.

[Rancher Desktop][rancher-desktop] is still very new and evolving fast!
We're always excited to see new tools in the local Kubernetes space - if you're using Rancher Desktop with Tilt, [let us know][tilt-contact] ❤️

[containerd]: https://containerd.io/
[k3s]: https://k3s.io/
[rancher-desktop]: https://rancherdesktop.io/
[rd-issues-1081]: https://github.com/rancher-sandbox/rancher-desktop/issues/1081
[tilt-contact]: https://tilt.dev/contact
[tiltfile-custom-build]: https://docs.tilt.dev/api.html#api.custom_build
[tiltfile-docker-build]: https://docs.tilt.dev/api.html#api.docker_build
