---
slug: september-commit-of-the-month
date: 2019-10-14
author: dmiller
layout: blog
title: "September Commit of the Month"
image: featuredImage.jpg
tags:
  - kubernetes
  - developer-tools
  - tilt
  - cotm
keywords:
  - kubernetes
  - developer-tools
---

September’s Commit of the Month is [089d99118f3c6123592994e476be200e5eb00f30](https://github.com/windmilleng/tilt/commit/089d99118f3c6123592994e476be200e5eb00f30).

Prior to this commit Tilt would create a run ID each time it started and use that to associate resources with that invocation of Tilt so we know which pods to watch.

This meant that would create new YAML with a different run ID each time it started. This resulted in Kubernetes tearing down the old pod and re-creating it, even though the only thing that changed was one label.

This commit, building on several before it, removed Tilt’s run IDs and instead uses owner UID’s to track which resources belong to Tilt. Now if a resource hasn’t changed between Tilt runs we don’t have to do any work. Thanks [Nick](https://twitter.com/nicksantos)!
