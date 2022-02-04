---
title: Contribute an Extension
description: "How to create and submit your own Tilt extension"
layout: docs
sidebar: guides
---

Tilt has many built-in APIs for defining local tasks, image builds, and
containerized servers.

Extensions let you package up a tool and plug it into any Tilt dev environment.

For common tools, like image builders and YAML template engines, our users often
share their extensions with the Tilt community by putting them in the common
[tilt-extensions repo](https://github.com/tilt-dev/tilt-extensions).

This page explains how to contribute a new extension to the shared repo.

If you're interested in how to use an existing extension, or how to share code
within a single team, start with our [extensions guide](extensions.html).

## Create the extension locally

First, fork the `tilt-extensions` repo. Clone it locally.

Create a new file where your extension code will live:

```
extension_name/Tiltfile
```

Create a new function in the Tiltfile you just created:

```
def hi():
  print("Hello world!")
```

Now, in your main project, point your default extension repo at the absolute path where you cloned `tilt-extensions`:

```python
v1alpha1.extension_repo(name='default', url='file:///usr/nick/src/tilt-extensions')
load('ext://extension_name', 'hi')
hi()
```

Hooray! The extension works! Now you're ready to send it out.

## Package your function and submit a pull request

First, update the root
[README.md](https://github.com/tilt-dev/tilt-extensions/blob/master/README.md),
explaining your extension.

Then, add `extension_name/README.md` with detailed information about your extension. Your README should include:

- The extension name

- The author name (you!)

- A brief description of the functions defined in the extension

- How to use the extension in practice

May of our extensions also have an `extension_name/test` directory with a working example project.
The `tilt-extensions` CI will run that project to make sure all the servers come up successfully.

Create and submit a pull request to the repo for review by the Tilt team.  Your
pull request should be prefixed with the name of your extension, e.g.:
`min_tilt_version: fix bug foobar`.

## Next steps

If you have an idea for an extension but aren't sure where to start, the [Tilt
community](https://docs.tilt.dev/#community) loves batting around extension
ideas. If you have an idea but aren't interested in writing it yourself, you can
also file a feature request in the [issue
tracker](https://github.com/tilt-dev/tilt-extensions/issues).
