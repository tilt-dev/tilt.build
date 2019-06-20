---
slug: local-development-at-kubecon-eu
date: 2019-05-29T19:01:59.467Z
author: nick
layout: blog
canonical_url: "https://medium.com/windmill-engineering/local-development-at-kubecon-eu-c9782146aad2"
title: "Local Development at KubeCon EU"
subtitle: ""
image: featuredImage.jpeg
tags:
  - kubernetes
  - bazel
  - microservices
  - kubecon
keywords:
  - kubernetes
  - bazel
  - microservices
  - kubecon
---

The Tilt engineering team is back from KubeCon in Barcelona. Thanks for everyone who visited our booth to press our button!

![[https://twitter.com/jazzdan/status/1131567233350668288](https://twitter.com/jazzdan/status/1131567233350668288)](/assets/images/local-development-at-kubecon-eu/1*NIX8WIDMr8IUOPVRwHeBbw.jpeg)*[https://twitter.com/jazzdan/status/1131567233350668288](https://twitter.com/jazzdan/status/1131567233350668288)*

We went to KubeCon to learn more about real-world struggles for engineers building services on Kubernetes.

Folks, the struggle is real.

Here’s a quick view of some of the common trends we saw:

### Bazel: A Better Container Builder

Three talks discussed Bazel:

* “[Repeatable Deployments with Kubernetes, Helm & Bazel](https://www.youtube.com/watch?v=T_Oi_CIe164)”
by Rohan Singh

* “[Streamlining Kubernetes Application CI/CD with Bazel](https://www.youtube.com/watch?v=DTvXa-iqrfA)”
by Gregg Donovan & Chris Love

* “[Reproducible Development and Deployment with Bazel and Telepresence](https://www.youtube.com/watch?v=tD0FIlxO1AQ)”
by Christian Roggia

Bazel is a language-agnostic build system based on over a decade of experience with large-scale build tools at Google. We’ve been [tongue-in-cheek critical of Bazel in the past](https://medium.com/windmill-engineering/bazel-is-the-worst-build-system-except-for-all-the-others-b369396a9e26), but it’s a great tool.

Bazel can also create reproducible container images. Unlike Dockerfiles, Bazel ensures that you get fast, iterative builds every time. No need to carefully stack Dockerfile layers like a Jenga tower to maximize caching.

If you’re using Tilt to run your microservices, Tilt has a plugin system to have
Bazel build the images. Head on over to our [Bazel & Tilt guide](https://docs.tilt.dev/integrating_bazel_with_tilt.html) to learn how. Two of the speakers mentioned that they were already using Tilt! 😊

### Connecting Local Dev Across Services

If you’re developing services in Kuberenetes, Tilt isn’t the only game in
town. We stopped by the booths of other teams in this space.

[Telepresence](https://www.telepresence.io/) tries to solve this problem by throwing networking at it. They give you a toolkit of network proxies that let you run a server locally, then connect it to the servers running in your cluster. The tools are flexible with many options, depending on how high fidelity you want the network to be.

[Garden](https://garden.io/) has built a graph-based visualization of the services you’re working
on. You codify which services in that graph update when you change a file. Then, when you make a change, you can watch your changes automatically propagate through the build-run-test graph.

For us, it was exciting to see multiple creative approaches to solving the same
problem.

### Kubernetes Clusters on Your Laptop

For a long time, Minikube was the best way to create a local Kubernetes cluster for testing. But now there are so many more tools with much lower overhead!

The [KIND](https://github.com/kubernetes-sigs/kind) (Kubernetes IN Docker) team gave two talks, one focused on [using KIND to test Kubernetes itself](https://www.youtube.com/watch?v=6m9frvTxK0o), and one focused on [using KIND to test your apps & controllers](https://www.youtube.com/watch?v=8KtmevMFfxA). They’ve put a lot of work into making the startup time fast, so that it’s cheap to throw away a broken cluster and start a new one.

Konstantinos Tsakalozos of the MicroK8s team was at the Ubuntu booth. [MicroK8s](https://microk8s.io/) makes your Linux desktop a single-node Kubernetes cluster. The overhead is so low that it’s been my go-to for local dev.

[Rancher](https://rancher.com/) had a booth too. I haven’t tried out their [k3s / k3d](https://github.com/rancher/k3d) yet. But the idea
of a Kubernetes with non-essential features stripped out for local dev is super
appealing. If you’ve tried it, we’d love to hear what you think of it and how it
compares to the others.

### Post-KubeCon Development

We hope you come away from this post with a better understanding of the problem space, and where the community is making progress. We’re hoping to post some more digested thoughts in the next couple weeks.

If you’re interesting in learning more about how Tilt approaches these problems, we’d love to hear from you.

We hang out in [the #tilt channel](https://kubernetes.slack.com/messages/CESBL84MV/) in Kubernetes slack (get an invite at [slack.k8s.io](https://slack.k8s.io)). We write code in [windmilleng/tilt](https://github.com/windmilleng/tilt).

Maybe we’ll see you at the next KubeCon?
