---
title: "Custom Resource Definitions"
description: "Configure your custom resources so that Tilt can monitor them."
layout: docs
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

### Is this an indepdent resource?

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

Tilt can sometimes follow the Kubernetes metadata to figure out
which pods belong to which resource. But other times it needs help.

To tell Tilt how to find the pods for a resource, you can use the `k8s_resource` function
for each resource to specify a custom label selector for that resource.

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

## Custom Resource Examples

If you have an example of a custom resource with Tilt you'd like to share, feel free to add it to this page!

- [KubeDB
  Postgres](https://github.com/tilt-dev/tilt-example-frameworks/tree/master/kubedb-postgres) -
  Expose a Postgres server running on Kubernetes.
