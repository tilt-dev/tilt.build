---
slug: more-customizable-tiltfiles-with-extensions
date: 2020-03-31
author: victor
layout: blog
title: "More customizable Tiltfiles with Extensions"
subtitle: "Share Tiltfile code snippets with the Tilt community in a streamlined platform. And get a free t-shirt!"
image: "/assets/images/more-customizable-tiltfiles-with-extensions/michael-dziedzic-XTblNijO9IE-unsplash.jpg"
image_caption: "Photo by <a href='https://unsplash.com/@lazycreekimages?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText'>Michael Dziedzic</a> on <a href='https://unsplash.com/?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText'>Unsplash</a>"
tags:
  - tilt  
keywords:
  - extensions
  - tilt
  - tiltfile
---

Since [releasing Tilt](/2018/08/28/how-tilt-updates-kubernetes-in-seconds-not-minutes.html), we’ve seen the Tilt community actively share code snippets of Tiltfile functionality in [Slack #tilt](https://kubernetes.slack.com/messages/CESBL84MV/), including ideas such as forcing resources into different namespaces, injecting sidecars, and even running tests. So we've created the open source Extensions platform to encourage this community collaboration in more structured fashion.

## What's an extension, exactly? And how do you use it?
An extension is simply a packaged function you call from within your Tiltfile. Simply import the extension (specifying the extension name and function name), and call it, all right inside your Tiltfile. 

For example, to use the `hi()` function in the [`hello_world` extension](https://github.com/windmilleng/tilt-extensions/tree/master/hello_world), first [`load()`](https://docs.tilt.dev/api.html#api.load) it by including this command in your Tiltfile:

```
load('ext://hello_world', 'hi')
```

Then call `hi()` later in you Tiltfile to print "Hello World!".

Read the [docs](https://docs.tilt.dev/extensions.html) for additional details and look at the [tilt-extensions repo](https://github.com/windmilleng/tilt-extensions) for a list of available extensions. But it's really that simple!

## I want to contribute an extension
If you're interested in contributing an extension, it's really easy. You just need to know some basic Python syntax. And if you've had practice editing a Tiltfile, that's good enough. You definitely do not need to know Go (which Tilt is written in) in order to contribute. Follow the simple instructions in [Contribute an Extension](https://docs.tilt.dev/contribute_extension.html) to submit a pull request.

If you submit an extension within the month of April 2020, and it's accepted and published, we'll send you a free Tilt t-shirt. [They look really awesome](https://twitter.com/tilt_dev/status/1212769783034384384)!