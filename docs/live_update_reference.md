---
title: Live Update Reference
layout: docs
---
##### (This doc provides the technical specifications of Tilt's `LiveUpdate` functionality. For a tutorial that walks you through a sample project, see [Optimizing a Tiltfile](live_update_tutorial.html).)

When specifying how to build an image (via `docker_build()` or `custom_build()`), you may optionally pass the `live_update` arg.

`live_update` takes a list of `LiveUpdateSteps` that tell Tilt how to update a running container in place. (This allows us to skip Docker build/push, take advantages of on-disk caches, and generally give you a faster development experience.)

The list of `LiveUpdateSteps` must be, in order:
- 0 or more `fall_back_on`	
- 0 or more `sync`	
- 0 or more `run`	
- 0 or 1 `container_restart`	

When a file changes:	
   1. If it matches any of the files in a `fall_back_on` step, we will fall back to a full rebuild + deploy (i.e., the normal, non-live_update process).	
   2. Otherwise, if it matches any of the local paths in `sync` steps, a live update will be executed:	
        1. copy any changed files according to `sync` steps	
        2. execute any relevant `run` steps	
        3. restart the container if a `container_restart` step is present
