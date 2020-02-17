---
title: Using Tilt Extensions (Preview)
layout: docs
---

Tilt Extensions are packaged functions that you can easily use from your Tiltfile to make a better Tiltfile, faster.

## Finding an Extension
The [tilt-extensions README](https://github.com/windmilleng/tilt-extensions/blob/master/README.md) contains an index of every extension that's currently available. Each extension is listed alongside a blurb. Try using your browser's search functionality to look for keywords related to what you're trying to do (e.g. "java", "helm", "debugger", etc).

## Using an Extension
Once you've found an extension, using it couldn't be easier! Say we wanted to use the "hello_world" extension. We'd simply [`load()`](api.html#api.load) it in to our Tiltfile using a special `ext://` prefix, like so:

```python
load('ext://hello_world', 'hi')
```

`ext://hello_world` is resolved to https://github.com/windmilleng/tilt-extensions/blob/master/hello_world/Tiltfile by Tilt. When the extension is loaded in to your project for the first time Tilt writes the Tiltfile in to the `tilt_modules` directory in your project. So in this case Tilt would write the contents of `ext://hello_world` to `tilt_modules/hello_world`.

The `tilt_modules` directory should be committed to your repo (**not** `gitignore`'d) to ensure that your teammates don't have to download it in the future, and to ensure that everyone on your team is using the same version of the extension.

## Next Steps
If you have an idea for an extension, check out our doc on [Writing Tilt Extensions](writing_tilt_extensions.html). If you just have an idea for an extension that you want to see made, [give us a shout](debug_faq.html#where-can-i-ask-questions).
