---
title: Resource Dependencies
layout: docs
---

Say you have a web service specified in a Tilt resource named `frontend` and a
database in a Tilt resource named `database`, and `frontend` fails to even
start up if `database` isn't running. This can lead to distracting errors on
startup (especially, e.g., if you have 5 services all depending on the same
backend!)

Tilt allows you to specify that `frontend` depends on `database`, so that
`frontend` will not be deployed until `database` has been successfully deployed:

```python
k8s_resource('frontend', resource_deps=['database'])
```

This has two effects:
1. `frontend` will not be deployed until `database` has been ready at least once
    since Tilt was started.
2. If you run `tilt up frontend` to select only some of your Tiltfile's resources,
    that also implicitly selects all of `frontend`'s transitive dependencies.

A resource is "ready" when:
* For K8s resources: the pod is running and K8s considers all of its containers ready
* For docker-compose resources: the container is started (NB: Tilt doesn't currently observe docker-compose health checks)
* For local resources: the command has succeeded at least once

Some other use cases:
* Define your resource deps such that teammates who work on different subsets of services
  can simply `tilt up svc1 svc2` to get the services they are working on, and
  any dependencies they need to work on those services, without having to
  explicitly list them all.
* Create a `local_resource` to generate language bindings from protobuf schemas,
  and make the services that use those language bindings depend on that `local resource`.

Caveat:
This feature currently mostly only helps in the common case that different versions
of services are broadly compatible with each other, and focuses on ensuring that
*some* instance of a resource's dependencies exist, without worrying too much about
whether it's a *current* version. A couple of ways in which this might affect your
expectations:
1. `resource_deps` only affects the first build after a `tilt up`. Once any version
    of `database` has been running at least once, its dependencies are unblocked
    for the rest of Tilt's lifetime.
2. Due to Tilt's ability to [reuse instances from previous Tilt invocations](https://blog.tilt.dev/2019/10/14/september-commit-of-the-month.html),
    if you have an old `database` running when you `tilt up`, it can satisfy
    `frontend`'s dependency. This can make it seem like `resource_deps` is not
    having any effect.

We think this feature is useful as-is, but are aware there are more possibilities
for it. Please [reach out](https://tilt.dev/contact) if it's not meeting your
needs!
