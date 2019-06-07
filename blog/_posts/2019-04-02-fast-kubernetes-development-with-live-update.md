---
slug: fast-kubernetes-development-with-live-update
date: 2019-04-02T09:27:35.205Z
author: dan
layout: blog
title: "Fast Kubernetes Development with Live Update"
image: featuredImage.jpeg
image_caption: Soon, your iteration loop will feel like this.
tags:
  - docker
  - development
  - kubernetes
  - microservices
  - tilt
keywords:
  - docker
  - development
  - kubernetes
  - microservices
  - tilt
---

Would you like to update your code on Kubernetes without waiting for a Docker build each time you change a file?

The new **Live Update** feature of Tilt does just that. It’s live in [Tilt v0.8](https://github.com/windmilleng/tilt/releases). This post walks through setting up Live Update and using Tilt to speed up your Kubernetes iteration loop to just seconds.

Live Update supports more projects than most sync tools because in addition to syncing files, it can run commands — which lets you call compilers, code generators, and more. (In particular, this means that Go projects can finally see the benefit of Go’s fast compiler even when running on Kubernetes.)

We’ll be using [this example repo](https://github.com/windmilleng/live_update/) to demonstrate how to get up and running with Live Update. Feel free to pull it down, [install Tilt](https://docs.tilt.dev/install.html), and follow along.

### Phase 0: Tilt-ify your Deployment

Live Update builds on top of Tilt’s ability to build, push, and apply images to Kubernetes. In this example, we’ll be iterating on a single Kubernetes Deployment. Let’s start with a simplified version of the Tiltfile for a Python project:

```
k8s_yaml('hello.yaml')
docker_build('hello-py-image', './hello')
```


Let’s explain each value:

1. `hello.yaml`: the path to a yaml file with your Kubernetes Deployment

1. `hello-py-image`: the name of the image, as used in your Deployment YAML

1. `./hello`: path to the directory to docker build

Now whenever you save a file in `./hello`, Tilt rebuilds and redeploys your Deployment. This is easier than manually running `docker build && kubectl apply` every time, but no faster. And in the words of the 1986 film “Top Gun”, “I feel the need. The need… for speed.”

### Phase 1: Sync Files

Let’s use Live Update to sync files into a running pod. In the Tiltfile, we tell Tilt that this image can be updated by syncing files directly into the running container:

```
k8s_yaml('hello.yaml')
docker_build('hello-py-image', './hello',
  live_update=[ sync('./hello', '/') ])
```


`sync` takes two arguments: the local path, and target path in the running container.

When you save a file in `./hello`, Tilt copies the file into the running container (at the root). Of course, if we can’t reach the container for some reason (e.g. if the pod dies), Tilt notices, and builds and deploys the image from scratch.

### Phase 2: Run Commands

Kubernetes sync tools have been limited to syncing code, which is fine for dynamic languages but doesn’t help you if you’re writing in a compiled language. This is especially frustrating for Go developers, because the Go compiler is really fast when it gets to use the cache — but a fresh image build can throw that cache away.

**Let’s switch gears and look at our example Go project.**

Here’s a simplified version of our example Go Tiltfile, using `run` to invoke a command on each Live Update:

```
k8s_yaml('hello.yaml')
docker_build('hello-go-image', './hello',
  live_update=[
    sync('./hello', '/app/src'),
    run('cd /app/src && go install .'),
    restart_container(),
  ])
```


When you save, Tilt will:

1. copy over the changed file(s)

1. run the command

1. restart the container (so we execute the updated binary)

### Phase 3: Fall Back to Full Build

Sometimes, though, you don’t want to execute commands on the running container. For instance, updating dependencies (with `npm` or `pip`) or generating code (with `protoc` or `thrift`) may be more complexity than you want to deal with in your cluster, and you’d rather just do a fresh image build.

Live Update lets you tell Tilt to fall back to a full build when certain files are edited. Say we don’t want our running container to have internet access; we can’t download new dependencies from the container, so we want to to a full image build whenever our deps change. Here’s the snippet of the Go project Tiltfile that accomplishes this:

```
docker_build('hello-go-image', './hello',
  live_update=[
    fall_back_on('hello/go.mod'),
    sync('./hello', '/app/src'),
    run('cd /app/src && go install .'),
    restart_container(),
  ])
```


When you save a file, Tilt will fall back if it matches `fall_back_on`. Here we fall back for `go.mod`, but in Python you might want to fall back on edits to `requirements.txt`, and in Javascript, `package.json`.

### Conclusion

Live Update gives you the fastest Kubernetes update cycle; not only can you sync code, but unlike other Kubernetes sync tools, you can run commands and take advantage of caches and existing artifacts. You also get Tilt’s UI (you can see when your code is up-to-date or failing) and Reliability (when a pod gets restarted, Tilt will automatically resync the latest code so it’s never out-of-date). Like all of Tilt, it works with any cluster (EKS, GKE, minikube, Docker-for-Desktop, etc.).

You can get started Live Updating in 10 minutes using the [example repo](https://github.com/windmilleng/live_update/tree/dbentley/initial) or set up your own project using our [Tutorial](https://docs.tilt.dev/tutorial.html). We’d love to hear what you think. Join the #tilt channel in [Kubernetes Slack](http://slack.k8s.io/) or reach out to [@windmill_eng](https://twitter.com/windmill_eng) on Twitter.
