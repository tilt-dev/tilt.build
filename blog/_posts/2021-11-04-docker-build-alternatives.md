---
slug: "docker-build-alternatives"
date: 2021-11-12
author: nick
layout: blog
title: "Three Image Builders to Try While You're Waiting on 'docker build' to Finish"
image: "/assets/images/docker-build-alternatives/containers.jpg"
subtitle: "A guide to Tilt extensions that build images differently"
description: "A guide to Tilt extensions that build images differently"
tags:
  - docker
  - images
  - extensions
---

Two things can be true at the same time:

- If you don't want to worry about containers, Docker is a great one-stop-shop
  for building, moving, storing, and running container images.

- Container nerds get frustrated with this, because bundling all these things
  together means you often get a slow tool that isn't particularly
  well-optimized for what you're doing.

Jason Hall recently tweeted about this, then wrote [a great blog
post](https://github.com/ImJasonH/ImJasonH/tree/main/articles/moving-and-building-images)
expanding on it.

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">You don&#39;t need `docker build` to build a container image, and you don&#39;t need to `docker pull / tag / push` to move one around. In a lot of cases it&#39;s actively slowing you down, or making you less secure.</p>&mdash; Jason is no longer spooky (@ImJasonH) <a href="https://twitter.com/ImJasonH/status/1446624521507819521?ref_src=twsrc%5Etfw">October 8, 2021</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

Teams using Tilt often ask us: if my Docker build is getting slow, how can Tilt help me make it faster?

Fortunately, Tilt lets you swap out and experiment with different image builders
in dev. And you can package up those experiments as
[extensions](https://github.com/tilt-dev/tilt-extensions). The Tilt community
frequently adds new types of image builders.

In this post, I want to brag about three very different types of image builders that exist today:

- `kubectl_build`,

- `ko`, and

- `pack`

We'll talk about why you'd want to use them, how to swap them out, and the pros/cons of each!

If you just want to see the code, it's here: [https://github.com/tilt-dev/tilt-example-builders](https://github.com/tilt-dev/tilt-example-builders).

## Kubectl Build

If you're perfectly happy with your Dockerfile, but just want to move Docker
builds off your laptop, [`kubectl
build`](https://github.com/vmware-tanzu/buildkit-cli-for-kubectl#getting-started)
is for you.

It's a drop-in replacement for `docker build`.

When you run `kubectl build`, the CLI:

- Deploys a Docker build server to your Kubernetes cluster.

- Sends your Dockerfile and source code to the build server.

- Runs the build and pushes to a registry.

A few months ago, [Gaëtan Lehmann](https://github.com/glehmann) added an
extension for Tilt that lets you use `kubectl build` for image-building.

If you have this Tiltfile:

```python
docker_build(
  'example-python-image', 
  '.', 
  build_args={'flask_env': 'development'},
  live_update=[
    sync('.', '/app'),
  ])
```

You can replace it with:

```python
load('ext://kubectl_build', 'kubectl_build')
kubectl_build(
  'example-python-image', 
  '.', 
  build_args={'flask_env': 'development'},
  live_update=[
    sync('.', '/app'),
  ])
```

The main difference is that you will now see a buildkit server in your cluster:

```shell
$ kubectl get deployment
NAME             READY   UP-TO-DATE   AVAILABLE   AGE
buildkit         1/1     1            1           70m
example-python   1/1     1            1           7s
```

This can be nice if you have a powerful cluster and a 13" laptop!

Read the full docs on the `kubectl_build` extension [here](https://github.com/tilt-dev/tilt-extensions/tree/master/kubectl_build).

## Ko

Maybe you're not happy with your Dockerfile.

The Dockerfile view of the world is: to build an image, run some commands in a container,
then save the results of those commands.

The Ko view is: an image is a tarball. If you have a Mac, why do you need a
Linux VM to run a container if you want a tarball? You already have good local tools
for making tarballs.

[Ko](https://github.com/google/ko#install) is an image builder aimed at Go
apps. Go apps are particularly ill-suited for `docker build`. The Go toolchain is
well-optimized to run locally and builds a single binary. Ko builds your Go app
locally, then packs it into an image. No build containers or VMs needed!

A while back, I wrote a small extension that lets you use `ko` in Tilt. Here's what it looks like:

```
load('ext://ko', 'ko_build')

ko_build(
  'example-go-image',
  './',
  deps=['.']
)
```

The upside of `ko` is that it's super simple to get started.

The downside is that if you want any features that can't be expressed in a
static Go binary, you'll need to configure `ko` to include them.  This includes:
extra files in the container filesystem, dynamic C libraries, or hot-reload.
For example, this [example
project](https://github.com/tilt-dev/tilt-example-builders/tree/main/ko) uses
the `kodata` directory and `KO_DATA_PATH` env variable to load HTML templates.

Read the full docs on the `ko` extension
[here](https://github.com/tilt-dev/tilt-extensions/tree/master/ko).

## Pack

[`pack`](https://buildpacks.io/docs/tools/pack/) is also addressing people who
are not happy maintaining Dockerfiles.

But where Ko's philosophy states that you don't need a container to build an
image, Buildpack takes the viewpoint that you need MORE containers.

Joking! `pack`'s real philsophy: you shouldn't have to worry about low-level
details of how images are assembled. You should have bigger building blocks and
let your builder decide how to quickly combine them.

With `pack`, there's a stronger separation between the container you use
to build an image and the container you end up running. The container images you use
to build stuff are called buildpacks.

Separating these out has some big advantages!

- You can stack buildpacks to mix in the features you want (like hot-reload tools).

- The buildpack keeps out lots of junk you don't want in the final image (like compilers).

The `pack` extension was one of the first Tilt extensions! [Gareth
Rushgrove](https://github.com/garethr) added it when we were still experimenting
with the extension system.

Since then, we worked closely with [Daniel
Mikusa](https://github.com/dmikusa-pivotal) of the buildpacks team to make it
even better.

Here's what it looks like in a Tiltfile:

```python
pack(
  'example-python-image', 
  '.',
  buildpacks=[
    'gcr.io/paketo-buildpacks/python',
    'gcr.io/paketo-buildpacks/environment-variables',
  ],
  env_vars=['BPE_FLASK_ENV=development'],
  live_update=[
    sync('.', '/workspace'),
  ])
```

In this example, we're using two buildpacks: a `python` buildpack that sets up a
Python image, and a `environment-variables` buildpack that sets
`FLASK_ENV=development` to get live-reloading (Flask is the python framework
that does the live-reload.)

Read the full docs on the `pack` extension
[here](https://github.com/tilt-dev/tilt-extensions/tree/master/pack).

### Fun aside: Future Buildpack Work

The layering approach to adding new functionality is getting a lot of excitement
right now from container nerds.

For security nerds, you can better track where source files come from and attach
[SBOMs](https://en.wikipedia.org/wiki/Software_bill_of_materials) (which are way beyond the scope of this post, but are fun to say out
load.)

One of the big reasons Tilters are excited about buildpacks is that there's a
lot of configuration in your Tiltfile that would be simpler if it was in the
buildpack.  Daniel has been working on an
[RFC](https://github.com/paketo-buildpacks/rfcs/issues/116) to add live-reload
behavior to each buildpack.

More medium-term, we believe that buildpacks should be able to auto-detect
live-update `sync` rules that Tilt can read, so you don't need to keep them
up-to-date in your Tiltfile.

## Testing Out a New Image Builder

I hope this guide gave you a good tour of different image builders and how to
use them with Tilt. You can see examples of all these image builders in the
[`tilt-example-builders`](https://github.com/tilt-dev/tilt-example-builders)
repo.

There are more image builders in the world that I didn't cover! I like this post
Jérôme Petazzoni wrote last year about a few more, including the image builders
in Nix and Bazel:

[https://jpetazzo.github.io/2020/04/01/quest-minimal-docker-images-part-3/](https://jpetazzo.github.io/2020/04/01/quest-minimal-docker-images-part-3/)

If you want to try out a new image builder today, you don't have to switch at
once.  The [Tiltfile config API](https://docs.tilt.dev/tiltfile_config.html)
lets you add custom flags to `tilt up`, so that different users on your team can
try out different image builders.

`docker build` is a good general-purpose builder, but depending on what you're
working on, there may be a faster and easier image builder out there for you!
