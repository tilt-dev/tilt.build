---
title: Frontend Microservices with Hot Reloading
layout: docs
---

It’s easy for front end developers to feel left behind in the transition towards microservices, containers and Kubernetes. Front end development tools, like TypeScript, hot reloading and chrome devtools are fantastic first-in-class experiences. However these tools are often broken or hard to setup in a microservices development environment. Many front end developers choose to develop outside of a container as a result.

Tilt enables you to do frontend development with microservices development in a consistent, shareable and **fast** way. Let’s demonstrate this by walking through how to set up a standalone Tiltfile for a frontend service.

_Note: before diving in to this doc you should brush up on Tilt’s Getting Started Guide, namely the [tutorial](tutorial.html). This guide also assumes that you already have a Docker image that runs your frontend service, and a set of Kubernetes objects that deploys that service._

## Tiltfile Walkthrough

This Tiltfile is going to start out looking like any other. We’re first going to grab the YAML that defines the Kubernetes service.

```python
k8s_yaml('serve.yaml')
```

Now we need to tell Tilt about the Docker image that is used in the provided Kubernetes YAML. But rather than use a standard `docker_build` we’re going to use `fast_build` to provide the lightning fast reload times that frontend developers have come to expect.

```python
img = fast_build('gcr.io/windmill-public-containers/docs-site',
                 'docs.dockerfile',
                 'bundle exec jekyll serve --config _config.yml,_config-dev.yml')
img.add(repo.path('src'), '/src/')
img.add(repo.path('docs'), '/docs/')
img.run('bundle update')
```

If we start using this Tiltfile we’ll notice one annoying thing: every time we change any file in our service we run a costly, slow `bundle up`. Each change is still taking minutes. That’s no good. Luckily Tilt provides a way to only run a command when _certain_ files change. Introducing run triggers:

```python
img.run('bundle update', trigger=['src/Gemfile', 'src/Gemfile.lock', 'docs/Gemfile', 'docs/Gemfile.lock'])
```

Much better! With this change updates only take seconds, not minutes. Now we only run `yarn install` when either the `package.json` or the `yarn.lock` files change. But it still takes a couple seconds because we’re restarting the container every time _anything_ changes. We don’t need to do that for this service: new changes are picked up automatically as they change thanks to the magic of JavaScript. Restarting the container is a waste of time. Luckily Tilt provides us with a way to prevent that.

```python
img.hot_reload()
```

Now we’re cruising! Updates that don't require a `bundle update` zoom by in less than a second.

## Further Reading
* The full [example Tiltfile](https://github.com/windmilleng/tilt.build/blob/master/Tiltfile) featured in this guide
* [Optimizing a Tiltfile](fast_build.html)
