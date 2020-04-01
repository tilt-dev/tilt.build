---
slug: more-customizable-tiltfiles-with-extensions
date: 2020-04-01
author: victor
layout: blog
title: "More customizable Tiltfiles with Extensions"
subtitle: "Contribute an extension; grow the Tilt community"
image: "/assets/images/more-customizable-tiltfiles-with-extensions/michael-dziedzic-XTblNijO9IE-unsplash.jpg"
image_caption: "Photo by <a href='https://unsplash.com/@lazycreekimages?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText'>Michael Dziedzic</a> on <a href='https://unsplash.com/?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText'>Unsplash</a>"
tags:
  - tilt
keywords:
  - extensions
  - tilt
  - tiltfile
---

In Tilt, you declare your dev environment in Starlark, a subset of Python. But Starlark is missing a big feature: there's no package manager! Starlark doesn't have built-in ways to share code.

The Tilt community noticed! We've seen people:
- Copy and paste "best practices" for different languages
- Struggle to share Tiltfiles across multiple repos
- Send each other Tiltfile snippets

To address this gap, as a first step toward a multi-service dev package manager, we've created Tilt extensions.

Tilt extensions are available starting in [v0.12.11](https://github.com/windmilleng/tilt/releases/tag/v0.12.11). ([Click here](https://docs.tilt.dev/upgrade.html) to upgrade!)

## What's an extension, exactly? And how do you use it?
An extension is an approved and packaged function containing functionality written and shared by (probably another) Tilt community member, that you can remotely import into your own Tiltfile.

For example, to use the `hi` function from the [`hello_world` extension](https://github.com/windmilleng/tilt-extensions/tree/master/hello_world), first [`load()`](https://docs.tilt.dev/api.html#api.load) it by including this command in your Tiltfile:

```
load('ext://hello_world', 'hi')
```

Then call [`hi()`](https://github.com/windmilleng/tilt-extensions/tree/master/hello_world/Tiltfile) later in your Tiltfile to print "Hello World!".

Read the [docs](https://docs.tilt.dev/extensions.html) for additional details and look at the [tilt-extensions repo](https://github.com/windmilleng/tilt-extensions) for a list of available and approved extensions. 

We've already seen the Tilt community activey share ideas, especially in [Slack #tilt](https://kubernetes.slack.com/messages/CESBL84MV/). We hope that by providing a more structured platform, community members can even more effectively collaborate and leverage the benefits of shared Tiltfile functionality. Users can take advantage of solutions that contributors have already worked through. And contributors can see their work being scaled to other organizations.

## I want to contribute an extension
If you're interested in contributing an extension, follow the instructions in [Contribute an Extension](https://docs.tilt.dev/contribute_extension.html) to submit a pull request. You'd likely write some Go in order to [contribute to Tilt](https://github.com/windmilleng/tilt/blob/master/CONTRIBUTING.md). Contributing an extension, however, means writing in Starlark, similar to editing your Tiltfile.

If you've already defined a function in your Tiltfile, we've designed extensions to create a clear path for you to:

- Take an existing function in your Tiltfile
- Publish that function to the [tilt-extensions repo](https://github.com/windmilleng/tilt-extensions)
- Replace that function in your Tiltfile with the published version

Some extensions that we think would be interesting include:
- kubectl commands exposed as extensions
- Validate certain tools (and their required versions) exist on the machine
- Change namespace of a Kubernetes yaml file

## Appreciation
If you submit an extension within the month of April 2020, and it's accepted and published, we'll send you a Tilt t-shirt (as long as you're in the United States, to simplify shipping). We think extensions will be a great way to further build the Tilt community, and we want to especially express our thanks to early adopters (contributors) in this way.

[The t-shirts look really awesome!](https://twitter.com/tilt_dev/status/1212769783034384384)