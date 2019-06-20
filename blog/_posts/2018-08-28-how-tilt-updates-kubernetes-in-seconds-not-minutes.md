---
slug: how-tilt-updates-kubernetes-in-seconds-not-minutes
date: 2018-08-28T15:28:24.574Z
author: dan
layout: blog
canonical_url: "https://medium.com/windmill-engineering/how-tilt-updates-kubernetes-in-seconds-not-minutes-28ddffe2d79f"
title: "How Tilt updates Kubernetes in Seconds, not Minutes"
images:
  - featuredImage.png
  - 1*GXhhCXThiOY8QNXOFDPKEA.png
  - 1*1etxOQd3bBcVFuLE10t-ZQ.png
  - 1*b0MM1kRRTvsix3uHxJ3dSA.png
  - 1*Hz6Ht0xggj6GO3vC8vmAUw.png
  - 1*2HUWuW8PNzzDZzwaeYP_pg.png
  - 1*OUhj_0ds9l4-ldyTripowQ.jpeg
tags:
  - docker
  - kubernetes
  - devops
  - developer
  - developer-tools
keywords:
  - docker
  - kubernetes
  - devops
  - developer
  - developer-tools
---
  
When I bring my cat a box of toys, he loves the box and ignores the toys. I wish he’d pay attention to the work I did, but I didn’t let it bother me because he’s a cat. Then I started getting the same reaction from Kubernetes developers.

We built our new tool [Tilt](https://tilt.build) to make Kubernetes updates fast. Really fast. Seconds-instead-of-minutes fast. Cloud-as-fast-as-laptop fast. But when we show it to developers, they love the UI and ignore the speed.

I understand why: Tilt’s [Heads-Up Display](https://www.youtube.com/watch?v=MGeUUmdtdKA) collects errors, from build breakages to stack traces, into one layout so problems are easy to see. Developers see it and grok that Tilt lets them stop playing 20 questions with `kubectl`. But developers stop using tools that get in their way, so even if you start using Tilt because of the UI, you’ll keep using it because your 2m `docker build && kubectl apply` now takes 5s.

I’ll bring you along on our journey of slashing 4 different Kubernetes update overheads. Even though Tilt doesn’t expose each as a configurable option, I want to share the excitement of finding and smashing a sequence of bottlenecks.

## Vanilla Kubernetes Deploy

Before we can update, we have to deploy an initial version. The Kubernetes deploy pipeline:

* send source code to Docker (as a build context)

* run a build command in Docker to create a layer with the generated/compiled artifacts

* push the resulting image to a registry

* allocate a new pod, pull the image and start running

![Vanilla k8s deploy](/assets/images/how-tilt-updates-kubernetes-in-seconds-not-minutes/featuredImage.png)*Vanilla k8s deploy*

## Second Time, Same as the First

Updating kubernetes isn’t an update so much as a second deploy. Even if you just changed one file, Docker will create a new layer with your current source code and start a build from scratch. (Docker’s layers and multistage builds can help, but require much cleverness)

![Two vanilla k8s deploys](/assets/images/how-tilt-updates-kubernetes-in-seconds-not-minutes/1*GXhhCXThiOY8QNXOFDPKEA.png)*Two vanilla k8s deploys*

## Incremental Build

Tilt’s image build API makes it easy to use your build cache on subsequent builds. Realistic builds improve from 30s to 1s.

Broadly speaking, Docker images are built in two steps: first, you copy over your source code; second, you run any steps to compile code or generate artifacts (e.g. “go build”, “proto gen”, “npm install”, etc.) Tilt’s `fast_build` improves both steps. In the copy step, Tilt updates just the edited file(s). In the build step Tilt injects the cache from the previous run.

![The second time you make an apple pie, reuse the previously created universe](/assets/images/how-tilt-updates-kubernetes-in-seconds-not-minutes/1*1etxOQd3bBcVFuLE10t-ZQ.png)*The second time you make an apple pie, reuse the previously created universe*

## Incremental Deploy

We’re not done! Kubernetes is fast at starting new pods, but it can still take seconds. Tilt reuses existing Pods.

A “Synclet” runs on the same node. When you update files, the Synclet adds them to the existing pod and restarts the container. (This is an example of the [Sidecar](https://kubernetes.io/blog/2015/06/the-distributed-system-toolkit-patterns/) pattern).

![Don’t tear down your house each time you want to change a doorknob](/assets/images/how-tilt-updates-kubernetes-in-seconds-not-minutes/1*b0MM1kRRTvsix3uHxJ3dSA.png)*Don’t tear down your house each time you want to change a doorknob*

## Skip Registry

Container registries are amazing for images with high fan-out, but our images are used once. Tilt reduces overhead by sending updates directly to the Synclet.

(This optimization creates corner cases when pods die and restart. Tilt watches your cluster to handle these cases and keep your personal instance in sync.)

![Mitigating the man-in-the-middle makes Mallory mad](/assets/images/how-tilt-updates-kubernetes-in-seconds-not-minutes/1*Hz6Ht0xggj6GO3vC8vmAUw.png)*Mitigating the man-in-the-middle makes Mallory mad*

## Build in Cloud

1KB of edits to a `.go` file creates a 10MB binary diff; or 1 extra line in `package.json` can imply dozens of added libraries. Tilt sends the smaller source edit and does the build on the same node with our personal instance.

Tilt manages the complexity and headaches of running build commands in your cluster so you get faster updates.

![The Code is coming from inside the Cluster](/assets/images/how-tilt-updates-kubernetes-in-seconds-not-minutes/1*2HUWuW8PNzzDZzwaeYP_pg.png)*The Code is coming from inside the Cluster*

## Stand on our shoulders

Sound good? Want this now?

* Read the [Docs](https://docs.tilt.build/) to get Tilt working with your project.

* Star our [GitHub](https://github.com/windmilleng/tilt). Or file an issue. Or fork and submit a pull request.

* Join #tilt in the [Kubernetes Slack](http://slack.k8s.io/) to discuss/request.

Once you’re working with vanilla deploys, upgrade your builds to `fast_build`, as described in our [docs](https://docs.tilt.build/fast_build.html), to get this goodness.

## Cat Photo

![Purring contentedly in his cardboard castle](/assets/images/how-tilt-updates-kubernetes-in-seconds-not-minutes/1*OUhj_0ds9l4-ldyTripowQ.jpeg)*Purring contentedly in his cardboard castle*
