---
slug: "dev-env-libraries"
date: 2022-02-24
author: nick
layout: blog
title: "Defining Your Own Library of Dev Env Patterns"
subtitle: "Announcing Updates to the Tilt Extensions API"
description: "Announcing Updates to the Tilt Extensions API"
image: "/assets/images/dev-env-libraries/cover.jpg"
image_caption: "The Shirlington Public Library during cherry blossom season."
tags:
  - extensions
  - dev environments
---

Tilt provides a few basic primitives for defining the local shell scripts, docker
builds, and Kubernetes pods in your dev environment.

But most teams have an opinionated way to build services! For example, you might have

- checks to make sure your laptop has the right tools,

- conventions for building images, 

- custom scripts for deploying objects, 

- custom buttons for debugging services!

As of v0.25, Tilt has a new API for managing your own repo of Tiltfile snippets,
so that you can easily set some standards across multiple repos or multiple
projects.

Let's take a quick tour of the extension system and how it works:

## Using an Extension

Let's look at the `hello_world` extension.

The source code for this extension is
[here](https://github.com/tilt-dev/tilt-extensions/blob/master/hello_world/Tiltfile)
and has exactly two (2) lines of code:

```python
def hi():
  print("Hello world!")
```

It exports one function, `hi`, that simply prints "Hello world!".

Let's load this extension into our project:

```python
load('ext://hello_world', 'hi')
hi()
```

When you run `tilt ci` in this project, you'll see output like:

```shell
Initial Build • (Tiltfile)
Loading Tiltfile at: /home/nick/src/scratch/Tiltfile
Hello world!
Successfully loaded Tiltfile (1.990905ms)
ERROR: No resources found. Check out https://docs.tilt.dev/tutorial.html to get started!
```

Tilt printed the message! Tilt also printed an error because it doesn't make any sense
to have a dev environment that only prints "Hello world!". 🙃

## Managing Your Own Extension Repo

The new `v1alpha1.extension_repo` API[^1] lets you change the behavior of `load()`.


Let's start with the `hello_world` example above:

```python
load('ext://hello_world', 'hi')
```

This is a shorthand with nice defaults. You could write it like this:

```python
v1alpha1.extension_repo(name='default', url='https://github.com/tilt-dev/tilt-extensions')
v1alpha1.extension(name='hello_world', repo_name='default', repo_path='hello_world')
load('ext://hello_world', 'hi')
```

These two snippets are equivalent. The second snippet explicitly spells out that
there's an extension repo called `default` at
`https://github.com/tilt-dev/tilt-extensions`.  The extension `hello_world`
gets loaded from the path `hello_world` in the `default` repo.


This API lets you fork the shared `tilt-extensions` repo, and instruct `load()`
to pull from there:

```python
v1alpha1.extension_repo(name='default', url='https://github.com/my-org/tilt-extensions')
load('ext://hello_world', 'hi')
```

Alternatively, you can add new extension repos alongside the default one.

```python
v1alpha1.extension_repo(name='my-repo', url='https://github.com/my-org/tilt-extensions')
v1alpha1.extension(name='hello_world', repo_name='my-repo', repo_path='hello_world')
load('ext://hello_world', 'hi')
```

Notice that in the above, we define `hello_world` to pull its source from
`my-repo` rather than `default`.

If your extension repo is private, you'll need to configure git to authenticate
against the private repo in the background. A common pattern (borrowed from [the
Go FAQ](https://go.dev/doc/faq#git_https)) is to setup your Git repo for SSH and
add these lines to your `~/.gitconfig`:

```
[url "ssh://git@github.com/"]
	insteadOf = https://github.com/
```

## Sharing Extensions with the Community

If you have an extension that you think would be generally useful, we love to
see people contribute them back to the main repo!

For more detail on the new extension system, check out:

- Our [documentation](https://docs.tilt.dev/extensions.html) on how to load
  shared code and develop an extension locally.

- Our [contributing extensions](contribute_extension.html) guide
  for to submit general-purpose extensions for common tools.

[^1]: The `v1alpha1` part of the API indicates that this is an object in the
      Tilt API server, matching the Kubernetes API conventions. You can use
      `tilt get extension` or `tilt get extensionrepo` as a CLI to see
      information about the extensions currently in your dev env.
