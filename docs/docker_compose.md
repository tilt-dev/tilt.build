---
title: Setting Up Docker Compose
description: "Using Docker Compose to run multiple containers in Tilt"
layout: docs
sidebar: guides
---

[Docker Compose](https://docs.docker.com/compose/) helps you define microservice apps
that run in multiple containers.

Most Tilt documentation uses Kubernetes to run multiple containers. But there's also a strong
subset of Tilt users who use Docker Compose as their container runtime!

In this guide, we'll show you how to connect Docker Compose to a Tilt dev environment. This lets you:
 
- Organize each Docker Compose service from the Tilt dashboard.

- Control when and how each service runs.

- Add live updates in-place for each service.

If you'd like to skip straight to the example code, visit this repo:

[tilt-example-docker-compose](https://github.com/tilt-dev/tilt-example-docker-compose){:.attached-above}

The repo contains a complete sample app, a Tiltfile, and a test that uses `tilt ci` to make sure
the app runs successfully.

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
version: "3.9"
services:
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

For more info on `live_update`, check out the [reference](live_update_reference.html).

## Multiple Compose Files

To use multiple
[Docker Compose files](https://docs.docker.com/compose/extends/), simply pass
the list of files to your `docker_compose` function.

```python
docker_compose(["./docker-compose.yml", "./docker-compose.override.yml"])
```

## Debugging

Tilt uses Docker Compose to run your services, so you can also use `docker-compose` to examine state outside Tilt.

## Organizing Services

The `dc_resource` Tiltfile function lets you pass options how your services run:

[Labels](tiltfile_config.html#labels) let you control put services into groups. The example repo contains these labels:

```
dc_resource('redis', labels=["database"])
dc_resource('app', labels=["server"])
```

If you have a server that doesn't need to run in every dev environment, you can tell
Tilt not to run it at startup:

```
dc_resource('storybook', auto_init=False)
```

For a complete list of options, see [the API reference](api.html#api.dc_resource).

## Try it Yourself

All the code in this tutorial is available in this repo:

[tilt-example-docker-compose](https://github.com/tilt-dev/tilt-example-docker-compose){:.attached-above}

Run it yourself and make changes to see how it works.
