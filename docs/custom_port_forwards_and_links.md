---
title: Custom port forward names and additional links for resources
layout: docs
---

By default, port forward links for resources are displayed as `localhost:<port-number>` in Tilt, at the top of the screen. This may be confusing if you have multiple port forwards per resource, such as:

<figure>
    <img src="/assets/img/port-forwards.png" title="Port forwards">
</figure>

A user would not know which port forward corresponds to which part of your app, without reading the Tiltfile. Tilt allows you to specify custom port forward names, displaying them in the UI instead of `localhost:<port-number>`. For example, specifying this in the Tiltfile

```
k8s_resource(
   'blog-site', 
   port_forwards=[
      port_forward(4002, name='blog-hero-post'), 
      port_forward(4003), 
      port_forward(4004, name='blog-archives')
   ]
)
```

would show this in Tilt:

<figure>
    <img src="/assets/img/port-forward-names.png" title="Port forward names">
</figure>

Read more in the [`port_forward` API](/api.html#api.port_forward).

You can also associate aribitrary links with a resource. For example, you may want to point users to a database URL for a database reset workflow. Specifying this in the Tiltfile

```
k8s_resource(
   'blog-site', 
   port_forwards=[
      port_forward(4002, name='blog-hero-post'), 
      port_forward(4004, name='blog-archives')
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

Read more in the [`k8s_resource`](/api.html#api.k8s_resource), [`local_resource`](/api.html#api.local_resource), and [`link`](/api.html#api.link) APIs.