---
slug: "joining-docker"
date: 2022-05-24
author: nick
layout: blog
title: "Joining Docker"
image: "/assets/images/joining-docker/logos.png"
image_type: "contain"
description: "Fixing the pains of microservice development for Kubernetes at a new company."
tags:
- tilt
---

Big news! The [Tilt team](https://tilt.dev/) is joining Docker. The [Tilt project](https://github.com/tilt-dev/tilt) is joining too.

We think this is a great fit and I will tell you why.

## The Problem

Modern apps are made of so many services. They’re everywhere.

Every team we talk to is trying to figure out how to set up environments to run
their apps in dev.

Simple
[`start.sh`](https://blog.tilt.dev/2018/12/05/tilt-is-the-start-sh-script-of-my-dreams.html)
scripts inevitably grow into mini bespoke orchestrators. They need to start
servers in the right order, update them in-place, and monitor when one is
failing.

We built Tilt, a dev environment as code for teams on Kubernetes, to help solve
these problems.

Whether your dev env is local processes or containers, in a local cluster or a
remote cloud, Tilt keeps you in flow and your feedback loops fast.

So how does this make sense at Docker?

When we started building Tilt in 2018, we thought of Docker as the container
company selling Swarm to enterprises. In 2019, the [Docker’s Next Chapter](https://www.docker.com/blog/docker-next-chapter-advancing-developer-workflows-for-modern-apps/) blog
post announced a change in focus to invest more in great tools for developers
and development teams to help them spend more time on innovation, less time on
everything else.

Tilt interoperates with Docker Buildkit, Docker Desktop, and Docker
Compose. Improvements to these tools help Tilt users too! We always had a hunch
that our product roadmaps might overlap. And in the years since Docker focused
on developers, we’ve been converging more and more.

Once we started talking more with Docker, we found more in common than just a
problem space including:

- A product philosophy around deeply understanding devs’ existing workflows, so
  we can make dramatic improvements in user experience that feel magic;

- An engineering philosophy around patterns and flexibility so devs can adapt their tools to their needs;

- A business philosophy around building a sustainable company so we can continue
  to make great free, open-source tools for every developer.

So you could say we got along. What’s next?

## What Does a Combined Tilt + Docker Look Like?

Tilt will remain open-source. It’s great! You should try it! We’ll still be
responding to [issues](https://github.com/tilt-dev/tilt/issues) and hanging out
in [the community slack channel](https://docs.tilt.dev/#community).

But this has never been about Tilt the technology. Or even about Kubernetes. Our
history is full of experiments.

Dan Bentley and I started hacking on ideas in 2017. We knew we were unhappy
about [microservice dev](https://blog.tilt.dev/2019/09/05/put-down-particle-accelerator.html). But we weren’t sure what the first stepping stone might
be.

This was more of a research project than a company. Some examples:

- Our first prototype was a more interactive, developer-focused CI.

- We almost trolled ourselves into becoming [a Bazel
  company](https://medium.com/windmill-engineering/bazel-is-the-worst-build-system-except-for-all-the-others-b369396a9e26).

- We bought two lab coats, poster board, glue, and glitter so we could show off
  our prototypes at [the GothamGo
  conference](https://medium.com/windmill-engineering/12-gothamgo-talks-that-could-have-used-more-glitter-72ee38ae9d94).

- We built many weird demos: (1) Mishell (an interactive multi-service shell)
  represented by a French-speaking hermit crab named Michel, and PETS (Process
  for Editing Tons of Services) represented by three cats overwhelmed by
  microservice dev. Our teammate Han Yu had a blast with mascot design (yeah to
  Docker for animal mascots):

![](/assets/images/joining-docker/mascots.png)

The first version of Tilt was a bare-bones terminal app to update containers in
a Kubernetes cluster. It resonated immediately.

Tilt has grown a lot since then. Running all or just a few of your services [is
easier than ever](https://blog.tilt.dev/2022/03/03/resource-catalog.html).

Why did we focus on Kubernetes? Kubernetes contains [a few simple, brilliant
ideas](https://blog.tilt.dev/2021/03/18/kubernetes-is-so-simple.html) for how to operate apps. Tilt borrows a lot of ideas ([and a lot of core
libraries](https://www.youtube.com/watch?v=uKF8v9X6hSE)) from Kubernetes on how to be scriptable and adaptable.

But more importantly, the Kubernetes community is lovely. They appreciate
[Goose-themed trolling](https://twitter.com/veekorbes/status/1400139022580826117). We found a worldwide community of people enthusiastic
about building better tools.

We’re sad we missed everyone at Kubecon EU this year! We didn’t know if this
deal would finish before, during, or after the conference.

That said, over the next couple months, we’ll be swapping notes with the Docker
team about what we’ve both learned and what we’ve both tried.

We don’t know yet where this will take us. Maybe you’ll see Tilt & Kubernetes
features in Docker Compose. Or maybe you’ll see Docker Desktop features in Tilt.

There will be research and tinkering, where we'll be in our lab coats and
glitter, but do expect us to bring the power of Tilt to Docker.

---

This announcement was originally posted to the Docker blog: ["Welcome Tilt:
Fixing the pains of microservice development for
Kubernetes."](https://www.docker.com/blog/welcome-tilt-fixing-the-pains-of-microservice-development-for-kubernetes/)
