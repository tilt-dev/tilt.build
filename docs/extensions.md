---
title: Extensions
description: "Extensions are open-source packaged functions that extend the capability Tilt, right inside your Tiltfile."
layout: docs
sidebar: guides
---

Extensions (available starting in v0.12.11, see [releases](https://github.com/tilt-dev/tilt/releases)) are open-source packaged functions that extend the capability Tilt, right inside your Tiltfile.

We've seen the Tilt community actively share code snippets of Tiltfile functionality in [Slack #tilt](https://kubernetes.slack.com/messages/CESBL84MV/), including ideas such as forcing resources into different namespaces, injecting sidecars, and even running tests. We've created the Extensions platform to streamline this effort, especially helping Tilt newcomers leverage ideas from existing users. Consider [contributing an extension](contribute_extension.html).

## Published extensions
The [tilt-extensions repo](https://github.com/tilt-dev/tilt-extensions) lists all published extensions.

## Use an extension
Suppose we want to use the [`hello_world` extension](https://github.com/tilt-dev/tilt-extensions/tree/master/hello_world), which prints "Hello world!". First, [`load()`](api.html#api.load) the extension with a special `ext://` syntax, referring to both the extension name `hello_world`, and function name `hi`,  in your Tiltfile:

```python
load('ext://hello_world', 'hi')
```

Now when you call `hi()` in your Tiltfile, Tilt will print "Hello world!".

## Behind the scenes
Tilt resolves `ext://hello_world` to [tilt-extensions/blob/master/hello_world/Tiltfile](https://github.com/tilt-dev/tilt-extensions/blob/master/hello_world/Tiltfile). So when the extension is first loaded into your project, Tilt copies the remote Tiltfile into the `tilt_modules` directory of your local project. I.e. Tilt writes the contents of `ext://hello_world` into `tilt_modules/hello_world`.

## Commit to source control
Commit the `tilt_modules` directory to your project repo (**do not** `gitignore` it), so that your teammates don't have to download it, and to ensure that your entire team uses the same copy of the extension. Once Tilt has downloaded an extension, it will not be updated, avoiding suprise breakages.

Tilt doesn't support versioning of extensions at the moment.

(To get notified about versioning, please subscribe to [this issue](https://github.com/tilt-dev/tilt/issues/3426)
and thumbs-up it so we know you care about it.)

## Avoid changing extensions
Avoid changing extensions directly in `tilt_modules`. If you're interested in modifying an extension, consider [contributing a new one](contribute_extension.html) instead,


## Next steps
[Request new extensions](https://github.com/tilt-dev/tilt/issues) or [contribute a new one](contribute_extension.html).
