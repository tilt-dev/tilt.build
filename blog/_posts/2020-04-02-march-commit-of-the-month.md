---
slug: march-2020-commit-of-the-month
date: 2020-04-02
author: dmiller
layout: blog
title: "Accessibility Matters"
subtitle: "Commit of the Month: Improve Accessibility of Status Icons"
image: /assets/images/march-2020-commit-of-the-month/featuredImage.jpg
image_caption: "A colorblind test. Photo by daltonien on <a href='https://flickr.com/photos/nicolasdumond79/13782659973'>Flickr</a>."
image_type: "contain"
tags:
  - tilt
  - cotm
  - accessibility
keywords:
  - tilt
  - accessibility
---

Details matter. Especially when those details impact usability. That’s why we paid close attention when we got reports that Tilt’s terminal UI was not colorblind friendly. Take a look at this screenshot:

![A photo of the Tilt UI with green and red icons next to each resource](/assets/images/march-2020-commit-of-the-month/colorblind1.png)

Can you tell at a glance which of these resources are up, and which ones have errored? It’s hard. If you were red-green colorblind, it would be even harder. It might look something like this:

![A photo of the Tilt UI with green and red icons next to each resource modified to show what it might look like to a colorblind person](/assets/images/march-2020-commit-of-the-month/colorblind1-mod.png)

While we expect most people to be using the Web UI (which is more fully featured though it exhibited a similar problem that was [fixed in a different commit](https://github.com/windmilleng/tilt/commit/0c1985c3e2ddeeedce7fb5633753d23730887f62)) if your workflow lives in the terminal we want to support that too. So in [842b83131f78431dd1ba8522e6288226a09c4cfc](https://github.com/windmilleng/tilt/commit/842b83131f78431dd1ba8522e6288226a09c4cfc) we improved the terminal UI’s accessibility by adding status icons that are structurally distinct from one another in addition to having distinct hues. Now Tilt’s status icons look like this:

![A photo of the Tilt new UI with green and red icons of different shapes for each different state](/assets/images/march-2020-commit-of-the-month/now.png)

Even in grayscale, it’s now easy to tell that these icons represent different states.

Thanks to Han Yu and Nick Santos for their work on this! 

[Over two billion people](https://www.who.int/news-room/fact-sheets/detail/blindness-and-visual-impairment) in the world have visual impairments, and we want them to have a great experience too. 

The only way to get there is with deliberate effort, and we’d like to thank the Tilt community members who brought this to our attention. If you spot any other accessibility concerns in Tilt, please [open a GitHub issue](https://github.com/windmilleng/tilt/issues/new)!
