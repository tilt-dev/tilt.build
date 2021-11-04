---
title: Overview
subtitle: Tilt Tutorial
layout: docs
sidebar: gettingstarted
permalink: /tutorial/index.html
redirect_from:
 - /tutorial.html
---
This tutorial is designed to introduce the key concepts of Tilt.

If you're new to containerized development, don't panic: this tutorial focuses on Tilt.
We won't dive into the internals of `Dockerfile` or Kubernetes YAML.

Throughout the tutorial, we'll refer to the [`tilt-avatars`][repo-tilt-avatars] project.
The full source is available on [GitHub][repo-tilt-avatars] to refer to or checkout locally to follow along interactively.
> 💡 In the first section, we'll make sure you've got the necessary prerequisites installed!

## Table of Contents
1. **Preparation (Optional)**

   If you want to follow along interactively, you'll need Tilt, Docker, and the sample project source code.
   We know it can be daunting, so we've tried to streamline the experience and will get you going from scratch in under 10 minutes!

2. **Launching & Managing Resources**

   Say hello to your new best friend: `tilt up`.
   This section introduces the Tilt control loop and will forever change the way you think about development tools.
   
3. **Tilt UI**

   Welcome to the command center.
   The Tilt UI aggregates logs across all your services, provides at at-a-glance view of your dev environment's state, and so much more.
   Did we mention it also looks ✨fantastic✨ while doing so?

4. **Code. Update. Repeat.**

   See Tilt in action and learn how Tilt optimizes your dev experience by building the right thing at the right time.

5. **Smart Rebuilds with Live Update**

   Syncing file changes is just the start.
   Tilt's Live Update provides the flexibility to support all languages and frameworks even if they don't offer native hot reload support.
   The only downside is you won't have time for [office sword fights][xkcd-compile] anymore.


## What's Next?
Ready to use Tilt in your _own_ project?
Fantastic!
The [Write a Tiltfile Guide](/tiltfile_authoring.html) will apply what you'll learn in this tutorial to write a `Tiltfile` from scratch and supercharge your dev environment. 

[repo-tilt-avatars]: https://github.com/tilt-dev/tilt-avatars
[xkcd-compile]: https://xkcd.com/303/
