---
slug: local-resource
date: 2019-11-13
author: maia
layout: blog
title: "Local Resource"
subtitle: "tbd"
image: "tbd.jpg"
image_caption: "tbd"
tags:
  - docker
  - kubernetes
  - tilt
  - dev tools
keywords:
  - bash
  - local
  - kubernetes
  - docker
  - tilt
---
Once upon a time, you might have written the following line in your Tiltfile:

```
local('go generate ./greeter_server')
watch_file('helloworld/helloworld.proto')
```

This would regenerate your protobufs every time you change `helloworld.proto`---but it would also re-execute your entire Tiltfile. More annoyingly, it would also regenerate your protobufs whenever your Tiltfile re-executed, whether they needed regenerating or not. This solution was hacky, resulted in commands running at unexpected times, and generally made things slow and annoying.

The alternative was running `go generate ./greeter_server` by hand whenever you changed your `.proto` file. Your Tiltfile execution was faster, your proto generation was predictable, but you had to remember to run the command when you changed a certain file, which shook you out of your workflow (assuming that you remembered at all, and didn't spend multiple minutes wondering why something on your server wasn't working).

If you're one of the many Tilt users who has bootstrapped `local` to do work that you don't _actually_ want to do every time your Tiltfile reloads, OR if you're annoyed at having to tab out of Tilt to run bits and pieces of your workflow from terminal, we've got a new feature that we think might help. It's called Local Resource, and here's how it works. (You can also play around with it in [this example repo](https://github.com/windmilleng/local_resource_example).)


## What is a "Local Resource"?

The first thing to understand is that every item that shows up in your sidebar is a _resource_---a unit of work managed by Tilt.

[[image? sidebar w/ labels]]

In the lifetime of Tilt so far, a resource has represented a service you're deploying, often in the form of image build + k8s deploy instructions (or in some cases, just k8s deploy instructions). But there are other kinds of resource now! In particular, a local resource represents a unit of work that is run _on your local machine_ rather than in your cluster. But like any other resource, a local resource runs in response to its dependencies (files on disk) changing, and prints logs to the UI, and surfaces alerts if anything goes wrong. The only difference is the work being done: where the work of a Kubernetes resource might be `docker build && kubectl apply`, a local resource runs a user-specified command against the local filesystem. You can specify a local resource in your Tiltfile with the following syntax:

```python
local_resource('yarn', cmd='yarn install', deps=['package.json'])
```

See also: [`local_resource` API spec](api.html#api.local_resource).

## Run commands locally on file change
Most uses of Tilt focus on easily and quickly seeing your code running in the cloud.
For some kinds of development, however, you might want to harness
Tilt's responsiveness to file changes to run commands _locally_ instead. Here are two
two general cases where running commands locally and responsively might come in handy:
- *file changes or other artifacts that you want on your local machine (e.g. for
git commit)*. For instance: when `package.json` changes, run `yarn install`
(because you want the resulting `yarn.lock` file to exist on your local computer
so that you can commit it to git).

```python
local_resource('yarn', cmd='yarn install', deps=['package.json'])
```
- *tooling that you have locally but don't want to put on your container images*.
For instance: rather than pulling/pushing big container images with the Go compiler,
you'd rather compile your binary locally, and pull that compiled binary into your Docker image
(or directly into your running container via Live Update).

```python
local_resource('compile-binary',
    cmd='go build -i -o ./bin/the-binary github.com/my-org/my-app/',
    deps='./my-app'
)
docker_build('gcr.io/my-org/my-app', context='./bin')
```

(Of course, the command you run doesn't have to be on that (only) affects your
local filesystem. It might, for instance, be a script that is _invoked locally_
but runs against your k8s cluster.)

## Local Resource + Live Update = <3

Local Resource and Live Update are two great tastes that taste great together.
A useful pattern is to have a local resource which creates an artifact
that is then picked up by a Live Update and synced to a running container.
For example, here's how you might use this combination to generate protobufs:
```python
# whenever `helloworld.proto` changes, generate Python protobufs
local_resource('proto',
    cmd='protoc --proto_path=src --python_out=build/gen',
    deps=['helloworld.proto']
)

# define your hello-world resource: k8s yaml + a Docker build
k8s_yaml('hello-world.yaml')
docker_build('hello-world', '.',
    ignore='helloworld.proto',  # don't step on the local resource's toes
    live_update=[ sync('.', '/app') ]
)
```

Note that the `docker_build` call specifies `ignore='helloworld.proto'`. This is
because we DON'T want an edit to that proto file to _directly_ kick off an update to
our Docker image (in this case, a Live Update). Rather, an edit to `helloworld.proto`
triggers the local resource to generate protobufs; when these protobufs appear on disk,
they register as file changes and trigger a Live Update to the `hello-world` resource,
i.e. they get `sync`'d to the container where `hello-world` is running.

To see this pattern in action, check out [this example repo](https://github.com/windmilleng/local_resource_example).

# Run occasional workflows (locally or against your cluster)

There's another class of workflow that local resource can help with; commands that
are a part of your development flow, but that you run only occasionally. This might
be a task like "ensure GKE user 'foo' exists" or "refresh my credentials" or even
"blow away my database".

You can trigger a local resource at will with the "force update" button:

!["force update" button](assets/img/force-update-button.png)

By default, a local resource will run on startup. To disable this behavior, put the
resource in `TRIGGER_MODE_MANUAL` and specify `auto_init=False`:
```python
local_resource('reset-db', cmd='reset_db.sh',
    trigger_mode=TRIGGER_MODE_MANUAL, auto_init=False
)
```

(`auto_init=False` is currently only compatible with `TRIGGER_MODE_MANUAL`. If
you'd like a local resource that runs automatically in response to file changes
but does NOT run on `tilt up`, [let us know](https://tilt.dev/contact).)

Note that you can mix and match manual and automatic runs as you like. For instance,
you might have a `seed-db` local resource. Usually, you run it manually whenever
you need to put new data into your DB, but want to run automatically if you touch
the `seed_db.sh` script:
```python
local_resource('reset-db',
    cmd='reset_db.sh',
    deps=['seed_db.sh'],
)
```

