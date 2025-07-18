---
title: Install
layout: docs
description: "Tilt is available for macOS, Linux, and Windows"
sidebar: gettingstarted
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
- In the preferences, click [Enable Kubernetes](https://docs.docker.com/desktop/kubernetes/)
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
- Install [ctlptl](https://github.com/tilt-dev/ctlptl) and use it to create Kind with a local registry
- Install `tilt` with:
```bash
curl -fsSL https://raw.githubusercontent.com/tilt-dev/tilt/master/scripts/install.sh | bash
```

Alternatively, Ubuntu users sometimes prefer
[Microk8s](choosing_clusters.html#microk8s) instead of Kind because it
integrates well with Ubuntu. See the [Choosing a Local Dev Cluster](choosing_clusters.html)
guide for more Linux options.

Windows
---------------

[Docker for Windows](https://docs.docker.com/docker-for-windows/install/) contains Docker, kubectl, and a Kubernetes cluster.

- Install [Docker for Windows](https://docs.docker.com/docker-for-windows/install/)
- In the preferences, click [Enable Kubernetes](https://docs.docker.com/docker-for-windows/#kubernetes)
- Make Docker for Windows your local Kubernetes cluster:
```powershell
kubectl config use-context docker-desktop
```
- Install `tilt` with Powershell:
```powershell
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

You're ready to start using Tilt!
Try our [Tutorial](/tutorial) to learn about Tilt or jump right in with the [Write a Tiltfile Guide](tiltfile_authoring.html).

---

Alternative Installations
-------------------------

We offer 1-step installation scripts that will install the most recent version of Tilt.

- [On macOS/Linux](https://raw.githubusercontent.com/tilt-dev/tilt/master/scripts/install.sh)
- [On Windows](https://raw.githubusercontent.com/tilt-dev/tilt/master/scripts/install.ps1)

The installer first checks if you can install Tilt with a package manager, like
[Homebrew](https://brew.sh/) or [Scoop](https://scoop.sh). 

You can also use these installers directly.

### Homebrew (macOS or Linux)

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

```bash
asdf plugin add tilt
asdf install tilt 0.35.0
asdf global tilt 0.35.0
```

### Manual Install

If you don't have a package manager installed, the installer will download a
`tilt` static binary for you and put it in a reasonable place. (`~/.local/bin`,
`/usr/local/bin`, or `~/bin` depending on your OS and what's already on your
$PATH.

See [Tilt's GitHub Releases page](https://github.com/tilt-dev/tilt/releases) for specific versions.
If you'd prefer to download the binary manually:

On macOS:

```bash
curl -fsSL https://github.com/tilt-dev/tilt/releases/download/v0.35.0/tilt.0.35.0.mac.x86_64.tar.gz | tar -xzv tilt && \
  sudo mv tilt /usr/local/bin/tilt
```

On Linux:

```bash
curl -fsSL https://github.com/tilt-dev/tilt/releases/download/v0.35.0/tilt.0.35.0.linux.x86_64.tar.gz | tar -xzv tilt && \
  sudo mv tilt /usr/local/bin/tilt
```

On Windows:

```powershell
Invoke-WebRequest "https://github.com/tilt-dev/tilt/releases/download/v0.35.0/tilt.0.35.0.windows.x86_64.zip" -OutFile "tilt.zip"
Expand-Archive "tilt.zip" -DestinationPath "tilt"
Move-Item -Force -Path "tilt\tilt.exe" -Destination "$home\bin\tilt.exe"
```

Finally, if you want to install `tilt` from source, see the [developers'
guide](https://github.com/tilt-dev/tilt/blob/master/CONTRIBUTING.md).

Building from source requires both Go and TypeScript/JavaScript tools, and
dynamically compiles the TypeScript on every run. We only recommend this if you
want to make changes to Tilt.
