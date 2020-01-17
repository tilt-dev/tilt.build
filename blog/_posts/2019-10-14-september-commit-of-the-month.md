---
slug: september-commit-of-the-month
date: 2019-10-14
author: dmiller
layout: blog
title: "September Commit of the Month"
image: featuredImage.jpg
image_needs_slug: true
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

Prior to this commit, Tilt would create a run ID each time it started and use that to associate k8s resources with that invocation of Tilt so we knew which pods to watch (and didn't pull in logs from old pods, etc.).

This meant that each `tilt up` would create new YAML with a different run ID. This resulted in Kubernetes tearing down the old pod and re-creating it, even though the only thing that changed was one label.

This commit, building on several before it, removed Tilt’s run IDs and instead uses k8s object owner UID’s to track which resources belong to Tilt. (E.g., we know that deployment X belongs to Tilt; if pod Z belongs to replicaset Y which belongs to deployment X, we know that pod _also_ belongs to Tilt.) Now if a resource hasn’t changed between Tilt runs, we don’t have to do any work.

Thanks [Nick](https://twitter.com/nicksantos)!
