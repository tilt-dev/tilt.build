---
slug: kubecon-faq
date: 2019-12-20
author: maia
layout: blog
title: "KubeCon NA 2019 FAQ"
image: "/assets/images/kubecon-faq/booth-photo.jpg"
image_caption: "Team Tilt at our booth at KubeCon NA 2019"
tags:
  - docker
  - kubernetes
  - tilt
  - dev tools
  - faq
  - kubecon
keywords:
  - bash
  - local
  - kubernetes
  - docker
  - tilt
  - faq
  - kubecon
  - kubecon NA
---
We had a blast at KubeCon NA 2019---a big shout-out to everyone who stopped by our booth to say
hi, watch a demo, or play with Duplos for a bit. We were blown away by the excitement about
Tilt, and you all asked some great questions, so before Team Tilt goes into hibernation for
the rest of December, we wanted to answer the most frequent questions we got at KubeCon.

### Q: How much does Tilt cost?
Tilt is free and open-source, and it’s going to stay that way. We’re currently funded by some
rad VCs, and in a forthcoming post, we’ll talk about our thoughts on how to build a sustainable
and profitable business where the core product is open-source; stay tuned!

### Q: Does Tilt replace CI?
Tilt does _not_ replace CI; it is a _pre-commit_ tool, and it comes earlier in the workflow.

Generally, the lifecycle of a code change looks something like this:

![Lifecycle of a code change: dev's laptop -> PR -> tests in CI -> merge to master -> deploy to
 production](/assets/images/kubecon-faq/code-change.png)
 *Lifecycle of a code change*

Tilt sits right at the first step.

We're there to help when you're writing a feature or fixing a bug. When you write a line of code and
look at your app to check that it’s doing what it’s supposed to do... that’s what Tilt makes easy.

### Q: Can I deploy to production with Tilt?
As discussed above, Tilt is a _pre-commit_ tool designed to help developers write and verify
features before pushing them up for review. Use Tilt to iterate on your Dockerfiles and Kubernetes
YAML, then use your favorite deploy tool to push to production!

### Q: Oh, so you’re like [Telepresence](https://www.telepresence.io/)?
Yeah, we are! Tilt and Telepresence both have a similar focus (improving Kubernetes
microservice development), but go about it in different ways.

Telepresence's solution is to zoom you in on one service; you can develop and run that service
locally, and Telepresence hooks it into the rest of the services in your staging cluster. You
get to keep your local dev workflow more or less intact, and focus on the one microservice
that you're developing, assuming that all of the other microservices in your staging cluster
keep working as expected.

Tilt gives you a bird's eye view of everything that's going on across all your microservices,
even as you iterate on one or two of them---because often when you're debugging a problem with
one service, the actual problem was an error in another service. So Tilt deploys all of your
services, watches your file-system, and syncs your local changes to the cluster; then gives
you visibility into logs, errors, and crashes across the whole application.

### Q: Oh, so you’re like [Skaffold](https://skaffold.dev/)?
Yeah, we are! Tilt and Skaffold both make Kubernetes development easier. The main differences
 between them are:
- Where Skaffold provides a simple CLI, Tilt has a full-fledged UI that tells you at a glance what’s
happening with your app and surfaces you the information you need.
- At Tilt, we care a lot about extensibility. We built our app on primitives that you can mix and
match to integrate Tilt easily into your existing workflow. (Use a custom script to generate
your YAML? No problem! Need to seed a database before any other services come up? We can
handle that!) Skaffold, on the other hand, supports a narrower range of use cases.

### Q: Oh, so you’re like [Garden](https://garden.io/)?
Yeah, we are! Garden is another tool in the make-Kubernetes-development-not-suck space, along
with Tilt, Skaffold, and Telepresence. The main differences we see between Tilt and Garden are:
- Tilt’s extensibility is a big point in its favor; Tilt’s primitives and composability mean it
supports a huge diversity of workflows.
- Garden has some features Tilt does _not_---primarily stuff outside the developer inner loop, like
CI capabilities and server provisioning logic.
- Less a matter of features and more of user experience: at Tilt, we’ve put a lot of effort into
our UI and UX, and we think it shows. If you’ve used both Tilt and Garden, we’d love to hear your reaction!

### Q: Does Tilt work with remote clusters, or only locally?

Tilt works with whatever cluster you like! Just point your `kubeconfig` to your preferred cluster
and run `tilt up`. Local, remote, it doesn’t matter---Tilt is cluster-agnostic. (Don’t know which
cluster to choose?
[We have some recommendations](https://docs.tilt.dev/choosing_clusters.html).)

This also means you can run the same Tiltfile against multiple different clusters, depending on
what you're trying to do.

### Q: Is Tilt an alternative to [minikube](https://minikube.sigs.k8s.io/) or [microk8s](https://microk8s.io/)?
Nope, Tilt isn’t a Kubernetes cluster; it’s an application to run your microservices in the
Kubernetes cluster of your choosing, with great visibility and fast updates.

### Q: Does Tilt run in my cluster as a sidecar, or...?
Tilt doesn’t run _in_ your cluster (i.e. it’s not a sidecar); Tilt is a binary that runs on your
local machine. Yes, Tilt pushes up your app(s) to Kubernetes, but Tilt itself is a binary that
runs locally.

### Q: If I’m developing in Kubernetes, how do I use my debugger?
Tilt lets you easily [port forward](https://docs.tilt.dev/tiltfile_authoring.html#step-3-watch-optional) from
your container to localhost, so for most debuggers it’s a matter of 1. making sure your app is
exposing a debugging port, and then 2. using Tilt to forward that port to localhost so you can
connect with your IDE. For more complex cases, we recommend looking into
[Squash](https://github.com/solo-io/squash).


### Q: Wow, Tilt updated that service so fast, how’d it do that!?
Tilt updates are so fast because instead of doing a whole `docker build && docker push && kubectl
apply`, it can sync your changed code directly to a running container. We call this
feature Live Update. Here’s how it works:
1. Change a line of code.
2. Tilt detects the change and copies the changed file to your running container.
3. Optionally, Tilt can run commands in the container e.g. `go install`, or if `requirements.txt`
changed, maybe `pip install`.
4. Optionally, Tilt restarts your app (e.g. if you built a new Go binary, you need to rerun it).
For more details, or to play around with an example project, check out
[the Live Update blog post](https://blog.tilt.dev/2019/04/02/fast-kubernetes-development-with-live-update.html).

## Any further questions, Your Honor?
Thanks again for stopping by our booth and/or this post. Still have questions about Tilt? [We’d
 love to hear them](https://tilt.dev/contact)!
