---
title: Building on a Base Image
layout: docs
---

When you start adding multiple services to your app, it's easiest
to just copy a new Dockerfile for each service and tweak a few parameters.

Once you have a few services, that duplication can start to feel messy.
Sometimes you update one Dockerfile but forget to update the others.
Building all the services is slow.

A common pattern is to create a common base image with the dependencies for
multiple services.

With Tilt, you can describe when to re-build each image in the dependency graph.

## Building a `node_modules` Base Image

Let's look at an example. We want to create a NodeJS server with two Docker images:

1. A Docker image that contains the node_module dependencies.

2. A Docker image that contains the server source code.

First we write a Dockerfile for the base node_modules image. We'll call this image
`local.tilt.dev/nodejs-express-deps`.

```dockerfile
# local.tilt.dev/nodejs-express-deps

FROM node:9-alpine
WORKDIR /src
ADD package.json package.json
RUN npm install
```

Next we'll create a Dockerfile for the app image. This is just an empty base image to build on.

```dockerfile
# local.tilt.dev/nodejs-express-app

FROM local.tilt.dev/nodejs-express-deps
```

Lastly, we'll add a Tiltfile that knows how to build both images.

```python
# Configure image build for our external dependencies.
docker_build(
  'local.tilt.dev/nodejs-express-deps',
  './package',
  dockerfile='deps.dockerfile')

# Configure build to copy our source code.
app = fast_build(
  'local.tilt.dev/nodejs-express-app',
  'app.dockerfile',
  'node server.js')
app.add('.', '/src')

# Set up the Kubernetes resources.
k8s_yaml('app.yml')
```

Notice that the Docker build for `nodejs-express-deps` uses the subdirectory `./package`.
Tilt will only rebuild this image when files under `./package` change.

When you run `tilt up`, Tilt will build both images, and make sure that the first image
gets injected into the second image.

```
STEP 1/3 — Building Dockerfile: [local.tilt.dev/nodejs-express-deps]
Building Dockerfile:
  # local.tilt.dev/nodejs-express-deps

  FROM node:9-alpine
  WORKDIR /src
  ADD package.json package.json
  RUN npm install

...

STEP 2/3 — Building from scratch: [local.tilt.dev/nodejs-express-app]
Building Dockerfile:
  FROM local.tilt.dev/nodejs-express-deps:tilt-af085becbf6ef0ef

  ADD . /
  ENTRYPOINT node server.js
```

If you make a change to server.js, Tilt knows it can skip the first image build
and copy files to the container in-place. You will see output that looks like this:


```shell
2 changed: [.#server.js server.js]

──┤ Rebuilding: nodejs-express-app ├──
  → Updating container…
  → Container updated!
nodejs-expr…┊ Server listening on port 3000
```

## Try it Yourself

All the source code for this example is [on GitHub](https://github.com/windmilleng/nodejs-express-k8s).

Try running it yourself with Tilt. Make changes to both `package.json` and `server.js`
and see how Tilt rebuilds only what has changed.
