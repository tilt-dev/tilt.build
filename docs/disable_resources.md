---
title: Disabling Resources Through Tilt
description: "Use Tilt's new feature to disable and enable resources through the UI. Manage what resources you have up and running more seamlessly."
layout: docs
sidebar: guides
---

> <span class="pill-tag">Beta</span> This feature is in beta. It's turned off by default, and breaking changes could be introduced while under development.

Through Tilt’s UI Dashboard, you can enable and disable resources that are available in your Tilt session.

Disabling a resource will stop the running process (if any) and delete any objects owned by that resource. It’s the equivalent of running `tilt down` on a specific resource. Enabling a resource will create, build, deploy, and start any processes for that resource.

Depending on your `Tiltfile` setup, it may be important to note:
* Disabling and enabling a resource doesn’t take into account any of its resource dependencies. For example, if resource B depends on resource A, disabling resource A will not disable resource B.
* If you’re using [`tilt args`](tiltfile_config.html) to define a subset of resources Tilt is running, only the resources that are defined through args will show up in the UI Dashboard. In a future release, we’re planning to display all defined resources from the Tiltfile in the UI.

## How to enable the feature
While in beta, Disabling Resources feature requires opting in. First, make sure you're on [Tilt v0.23.5+](https://github.com/tilt-dev/tilt/releases). Then, add the following line to your Tiltfile:

```
enable_feature("disable_resources")
```

Save your Tiltfile and you should see the Disable Resources functionality available in the UI.
## How to use the feature

### From the UI Dashboard
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

### From the Tilt API
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
$ tilt patch configmap glitch-disable -p '{ "data": { "isDisabled": "true" } }'
```

## What can I use this feature for? 
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
