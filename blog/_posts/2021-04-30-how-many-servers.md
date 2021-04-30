---
slug: "how-many-servers"
date: 2021-04-30
author: nick
layout: blog
title: "Nobody Knows How Many Servers They Need to Run Their App"
image: "/assets/images/how-many-servers/manifestacion.jpg"
image_caption: "An illustation of servers in a typical app in 2021. Manifestacion by José Clemente Orozco, via <a href='https://artsandculture.google.com/asset/manifestacion-jose-clemente-orozco/3AE79k-2WjZczQ'>Google Arts &amp; Culture</a>"
tags:
  - api
  - microservices
---

Tilt v0.20.0 has a weird new feature: the Tilt apiserver.

Our end goal is for Tilt to expose its internal status as an API, and
provide tooling on how to interact with that status to do stuff.

This is a bit abstract. I'm not sure I have a pithy way to summarize it.  But I
do have a verbose way to summarize it!

## Services Services Everywhere and All the APIs Did Shrink

Modern apps are made of too many services. They’re everywhere and in constant
communication.

You probably don't even know how many services you're running when you're doing
development.

I've been doing development for a long time. I was thinking back to all the
times I suddenly found a "surprise" service.

For example:

- [Watchman](https://facebook.github.io/watchman/), a tool to trigger events
  when files change, runs a long-lived server listening on [a
  socket](https://facebook.github.io/watchman/docs/socket-interface.html).
  
- [Bazel](https://bazel.build), a multi-language build system, runs
  a long-lived server with [a client that sends it build jobs](https://docs.bazel.build/versions/master/guide.html#client/server).
  
- [tiny-lr](https://www.npmjs.com/package/tiny-lr), runs a notification service
  that tells browsers when they need to reload.
  
There's a lot of jargon thrown around to try to taxonimize the kinds and size of
services we have these days.  Monoliths. Microservices. Service-oriented
architectures. Functions as a service.

But the size of the services isn't really what bothers me.

It's how we compose services.

## Service Composition 

Unix has a lot of commandline tools. And you can pipe them together! This
lets you combine tools in novel ways.

We never really figured out how to compose services.

Even the servers I listed above speak wildly different protocols:

- Watchman listens on a domain socket for newline-delimited JSON (or binary BSER) that encodes commands.

- Bazel listens on localhost with GRPC.

- tiny-lr listens on localhost for GET/POST JSON and broadcasts changes with Websockets.

If we want to fit them together (e.g., run Bazel every time a file changes), the
best answer we have is to use commandline tools to chain them together.

Is there a better way? 

## How Kubernetes Composes Services

I think a lot about how we're seeing more systems that have to deal with
multiple servers and figure out how they fit together.

Even tools that don't want to be a server orchestration system
end up growing into one (*cough* webpack *cough*).

Kubernetes has a simple and genius idea for how to deal with this problem: you can compose servers by adding more servers!

More specifically, Kubernetes gives you:

- An HTTP API for proposing "here's what servers should run."

- An HTTP API for asking "what are my servers doing now?"

- A control loop to robustly figure out these questions.

- A RESTful simplicity and consistency so that you can add new types of objects and get all the API / CLI infrastructure for free.

This is a brilliant way to build systems! And we can use it to compose servers.

## A Small Taste

As of Tilt v0.20.0, Tilt runs a Kubernetes API server to answer questions about
what's running in the dev environment.

If I have Tilt running in one terminal, I can, in another terminal, run:

```
$ tilt get session
NAME       CREATED AT
Tiltfile   2021-04-30T18:54:31Z
```

If I want more detail, I can run:

```
$ tilt get session Tiltfile -o yaml
apiVersion: tilt.dev/v1alpha1
kind: Session
metadata:
  creationTimestamp: "2021-04-30T18:54:31Z"
  name: Tiltfile
  resourceVersion: "5"
  uid: 811645a0-d246-4ed7-ac10-23f6ac770676
spec:
  exitCondition: manual
  tiltfilePath: /home/nick/src/tilt-example-html/0-base/Tiltfile
status:
  done: false
  pid: 209244
  startTime: "2021-04-30T18:54:31.049171Z"
  targets:
  - name: example-html:runtime
    resources:
    - example-html
    state:
      active:
        ready: true
        startTime: "2021-04-27T23:55:47.000000Z"
    type: server
  - name: example-html:update
    resources:
    - example-html
    state:
      terminated:
        finishTime: "2021-04-30T18:54:31.383351Z"
        startTime: "2021-04-30T18:54:31.123758Z"
    type: job
  - name: tiltfile:update
    resources:
    - (Tiltfile)
    state:
      terminated:
        finishTime: "2021-04-30T18:54:31.121838Z"
        startTime: "2021-04-30T18:54:31.108614Z"
    type: job
```

Now we know exactly how many services we're running in dev! This particular dev
environment has 3: a job that evaluates the Tiltfile, a job that builds an
image, and a server that runs in Kubernetes.

## What This Means

This probably isn't too impressive yet. I can read status. So what?

But the real power is when I have multiple objects, and have a way to chain them
together in novel ways. But I need to go hack those APIs together tomorrow, so
you'll have to wait until the next post!



