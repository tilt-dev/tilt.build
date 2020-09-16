---
title: Install
layout: docs
description: "Tilt is available for macOS, Linux, and Windows"
has_calendly: true
has_calendly_popup: true
---

Tilt is available for [macOS](#macos), [Linux](#linux), and [Windows](#windows).

You'll also need:

- Docker, to build containers
- kubectl, to get information about your cluster
- A local Kubernetes cluster (on macOS and Windows, Docker for Desktop works for this!)

macOS
-------

[Docker for Mac](https://docs.docker.com/docker-for-mac/install/) contains Docker, kubectl, and a Kubernetes cluster.

- Install [Docker for Mac](https://docs.docker.com/docker-for-mac/install/)
- In the preferences, click [Enable Kubernetes](https://docs.docker.com/docker-for-mac/#kubernetes)
- Make Docker for Mac your local Kubernetes cluster:

```bash
kubectl config use-context docker-desktop
```

- Install `tilt` with:

```bash
curl -fsSL https://raw.githubusercontent.com/tilt-dev/tilt/master/scripts/install.sh | bash
```

Linux
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

- Install `tilt` with:

```bash
curl -fsSL https://raw.githubusercontent.com/tilt-dev/tilt/master/scripts/install.sh | bash
```

Windows
---------------

[Docker for Windows](https://docs.docker.com/docker-for-windows/install/) contains Docker, kubectl, and a Kubernetes cluster.

- Install [Docker for Windows](https://docs.docker.com/docker-for-windows/install/)
- In the preferences, click [Enable Kubernetes](https://docs.docker.com/docker-for-windows/#kubernetes)
- Make Docker for Windows your local Kubernetes cluster:

```bash
kubectl config use-context docker-desktop
```

- Install `tilt` with:

```bash
iex ((new-object net.webclient).DownloadString('https://raw.githubusercontent.com/tilt-dev/tilt/master/scripts/install.ps1'))
```

If you have [Scoop](https://scoop.sh) installed, the installer will use
that to make Tilt easy to access and upgrade.

Otherwise, you will need to add the `tilt` install directory on your $PATH
(or create an alias) to make it easier to access.

Verify
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

Alternative Installations
-------------------------

We offer 1-step installation scripts that will install the most recent version of Tilt.

- [On macOS/Linux](https://raw.githubusercontent.com/tilt-dev/tilt/master/scripts/install.sh)
- [On Windows](https://raw.githubusercontent.com/tilt-dev/tilt/master/scripts/install.ps1)

The installer first checks if you can install Tilt with a package manager, like
[Homebrew](https://brew.sh/) or [Scoop](https://scoop.sh). 

You can also use these installers directly.

### Homebrew (macOS)

```bash
brew install tilt-dev/tap/tilt
```

### Scoop (Windows)

```bash
scoop bucket add tilt-dev https://github.com/tilt-dev/scoop-bucket
scoop install tilt
```

### Conda Forge

```bash
conda config --add channels conda-forge
conda install tilt
```

## asdf

```
asdf plugin add tilt
asdf install tilt 0.17.5
asdf global tilt 0.17.5
```

### Manual Install

If you don't have a package manager installed, the installer will download a
`tilt` static bianry for you and put it in a reasonable place. (`~/.local/bin`,
`/usr/local/bin`, or `~/bin` depending on your OS and what's already on your
$PATH.

See [Tilt's GitHub Releases page](https://github.com/tilt-dev/tilt/releases) for specific versions.
If you'd prefer to download the binary manually:

On macOS:

```bash
curl -fsSL https://github.com/tilt-dev/tilt/releases/download/v0.17.5/tilt.0.17.5.mac.x86_64.tar.gz | tar -xzv tilt && \
  sudo mv tilt /usr/local/bin/tilt
```

On Linux:

```bash
curl -fsSL https://github.com/tilt-dev/tilt/releases/download/v0.17.5/tilt.0.17.5.linux.x86_64.tar.gz | tar -xzv tilt && \
  sudo mv tilt /usr/local/bin/tilt
```

On Windows:

```powershell
Invoke-WebRequest "https://github.com/tilt-dev/tilt/releases/download/v0.17.5/tilt.0.17.5.windows.x86_64.zip" -OutFile "tilt.zip"
Expand-Archive "tilt.zip" -DestinationPath "tilt"
Move-Item -Force -Path "tilt\tilt.exe" -Destination "$home\bin\tilt.exe"
```

Finally, if you want to install `tilt` from source, see the [developers'
guide](https://github.com/tilt-dev/tilt/blob/master/CONTRIBUTING.md).

Building from source requires both Go and TypeScript/JavaScript tools, and
dynamically compiles the TypeScript on every run. We only recommend this if you
want to make changes to Tilt.
