---
title: Overview
subtitle: Tilt Tutorial
layout: docs
permalink: /tutorial/index.html
redirect_from:
 - /tutorial.html
---
This tutorial is designed to introduce the key concepts of Tilt.

{{ site.url }}

If you're new to multi-service containerized development, don't panic: this tutorial focuses on Tilt.
We won't dive into the internals of `Dockerfile` or Kubernetes YAML.

Throughout the tutorial, we'll refer to the [`tilt-avatars`][repo-tilt-avatars] project.
The full source is available on [GitHub][repo-tilt-avatars] to refer to or checkout locally to follow along interactively.
> 💡 In the first section, we'll make sure you've got the necessary prerequisites installed!

## Table of Contents
1. Preparation (Optional)

   If you want to follow along interactively, you'll need Tilt, Docker, and the sample project source code.
   We know it can be daunting, so we've tried to streamline the experience and will get you going from scratch in under 10 minutes!

2. Tilt Up, Up, and Away

   Say hello to your new best friend: `tilt up`.
   This section introduces the Tilt control loop and will forever change the way you think about development tools.
   
3. Tilt UI

   Welcome to the command center.
   The Tilt UI aggregates logs across all your services, provides at at-a-glance view of your dev environment's state, and so much more.
   Did we mention it also looks ✨fantastic✨ while doing so?

4. Smart Rebuilds with Live Update

   Syncing file changes is just the start.
   Tilt's Live Update provides the flexibility to support all languages and frameworks even if they don't offer native hot reload support.
   The only downside is you won't have time for [office sword fights][xkcd-compile] anymore.

5. What's Next? I Need More!

   Want to know _everything_ there is to know about Tilt?
   Need to learn more about multi-service development?
   We've got you covered with references no matter where you are in your Tilt journey.
   Plus, rumor has it that one of the links is actually a goose in disguise!

[repo-tilt-avatars]: https://github.com/tilt-dev/tilt-avatars
[xkcd-compile]: https://xkcd.com/303/
