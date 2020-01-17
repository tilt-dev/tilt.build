---
slug: the-kubectl-with-a-thousand-faces
date: 2019-11-12
author: nick
layout: blog
title: "The Kubectl with a Thousand Faces"
subtitle: "Commit of the Month / October 2019"
image: yuri-bodrikhin-dXLnq8z8x4k-unsplash.jpg
image_needs_slug: true
image_caption: "Photo by <a href='https://unsplash.com/@bodriy?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText'>Yuri Bodrikhin</a> on <a href='https://unsplash.com/backgrounds/art/diamond?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText'>Unsplash</a>"
tags:
  - kubernetes
  - ux
---

Welcome to the Commit of the Month, the blog post series where we highlight
recent work on Tilt.

October's commit is

[28f7aba7cb73d42194deaba0543be514f3c858bf](https://github.com/windmilleng/tilt/commit/28f7aba7cb73d42194deaba0543be514f3c858bf)

Or for you humans:

[facets: show the applied k8s yaml](https://github.com/windmilleng/tilt/pull/2440)

## What Does it Do?

When you're watching a resource in Tilt, you used to see two tabs: Logs and Alerts.

The Logs tab displays the most recent output of building and running something
on Kuberenetes. That includes image build logs, pod logs, events that popped up,
etc. All of it is in recency order.

The Alerts tab displays messages that we think you should look at Right Now,
like build failures or pod crashes.

This commit adds data to a third tab, the Facets tab.

![A screenshot of Facets](/assets/images/the-kubectl-with-a-thousand-faces/facet-screenshot.png)

Facets are diagnostic information about your dev environment. If your dev env is
misbehaving, and you're not sure why, you can dig into the facets tab to get
more detail on what Tilt knows. This includes:

- The Kubernetes objects that Tilt applied to your cluster
- The most recent build log
- The build history

Maybe these details will point to the problem. Maybe they'll help rule out a few
suspects. Maybe they won't help at all!

## Wait, Why Does it Do That?

Kubernetes exposes a ton of its internal state via
its API. `kubectl` lets you systematically query most of that state.

That makes `kubectl` the
[monkey's paw](https://en.wikipedia.org/wiki/The_Monkey%27s_Paw) of command-line
interfaces. It will always give you what you ask for. But it may not give you
what you need. A big part of learning Kubernetes is just learning how to navigate `kubectl`.

We want to make Kubernetes a pleasant development environment for everyone, not
just `kubectl` pros.

On team Tilt, we spend a lot of time talking about how to make the right
information available when you need it. We don't want to hide information from
you. But we also don't want to overwhelm you with irrelevant dumps of Tilt's
internal state.

How does a vague idea to display some internal Kubernetes detail evolve into an
essential "check engine" light?

The Facets tab is a laboratory where we try out new displays. When we're hacking
on our own projects and have a problem, we check the Facets tab to see if the
data helps. As we put this to use and watch other teams play with it, we expect to
get a better sense of when this information should "pop up" in other places in
the interface.

So the next time you're puzzling over why your app is broken, check the facets
tab! We'd [love to know](https://tilt.dev/contact) if you found it useful, or even if you didn't.

Thanks [Matt](https://github.com/landism)!

## Further Reading

[Lessons from Building Static Analysis Tools at Google](https://cacm.acm.org/magazines/2018/4/226371-lessons-from-building-static-analysis-tools-at-google/fulltext),
a great overview of some of the trade-offs in tooling that tries to
surface high-quality information to developers.



