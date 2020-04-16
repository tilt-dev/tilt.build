---
slug: "how-to-not-break-server-startup"
date: 2020-04-16
author: nick
layout: blog
title: "How to Confidently Not Break Server Startup"
subtitle: "Introducing Tilt CI"
image: "/assets/images/how-to-not-break-server-startup/header.jpg"
image_caption: "Photo by <a href='https://unsplash.com/@giancarlor_photo?utm_source=unsplash&amp;utm_medium=referral&amp;utm_content=creditCopyText'>Giancarlo Revolledo</a> on <a href='/s/photos/broken?utm_source=unsplash&amp;utm_medium=referral&amp;utm_content=creditCopyText'>Unsplash</a>"
tags:
  - ci
  - testing
  - kind
---

Does this story sound familiar?

You commit a change. You push it to CI. All tests pass. You merge. The change
deploys to staging.

Then your Ops team notifies you that all the staging servers are down. But don't
worry, they've already reverted your change!

😭😭😭

Oh, the war stories I could tell you about staging servers that failed to
start. I remember one bug where the code assumed process IDs were pseudo-random,
and _of course_ each new server process would get a unique process ID. Or
another where a Javascript bundler changed where the generated files lived in
the prod builds. Or the struggles to adapt how each generation of compiled
language invents a new way to
[package](https://docs.microsoft.com/en-us/aspnet/core/fundamentals/static-files?view=aspnetcore-3.1)
[static](https://en.wikipedia.org/wiki/Java_resource_bundle)
[resources](https://github.com/markbates/pkger).

But after years of failure, I'm optimistic.

Kubernetes is becoming a shared standard for running multi-service apps in prod.
Lots of teams are getting Kubernetes into lots of different environments,
including CI.

Does that mean we have the tools to test, in CI, that all the servers in our app
can start?

## Introducing `tilt ci`

To test our Kubernetes app in CI, we need two big pieces.

We need [a new kind of build system that knows how to watch
runtime](https://blog.tilt.dev/2019/09/05/put-down-particle-accelerator.html)
and verify your server is healthy.

We need a way to spin up [short-lived clusters from
scratch](https://blog.tilt.dev/2020/02/11/delete-clusters-faster-with-kind.html).

We're going to briefly walk you through each piece.

### `tilt ci` Command

Tilt now has a new command: [`tilt ci`](https://docs.tilt.dev/cli/tilt_ci.html).

If `tilt up` is for an interactive multi-service development environment, 
`tilt ci` is for testing that same environment in CI.

When you run `tilt ci`, Tilt will:

1. Read your Tiltfile
2. Build and push all the container images
3. Deploy the servers 
4. Wait until the servers are healthy
5. And exit on success!

If it encounters any unrecoverable errors, Tilt will quit immediately.

If you want to customize how Tilt defines "healthy", Kubernetes lets you define [readiness
probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)
that let you provide your own definition.

And when you need checks beyond what you can express in readiness probes, use [a
`local_resource`](https://docs.tilt.dev/local_resource.html) with arbitrary
commands to run against your server.

### Ephemeral CI clusters

You can run `tilt ci` against any cluster, even a production one like AKS or
GKE.

But for testing on CI, we recommend [Kind](https://kind.sigs.k8s.io/).

When you start [Kind with a local
registry](https://blog.tilt.dev/2020/02/11/delete-clusters-faster-with-kind.html),
you have an entirely self-contained cluster environment. No secret
keys for a private container registry. No service accounts. No hosted
inscrutable magic. Just you and your cluster.

For specific details on how to get a Kind cluster set up on your own CI environment, see:

- [Kind on CircleCI with Tilt](https://github.com/windmilleng/kind-local/blob/master/.circleci/README.md)
- [Kind with Tilt](https://github.com/windmilleng/kind-local/blob/master/README.md)
- [Other Kind on CI Examples](https://github.com/kind-ci/examples)

## See it in Action

[`tilt ci`](https://docs.tilt.dev/cli/tilt_ci.html) is available in [Tilt
v0.13.0](https://github.com/windmilleng/tilt/releases/tag/v0.13.0) and higher.

We're not just advocates for the local Kubernetes dev club. We're also clients! 👨‍🦲

Every change in our [repo](https://github.com/windmilleng/tilt) creates a new
Kind cluster and runs the latest build of Tilt against it.

We recently developed guides for servers written in:

- [HTML](https://github.com/windmilleng/tilt-example-html)
- [Go](https://github.com/windmilleng/tilt-example-go)
- [Python](https://github.com/windmilleng/tilt-example-python)
- [NodeJS](https://github.com/windmilleng/tilt-example-nodejs)
- [Java](https://github.com/windmilleng/tilt-example-java)
- and [C#](https://github.com/windmilleng/tilt-example-csharp)

All of them use `tilt ci` with a Kind cluster to test that the servers start
up. With each Tilt release, we create a [Tilt Docker
image](https://hub.docker.com/repository/docker/tiltdev/tilt/general) that
contains Tilt and Kind for use in CI. Check out the guides if you need a working
example!


