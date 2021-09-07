---
slug: "tilt-news-august-2021"
date: 2021-08-31
author: l
layout: blog
title: "Tilt News, August 2021"
image: "/assets/images/tilt-news-august-2021/onlydev.jpg"
description: "A round-up of our latest trolling and feature announcements."
tags:
  - news
---

Hey Tilters! 

Hard to believe it’s almost September, innit? Welp, we dun got a ton of
Tilt-related news for ya!

## Features

**Resource grouping has arrived!** No more scrolling through long lists or services
and custom functionality on the sidebar. Now you can group them all in ways that
make sense for your application and show & hide them as you please. Check out
[Lizz’s article](https://blog.tilt.dev/2021/08/09/resource-grouping.html) on it for more details.

![resource grouping demo](/assets/images/resource-grouping/demo.gif)

More **extensibility** options! As Tilt’s internal API matures, it’s becoming
easier and easier to add functionality to it without having to deal with Tilt’s
internal codebase. In [this
article](https://blog.tilt.dev/2021/08/17/write-more-bash.html) Nick describes
how we created the [cancel
button](https://github.com/tilt-dev/tilt-extensions/tree/master/cancel)
extension using nothing but Bash.

If creating new functionality in Tilt is important for your team, definitely
check it out!

## Kubecon

Two Tilters will be speaking at KubeCon this October! Both talks are
tangentially related to Tilt, and mostly about Kubernetes, the ideas behind
Kubernetes, and how those ideas can—and should!—affect your life as a developer.

Nick’s talk, [The Control Loop As An Application Development
Framework](https://kccncna2021.sched.com/event/lV1E), focuses on the Kubernetes
ideas and libraries that Tilt is built on top of. The Kubernetes libraries have
a lot of tools to help us build robust systems.

L’s talk, [Beyond Kubernetes
Security](https://kccncna2021.sched.com/event/lV4f), is, well, not exactly a
talk. More of a hacking movie. Think Hackers (1995) but with real hacks and even
sillier special effects. It’s very, very extra, but there’ll be no rollerblades,
unfortunately!

## VSCode Extension Prototype

Speaking of things that are very, very extra… We’ve been wanting to experiment
with a VSCode extension for a while, and Tilt’s API has now reached a point
where a VSCode extension is super easy to build. So we decided to build one,
just for fun.

This is definitely not meant for real use just yet—it honks!—but more as a way
to assess how much the new API let’s us do. If by any chance you’re interested
in a real version of this, smash that reply button :-)

Here’s [the very extra overly produced
video](https://twitter.com/ellenkorbes/status/1419717201536356361) L made about
it, and [here’s the link to the VSCode
marketplace](https://marketplace.visualstudio.com/items?itemName=tilt-dev.tilt-status)
in case you’d like to download it and try it out. Once again: If this is your
jam, do let us know about it!

![vscode status](/assets/images/tilt-news-august-2021/status.jpg)

## Pixeltilt

Lastly, if you’re familiar with our to-go example project,
[Pixeltilt](https://github.com/tilt-dev/pixeltilt/), is has been revamped to
feature Tilt’s latest features e.g. buttons and resource groups, and the
codebase has been cleaned up and more intuitively commented.

If you’re new at Tilt and wanting to try it out, there has never been a better
time to get started! :-)

![pixeltilt](/assets/images/tilt-news-august-2021/pixeltilt.jpg)

_Originally sent to [the Tilt News mailing
list](https://tilt.dev/subscribe). View
[in-browser](https://mailchi.mp/tilt.dev/tilt-dev-news-august-2021)._
