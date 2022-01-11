---
slug: clearstreet-casestudy
date: 2020-01-15
author: lian
layout: casestudy
title: "Taking Your Local Dev Environment From Zero to Hero"
subtitle: "Why Clear Street Moved to Local Kubernetes Development With Tilt"
tags:
  - case-study
  - kubernetes
keywords:
  - case-study
  - kubernetes
---
According to a [recent survey](https://www.datadoghq.com/container-report-2020/#1) by Datadog, Kubernetes has, in fact, become the industry standard for orchestrating containers, with over half of organizations running Kubernetes in their environments.


While this has made maintaining, observing and deploying to shared environments like staging or production easier, the burden on developers to integrate their dev environments has grown.  
Tilt aims to close the technical gap between development and post-commit environments, by providing a seamless developer experience that just works.


Read on to find out how Clear Street, a digital trading company, has improved their time to launch. After integrating Tilt into their development workflow, they are iterating on the inner loop two to four times faster!


_This case study was originally published on [Medium by Ottavio Hartman](https://medium.com/clear-street/why-we-moved-to-local-kubernetes-development-at-clear-street-523045dd2ac8)_

---

At Clear Street, we run hundreds of services to provide prime brokerage products to our clients. Dozens of scheduled batch jobs process millions of trades, journals, and transactions every day to facilitate trade clearing, calculate risk, and generate financial reports.

![Kubernetes Logo](/assets/img/casestudy_clearstreet/kubernetes.png)

Our Kubernetes clusters manage all of these critical microservices and batch jobs; we rely on Kubernetes for networking, deployments, pod scaling, load balancing, node auto-scaling, cron jobs — the list goes on. So, it might come as a surprise that developers at Clear Street weren’t using Kubernetes during their local development loop until this year. They weren’t able to leverage any Kubernetes features nor use Kubernetes-native infrastructure like [Argo](https://argoproj.github.io/argo-workflows/).


Today, nearly every Clear Street developer’s inner loop involves Kubernetes with what we’ve dubbed “localkube”: local development with Kubernetes.


## Local development before localkube

At the end of last year, we began to see repeating issues crop up with local development. Services’ local configuration was quite different from their cluster configuration: networking, service discovery, replication, pod readiness, and more were all different.


Eventually, local configuration issues started to eat into developer time. The problem was twofold:
1. We had to maintain separate local and cluster configurations (and code!).
2. Cluster configurations remained untested until deployed in our development cluster.

While using Docker Compose and Docker networks would solve some of these problems, we saw that as a half-baked solution that would still miss out on some essential Kubernetes features.


### Why use Kubernetes locally?

We decided to move to local Kubernetes development for the following benefits. It lets us:
1. Bring local configuration as close as possible to our clusters.
2. Test Kubernetes configuration (resource limits, exposed ports/services, environment variables, liveness/readiness probes) earlier in our testing pipeline, even before code reaches our development cluster.
3. Quickly test replicated services, including pod startup and shutdown behavior.
4. Develop and experiment with Kubernetes-native tools, like Argo and service meshes.
5. Easily test upgrading Kubernetes.
6. Remove our bespoke service startup scripts and reduce technical debt.


## Our local Kubernetes tooling choices

This article won’t go into comparing tools — there are [plenty](https://www.rookout.com/blog/developer-tooling-for-kubernetes-in-2021-part-2) of [articles](https://www.bizety.com/2020/07/02/kubernetes-tools-helm-skaffold-tilt-draft-and-garden/) available [already](https://medium.com/containers-101/the-ultimate-guide-for-local-development-on-kubernetes-draft-vs-skaffold-vs-garden-io-26a231c71210). However, we include some reasons as to why we chose the tools we did.


### kind

First, we need to create a local Kubernetes cluster. We picked [kind](https://kind.sigs.k8s.io/) because of its fast startup and shutdown speed, simplicity, good documentation, and community support.

After wrapping some startup configuration in a script, creating a local cluster is as simple as:
```
make create-cluster
```

This does several things:
1. Creates a Kubernetes cluster pinned to our production Kubernetes version.
2. Adds Ingress support to the cluster.
3. Creates a local Docker registry and connects the cluster to it.

Deleting or recreating the local cluster is simple as well:
```
# delete
make delete-cluster

# recreate
make delete-cluster create-cluster
```


### Tilt

Next, we found a solution for the “inner development loop”: code, build, run, repeat.


The tooling landscape for this task is extensive, with notable contenders being [skaffold](https://skaffold.dev/), [garden](https://garden.io/), and [Tilt](https://tilt.dev/).


We chose Tilt for managing the inner development loop for the following reasons:
1. Its simple web UI for log viewing and high-level information is essential for developers new to Kubernetes.
2. Its large feature set, including container building improvements like “[live update](https://docs.tilt.dev/live_update_reference.html).”
3. The [Starlark](https://github.com/bazelbuild/starlark) configuration language (a dialect of Python) is powerful and straightforward to learn.

Out-of-the-box, Tilt was easy to incorporate into our codebase. In about a week, we could launch most of our services in a local Kubernetes environment.


After describing how to build our images in Starlark, we tell Tilt the services we want to run, like `bank` and `appliances`:
```
tilt up appliances bank
```
Here, `appliances` is an alias to our shared core infrastructure: Postgres, Kafka, Schema Registry, etc.
After running this command, Tilt serves a pleasant web UI with service status, build and runtime logs, service groupings, and Kubernetes information like Pod ID:

![Tilt UI](/assets/img/casestudy_clearstreet/tilt-ui.png)

Once Tilt detects that the code has changed, it will automatically update the correct service in your cluster!


One of Tilt’s many valuable features is describing services’ dependencies. Above, we’ve only specified the `bank` service, but our Starlark configuration reads other YAML configuration files and figures out that `bank` needs several other services and launches those.


As a performance improvement, Tilt uses the local registry we set up earlier to send Docker images into the cluster quickly.


### Control loop

At its core, Tilt:
1. Watches your file system for file changes
2. Builds and tags Docker images of your services when files change
3. Pushes images to the local registry
4. Tells Kubernetes to pull the new images and restart specific Pods

Of course, it does much, much more than this, and we rely on its extensive feature set for an improved developer experience.


## Tilt performance improvements

After the initial honeymoon period with Tilt, we improved the local developer experience even more by speeding up Tilt’s inner loop.


### Build caching

What if we want to launch 50 microservices to test some complicated workflows for a code change? At Clear Street, the time to build 50 Go, Node.js, and Python Docker images is unacceptable.


Instead, we use a performance trick: pull the latest-tagged Docker image for each service, unless specified otherwise.


For example:
```
tilt up appliances price -- --local bank
```
We use this syntax to say:
1. Launch `appliances`, `bank`, `price`, and their dependencies.
2. For everything except `bank`, pull the `latest` image from our Docker registry.
3. Read the local file system for `bank`, build the Docker image, and inject it into the local cluster.

Why does this caching mechanism work well? It’s because any code that merges to our main branch will automatically generate a new `latest`-tagged image. When the local branch is recent enough with the main branch, it will be running the same image as if it were built locally.


For our services, the time saved from caching is enormous. Additionally, restarts are fast because the local cluster caches the images.


### Dockerfile best practices

By following the [Dockerfile best practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/) from the beginning of Clear Street, we’ve benefited from fast reloading of Docker images: carefully ordering Docker layers goes a long way towards speeding up Docker builds.


For example, Go Dockerfiles have:
```
# Rarely changing code above

COPY go.mod go.mod
COPY go.sum go.sum
RUN go mod download

# Frequently changing below
```

With a warm cache, Docker will altogether skip the `go mod download` as long as `go.mod` and `go.sum` haven’t changed.


### live_update

Finally, some of our services benefited immensely from a Tilt feature called `live_update`. Rather than build a Dockerfile from scratch every time, `live_update` lets us sync files into the container instantly and run arbitrary commands.


For our Node.js services, we wanted to use `nodemon` because:
1. It’s how our engineers are used to working.
2. It can quickly rebuild Node apps (under five seconds).

With just a few lines of code in Starlark, we could automatically sync our Node.js services’ code into the container and run `nodemon` like normal. This brought the inner development loop speed to parity as before with those services.


## Outcomes

After rolling out localkube, we saw developers take off with the new capabilities. We:
1. Began using Argo Workflows and Argo Events.
2. Created sandboxed environments in the cloud for a specific branch (more on that in a future blog post!).
3. Tested deployments before merging to our main branch.
4. Tried out more Kubernetes-native tools like service meshes.
5. Gained higher confidence and a lower failure rate in production.

The Tilt UI has been instrumental in developer experience and has helped us teach Kubernetes and Docker to more Clear Street developers. Additionally, switching branches and work contexts has never been easier for us.


The Tilt team has been great to work with; they’ve helped us onboard more developer workflows and have promptly released features that we have requested.


On average, our developers have been able to increase their development time, being able to iterate on the inner development loop two to four times faster than before.


## Looking forward

Our developers are excited by this new workflow and are looking forward to further enhancements down the road. For example, we don’t support debugging services running in a cluster yet. Luckily, [Tilt has a guide for this](https://docs.tilt.dev/debuggers_python.html), and we intend to enable it soon.


One long-desired feature at Clear Street was branch deploys: ephemeral, sandboxed, cloud environments built from a single source branch. Because of Tilt and localkube, we’ve been able to create and delete these ephemeral environments quickly. For the tech behind that, stay tuned for a future blog!


Finally, things keep getting better in the local Kubernetes development landscape. Kind has gotten more stable, and the Tilt team consistently improves the tool with the features we request. There is no looking back for Clear Street: local Kubernetes development with these tools has improved developer experience and reduced production risk.
