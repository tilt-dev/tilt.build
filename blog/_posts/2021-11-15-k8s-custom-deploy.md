---
slug: "k8s-custom-deploy"
date: 2021-11-18
author: milas
layout: blog
title: "Deploy All The Things Even If They Aren't YAML"
image: "/assets/images/k8s-custom-deploy/title.jpg"
description: "Integrate Tilt with custom Kubernetes deployment scripts & tools"
tags:
  - kubernetes
  - tilt
  - helm
---

If you've used Tilt, chances are you are well acquainted with the [`k8s_yaml`][api-k8s_yaml] Tiltfile function, which deploys objects to Kubernetes from either a file or string.
(Think `kubectl apply -f ...`)

Most of the time, this is all you need - after all, YAML is the go-to choice for Kubernetes tooling.
Many tools, such as [`kustomize`][kustomize], always output YAML, while others, like [Helm][helm] (which manages the entire deployment lifecycle), offer a template subcommand.

In some instances, however, pre-templated YAML alone is not sufficient or might not even exist!
For example, Helm charts can include "hooks" to run at a specific part of the deployment lifecycle but aren't part of the templated YAML.
Other tools, such as [OpenFaaS][openfaas], provide a streamlined build & deploy experience managed entirely by their CLI, so there's no YAML at all.
It's also common for teams to have their own custom deployment shell scripts (e.g. for use with CI/CD).

While it's possible to use Tilt's [`local_resource`][api-local_resource] function as a workaround in these instances, that means giving up much of Tilt's deep Kubernetes integration for the resource as a result.

In Tilt [v0.23.0][tilt-releases], we've introduced a built-in function to enable the use of an external Kubernetes deployment tool or script.
With the new [`k8s_custom_deploy`][api-k8s_custom_deploy] function, Tilt will delegate to a command or shell script to perform the deployment instead of directly calling the Kubernetes API with YAML.
Tilt features like status reporting and log streaming work automatically.
Even the more advanced customizations provided by [`k8s_resource`][api-k8s_resource] such as port forwards are supported!

## Example
Let's use [`k8s_custom_deploy`][api-k8s_custom_deploy] to deploy Kafka using a public Helm chart into our cluster:
```python
# configure the remote Helm repo
local('helm repo add bitnami https://charts.bitnami.com/bitnami',
      quiet=True,
      echo_off=True)

# on deploy -> run the Helm install and then query for what it deployed
apply_cmd = """
helm upgrade --install -f values.yaml local-kafka bitnami/kafka 1>&2
helm get manifest local-kafka | kubectl get -oyaml -f -
"""

# on `tilt down` -> uninstall the release with Helm
delete_cmd = 'helm uninstall local-kafka'

k8s_custom_deploy(
    'kafka',
    apply_cmd=apply_cmd,
    delete_cmd=delete_cmd,
    # apply_cmd will be re-executed whenever these files change
    deps=['values.yaml'],
)

# add a port forward so it's possible to access/debug the cluster from
# our host machine
k8s_resource('kafka', port_forwards=['9092:9092'])
```

When we run `tilt up`, Tilt will execute the `apply_cmd`, which performs the deployment using Helm and then returns the _result_ as YAML so Tilt can track the new or updated Kubernetes objects.
If `values.yaml` changes, the `apply_cmd` will be automatically re-run.

If we query Helm, we'll see that it knows about this release:
```bash
$ helm ls
NAME       	NAMESPACE	REVISION	UPDATED                             	STATUS  	CHART       	APP VERSION
local-kafka	default  	3       	2021-11-16 09:24:48.386254 -0500 EST	deployed	kafka-14.4.1	2.8.1
```

Now, if we run `tilt down`, we'll see that our `delete_cmd` is invoked:
```bash
$ tilt down
Loading Tiltfile at: ./Tiltfile
Successfully loaded Tiltfile (177.134ms)
Running cmd: helm uninstall local-kafka
release "local-kafka" uninstalled
```
This allows tools like Helm to not only delete any objects from Kubernetes that they created but also clean up any extra state (e.g. Helm release metadata).

## What's The Catch?
We are still exploring the best semantics for passing Tilt-built image references to external tools, so they can interoperate with `docker_build`.
In its initial state, [`k8s_custom_deploy`][api-k8s_custom_deploy] is best suited for use with pre-built images or tools that handle both image build + deploy.

Additionally, if your tool is capable of templating YAML, and you don't need other functionality provided by it while developing, [`k8s_yaml`][api-k8s_yaml] is often simpler and faster.


[api-helm]: https://docs.tilt.dev/api.html#api.helm
[api-k8s_custom_deploy]: https://docs.tilt.dev/api.html#api.k8s_custom_depliy
[api-k8s_yaml]: https://docs.tilt.dev/api.html#api.k8s_yaml
[api-k8s_resource]: https://docs.tilt.dev/api.html#api.k8s_resource
[api-local_resource]: https://docs.tilt.dev/api.html#api.local_resource
[docs-helm-reimplement]: https://docs.tilt.dev/helm.html#re-implementing-the-helm-built-in
[ext-helm_remote]: https://github.com/tilt-dev/tilt-extensions/tree/master/helm_remote
[helm]: https://helm.sh/
[kustomize]: https://kustomize.io/
[openfaas]: https://www.openfaas.com/
[tilt-releases]: https://github.com/tilt-dev/tilt/releases
