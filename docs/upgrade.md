---
title: Upgrade
layout: docs
---

You can find a list of Tilt releases on [Tilt's GitHub Releases page](https://github.com/windmilleng/tilt/releases). 

Based on how you previously [installed Tilt](install.html), upgrade to the latest version with one of these commands. 

macOS
-----

### If you installed with the install script or directly with a release binary

```bash
curl -L https://github.com/windmilleng/tilt/releases/download/v0.12.10/tilt.0.12.10.mac.x86_64.tar.gz | tar -xzv tilt && \
  sudo mv tilt /usr/local/bin/tilt
```

### If you installed via Homebrew

```
$ brew update && brew upgrade windmilleng/tap/tilt
$ brew install windmilleng/tap/tilt
```

Linux
-----

```bash
curl -L https://github.com/windmilleng/tilt/releases/download/v0.12.10/tilt.0.12.10.linux.x86_64.tar.gz | tar -xzv tilt && \
    sudo mv tilt /usr/local/bin/tilt
```

Verify
------

Verify you have upgraded to the [latest version](https://github.com/windmilleng/tilt/releases) with:

```bash
tilt version
```
