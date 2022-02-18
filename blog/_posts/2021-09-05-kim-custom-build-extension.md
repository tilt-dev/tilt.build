---
slug: "kim-extension"
date: 2021-09-05
author: milas
layout: blog
title: "Writing Yet Another Custom Image Builder"
image: "/assets/images/kim-extension/title.jpg"
image_caption: '<a href="https://www.flickr.com/photos/44124427152@N01/42670013">"construction in Dublin Docklands"</a> by Salim Virji (<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC BY-SA 2.0</a>)'
description: "Configure Tilt to build images with the experimental Kubernetes Image Manager (kim) project"
tags:
- docker
- kubernetes
---

---

## **UPDATE**: The `kim` project is not currently active

If you're using Rancher Desktop, don't fret!

We've got updated guidance available: [Switch from Docker Desktop to Rancher Desktop in 5 Minutes](/2021/09/07/rancher-desktop.html).

If you are still using `kim`, we've also got you covered: there is a [`kim` Tilt extension][tilt-ext-kim].
Please note, however, that this extension is now deprecated and is unlikely to receive further updates.

If you're interested in how Tilt extensions for non-Docker container builders work, read on!

---

At Tilt, we see a lot of different ways to build images for containers beyond `docker build`.
These alternatives are often very attractive:
 * Language-specific builders like [ko][] can leverage native tooling for lightning-fast builds
 * Cluster-integrated builders like [BuildKit CLI for kubectl][kubectl-build] can help with multi-architecture images

Not only do we want to make sure that we support using alternative image builders, we strive to make them feel just as native as using the built-in `docker_build`!

In this post, we'll look at building a wrapper for a new, experimental image builder: [`kim`][kim].

[`kim`][kim], or the **K**ubernetes **I**mage **M**anager, uses a BuildKit daemon bound to the containerd socket on a Kubernetes node.
If your eyes glazed over during that sentence: images are built directly _within_ the Kubernetes cluster using the same underlying technology (BuildKit) as Docker.
This eliminates the need for a local registry and can save time & disk space by avoiding an image push.

To use it with Tilt, we'll write a small `kim_build` function, which will use [`custom_build`][tiltfile-custom-build] under the hood (instead of [`docker_build`][tiltfile-docker-build]).

Without further ado, let's write our `kim_build` function:
```python
def kim_build(ref, context, deps=None, **kwargs):
    custom_build(
        ref,
        command='kim build -t $EXPECTED_REF ' + shlex.quote(context),
        command_bat='kim build -t %%EXPECTED_REF%% ' + shlex.quote(context),
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
3. Deployment was applied to our cluster!

You might have noticed that we also passed Live Update steps, yet didn't add any custom logic within `kim_build` to handle it.
Because [`custom_build`][tiltfile-custom-build] supports Live Update regardless of _how_ you build your images, we passed through the `live_update` and any other non-`kim` specific arguments via `**kwargs`.

And of course, you still get all the other Tilt goodies like triggering rebuild on changes and [immutable tags][immutable-tags].

A full `kim_build` implementation might take more arguments, e.g. custom path to `Dockerfile`, build args, and more.
(There is a [`kim_build` extension][tilt-ext-kim] available.)

We're always excited to see new tools in the local Kubernetes and image-building spaces, and it's important that Tilt can work with them out-of-the-box.
So go ahead, try out a crazy new image builder today - Tilt can handle it! 💪

[immutable-tags]: https://docs.tilt.dev/custom_build.html#why-tilt-uses-immutable-tags
[kim]: https://github.com/rancher/kim
[ko]: https://github.com/google/ko
[kubectl-build]: https://github.com/vmware-tanzu/buildkit-cli-for-kubectl
[rancher-desktop]: https://rancherdesktop.io/
[tilt-contact]: https://tilt.dev/contact
[tilt-ext-kim]: https://github.com/tilt-dev/tilt-extensions/tree/master/kim
[tilt-extensions]: https://docs.tilt.dev/contribute_extension.html
[tiltfile-custom-build]: https://docs.tilt.dev/api.html#api.custom_build
[tiltfile-docker-build]: https://docs.tilt.dev/api.html#api.docker_build
