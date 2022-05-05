---
slug: "tilt-ui-cluster-status"
date: 2022-05-05
author: milas
layout: blog
title: "O Kubernetes Cluster, Where Art Thou?"
image: "/assets/images/cluster-status/title.jpg"
image_caption: 'Photo by <a rel="noopener noreferrer" href="https://unsplash.com/photos/0W4XLGITrHg">
Michael Dziedzic</a> on Unsplash'
description: "The answer to your Kubernetes cluster problems isn’t in Shakespeare – it’s in the Tilt UI!"
tags:
- kubernetes
---

Multiservice development often means jumping between multiple consoles, terminals, and browser tabs to debug an issue.
Frequently, the location of the error message is not even the same as the location of the root cause!

One of Tilt’s superpowers is aggregating and centralizing your project’s logs and status into a single place, which can dramatically simplify cross-service debugging.
However, the world extends beyond our own code, and infrastructure errors can be some of the most inscrutable to debug.

Recently, we’ve made changes to Tilt’s internals to improve the Kubernetes cluster connection experience:

* `k8s_resource`s will pause deployment if the cluster connection is not healthy
* Kubernetes cluster connection status is shown in the Tilt navbar
* Kubernetes cluster connection details are available in the Tilt web UI and Tilt API

![Tilt UI updating cluster status in navbar when cluster has an error](/assets/images/cluster-status/fail.gif)

After Tilt establishes a connection to your Kubernetes cluster, that connection will be monitored by polling the Kubernetes API readiness endpoints to ensure that the cluster is accessible, live, and ready.

Imagine you leave the office and board a train but forget to connect to VPN – you will be able to see that the cluster connection is temporarily unavailable directly from the Tilt UI, and updates to Kubernetes resources will be queued but not executed.

![Resource in Tilt UI showing the "Waiting for cluster" status](/assets/images/cluster-status/resource-waiting.png)

Sometimes you need a deeper understanding of what’s going on between Tilt and your Kubernetes cluster.
For example, manually setting up a local Kubernetes cluster with its own registry can be a tricky process[^1].
The new Kubernetes cluster status pop-up in the Tilt UI means you can quickly see how Tilt inferred the local registry without triggering a bunch of unnecessary builds and scrutinizing the logs.

![Kubernetes cluster metadata popup in Tilt UI](/assets/images/cluster-status/popup.png)

To take advantage of the new Kubernetes cluster status features, make sure you’re on the [latest version of Tilt][tilt-install], and you’ll see a new icon in the navbar (three stacked hexagons ​​⬡), which you can click for details.

That’s it! We know your time and attention are invaluable, so these improvements are designed to seamlessly integrate into your existing workflows without adding another new interruption 🤗

[^1]: Unless you’re using [ctlptl][]!
[ctlptl]: https://github.com/tilt-dev/ctlptl#kind-with-a-built-in-registry-at-a-pre-determined-port
[tilt-install]: https://docs.tilt.dev/install.html
