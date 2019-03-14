---
title: Fast Build With Your Existing Dockerfile
layout: docs
---

Want to take advantage of `fast_build` for lightning-fast live updates of your running containers, but don't want to redo your whole Dockerfile for it? Now you don't have to.

You can read more in [Optimizing A Tiltfile](/fast_build.html), but in brief, when you make a call to `fast_build`, you specify a set of instructions that can be used to _both_:

1. Build your image for the first time, and
2. Update a live container that is already running that image (so that you don't have to rebuild the whole dang thing; you just push up some changed files, maybe run a command, and you're done).

In order to express an image as a set of steps that could equally be used to build from scratch or update in place, we required that you supply a stripped-down version of your Dockerfile, and specify all `COPY/ADD` and `RUN`'s in your Tiltfile.
```python
img_name = 'myproject/server'
(fast_build(img_name, 'Dockerfile.stripped', entrypoint='/go/bin/server')
  .add('./server', '/go/src/myproject/server')
  .run('go install myproject/server'))
```

Who wants to maintain two separate Dockerfiles, when part of the point of Tilt is to get your dev environment as close to your prod environment as possible?

Well, now we have a solution. You can now specify steps for (1) and (2) separately: use your existing Dockerfile when building the image from scratch, and add specific files/run specific commands when updating in place.

```python
img_name = 'myproject/server'

# use your existing Dockerfile for image builds
server = docker_build(img_name, ',/server')

# specify how to update the image in place
server.add('./server', '/go/src/myproject/server')
server.run('go install myproject/server')
```

Tada! Extra speed, without having to maintain different Dockerfiles for dev and prod.
