---
slug: august-tilt-commit-of-the-month
date: 2019-09-09
author: maia
layout: blog
title: "Tilt Commit of the Month: August 2019"
subtitle: "Protect Your Production Clusters"
image: featuredImage.png
image_needs_slug: true
image_type: "contain"
tags:
  - docker
  - kubernetes
  - microservices
  - tilt
  - cotm
keywords:
  - safety
  - kubecontext
  - tilt
---

It’s our third post of the Commit of the Month series---where we highlight the work we’ve been doing on Tilt lately---and we’re continuing our proud tradition of posting a couple of days late. Never fear, though: this commit was made early in August, and merged without much fanfare, but it addressed an issue that multiple users have complained about, and has saved my personal bacon multiple times already.

August’s commit of the month is: [**Disallow deploys to remote kube by default**](https://github.com/windmilleng/tilt/commit/58bad17e22b6994aed9e688972815b41c86c87b7). If you use Tilt and you have a remote Kubernetes cluster anywhere in your life, you may have seen it in action:

!["Watch out, this might be production!" warning in the WebUI](/assets/images/august-tilt-commit-of-the-month/featuredImage.png)


## What’s the point?

The point, simply, is to keep you from `tilt up`-ing your local code into your production cluster [Multiple users reported doing this accidentally](https://github.com/windmilleng/tilt/issues/1096), and borking their production cluster because of it---overwriting production secrets, serving untested code to users, etc. Whoops! So we put in some protections.

This feature uses heuristics to guess whether you’re running in a local cluster (like Minikube or Docker Desktop). Local cluster are obviously not production, so they’re always safe. If your KubeContext is _not_ pointing to something that we can identify as a local cluster, then we block your deploy and throw up this warning instead.

If you were in fact pointing at your production cluster, then yay, crisis averted! If you actually _meant_ to deploy to this cluster (say, it’s your staging cluster, or maybe you’re excited about all the benefits you get from developing against a remote k8s cluster), you can easily [allow the cluster in your Tiltfile](https://docs.tilt.dev/api.html#api.allow_k8s_contexts), and Tilt won’t bother you about it anymore. (You don’t even to have to restart Tilt, because it’s responsive to changes in your Tiltfile!)

```
allow_k8s_contexts('my-staging-cluster')
```

We love it when users tell us they like a feature, but the most direct feedback available to us is is when the Tilt team likes a feature; it’s proved pretty helpful for us so far, and we hope it’s useful for you too!

![Slack messages from the Tilt team about this feature](/assets/images/august-tilt-commit-of-the-month/slack-praise-matt.png)

![Slack messages from the Tilt team about this feature](/assets/images/august-tilt-commit-of-the-month/slack-praise-maia.png)
*Actual footage of this feature saving Team Tilt's production cluster*

Is there some way we can make Tilt safer for you? Let us know! If you have a feature request or bug report, [file an issue](https://github.com/windmilleng/tilt/issues), and maybe the fix will be the next Commit of the Month.

So, until the end of September (or, let’s be honest, the beginning of October): happy Tilting!
