---
title: Help teams not yet on Kubernetes, adopt Tilt
layout: docs
---

Tilt is a tool to help dev teams develop software, especially with multiple services that are being deployed to Kubernetes today, or will likely be doing so in the future. The [15 minute tutorial](/tutorial.html) helps you get set up with a single project. And [Tiltfile Concepts](/tiltfile_concepts.html) is a primer on using a Tiltfile to configure Tilt for your specific needs. This doc helps you, as the **devex (developer experience) engineer** or **dev team advocate**, to guide your dev team not yet on Kubernetes, **to adopt Tilt as quickly as possible**.

## Avoid implementing Kubernetes and Tilt at the same time

If your organization already deploys to Kubernetes in production, or is planning to do so soon, you may be tempted to ask your developers to use a local development Kubernetes cluster when they begin using Tilt, in order to streamline broader organizational operations. However, this is especially difficult for a dev team if they are currently developing in a non-Kubernetes environment and/or have little Kubernetes experience. **It is painful for a developer to adopt two new technologies at once, and also adapt their existing code projects accordingly in a Kubernets context.** Rolling out Tilt in this fashion, may actually backfire, since any benefits from the new setup, would be overshadowed by the pain of initial adoption experienced by the dev team. Instead, the best practice is to first introduce Tilt only.

## Tilt is great for non-Kubernetes development

Tilt is fully compatible with non-Kubernetes development. So prior to introducing Tilt to your dev team, [create a Tiltfile](/tutorial.html) to bring up services using [`local_resoure`](/local_resource.html) or [`docker_compose`](/api.html#api.docker_compose) (if your dev team is already using containers, but not yet Kubernetes). Then ask your dev team to [install Tilt](/install.html) and run `tilt up`, to immediately experience the many benefits of Tilt, such as the interactive web UI with a consolidated view of all resources and logs, as well as services that automatically update. Your dev team will quickly see that Tilt is great for multi-service development, even without Kubernetes.

## Provide a local Kubernetes option

Eventually you may want to nudge your dev team toward using Kubernetes for local development. First, [choose a local cluster](/choosing_clusters.html) that meets your operational requirements and help your developers install it in their development environments (e.g., on their laptops). Then, add required Kubernetes yaml files and update the Tiltfile so that resources are [optionally run](/tiltfile_config.html) in Kubernetes, using [`k8s_yaml`](/api.html#api.k8s_yaml). You can now encourage the dev team to run Tilt using the Kubernetes option. It's recommended to keep the legacy non-Kubernetes option available as well, at least temporarily, for instances where a developer is blocked, and needs to revert to the previous mode of development. This allows you, the devex engineer, a migration period to fix bugs in the Tiltfile, as well as guiding developers toward Kubernetes-based Tilt usage, with minimal friction. You can also consider individual migration periods (`local_resource -> k8s_yaml`) for one or more services, instead of all of them at once. Use [Tiltfile Configs](/tiltfile_config.html) to achieve all these options for your dev team.

## Tilt helps your team migrate to Kubernetes development

Tilt helps your dev team with multi-service development, whether that's outside or inside a Kubernetes environment. But if you know your dev team needs to migrate to Kubernetes at some point in the future, Tilt provides a painless path to get there, by providing them with value of Tilt immediately.

<img src="/assets/img/kubernetes-migration.png">
