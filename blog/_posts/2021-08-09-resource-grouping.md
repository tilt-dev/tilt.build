---
slug: "resource-grouping"
date: "2021-08-09"
author: lizz
layout: blog
title: "Spark joy with Tilt's resource grouping"
image: "/assets/images/resource-grouping/spark-joy-with-groups.jpg"
description: "Use labels to organize your multiservice dev environment"
tags:
  - api
  - ui
  - groups
  - labels
---
Multiservice development means you’re often scrolling through a long list of resources and tools, while you may only be dealing with a small slice of that larger pie. How do you stay organized? Through Tilt’s new resource grouping!

Tilt’s new UI feature allows you to define and add custom labels to your resources from the Tiltfile. The Tilt dashboard then displays this list of resources in expandable and collapsible groups, so you can visually hide resources that aren’t relevant to you on the fly.

![resource grouping demo](/assets/images/resource-grouping/demo.gif)

Over the [last few blog posts][uibutton-intro-blog], we’ve been talking a lot about Tilt UI’s customizability. With the new [UI button extension][uibutton-ext], you can add buttons to run tasks through Tilt’s dashboard. You can replace a long list of local resources that run one-off commands with easy-to-use triggers in the UI that are displayed next to the resource(s) they’re relevant to. But what happens to that long list of services you still need to run? This is where resource grouping comes in.

With groups, you can reduce the amount of resources you have to sift through to see what’s important to you. No more naming services like `store-service`, `store-database`, `store-test1`, `store-myspecial-cmd`, etc, to group relevant services together.

You might choose to group your services by engineering expertise, so that frontend, backend, and infrastructure services are grouped separately; or you might group by type of code, so services, tests, and linters are easily accessible; or you might organize similar resources together, so that a retail store service and inventory database are grouped.

Let’s dive into an example. We’ll start with the [PixelTilt example repo][pixeltilt], which runs a simple image-editing app with several backend services. We can add a label or list of labels to any resource call, including [`k8s_resource()`][k8s-docs], [`local_resource()`][local-docs], and [`dc_resource()`][dc-docs].

Here, we can group our `storage` and `object-detector` resources with an `infra` label.

```python
# k8s_resource allows customization where necessary such as adding port forwards
# https://docs.tilt.dev/api.html#api.k8s_resource
k8s_resource("frontend", port_forwards="3000")
k8s_resource("storage", port_forwards="8080", labels=["infra"])
k8s_resource("max-object-detector", new_name="object-detector", labels=["infra"])
```

As labels are added to resources, the dashboard will update and display the label groups. Any resources without a label will be grouped into an `unlabeled` section displayed at the bottom of the resource list. If a service has multiple labels, it will appear under each resource group in the UI.

![adding labels with the tiltfile demo](/assets/images/resource-grouping/add-labels-demo.gif)

Each group also comes with a resource status summary, so you can quickly understand the state for a subset of your services. It’s much easier to see if there’s an unhealthy resource in a particular set of services you care about.

![resource grouping statuses](/assets/images/resource-grouping/grouping-statuses.png)

Organizing resources into groups in log view is just the beginning. In the near future, we’re planning to roll out grouping to our newly launched Table View. Resource grouping is also a building block for much-requested features like bulk actions (and custom bulk actions!), as well as enabling and disabling services. 

You can start with labels and resource grouping by upgrading to [v0.22.2][upgrade]. 🏷 ✨

[dc-docs]: https://docs.tilt.dev/api.html#api.dc_resource
[k8s-docs]: https://docs.tilt.dev/api.html#api.k8s_resource
[local-docs]: https://docs.tilt.dev/api.html#api.local_resource
[pixeltilt]: https://github.com/tilt-dev/pixeltilt
[uibutton-ext]: https://github.com/tilt-dev/tilt-extensions/tree/master/uibutton
[uibutton-intro-blog]: /2021/06/21/uibutton.html
[upgrade]: https://docs.tilt.dev/upgrade.html
