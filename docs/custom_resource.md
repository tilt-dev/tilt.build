---
title: "Custom Resource Definitions"
description: "Configure your custom resources so that Tilt can monitor them."
layout: docs
sidebar: guides
---

Kubernetes defines well-thought-out primitives like Deployments, Jobs, and
StatefulSets for running your containers.

Tilt knows how to inject images, monitor status, and fetch logs for these
built-in resources.

But your team may define your own custom resources! Or you may use a project
like KubeDB that uses custom resources to operate a database.

Tilt needs your help to recognize them.

## Custom Resource Functions

For any resource, Tilt needs to know 3 things:

### Is this an independent resource?

By default, Tilt doesn't categorize custom resources. They all get grouped together
in one "uncategorized" bucket of resources.

When a resource is independent, Tilt deploys it separately, and gives it its own
log pane.

You can watch its status and logs separate from other resources.

To make a resource independent, use the `k8s_resource` function in your
Titlfile:

```python
k8s_resource(new_name='my-postgres-server',
             objects=['postgres-name'])
```

### Does it contain images?

Tilt can build images and deploy them with your resource -- if it knows how to find them!

To identify the location of the resource, use the `k8s_kind` function in your Tiltfile:

```python
k8s_kind('UselessMachine', image_json_path='{.spec.image}')
```

See the [k8s_kind API docs](api.html#k8s_kind) for more detail, or look at [this
example](https://github.com/tilt-dev/tilt/blob/master/integration/crd/Tiltfile#L8).

### Does it create pods?

Tilt can sometimes follow the Kubernetes metadata to figure out which resources
have pods, and which pods belong to which resource. But other times it needs
help.

To tell Tilt that a resource has pods, and it should wait for them to become healthy:

```python
k8s_kind('UselessMachine', image_json_path='{.spec.image}', pod_readiness='wait')
```

To tell Tilt that a resource does NOT have pods, and it should consider a
resource healthy if no pods come up:


```python
k8s_kind('UselessMachine', image_json_path='{.spec.image}', pod_readiness='ignore')
```

Most custom resources set owner references, which Tilt can follow to determine
which pods belong to your resource. If your resource does not, you can use the
`k8s_resource` function for each resource to specify a custom label selector for
that resource.

```
k8s_resource(new_name='postgres',
             extra_pod_selectors=[{'kubedb.com/name': 'quick-postgres'}])
```

See the [k8s_resource API docs](api.html#k8s_resource) for more detail, or look
at [this
example](https://github.com/tilt-dev/tilt-example-frameworks/blob/master/kubedb-postgres/Tiltfile)
that selects the Postgres pods created by the KubeDB Postgres operator.

### Congratulations!

Once you've specified a resource name, an image location, and a pod selector for your custom
resource, you can treat it like any other Kubernetes built-in.

Tilt will automatically fetch logs, and create any port-forwards you specify.

## Installing Custom Resource Operators

To use a custom resource in a cluster, you'll need to install
the [Kubernetes operator](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/) that reads the new object type.

Most frameworks have an installation guide to help you set it up.

Here are some options for standardizing that installation in a Tilt environment.

### Using `local()` or `local_resource()`

The [`local`](/api.html#api.local) Tiltfile function can run arbitrary shell
scripts. This is the easiest way to get started.

But `local` is a blunt instrument - it will run everytime the Tiltfile reloads,
and it will block startup while it waits for the install to finish.

```python
local('./install-my-crd-operator.sh')
```

If you want to parallelize it, you can use `local_resource()`:

```python
local_resource(
  name='my-crd-operator',
  cmd='./install-my-crd-operator.sh',
  allow_parallel=True)
```

Then, use [`resource_deps`](resource_deps.html) on your other resources to make
sure they wait on your `local_resource` to finish.

```python
k8s_resource(
  name='custom-resource',
  resource_deps=['my-crd-operator'])
```

### Using `k8s_custom_deploy()`

The [`k8s_custom_deploy`](/api.html#api.k8s_custom_deploy) Tiltfile function
uses a shell script to apply changes to a cluster.

The install shell script must print the result YAML to `stdout`
so that Tilt can track which objects the custom deployer has created.

```
k8s_custom_deploy(
  name='my-crd-operator',
  apply_cmd='./install-my-crd-operator.sh',
  delete_cmd='./teardown-my-crd-operator.sh')
```

Use `k8s_custom_deploy` if you want to monitor the health of your operator and
view its logs from the interface. See the
[`knative`](https://github.com/tilt-dev/tilt-extensions/blob/master/knative/Tiltfile)
extension for a working example.

## Advanced Pod Creation
    
Many Kubernetes-based frameworks create pods that themselves create other pods!

How do you build images for these second-order pods?

We see two common techniques:

### Custom Resource Injection

If the framework uses a custom resource, you can use the `k8s_kind` function
described above to inject an image anywhere in the resource! It doesn't have to
be a "normal" image field.

```
k8s_kind('UselessMachine', image_json_path='{.spec.imageToDeploy}')
```

### Env Variable Injection

Another common strategy is to use environment variables.

In your Kuberentes container spec, add an env variable like:

```
env:
- name: IMAGE_TO_DEPLOY
  value: my-image
```

In your Tiltfile, build the image, and tell Tilt to look in env variables for the image name.

```
docker_build('my-image', '.', match_in_env_vars=True)
```

Tilt will replace `my-image:latest` with the content-based image reference that
Tilt built. (The custom_build guide has [more
details](custom_build.html#why-tilt-uses-immutable-tags) on this.)  Your
framework can then read the image reference and create pods with it.

The [Airflow
example](https://github.com/tilt-dev/tilt-example-frameworks/tree/master/airflow)
uses this strategy with Airflow's
[KubernetesPodOperator](https://airflow.apache.org/docs/stable/kubernetes.html).

## Custom Resource Examples

If you have an example of a custom resource with Tilt you'd like to share, feel free to add it to this page!

- [KubeDB
  Postgres](https://github.com/tilt-dev/tilt-example-frameworks/tree/master/kubedb-postgres) -
  Expose a Postgres server running on Kubernetes.
- [ElasticSearch and Kibana](https://github.com/tilt-dev/tilt-example-frameworks/tree/master/kibana) -
  Expose a ElasticSearch cluster with a Kibana frontend running on Kubernetes.
- [Airflow](https://github.com/tilt-dev/tilt-example-frameworks/tree/master/airflow) -
  Deploy an Airflow cluster and iterate on tasks. This doesn't use custom resources
  but it demonstrate alternative ways of using and injecting images.
- [Prometheus](https://github.com/tilt-dev/tilt-example-frameworks/tree/master/prometheus) -
  Deploy the Prometheus operator and an instance of Prometheus. Demonstrates how to
  use resource dependencies and pod selectors to install the CRDs in the right order,
  and monitor the pods created by those CRDs.
- [Knative](https://github.com/tilt-dev/tilt-extensions/tree/master/knative) -
  Knative gives you CRDs to describe scale-to-zero services with DNS set up for
  you. The Knative extension has Tiltfile functions to help set it up.  Install
  the Knative operator with `knative_install`, and inject images into Knative
  Services with `knative_yaml`.
