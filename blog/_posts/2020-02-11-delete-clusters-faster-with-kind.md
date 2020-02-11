---
slug: delete-clusters-faster-with-kind
date: 2020-02-11
author: nick
layout: blog
title: "Delete Your Kubernetes Clusters Faster with Kind"
subtitle: "Announcing a Big Improvement in Local Development"
image: "/assets/images/delete-clusters-faster-with-kind/priscilla-du-preez-acNPOikiDRw-unsplash.jpg"
image_caption: "Photo by <a href='https://unsplash.com/@priscilladupreez?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText'>Priscilla Du Preez</a> on <a href='https://unsplash.com/s/photos/local?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText'>Unsplash</a>"
tags:
  - tilt
keywords:
  - tilt
  - kind
  - local development
---

A few weeks ago, we at Tilt asked the [Cluster API](https://github.com/kubernetes-sigs/cluster-api) 
team how to make their development experience even better.

They said some nice things about Tilt. But they really wanted to rave about
[Kind](https://kind.sigs.k8s.io/). One contributor told us: "Tilt
is good, and I'll let you finish, but Kind is one of the best Kubernetes dev
tools of all time!" (Lightly paraphrasing.)

That made a lot of sense! Because Cluster API is a project to help you spin up
new Kubernetes clusters with a Kubernetes-style API, Kind's ability to quickly
create and delete dev clusters is *huge*.

That's why we're excited to announce some big changes to make Kind + Tilt faster
than ever. Just use this setup script to create a cluster:

[kind-with-registry.sh](https://github.com/windmilleng/kind-local)

The script may look simple. But a lot of work from a lot of different people in
the Kubernetes community went into making this possible.

Let's talk about what this script does and why it's such an important change.

## What is Kind?

The Kubernetes team needed a better way to test Kubernetes itself. That meant: 

- Fast startup time, faster teardown time

- Works in continuous integration for testing apps

- Can run multiple versions of Kubernetes, even one you built yourself

Kind is the solution. It's an acronym for Kubernetes IN Docker. It runs a
Kubernetes cluster in a Docker container, so that you don't need an additional
VM.

The first time I heard about Kind reminds me of the first time I heard about the
Go language. Someone explained Go to me as a bunch of engineers at Google in a
silo, trying to redesign C++ to optimize for fast compile times. I remember
thinking at the time: of all the things you can optimize in a language, why fast
compile times?

They were so right. Fast compile times absolutely changes how you use Go. You
start using it for entirely new use-cases. 

I feel the same way about Kind. It may have been built for testing
Kubernetes. Its approach means that it also makes a great solution for local
app development.

## What's New?

To make Kind your multi-service development environment, you need to:

1) Start the cluster

2) Install your base services

3) Update them quickly with your changes

Kind already made #1 fast. Tilt tries to make #3 fast with tools like
[live_update](https://docs.tilt.dev/live_update_tutorial.html). The missing
piece was #2.

There are a couple ways you can initialize a cluster. 

You can push images to a remote image registry, and pull them down again. But
images are big, and that eats up your network. You need to share secrets so that
both your local computer and your cluster can talk to the registry.

You can pack your images into a tarball, and copy them into the cluster
directly. But monolithic tarballs are hard to cache effectively.

Then the community had a key insight: what if you had a local registry? They
cache layer by layer, but don't eat up the network. The hard part is wiring
everything together. You need:

- A container runtime config that allows you to use a local image registry

- A Kind API that lets you patch the container runtime config.

- A way to start a registry that's reachable from both local and the cluster

- A way to tell other tooling about this registry

The [setup script](https://github.com/windmilleng/kind-local) puts these APIs
together. The containerd and Kind teams did most of the work! We're just tying
a bow on it. Now you've got a way to cold-start services in the cluster quickly
and start hacking.

## Is Kind Right for Me?

If you're currently doing multi-service development in Docker for Mac, 
and having performance or stability issues, try out Kind!
Don't be afraid to delete clusters and create new ones. 
Cleaning up from time to time makes things more stable.

If you're on Linux, also look into [Microk8s](https://microk8s.io/). It's
integrates well with your OS so that you always have a dev cluster available with no
VM at all.

We also plan to write up a similar setup script for
[K3D](https://github.com/rancher/k3d) using the same approach described here. If
you're interested in K3D, [come talk to
us](https://github.com/windmilleng/tilt#community--contributions)!

## Further Reading

- [Choosing a Local Dev Cluster](https://docs.tilt.dev/choosing_clusters.html), 
  which has more details on the pros and cons of different clusters
- [The Kind Homepage](https://kind.sigs.k8s.io/)
- Thanks to [the ClusterAPI project](https://github.com/kubernetes-sigs/cluster-api) for sharing [their Tilt setup](https://cluster-api.sigs.k8s.io/developer/tilt.html)
