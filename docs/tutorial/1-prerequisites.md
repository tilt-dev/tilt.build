---
title: Preparation (Optional)
subtitle: Tilt Tutorial
layout: docs
sidebar: gettingstarted
---

For this tutorial, we'll focus on Tilt fundamentals by walking through a sample project.

Our sample project uses Docker for building container images and Kubernetes for running them.
However, it's possible to use Tilt without Docker or Kubernetes!
Tilt is incredibly flexible and supports a variety of ways to build and run your services during local development.

We won't actually dive into a Dockerfile or Kubernetes YAML, since that's out of scope for this introduction.

To follow along interactively, you'll need to have Docker and Tilt installed on your machine.

Prefer not to download additional tools?
You can still follow along on the web - go ahead and skip to the [next section][tutorial-tilt-up]!

> 💁‍♀️ **Not using Kubernetes or Docker?**
> 
> We've got plenty of guides for using Tilt with Helm, podman, local processes, and more to help you get started after learning the Tilt fundamentals from this tutorial.

## Install Tilt
On macOS/Linux, we've got an install script that will use [Homebrew][brew] if available (and a direct download otherwise):
```bash
curl -fsSL https://raw.githubusercontent.com/tilt-dev/tilt/master/scripts/install.sh | bash
```

On Windows, we've got an install script that will use [Scoop][scoop] if available (and a direct download otherwise):
```powershell
iex ((new-object net.webclient).DownloadString('https://raw.githubusercontent.com/tilt-dev/tilt/master/scripts/install.ps1'))
```

If you'd rather install manually or via another method, refer to the guide on [Alternative Installations][install-tilt-alternate].

## Install Docker
Docker provides comprehensive [install instructions][install-docker] for all supported OSes and Linux distributions:
 * [Docker Desktop for Mac][install-docker-mac]
 * [Docker Desktop for Windows][install-docker-windows] (including WSL)
 * Docker for Linux
   * [Ubuntu][install-docker-linux-ubuntu]
   * [Direct from binary][install-docker-linux-manual]
   * [All other distributions][install-docker-linux]
   * Convenience script (auto-detects distribution):
     ```bash
     curl -fsSL https://get.docker.com | sh
     ```

> 💡 On Linux, following the [Manage Docker as a non-root user][docker-non-root] post-install guide is suggested so that you don't have to run Tilt with `sudo`.
> (Please take careful note of the security considerations outlined in the guide.)

A quick way to test out your Docker install is to run the `hello-world` container:
```bash
docker run --rm hello-world
```
You should see some output from Docker as it downloads the `hello-world` image followed by a greeting message with some information about Docker.
If you are having trouble, Docker provides troubleshooting guides for [macOS][troubleshoot-docker-mac] and [Windows][troubleshoot-docker-windows].

[brew]: https://brew.sh
[docker-kubernetes]: https://docs.docker.com/desktop/kubernetes/#enable-kubernetes
[docker-non-root]: https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user
[guide-local-cluster]: /choosing_clusters.html
[k3d]: https://k3d.io
[k3s]: https://k3s.io
[install-docker]: https://docs.docker.com/get-docker/
[install-docker-linux]: https://docs.docker.com/engine/install/#server
[install-docker-linux-manual]: https://docs.docker.com/engine/install/binaries/
[install-docker-linux-ubuntu]: https://docs.docker.com/engine/install/ubuntu/
[install-docker-mac]: https://docs.docker.com/desktop/mac/install/
[install-docker-windows]: https://docs.docker.com/desktop/windows/install/
[install-tilt-alternate]: /install.html#alternative-installations
[scoop]: https://scoop.sh/
[troubleshoot-docker-mac]: https://docs.docker.com/desktop/mac/troubleshoot/
[troubleshoot-docker-windows]: https://docs.docker.com/desktop/windows/troubleshoot/
[tutorial-tilt-up]: ./2-tilt-up.html
