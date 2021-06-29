---
slug: "namespace-flag"
date: 2021-06-30
author: lucie
layout: blog
title: "Namespace Flag"
image: ""
image_caption: 'namespace and flag'
tags:
  - kubernetes
  - kubectl
  - namespaces
keywords:
  - terminal
  - flag
  - namespace
  - kubecontext
  - development
---

As of Tilt [v0.20.9](https://github.com/tilt-dev/tilt/releases/tag/v0.20.9), you can now set a default namespace on `tilt up`. 
Instead of using the default namespace set in your local kubernetes config, Tilt can now use a command line-specified namespace to start resources.

This is the first step in an effort to give Tilt users greater control over the namespaces their resources use when they run `tilt up`.

It’s common to omit the namespace field in YAML configuration files, which lets resources get created wherever the default namespace happens to be set.
While this is useful in reducing repetition, it can also create conflicts with resources created outside of Tilt that also exist in the default namespace.

Working around this was doable but not exactly the easiest experience.
Maybe you used the [namespace extension](https://github.com/tilt-dev/tilt-extensions/tree/master/namespace) to manually set the namespace for each of your resources:
```
load('ext://namespace', 'namespace_create', 'namespace_inject')
namespace_create('test-default')
k8s_yaml(namespace_inject(read_file('service1.yaml'), 'test-default'))
k8s_yaml(namespace_inject(read_file('service2.yaml'), 'test-default'))
k8s_yaml(namespace_inject(read_file('service3.yaml'), 'test-default'))
```

Maybe you resigned yourself to shutting down other running resources and then [waiting](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#wait)
for them to be truly gone to prevent namespace conflicts.
```
$ kubectl get deployments
default 	my-deployment
$ kubectl delete deployment my-deployment 
delete deployment my-deployment
$ kubectl wait deployment/my-deployment --for=delete
$ tilt up
....
```

This can now be avoided altogether by adding an extra flag to your tilt up command, like so:
```
$ tilt up --namespace=testing
```
When a namespace is specified, Tilt sets its internal Kubernetes context to include the custom default namespace.

Note that the flag only affects resources whose namespaces are left unspecified. Resources that explicitly specify a namespace will not be affected. 


