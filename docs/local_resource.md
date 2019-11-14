---
title: Run Local and/or Occasional Workflows with Local Resource
layout: docs
---
Each entry in your Tilt sidebar is a **resource**---a unit of work managed by Tilt. (For context,
the most common type of Tilt resource is one that represents a deployed service, and is made up of
some combination of image build instructions and Kubernetes YAML.) A **local resource** works
like any other resource in your sidebar; it represents a unit of work, and executes either
automatically in response to file changes, or [manually](https://docs.tilt.dev/manual_update_control.html)
on signal from the user. For your resource `MyGreatService`, when one of its file dependencies
changes, its work is to build a Docker image and deploy some k8s yaml; for a local resource, it's
to execute an arbitrary command on your local filesystem.

You can define a local resource in your Tiltfile as follows:
```python
local_resource('yarn', cmd='yarn install', deps=['package.json'])
```

See the [`local_resource` API spec](api.html#api.local_resource) for more details.

## Specifying dependencies
The `deps` argument allows you to specify file dependencies for your local
resource---either as a string (filepath) or a list of strings (list of filepaths).

When Tilt detects a change to any of a resource's `deps`, the resource will execute
(unless the resource is in `TRIGGER_MODE_MANUAL`, in which case the resource will not
execute, but you'll see the "pending changes" indicator next to your resource in the sidebar).

Specifying `deps` is optional. By default, a local resource without `deps` runs only once:
on `tilt up` (and any time you change its definition in your `Tiltfile`). You can
always manually trigger a local resource (or any resource) with the "force update" button:

!["force update" button](assets/img/force-update-button.png)

You might use this pattern to, for instance, define a local resource that refreshes tokens/credentials
needed by your app---you want to do it once on `tilt up`, and every now and then as needed,
but not in response to any particular file changes.

As with `docker_build` and `custom_build`, you can specify files/directories to be
ignored [with the `ignore` argument](http://tilt.dev/2019/06/07/better-monorepo-container-builds-with-context-filters.html).

## auto_init

By default, a local resource will run on startup. To disable this behavior, put the
resource in `TRIGGER_MODE_MANUAL` and specify `auto_init=False`:
```python
local_resource('reset-db', cmd='reset_db.sh',
    trigger_mode=TRIGGER_MODE_MANUAL, auto_init=False
)
```

For more on trigger mode, [see the docs](https://docs.tilt.dev/manual_update_control.html).

`auto_init=False` is currently only compatible with `TRIGGER_MODE_MANUAL`. If
you'd like a local resource that runs automatically in response to file changes
but does NOT run on `tilt up`, [let us know](https://tilt.dev/contact).
