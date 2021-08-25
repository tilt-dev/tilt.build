---
title: Preparation (Optional)
subtitle: Tilt Tutorial
layout: docs
---
For this tutorial, we've designed a sample project that uses Docker for building container images and Kubernetes for running them.
This section will walk you through installing Tilt and Docker, provisioning a local Kubernetes cluster, and cloning the sample project.

In practice, Tilt is incredibly flexible and supports a variety of ways to build and deploy your services during local development.
It's possible to use Tilt without Kubernetes and Docker!

> 💁‍♀️ The [What's Next?][tutorial-references] section includes resources for using Tilt with Helm, podman, local processes, and more

This tutorial is focused on the Tilt fundamentals: we won't actually dive into a `Dockerfile` or Kubernetes YAML.
(We have chosen them due to their prevalence and to ensure a consistent experience.)

Regardless, if you'd prefer to not download additional tools, you can still follow along on the web - go ahead and skip to the [next section][tutorial-tilt-up]!

## Install Tilt
On macOS/Linux, we've got an install script that will use [Homebrew][brew] if available (and a direct download otherwise):
```bash
curl -fsSL https://raw.githubusercontent.com/tilt-dev/tilt/master/scripts/install.sh | bash
```

On Windows, we've got an install script that will use [Scoop][scoop] if available (and a direct download otherwise):
```powershell
iex ((new-object net.webclient).DownloadString('https://raw.githubusercontent.com/tilt-dev/tilt/master/scripts/install.ps1'))
```

If you'd rather install manually or with an alternative method, refer to the [Alternative Installations][install-tilt-alternate] guide.

## Install Docker
Docker provides comprehensive [install instructions][install-docker] for all supported OSes and Linux distributions:
 * [Docker Desktop for Mac][install-docker-mac]
 * [Desktop Desktop for Windows][install-docker-windows] (including WSL)
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

A quick way to test our your Docker install is to run the `hello-world` container:
```bash
docker run --rm hello-world
```
You should see some output from Docker as it downloads the `hello-world` image followed by a greeting message with some information about Docker.
If you are having trouble, Docker provides troubleshooting guides for [macOS][troubleshoot-docker-mac] and [Windows][troubleshoot-docker-windows].

## Provision a Local Kubernetes Cluster
There are many different options for local development Kubernetes clusters such as KIND, k3d, and Docker Desktop.
If you're curious about the different options, refer to the [Choosing A Local Cluster][guide-local-cluster] guide.

Regardless of your choice, Tilt will detect the optimal configuration to ensure your image builds and deployments are as fast as possible.
While Tilt also supports using a remote cluster for development, we recommend using a local cluster for this tutorial.

### Docker Desktop
If you're using Docker for Mac or Docker for Windows, you can enable the built-in [Kubernetes Support][docker-kubernetes]:
 1. Opening Docker Desktop preferences
 2. Navigate to the "Kubernetes" section
 3. Check the "Enable Kubernetes" option
 4. Click "Apply & Restart"
 5. Click "Install" on the confirmation dialog

It can take several minutes to start up the first time.
You can run the following command after clicking "Install" to let you know when it's ready:
```bash
kubectl wait --for=condition=Ready --all node
```
You should see `node/docker-desktop condition met` and the command will return if it's ready.
(If you get an error such as `Unable to connect to the server: EOF`, re-run the command.)

### k3d
[k3d][] is an easy way to create single-node [k3s][] (a lightweight Kubernetes distribution) clusters in Docker.
This is fast, does not require the download of additional tools, and is easy to delete when you're done.

Run the following command to provision a cluster named `k3d-tilt`:
```bash
docker run --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v "${HOME}/.kube:/.kube" \
  rancher/k3d:v4.4.7 \
  cluster create tilt --registry-create --kubeconfig-switch-context --kubeconfig-update-default --no-hostip
```

> **🤔 What is this doing?**
>
> `docker run` creates an ephemeral container to run the [k3d][] provisioner.
>
> The Docker socket (`/var/run/docker.sock`) is attached as a volume so that k3d can create the cluster containers.
>
> The Kubernetes config directory (`~/.kube`) is attached as a volume so that k3d can populate it with the cluster connection.

When you're done with the tutorial, you can delete the `k3d-tilt` cluster:
```bash
docker run --rm \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v "${HOME}/.kube:/.kube" \
  rancher/k3d:v4.4.7 \
  cluster delete tilt
```

## Clone the Sample Project
You can clone the repo from the command line:
```bash
git clone https://github.com/tilt-dev/tilt-avatars.git
```
If you prefer to use GitHub Desktop or another method, that works too!

Throughout the rest of the tutorial, unless otherwise specified, all commands can be run from the root of the repository (i.e. the `tilt-avatars` directory). 

For now, cloning the project is sufficient.
In the next step, we'll launch it (with Tilt, of course!)

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
[tutorial-references]: ./references.html
[tutorial-tilt-up]: ./2-tilt-up.html
