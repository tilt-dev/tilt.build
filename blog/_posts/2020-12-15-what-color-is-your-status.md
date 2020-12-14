---
slug: "what-color-is-your-status"
date: 2020-12-14
author: han
layout: blog
title: "What Color is Your Status"
image: "/assets/images/ctlptl/joe-cox-HVXujL72Dug-unsplash.jpg"
image_caption: "Photo by <a href=\"https://unsplash.com/@joecoxx?utm_source=unsplash&amp;utm_medium=referral&amp;utm_content=creditCopyText\">Joe Cox</a> on <a href=\"https://unsplash.com/s/photos/ducks-puddle?utm_source=unsplash&amp;utm_medium=referral&amp;utm_content=creditCopyText\">Unsplash</a></span>"
tags:
  - kubernetes
  - local development
  - ux
---

What happened here?

[snapshot]

As of Tilt v0.18.0, every resource gets two colors! They might even be the same
color.

You may ask "Why do we need two colors? One color seemed perfectly fine!"

We're glad you asked!

## Why Two Colors is Better Than One

Tilt sets up local dev environments. 

Your dev environment has two pieces: the binary to build, and the binary
currently running. Build-time and run-time.

As a short hand, collapsing build status and runtime status into one was a way
to give you a single place to glance.

But it wasn't very transparent. People regularly complained: my resource is
red. But the server is still responding to requests. Does that mean Tilt made a
mistake?

The single status made it hard to guess what was going on in some cases: your
binary doesn't compile, so Tilt can't update the server.

We're still investigating ways to give users a single place to glance to see
what they need to take action on.  But we want to make it clear and transparent,
and help you to understand what part of the build is failing.

## What's Next

We're currently working on a major revamp to make Tilt a shared dashboard for
multi-service dev environments.

The "shared" is the sticking point, because we're trying to serve everyone on your team:

- The person who set up the dashboard and understands how it works

- Everyone else who has to glance at the dashboard and _infer_ how it works

And at the same time, we want to make this feel like your team's dashboard, not Tilt's!

A lot of these changes come out of weekly conversations we've been having with
lots of teams about what they understand about their dev environments and what's
frustrating. If you like complaining, or want to try out some early prototypes,
please reach out!



