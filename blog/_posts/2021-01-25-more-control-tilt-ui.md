---
slug: "more-control-tilt-ui"
date: 2021-01-25
author: victor
layout: blog
title: "Offering More Control in the New Tilt UI"
image: ""
tags:
  - tilt
  - ui
---

In Tilt v0.18.6, we shipped a brand new web experience in Tilt. There's now two modes to using Tilt in a browser: The overview grid panel view, and the resource logs view with multi-tab support. The first view allows you, at a glance, to get a high-level overview of all your resources running in Tilt. And the second view provides you log-level details when you need it.

_Image of new UI here_

## Why The Change?

This is a continuation of [the work from last year](https://blog.tilt.dev/2020/06/19/the-right-display-for-now.html) in providing an exprerience that truly cater to the needs of Tilt users. When speaking with multi-service developers, we got a variety of feedback, but with a few distinct themes:

- The previous UI uses a lot of screen real estate to show something that's only occasionally helpful, in particular logs.
- The previous UI doesn't communicate some relevant details to how Tilt works, such as resource state under the hood. There's [too much "magic"](https://blog.tilt.dev/2020/11/13/demystified.html) going on.
- After encountering laptop slowdowns (such as those often caused by Docker), Tilt no longer feels nimble, but instead too heavy duty. Users were then reserving Tilt for only when it was aboslutely necessary. We should help users understand that the root cause is outside of Tilt, and point them solutions, such as pulling in the right folks to help.

So we set out to design something that simplifies the mental model of what Tilt is doing. And in particular, by showing logs (which take a big chunk of real estate) only when the user decides to see it.

## Design themes

We settled on a few design themes culminating in the UI in the current release:

- We drew inspiration from a monitoring dashboard style UI , where you can easily see a high-level overview of everything, at a quick glance. At the same time, starting from the overview view, you can quickly drill down to investigate a problem as necessary
- In overview grid panel view, you can get re-assurance that everything is stable, and nothing is broken. But when something does break, you can still it quickly. And make a decision in real-time whether to take action or not.
- We want to offer more control for the developer using Tilt. We know that even for developers working in the same team, they might have very different preferences whilst working on code. Pinning and tabs are our initial concept in making Tilt a more customizable experience for the individual developer using Tilt.


## What's Next