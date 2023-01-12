---
title: Smart Rebuilds with Live Update
subtitle: Tilt Tutorial
layout: docs
sidebar: gettingstarted
---
Tilt's deep understanding of your resources means the right things get rebuilt at the right times.

Even with Docker layer caching, rebuilding a container image can be slow.
For unoptimized Kubernetes-based development, every code change requires:
 1. Rebuilding the container image (`docker build ...`)
 2. Pushing the built image to a registry (`docker push ...`)
 3. Updating the tag in YAML and applying the the Deployment to the cluster (`kubectl apply -f ...`)
 4. Waiting for the roll out of new Pods using the updated image (open Reddit, 😴, etc.)

Live Update solves these challenges by performing an **in-place update of the containers in your cluster**.

It works with frameworks that natively support hot reload (e.g. Webpack), as well as compiled languages.

Time to try it out:
 1. Open `api/app.py` in your favorite editor
 2. Find the commented out line `# 'other': ['accessory']`
 3. Uncomment it (remove the leading `#`)
 4. Save the file
 5. Watch magic happen for the `api` resource in the Tilt UI
 6. Open the Tilt Avatars web app ([http://localhost:5735/]())
 7. Dress the character with some stylish glasses (this is important!!! 😎) 

![Tilt Live Updating a container after a code change](/assets/docimg/tutorial/tilt-code-change-live-update.gif)

To understand what happened, let's take a look at the `docker_build` configuration for the `tilt-avatar-api` image:
```python
docker_build(
    'tilt-avatar-api',
    context='.',
    dockerfile='./deploy/api.dockerfile',
    only=['./api/'],
    live_update=[
        sync('./api/', '/app/api/'),
        run(
            'pip install -r /app/requirements.txt',
            trigger=['./api/requirements.txt']
        )
    ]
)
```

It looks a lot like the `tilt-avatar-web` image configuration we saw in the last section.

What's not omitted this time is the `live_update` argument value, which defines a series of steps to run (in-order) to Live Update a container.

## `sync()` Steps
We have a single sync step defined:
```python
sync('./api/', '/app/api/')
```
The first argument (`./api/`) is the path, relative to the `Tiltfile`, on our machine that we want Tilt to watch for changes to (recursively).
The destination path (`/app/api/`) is the absolute path _inside the container_ where we want the files copied to.

> 💁‍♀️ Files you sync to the container _must_ match paths that Tilt is already watching for the image configuration

In practice, that results in what we saw in the "api" logs in Tilt:
```log
Will copy 1 file(s) to container: 4a9aac5527
- '/Users/quixote/dev/tilt-avatars/api/app.py' --> '/app/api/app.py'
  → Container 4a9aac5527 updated!
```

Since Flask (Python web framework) provides a dev server with hot module support, copying the file is all that was needed!
Live Update also supports situations where the framework does not support reloading code at runtime by restarting your process with an updated version of the code in the container, which saves the overhead of image build and deployment.
For details, refer to the full [Live Update Reference][guide-live-update-restart].

## `run()` Steps
When modifying non-code files, it's sometimes necessary to run additional command(s) to process them.

For example, our project has a run step to install new or updated Python dependencies using pip (Python package manager):
```python
run(
    'pip install -r /app/requirements.txt',
    trigger=['./api/requirements.txt']
)
```

The first argument is a command to run _inside the container_.
The `trigger` argument defines a path, relative to the `Tiltfile`, on our machine that, when changed, will result in the command being run in the container.

Now, when we change our project's dependencies in `./api/requirements.txt`, the updated version of the file will first be synced to the container.
Then, because it matches the run step's `trigger` condition, the command will be run in the container to install new/updated dependencies.

Go ahead and try it out by making a change to `./api/requirements.txt`.
(Hint: lines beginning with `#` will be ignored, so add a new line like `# hello from Tilt tutorial!` and save the file.)
You'll see that not only is the file copied as before when we modified `./api/app.py`, but that this time, the run step executes as well:
```log
Will copy 1 file(s) to container: 4a9aac5527
- '/Users/quixote/dev/tilt-avatars/api/requirements.txt' --> '/app/api/requirements.txt'
[CMD 1/1] sh -c pip install -r /app/requirements.txt
   ...
  → Container 4a9aac5527 updated!
```

## But Wait...There's More
We think Live Update is part of what makes Tilt truly special.
Its flexibility makes it possible to use with both interpreted and compiled languages, regardless of whether the framework supports hot module reload.

This tutorial has only scratched the surface of what's possible, and we know it can be daunting, but you've got this.
Now that you're familiar with how Tilt works and have seen some `Tiltfile` snippets, you're ready to follow the [Write a Tiltfile Guide][guide-tiltfile-authoring] and start using Tilt in your _own_ project!

We're also always excited to hear about how you are using Tilt or provide a helping hand, so do [be in touch][contact] ❤️


[contact]: /contact
[guide-live-update-restart]: /live_update_reference.html#restarting-your-process
[guide-tiltfile-authoring]: /tiltfile_authoring.html
