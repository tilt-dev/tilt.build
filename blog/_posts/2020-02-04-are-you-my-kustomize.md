---
slug: are-you-my-kustomize
date: 2020-02-04
author: nick
layout: blog
title: "Are You My Kustomize?"
subtitle: "Commit of the Month / January 2020"
image: /assets/images/are-you-my-kustomize/nathalie-spehner-V4UbRPvyaUY-unsplash.jpg
image_caption: "Photo by <a href='https://unsplash.com/@nathalie_spehner?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText'>Nathalie SPEHNER</a> on <a href='https://unsplash.com/?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText'>Unsplash</a>"
tags:
  - tilt
  - cotm
keywords:
  - tilt
  - kustomize
  - kubectl
---

Every commit has a story behind it.

Every month, the Tilt team picks a Commit of the Month, and tells its story.

January's commit of the month is a doozy:

["tiltfile: make kustomize fallback more clear with log statement"](https://github.com/windmilleng/tilt/pull/2795/commits/8984eac240be1948b1719d1b9f90f91a9efb64ab)

To understand it, you need some background.

## What is Kustomize?

The brilliant idea behind Kubernetes is "infrastructure as data". Obligatory Kelsey Hightower tweet:

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">Declarative
configuration is about treating infrastructure as data, which is more portable
than code, and enables workflows that manipulate desired state based on policy,
while serializing the results between each step of the pipeline.</p>&mdash;
Kelsey Hightower (@kelseyhightower) <a href="https://twitter.com/kelseyhightower/status/1164194470436302848?ref_src=twsrc%5Etfw">August 21, 2019</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

When I want to adapt my Kubernetes configs for local development,
I need a way to apply small patches so that they work locally.

Kustomize and Helm are popular solutions. Both are reasonable choices.

## Where is Kustomize?

Kustomize is available as [a standalone binary](https://github.com/kubernetes-sigs/kustomize/blob/master/docs/INSTALL.md).

Kustomize is also available as [`kubectl kustomize`](https://kubectl.docs.kubernetes.io/pages/app_customization/introduction.html), as of Kubernetes v1.14. Kubectl is the all-in-one CLI for interacting with Kubernetes.
Now that config-modification is a standard part of the Kubernetes ecosystem, the Kubernetes CLI team decided it made sense to support a solution natively.

But here's the rub.

The latest version of Kustomize is v3.5.4.

The Kustomize in Kubectl is v2.0.3.

Attempts to upgrade Kustomize in Kubectl [appear to have stalled](https://github.com/kubernetes-sigs/kustomize/issues/1500). To make matters worse, 
`kubectl kustomize` [doesn't report](https://github.com/kubernetes/kubectl/issues/797)
any identifying version info about what version of Kustomize it's using. It would be so nice if it did!

## How do I Kustomize?

A Tiltfile is like a Makefile for local Kubernetes development. Tilt keeps track
of your configs. It also keeps track of where those configs come from.

Kustomize users add a line like this to their Tiltfile:

```python
k8s_yaml(kustomize('./path/to/config/dir'))
```

Tilt will re-run `kustomize` every time you edit the config dir or `kustomization.yaml`.

But which Kustomize should it use? Please tell us because we're not sure!

## Are you my Kustomize?

Currently, Tilt's strategy is to check:
- Do you have `kustomize`? If so, use that.
- Do you have `kubectl` ? If so, try `kubectl kustomize`.

Oh and by the way! `kustomize` might be v2 or v3. `kubectl kustomize` can only be v2.

Ugh, I'm making myself dizzy just writing this.

We don't have a good answer. Commit
[8984eac240be1948b1719d1b9f90f91a9efb64ab](https://github.com/windmilleng/tilt/pull/2795/commits/8984eac240be1948b1719d1b9f90f91a9efb64ab)
adds some extra logging to tell you which path Tilt is taking.

### Further Reading:

- [Kustomize.io](https://kustomize.io/)
- [The Kubernetes Kustomize KEP Kerfuffle](https://gravitational.com/blog/kubernetes-kustomize-kep-kerfuffle/)
- [kustomize() in the Tilt API docs](https://docs.tilt.dev/api.html#api.kustomize)
