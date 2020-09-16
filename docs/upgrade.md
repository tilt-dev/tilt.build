---
title: Upgrade
description: "Based on how you previously installed Tilt, upgrade to the latest version with one of these commands."
layout: docs
---

You can find a list of Tilt releases on [Tilt's GitHub Releases page](https://github.com/tilt-dev/tilt/releases). 

Usually it is sufficint to rerun the install script. However, if you installed Tilt using one of the [alternative installation methods](install.html) you may need to use one of the [other upgrade methods](upgrade.html#other-upgrade-methods) listed below.

macOS or Linux
-----

Rerun the install script:

```bash
curl -fsSL https://raw.githubusercontent.com/tilt-dev/tilt/master/scripts/install.sh | bash
```

Windows
-----

```powershell
iex ((new-object net.webclient).DownloadString('https://raw.githubusercontent.com/tilt-dev/tilt/master/scripts/install.ps1'))
```

Other Upgrade Methods
---------------------


## Homebrew

```
$ brew update && brew upgrade tilt-dev/tap/tilt
$ brew install tilt-dev/tap/tilt
```

## Scoop

```
scoop update tilt
```

## Conda

```
conda update -c conda-forge tilt
```

## asdf

```
asdf plugin add tilt
asdf install tilt 0.17.3
asdf global tilt 0.17.3
```

## Manual Install
If you installed Tilt manually by downloading a release binary and moving in to your PATH you may need to do the same to upgrade.

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
