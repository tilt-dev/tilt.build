---
slug: "apis-under-control"
date: 2022-01-01
author: siegs
layout: blog
title: "APIs Under Control"
subtitle: "Why the Kubernetes APIs are so powerful"
description: "We explore what makes the Kubernetes approach to APIs so useful, and how we applied them to Tilt."
image: "/assets/images/apis-under-control/flying-jeep.jpg"
tags:
  - kubernetes
  - api
  - api-server
---
An underrated aspect of Kubernetes is how open and extensible the system is. Every facet of a Kubernetes cluster can be browsed, inspected and modified via a standard [REST API][K8SREST]. [Custom resources][CustomResources] can be defined in the API to hold data specific to each production system. [Operators][] can be added to react to changes to the system and perform new functionality that goes beyond what the Kubernetes developers originally intended.

At its core, Kubernetes is more than an API or even a container orchestration platform, it's a pattern for building distributed systems, modeled after a [feedback control system][control-system] from systems engineering. In essence:

1. Declare a desired _setpoint_ for the system, using a [uniform interface][REST] (resources in the Kubernetes API).
2. Operate a _[control loop][control-loop]_ to monitor all inputs to the system and converge the system state towards the setpoint (the Kubernetes [control plane][control-plane]).
3. Allow any interested consumer to monitor inputs and make changes to the system and its setpoint ([watches][] and [operators][Operators]).

In this way, Kubernetes does for computing workloads what cruise control (speed as a setpoint) or autopilot (destination as a setpoint) do for your automobile, except in an open and extensible fashion. (This reminds me of a [vulnerability in Fiat/Chrysler/Jeep automobiles][jeep] years ago that allowed remote attackers complete control of the vehicle. [Secure your clusters][secure-clusters], everyone!)

### From prod to dev

When it comes to the software tools we use to develop our own systems, however, they are usually not so dynamic. They typically operate on some fixed configuration inputs, require us to run them manually after we make changes, and produce relatively static output. They may make assumptions about prerequisites that need to be installed. Errors can be cryptic. Some tools and frameworks have gotten a little more dynamic with auto-reloading development web servers, but that's about it. And then, gaining insight into how the tool operates or what produced the result is a difficult, frustrating task. Finally, getting different tools to work together is a constant tangle of shell scripts and baling wire.

With Tilt, we are working to change the state of development environments from the fragile, static, duct-taped approach to a dynamic open, extensible environment that responds to your changes and immediately takes action, keeping you in a state of flow.

### Dev environments as APIs

It's [no][t8] [secret][t3] [that][t4] [we're][t5] [big][t6] [fans][t7] of [Kubernetes][t1], the [control loop][nicks-kubecon], and the [API][t2]. We like it so much, we spent most of 2021 migrating and adapting Tilt to use the Kubernetes API machinery. It's not an analog, it literally uses the same building blocks as Kubernetes.

To see for yourself, start Tilt in one shell:
```
tilt up
```
In another shell, tell `kubectl` about Tilt's API server:
```
export KUBECONFIG=~/.tilt-dev/config
kubectx tilt-default
```
Now you can browse Tilt using kubectl:
```
kubectl api-resources
```
This outputs:
```
NAME                    SHORTNAMES     APIVERSION          NAMESPACED   KIND
clusters                               tilt.dev/v1alpha1   false        Cluster
cmds                                   tilt.dev/v1alpha1   false        Cmd
# ...all the resource kinds Tilt knows...
```
Now ask to see the filewatch resources:
```
kubectl get filewatches
```
This outputs:
```
NAME                 CREATED AT
configs:(Tiltfile)      2021-12-15T21:10:03Z
image:tilt-avatar-api   2021-12-15T21:10:03Z
image:tilt-avatar-web   2021-12-15T21:10:03Z
```

(For convenience, `tilt api-resources` and `tilt get` work just like `kubectl` so you don't have to mess around with `KUBECONFIG` like we did here. [Read more in the command-line docs][cli-docs].)

You can even browse Tilt data in [K9s](https://k9scli.io):

```
k9s --command filewatches
```
![K9s](/assets/images/apis-under-control/k9s-describe-filewatch.png)

The only thing Tilt's API server doesn't support as of this writing are Custom Resource Definitions (CRDs). (We'd like to support them eventually but are still gathering use cases -- if you have a use for custom resources inside of Tilt, [let's talk!]({{site.landingurl}}/contact))

### A language for dev environments

"Kubernetes for prod, Tilt for dev" says the [title bar on the Tilt homepage]({{site.landingurl}}). Indeed, if Kubernetes resources are a way to describe the setpoint of your production environment, then Tilt resources are the same for your development environment. Except that in Tilt, resources are described by the _Tiltfile_, Tilt's main configuration entrypoint. Think of the Tiltfile as a domain-specific language for describing development environments. That's right, the Tiltfile is meant to be thought of as a declarative program. When the Tiltfile executes, it doesn't run any commands, build any images or deploy any workloads to Kubernetes. Instead, it creates or modifies data in the Tilt API server. Tilt runs its own control loop in the background, looking at changes in the API server and reconciling any resources that need to be run, built, or deployed. And as you saw above, the Tiltfile is itself registered in the Tilt API as a filewatch, so Tilt instantly picks up changes to the Tiltfile and applies them to the API.

### An API for extending Tilt

We want to make it easy to extend Tilt to do useful things that we never conceived ourselves.

Since the Tiltfile is written in Starlark, a Python-like language, it's often easiest to write extensions to Tilt in Starlark, [like numerous Tilt extensions already do][tilt-extensions].


[K8SREST]: https://kubernetes.io/docs/concepts/overview/kubernetes-api/
[CustomResources]: https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/
[Operators]: https://kubernetes.io/docs/concepts/extend-kubernetes/operator/
[REST]: https://www.ics.uci.edu/~fielding/pubs/dissertation/rest_arch_style.htm#sec_5_1_5
[control-system]: https://en.wikipedia.org/wiki/Control_system
[control-loop]: https://en.wikipedia.org/wiki/Control_loop
[control-plane]: https://kubernetes.io/docs/concepts/overview/components/
[watches]: https://kubernetes.io/docs/reference/using-api/api-concepts/#efficient-detection-of-changes
[jeep]: https://www.forbes.com/sites/thomasbrewster/2015/07/21/jeep-vulnerability-fixed/
[secure-clusters]: https://kubernetes.io/docs/tasks/administer-cluster/securing-a-cluster/

[nicks-kubecon]: https://www.youtube.com/watch?v=uKF8v9X6hSE

[t9]: {{site.blogurl}}/2021/12/07/measuring-dev-env-health.html
[t8]: {{site.blogurl}}/2021/12/03/k8s-custom-deploy.html
[t7]: {{site.blogurl}}/2021/08/17/write-more-bash.html
[t6]: {{site.blogurl}}/2021/07/19/kubernetes-apply.html
[t5]: {{site.blogurl}}/2021/07/12/portforwarding-is-awesome.html
[t4]: {{site.blogurl}}/2021/07/08/uibutton-navbar.html
[t3]: {{site.blogurl}}/2021/05/07/eyes-on-the-watchers.html
[t2]: {{site.blogurl}}/2021/04/30/how-many-servers.html
[t1]: {{site.blogurl}}/2021/03/18/kubernetes-is-so-simple.html

[cli-docs]: {{site.docsurl}}/cli/tilt.html

[tilt-extensions]: {{site.docsurl}}/api.html#extensions
