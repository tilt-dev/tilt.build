---
title: Upgrading
layout: docs
---

You can find a list of Tilt releases on [Tilt's GitHub Releases page](https://github.com/windmilleng/tilt/releases).

On MacOS
--------

### Option A) If you installed Tilt via Homebrew

```
$ brew update && brew upgrade windmilleng/tap/tilt
$ brew install windmilleng/tap/tilt
```

### Option B) Installing Tilt from release binaries

```bash
curl -L https://github.com/windmilleng/tilt/releases/download/v0.12.1/tilt.0.12.1.mac.x86_64.tar.gz | tar -xzv tilt && \
  sudo mv tilt /usr/local/bin/tilt
```

On Linux
--------

```bash
curl -L https://github.com/windmilleng/tilt/releases/download/v0.12.1/tilt.0.12.1.linux.x86_64.tar.gz | tar -xzv tilt && \
    sudo mv tilt /usr/local/bin/tilt
```

Verifying
---------

After you install Tilt, verify that you installed it correctly with:

```bash
tilt version
```
