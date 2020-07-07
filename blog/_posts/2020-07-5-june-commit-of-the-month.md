---
slug: June-2020-commit-of-the-month
date: 2020-07-04
author: dmiller
layout: blog
title: "I heard you like extensions"
subtitle: "So I put extensions inside your extensions so you can extend your extension while you extend Tilt"
image: /assets/images/june-2020-commit-of-the-month/featuredImage.jpg
image_caption: "Photo by raincrystal on <a href='https://www.flickr.com/photos/catherine_rain/2240344654'>Flickr</a>."
image_type: "contain"
tags:
  - tilt
  - cotm
  - extensions
keywords:
  - tilt
---

June's commit of the month is [0860db](https://github.com/tilt-dev/tilt/commit/0860db76f8cbaa7dae551f7800f5480593a2ec95)! To explain why let's start with a bit of background on Tilt Extensions.

[Extensions were released](2020/04/01/more-customizable-tiltfiles-with-extensions.html) a couple months ago to make it easier to share Tiltfile functionality with other Tilt users. You can think of Tilt Extensions as a Tiltfile package manager.

You can see all of the currently available Tilt Extensions in the [Tilt Extensions Repository](https://github.com/tilt-dev/tilt-extensions). More than 10 extensions! Some of them, like the [`git_resource`](https://github.com/tilt-dev/tilt-extensions/tree/master/git_resource) extension, already have multiple contributors on their own.

It's natural that as this ecosystem grows, extension authors would want to use others' extensions in their own. For example, many extensions could benefit from using the [`local_output` extension](https://github.com/tilt-dev/tilt-extensions/tree/master/local_output). Unfortunately we made the decision early on to disallow loading extensions from other extensions in order to avoid having to deal with the [diamond dependency problem](https://www.well-typed.com/blog/2008/04/the-dreaded-diamond-dependency-problem/). The diamond dependency problem is essentially: what happens if packages transitively depend on different versions of the same package? For example:

![Package A uses Package B and C. Package B uses package D version 1.0, package C uses package D version 1.1](/assets/images/june-2020-commit-of-the-month/diamond.png)

There are no easy solutions to the diamond dependency problem, so rather than trying to solve it right away, we decided to punt on it and see how extensions would be used. We've taken some precautionary measures, like vendoring all dependencies, but it seems too useful to keep turned off. So in June's commit of the month we enabled loading extensions from other extensions.

The history of software is rife with examples of things being built on top of other things. We are all building on the shoulders of giants.

Thanks to all of the folks who have contributed Tilt Extensions so far!