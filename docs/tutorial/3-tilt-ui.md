---
title: Tilt UI
subtitle: Tilt Tutorial
layout: docs
---
## Launching the Web UI
In your terminal window running `tilt up`, press `(Spacebar)`. Tilt will open your default browser to the Tilt UI. (Or you can navigate to [http://localhost:3366]().)

## Resource Overview
The Resource Overview is the first thing you see when you open the Tilt UI (or click the Tilt logo in the upper left corner).

![Tilt UI resource overview](/assets/docimg/tutorial/tilt-ui-table.png)

This view shows all your resources (services) at a glance, grouped by their [resource labels][tiltfile-labels].

In the `tilt-avatars` project, we've defined two labels: `backend` and `frontend`.
The `backend` group has the `api` resource and the `frontend` resource has the `web` resource.
Additionally, there is a built-in `Tiltfile` group.

How you choose to group your services is up to you!

![api resource status in resource overview](/assets/docimg/tutorial/tilt-ui-status.png)

If you look at the `api` resource row, you'll see both the update and runtime status.
Since this is a "Kubernetes Deploy" type resource, the update included building the image and `kubectl apply`ing it the cluster.
The runtime status reflects the Pod's current state in the cluster. e.g. Is it running and passing readiness checks?

![Copy pod ID button in resource overview](/assets/docimg/tutorial/tilt-ui-copy-pod-id.gif)

The Resource Overview also includes the Pod ID, so you can quickly interact with it as needed via `kubectl` or other tools.

![Port forward endpoint URLs in resource overview](/assets/docimg/tutorial/tilt-ui-endpoints.png)

Endpoints shows you configured port forwards, so you don't have to memorize port numbers.

![Trigger mode toggle in resource overview](/assets/docimg/tutorial/tilt-ui-trigger-mode.png)

By default, resources in Tilt are updated whenever a relevant file changes.
It's possible to change the default behavior on a per-resource basis (or globally) in the Tiltfile with [manual update control][tiltfile-trigger-mode].
The trigger mode toggles for each resource in the UI make it easy to quickly pause and resume automatic updates to it.

Even if a resource is in manual mode, it's always possible to trigger an update on-demand!

Let's take a look at the Resource Details next.

## Resource Details
From the Resource Overview, you can click on any resource's name to dive into it.

![Resource detail view for api resource](/assets/docimg/tutorial/tilt-ui-resource-detail.png)

The central focus of the Resource Detail view are logs.

> 📚 The "All Resources" link in the navbar will show logs for all services at once instead of a single service

The endpoint and pod IDs are available here in addition to the resource overview.

### Log Filtering
Tilt provides several mechanisms to focus your logs.

![Filtering logs by source (build or runtime)](/assets/docimg/tutorial/tilt-ui-log-filter-source.gif)

By default, Tilt shows both build/update and runtime logs interleaved.
It's possible to restrict this to a single source.
For example, if you're trying to fix an error during your resource start, it might be helpful to temporarily hide the build logs to reduce noise as you make changes.

![Filtering logs by level (error or warning)](/assets/docimg/tutorial/tilt-ui-log-filter-level.png)

In addition to unifying your logs, Tilt collects errors and warnings from different tools such as Docker build errors, Kubernetes events, and more.
You can quickly filter the view to just these important events including the surrounding context by clicking `... (more)`.

[tiltfile-labels]: /tiltfile_concepts.html#resource-groups
[tiltfile-trigger-mode]: /manual_update_control.html
