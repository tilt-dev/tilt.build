---
slug: "old-school-remote-dev-clusters"
date: 2021-10-11
author: nick
layout: blog
title: "Setting up a Remote Dev Environment When You're a Cloud Skeptic"
subtitle: "We'll use Tailscale and Kind to Duct Tape Together a Dev Env"
description: "We'll use Tailscale and Kind to Duct Tape Together a Dev Env"
image: "/assets/images/old-school-remote-dev-clusters/cloud.jpg"
tags:
  - ctlptl
  - tailscale
  - kind
---

Lately, when I try to present demo apps, they're often very slow. 
Zoom is a CPU hog. And doesn't leave much CPU left for my apps to run.
When I try to run demos on MacOS with Docker Desktop running, it's even
worse.

There are lots of teams who are trying to sell you on a remote
dev environment as a service. And that's fine. This is a good problem
to solve. Maybe we'll all be on dev envs as a service some day.

But we live in a world where there are computers EVERYWHERE.  In my
pocket. Under my desk. I wondered: could I offload my dev environment to ANY
random computer?

It turns out you can!

In this post, I want to share how I set up my standard remote dev environment.

We'll use:

- A box under my desk.

- [Tailscale](https://tailscale.com/) to create a secure tunnel to the box.

- A Docker daemon that listens on the Tailscale network.

- [Kind](https://kind.sigs.k8s.io/) to create a self-contained Kubernetes environment.

Let me show you!

## Setting up Tailscale

Let's be clear: we're setting up a remote box that can run arbitrary servers.

If we don't want it to be hacked by crypto miners, we'll need to secure it.

Tailscale creates a VPN so that I can have a
point-to-point secure connection between my laptop running my IDE, and my
remote dev environment running my services.

I'm currently using the free, single-player Tailscale since the remote box is
just for me.

1. I [installed](https://tailscale.com/download) Tailscale on both my laptop and
   the remote box.

1. I [disabled key expiry](https://tailscale.com/kb/1028/key-expiry/) on the
   remote box so that I don't need to login and re-auth.
   
1. I [configured](https://tailscale.com/kb/1077/secure-server-ubuntu-18-04/)
   Ubuntu's Uncomplicated Firewall (UFW) to deny all traffic, except for traffic over
   the Tailscale network. (edited 10/12 - see below for a big security caveat [^1].)
   
This box will only run dev services for now. I'll talk later about how
I access the services.

## Setting up Docker

Normally, the Docker daemon listens on a Unix socket (basically a file).

We want to expose it to the Tailscale network. 

The network gives the box a name and an IP. On my network, the remote box is
named `ed`. We'll say `ed` has IP `100.2.3.4`.

1. On the remote box, I [installed](https://docs.docker.com/engine/install/) Docker.

1. On my system, this runs Docker with systemd. (The following instructions
   might be different if you're on a distro that doesn't use systemd.)
   
1. On the remote box, I ran `sudo systemctl edit docker.service` to edit the Docker config.

1. I added these lines:

    ```
    [Service]
    ExecStart=
    ExecStart=/usr/bin/dockerd -H fd:// -H tcp://100.2.3.4:2375
    ```

    with the IP address of my box.

1. On my laptop, I set `export DOCKER_HOST=tcp://ed:2375/` to connect, where `ed`
   is the name of my remote box. I put this in my `~/.profile` so that my
   `docker` command connects to it by default.

I got these instructions from [this Docker
guide](https://docs.docker.com/engine/install/linux-postinstall/#configure-where-the-docker-daemon-listens-for-connections).

Now I don't need to run Docker Desktop on my laptop at all!

## Setting up the Remote Dev Environment

Team Tilt maintains an open source tool called [`ctlptl`](https://github.com/tilt-dev/ctlptl/) for setting up a dev cluster.

You can do this without `ctlptl`, but `ctlptl` does all the plumbing of creating
a Kind cluster, creating an image registry, connecting the cluster to the
registry, then forwarding localhost to both the cluster and registry.

There are a bunch of pieces! `ctlptl` coordinates the pieces.

These instructions are for MacOS (though `ctlptl` should work on Linux and Windows too).

1. Install tools: 

    ```bash
    brew install socat kind tilt-dev/tap/ctlptl
    ```

2. Create the cluster: 

    ```bash
    ctlptl create cluster kind --registry=ctlptl-registry
    ```

That's it!

As `ctlptl` sets up the cluster, it should detect that you have `DOCKER_HOST`
pointing at a remote box, and set up localhost connections. The output looks like this:

```
 🎮 Env DOCKER_HOST set. Assuming remote Docker and forwarding apiserver to localhost:39477
 🔌 Connected cluster kind-kind to registry ctlptl-registry at localhost:38335
 👐 Push images to the cluster like 'docker push localhost:38335/alpine'
cluster.ctlptl.dev/kind-kind created
```

When you use Tilt to start your dev environment, Tilt will build images
on the remote Docker server, push them to the remote registry, run them
on the remote cluster, and live-update the containers in-place! 

You can access the services like any other `localhost` service. Tilt can
[set up port-forwards](https://docs.tilt.dev/accessing_resource_endpoints.html#creating-a-kubectl-port-forward-tunnel)
that go through the Tailscale network
and make the remote service available on `localhost:8000`.

None of it runs on your laptop at all, which leaves plenty of CPU for Zoom to
waste!

## A Defense on Clusters Under Desks

I'm sure there's some Ops person reading this and shouting "NOOOO you can't run
a dev cluster under your desk."

And maybe someday I'll move to a SAAS.

But...it's also fine? I don't need 99% uptime.

When I worked at Google, it will still VERY normal until 2009/2010-ish to
ask IT for a machine, put it under your desk, and run a CI like Jenkins on it.

And at least until 2011-ish, a substantial number of Google's internal
apps linked to Javascript served from a box under Dan Pupius' desk. Those internal
apps would go down on the weekends when he moved desks. But sure, OK.

Maybe I'm an old internet person. But I think that approach to the internet is
underrated!

[^1]: Mike Deeks [points
    out](https://twitter.com/mike_deeks/status/1447750784326651904) that when
    used together, Docker can bypass UFW, and containers can be exposed to the
    public internet. The setup in this post should be OK due to additional
    layers of security (in particular, Kubernetes). But double-check your
    firewall if you plan on using, say, Docker Compose to run dev contianers.
