---
slug: "resource-catalog"
date: 2022-03-03
author: lizz
layout: blog
title: "Running just a few of your many services should be easy"
subtitle: "Use Tilt to build a flexible, browsable resource catalog for your team"
description: "Use Tilt to build a flexible, browsable resource catalog for your team"
image: "/assets/images/disable-resources/pen-catalog.jpg"
image_caption: "Photo by <a href='https://unsplash.com/@amseaman?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText'>Andrew Seaman</a> on <a href='https://unsplash.com/?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText'>Unsplash</a>"
tags:
  - tilt
  - api
  - ui
  - groups
  - labels
---
Many developers have far more resources defined in Tilt than they’d actually want to run at once.

*  Different teams require different subsets of resources to do their day-to-day tasks.
*  Your work is exploratory, so it's not feasible to define upfront which resources you need. Intermittently, you might want to bring up additional resources to test the changes you just made.
*  Some resources are so CPU-intensive that you only want to run the bare minimum you need.

Do any of these scenarios seem familiar to you? Read on to learn how to use Tilt as a resource catalog tailored to your team's needs.

## A Better Workflow

Tilt already helps you move away from clunky workflows where you need to remember a series of bash commands to run the resources you need. But for managing an active set of resources, we still found our users resorting to the command line:

```shell
# Start Tilt with only the storage resource
$ tilt up storage

# Oh wait, let's add these other resources I need to work on
$ tilt args storage frontend glitch object-detector color

# Ahh, my work changed and I need a different set running
$ tilt args storage frontend object-dectector bounding-box muxer
```

Now, Tilt makes it easier to enable and disable individual and sets of resources. You don't need to restart Tilt or copy and paste long [`tilt args` commands][tilt-args] when you want to work with different resources.

In your Tiltfile, you can define the resources that automatically run on `tilt up,` and all other resources will be disabled, but available to enable through Tilt’s UI and CLI. The Tilt UI lets you show or hide disabled services. And in the table view, you can select multiple resources to enable or disable at once. When you’re viewing logs, there’s also a handy way to disable troublesome resources. 

[See our docs for a more detailed walkthrough.][disable-resources]

![disable a single resources](/assets/images/disable-resources/single-resource-disable.gif)

## If you’re setting up Tilt for your team...

Enabling and disabling resources on the fly should make workflows easier for individual contributors focused on shipping. But, let’s zoom out and talk about how a “resource catalog” can improve the overall development experience for your team.

```python
# In your Tiltfile
config.define_string_list("to-run", args=True)
cfg = config.parse()

groups_by_team = {
  'client_team': ['service_a', 'service_b', 'service_c', 'service_d', 'service_m', 'service_p'],
  'data_team': ['service_b', 'service_d', 'service_m', 'service_n']
  'infra_team': ['service_x', 'service_y', 'service_z']
}

to_run = []
for arg in cfg.get('to-run', []):
    if arg in groups_by_team:
        # Add any resources by their predefined groups
        to_run.extend(groups_by_team.get(arg))
    else:
        # Add any resources by their individual names
        to_run.append(arg)

config.set_enabled_resources(to_run)
```

You can define sensible defaults for engineers, like grouping services based on those frequently used by particular teams, or based on your stack. Engineers can start Tilt with these [predefined groups][tiltfile-config], but they won’t be excessively constrained by them. Both Tilt’s UI and CLI makes it easy to override the running set of services and add or subtract based on what they need.

```shell
# Start Tilt with the data_team resource group
$ tilt up data_team

# Bring up an additional resource outside of the data_team group
$ tilt enable service_a

# Bring down resources from the data_team that are no longer needed
$ tilt disable service_b service_d
```

Organizing your resources with labels is particularly useful so engineers can quickly enable and disable all resources in a group using the UI.

![enable multiple resources](/assets/images/disable-resources/bulk-disabling.gif)

One caveat to note: enabling and disabling individual resources doesn’t consider any dependencies they rely on. (Though we have several [feature requests][disable-issues] here!) If you’ve got resources with a lot of dependencies, start with the Tiltfile config and use `tilt args` to define sets to take dependencies into account.

This “resource catalog” experience can dramatically improve onboarding time for new engineers, and also just make the day-to-day workflow more pleasant for engineers on your team.

If you try some version of this, [get in touch][feedback]! We are always interested in hearing about what makes your workflow better.

_Major shoutouts to Han, Matt, Lian, and Nick Santos for their contributions on these features!_

[tilt-args]: https://docs.tilt.dev/cli/tilt_args.html
[tiltfile-config]: https://docs.tilt.dev/tiltfile_config.html#run-a-defined-set-of-services
[disable-resources]: https://docs.tilt.dev/disable_resources.html
[disable-issues]: https://github.com/tilt-dev/tilt/issues?q=is%3Aissue+is%3Aopen+disable+resource+label%3Aenhancement
[feedback]: https://docs.tilt.dev/disable_resources.html#feedback