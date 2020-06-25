---
title: Tiltfile Resource Assembly Migration
description: "Tilt changed how it combines k8s objects and images into Tilt resources."
layout: docs
---

Tilt changed how it combines k8s objects and images into Tilt [resources](tiltfile_concepts#resources). The new behavior is to simply make one Tilt resource per k8s object that has at least one
container.

The TL;DR is:
* Your tilt resources' names may have changed.
* You might need to change how you're calling `k8s_resource`.
* If you were using `k8s_resource_assembly_version` to revert to the old way that assembly worked, you will have to remove that as Tilt is removing the old assembly functionality.

The old `k8s_resource` behavior was kind of weird: sometimes you could just use
the image name, and sometimes you'd pass the yaml, and sometimes you'd pass the
image. Sometimes it was used for creating a resource, and sometimes it was used
for configuring an existing resource.

We've eliminated `k8s_resource`'s 'yaml' and 'image' parameters. It's now a
function for configuring a workload's resource. ([See the API docs for the new `k8s_resource`](api.html#api.k8s_resource))

Migrating to the new behavior should mostly be a matter of:
1. Remove any 'yaml' or 'image' args to `k8s_resource` calls
2. and make sure any removed 'yaml' args from (2) are passed to `k8s_yaml` somewhere else in your Tiltfile.
3. If your `k8s_resource` calls say unknown resource (because Tilt now names by k8s object instead of image),
   either change the first arg to `k8s_resource` to match the new name, or use [`workload_to_resource_function`](/api.html#api.workload_to_resource_function) to change the naming rules.
4. Let any teammates know that they need to upgrade Tilt.

Please don't hesitate to [reach out](faq.html#q-how-do-i-get-help-with-tilt)
if you run into any problems or confusion!
