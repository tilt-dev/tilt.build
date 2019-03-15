---
title: Features
layout: docs
---

`.tiltignore`
---
`.tiltignore` allows you to tell tilt about file changes that should not cause Tilt to build your code.

Tilt looks for a file named `.tiltignore` in the same directory as your `Tiltfile` and parses it using the [.dockerignore syntax](https://docs.docker.com/engine/reference/builder/#dockerignore-file). If a path is filtered by this file, it will not cause Tilt to build your code, but it is still eligible to be used as part of the docker build itself.
