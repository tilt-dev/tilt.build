---
title: Docker Compose
layout: docs
---

Most of our documentation describes using Tilt to deploy to Kubernetes.

But if you already use Docker Compose, don't worry! Tilt can use `docker-compose` to orchestrate your services instead.

This doc describes how you can get Tilt's UX for your Docker Compose project using the same config and tools plus a
one-line Tiltfile. (This is simpler than the config for Kubernetes projects
described in the [Tutorial](tutorial.html).)

## Comparison

Tilt helps you manage your Docker Compose environment:

* The UI shows you status at a glance, so errors can't scroll off-screen.
* You can navigate the combined log stream, or dig into the logs for just one service.
* Tilt handles filesystem watching and updating containers in-place.

If you decide to move to Kubernetes later, your Tilt workflow will be the same.

## Getting Started

Create a Tiltfile in the root of your repo:

```python
# point Tilt at the existing docker-compose configuration.
docker_compose("./docker-compose.yml")
```

That's it! Then run:

```
$ tilt up
```

Tilt will pick up your Docker Compose file and start running your srvices.

## Making Changes

Tilt has two functions for building container images.

With `docker_build`, Tilt builds an image from your existing Dockerfile. Every time the files change,
Tilt will re-build the image and update the container.

With `fast_build`, Tilt knows how to copy files directly to your container. When you build for the first
time, Tilt builds the image. When you change a file, Tilt will try to be smarter and only sync the files
it needs.

When you declare either `docker_build` or `fast_build`,
Tilt will find the image name in your `docker-compose.yml`,
and use its own container-updating strategy instead of the one in the `docker-compose.yml` file.

For more details on Tilt's image-building strategies, see the [fast build
documentation](fast_build.html) or the [api reference](api.html).

## Debugging

Tilt uses Docker Compose to run your services, so you can also use `docker-compose` to examine state outside Tilt.

## Troubleshooting

Our Docker Compose support is not as widely used as Tilt's Kubernetes support.

You may hit more/different bugs, which we want to fix -- please file issues or tell us in Slack.
