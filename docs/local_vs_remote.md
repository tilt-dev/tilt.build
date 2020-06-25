---
title: Local vs Remote Services
description: "Tilt doesn't care where your services live. Whether they're local or remote, Tilt can live-update them. But we have some suggestions on how to organize them."
layout: docs
---

Modern apps are made of too many services. They're everywhere and in constant
communication.

Tilt doesn't care where your services live. Whether they're local or remote,
Tilt can live-update them.

But you still have to choose how to organize your dev environment.  The possible
setups can be overwhelming.  We're here to help you figure out the right one for
your app.

Solutions:

- [All Local](#all-local)
- [Hybrid](#hybrid)
- [All Remote](#all-remote)

Enhancements:

- [Remote Builds](#remote-builds)
- [Local/Remote Networking](#local-remote-networking)

## All Local

Many teams build and run all services in a local cluster.

### Pros

- A local Kubernetes cluster is easier to setup than ever, 
  see our guide to [Choosing a Cluster](choosing_clusters.html).

- If you mess up, you can reset it.

- Tilt has tooling to help [local processes](local_resource.html) interoperate
  with what's in your local cluster.

## Hybrid

The most common set up we see is a hybrid:

- Remote or hosted services (e.g., databases) that accept inbound requests

- Local pre-built services installed from an existing image or Helm chart

- Local dev services that you're building and iterating on yourself

Pros:

- Offers a lot of flexibility

- Use remote hosted services for things you don't need to reset, or have
  special CPU/data requirements

- [Use local dev clusters](choosing_clusters.html) for things that need to be
  hermetic
  
## All-Remote

Before you go all-remote, ask yourself these questions:

1. Is my app CPU-bound? Can all my dev services run on my laptop? Do any of my
   services have special GPU or hardware requirements?

2. Is my app Data-bound? Can I pull down all the dev data I need to my laptop
   for local development? Are there any security considerations that make
   this impossible?
   
3. Is my app Cluster-bound? Do my dev services need to be colocated with a
   hosted service that's unavailable locally? Is it important that I test on
   different types of clusters?

An all-remote approach might make sense if you answered "yes" to one of these
questions.

And even then, we encourage people to consider a hybrid approach, where the
service with the bottleneck is remote, and the other services are local.

A remote dev cluster takes some operational work to organize and maintain, and
we only recommend it for teams that have a DevOps team to support it.

---

# Enhancements

Once you've gone down the path of remote dev services,
there are some enhancements we often see teams tackle.

## Remote Builds

Instead of building images locally, you can
build images in Kuberentes with [Kaniko](https://github.com/GoogleContainerTools/kaniko)
or [Docker BuildX](https://medium.com/nttlabs/buildx-kubernetes-ad0fe59b0c64).

Tilt's `custom_build` is flexible enough to support this:

```
custom_build(
  'gcr.io/tilt/image-name',
  'docker buildx build --platform=linux/amd64 -t $EXPECTED_REF --push .',
  ['./'],
  skips_local_docker=True,
  disable_push=True,
)
```

But in our experience, teams have a lot of trouble getting it to work well,
including:

- Configuring the build jobs

- Communcation between the build jobs and your cluster image registry

- Caching builds effectively

- Sending only diffs of the build context, instead of re-uploading
  the same files over and over

If you're interested in setting this up, or chatting about potential native
solutions in Tilt to auto-configure this, please reach out to us.

[**Schedule a Meeting**](https://calendly.com/nick-at-tilt/remote-builds)

## Local/Remote Networking

In the Kubernetes community, there's a lot of enthusiasm for software-defined
networking like service meshes and proxies.

Examples:

- The Istio service mesh can route traffic across [multiple
  clusters](https://istio.io/latest/docs/setup/install/multicluster/).

- [Inlets](https://blog.alexellis.io/ingress-for-your-local-kubernetes-cluster/)
  allocates a public load balancer to route traffic to your local
  cluster.

- [Telepresence](https://telepresence.io) replaces your remote service
  with a proxy that routes traffic to your local service.
  
We think these projects are great and complement Tilt well! You can use them to
connect other clusters to the cluster that you're developing on.
