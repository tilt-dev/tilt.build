---
title: Fast Build With Your Existing Dockerfile
layout: docs
---

Want to take advantage of `fast_build` for live updates of your running containers, but don't want to redo your whole Dockerfile for it? Now you don't have to.

You can read more about the _old_ `fast_build` syntax in [Optimizing A Tiltfile](/fast_build.html), but in brief, you specified a stripped-down version of your Dockerfile, plus a series of `COPY/ADD` and `RUN` calls. This set of steps could be used to _both_:

1. Build your image for the first time, and

2. Update a live container that is already running that image

Well, good news: you can now specify steps for (1) and (2) separately! That is, you can use your existing Dockerfile when building the image from scratch, and add specific files/run specific commands when updating in place.

```python
img_name = 'myproject/server'

# (1) use your existing Dockerfile for image builds
server = docker_build(img_name, ',/server')

# (2) specify how to update the image in place
server.add('./server/static', '/server/static')  # copy over static files
server.add('./server/app', '/server/app')  # copy over app files
server.run('pip install -r /server/app/requirements.txt',
           trigger='./server/app/requirements.txt')  # if requirements have changed, pip install
```

Tada! Extra speed, without having to maintain different Dockerfiles for dev and prod.
