---
slug: add-your-own-options-to-your-tilt-config
date: 2020-02-21
author: matt
layout: blog
title: "Add Your Own Options To Your Tilt Config"
image: "/assets/images/add-your-own-options-to-your-tilt-config/alexey-ruban-73o_FzZ5x-w-unsplash.jpg"
image_caption: "Photo by <a href='https://unsplash.com/@intelligenciya?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText'>Alexey Ruban</a> on <a href='https://unsplash.com/?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText'>Unsplash</a>"
tags:
  - tilt
keywords:
  - tilt
  - local development
  - tiltfile
---

Tilt is configured by programming your Tiltfile, which provides for a lot of flexibility, but sometimes a lighter-weight method of adjusting Tilt's behavior would feel better.

Tiltfile configs let your Tiltfile interact with command-line args at runtime, allowing users of your Tiltfile to do things like select groups or modes of services to run without having to edit a file or learn how Tiltfiles work.

## Using Tiltfile Configs

For example, many users want to be able to define groups of resources and be able to just `tilt up frontend` or `tilt up backend` and run just their frontend or backend services, without having to know and keep everyone updated on and type their current full list of frontend or backend services when they run `tilt up`.

Along with the new Tiltfile builtins to enable this behavior, we've added a new `tilt args` command that lets you edit the args you passed to `tilt up` without restarting. As a concrete example, if you ran `tilt up frontend` and then realized you also needed the backend running, without quitting Tilt, you can run `tilt args frontend backend`, and the Tiltfile will reexecute as if you'd originally executed `tilt up frontend backend` (which in this case would probably leave the frontend as-is and just start up the backend).

As someone who's just using Tilt with a Tiltfile your teammate wrote, that's all you need to know (well, aside from what options your teammate actually wrote).

## Defining Tiltfile Configs

Let's take a look at how you can write a Tiltfile that defines a `tilt up` command-line interface to allow your teammates to configure Tilt at runtime.

To write a Tiltfile that behaves this way, you're basically taking advantage of a few new builtins added to the Tiltfile language:
1. `config.define_string_list` and `config.parse` will let you access the values of the `tilt up` args in your Tiltfile.
2. `config.set_enabled_resources` instructs Tilt which resources to bring up, overriding its default behavior of just upping all of them.

At the risk of diving into the deep end, here's a quick example to make it more concrete.
```python
# define which services belong to which groups
groups = {
    'frontend': ['web', 'auth'],
    'backend': ['server', 'redis'],
}
# specify that `tilt up` args should be read into the config key "to-run"
config.define_string_list("to-run", args=True)
# actually parse the `tilt up` args
# e.g., if the user runs `tilt up frontend`, this will return `{'to-run': ['frontend']}`
cfg = config.parse()
resources = []
for arg in cfg.get('to-run', []):
    resources += groups[arg]
# instruct Tilt which resources to load
config.set_enabled_resources(resources)
```

The Tiltfile specifies what services belong to 'frontend' and 'backend'. It also declares that args to `tilt up` should be saved in a config setting named "to-run".

It then calls `config.parse()` to get the config settings, iterates over its "to-run" key, converting the list of group names into a list of resource names, and then passes them to `config.set_enabled_resources`, which tells Tilt to only load those resources (by default, Tilt loads all defined resources).

You can take a more leisurely stroll through this feature and see other examples of its use in the [Tiltfile Config guide](https://docs.tilt.dev/tiltfile_config.html).

As always, if you've got questions or feedback on any new
feature, [we'd love to hear from you](https://tilt.dev/contact)!

## Further Reading

- The [Tiltfile Config docs](https://docs.tilt.dev/tiltfile_config.html)
