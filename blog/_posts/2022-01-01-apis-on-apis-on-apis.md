---
slug: "apis-on-apis-on-apis"
date: 2022-01-01
author: siegs
layout: blog
title: "APIs on APIs"
subtitle: "Why APIs modeled after Kubernetes are so powerful"
description: "We explore what makes the Kubernetes approach to APIs so useful."
image: "/assets/images/apis-on-apis-on-apis/turtles.jpg"
tags:
  - kubernetes
  - api
  - api-server
---
An underrated aspect of Kubernetes is how open and extensible the system is. Every facet of a Kubernetes cluster can be browsed, inspected and modified via a standard [REST API][K8SREST]. [Custom resources][CustomResources] can be defined in the API to hold data specific to each production system. [Operators][] can be added to act on the API data to perform new functionality that goes beyond what the Kubernetes developers originally intended.

[K8SREST]: https://kubernetes.io/docs/concepts/overview/kubernetes-api/
[CustomResources]: https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/
[Operators]: https://kubernetes.io/docs/concepts/extend-kubernetes/operator/
