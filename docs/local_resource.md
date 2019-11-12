---
title: Run Local and/or Occasional Workflows with Local Resource
layout: docs
---
Each entry in your Tilt sidebar is a **resource**---a unit of work managed by Tilt. (Until
this point, most Tilt resources have been a some combination of image instructions and Kubernetes
YAML). A **local resource** works like any other resource in your sidebar; it represents a
unit of work, and executes either automatically in response to file changes, or
[manually](https://docs.tilt.dev/manual_update_control.html) on signal from the user.
For your resource `MyGreatService`, when one of its file dependencies changes, its work
is to build a Docker image and deploy some k8s yaml; for a local resource, it's
to execute an arbitrary command on your local filesystem.

# Run commands locally on file change
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
    cmd='go build -i -o ./bin/the-binary github.com/my-org/my-app/', deps='./my-app')
docker_build('gcr.io/my-org/my-app', context='./bin')
```

See also: [`local_resource` API spec](api.html#api.local_resource).

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
