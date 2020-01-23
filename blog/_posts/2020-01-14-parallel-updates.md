---
slug: parallel-updates
date: 2020-01-14
author: maia
layout: blog
title: "Parallel Builds and Updates are Here!"
subtitle: "Make Shouldn't Have Mutexes"
image: "/assets/images/parallel-updates/tim-mossholder-u_kg0bcA4qk-unsplash.jpg"
image_caption: "Photo by <a href='https://unsplash.com/@timmossholder?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText'>Tim Mossholder</a> on <a href='https://unsplash.com/?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText'>Unsplash</a>"
tags:
- build
- parallel
---

Building and updating just one service in Kubernetes can be slow.

In microservice land, you potentially have a lot of services: databases, API
gateways,
[internet-enabled teapots](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/418),
and so on. That's a lot of time spent waiting around for Docker builds.

A lot of that idle time is waiting on disk or network I/O. One of the Tilt
community's first big feature requests was for
[parallel builds](https://github.com/windmilleng/tilt/issues/1438), to help
take advantage of unused resources.

We're happy to announce that parallel builds are finally here. Now you can pull
those big docker images in the background and max out your CPU fan at the same
time. Yay!

## You Say Parallel Build, I Say Parallel Update, Let's Call the Whole Thing Fast

We say “update” to refer to any change to, or execution of, a resource.

Examples of updates include:
- `docker build && kubectl apply` to push a new deployment
- Syncing a file to a container
- Running a build script in a container
- Restarting a pod

Tilt wants resource-updating at all scales to be fast, from the small-scale "copy an HTML file pls" to the mega-corp scale `bazel build`.

## How Do I Turn it On?

As of Tilt v0.11.0, parallel updates are included FREE.

By default, Tilt will run up to 3 updates in parallel. More parallel updates are also
available for the low, low cost of [one function call](https://docs.tilt.dev/api.html#api.update_settings) in your Tiltfile:

```python
update_settings(max_parallel_updates=11)
```

We chose 3 for the initial launch to be cautious. We think it strikes a good
balance between showing off the benefits of parallel updates (faster updates and
better network utilization) without too much of the costs (confusingly
interleaved logs and CPU exhaustion).

We may change the default in the future.

## How Do I Turn it Off?

If you want the old behavior, you can disable parallel updates with this line in your Tiltfile:

```python
update_settings(max_parallel_updates=1)
```

Then Tilt will only update one service at a time.

We've found that some users want to guarantee that services come up in a
specific order. For example, maybe you want to ensure the database starts before
your internet-enabled teapot. Don't worry, you don't have to artificially slow yourself down with `max_parallel_updates=1`;
instead, use [resource dependencies](https://docs.tilt.dev/resource_dependencies.html) to
tell Tilt about your service order.

```python
k8s_resource('database', …)
k8s_resource('teapot', …, resource_deps=['database'])
```

With these `resource_deps`, Tilt won't start building `teapot` until the `database` pod is ready.

## What's Next?

We saw this feature help build times for our partners, so wanted to get it in
your hands as soon as possible. We know there are still things to improve! Like:

- [Improving the parallel logic](https://github.com/windmilleng/tilt/issues/2770) to work better with `resource_deps`
- Determining `max_parallel_updates` dynamically based on your computer's capabilities

Have other ideas? Join [the Kubernetes slack](http://slack.k8s.io) and
let us know in the [#tilt](https://kubernetes.slack.com/messages/CESBL84MV/)
channel. Or [file an issue](https://github.com/windmilleng/tilt/issues).
