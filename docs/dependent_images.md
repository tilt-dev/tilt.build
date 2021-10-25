---
title: Building on a Base Image
description: "With multiple services in your app, a common pattern is to create a common base image with common dependencies"
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
`nodejs-express-base-image`.

```dockerfile
# nodejs-express-base-image
# base.dockerfile

FROM node:16-alpine

# Default value; will be overridden by build_args, if passed
ARG node_env=production

ENV NODE_ENV $node_env

WORKDIR '/var/www/app'
ADD package.json package.json
RUN npm install
ENTRYPOINT node server.js
```

Next we'll create a Dockerfile for the app image. This is just an empty base image to build on.

```dockerfile
# nodejs-express-app-image
# app.dockerfile

FROM nodejs-express-base-image

WORKDIR '/var/www/app'

ADD . .
```

Lastly, we'll add a Tiltfile that knows how to build both images.

```python

# Set up the Kubernetes resources.
k8s_yaml('app.yml')

# Configure image build for our external dev dependencies.
docker_build('nodejs-express-base-image',
             './package',
             dockerfile='base.dockerfile',
             build_args={'node_env': 'development'})

# Configure build to copy our source code.
docker_build('nodejs-express-app-image',
             '.',
             dockerfile='app.dockerfile')
             
# Configure the Kuberentes deploys.
k8s_resource('nodejs-express-app', port_forwards=3000)
```

Notice that the Docker build for `nodejs-express-deps` uses the subdirectory `./package`.
Tilt will only rebuild this image when files under `./package` change.

When you run `tilt up`, Tilt will build both images, and make sure that the first image
gets injected into the second image.

```
STEP 1/5 — Building Dockerfile: [nodejs-express-base-image]
Building Dockerfile:
  FROM node:16-alpine
  
  # Default value; will be overridden by build_args, if passed
  ARG node_env=production
  
  ENV NODE_ENV $node_env
  
  WORKDIR '/var/www/app'
  ADD package.json package.json
  RUN npm install
  ENTRYPOINT node server.js

...

STEP 3/5 — Building Dockerfile: [nodejs-express-app-image]
Building Dockerfile:
  FROM localhost:5005/nodejs-express-base-image:tilt-19328501fd376562
  
  WORKDIR '/var/www/app'
  
  ADD . .


     Tarring context…
     Building image
     copy /context / [done: 44ms]
     [1/3] FROM localhost:5005/nodejs-express-base-image:tilt-19328501fd376562
     [2/3] WORKDIR /var/www/app [cached]
     [3/3] ADD . . [done: 18ms]
     exporting to image [done: 21ms]
```

If you make a change to server.js, Tilt knows it can skip the first image build
and just do the second.

## Adding Live Updates

Once you've got the two image builds working, you can add a
live update rule to sync files into your app. This is much faster
than building the app image each time.

Every live update needs two steps:

- A step to copy the files.

- A step to reload the files into the running server.

In this example, we use a `sync` step to copy the files. Then we add a custom
`entrypoint` that runs our server with `nodemon`, which does the reload.

Here's what it looks like:

```

docker_build('nodejs-express-app-image',
             '.',
             dockerfile='app.dockerfile',
             entrypoint='yarn run nodemon /var/www/app/server.js',
             live_update=[
               sync('.', '/var/www/app')
             ])
```


Note that live update steps should always be attached to the deployed image,
never the base image. Tilt's live update system matches the image in the container,
so needs to be attached to the deployed image to figure out which container
to update.

## Try it Yourself

All the source code for this example is [on
GitHub](https://github.com/tilt-dev/tilt-example-base-image).

Try running it yourself with Tilt. Make changes to both `package.json` and `server.js`
and see how Tilt rebuilds only what has changed.
