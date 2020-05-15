---
title: Upgrade
layout: docs
---

You can find a list of Tilt releases on [Tilt's GitHub Releases page](https://github.com/tilt-dev/tilt/releases). 

Based on how you previously [installed Tilt](install.html), upgrade to the latest version with one of these commands. 

macOS
-----

### If you installed with the install script or directly with a release binary

```bash
curl -L https://github.com/tilt-dev/tilt/releases/download/v0.13.6/tilt.0.13.6.mac.x86_64.tar.gz | tar -xzv tilt && \
  sudo mv tilt /usr/local/bin/tilt
```

### If you installed via Homebrew

```
$ brew update && brew upgrade tilt-dev/tap/tilt
$ brew install tilt-dev/tap/tilt
```

Linux
-----

```bash
curl -L https://github.com/tilt-dev/tilt/releases/download/v0.13.6/tilt.0.13.6.linux.x86_64.tar.gz | tar -xzv tilt && \
    sudo mv tilt /usr/local/bin/tilt
```

Windows
-----

```powershell
Invoke-WebRequest "https://github.com/tilt-dev/tilt/releases/download/v0.13.6/tilt.0.13.6.windows.x86_64.zip" -OutFile "tilt.zip"
Expand-Archive "tilt.zip" -DestinationPath "tilt"
Move-Item -Force -Path "tilt\tilt.exe" -Destination "$home\bin\tilt.exe"
```

Verify
------

Verify you have upgraded to the [latest version](https://github.com/tilt-dev/tilt/releases) with:

```bash
tilt version
```
