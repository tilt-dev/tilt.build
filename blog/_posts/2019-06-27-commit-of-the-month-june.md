---
slug: june-tilt-commit-of-the-month
date: 2019-07-03T15:26:34.743Z
author: dmiller
layout: blog
title: "Tilt Commit of the Month: June 2019"
subtitle: "Support More Kubernetes Clusters"
image: featuredImage.jpg
image_needs_slug: true
image_type: "contain"
tags:
  - docker
  - kubernetes
  - microservices
  - tilt
  - cotm
keywords:
  - docker
  - kubernetes
  - microservices
  - tilt
---

Welcome to a new series of blog posts we're calling Tilt Commit of the Month. Commit of the Month is a lightweight way to highlight work that goes on in the Tilt project that might fly under the radar otherwise.

We’re already cheating: this month we’re going to highlight a multiple commits, instead of just one. All of these commits are related to detecting and working better with different kinds of Kubernetes clusters.

Commits:
* [k8s: auto-detect microk8s registry](https://github.com/windmilleng/tilt/commit/d293a0ba0216711c855526100490e21733ada194)
* [docker: dynamically switch between local docker daemon and the in-cluster daemon](https://github.com/windmilleng/tilt/commit/af5a0a7e0c32c8b55117c9f22c28008f8af67d2d)
* [engine: fix exec syncing on busybox](https://github.com/windmilleng/tilt/commit/6678de099fd559b8e02240a3a807d3b06e65aff8)


## What they do
Combined, these changes improve Tilt support for [KIND](https://github.com/kubernetes-sigs/kind), [microk8s](https://microk8s.io/), and [minikube](https://kubernetes.io/docs/setup/learning-environment/minikube/). On microk8s we now detect whether we should use a registry built in microk8s, or an external one. Finally [`live_update`](https://docs.tilt.dev/live_update_reference.html) on KIND clusters no longer results in full rebuilds.

## Why they're important
Aside from making Tilt work better on various Kubernetes clusters, these change also pave the way for us to run our integration tests across many different types of Kubernetes clusters, rather than just one. With this we'll be better able to catch edge-cases that affect only certain clusters. Hooray for test coverage!
