---
title: Extensions
description: "Packaged functions that add new functionality to your dev env."
layout: docs
sidebar: guides
---

Tilt lets you define your dev environment with a Tiltfile.

We have many built-in APIs for defining local tasks, image builds, and containerized servers.

But we also see dev rules that are particular to a team like:

- Checks that the right versions of local tools are installed.

- Scripts for defining image builds or deploys.

- Custom buttons for operations like resetting a dev database or upgrading a dependency.

And you want to share those snippets across repos or even across companies!

That's why Tilt has an extension system for writing and sharing snippets of
Tiltfile functionality!

## Using an extension: "Hello world!"

As an easy introduction, let's look at the `hello_world` extension.

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

## Discovering extensions

The [tilt-extensions repo](https://github.com/tilt-dev/tilt-extensions) contains
many general-purpose extensions from the Tilt community.

```python
load('ext://hello_world', 'hi')
```

The `load()` call above is loading the extension from the `tilt-extensions` repo!

In particular,

- The `tilt-extensions` repo gets checked out in the background.

- Tilt reads the Tiltfile under `hello_world/Tiltfile`

- Tilt sets the variable `hi` in the local scope to the `hi` function in the extension.

## Sharing Tiltfile Code in a Single Repo

If the common Tiltfile code you want to share is in a single repo, you don't need the
extension system at all!

The first argument to `load()` can be a relative file path.

```python
load('./common/Tiltfile', 'hi')
```

The `load()` function has a nice syntax for binding variables, but that makes
its API a bit rigid. For more complex scripting, there's a `load_dynamic`
function.

```python
symbols = load_dynamic('./common/Tiltfile')
hi = symbols.get('hi')
```

For more on `load()` and `load_dynamic()`, see the [API
reference](https://docs.tilt.dev/api.html#api.load) or our blog post [Load
Dynamic](https://blog.tilt.dev/2020/11/03/load-dynamic.html).

## Modifying the Default Extensions Locally

In Tilt v0.25, we've made it easy to load the default extension repo locally.

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

We could also use a repo on local disk:

```shell
v1alpha1.extension_repo(name='default', url='file:///usr/nick/src/tilt-extensions')
load('ext://hello_world', 'hi')
```

The `file:///` syntax only accepts absolute paths. You would only use it for local
experimentation. `load()` and `load_dynamic()` are better fits when you want to load
shared functions from a relative path.

## Managing Your Own Extension Repo

The `extension_repo` API lets you replace the default repo with your own fork.

For example, you can fork the shared `tilt-extensions` repo, use a `stable` tag 
to denote the version that most people should use, then add some code to your Tiltfile to pin it:

```python
v1alpha1.extension_repo(name='default', url='https://github.com/my-org/tilt-extensions', ref='v0.25.0')
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

## Debugging Extension Loading with the CLI

A Tilt session publishes the names of all repos and extensions it's using and where they live on disk.

You can read this info with the CLI. Here are some common commands you might use
to explore the status. (We use `jq` to prettify the JSON.)

```bash
$ tilt get extensionrepo
NAME      CREATED AT
default   2022-02-04T18:56:38Z

$ tilt get extensionrepo default -o jsonpath='{.status}{"\n"}' | jq
{
  "checkoutRef": "6f4d3436c557d70bb0810b0da1acb99c364120b6",
  "lastFetchedAt": "2022-02-04T17:18:44Z",
  "path": "/home/nick/.local/share/tilt-dev/tilt_modules/github.com/tilt-dev/tilt-extensions"
}

$ tilt get extension
NAME          CREATED AT
hello_world   2022-02-04T18:56:38Z

$ tilt get extension hello_world -o jsonpath='{.status}{"\n"}' | jq
{
  "path": "/home/nick/.local/share/tilt-dev/tilt_modules/github.com/tilt-dev/tilt-extensions/hello_world/Tiltfile"
}
```

## Sharing Extensions with the Community

If you have an extension that you think would be generally useful, we love to
see people contribute them!

Check out our [contributing extensions](contribute_extension.html) guide
for more detail on the pull request and review process.

