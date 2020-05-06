---
slug: April-2020-commit-of-the-month
date: 2020-05-04
author: dmiller
layout: blog
title: "Using Pack and Buildpacks"
subtitle: "Commit of the Month: A Buildpack Extension"
image: /assets/images/april-2020-commit-of-the-month/featuredImage.jpg
image_caption: "Photo by Iris Aldeguer on <a href='https://www.flickr.com/photos/irisux/4372485391'>Flickr</a>."
image_type: "contain"
tags:
  - tilt
  - cotm
  - extensions
keywords:
  - tilt
  - pack
  - buildpack
---

In April we introduced [Tilt Extensions](https://docs.tilt.dev/extensions.html). Extensions are open-source packaged functions that extend the capability of Tilt, right inside your Tiltfile. Since releasing them we've seen several great extensions contributed by members of the community and we're highlighting one of them as April's Commit of the Month: [an extension to use pack and buildbacks to build container images](https://github.com/windmilleng/tilt-extensions/commit/e1d193e508ce8468800d0985ee4714aa65d78c87) by [Gareth Rushgrove](https://twitter.com/garethr)!

## What is a buildpack? What is `pack`?

From [the docs](https://buildpacks.io/docs/concepts/components/buildpack/): A buildpack is a unit of work that inspects your app source code and formulates a plan to build and run your application.

Typical buildpacks are a set of at least three files:

- `buildpack.toml` – provides metadata about your buildpack
- `bin/detect` – determines whether buildpack should be applied
- `bin/build` – executes buildpack logic

`pack` is a command line tool that takes your source code and invokes the appropriate buildpack(s) to create a Docker image, or deploy it straight in to the cloud of your choice.

## How does the Tilt pack extension work?

This extension makes the `pack` function available in your Tiltfile, which is used the same way as `docker_build` to allow Tilt
to automatically build a container image with a known name.

```python
load('ext://pack', 'pack')

pack('example-image')
k8s_yaml('kubernetes.yaml')
k8s_resource('example-deployment', port_forwards=8000)
```
_Example taken from the [extension README](https://github.com/windmilleng/tilt-extensions/blob/master/pack/README.md)_

It's implemented as a light wrapper around `custom_build`:

```python
def pack(name, path=".", builder="gcr.io/paketo-buildpacks/builder:base", **kwargs):
     custom_build(
         name,
         "pack build $EXPECTED_REF -p %s --builder %s" % (path, builder),
         [path],
         **kwargs
     )
```

Due to the use of `**kwargs` you can pass any `custom_build` parameter like so:

```python
pack('example-image', ignore=['.vim'])
```

We love this method of providing an easy abstraction to use something complex like `custom_build`, without losing access to the full power of `custom_build` if you need it.

## Have an idea for an extension?

Do you have an idea for an extension? We'd love to [chat about it](https://docs.tilt.dev/debug_faq.html#where-can-i-ask-questions) and help you [contribute it](https://docs.tilt.dev/contribute_extension.html) to the [Tilt Extensions Repository](https://github.com/windmilleng/tilt-extensions).
