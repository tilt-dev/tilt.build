---
slug: "plug-and-play-extensions"
date: 2021-08-30
author: nick
layout: blog
title: "The Solution to Too Many Servers is More Servers"
subtitle: "Or: how to use Tilt reactive extensions and how to write your own"
description: "Or: how to use Tilt reactive extensions and how to write your own"
image: "/assets/images/plug-and-play-extensions/cranes.jpg"
image_caption: "'Crowd of Cranes', photo by Uzi Yachin. Via <a href='https://www.flickr.com/photos/93402933@N00/389251974'>Flickr</a>."
tags:
  - api
  - bash
  - extensions
---

Setting up a dev environment isn't about setting up a single tool in a carefully
manicured garden.

We have messy systems that need to interoperate!

One way to help systems interoperate is to build piles of
configuration. That's how teams end up with large YAML templates to express
the ways server X's configuration depends on server A, B, and C's configuration.

Another way is to react in realtime and have servers, or controllers, that manage the
configuration for us.

Both strategies have their pros and cons. In this blog post, we're going to
explore Tilt extensions that use each strategy, and how they work in practice.

## Plugging Tools Together With More Config

Lots of teams want to extend Tilt to support more types of dev environments. We
gave them the ability to add new functions to their Tiltfile.

Here's a good example of a Tilt extension: [`git_resource`](https://github.com/tilt-dev/tilt-extensions/tree/master/git_resource). From the README:

> Author: Bob Jackman
>
> Deploy a dockerfile from a remote repository -- or specify the path to a local checkout for local development.
>
> Install a Remote OR Local Repository
>
> `load('ext://git_resource', 'git_resource')`
> 
> `git_resource('myResourceName', 'git@github.com:tilt-dev/tilt-extensions.git#master')`
> 
> `# -- OR --`
> 
> `git_resource('myResourceName', '/path/to/local/checkout')`
>
> This will clone/pull your repo, build your dockerfile, and deploy your image
> into the cluster all in one fell swoop. This function is syntactic sugar and
> would be identical to sequentially making calls to `git_checkout()` and
> `deploy_from_dir()`

When you start Tilt:

1. `load()` checks if you've downloaded the code for the `git_resource` extension.
1. If the code isn't loaded, the function blocks while it downloads.
1. `load()` executes the extension code, then imports the `git_resource` function.
1. The `git_resource()` function checks if you've downloaded the given repository.
1. If the repository isn't cloned, the function blocks while it does a `git clone`.
1. The `git_resource()` function finds the Dockerfile (for any image builds) and Kubernetes YAML (for any deploys) in the repository.

We love the `git_resource` extension! We see teams use this a lot for multi-repo
projects (where each service is in its own repo). They can 
load configs from multiple repositories and duct tape them together.

All that duct tape happens at Tilt startup. And it happens synchronously, so it's
easy to reason about. If any part of it fails, Tilt won't start.

But this also has downsides! As the extension ecosystem grew, we started to see them:

- If we have a lot of synchronous extensions, starting Tilt can become
slow. Reloading the configuration can become slow. Optimizing may be a pain.
- We can't parallelize `load()` or `git_resource()` while they're downloading. We
could try to change the API to make them async.  But then we would need better
primitives for expressing dependencies and pipelines of async operations.
- People started asking for the ability to pass more configuration parameters to
`load()`, so we could change the execution of the extensions themselves. Or they
wanted a way to hook into the "end" of the Tiltfile, so they could inspect all
the resources that were defined.

When this starts to happen, it's a sign that we need a better tool: reactive controllers.

## Plugging Tools Together With Reactive Controllers

With a reactive controller extension, there are no functions to load. There are
no arguments to pass.

You can load them from the Tiltfile. You can load them from the CLI.

They're intended for auto-managing config, rather than for
piles of configuration.

Here's what it looks like. 

### Installing Extensions

In your Tiltfile, we write:

```python
v1alpha1.extension_repo(name='default', url='https://github.com/tilt-dev/tilt-extensions')
```

This registers a new extension repo named `default`. In the background, Tilt
downloads the repo.

The `url` will work for most major `git` hosts. If you're developing an extension,
you can use a `file://` URL. Here's the declaration I use when I'm developing extensions
locally:

```python
v1alpha1.extension_repo(name='default', url='file:///home/nick/src/tilt-extensions')
```

Then, we load the extension we want with the line:

```python
v1alpha1.extension(name='cancel', repo_name='default', repo_path='cancel')
```

An extension needs 3 parameters:
- A `name`, which is what it will show up as in the Tilt UI.
- A `repo_name`, which refers to the name of the repo we installed with `extension_repo`.
- A `repo_path`, which is the directory that the extension lives at in the repo.

Once the extension repo is finished downloading, Tilt will load the extension
configuration. This is an extension Tiltfile that loads independently of the rest of your
main Tiltfile.

### Managing Extensions

If you have a running Tilt session, you can use the CLI to inspect the extensions
you have installed and their current status.

```shell
$ tilt get extensionrepo
NAME      CREATED AT
default   2021-08-25T00:30:29Z
$ tilt get extension
NAME     CREATED AT
cancel   2021-08-25T00:30:29Z
```

We can even install and uninstall extensions from the command-line with `tilt
delete` and `tilt apply`. Or write extensions that manage other extensions! 😈

## Configs vs. Controllers

Last week, I wrote about the `cancel` extension [in more detail](https://blog.tilt.dev/2021/08/17/write-more-bash.html). `cancel` registers a server that watches Tilt resources,
and adds cancel buttons to their UI dashboard if they need it. 

If we were trying to implement `cancel` with config management tools, we would
write a new template function. Maybe we'd call it
`local_resource_and_cancel_button`. Then anything in our project that wanted a
cancel button would need to call our new function.

But with a cancel server, there are no templates and no dependency management.
We don't need to pass around button configuration.  We simply have our cancel
server watch for new resources, respond, and auto-configure the buttons!

In a future blog post, I'm going to write about how we use this new philosophy
to handle a more complex use-case that a lot of teams struggle with:
[auto-configuring and
auto-restarting](https://github.com/tilt-dev/tilt-extensions/tree/master/kubefwd)
`kubefwd`. Until next week!
