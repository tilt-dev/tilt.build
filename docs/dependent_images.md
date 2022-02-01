---
title: Getting Started with Image Builds
description: "How to go from building one image to building multiple images"
layout: docs
sidebar: guides
---

This is a brief intro to automatically build and deploy images
to a local dev environment.

We'll start with a single image.

## Going from `docker build` to `docker_build`

On the command-line, an image build looks like this:

```shell
docker build -t my-image .
```

`my-image` is the image name. `.` is the directory of files that you're including in the image.

To make this part of your dev environment, add this to your Tiltfile:

```python
docker_build('my-image', '.')
```

`.` is still the directory of files you're including. Tilt will automatically watch them for changes.

`my-image` is an image selector. Tilt will scan all your workload manifests for
images, and match any object that contains the image name `my-image` (regardless
of tag).

This creates a dependency between your deploy YAML and `my-image`. Every time 
the image rebuilds, Tilt knows it may need to restart your containers.

- If the image hasn't changed, the containers won't restart.

- If the image has changed, the containers should always restart with a fresh image.

(Note that this is different than what usually happens in prod, where you want
more control over the gradual rollout of a new image. Tilt has some tricks to
make this work well in dev. The implementation details are discussed a bit in
[our custom_build guide](custom_build.html).)

### Advanced Image Matching

`my-image` is a matcher that ignores tags.

Some teams have one mega image with all their services, and use tags to
denote which service to run.

```python
docker_build('my-mega-image:service-a', '.', entrypoint='/service-a')
docker_build('my-mega-image:service-b', '.', entrypoint='/service-b')
```

If you specify a tag, Tilt will only match deploy objects with that exact tag in
their image name.

If you're trying to inject images into [Custom
Resources](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/)
(in other words, if you're not using built-in Kubernetes objects like Deployment and Job),
check out our [custom resource guide](custom_resource.html).

## Multiple Images

When you start adding multiple services to your app, it's easiest
to just copy a new Dockerfile for each service and tweak a few parameters.

Once you have a few services, you may find that duplication can start to feel messy.
Sometimes you update one Dockerfile but forget to update the others.
Building all the services is slow.

A common pattern is to create a common base image with the dependencies for
multiple services.

So let's set up a dependency tree of `docker_build`s that build on each other.

### Building a `node_modules` Base Image

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
             
# Configure the Kubernetes deploys.
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

### Adding Live Updates

Once you've got the two image builds working, you can add a
live update rule to sync files into your app. This is much faster
than building the app image each time.

In this example, we'll use a `sync` step to copy the files. 

Then we'll add a custom `entrypoint` that runs our server with `nodemon`, which does the reload.

Here's what it looks like:

```

docker_build('nodejs-express-app-image',
             '.',
             dockerfile='app.dockerfile',
             live_update=[
               sync('.', '/var/www/app')
             ],
             entrypoint='yarn run nodemon /var/www/app/server.js')
```

Every app needs to specify both a sync step and a reload step. But reload steps
tend to be specific to the programming language and framework you're using. Some
frameworks even handle it automatically. This example uses an entrypoint with
`nodemon`, but the reload step for your project will probably look
different. For more examples, see the language-specific example projects or [the
live update refrence](live_update_reference.html).

Note that live update steps should always be attached to the deployed image,
never the base image. Tilt's live update system matches the image in the container,
so needs to be attached to the deployed image to figure out which container
to update.

## Example Code

- An example of a base image for package.json dependencies: [tilt-example-base-image](https://github.com/tilt-dev/tilt-example-base-image)

- An integration test that uses 2 levels of base images: [live_update_base_image](https://github.com/tilt-dev/tilt/blob/master/integration/live_update_base_image/Tiltfile)

- An integration test that uses tag-based image matching: [imagetags](https://github.com/tilt-dev/tilt/blob/master/integration/imagetags/Tiltfile)
