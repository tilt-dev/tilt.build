---
slug: multi-container-live-update
date: 2019-08-27
author: maia
layout: blog
title: "Live Update Multiple Containers Per Pod"
subtitle: "Because your sidecar deserves iteration too!"
image: sidecarDog.jpg
image_needs_slug: true
image_caption: "Who WOULDN'T want to iterate on this sidecar?!"
tags:
  - docker
  - kubernetes
  - microservices
  - tilt
  - containers
keywords:
  - live-update
  - terminal
  - tilt
  - development
---
Back in the Dark Ages (i.e. last week), the lion’s share of Tilt’s logic relied on the constraint that there was only one container per pod that was worth caring about. This was the container that we got restart counts from, that we monitored for stale code, and that we updated in place. If you were running your code on _more than one_ container per pod, well, we could only Live Update[^1] the first one, because that was the only one that Tilt supported. Any changes to the other containers would result in a full `docker build && kubectl apply`.

But, as the Bard said: "There are more workflows in heaven and Earth, Horatio, than are dreamt of in your initial product spec." (Or something.) So, we got cracking on some new functionality: as of [Tilt v0.10.0](https://github.com/windmilleng/tilt/releases), you can use Live Update on as many containers per pod as you want! This feature didn’t change much on the surface of Tilt, but involved a bunch of restructuring and rewriting under the hood--we had to change a bunch of internal assumptions to account for multiple multiple per pod. This touched everything from logs (`kubectl get logs podabc -c mycontainer`) to resource readiness checks to health monitoring--but we think it was worth it!

[Here’s an example repo](https://github.com/windmilleng/sidecar_example) you can take for a spin, based on the premise that you might want to iterate on your app and your home-rolled sidecar at the same time. In this Kubernetes YAML, you can see that we have two different containers running on a single pod:

```yaml
apiVersion: apps/v1
kind: Deployment
...
spec:
  ...
    spec:
      containers:
        - name: randword
          image: randword
          ...
        - name: log-ingester
          image: log-ingester
```

The app is called `randword`, and every second, it logs a random word to a file. The log ingester runs the same pod as the app, reads in the app's logfile by means of a shared volume, and "ingests" the logs (here, just printing them to stdout).

The Tiltfile seems simple, because it’s probably what you expected you could write all along, right up until the point you tried, and got the error: "Tilt only supports Live Updates for the first Tilt-built container on a pod." But now it works!

```python
k8s_yaml('deploy.yaml')

# instructions for how to a. build and b. quickly update the app image
docker_build('randword', '.', dockerfile='Dockerfile.app',
             live_update=[
                 # detect changes to ./app, copy them to the
                 # running container, and restart the app
                 sync('./app', '/app'),
                 run('/restart.sh'),
             ])

# instructions for how to a. build and b. quickly update the sidecar image
docker_build('log-ingester', '.', dockerfile='Dockerfile.sidecar',
             live_update=[
                 # detect changes to ./app, copy them to the
                 # running container, and restart the app
                 sync('./sidecar', '/'),
                 run('/restart.sh'),
             ])
```

Hacking on your sidecar is now just as fast as hacking on your app: make a change in your editor and poof, it’s running in your cluster. Heck, now you can tweak your app and your sidecar at the same and see how they interact! It’s development as it’s meant to be.

## What’s next?

Awareness of multiple containers on a single pod sets us up for awareness of multiple containers across multiple pods--from here, it’ll be much easier to implement Live Updates of a single image across multiple pods. Want to be running multiple replicas of a pod in dev? [Let us know](https://tilt.dev/contact)!

In the meantime, take this new functionality for a spin, and enjoy the wind in your hair as you update _all_ your containers with speed. As always, if you run into problems, or have a use case that you want us to support, [get in touch](https://tilt.dev/contact).

[^1]: Live Update is Tilt's way of updating a running container in place, letting you bypass `docker build` / `docker push` / `kubectl apply`. [Read more about Live Update here](https://blog.tilt.dev/2019/04/02/fast-kubernetes-development-with-live-update.html).
