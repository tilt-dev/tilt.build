---
title: Code. Update. Repeat.
subtitle: Tilt Tutorial
layout: docs
---

We mentioned that Tilt embraces the concept of a [control loop][tutorial-control-loop], so once you've run `tilt up`, it's a "hands free" development experience.

As you edit your code, Tilt will automatically run update steps such as building an updated container image and deploying it.

> 📓 Navigate to the "web" resource in the Tilt UI and "Clear Logs" before continuing

Let's test it out:
 1. Open `web/vite.config.js` in your favorite editor
 2. Find the `logLevel` line and change it from `'error'` to `'info'`
 3. Save the file
 4. Watch magic happen for the `web` resource in the Tilt UI 

![Tilt updating a resource after a code change](/assets/docimg/tutorial/tilt-code-change-full-rebuild.gif)

Whoa, a lot just happened - time to break it down!

## 1. File Changed
First, Tilt saw a file change:
```log
1 File Changed: [web/vite.config.js] • web
```

The [Tilt Avatars][repo-tilt-avatars] file hierarchy looks like this:
```log
tilt-avatars/
├── api/
│   └── ...
├── deploy/
│   ├── web.dockerfile
│   └── ...
├── web/
│   ├── vite.config.js
│   └── ...
└── Tiltfile
```

In the `Tiltfile`, the container image build for the "web" resource looks like this:
```python
docker_build(
    'tilt-avatar-web',
    context='.',
    dockerfile='./deploy/web.dockerfile',
    only=['./web/'],
    ignore=['./web/dist/'],
    live_update=[...]  # omitted for brevity
)
```

Several of these arguments include paths.
Paths arguments for functions in the `Tiltfile` are relative to the `Tiltfile` (refer back to the file hierarchy above if you get confused).

The `context` argument specifies the build context for Docker as the current directory, which is the repo root (`tilt-avatars/`).
As a result, Tilt watches for changes to any modified files in this directory or any subdirectory, recursively.

However, we also specified `only`, which is an optional argument that does two things:
 * Filter files included in the build context
 * Restrict file watching to the subset of paths

Lastly, we've also provided a value for `ignore`, which as an optional argument to exclude certain paths from the build context and not watch for file changes to them. 

If we put all this together, Tilt is watching for any file changes in the `web/` directory or any of its subdirectories, recursively, EXCEPT for those in `web/dist` (or any of its subdirectories, recursively).
Phew!

When a matching file changes, such as `web/vite.config.js`, because it's watched by the `tilt-avatar-web` container image build configuration, Tilt initiates an update for the "web" resource.

> **How does Tilt know the `tilt-avatar-web` image belongs to the "web" resource?**
>
> You might remember that a resource can be composed of multiple bits of work.
> In the case of the "web" resource, it has a container image build and a Kubernetes Deployment.
>
> Tilt associated the `tilt-avatar-web` container image with the "web" resource because the container image name is referenced in Kubernetes YAML loaded in the `Tiltfile` with `k8s_yaml`.
> (This is not the only way that container images can be assembled into a resource, and it's possible to manually configure where auto-assembly is insufficient.)


## 2. Resource Update
Now, the update process starts:
```log
STEP 1/3 — Building Dockerfile: [tilt-avatar-web]
  ...

STEP 2/3 — Pushing localhost:44099/tilt-avatar-web:tilt-0b9fcdf9cfea47ba
  ...

STEP 3/3 — Deploying
     Injecting images into Kubernetes YAML
     Applying via kubectl:
     → web:deployment
```
First, Tilt built an updated version of the container image.
Then, it pushed it to our local registry so that it can be used by Kubernetes.
(This step could look different for you!
Tilt adapts its workflow based on your local cluster setup, which might not require image pushes.)
Finally, it deployed the updated image.

> 🏷 **Immutable Image Tags**
>
> Tilt tags every image it builds with a unique `:tilt-<hash>` tag.
> It then rewrites the Kubernetes YAML (or Helm chart) on the fly during deployment to use this tag.
>
> Why?
> Using a "rolling" tag (such as `:latest`) can result in hard-to-debug issues depending on factors like image pull policy configuration.
> With an immutable tag, you're guaranteed _exactly_ what got built is what will run.
>
> It's just one more thing Tilt takes care of without any extra configuration to save you a headache later!

## 3. Resource Runtime Monitoring
Once deployed, Tilt starts tracking the updated version of the resource:
```log
Tracking new pod rollout (web-7f9b8b65f4-wt97k):
     ┊ Scheduled       - <1s
     ┊ Initialized     - <1s
     ┊ Ready           - 1s
```
As Tilt waits for the resource to become ready, it'll pass along relevant events, such as image pull status or container crashes, so you don't need to resort to manually investigating a failed deploy with `kubectl`.

Once the container has started, Tilt will stream the logs.
In our case, since we enabled more verbose logging for Vite (the dev server that hosts the frontend), we should see some messages as it starts up:
```log
yarn run v1.22.5
$ vite
Pre-bundling dependencies:
  react
  react-dom
(this will be run only when your dependencies or config have changed)

    ...

  ready in 946ms.
```

If you're a bit underwhelmed by changing a log level - you caught us!
The [Tilt Avatars][repo-tilt-avatars] project is configured to use Live Update for regular development, so we purposefully made a change in a config file that meant the full container would be rebuilt.

Let's move on to the next section where we'll make more interesting code changes with Live Update.

[repo-tilt-avatars]: https://github.com/tilt-dev/tilt-avatars
[tutorial-control-loop]: ./2-tilt-up.html#the-control-loop
