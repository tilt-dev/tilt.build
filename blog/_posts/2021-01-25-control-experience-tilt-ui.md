---
slug: "control-experience-tilt-ui"
date: 2021-01-25
author: victor
layout: blog
title: "Control your Developer Experience with the new Tilt UI"
image: "/assets/images/control-experience-tilt-ui/jumpei-mokudai-KlrtaUcM8D0-unsplash.jpg"
image_caption: "Photo by <a href='https://unsplash.com/@smoothjazz?utm_source=unsplash&amp;utm_medium=referral&amp;utm_content=creditCopyText'>Jumpei Mokudai</a> on <a href='https://unsplash.com/s/photos/cockpit?utm_source=unsplash&amp;utm_medium=referral&amp;utm_content=creditCopyText'>Unsplash</a>"
tags:
  - tilt
  - ui
---

In Tilt v0.18.6, we shipped a brand new web experience in Tilt. There's now two modes to using Tilt in a browser: The overview grid panel view, and the resource logs view with multi-tab support. The first view allows you, at a glance, to get a high-level overview of all your resources running in Tilt. And the second view provides you log-level details when you need it.

![Grid view](/assets/images/control-experience-tilt-ui/grid-view.png)

![Sidebar view](/assets/images/control-experience-tilt-ui/sidebar-view.png)

## Why The Change?

This is a continuation of [the work from last year](https://blog.tilt.dev/2020/06/19/the-right-display-for-now.html) in providing an exprerience that truly caters to the needs of Tilt users. When we speak with multi-service developers, we get a variety of feedback, but typically with a few distinct themes:

- The previous UI uses a lot of screen real estate to show something that's only occasionally helpful, in particular, the logs.
- The previous UI doesn't communicate some relevant details to how Tilt works, such as resource state under the hood. There's [too much "magic"](https://blog.tilt.dev/2020/11/13/demystified.html) going on.
- After encountering laptop slowdowns (such as those often caused by Docker), Tilt no longer feels nimble, but instead too heavy-duty. Users are  reserving Tilt for only when it is aboslutely necessary. We should help users understand that the root cause is outside of Tilt, and point them toward solutions, such as pulling in the right folks to help refine their Tiltfile.

So we set out to design something that simplifies the mental model of what Tilt is doing. And in particular, by showing logs (which take a big chunk of real estate) only when the user decides to see it.

## Design Themes

We settled on a few design themes culminating in the UI in the current release:

- We drew inspiration from a monitoring dashboard style UI , where you can easily see a high-level overview of everything, at a quick glance. At the same time, starting from the overview view, you can quickly drill down to investigate a problem as necessary
- In overview grid panel view, you can get re-assurance that everything is stable, and nothing is broken. But when something does break, you can still access it quickly. And make a decision in real-time whether to take action or not.
- We want to offer more control for the developer using Tilt. We know that even for developers working in the same team, they might have very different preferences whilst working on code. Pinning and tabs are our initial concepts in making Tilt a more customizable experience for the individual developer using Tilt.

## What's Next

We're continually evolving the user experience for Tilt users. A few things on our mind as upcoming next steps:

- Alerts and notifications: You can now glance at Tilt and make sure everything is okay. But we think sometimes Tilt should nudge you a bit more and reach out for your attention if something is truly broken.
- Further customization of the web UI: Beyond pinning and tabs, and updating the Tiltfile itself, we want to offer even more customization of the Tilt experience. Sorting panels? Notifications per resource? We're thinking of ways to make the Tilt UI more _extensible_, not just customizable.
- Beyond the Tilt web UI: Some folks may want to totally eschew the Tilt web UI, and create their own UIs (like a desktop app) that talks with the [Tilt engine]((https://blog.tilt.dev/2020/11/13/demystified.html)). We want to offer that.


What do you think about this new change? [Let us know!](https://docs.tilt.dev/#community)