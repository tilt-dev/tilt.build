---
title: Links to Your Services
layout: docs
---

You have a few services running on Tilt. And they're all green!

Now you want to navigate to them to see how they look.

Tilt standardizes your dev environment so that on every dashboard, you have links
to the services that you're running. And Tilt takes care of the plumbing that makes
those links work, from `kubectl port-forward` to public tunnels like `ngrok`.

## Displaying a Static Link

All resources in your Tiltfile support a [`link`](/api.html#api.link) to add links manually.

For example, you may want to point users to a database URL for a database reset workflow. 

If your Tiltfile contains:

```
k8s_resource(
   workload='blog-site',
   links=[
      'blog-db.storage.acme.com',
      link('internal-eng.acme.com/docs/blog-db-reset', 'Blog db reset docs')
   ]
)
```

then you will see the new links show up on the main dashboard.

<figure>
    <img src="/assets/img/additional-resource-links-table.png" title="Additional resource links">
</figure>

You can also see the links on the individual resource page.

<figure>
    <img src="/assets/img/additional-resource-links.png" title="Additional resource links">
</figure>


You can specify links for:
- Local servers run with [`local_resource`](/local_resource.html),
- Kubernetes servers with [`k8s_resource`](/api.html#api.k8s_resource),
- and Docker Compose servers with [`dc_resource`](/api.html#api.dc_resource).

## Creating a `kubectl port-forward` tunnel

Kubernetes provides [port
forwarding](https://kubernetes.io/docs/tasks/access-application-cluster/port-forward-access-application-cluster/)
to allow you to access via your local machine with `localhost`.

Tilt exposes this feature through a configuration in
[`k8s_resource`](/api.html#api.k8s_resource). For example, if you have in your
Tiltfile:

```
k8s_resource(workload='blog-site', port_forwards=4002)
```

`localhost:4002` will be connected to container port 4002. 

Tilt automatically displays a link at the top of the screen. No need to manually create it with the `links=` API.

<figure>
   <img src="/assets/img/port-forward.png" title="Port forward">
</figure>

With:

```
k8s_resource(workload='blog-site', port_forwards='9000:4002')
```

`localhost:9000` will be connected to container port 4002.

## Bulk Creation of `kubectl port-forward` tunnels

If you're starting out with Kubernetes and still exploring, 
[`kubefwd`](https://kubefwd.com/) can bulk-forward all your services automatically, rather
than forcing you to pick and choose which services you want tunnels for.

Tilt's `kubefwd` operator will create port-forwards for every service
in the namespace you're deploying to.

```
# kubefwd all namespaces Tilt deploys to.
v1alpha1.extension_repo(name='default', url='https://github.com/tilt-dev/tilt-extensions')
v1alpha1.extension(name='kubefwd:config', repo_name='default', repo_path='kubefwd')
```

The only downside of `kubefwd` is that Tilt will need to prompt you for `sudo`
privileges, because it changes the DNS on your local machine.

For more details, refer to the [kubefwd extension
documentation](https://github.com/tilt-dev/tilt-extensions/tree/master/kubefwd).

## Naming All Those Port Forwards

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


In this case, a user may not know which port forward corresponds to which part
of your app, without reading the Tiltfile.

Tilt allows you to specify custom port forward names, displaying them instead of
`localhost:<port-forward>`. For example, specifying this in the Tiltfile

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

## Public Tunnels

[`ngrok`](https://ngrok.com/) can create public tunnels for your services,
to expose them on a public URL rather than on `localhost`.

Tilt has an `ngrok` operator that adds buttons to the Tilt UI, which you can
click to start/stop the public tunnel when you need it.

For more info, see:
- ["How to Standardize Ngrok Tunnels in Your Dev Environment"](https://blog.tilt.dev/2021/09/21/ngrok-operator.html)
- [The ngrok extension README](https://github.com/tilt-dev/tilt-extensions/blob/master/ngrok/README.md)
