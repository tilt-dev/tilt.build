---
slug: "how-to-not-break-server-startup"
date: 2020-04-14
author: nick
layout: blog
title: "How to Confidently Not Break Server Startup"
subtitle: "Introducing Tilt CI"
image: "/assets/images/how-to-not-break-server-startup/header.jpg"
image_caption: "I took this picture of <a href='https://www.youtube.com/watch?v=_HTIEcOm3SA'>Flynn's talk at Kubecon 2019</a>, and loved this slide so much."
tags:
  - ci
  - testing
  - kind
---

Does this story sound familiar?

Make a change. Passes all tests. Push to production.

Explosions!

How did that happen?

Faked everything out. Mismatch between dev and prod env

But migrating to Kubernetes means changes to your prod env. Implies changes to server startup.

Slows down migrations to Kubernetes

Every prod migration I've been a part of has broken startup all the time.

How do we prevent this?

## Introducing Tilt CI Vision

Tilt vision: two big pieces

Piece #1: You need a build system that also watches runtime

Piece #2: Ephemeral dev clusters

## `tilt ci` Command

New command: 

`tilt ci`

Build your containers

Run your servers

Healthcheck your servers

Kubernetes has primitives for this!

When it doesn't, use local_resource.

### Kind with Local Registry

Start a cluster

Use a local registry

No external dependencies or special access keys required

Samples links:

- [Kind on CircleCI with Tilt](https://github.com/windmilleng/kind-local/blob/master/.circleci/README.md)
- [Kind with Tilt](https://github.com/windmilleng/kind-local/blob/master/.circleci/README.md)
- [Other Kind on CI Examples](https://github.com/kind-ci/examples)

## See it in Action

For Tilt v0.13.0

Run `tilt ci` to test your servers.

We're not just advocates for the local Kubernetes dev club. We're also clients! :baldman:

Every change in Tilt spins up a local Kind cluster and runs Tilt against it.

Recently developed guides for

- [HTML](https://github.com/windmilleng/tilt-example-html)
- [Go](https://github.com/windmilleng/tilt-example-go)
- [Python](https://github.com/windmilleng/tilt-example-python)
- [NodeJS](https://github.com/windmilleng/tilt-example-nodejs)
- [Java](https://github.com/windmilleng/tilt-example-java)
- [C#](https://github.com/windmilleng/tilt-example-csharp)

All of them use `tilt ci` with a Kind cluster to test that the servers start up.


