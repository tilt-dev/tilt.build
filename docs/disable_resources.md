---
title: Disabling Resources Through Tilt
description: "Use Tilt's new feature to disable and enable resources through the UI. Manage what resources you have up and running more seamlessly."
layout: docs
sidebar: guides
pilltag: new
---

> 💡 This feature is available in [Tilt v0.23.10+](https://github.com/tilt-dev/tilt/releases).

For many developers, it's not practical or feasible to run all your resources all the time. It shouldn't interrupt your flow to change what resources you're running, or disable a troublesome resource on the fly.

With the Tilt UI and `tilt args`, you can enable and disable resources at any time and more seamlessly manage your resource catalog.

Disabling a resource will stop the running process (if any) and delete any objects owned by that resource. It’s the equivalent of running `tilt down` on a specific resource. Enabling a resource will create, build, deploy, and start any processes for that resource.

## How to enable and disable resources

### With `tilt args`
You can use [`tilt args`](cli/tilt_args.html) to run a specific set of resources, as well as define groups of resources through the config API. Any resources defined through args will be enabled, while the rest of resources defined in your Tiltfile will be disabled and display in the Tilt UI. (See the [Tiltfile config guide](tiltfile_config.html#examples) for more detail.)

From the Tilt UI, you can also enable and disable resources, but doing so won't change value of `tilt args`.

Here's an example taken from Tilt’s [pixeltilt project](https://github.com/tilt-dev/pixeltilt/):
```shell
# enable only the resources named 'frontend' and 'glitch',
# all other resources will be disabled and visible in the UI
$ tilt up frontend glitch
```

To edit the args, you can run `tilt args` with a new set of arguments that will replace the existing ones, or without a new set of arguments to open the current args for editing. See the [args CLI reference](cli/tilt_args.html) for details.
```shell
# edit the current arts to enable only 'bounding-box,'
# 'muxer,' and 'max-object-detector'
$ tilt args bounding-box muxer max-object-detector
```

> 💡 Note: if your args don't change between edits, Tilt will consider that a no-opt, even if you've enabled or disabled a different set of resources through the UI.

### With the Tilt UI

In Detail View, look for the "Disable Resource" button on an individual resource near its logs. Logs will remain visible for disabled resources, along with an “Enable Resource” button.

<figure>
  <img src="/assets/img/disable-resources-detail-view.gif" alt="An animated gif showing an enabled resource in Detail View of Tilt's UI. A mouse clicks on the 'Disable Resource' button, waits for the resource to show up as disabled, and then clicks on the 'Enable Resource' button.">
</figure>

In Table View, you can select multiple resources by clicking on the checkbox column and enable or disable them at once. The bulk action buttons will appear when any resource is selected.

<figure>
  <img src="/assets/img/disable-resources-table-view.gif" alt="An animated gif showing Table View of Tilt's UI. Three of the five resources displayed in the table are disabled. A mouse clicks on each of the checkboxes next to the disabled resources and enables them through the bulk action buttons above the table.">
</figure>

Disabled resources will be listed at the bottom of resource groups (if you’re using [labels to group resources](tiltfile_concepts.html#resource-groups)) or the whole resource list in both Table View and Detail View.

> 💡 Note: Disabling and enabling a resource through the Tilt UI doesn’t take into account any of its resource dependencies. For example, if resource B depends on resource A, disabling resource A will not disable resource B.

### With the Tilt CLI

```shell
# enable the resources named 'frontend' and 'storage'
$ tilt enable frontend storage
```
```shell
# enable 'frontend' and 'storage', and disables all others
$ tilt enable --only frontend storage
```
```shell
# enable all resources
$ tilt enable --all
```
```shell
# disable the resources named 'frontend' and 'storage'
$ tilt disable frontend storage
```
```shell
# disable all resources
$ tilt disable --all
```

### With your Tiltfile

To define a default or programmatic list of enabled resources, you can use the config built-ins from your Tiltfile. The [Tiltfile config guide](tiltfile_config.html#examples) walks through detailed examples of enabling and configuring groups of resources.

To disable all resources by default, you can call [`config.clear_enabled_resources()`](api.html#modules.config.clear_enabled_resources) in your Tiltfile. This starts Tilt with all resources disabled and visible in the UI, where you can selectively enable what you need.

```python
# from your Tiltfile
config.clear_enabled_resources()
```
### Feedback
Does this feature work for you? We want to reduce the cognitive load of finding and running the right resources. Please reach out:
* Slack us from the [Kubernetes #tilt channel](http://slack.k8s.io)
* Send an email to [hi@tilt.dev](mailto:hi@tilt.dev)
* File an issue on [Github](https://github.com/tilt-dev/tilt/issues)
* Sign up for an office hours session with [Calendly](https://calendly.com/han-yu/user-research)