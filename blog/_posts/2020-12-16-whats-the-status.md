---
slug: "new-status-indicators"
date: 2020-12-16
author: han
layout: blog
title: "What's the Status? More Insight on your Resources"
image: "/assets/images/whats-the-status/telescope.jpg"
image_caption: "A stereocard of the Lick Observatory Telescope, courtesy of <a href=\"https://www.metmuseum.org/art/collection/search/813899\">The Metropolitan Museum of Art</a>"
tags:
  - kubernetes
  - local development
  - ux
---

As of Tilt v0.18.0, there's something new in the Sidebar! Each resource now shows BOTH the runtime status AND build status, rather than combining both into a single status.

![Web UI](/assets/images/whats-the-status/two-status-view.jpg)

## Why The Change?

Tilt sets up local dev environments. Your dev environment has two pieces: the binary to build, and the binary
currently running. Build-time and run-time.

When we first launched Tilt, we collapsed build status and runtime status into a single indicator. This seemed like a good tradeoff for an interface that was easy to scan, and informative _most_ of the time.

But this design could be misleading. We heard feedback like, "My resource is red. But the server is still responding to requests. What's going on?"

In these cases, the single indicator made it hard to guess at the true status. (i.e., Your binary doesn't compile, so Tilt can't update the server. But the server's still running with the last build we deployed!)

We want Tilt to support an accurate good mental model of what's happening to your services as you code, while keeping the interface digestible. 


## What's Next

We're currently working on a major revamp to make Tilt a shared dashboard for
multi-service dev environments.

The "shared" is the sticking point, because we're trying to serve everyone on your team:

- The person who set up the dashboard and understands how it works

- Everyone else who has to glance at the dashboard and _infer_ how it works

And at the same time, we want to make this feel like your team's dashboard, not Tilt's!

A lot of these changes come out of weekly conversations we've been having with
lots of teams about what they understand about their dev environments and what's
frustrating. If you'd like to chat, or want to try out some early prototypes,
please [reach out](https://docs.tilt.dev/#community)!



