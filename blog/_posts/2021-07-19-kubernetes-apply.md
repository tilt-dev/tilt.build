---
slug: "kubernetes-apply"
date: 2021-07-19
author: nick
layout: blog
title: "More Continuous than Continuous Deployment"
subtitle: "A brief intro to the KubernetesApply API, and how Tilt uses it to keep your env up to date"
description: "A brief intro to the KubernetesApply API, and how Tilt uses it to keep your env up to date"
image: "/assets/images/kubernetes-apply/drinking-bird.jpg"
image_caption: "A patent application for a continuously drinking bird, via <a href='https://commons.wikimedia.org/wiki/File:US2402463-0.png'>Wikipedia</a>."
tags:
  - api
  - kubernetes
---

Over the past decade, the infra ecosystem has gotten really great at watching git
repositories, and kicking off jobs when they change. e.g.:

- CI: When my repo changes, run a test.

- GitOps: When my repo changes, compare the contents to my cluster and bring it
  up to date.
  
- Ephemeral Environments: When my branch changes, create a temporary preview
  environment to show my team.
  
But we live in a world where you still have tools running on a local laptop.

Maybe CI failed, and you want to set up a port-forward to connect your local
debugger to the remote environment.

Maybe the ephemeral environment doesn't look right, and you want to live-update some
files into the container to see if you can diagnose the problem quickly.

Tilt sees your local laptop as a part of your infra. We create tools and APIs to
help you connect them. In this post, I'm going to introduce one of the core APIs
that Tilt uses to continuously deploy your local files, and connect to what you
just deployed: the
[KubernetesApply](https://api.tilt.dev/kubernetes/kubernetes-apply-v1alpha1.html)
object.

## Apply Yourself

In any project, you can run `tilt get kubernetesapplys` to get all the
Kubernetes resources that the active Tilt environment is deploying to a cluster.

Here's what this looks like with the example go project:

```
$ git clone git@github.com:tilt-dev/tilt-example-go
$ cd tilt-example-go/0-base
$ tilt up --stream
```

And then in another terminal:

```
$ tilt get kubernetesapplys
NAME         CREATED AT
example-go   2021-07-16T20:43:27Z
```

You can also use `tilt get ka` or `tilt get kapp` for short. We can get the full
spec and status of the apply. It's pretty big, so instead we're going to
break it apart.

The spec of KubernetesApply tells Tilt how to deploy your resources, and when
to redeploy them.

```
$ tilt get kapp example-go -o jsonpath={.spec.yaml} | head -n 6
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: example-go
  name: example-go
```

This project creates a Deployment called `example-go`.

When the deploy is finished, the KubernetesApply object keeps track of the
result.

```
$ tilt get kapp example-go -o jsonpath={.status.resultYAML} | head -n 12
apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: "2021-07-16T20:43:27Z"
  generation: 1
  labels:
    app: example-go
    app.kubernetes.io/managed-by: tilt
  name: example-go
  namespace: default
  resourceVersion: "20821"
  uid: aa46b596-d132-4f04-a503-f52bf61f0f9c
```

If you ever want to know what Tilt is deploying and when, the KubernetesApply can tell you!

## Making the Connection

On its own, the KubernetesApply isn't that much more useful than simply having a terminal
that runs `kubectl apply` every time a file changes.

The power of the API comes with how we connect it! 

We can write other local controllers that watch the API for changes, and react to new apply status. 

Tilt comes out of the box with 3 that are managed directly KubernetesApply:

- KubernetesDiscovery finds pods that belong to the resources you deployed
- PortForward connects those pods to ports on localhost
- PodLogStream copies logs of those pods into the Tilt UI

Let's look at how they work in our example project:

```
$ tilt get kapp example-go -o jsonpath={.spec.portForwardTemplateSpec}
{"forwards":[{"containerPort":0,"host":"localhost","localPort":8000}]}
```

These built-ins ensure that whenever you apply resources, we will always
connect localhost:8000 to the latest version.

And because it's an API, we can write newer and sillier tools that react to the
latest version of our server. Stay tuned for future videos and demos!



