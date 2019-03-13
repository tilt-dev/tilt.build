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

Tilt will pick up your Docker Compose file and start running your services.

Be aware of one important difference between `tilt up` and `docker-compose up`: Tilt
will leave your services up when it exists. To turn the services down, run:

```
$ tilt down
```

## Making Changes

You can let Docker Compose take care of building images with [a `build` config](https://docs.docker.com/compose/compose-file/#build).

But if you want to leverage Tilt's image-building optimizations,
Tilt has two functions to help you out.

With `docker_build`, Tilt builds an image from your existing Dockerfile. Every time the files change,
Tilt will re-build the image and update the container.

With `fast_build`, Tilt knows how to copy files directly to your container. When you build for the first
time, Tilt builds the image. When you change a file, Tilt will try to be smarter and only sync the files
it needs.

When you declare either `docker_build` or `fast_build`,
Tilt will find the image name in your `docker-compose.yml`,
and use its own container-updating strategy instead of the one in the `docker-compose.yml` file.

## Sample Project With `docker_build`

Let's look at a simple example app that runs Redis and a NodeJS-based server with Docker Compose.
We'll use the same example as in
[this blog post](https://codewithhugo.com/setting-up-express-and-redis-with-docker-compose/) with
[this Git repo](https://github.com/windmilleng/express-redis-docker).

First, we create a `Dockerfile` that sets up a NodeJS environment,
adds the NodeJS dependencies, then adds the source code.

```dockerfile
FROM node:9-alpine
WORKDIR '/var/www/app'
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
and re-build correctly every time a file changes.

## Sample Project With `fast_build`

We usually recommend people start with `docker_build` just to make sure everything works.

When you're ready to optimize your local workflow to be even faster,
that's when you want to try fast_build. Let's look at the
same project as above.

First, we want to remove all the lines from the Dockerfile that add source code. Now our Dockerfile is:

```dockerfile
FROM node:9-alpine
WORKDIR '/var/www/app'
```

Now, we put those lines for installing dependencies and adding source code into our Tiltfile:

```python
docker_compose('docker-compose.yml')

img = fast_build(
  'tilt.dev/express-redis-app',
  'Dockerfile',
  'node server.js')

img.add('.', '/var/www/app')

img.run('npm install', trigger='package.json')
```

This tells Tilt how to copy files to the container.

Now, when we run `tilt up` and update a file, Tilt will update the container in-place. You should
see output that looks like this:

```
──┤ Rebuilding: app ├────────────────────────────────────────────
  → Updating container…
express-redis-docker_app_1 exited with code 137
  → Container updated!
app_1    | 2019-03-13T17:15:25.742414920Z Server listening on port 3000
```

For more details on Tilt's image-building strategies, see the [fast build
documentation](fast_build.html) or the [api reference](api.html).

To run this app yourself, check out the [git repo](https://github.com/windmilleng/express-redis-docker).

## Debugging

Tilt uses Docker Compose to run your services, so you can also use `docker-compose` to examine state outside Tilt.

## Troubleshooting

Our Docker Compose support is not as widely used as Tilt's Kubernetes support.

You may hit more/different bugs, which we want to fix -- please file issues or tell us in Slack.
