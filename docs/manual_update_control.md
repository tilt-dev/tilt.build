---
title: Play and Pause Resources with Manual Update Control
description: "How to configure Tilt to indicate in the UI that files have changed, and give you a button that you can use to kick off the update."
layout: docs
sidebar: guides
---

By default, Tilt watches your filesystem for edits and, whenever it detects a change affecting Resource X, triggers an update of that resource. All your local code, synced to your cluster as you edit it! What could be better?

Well, sometimes that's _not_ what you want. Maybe updating Resource X takes a long time and so you only want to run updates when you're actually ready. Maybe you're about to check out a branch and don't want all the spurious file changes to launch a lot of updates. Whatever your reason, Manual Update Control is here to help.

The behavior described above is `TriggerMode: Auto` (Tilt's default); that is, updates are _automatically_ triggered whenever Tilt detects a change to a relevant file.

There's another way of doing things: `TriggerMode: Manual`. Tilt will still monitor file changes associated with your resources, but instead of automatically rebuilding and/or deploying every time a relevant file changes, Tilt will simply indicate in the UI that files have changed, and give you a button that you can use to kick off the update.

## Using TriggerMode
You can change the trigger mode(s) of your resources in your Tiltfile in two different ways:

1. Functions that configure resources ([`k8s_resource()`](/api.html#api.k8s_resource), [`local_resource()`](/api.html#api.local_resource), and [`dc_resource()`](/api.html#api.dc_resource)) have an optional arg, `trigger_mode`; for that specific resource, you can pass either `TRIGGER_MODE_AUTO` or `TRIGGER_MODE_MANUAL`.
2. If you want to adjust all of your resources at once, call the top-level function [`trigger_mode()`](/api.html#api.trigger_mode) with one of those two constants. This sets the _default trigger mode for all resources_. (You can still use `k8s_resource()` to set the trigger mode for a specific resource.)

Here are some examples:
```python
...
# TriggerMode = Auto by default
k8s_resource('snack')
```

```python
...
# TriggerMode = Manual
k8s_resource('snack', trigger_mode=TRIGGER_MODE_MANUAL)
```

```python
trigger_mode(TRIGGER_MODE_MANUAL)
...
# TriggerMode = Manual (default set above)
k8s_resource('snack')

# TriggerMode = Auto (can override the above default
# for specific resources)
k8s_resource('bar', trigger_mode=TRIGGER_MODE_AUTO)
```

<div class="block u-margin1_5">
 <img src="assets/img/update-control.gif">
</div>

When you make changes to "snack", instead of them being automatically applied, Tilt will simply indicate unapplied changes by the asterisk to the right of `snack` in the sidebar. It will not automatically apply those changes. Instead, it will wait until you click the apply button to the left of `snack`.

## Auto Init
TriggerMode can be combined with the `auto_init` argument on [`k8s_resource()`](/api.html#api.k8s_resource), [`local_resource()`](/api.html#api.local_resource), and [`dc_resource()`](/api.html#api.dc_resource) for even more fine-grained control.

To configure a resource to _only_ run when explicitly triggered from the UI, set `auto_init=False` and `trigger_mode=TRIGGER_MODE_MANUAL`. It will not run on start nor when files are changed.

To configure a resource that does _not_ run at start, but still runs whenever a file dependency is changed,
set `auto_init=False` and `trigger_mode=TRIGGER_MODE_AUTO`. This can be useful for tasks like linting or
executing tests automatically, for example.

## <span class="pill-tag">Beta</span> Disabling resources through Tilt

Through Tilt’s UI Dashboard, you can enable and disable resources that are available in your Tilt session.

Disabling a resource will stop the running process (if any) and delete any objects owned by that resource. It’s the equivalent of running `tilt down` on a specific resource. Enabling a resource will create, build, deploy, and start any processes for that resource.

> 💡 Disabling and enabling a resource doesn’t take into account any of its resource dependencies. For example, if resource B depends on resource A, disabling resource A will not disable resource B.

> 💡 If you’re using [`tilt args`](tiltfile_config.html) to define a subset of resources Tilt is running, only the resources that are defined through args will show up in the UI Dashboard. In a future release, we’re planning to display all defined resources from the Tiltfile in the UI.

### How to enable the feature
While in beta, Disabling Resources feature requires opting in. First, make sure you're on [Tilt v0.23.5+](https://github.com/tilt-dev/tilt/releases). Then, add the following line to your Tiltfile:

```
enable_feature(“disable_resources”)
```

Save your Tiltfile and you should see the Disable Resources functionality available in the UI.
### How to use the feature

#### From the UI Dashboard
Navigate to Detail View by clicking on the “All Resources” link in the header.

Then, click on an individual resource from the sidebar. Each resource that can be disabled will have a “Disable Resource” button in the upper left of the log pane, next to the “All Levels” log filter button.

<figure>
  <img src="/assets/img/disable-resources-detail-button.png" alt="A screenshot of the Tilt Web UI's Detail View with a 'Disable Resource' button circled in blue">
</figure>

Disabled resources will be listed at the bottom of resource groups (if you’re using [labels to group resources](tiltfile_concepts.html#resource-groups)) or the whole resource list in both Table View and Detail View.

<figure>
  <img src="/assets/img/disable-resources-detail-sidebar.png" alt="A screenshot of the Tilt Web UI's Detail View sidebar with a list of enabled and disabled resources. A blue arrow points to a disabled resource at the bottom of the sidebar list.">
</figure>

Logs will remain visible for disabled resources, along with an “Enable Resource” button in the upper left of the long pane.

<figure>
  <img src="/assets/img/disable-resources-detail-view.png" alt="A screenshot of the Tilt Web UI's Detail View with a disabled resource selected. The central log pane shows all the resource's logs.">
</figure>

#### From the Tilt API
You can also enable and disable resources programmatically.

The source of truth for a resource’s disabled status is a [ConfigMap](https://api.tilt.dev/core/config-map-v1alpha1.html). To enable or disable a specific resource, you’ll need to edit the ConfigMap.

Using Tilt’s sample [pixeltilt project](https://github.com/tilt-dev/pixeltilt/), let’s walk through the steps of disabling a specific resource called `glitch`, accessing the Tilt API via the `tilt` command.

First, find the name of the ConfigMap that corresponds to the resource we want to disable. (Tip: Disable ConfigMap names generally follow the pattern of `<uiresource name>-disable`.)

Start by listing all resources to find the [UIResource](https://api.tilt.dev/interface/ui-resource-v1alpha1.html) name:
```shell
$ tilt get uiresource

NAME              CREATED AT
storage           2021-12-23T16:19:51Z
muxer             2021-12-23T16:19:51Z
object-detector   2021-12-23T16:19:51Z
frontend          2021-12-23T16:19:51Z
glitch            2021-12-23T16:19:51Z
color             2021-12-23T16:19:51Z
bounding-box      2021-12-23T16:19:51Z
(Tiltfile)        2021-12-23T16:19:51Z
```

Then look at the details of the specific resource to find the ConfigMap name:
``` shell
$ tilt get uiresource glitch -ojson

{
    "apiVersion": "tilt.dev/v1alpha1",
    "kind": "UIResource",
    …
    "status": {
        "disableStatus": {
            "disabledCount": 1,
            "enabledCount": 0,
            "sources": [
                {
                "configMap": {
                    "key": "isDisabled",
                    "name": "glitch-disable"
                    }
                }
            ]
        }
    }
}
```
The configmap name will be under the UIResource’s `status.disableStatus.sources[0].configMap.name`.

Now that you have the ConfigMap name, edit it with the desired disabled state:

```shell
$ tilt patch configmap glitch-disable -p ‘{ “data”: { “isDisabled”: “true” } }’
```

### What can I use this feature for? 
We saw that for many cases, it’s not practical or feasible to run all your resources all the time. But changing resources can interrupt your flow (e.g., you have to switch between the UI and command line). Improving Tilt's interface can make it more seamless to change the resources you’re running at any given time, and reduce the cognitive load of finding and running the right resources you need to run.

So, we’re planning these future features to make it easier to manage sets of resources, and pick up from where you left off every time you restart Tilt:
- Disabling and enabling multiple resources at once from Table View
- `tilt args` persistence, so that `tilt up` starts by default with the last used set of resources, similar to how your editor might reopen with the last set of open documents
- Changing `tilt args` and `config.set_enabled_resources()` to use this new feature, rather than dropping non-enabled resources entirely; the Tilt UI will show all resources with only the specified resources enabled.
- Defaulting resources to disabled rather than enabled, to give the user better control over which resources are running

But! We might be wrong. Maybe you have another use case that we haven't considered? Please talk to us.
* Slack us from the [Kubernetes #tilt channel](http://slack.k8s.io)
* Send an email at [hi@tilt.dev](mailto:hi@tilt.dev)
* Sign up for an office hours session with [Calendly](https://calendly.com/han-yu/user-research)
* File an issue on [Github](https://github.com/tilt-dev/tilt/issues)

(And of course, we welcome bug reports, UI issues, or any other thoughts you have that could improve your experience.)
