---
title: Install
layout: docs
---

Tilt is currently available for MacOS and Linux.

You'll also need:

- Docker, to build containers
- Kubectl, to cuddle your cluster
- A local Kubernetes cluster (on MacOS, Docker For Mac works for this!)


Already use Docker Compose for local dev? You can also use Tilt to [run your existing Docker Compose setup](docker_compose.html), in which case all you need to have installed (besides Tilt) is Docker Compose, and you can ignore Kubernetes-specific instructions on this page.

On MacOS
--------

- Install [Docker For Mac](https://docs.docker.com/docker-for-mac/install/)
- In the Docker For Mac preferences, click [Enable Kubernetes](https://docs.docker.com/docker-for-mac/#kubernetes)
- Verify that it works by opening a terminal and running

```bash
kubectl config get-contexts
kubectl config use-context docker-for-desktop
```

### Option A) Installing Tilt with Homebrew (recommended)

```bash
brew tap windmilleng/tap
brew install windmilleng/tap/tilt
```

### Option B) Installing Tilt from release binaries

```bash
curl -L https://github.com/windmilleng/tilt/releases/download/v0.9.6/tilt.0.9.6.mac.x86_64.tar.gz | tar -xzv tilt && \
  sudo mv tilt /usr/local/bin/tilt
```

On Linux
--------

- Install [Docker](https://docs.docker.com/install/)
- Setup Docker as [a non-root user](https://docs.docker.com/install/linux/linux-postinstall/).
- Install [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- Install [Minikube](https://github.com/kubernetes/minikube#installation)
- Start Minikube as

```bash
minikube start
```

- Verify that it works by opening a terminal and running

```bash
kubectl cluster-info
```

- Install the Tilt binary with:

```bash
curl -L https://github.com/windmilleng/tilt/releases/download/v0.9.6/tilt.0.9.6.linux.x86_64.tar.gz | tar -xzv tilt && \
    sudo mv tilt /usr/local/bin/tilt
```

From Source
-----------

If you'd prefer to install `tilt` from source, see the [developers'
guide](https://github.com/windmilleng/tilt/blob/master/DEVELOPING.md).

Building from source requires both Go and TypeScript/JavaScript tools, and
dynamically compiles the TypeScript on every run. We only recommend this if you
want to make changes to Tilt.

Verifying
---------

After you install Tilt, verify that you installed it correctly with:

```bash
tilt version
```

Troubleshooting
---------------

If you have any trouble installing Tilt, look for the error message in the
[Troubleshooting FAQ](faq.html#Troubleshooting).


Next Steps
----------

You're ready to start using Tilt! Try our [Tutorial](tutorial.html) to setup your project in 15 minutes.
