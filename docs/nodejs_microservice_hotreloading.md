---
title: Node.js Microservice with Hot Reloading
layout: docs
---

It’s easy for frontend developers to feel left behind in the transition towards microservices, containers and Kubernetes. Frontend development tools, like TypeScript, hot reloading and chrome devtools are fantastic first-in-class experiences. However these tools are often broken or hard to setup in a microservices development environment. Many frontend developers choose to develop outside of a container as a result.

Tilt enables you to do frontend development with microservices development in a consistent, shareable and **fast** way. Let’s demonstrate this by walking through how to set up a standalone Tiltfile for a frontend service.

_Note: before diving in to this guide you should brush up on Tilt’s Getting Started Guide, namely the [tutorial](tutorial.html). This guide also assumes that you already have a Docker image that runs your frontend service, and a set of Kubernetes objects that deploys that service._

## The Node Service

The [node service](https://github.com/windmilleng/tilt-frontend-demo) we'll be setting up on Tilt was created using [create-react-app](https://github.com/facebook/create-react-app). The [start script](https://github.com/windmilleng/tilt-frontend-demo/blob/master/scripts/start.js) uses [`webpack-dev-server`](https://github.com/webpack/webpack-dev-server) to provide live reloading.

## Tiltfile Walkthrough

This Tiltfile is going to start out looking like any other. We’re first going to grab the YAML that defines the Kubernetes service.

```python
k8s_yaml('serve.yaml')
```

Next we tell Tilt about how to build the Docker image. We also use [`live_update`](live_update_tutorial.html) to provide the lightning-fast reload times that frontend developers expect.
```python
docker_build('tilt-frontend-demo', '.',
  live_update=[
    # Map the local source code into the container under /src
    sync('.', '/src'),
  ])
```

This is fast, but has a bug: when you change `package.json`, the dependencies don't get updated. Let's use the fall back feature of Live Update to fix that:

```python
docker_build('tilt-frontend-demo', '.',
  live_update=[
    # when package.json changes, we need to do a full build
    fall_back_on(['package.json', 'package-lock.json']),
    # Map the local source code into the container under /src
    sync('.', '/src'),
  ]
)
```


Now we’re cruising! Updates that don't require a `npm install` zoom by in less than a second.

## Further Reading
* The full [example Tiltfile](https://github.com/windmilleng/tilt-frontend-demo/blob/master/Tiltfile) featured in this guide
* [Faster Development with Live Update (Tutorial)](live_update_tutorial.html)
