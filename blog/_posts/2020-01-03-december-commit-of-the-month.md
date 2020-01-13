---
slug: december-commit-of-the-month
date: 2020-01-02
author: dmiller
layout: blog
title: "Tilt Commit of the Month: December 2019"
subtitle: "Tilt now supports Helm 3"
image: /assets/images/december-commit-of-the-month/helm-logo.svg
image_type: "contain"
tags:
  - tilt
  - cotm
keywords:
  - tilt
  - helm
---

December's commit of the month is [db6695](https://github.com/windmilleng/tilt/commit/db669506c9d040a8ffa608dd152c75fed2646ac8)!

With this commit, Tilt's [`helm()` built-in](https://docs.tilt.dev/api.html#api.helm) now natively supports [Helm 3](https://helm.sh/blog/helm-3-released/). While there were some CLI API changes in Helm 3 (e.g. [name is now a required parameter](https://helm.sh/docs/faq/#name-or-generate-name-is-now-required-on-install) for `helm template`), if you're using the `helm()` built-in with Tilt, you can upgrade to Helm 3 without changing your Tiltfile. Tilt automatically detects if you're using Helm 2 or Helm 3 and invokes it appropriately.

Happy Tilting, and Happy New Year!
