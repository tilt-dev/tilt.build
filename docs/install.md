---
title: Install
layout: docs
---

Tilt is currently available for MacOS and Linux.

You'll also need:

- Docker, to build containers
- Kubectl, to get information about your cluster
- A local Kubernetes cluster (on MacOS, Docker For Mac works for this!)

On MacOS
--------

- Install [Docker For Mac](https://docs.docker.com/docker-for-mac/install/)
- In the Docker For Mac preferences, click [Enable Kubernetes](https://docs.docker.com/docker-for-mac/#kubernetes)
- Make Docker For Mac your local Kubernetes cluster:

```bash
kubectl config use-context docker-desktop
```

Installing the `tilt` binary is a one-step command:

```bash
curl -fsSL https://raw.githubusercontent.com/windmilleng/tilt/master/scripts/install.sh | bash
```

On Linux
--------

- Install [Docker](https://docs.docker.com/install/)
- Setup Docker as [a non-root user](https://docs.docker.com/install/linux/linux-postinstall/).
- Install [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- Install [Microk8s](https://microk8s.io/):

```bash
sudo snap install microk8s --classic && \
sudo microk8s.enable dns && \
sudo microk8s.enable registry
```

- Make microk8s your local Kubernetes cluster:

```bash
sudo microk8s.kubectl config view --flatten > ~/.kube/microk8s-config && \
KUBECONFIG=~/.kube/microk8s-config:~/.kube/config kubectl config view --flatten > ~/.kube/temp-config && \
mv ~/.kube/temp-config ~/.kube/config && \
kubectl config use-context microk8s
```

Installing the `tilt` binary is a one-step command:

```bash
curl -fsSL https://raw.githubusercontent.com/windmilleng/tilt/master/scripts/install.sh | bash
```

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

---

Alternative Installation
------------------------

The [1-step installation script](https://github.com/windmilleng/tilt/blob/master/scripts/install.sh)
will install the most recent version of Tilt.

The installer first checks if you can install Tilt with Homebrew. If you'd prefer
to run Homebrew manually, run:

```bash
brew tap windmilleng/tap
brew install windmilleng/tap/tilt
```

Otherwise, the installer downloads a static `tilt` binary and puts it under `/usr/local/bin`.
See [Tilt's GitHub Releases page](https://github.com/windmilleng/tilt/releases) for specific versions.
If you'd prefer to download the binary manually:

On MacOS:

```bash
curl -fsSL https://github.com/windmilleng/tilt/releases/download/v0.10.9/tilt.0.10.9.mac.x86_64.tar.gz | tar -xzv tilt && \
  sudo mv tilt /usr/local/bin/tilt
```

On Linux:

```bash
curl -fsSL https://github.com/windmilleng/tilt/releases/download/v0.10.9/tilt.0.10.9.linux.x86_64.tar.gz | tar -xzv tilt && \
  sudo mv tilt /usr/local/bin/tilt
```

Finally, if you want to install `tilt` from source, see the [developers'
guide](https://github.com/windmilleng/tilt/blob/master/DEVELOPING.md).

Building from source requires both Go and TypeScript/JavaScript tools, and
dynamically compiles the TypeScript on every run. We only recommend this if you
want to make changes to Tilt.
