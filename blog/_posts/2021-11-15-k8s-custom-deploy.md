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

If you've used Tilt, chances are you are well acquainted with the [`k8s_yaml`][api-k8s_yaml] and [`k8s_resource`][api-k8s_resource] Tiltfile functions.
The [`k8s_yaml`][api-k8s_yaml] function deploys entities to Kubernetes from either a file or string.
The [`k8s_resource`][api-k8s_resource] function configures port forwards and other behaviors for the deployed entities.

In the Kubernetes landscape, [Helm][helm] is very popular, especially for packaging and distributing external dependencies such as nginx or Kafka.
Tilt has a built-in [`helm`][api-helm] function for working with local charts and a [`helm_remote`][ext-helm_remote] extension for external charts stored in a Helm repo.

Behind the scenes, both of these invoke `helm template` via CLI to get a locally-rendered version of the chart YAML to pass to the [`k8s_yaml`][api-k8s_yaml] built-in Tilt function.
That is, the actual deployment to Kubernetes is done via Tilt using the Kubernetes API rather than Helm itself.

More generally, this is the pattern we recommend for integrating custom Kubernetes deploy tools with Tilt, and for a lot of local development use cases, this works great!
Tilt can take "shortcuts" to ensure a frictionless and snappy experience because, as a dev tool, its concerns are very different than those of a production deployment tool.

However, there are cases where it's critical to let another tool handle deployment to Kubernetes.
With Helm, for example, charts can query the Kubernetes cluster's capabilities at deployment time and use it to alter their behavior, which isn't possible with `helm template`, as it runs entirely offline.
Additionally, Helm charts can include "hooks" to run at a specific part of the deployment lifecycle.

With Tilt [v0.23.0][tilt-releases], we've introduced a new [`k8s_custom_deploy`][api-k8s_custom_deploy] built-in function to enable the use of an external Kubernetes deployment tool.
When using [`k8s_custom_deploy`][api-k8s_custom_deploy], Tilt features like status reporting and log streaming work automatically.
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

Here's what it looks like when we run `tilt up`:
![Tilt web UI after running "tilt up" against the sample Tiltfile included in this blog post](/assets/images/k8s-custom-deploy/demo.gif)

Tilt runs the `apply_cmd` passed to [`k8s_custom_deploy`][api-k8s_custom_deploy] on `tilt up` and whenever any path from the `deps` argument changes.
The `apply_cmd` deploys to Kubernetes (`helm upgrade --install ...`) and writes the _result_ of the deploy as YAML to stdout (`helm get manifest...`).
(This is what allows Tilt to know what was deployed so that it can monitor status, tail logs, set up port forwards, and perform Live Updates.
As a result, all logs for the deploy are redirected to stderr with `1>&2` so that _only_ the YAML is written to stdout.
For more details, see the [Tiltfile API reference][api-k8s_custom_deploy].)

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
This allows tools like Helm to not only delete any entities from Kubernetes that they created but also clean up any extra state (e.g. Helm release metadata).

## What's The Catch?
We are still exploring the best semantics for passing Tilt-built image references to external tools, so they can interoperate with `docker_build`.
In its initial state, [`k8s_custom_deploy`][api-k8s_custom_deploy] is best suited for use with pre-built images or tools that handle both image build + deploy.

Additionally, if your tool is capable of templating YAML, and you don't need other functionality provided by it while developing, [`k8s_yaml`][api-k8s_yaml] is often simpler and faster.


[api-helm]: https://docs.tilt.dev/api.html#api.helm
[api-k8s_custom_deploy]: https://docs.tilt.dev/api.html#api.k8s_custom_depliy
[api-k8s_yaml]: https://docs.tilt.dev/api.html#api.k8s_yaml
[api-k8s_resource]: https://docs.tilt.dev/api.html#api.k8s_resource
[docs-helm-reimplement]: https://docs.tilt.dev/helm.html#re-implementing-the-helm-built-in
[ext-helm_remote]: https://github.com/tilt-dev/tilt-extensions/tree/master/helm_remote
[helm]: https://helm.sh/
[tilt-releases]: https://github.com/tilt-dev/tilt/releases
