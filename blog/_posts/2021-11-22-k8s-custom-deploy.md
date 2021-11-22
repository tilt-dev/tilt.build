---
slug: "k8s-custom-deploy"
date: 2021-11-22
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
Let's use [`k8s_custom_deploy`][api-k8s_custom_deploy] to deploy an [OpenFaaS][openfaas] function without writing a Dockerfile or Kubernetes YAML.

For this example, I've installed the OpenFaaS components in my cluster manually; in a real Tiltfile, you could include this as well to ensure the local environment is set up properly.
The [OpenFaaS blog][openfaas-blog-tilt] has a guide that might be useful.

I'm using a Golang handler bootstrapped by running `faas-cli new go-fn --lang go`.
This created a `go-fn.yml` file (this is an OpenFaaS config, NOT a Kubernetes manifest.)
It also made a `go-fn/` directory with "Hello world" example handler code.

```python
# on `tilt up` and file changes -> run the OpenFaaS build + deploy and then query for what it deployed
apply_cmd = """
faas-cli up -f go-fn.yml 1>&2
kubectl get -oyaml --namespace=openfaas-fn all -l "faas_function=go-fn"
"""

# on `tilt down` -> delete the OpenFaaS function from the cluster
delete_cmd = 'faas-cli delete -f go-fn.yml'

k8s_custom_deploy(
    'go-fn',
    apply_cmd=apply_cmd,
    delete_cmd=delete_cmd,
    # apply_cmd will be re-executed whenever these files change
    deps=['./go-fn.yml', './go-fn/']
)

# add a port forward so we can debug the function from our host machine directly
k8s_resource('go-fn', port_forwards=['9372:8080'])
```

When we run `tilt up`, Tilt will execute the `apply_cmd`, which in our case invokes `faas-cli up` to build and deploy an image and then returns the _result_ as YAML so Tilt can track the new or updated Kubernetes objects.
If `go-fn.yml` or any file in the `go-fn/` directory tree changes, the `apply_cmd` will be automatically re-run.

On `tilt down`, our `delete_cmd` will be invoked, which allows `faas-cli` to delete any objects from Kubernetes it created as well as clean up any extra OpenFaaS state.

## What if Something Goes Wrong?
Integrating an external tool can be tricky!
Luckily, the Tilt API allows us to quickly introspect what's happening behind the scenes.

> 💡 Use `tilt describe kapp` to get a human readable version!

If something goes wrong, the `error` field in the `KubernetesApply` object status will have more information:
```shell
$ tilt get -ojsonpath='{.status.error}' kapp go-fn | head -n 5
apply command returned malformed YAML: error converting YAML to JSON: yaml: control characters are not allowed
stdout:
[0] > Building go-fn.
Clearing temporary build folder: ./build/go-fn/
Preparing: ./go-fn/ build/go-fn/function
```
In this case, our `apply_cmd` wrote back invalid YAML to `stdout` because we forgot to redirect the diagnostic logs to `stderr` - oops!

Or, we can see what objects were deployed:
```bash
$ tilt get -ojsonpath='{.status.resultYAML}' kubernetesapply go-fn | yq '.kind + "/" + .metadata.name'
"Pod/go-fn-fd78fc4d8-d558b"
"Deployment/go-fn"
"ReplicaSet/go-fn-fd78fc4d8"
```

Important information will always be shown in the Tilt web UI, but the API lets you see the exact same data that Tilt is using internally.
We've begun to rely on it ourselves for debugging heavily and hope you find it as useful as we do!

## What's the Catch?
At the moment, it is not practical to use images built with Tilt (e.g. via [`docker_build`][api-docker_build]) in conjunction with [`k8s_custom_deploy`][api-k8s_custom_deploy].
We are still exploring the best semantics for passing Tilt-built image references to external tools.
In its initial state, [`k8s_custom_deploy`][api-k8s_custom_deploy] is best suited for use with pre-built images or tools that handle both image build + deploy.

Additionally, if your tool is capable of templating YAML, and you don't need other functionality provided by it while developing, [`k8s_yaml`][api-k8s_yaml] is often simpler and faster.

## Looking for a More Complete Example?
The [knative Tilt extension][ext-knative] uses [`k8s_custom_deploy`][api-k8s_custom_deploy] to deploy and monitor the Knative serving components.
Be sure to check it out if you're looking to use [Knative serving][knative] with Tilt or a real world example.

[api-docker_build]: https://docs.tilt.dev/api.html#api.docker_build
[api-helm]: https://docs.tilt.dev/api.html#api.helm
[api-k8s_custom_deploy]: https://docs.tilt.dev/api.html#api.k8s_custom_depliy
[api-k8s_yaml]: https://docs.tilt.dev/api.html#api.k8s_yaml
[api-k8s_resource]: https://docs.tilt.dev/api.html#api.k8s_resource
[api-local_resource]: https://docs.tilt.dev/api.html#api.local_resource
[docs-helm-reimplement]: https://docs.tilt.dev/helm.html#re-implementing-the-helm-built-in
[ext-helm_remote]: https://github.com/tilt-dev/tilt-extensions/tree/master/helm_remote
[ext-knative]: https://github.com/tilt-dev/tilt-extensions/tree/master/knative
[helm]: https://helm.sh/
[knative]: https://knative.dev/docs/serving/
[kustomize]: https://kustomize.io/
[openfaas]: https://www.openfaas.com/
[openfaas-blog-tilt]: https://www.openfaas.com/blog/tilt/
[tilt-releases]: https://github.com/tilt-dev/tilt/releases
