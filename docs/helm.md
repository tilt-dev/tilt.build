---
title: Installing YAML with Helm
description: "Tilt supports Helm out-of-the-box. Here are two ways you can use Helm charts with Tilt."
layout: docs
sidebar: guides
---

Tilt supports Helm out-of-the-box.

There are two major ways we see teams use Helm charts with Tilt.

- Install a Helm chart from the rich library of existing charts. 

- Iterate on a Helm chart that you're building.

Let's dig into each one.

## Installing existing charts

Many off-the-shelf tools have Helm charts. The chart is an easy way to install a
collection of objects into your Kubernetes cluster.

The [`helm_resource`
extension](https://github.com/tilt-dev/tilt-extensions/tree/master/helm_resource)
makes this easy.

Here's an example that deploys the [Bitnami `mysql`
chart](https://artifacthub.io/packages/helm/bitnami/mysql):

```
# Tiltfile

load('ext://helm_resource', 'helm_resource', 'helm_repo')
helm_repo('bitnami', 'https://charts.bitnami.com/bitnami')
helm_resource('mysql', 'bitnami/mysql', resource_deps=['bitnami'])
```

Visit [Artifact Hub](https://artifacthub.io/) to find Helm charts for
many off-the-shelf tools. They each list the repo URL and chart name to
use with `helm_resource`.

### Pros and Cons of `helm_resource()`

The `helm_resource` function has additional options for adding flags to `helm
install`, redeploying on file changes, and injecting images built locally.

Under the hood, here's how it works:

- On `tilt up`, `helm_resource` will install your chart with `helm install`.

- When the install is finished, `helm_resource` will tell about the objects it installed.

- Tilt will display any logs, events, or health checks in the Tilt UI.

This is perfect if you're installing a new operator or server into your dev
environment, but don't need to debug the installation process.

If you're using Helm to organize your own servers, this can be a bit opaque.
So Tilt also offers a second approach.

## Iterate on chart YAML

The `helm` built-in function lets you load from a chart on your filesystem.

Calling `helm()` runs `helm template` on a chart directory and
returns a blob of the Kubernetes YAML, which you can then
deploy with `k8s_yaml`.

```python
k8s_yaml(helm('./charts/my-chart'))
```

When you make edits to the files in the chart directory, 
Tilt will automatically re-deploy the chart.


### `helm()` Options

The `helm` function has a few options for common arguments:

```python
yaml = helm(
  'path/to/chart/dir',
  # The release name, equivalent to helm --name
  name='release-name',
  # The namespace to install in, equivalent to helm --namespace
  namespace='my-namespace',
  # The values file to substitute into the chart.
  values=['./path/to/chart/dir/values-dev.yaml'],
  # Values to set from the command-line
  set=['service.port=1234', 'ingress.enabled=true']
  )
k8s_yaml(yaml)
```

### Pros and Cons of `helm()`

The `helm()` function treats Helm as a YAML templating tool. You then
register the YAML so that Tilt can deploy it.

Tilt can validate your YAML, split it into individual resources for each server,
and auto-inject images that you built locally.  This makes it a good fit when
you're developing your own chart.

But modern Helm charts are more than just YAML. Helm supports 
[chart hooks](https://helm.sh/docs/topics/charts_hooks/) for modifying the install process.
Helm can also read settings from your cluster, and make installation decisions based
on what cluster you're using.

The `helm()` function uses Tilt's deployment engine, so skips the chart hooks.
It's offline-only. If you want to install a remote chart, you need to use the
`helm_remote` extension to download the chart locally.

### Remote charts

The [`helm_remote` extension](https://github.com/tilt-dev/tilt-extensions/tree/master/helm_remote)
downloads remote charts and loads their YAML with `helm()`.

Here's an example that deploys the `bitnami/mysql` chart:

```python
# Tiltfile

load('ext://helm_remote', 'helm_remote')
helm_remote('mysql',
            repo_name='bitnami',
            repo_url='https://charts.bitnami.com/bitnami')
```

To customize the chart with your own `values.yaml` settings, see the [`helm_remote`
README](https://github.com/tilt-dev/tilt-extensions/tree/master/helm_remote)
for additional options to configure the chart.

### Sub-charts and requirements.txt

If you have chart dependencies, you need to run:

```
helm dep update
```

outside of Tilt to download the dependencies to your repo. Then create a
`.tiltignore` with the contents:

```
**/charts
**/tmpcharts
```

Or, if you want be more cautious:

```
path/to/your/chart/charts
path/to/your/chart/tmpcharts
```

When Helm runs, it touches these chart directories. Adding these lines ensures that Tilt
doesn't reload the Tiltfile every time Helm touches them.

## Advanced Helm

Helm can also do more advanced templating -- like downloading remote charts and injecting run-time variables.

Fortunately, Tilt has a plugin API. You can tell it how to shell out to other build and deploy tools.

The plugin API has two important functions:

- `local()` for running local shell commands

- `watch_file()` for telling Tilt to reload its configuration when a file changes

Let's take a look at some common recipes for using the plugin API with Helm.

### Example Repo

If you prefer to play with a code sample, see

[tilt-dev/tilt-helm-demo](https://github.com/tilt-dev/tilt-helm-demo)

### Re-implementing the `helm()` built-in

To start, let's try implementing the `helm()` built-in ourselves.

```
k8s_yaml(local('helm template path/to/chart/dir'))
watch_file('path/to/chart/dir')
```

The real `helm()` built-in handles some extra optimizations and edge cases, but that's basically all it does!

### Passing a single variable

Now that we know how to shell out to `helm`, we can pass arbitrary flags. Let's try using `--set` to set a variable.

```
k8s_yaml(local('helm template --set key1=val1,key2=val2 path/to/chart/dir'))
watch_file('path/to/chart/dir')
```

### Passing a values file

If you're passing a lot of variables, it's usually better to put those in a values.yaml file.

```
k8s_yaml(local('helm template -f ./values.yaml path/to/chart/dir'))
watch_file('path/to/chart/dir')
watch_file('values.yaml')
```

### Other Helm tools

There are other helm tools like [helmfile](https://github.com/helmfile/helmfile) for working with Helm charts.

We can use the same plugin commands to implement those as well. In this example, we factor out `helmfile` into a helper function.

```
# Helper function to read K8s config YAML from helmfile.
def helmfile(file):
  watch_file(file)
  return local("helmfile -f %s template" % file)

# Tell Tilt to apply to k8s config generated by helmfile.
k8s_yaml(helmfile("k8s/staging/helmfile.yaml"))
```

You can try out this example yourself in [this example repo](https://github.com/tilt-dev/tilt-helmfile-demo).

