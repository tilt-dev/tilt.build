---
title: Live Update Reference
layout: docs
---
##### (This doc provides the technical specifications of Tilt's `LiveUpdate` functionality. For a tutorial that walks you through a sample project, see [Faster Development with Live Update (Tutorial)](live_update_tutorial.html).)

When specifying how to build an image (via `docker_build()` or `custom_build()`), you may optionally pass the `live_update` arg.

`live_update` takes a list of `LiveUpdateSteps` that tell Tilt how to update a running container in place (instead of paying the cost of building a new image and redeploying).

The list of `LiveUpdateSteps` must be, in order:
- 0 or more [`fall_back_on`](api.html#api.fall_back_on) steps
- 0 or more [`sync`](api.html#api.sync) steps
- 0 or more [`run`](api.html#api.run) steps
- 0 or 1 [`restart_container`](api.html#api.restart_container) steps

When a file changes:
   1. If it matches any of the files in a `fall_back_on` step, we will fall back to a full rebuild + deploy (i.e., the normal, non-live_update process).
   2. Otherwise, if it matches any of the local paths in `sync` steps, a live update will be executed:
        1. copy any changed files according to `sync` steps
        2. for every `run` step:
            * if the `run` specifies one or more `triggers`, execute the command iff any changed files match the given triggers
            * else, simply execute the command
        3. restart the container if a `restart_container` step is present. (This is tantamount to re-executing the container's `ENTRYPOINT`.)

## LiveUpdateSteps
Each of the functions above returns a `LiveUpdateStep` -- an object like any other, i.e. it can be assigned to a variable, etc. That means that something like this is perfectly valid syntax:
```python
sync_src = sync('./source', '/app/src')
sync_static = sync('./static', '/app/static')
docker_build('my-img', '.', live_update=[sync_src, sync_static])
```

As part of Tiltfile validation, we check that all of the `LiveUpdateSteps` you've created have been used in at least one Live Update call. If not, we throw an error.

### [sync(local_path: str, remote_path: str)](api.html#api.sync)
Even though `sync` steps must come _after_ any `fall_back_on` steps (if the latter are present), we'll discuss them first, since they are the backbone of a Live Update. To wit: _Tilt will only run a Live Update if it detects a change to one or more files matching a `sync` step._

A `sync` call takes two args: the local path of a file/directory, and the remote path to which Tilt should sync that file/directory if it changes. (This includes deleting the file remotely if it is deleted locally.)

#### What files can I sync? How are builds triggered?
When you tell Tilt how to build an image, you specify some set of files to watch. In the case of a `docker_build` call, Tilt watches the directory that you pass as `context`. Your sync'd local paths must fall within that context. (If you're using `custom_build`, all of the above applies, only with `deps` in place of `context`.)

![An illegal "sync"](/assets/img/liveupdate-sync-illegal.png)

The `sync` here is invalid, because it attempts to sync files that we're not even watching. (To put it another way: there's no way for those files to get into the container in the first place, because they would never be included in the Docker build.) If this is functionality you need, [let us know](https://tilt.dev/contact). 

![Valid use of "sync" (all sync'd files are subsets of docker_build.context)](/assets/img/liveupdate-sync-docker-context.png)
Here are some valid `sync`s. A change to any of the green files will kick off a Live Update, because they match a `sync` step. A change to any of the yellow files will kick off a full Docker build + deploy, because they're part of the Docker context but we don't have instructions on how to Live Update them. (Coming soon: a way to be to be more selective in what parts of your Docker context Tilt watches!)

![How to use "sync" with multiple dependent docker images](/assets/img/liveupdate-sync-dep-images.png)

If you have multiple docker images that depend on each other, you can sync files from anywhere within the contexts of any of the images. (In this diagram, Tilt is building two images; the blue image depends on -- i.e. `FROM`'s -- the yellow image.)

The rule of thumb is: you can `sync` it if Tilt is watching it, and Tilt will watch it if it's in a `docker_build.context` or `custom_build.deps`.


#### Let's review
For instance, take the following sync statements:
```python
docker_build('my-img', './server', live_update=[
    sync('./server/src', '/app'),
    sync('./server/package.json', '/app/web/package.json')
])
```
1. change to `./server/src/A.txt` => synced to `/app/A.txt`
2. change to `./server/package.json` => synced to `/app/web/package.json`
3. change to `./server/some_file.txt` => doesn't match any `sync` statements, but _does_ match the `docker_build` context; instead of a Live Update, Tilt performs a Docker Build
3. change to `./stuff.txt` => doesn't match a `sync` statement OR the `docker_build` context; nothing happens 

### [fall_back_on(files: str || List[str])](api.html#api.fall_back_on)
This step is optional, though if provided, it must come at the beginning of the `live_update` call. The argument is a filepath (string) or multiple filepaths (list of strings) on your local machine, either absolute or relative to the Tiltfile. Whenever Tilt detects a change to your local filesystem that would otherwise trigger a LiveUpdate, it first checks if it matches any `fall_back_on` files; if yes, instead of doing a LiveUpdate, Tilt _falls back_ to a full rebuild + deploy.


### [run(cmd: str, trigger=None: str || List[str])](api.html#api.run)
The first argument to `run` is a the command to be executed _on the running container_. Currently, all commands are executed from `/`, so be sure to use absolute paths!

Currently, all of your `run` steps must come after all of your `sync` steps. (If you need different behavior, let us know!) If you provide multiple `run` steps, the commands will be executed in the order given. 

#### Run triggers

The second arg, `trigger`, is optional. If you don't provide a trigger, then the command is executed on the container whenever Tilt performs a LiveUpdate (i.e. whenever Tilt detects a change to one or more files matching a `sync`).

A trigger is a filepath (string) or multiple filepaths (list of strings) on your local machine, either absolute or relative to the Tiltfile. If a trigger is provided, Tilt _only_ executes the command if a changed file matches one the trigger paths.

Note that specifying a file as a trigger does _not_ tell Tilt to watch and/or sync that file; that is, all `trigger` files must also be included in a `sync` step.

Let's walk through what will and won't happen when various files change, given this example Tiltfile:
```python
docker_build('my-img', '.', live_update=[
    sync('./src', '/app'),
    run('/app/setup.sh'),
    run('cd /app/web && yarn install', trigger='./src/web/yarn.lock'),
    run('/app/run_configs.sh', trigger=['./configs/foo.yaml', './configs/bar.yaml'])
])
```
1. change to `./src/main.py` => this file matches a sync step, so we run the Live Update. We run `setup.sh`, because it has no triggers and so runs on every Live Update. We run neither of the other `run` steps, b/c this file doesn't match any of their triggers.
2. change to `./src/web/yarn.lock` => run the Live Update; run `setup.sh`; run `cd /app/web && yarn install`, because this file matches that command's trigger
3. change to `./configs/foo.yaml` => whoops, this file doesn't match any `sync` steps! Even though it matches a trigger (for the third `run`), we won't do a Live Update for this change; instead, we do a full Docker build (see notes on `sync`, above, for what changes trigger a Live Update vs. a full build + deploy).

### [`restart_container()`](api.html#api.restart_container)

This step is optional. If you have a `restart_container` step, it must come at the very end of your list of Live Update steps. When this step is present, it tells Tilt to restart the container after all the files have been sync'd, runs have been executed, etc. In practice, this means that the container re-executes its `ENTRYPOINT` within the changed filesystem.

If your container executes a binary and your Live Update changes that binary, you probably want to restart the container to re-execute it. If, however, you're running a Flask or Node app that responds to filesystem changes without requiring a restart, you can probably leave this step out.
