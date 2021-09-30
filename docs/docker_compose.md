---
title: A Better UI for Docker Compose
description: "Tilt can use 'docker-compose' to orchestrate your services instead."
layout: docs
sidebar: guides
---

Most of our documentation describes using Tilt to deploy to Kubernetes.

But if you already use Docker Compose, don't worry! Tilt can use `docker-compose` to orchestrate your services instead.

This doc describes how you can get Tilt's UX for your Docker Compose project using the same config and tools plus a
one-line Tiltfile. (This is simpler than the config for Kubernetes projects
described in the [Write a Tiltfile Guide](tiltfile_authoring.html).)

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

```bash
tilt up
```

Tilt will pick up your Docker Compose file and start running your services.

Be aware of one important difference between `tilt up` and `docker-compose up`: Tilt
will leave your services up when it exits. To turn the services down, run:

```bash
tilt down
```

## Using Tilt's `docker_build`

Tilt automatically uses your [`build` configuration](https://docs.docker.com/compose/compose-file/#build)
from Docker Compose. You can also use the `docker_build` function to use Tilt's
updating optimizations. Tilt will find the image name in your `docker-compose.yml`,
and use its own updating strategy instead of the one in the `docker-compose.yml` file.

Let's look at a simple example app that runs Redis and a NodeJS-based server with Docker Compose.
We'll use the same example as in
[this blog post](https://codewithhugo.com/setting-up-express-and-redis-with-docker-compose/) with
[this Git repo](https://github.com/tilt-dev/express-redis-docker).

First, we create a `Dockerfile` that sets up a NodeJS environment,
adds the NodeJS dependencies, then adds the source code.

```dockerfile
FROM node:9-alpine
WORKDIR /var/www/app
ADD package.json .
RUN npm install
ADD . .
```

Next, we put an image name in our `docker-compose.yml` file.
We're not going to be pushing this image
to a remote registry, so any image name will do. We use `tilt.dev/express-redis-app`.

```yaml
redis:
  image: redis
  container_name: cache
  expose:
    - 6379
app:
  image: tilt.dev/express-redis-app
  links:
    - redis
  ports:
    - 3000:3000
  environment:
    - REDIS_URL=redis://cache
    - NODE_ENV=development
    - PORT=3000
  command:
    sh -c 'node server.js'
```

Lastly, we need to tell Tilt how to build this image. Here's our Tiltfile:

```python
docker_compose('docker-compose.yml')
docker_build('tilt.dev/express-redis-app', '.')
```

Now, when we run `tilt up`, Tilt will manage the image builds
and re-build every time a file changes.

## Using Tilt's `live_update`

This works OK. But building a new image on every change can be a drag.

With the `live_update` option, we can make it a lot faster by updating the container in-place.

Here's the new Tiltfile:

```python
docker_compose('docker-compose.yml')
docker_build('tilt.dev/express-redis-app', '.',
  live_update = [
    sync('.', '/var/www/app'),
    run('npm i', trigger='package.json'),
    restart_container()
  ])
```

The `live_update` option is expressed as a sequence of in-place update steps.

1. The `sync` step copies your local files into the running container.

2. The `run` step re-runs `npm i` inside the container every time you edit `package.json`.

3. The `restart_container` step restarts the server so that your changes are picked up.

For more info on `live_update`, check out the [full tutorial](live_update_tutorial.html).

## Multiple Compose Files

To use multiple
[Docker Compose files](https://docs.docker.com/compose/extends/), simply pass
the list of files to your `docker_compose` function.

```python
docker_compose(["./docker-compose.yml", "./docker-compose.override.yml"])
```

## Debugging

Tilt uses Docker Compose to run your services, so you can also use `docker-compose` to examine state outside Tilt.

## Try it Yourself

All the code in this tutorial is available in [this Git repo](https://github.com/tilt-dev/express-redis-docker).
Run it yourself and make changes to see how it works.

## Troubleshooting

Our Docker Compose support is not as widely used as Tilt's Kubernetes support.

You may hit more/different bugs, which we want to fix -- please file issues or tell us in Slack.
