---
title: Modifying YAML for Dev
description: "How to adapt your prod Kubernetes configs to your dev environment."
layout: docs
sidebar: guides
---

Kubernetes lets you define your running services with declarative YAML.

It's really common to want to make a few tweaks to that YAML for dev, e.g.,

- Set an env variable like `DEBUG=true`.

- Set the number of servers to exactly 1 (rather than auto-scaling).

- Set a label to distinguish dev servers from prod servers.

Fortunately, there's a great ecosystem of YAML management tools to help you!
[`helm`](https://helm.sh/),
[`kustomize`](https://kustomize.io/), and [`ytt`](https://carvel.dev/ytt/)
are all great.

In this guide, we'll show you how to patch your YAML for your dev environment -- either 
with a few lines of Tiltfile code or with one of the tools above.

## What Tilt Does Automatically

Let's start with a basic example project:

```python
docker_build('example-html-image', '.')
k8s_yaml('deployment.yaml')
```

When Tilt deploys this YAML, it will automatically:

- Apply the label `app.kubernetes.io/managed-by: tilt` to every resource.

- Ensure that all containers have `pullPolicy: IfPresent` or `pullPolicy: Never`
  set when using a local cluster (so that you get the locally-built image).  app

- Inject a fully-resolved image tag into the resource.

If you want to drill down more, you can use the CLI to explore
what YAML Tilt is aware of and what it has applied to the cluster.

To view the YAML sets in a running dev env, use:

```
$ tilt get kubernetesapply
NAME        CREATED AT
tilt-site   2022-01-18T15:20:55Z
docs-site   2022-01-18T15:20:55Z
blog-site   2022-01-18T15:20:55Z
```

This tells us we have 3 resources that apply YAML: `tilt-site`, `docs-site`, and `blog-site`.

To see the YAML in a specific resource:

```
$ tilt get kubernetesapply docs-site -o yaml
```

This will print both `spec.yaml` (the YAML that you originally gave Tilt)
and `status.resultYAML` (the YAML that came back from the cluster).

## How to Make Small Patches in a Tiltfile

If you're already using a tool like Helm for managing YAML, keep using it! It's
great! Tilt is NOT trying to replace it for you!

But for one-off cases where you want to make a small patch, 
here are a few Tiltfile APIs that you may see:

- `read_yaml_stream` reads a file from disk and decodes it to a list of objects.

- `decode_yaml_stream` takes a YAML string and decodes it to a list of objects.

- `encode_yaml_stream` takes a list of objects and encodes them to a string.

For example, to set the namespace on a list of objects:

```python
objects = read_yaml_stream('deployment.yaml')
for o in objects:
  o['metadata']['namespace'] = 'my-ns'
k8s_yaml(encode_yaml_stream(objects))
```

You can see this approach in practice in [the `namespace`
extension](https://github.com/tilt-dev/tilt-extensions/tree/master/namespace).

## How to Connect Existing YAML Tools

If you have an existing shell script that produces YAML,
connecting it to Tilt is easy.

```python
k8s_yaml(local('./generate-yaml.sh'))
```

Tilt will run the script on startup, register the YAML, and deploy it.

This approach is so common that there are two built-in functions
for pulling YAML from existing templating tools:

- [`kustomize('.')`](/api.html#api.kustomize) invokes `kustomize` on the given directory.

- [`helm('./path/to/chart')`](/api.html#api.helm) invokes `helm template` on the given chart directory.

Both of these functions return YAML so that you can register them with `k8s_yaml`.

They're both simply wrappers around `local()`, but have some nice ergonomics for
passing arguments and watching dependencies.

If you'd like to add new template tools, you don't need to make them built-in
functions! These tools can be packaged up as [Tilt Extensions](/extensions.md)
and shared with the community of Tilt users.

## When YAML is Not Enough

Some modern Kubernetes tools don't produce a pile of YAML for you to deploy
yourself.

They deploy resources in a particular order, wait on health checks, or 
add post-deploy hooks. Then they output the YAML at the end!

For example,
[Pulumi](https://www.pulumi.com/docs/get-started/kubernetes/review-project/)
lets you define your infra in Javascript or Python. Helm can download packages
from a remote repository you found on
[Artifact Hub](https://artifacthub.io/). And Helm packages can have [chart
hooks](https://helm.sh/docs/topics/charts_hooks/) that modify the release
life-cycle.

For these tools, we recommend using
[`k8s_custom_deploy`](/custom_resource.html#using-k8s_custom_deploy) to deploy
instead of `k8s_yaml`. For an example, see [the `helm_resource`
extension](https://github.com/tilt-dev/tilt-extensions/tree/master/helm_resource).

## Further Reading

- For more on Helm, we have [a complete Helm guide](/helm.html).

- For more on `k8s_custom_deploy` and non-YAML deploys, see ["Deploy All The Things Even If They Aren't YAML."](https://blog.tilt.dev/2021/12/03/k8s-custom-deploy.html)

- For more on Kustomize interop, see ["Are You My Kustomize?"](https://blog.tilt.dev/2020/02/04/are-you-my-kustomize.html)
