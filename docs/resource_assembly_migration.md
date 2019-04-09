---
title: Tiltfile Resource Assembly Migration
layout: docs
---

Tilt is changing how it combines k8s objects and images into Tilt [resources](tiltfile_concepts#resources). The new behavior is to simply make one Tilt resource per k8s object that has at least one
container.

The TL;DR is:
* Your tilt resources' names might change.
* You might need to change how you're calling `k8s_resource`.
* You might need to temporarily add a call to `k8s_resource_assembly_version` to the top of your Tiltfile.

The old `k8s_resource` behavior was kind of weird: sometimes you could just use
the image name, and sometimes you'd pass the yaml, and sometimes you'd pass the
image. Sometimes it was used for creating a resource, and sometimes it was used
for configuring an existing resource.

We've eliminated `k8s_resource`'s 'yaml' and 'image' parameters. It's now a
function for configuring a workload's resource. ([See the API docs for the new `k8s_resource`](api.html#api.k8s_resource))

Migrating to the new behavior should mostly be a matter of:
1. Adding a call to `k8s_resource_assembly_version(2)` to the top of your Tiltfile (if running Tilt version < 0.8.0)
2. removing any 'yaml' or 'image' args to `k8s_resource` calls
3. and making any removed 'yaml' args from (2) are passed to `k8s_yaml` somewhere else in your Tiltfile.
4. Letting any teammates know that they need to upgrade Tilt.

Please don't hesitate to [reach out](faq.html#q-how-do-i-get-help-with-tilt)
if you run into any problems or confusion!
