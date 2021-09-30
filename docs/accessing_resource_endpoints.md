---
title: Accessing your resource with endpoints
layout: docs
sidebar: guides
---

## Access your resource with Kubernetes port forwarding

As you're configuring [resources in Tilt](/tiltfile_concepts.html#resources), you'll often want to access an app within a Kubernetes resource, for example, a web app or a database server. Kubernetes provides [port forwarding](https://kubernetes.io/docs/tasks/access-application-cluster/port-forward-access-application-cluster/) to allow you to access via your local machine with `localhost`. Tilt exposes this feature through a configuration in [`k8s_resource`](/api.html#api.k8s_resource). For example, if you have in your Tiltfile: 

```
k8s_resource(workload='blog-site', port_forwards=4002)
```

`localhost:4002` will be connected to container port 4002. Tilt also displays a link at the top of the screen.

<figure>
   <img src="/assets/img/port-forward.png" title="Port forward">
</figure>

With:

```
k8s_resource(workload='blog-site', port_forwards='9000:4002')
```

`localhost:9000` will be connected to container port 4002.

## Naming port forwards

A resource may have multiple port forwards. You can configure them with:

```
k8s_resource(
   workload='blog-site',
   port_forwards=['9000:4002', '9001:4003']
)
```

And you would see:

<figure>
    <img src="/assets/img/port-forwards.png" title="Port forwards">
</figure>


In this case, a user may not know which port forward corresponds to which part of your app, without reading the Tiltfile. Tilt allows you to specify custom port forward names, displaying them instead of `localhost:<port-forward>`. For example, specifying this in the Tiltfile

```
k8s_resource(
   workload='blog-site',
   port_forwards=[
      port_forward(9000, 4002, name='blog-hero-post'), 
      port_forward(9001, 4003, name='blog-archives')
   ]
)
```

would show this in Tilt:

<figure>
    <img src="/assets/img/port-forward-names.png" title="Port forward names">
</figure>

Read more in the [`port_forward` API](/api.html#api.port_forward).


## Arbitrary links

You can also associate aribitrary links with a resource, using [`link`](/api.html#api.link). For example, you may want to point users to a database URL for a database reset workflow. Specifying this in the Tiltfile:

```
k8s_resource(
   workload='blog-site',
   port_forwards=[
      port_forward(9000, 4002, name='blog-hero-post'), 
      port_forward(9001, 4003, name='blog-archives')
   ],
   links=[
      'blog-db.storage.acme.com',
      link('internal-eng.acme.com/docs/blog-db-reset', 'Blog db reset docs')
   ]
)
```

would show this in Tilt:

<figure>
    <img src="/assets/img/additional-resource-links.png" title="Additional resource links">
</figure>

Arbitrary links are supported on both [`local_resource`](/api.html#api.local_resource) and `k8s_resource`.
