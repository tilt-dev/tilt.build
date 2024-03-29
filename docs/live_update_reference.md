---
title: Live Update Reference
description: "A technical specification of Tilt's live_update functionality"
layout: docs
sidebar: guides
---

Live Update optimizes your setup to get updates down from minutes to **seconds**.

This document is a technical specification of `live_update`. If you're looking
for sample projects and examples for your project, see:

* [Go](/example_go.html)
* [NodeJS](/example_nodejs.html)
* [Python](/example_python.html)
* [Java](/example_java.html)
* [Static HTML](/example_static_html.html)
* [C# + ASP.NET Core](/example_csharp.html)
* [Bazel](/example_bazel.html)

## Tiltfile API

When specifying how to build an image (via `docker_build()` or `custom_build()`), you may optionally pass the `live_update` argument.

`live_update` takes a list of `LiveUpdateSteps` that tell Tilt how to update a running container in place (instead of paying the cost of building a new image and redeploying).

The list of `LiveUpdateSteps` must be, in order:
- 0 or more [`fall_back_on`](api.html#api.fall_back_on) steps
- 0 or more [`sync`](api.html#api.sync) steps
- 0 or more [`run`](api.html#api.run) steps

When you `tilt up`, your initial build will be a full build---i.e., the specified Docker build or Custom build.[^1]

When a file changes:
   1. If it matches any of the files in a `fall_back_on` step, we will fall back to a full rebuild + deploy (i.e. the normal, non-live_update process).
   2. Otherwise, if it matches any of the local paths in `sync` steps, a live update will be executed as follows:
        1. copy any changed files according to `sync` steps
        2. for every `run` step:
            1. if the `run` specifies one or more `triggers`, execute the command iff any changed files match the given triggers
            2. otherwise, simply execute the command

## LiveUpdateSteps
Each of the functions above returns a `LiveUpdateStep` -- an object like any other, i.e. it can be assigned to a variable, etc. That means that something like this is perfectly valid syntax:
```python
sync_src = sync('./source', '/app/src')
sync_static = sync('./static', '/app/static')
docker_build('my-img', '.', live_update=[sync_src, sync_static])
```

As part of Tiltfile validation, we check that all of the `LiveUpdateSteps` you've created have been used in at least one Live Update call. If not, we throw an error.

### [sync(local_path: str, remote_path: str)](api.html#api.sync)
`sync` steps are the backbone of a Live Update. (For this reason, we'll discuss them first, even though they may be preceeded by one or more `fall_back_on` steps in a Tiltfile.) 

_Tilt will only run a Live Update if it detects a change to one or more files matching a `sync` step._

A `sync` call takes two args: the local path of a file/directory, and the remote path to which Tilt should sync that file/directory if it changes. (This includes deleting the file remotely if it is deleted locally.)

#### What files can I sync? How are builds triggered?
When you tell Tilt how to build an image, you specify some set of files to watch. In the case of a `docker_build` call, Tilt watches the directory that you pass as `context`. Your sync'd local paths must fall within that context. (If you're using `custom_build`, all of the above applies, only with `deps` in place of `context`.) Let's look at some examples:

<figure>
    <img src="/assets/img/liveupdate-sync-illegal.png" class="no-shadow" alt="An illegal 'sync'">
    <figcaption>An illegal 'sync': attempting to sync files that aren't included in the docker_build context</figcaption>
</figure>

The `sync` above is invalid, because it attempts to sync files that we're not even watching (seen here highlighted in blue). To put it another way: there's no way for those files to get into the container in the first place, because they would never be included in the Docker build.

<figure>
    <img src="/assets/img/liveupdate-sync-docker-context.png" class="no-shadow" alt="A valid use of 'sync' (all sync'd files are subsets of docker_build.context)">
    <figcaption>A valid use of 'sync' (all sync'd files are subsets of docker_build.context)</figcaption>
</figure>

Above is an example of a valid `sync`s. A change to any of the green files will kick off a Live Update, because they match a `sync` step. A change to any of the yellow files will kick off a full Docker build + deploy, because they're part of the Docker context but we don't have instructions on how to Live Update them. (Want to be more selective in which files do/don't kick off full builds? Check out [context filters for `docker_build`](https://blog.tilt.dev/2019/06/07/better-monorepo-container-builds-with-context-filters.html).)

<figure>
    <img src="/assets/img/liveupdate-sync-dep-images.png" class="no-shadow" alt="How to use 'sync' with multiple dependent docker images">
    <figcaption>An example of 'sync' used with dependent Docker images</figcaption>
</figure>


If you have multiple Docker images that depend on each other, you can sync files from anywhere within the contexts of any of the images. (In the diagram above, Tilt is building two images; the yellow image in the `server1` directory depends on--i.e. `FROM`'s--the red image in the `common` directory.)

The rule of thumb is: if Tilt is watching it, you can `sync` it. (Tilt will watch it if it's in a `docker_build.context` or `custom_build.deps`).


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

Currently, all of your `run` steps must come after all of your `sync` steps. 

If you provide multiple `run` steps, the commands will be executed in the order given. 

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

## Restarting your Process

Some apps or invocations thereof (e.g. Javascript apps run via `nodemon`, or Flask apps run in debug mode) detect and incorporate code changes without needing to restart. For other apps, though, you'll need to re-execute them for changes to take effect.

For most setups, you'll be able to use the [`restart_process` extension](https://github.com/tilt-dev/tilt-extensions/tree/master/restart_process): import the extension, replace your `docker_build` call with a `docker_build_with_restart` call, and specify the `entrypoint` parameter (i.e. the command to run on container start and _re-run_ on Live Update).

There are a few exceptions to the above; the `restart_process` extension doesn't work for:
* Docker Compose resources; you should use the [`restart_container()`](api.html#api.restart_container) Live Update step instead
* Images build via `custom_build`
* Container images without a shell (e.g. `scratch`, `distroless`)
* CRDs

If any of the exceptions above apply to you, or `restart_process` doesn't otherwise work for your use case, read on.

### Workarounds for Restarting Your Process

Tilt is flexible enough that you can employ any number of workarounds for restarting your process as part of a Live Update. The basic idea is to invoke your process such that a single command (specified as a `run` step) causes it to restart. Here are a few approaches we recommend:
* We've written a [set of wrappers for your process](https://github.com/tilt-dev/rerun-process-wrapper). Put these scripts in your container and invoke your process as:
    ```bash
/path/to/start.sh /path/to/bin
    ```
    You can then restart your process with Live Update step: `run('/path/to/restart.sh')`. (Requires that shell be available on your container.)
* [`entr`](https://github.com/eradman/entr/) is a neat utility for (re)running processes when specified files change. You can designate an arbitrary file to trigger process restart, say `/restart.txt`, and invoke your process like this:
    ```bash
echo /restart.txt | entr -rz /path/to/bin
    ```
    You can then your process with Live Update step: `run('date > /restart.txt')`. (You'll have to ensure that `entr` is present in your Docker image, and that your arbitrary file for restarting exists.) (Requires that shell be available on your container.)

Recall that you can change the command run by your container in a few ways:
* in the Dockerfile, via `ENTRYPOINT`/`CMD`
* in your Kubernetes YAML, via `spec.containers.[the_container].command`
* in your Tiltfile, via the `docker_build.entrypoint` parameter (or analogously, `custom_build.entrypoint`)

## More Examples

If you need more specifics on how to set up Live Update with your programming
language, all our major example projects use Live Update:

<ul>
  {% for page in site.data.examples %}
    <li><a href="/{{page.href | escape}}">{{page.title | escape}}</a></li>
  {% endfor %}
</ul>

---

[^1]: The initial build is always a full build because Live Update needs a running container to modify. Thus, your base build (Docker/Custom Build) should be sufficient to create your dev image, and should not rely on any `sync`'d files or `run` commands.
