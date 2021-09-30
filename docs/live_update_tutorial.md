---
title: Faster Development with Live Update (Tutorial)
description: "This tutorial looks at a `Tiltfile` with build optimizations. We explain what they do, and why you would want to use them."
layout: docs
sidebar: guides
---
This tutorial looks at a `Tiltfile` with build optimizations.
We explain what they do, and why you would want to use them.

##### (This is a tutorial that walks you through a sample project. If you're looking for technical specs and details, check out the [Live Update Reference](live_update_reference.html) docs.)

In the [Tutorial](/tutorial), we introduced the `docker_build()` function.
This function builds a Docker image. Tilt will watch the inputs to the
image, and do a fresh build every time the inputs change.

However, rebuilding your Docker image every time you change some code isn't super efficient, even if your caching is good. The efficiency is even worse if you're working with compiled languages, and even worse if you're pushing images into the cloud.

That's why Tilt has a feature called Live Update, to make your containerized
development lightning-fast.

## Let's Look At an Example
Let's look at an example app, [`random_number`](https://github.com/tilt-dev/random_number):

```
git clone https://github.com/tilt-dev/random_number
cd random_number
```

This "microservice" app consists of:
* `numbers`, a Python+Flask server which serves a random number
* `fe`, a Golang server frontend which hits `numbers` for a random number


The `Tiltfile` at the root of the repo contains this example:

```python
# Service: numbers
docker_build('random_number/numbers', 'numbers',
    live_update=[
        sync('./numbers', '/app'),
        run('cd /app && pip install -r requirements.txt',
            trigger='numbers/requirements.txt'),
    ]
)

# Service: fe
docker_build_with_restart('random_number/fe', 'fe',
    entrypoint='/go/bin/fe',
    live_update=[
        sync('./fe', '/go/src/github.com/tilt-dev/random_number/fe'),
        run('go install github.com/tilt-dev/random_number/fe'),
    ]
)
```

This looks similar to the `Tiltfile` in previous tutorials, but when we specify
how to build the image with `docker_build()`, we pass an additional argument,
`live_update`, containing a list of steps for how to update the running container.

### Service #1: `numbers` (Python + Flask)
Let's zoom in on the `live_update` configuration for the `numbers` service first:


```python
docker_build('random_number/numbers', 'numbers',
    live_update=[
        sync('./numbers', '/app'),

        # run `pip install` IF `requirements.txt` has changed
        run('cd /app && pip install -r requirements.txt',
            trigger='numbers/requirements.txt'),
    ]
)
```

These lines configure Tilt to, when possible, update containers running the image `random_number/numbers`
 _incrementally_ rather than doing a full build every time code changes. We'll step through it line by line.

* `sync('./numbers', '/app'),`

The `sync` method watches a file or directory on your local filesystem, and when it detects a change, copies the changed file(s) into your container at the specified path.

In this case, we map the directory `./numbers` (relative to the Tiltfile) into
the container filesystem at `/app`.

The normal `docker_build` behavior is to watch all files in the Docker build context (here, `./numbers`),
and any time one changes, rebuild the image and re-deploy it to Kubernetes. The `sync` here says that, if
the changed file matches `./numbers`, to instead do a `live_update`: Tilt will copy
the changed files into the container and execute any appropriate `run`
steps, without actually building or pushing a Docker image or performing a Kubernetes deploy.

* `run('cd /app && pip install -r requirements.txt', trigger='numbers/requirements.txt'),`

The `run` method runs shell commands inside your container.

This particular run step relies on a `trigger`: when this resource Live Updates, Tilt will
run this command in the container _if_ any changed files match the trigger (here,
`numbers/requirements.txt`). This specificity means that we'll only run `pip install` if
dependencies have actually changed.

### Service #2: `fe` (Golang)
Let's now look at the `live_update` configuration for the other service in this app, the frontend, which is written in Go:
```python
docker_build_with_restart('random_number/fe', 'fe',

    # command to run on container start/re-run on live update
    entrypoint='/go/bin/fe',

    live_update=[
        sync('./fe', '/go/src/github.com/tilt-dev/random_number/fe'),
        run('go install github.com/tilt-dev/random_number/fe'),
    ]
)
```
The eagle-eyed among you will notice that the function called here is slightly different: instead of `docker_build`, we call `docker_build_with_restart`. More on that in a moment; first let's go through the `live_update` steps one a time.

* `sync('./fe', '/go/src/github.com/tilt-dev/random_number/fe')`

As we saw in the configuration for `numbers`, this `sync` call maps a local directory to a path on the container. Any time a file on disk changes, if it matches the path `./fe`, Tilt will copy it to the designated path in the container.

* `run('go install github.com/tilt-dev/random_number/fe')`

Unlike the `run` step seen in `numbers`, this one lacks a `trigger`, which means that Tilt will run this command in the container _every time a Live Update happens_ (i.e., when a file matching a `sync` changes). In this example, every time Tilt syncs changed files to the container, it then recompiles the Go binary.

One of the major build optimizations here is that Tilt runs your command inside the existing
container, instead of building from scratch to create a fresh image. This is much closer to how
we normally run commands for local development. Real humans don't delete all their code and
re-clone it from GitHub every time we need to do a new build! Instead, we re-run the command in
the same directory. Modern tools then take advantage of local caches; Tilt runs commands with
the same approach, but inside a container.

* What about `docker_build_with_restart`?

This function is imported from
[the `restart_process` extension](https://github.com/tilt-dev/tilt-extensions/tree/restart_proc_custom_build/restart_process)
via a `load` call at the top of the Tiltfile:
```python
load('ext://restart_process', 'docker_build_with_restart')
```

(Extensions are open-source packaged functions that extend the capability Tilt;
[check out the docs](extensions.html) for more info.)

`docker_build_with_restart` works just like the `docker_build` call you're used to, except that at the end of every Live Update, it restarts your process--in this case, it runs the newly built Go
binary. Notice the extra argument `entrypoint` (in this example, `/go/bin/fe`): this is the command
that you want to run on container start and _re-run_ on Live Update.

For languages/frameworks like Node or Flask that have hot reloading (i.e., they can pick up code
changes without restarting the process), you don't need to restart your process. For instance, the
`numbers` app takes advantage of Flask's hot reloading, and thus doesn't need a `docker_build_with_restart` call.

## Further Reading
In this guide, we explored just a few of the functions we can use in a `Tiltfile`
to keep your build fast. For even more functions and tricks,
read the complete [Tiltfile API reference](api.html).

For more details on Live Update, see the [Live Update Reference Documentation](live_update_reference.html).

If you need more specifics on how to set up Live Update with your programming
language of choice, all our major example projects use Live Update:

<ul>
  {% for page in site.data.examples %}
    <li><a href="/{{page.href | escape}}">{{page.title | escape}}</a></li>
  {% endfor %}
</ul>
