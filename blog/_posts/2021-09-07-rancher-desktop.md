---
slug: "rancher-desktop"
date: 2021-09-07
author: milas
layout: blog
title: "Switch from Docker Desktop to Rancher Desktop in 5 Minutes"
image: "/assets/images/rancher-desktop/title.jpg"
image_caption: 'Photo by <a rel="noopener noreferrer" target="_blank" href="https://unsplash.com/@timwilson7">Tim Wilson</a>'
description: "Configure Tilt to build images with kim for use with Rancher Desktop"
tags:
- docker
- rancher
- kubernetes
---

---

## **UPDATE**: There is a [`kim` Tilt extension][tilt-ext-kim] available!

If you want to get building using `kim` as fast as possible, check out the [usage instructions][tilt-ext-kim] for how to add it to your `Tiltfile`.

If you're interested in how Tilt extensions for non-Docker container builders work, read on!

---

[Rancher Desktop][rancher-desktop] is a new way to run Kubernetes on macOS and Windows.

![Rancher Desktop interface on macOS](/assets/images/rancher-desktop/rancher-desktop.png)

While there are some similarities with Docker Desktop due to using a transparent VM, Rancher Desktop does not include the Docker Engine.

Instead, images are built with [`kim`][kim] (**K**ubernetes **I**mage **M**anager), which uses a BuildKit daemon bound to the containerd socket on a Kubernetes node.
If your eyes glazed over during the second half of that sentence: images are built directly _within_ the Kubernetes cluster using the same underlying technology (BuildKit) as Docker.

You'll need to activate the [`kim`][kim] symlink from the Rancher Desktop settings for Tilt to be able to use it:
![Rancher Desktop open to the "Kubernetes Settings" section highlighting the checkbox for /usr/local/bin/kim](/assets/images/rancher-desktop/rancher-desktop-kim.png)

**⚠️ [kim][] is still considered experimental!**

Since Tilt's built-in [`docker_build`][tiltfile-docker-build] function does not natively support kim, we can use [`custom_build`][tiltfile-custom-build] instead.

To start, if you're using Tilt < v0.22.7, you'll need to approve the Rancher Desktop Kubernetes context:
```python
allow_k8s_contexts('rancher-desktop')
```
Place this as early as possible in your `Tiltfile`.
(By default, Tilt will only run against a built-in set of known context names corresponding to local K8s cluster tools such as minikube or KIND to prevent an accidental deploy to prod! 😰)

Let's create a `kim_build` function that uses [`custom_build`][tiltfile-custom-build]:
```python
def kim_build(ref, context, deps=None, **kwargs):
    custom_build(
        ref,
        command='kim build -t $EXPECTED_REF ' + shlex.quote(context),
        command_bat='kim build -t %EXPECTED_REF% ' + shlex.quote(context),
        deps=deps or [context],
        disable_push=True,
        skips_local_docker=True,
        **kwargs
    )
```

Now, we can replace our [`docker_build`][tiltfile-docker-build] calls with `kim_build` calls:
```python
# docker_build(
#     'my-static-site',
#     '.',
#     only=['web/'],
#     live_update=[
#         sync('web/', '/usr/share/nginx/html/')
#     ])
# ⬇️ ⬇️ ⬇️ ⬇️ ⬇️ ⬇️ ⬇️

kim_build(
    'my-static-site',
    '.',
    deps=['web/', 'Dockerfile'],
    live_update=[
        sync('web/', '/usr/share/nginx/html/')
    ])
```

And that's it!

When we `tilt up`, we'll see:
```
STEP 1/3 — Building Custom Build: [my-static-site]
    Custom Build: Injecting Environment Variables
        EXPECTED_REF=my-static-site:tilt-build-1630528500
    Running custom build cmd "kim build -t $EXPECTED_REF ."

    ...

STEP 2/3 — Pushing my-static-site:tilt-build-1630528500
     Skipping push: custom_build() configured to handle push itself

STEP 3/3 — Deploying
     Injecting images into Kubernetes YAML
     Applying via kubectl:
     → my-static-site:deployment

    ...
```

What just happened?
1. Tilt invoked our [`custom_build`][tiltfile-custom-build] command to run [`kim`][kim]
2. No registry push was performed because [`kim`][kim] builds directly on the cluster node and we passed `disable_push=True` and `skips_local_docker=True`
3. Deployment was applied to our Rancher Desktop cluster!

You might have noticed that we also passed Live Update steps, yet didn't add any custom logic within `kim_build` to handle it.
Because [`custom_build`][tiltfile-custom-build] supports Live Update regardless of _how_ you build your images, we passed through the `live_update` and any other non-`kim` specific arguments via `**kwargs`.

And of course, you still get all the other Tilt goodies like triggering rebuild on changes and [immutable tags][immutable-tags].

A full `kim_build` implementation might take more arguments, e.g. custom path to `Dockerfile`, build args, and more.
There is a [`kim_build` extension][tilt-ext-kim] available and we're always open to PRs to improve it!

Both [Rancher Desktop][rancher-desktop] and [`kim`][kim] are new and evolving fast!
We're always excited to see new tools in the local Kubernetes space - if you're using Rancher Desktop with Tilt, [let us know][tilt-contact] ❤️

[immutable-tags]: https://docs.tilt.dev/custom_build.html#why-tilt-uses-immutable-tags
[kim]: https://github.com/rancher/kim
[rancher-desktop]: https://rancherdesktop.io/
[tilt-contact]: https://tilt.dev/contact
[tilt-ext-kim]: https://github.com/tilt-dev/tilt-extensions/tree/master/kim
[tilt-extensions]: https://docs.tilt.dev/contribute_extension.html
[tiltfile-custom-build]: https://docs.tilt.dev/api.html#api.custom_build
[tiltfile-docker-build]: https://docs.tilt.dev/api.html#api.docker_build
