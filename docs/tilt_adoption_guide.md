---
title: Tilt Adoption Guide for Dev Teams
layout: docs
---

Tilt is a tool to help dev teams develop software, specifically during the [inner-loop of development](https://mitchdenny.com/the-inner-loop/), and especially with multiple services that are being deployed to Kubernetes today, or will be doing so in the future. The [15 minute tutorial](/tutorial.html) helps you get set up with a single project. And [Tiltfile Concepts](/tiltfile_concepts.html) is a primer on using a Tiltfile to configure Tilt for your specific needs. This guide helps you, as the **dev team lead** or **dev team advocate**, to adopt Tilt in a methodical way for your dev team, regardless of your greater organization's current Kubernetes migration progress.

## Stay ahead of Kubernetes production migration

We've seen many organizations have a detailed Kubernetes production migration plan, but with little appreciation on how it will impact development and dev teams. Sometimes dev teams will be left scrambling to learn Kubernetes and adjust their workflows in a short migration time window. The best practice is for you, as the dev team, to **stay ahead** of your organization's Kubernetes production migration plan. In particular, developers can adopt Tilt today, getting the benefits of streamlined multi-service development, even before production has moved to Kubernetes. By staying ahead, you can introduce change at your own schedule, having a stronger voice in the resulting dev workflows that will eventually ship to a Kubernetes production environment. If your organization has already started the Kubernetes production migration process, be sure to adopt Tilt as soon as you can to catch up, since you **do not need to wait** until it has finished.

## Just-in-time learning for Kubernetes

Kubernetes is a new technology aimed at solving problems for production operators, not software developers. As such, your dev team might be put off if they hear that your organization is moving to Kubernetes, and they are forced to learn something that can be quite complicated. Don't overwhelm them by asking them to learn Kubernetes all at once, especially since Tilt abstracts away much of the low-level details anyways. Instead, follow the steps below, and have the team learn new concepts incrementally, only when they are rewarded with immediate value. In particular, only the last step requires developers to learn Kubernetes. There is already a lot of direct developer value from Tilt, in the earlier steps. **We want developers to experience the many benefits of Tilt, before asking them to learn Kubernetes.** 

_Rough outline for rest of document_

## Stage 1: Install Tilt and set up Tiltfile

- Everyone on the team installs Tilt.
- Set up a Tiltfile. Check it into source code.
- Developers install Tilt.
- Set up Tilt Cloud and set_team (Optional)
- You can wrap _one_ services in Tilt local_resource within Tilt right now.
- Production could be using containers and/or Kubernetes.
- First step is to start using local_resource to help your team adopt Tilt and get it's benefits right away with minimal risk and effort.
- Get feedback from your development team. Observe Tilt Cloud.

## Stage 2: Use Tilt Cloud to facilitate team adoption (optional)

- Use Tilt Cloud to see adoption.
- Use snapshots for debugging and helping developers.

## Stage 3: Scale to all services on your team

- Get the rest of your services into Tilt with local_resource

## Stage 4: Tilt with containers

- Teach team about containers and Docker.
- Containers and Tilt docker_compose
- If your company is using docker-compose for production, you can make your development more production-like right away.
- To go from Stage 1 to Stage 2, need a docker-compose yaml file.
- Don't have to do it all at once. Can use mix of local_resource and docker_compose

## Stage 5: Tilt with local Kubernetes cluster

- Teach team about orchestration and Kubernetes
- Choose a local cluster.
- Help devs install local cluster.
- Minimal k8s knowledge required.
- To get to stage 3, need a Kubernetes yaml file
- You can do this even before production goes to kubernetes.
- Staying ahead, helps you mitigate risk.
- Developers have a stronger voice.
- Don't have to do it all at once. Can use mix of docker_compose and k8s_yaml.

## Key insight: Deliver value to your dev team immediately

Help your team get value in a multi-service context immediately. Don't wait for Kubernetes production migration.