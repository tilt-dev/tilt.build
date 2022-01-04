---
slug: "arm-wrestling-in-dev"
date: 2022-01-04
author: nick
layout: blog
title: "ARM/M1 + Tilt = ❤"
subtitle: "Ways to set the right platform for your images"
description: "Ways to  set the right platform for your images"
image: "/assets/images/arm-wrestling-in-dev/cover.jpg"
image_caption: "The M1 high-throughput bus in action. Wah wah. Courtesy of <a href='https://commons.wikimedia.org/wiki/File:MTA_NYC_Bus_M1_bus_at_Broadway_%26_8th_St.jpg'>Mtattrain on Wikimedia.org</a>."
tags:
  - docker
  - arm
---

Maybe you got a fancy new MacOS M1 laptop and now you're getting [cryptic
errors](https://github.com/docker/for-mac/issues/5873) when you build your app.

Or maybe you're trying out [EC2
Graviton](https://aws.amazon.com/ec2/graviton/) machines in your dev cluster,
but now none of your images work right.

Welcome to the world of ARM processors! The x86 monoculture has been broken!

Better processors is good for the ecosystem in general. But now your dev environment has to
handle the case where your host CPU is different from the target CPU.

Tilt has shipped a few small tweaks recently that we hope will help build for
the right CPU without having to think about it.

## Setting Platform Automatically

If you're using Tilt to build Docker images with `docker_build`,
we'll now automatically read the architecture off the cluster
and use that in the Docker build.

In the logs, you'll see a line like this:

```
STEP 1/5 — Building Dockerfile: [tilt-site]
Building Dockerfile for platform linux/amd64:
```

We've detected that the cluster architecture is `amd64` and will use this instead of your
host architecture.

## Setting Platform Manually

Maybe you want to force a particular architecture, or build multi-platform images in dev.

You can override the platform manually by:

- Setting the `DOCKER_DEFAULT_PLATFORM` [env var](https://docs.docker.com/engine/reference/commandline/cli/#environment-variables) before you run `tilt`.

```bash
export DOCKER_DEFAULT_PLATFORM="linux/amd64,linux/arm64"
tilt up
```

- Setting the `DOCKER_DEFAULT_PLATFORM` env var in your Tiltfile:

```python
os.environ['DOCKER_DEFAULT_PLATFORM'] = 'linux/amd64,linux/arm64'
```

- Setting the `platform` argument for `docker_build` in your Tiltfile. 

```python
docker_build('fe', '.', platform='linux/amd64,linux/arm64')
```

## Wiring it Yourself

One of our goals with Tilt is to expose every part of your dev environment
as a Kubernetes-style API, so you can use it in your own scripts
to make decisions in an automated way.

Our current solution is the [Cluster API](https://api.tilt.dev/kubernetes/cluster-v1alpha1.html).

The `default` cluster object is what Tilt knows about the place it's deploying images.

```bash
$ tilt describe cluster default
Name:         default
...
Spec:
  Connection:
    Kubernetes:
Status:
  Arch:  amd64
```

In this example, we're using the default Kubernetes cluster connection.

If you want to get the architecture of that cluster only, you can use the CLI:

```
$ tilt get cluster default -o=jsonpath --template="{.status.arch}"
amd64
```

## The Future

Stay tuned for future changes to the cluster API so that you can
use cluster info in your dev env, reset the cluster, and create new ones!

Shout out to Nick Jüttner, Jérôme Petazzoni, and Nick Sieger for [suggesting
ideas](https://github.com/tilt-dev/tilt/issues/4274) on how to better support
multiple architectures.
