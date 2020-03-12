---
title: Using Tilt Extensions
layout: docs
---

Tilt Extensions are packaged functions that you can easily use from your Tiltfile to make a better Tiltfile, faster.

## Finding an Extension
The [tilt-extensions README](https://github.com/windmilleng/tilt-extensions/blob/master/README.md) lists every published Tilt extension, along with a short a blurb. The full source of the extension is also available in the repo.

## Using an Extension
Once you've found an extension, using it couldn't be easier! Say we wanted to use the "hello_world" extension. We'd simply [`load()`](api.html#api.load) it in to our Tiltfile using a special `ext://` prefix, like so:

```python
load('ext://hello_world', 'hi')
```

`ext://hello_world` is resolved to https://github.com/windmilleng/tilt-extensions/blob/master/hello_world/Tiltfile by Tilt. When the extension is loaded into your project for the first time, Tilt copies the remote Tiltfile into the `tilt_modules` directory of local your project. So in this case Tilt would write the contents of `ext://hello_world` to `tilt_modules/hello_world`.

`hi` is the name of the function defined in [hello_world/Tiltfile](https://github.com/windmilleng/tilt-extensions/blob/master/hello_world/Tiltfile) and now made available to your local project Tiltfile. Simply call `hi()` anywhere to execute it, printing "Hello world!".

The `tilt_modules` directory should be committed to your repo (**not** `gitignore`'d) to ensure that your teammates don't have to download it in the future, and to ensure that everyone on your team is using the same version of the extension.

## Changing an Extension

We don't recommend changing extensions directly in `tilt_modules`. If you want to customize an extension you are already using, consider [contributing a change or a brand new extension](writing_tilt_extensions.html). Once the change is merged into [windmilleng/tilt-extensions](https://github.com/windmilleng/tilt-extensions/), get the updated or new extension (first deleting your local version in `tilt_modules` as necessary). Commit your changes to source control so that they will propagate to your team.

Tilt doesn't support versioning of extensions currently. If you are interested in versioning, [let us know](https://tilt.dev/contact).

## Next Steps
If you have an extension request, [give us a shout](https://tilt.dev/contact). If you'd like to contribute a new extension, visit [Writing Tilt Extensions](writing_tilt_extensions.html).
