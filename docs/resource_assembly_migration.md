---
title: Tiltfile Resource Assembly Migration
layout: docs
---

Tilt is changing how it combines k8s objects and images into Tilt resources.

If you don't want to deal with this right now, you can get back the old
behavior for now by adding `k8s_resource_assembly_version(1)` to the top of
your Tiltfile. We plan to remove that option on 2019-05-01. [Please let us know](http://localhost:4001/faq.html#q-how-do-i-get-help-with-tilt) if you have questions or concerns about any of this!

The old behavior was roughly to make one Tilt resource per image, and associate
a resource with all k8s objects that use that image. This led to confusing behavior
when multiple Deployments used the same image, and was just generally unintuitive.

The new behavior is to simply make one Tilt resource per k8s object that has a
container. It's described [here](tiltfile_concepts.html#resources).

This might affect you in a few ways:
* Tilt resources are now named after their k8s objects rather than their images.
* If you had multiple k8s objects using the same image, they'll now each be
a separate Tilt resource, instead of all getting combined into one.
* `k8s_resource` arguments are changing.

The old `k8s_resource` behavior was kind of weird: sometimes you could just use
the image name, and sometimes you'd pass the yaml, and sometimes you'd pass the
image. Sometimes it was used for creating a resource, and sometimes it was used
for configuring an existing resource.

We've eliminated `k8s_resource`'s 'yaml' and 'image' parameters. It's now a
function for configuring a workload's resource. You can find documentation
for its new behavior [here](api.html#api.k8s_resource).

Migrating to the new behavior should mostly be a matter of removing any 'yaml'
or 'image' args to `k8s_resource` calls, and making sure those 'yaml' args
are passed to `k8s_yaml` somewhere else in your Tiltfile.

Please don't hesitate to [reach out](http://localhost:4001/faq.html#q-how-do-i-get-help-with-tilt)
if you run into any problems or confusion!
