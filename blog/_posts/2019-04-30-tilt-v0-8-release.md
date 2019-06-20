---
slug: tilt-v0-8-release
date: 2019-04-30T16:03:34.743Z
author: nick
layout: blog
canonical_url: "https://medium.com/windmill-engineering/tilt-v0-8-release-57d47beb38b6"
title: "Tilt v0.8 Release!"
subtitle: "New Logs View, Live Update, Bazel Support, and Improved Resource Splitting"
images:
  - featuredImage.gif
image_type: "contain"
tags:
  - docker
  - kubernetes
  - microservices
  - tilt
  - release-notes
keywords:
  - docker
  - kubernetes
  - microservices
  - tilt
  - release-notes
---

We released [Tilt v0.8](https://github.com/windmilleng/tilt) on April 22nd. This was a big release for us! So big that we’re only getting around to writing release notes now.

![](/assets/images/tilt-v0-8-release/featuredImage.gif)

Since Tilt v0.7, we’ve learned a lot about how teams develop their microservices locally. Thank you to everyone who filed bugs and feature requests. We’re hoping that each one of you finds at least one feature in this release that helps them be more productive. Let’s take a quick tour.

### New Logs View

Digging through logs locally is totally different from digging through logs in production.

When you start working on microservices, it’s easy to cobble together a solution:

* Some developers keep N terminal windows open, one for each process

* Other devs merge all the logs into one stream, prefixed by the name of the process

* The coolest devs add rainbow-colored logs 🌈

This only holds together so long.

With v0.8, Tilt now has a web view that helps you focus on the logs you want to see. Han Yu [wrote a blog post](https://medium.com/windmill-engineering/designing-a-better-interface-for-microservices-development-b0b6637a52fa) that breaks down how we’re thinking about this interface and how we expect it to evolve.

### Live Update

It’s always been easy to get started with Tilt when you just have a Dockerfile and some Kubernetes YAML.

But many users were struggling to make container updates fast.

With Tilt v0.8, you can layer “sync” and “run” steps onto an existing Dockerfile. These steps tell Tilt to automatically sync files and run commands directly in the container. You’ll see your changes much faster because you skip the overhead of creating a new container image and scheduling a new Kubernetes Pod.

Read [Dan Bentley’s guide](https://medium.com/windmill-engineering/fast-kubernetes-development-with-live-update-7b2395490d68) for more on how to get started.

### Bazel Support

If you’re developing microservices in a monorepo, Bazel is a great way to do it. Bazel scales well to large teams. There are off-the-shelf rules for building slim container images. Anyone on the team can build any binary with a consistent `bazel build`.

But Bazel looks different than other container tooling. Running multiple servers and orchestrating them is a pain. Because it tries to take over your build process end-to-end, even senior engineers struggle to make it interoperate with other tools.

With v0.8, Tilt has a few new plugin hooks that let it “shell out” to Bazel. Dan Miller has already set up a few teams on it, and [has written a guide](https://docs.tilt.dev/integrating_bazel_with_tilt.html) on how to do it yourself.

If you’re already using Bazel to build container images, try out Tilt v0.8 to make it even easier to update and understand multiple servers.

### Better Resource Splitting

If you’re upgrading from Tilt v0.7 to Tilt v0.8, we made a major change in how Tilt divides objects into buckets.

Before, we grouped everything by image name. We learned that lots of teams get started with containers by putting all their servers into a single image, then choosing which server to run based on command arguments. This makes migration much easier! But Tilt was grouping all their pods into one UI view.

Now, Tilt groups by the name of the Kubernetes owner object. If you upgrade and are confused by what you see, see [our migration guide](https://docs.tilt.dev/resource_assembly_migration.html) for more detail.

### What’s Next?

How do we know what features to work on? If you’re using Tilt day-to-day, we hope you’ve turned on analytics:

```
tilt analytics opt in
```


Analytics are like census questions: we feel queasy and invasive asking about it, but they’re invaluable for helping us prioritize engineering work. We anonymize all metrics to protect your privacy.

We’ll be at [KubeCon EU](https://events.linuxfoundation.org/events/kubecon-cloudnativecon-europe-2019/) from May 20–24. If you’re there, we’d love to meet you in-person! Come find our booth. Maybe you’ll get a sneak peek at some upcoming features.

If you’re not at KubeCon EU but want to say hi, come find us on the Kubernetes Slack in [the **#tilt** channel](https://kubernetes.slack.com/messages/CESBL84MV/) (if you’re not already a member, [get your invite here](http://slack.k8s.io)).
