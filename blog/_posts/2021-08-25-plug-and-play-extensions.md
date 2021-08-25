---
slug: "plug-and-play-extensions"
date: 2021-08-17
author: nick
layout: blog
title: "The Solution to Too Many Servers is More Servers"
subtitle: "Or: how to use Tilt plug-and-play extensions and how to write your own"
description: "Or: how to use Tilt plug-and-play extensions and how to write your own"
image: "/assets/images/plug-and-play-extensions/cranes.jpg"
image_caption: "'Crowd of Cranes', photo by Uzi Yachin. Via <a href='https://www.flickr.com/photos/93402933@N00/389251974'>Flickr</a>."
tags:
  - api
  - bash
  - extensions
---

When you first start working with Kubernetes, the amount of YAML config can be
overwhelming.

The obvious solution is to start writing tools to manage all that YAML!

But that focus on YAML means we often miss two pretty big philosophical points:

1. Most of the configuration in Kubernetes is stuff that we don't even see.

2. The reason that we don't see it is because we have servers that manage it for us,
   self-configuring without any intervention.
   
Now, don't misunderstand me. A bit of YAML duplication is fine. Copying and pasting
the same set of labels over and over is fine. If it starts to get duplicative,
you can group things into a Helm chart to templatize your YAML.

Sometimes it's not just about duplication. We need systems that
interoperate.  Maybe that means server X's configuration needs to depend on
server A, B, and C's configuration.  Maybe we need conditional configs, or
loops, or server dependencies (e.g., don't even start server B until server A is
healthy.) You *could* lean into YAML to manage that complexity.

But Kubernetes gives us another tool: more servers.

I like [this blog
post](https://medium.com/pinterest-engineering/building-a-kubernetes-platform-at-pinterest-fb3d9571c948)
from the Pinterest Engineering team where they use Kubernetes this way.

They abstracted out their YAML into a high-level `PinterestService`,
then wrote a server that translated `PinterestService` into low-level objects.

I've been thinking a lot about servers as a tool, and how we can use it at Tilt.

## Extending Tilt With More Config

Lots of teams want to extend Tilt to support more types of dev environments. We
gave them the ability to add new functions to their Tiltfile.

Here's a good example of a Tilt extension: [`git_resource`](https://github.com/tilt-dev/tilt-extensions/tree/master/kubefwd). From the README:

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

- `load()` checks if you've downloaded the code for the `git_resource` extension.

- If the code isn't loaded, the function blocks while it downloads.

- `load()` executes the extension code, then imports the `git_resource` function.

- The `git_resource()` function checks if you've downloaded the given repository.

- If the repository isn't cloned, the function blocks while it does a `git clone`.

- The `git_resource()` function finds the Dockerfile (for any image builds) and Kubernetes YAML (for any deploys) in the repository.

This is great! We see teams use this a lot for multi-repo projects (where each service is in its own repo).

But as our extension ecosystem grew, we started to see problems.

A lot of this logic is blocking! Starting Tilt was slow. Reloading the
configuration was slow. Optimizing it was a pain.

We can't parallelize `load()` or `git_resource()` while they're downloading. We
could try to change the API to make them async.  But then we would need better
primitives for expressing dependencies and pipelines of async operations.

People started asking for the ability to pass parameters to `load()`, so we
could change the execution of the extensions themselves. Or they wanted a way to
hook into the "end" of the Tiltfile, so they could inspect all the resources that
were defined.

We started to see all the same problems when you're managing lots of YAML!

More and more, Tiltfile configuration started to grow into a real programming
language, rather than a limited language for declaring resources.

We stepped back to rethink this. 

WWKD??? (What Would Kubernetes Do???)

## Extending Tilt With More Servers

Tilt has a new way to load extensions without any configuration at all. 

There are no functions to load. There are no arguments to pass.

You can load them from the Tiltfile. You can load them from the CLI.

They're intended for creating servers that auto-manage config, rather than for
templating config.

Here's what it looks like. 

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
main Tiltfile. (One doesn't block the other, and they can even load in parallel.)

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

Last week, I wrote about the `cancel` extension [in more detail](https://blog.tilt.dev/2021/08/17/write-more-bash.html). `cancel` registers a server that watches Tilt resources,
and adds cancel buttons to their UI dashboard if they need it. 

If we were trying to implement `cancel` with YAML management tools, we would
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
