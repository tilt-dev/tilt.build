---
title: Working with Multiple Clusters
layout: docs
---

Tilt can talk to any Kubernetes cluster. This doc describes idioms that can make Tilt work better when you frequently connect to multiple clusters.

## One Context
Tilt uses the cluster specified by your [context](https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/). Tilt reads this value once at startup and continues to talk to the same cluster. If you change the value outside Tilt, Tilt will remain connected to the cluster that it started with.

The context that Tilt selected at startup is exposed via the Tiltfile function `k8s_context`.

## Don't Touch Prod
You don't want Tilt to start updating the production cluster just because you forgot to switch contexts. This Tiltfile snippet prevents talking to Prod by checking the current context is a known dev cluster:

```python
dev_clusters = ['docker-for-desktop', 'minikube']
if k8s_context not in dev_clusters:
  fail('unknown context %s; failing early to avoid Tilt talking to a production cluster' % k8s_context())
```

## Use a Local Registry for Microk8s
[Microk8s](https://github.com/ubuntu/microk8s) is a local Kubernetes cluster for Linux. Its registry extension can serve an image registry at `localhost:32000`, which saves the overhead of having to push an image to a remote registry.

You can tell Tilt to use this registry only when you're connected to microk8s:
```python
registry = 'gcr.io/company'
if k8s_context() == 'microk8s':
  registry = 'localhost:32000'
default_registry(registry)
```
