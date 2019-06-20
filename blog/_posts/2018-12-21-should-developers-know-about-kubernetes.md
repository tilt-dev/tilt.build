---
slug: should-developers-know-about-kubernetes
date: 2018-12-21T17:18:07.059Z
author: dmiller
layout: blog
canonical_url: "https://medium.com/windmill-engineering/should-developers-know-about-kubernetes-1df432ce057d"
title: "Should Developers Know about Kubernetes?"
image: featuredImage.jpeg
image_caption: "Intrepid Windmill employees hanging out with various Kubernetes mascots"
tags:
  - kubernetes
  - devops
  - docker
  - programming
  - microservices
keywords:
  - kubernetes
  - devops
  - docker
  - programming
  - microservices
---

That’s a wrap on Kubecon 2018, and on 2018 as a whole. As I reflect on the Kubecon experience, one question stands out: should application developers be aware of Kubernetes?

I heard this question asked by cluster operators, developers, and vendors alike. The outcome of this debate will shape the future of Kubernetes. Let’s look at the two sides of this debate, with an eye towards the trends I’ve observed over my career as an infrastructure engineer.

### Kubernetes is an implementation detail: hide it

Kubernetes provides far more functionality than your average developer actually needs. I’ve been working with Kubernetes for a year and off the top of my head I can only name 8 kinds of objects, out of around 50 total. (For context, [k3s](https://github.com/ibuildthecloud/k3s) is a minimal Kubernetes distribution that axed a huge number of features and runs the majority of Kubernetes apps just fine.) Developers don’t care how many replicas of their service are running, or what `Role`s it has, or whether it’s running via `StatefulSet`s; all they care about is getting an HTTP endpoint up that helps deliver a product. As a result, some operators choose to hide Kubernetes inside the CI/CD pipeline. Devs don’t get bogged down by k8s minutiae; they simply push code to GitHub and the rest is taken care of for them.

Even if developers are fluent in Kubernetes, operators may be reluctant to give them unfettered access to a cluster, since small changes can have outsized ripple effects. (For instance: changes to resource limits for a Pod or Container could cause issues with other deployments that are scheduled to the same nodes.) In many organizations operators will provide an intermediary layer, either with a DSL or a separate API, to restrict what developers can modify and maintain a tighter control of the cluster.

### Kubernetes is the lingua franca of infrastructure: expose it

Developers are no longer just writing application code. As our industry moves more towards microservices, developers are empowered (and expected) to make more infrastructure decisions — and must then build and maintain that infrastructure.

Kubernetes is quickly becoming the de facto way to specify infrastructure. Everything a system needs — including processes, load balancers and GPUs — can now be articulated in YAML and scheduled via Kubernetes. As Kubernetes becomes more prevalent developers will write tons of documentation, from tutorials to stack overflow answers, making it the way to make infrastructure explicit. We see this today with Dockerfiles. A couple of years ago the installation instructions for a developer tool probably contained a slew of `apt-get` commands. Today all that environment specific setup has been replaced by a single `docker run` command.

As someone who’s worked at places with home-grown container orchestrators and ORMs, I know first-hand that the Google-ability that standardization affords is invaluable.

Just as developers chafe at being denied shell access to servers when they’re trying to debug something, they will chafe at not being able to see the underlying Kubernetes definitions when debugging a services issue.

### Looking to history

As is often the case, both sides have a point. Kubernetes is really complicated, potentially distracting, and because of its complexity, easy for the inexperienced to mess up in unpredictable ways. However, it’s also the best way to make your infrastructure explicit — and these days developers are dealing with *more* infrastructure, not less.

I’m reminded of the transformation we went through a couple years ago with Docker. Prior to Docker, the notion of dependencies for applications only went as far as code dependencies: First it was `.deb` packages ensuring that ImageMagick was installed; then it was `Gemfiles` and `package.json`s making native dependency management easier. Eventually we realized that there were other, implicit dependencies that weren’t described, such as the kernel version or the layout of the filesystem. There’s nothing more frustrating then running `gdb` to diagnose an issue in production only to discover that the kernel version is different from box to box. Dockerfiles finally allowed us to specify these system-level dependencies.

Today we need a similarly simple way to express service dependencies. Even for a basic LAMP app, communicating to coworkers that you added a Redis dependency is an exercise in relentless repetition. In a 100-engineer organization with a complex microservices app, changing the topology can mean days of helping junior engineers debug their broken dev environments. We need Dockerfile but for microservices; and while you can imagine a universe where operators handle all the Dockerfiles and devs keep their hands totally clean, it’s much easier to write code and debug problems when you can understand at least a bit of what goes on in your Dockerfile. Likewise, whatever our new way of specifying services and their dependencies, developers will learn it and take advantage of it to gain more leverage over their increasingly complex environments.

Just as Docker grew namespaces and cgroups into a user-friendly product, something must grow Kubernetes in to a user-friendly service dependency framework.

### Looking to the future

I’ve heard it said that Kubernetes makes easy things hard and hard things possible. This is true both in production and development. For example: it’s easy to make a highly available stateless app on Kubernetes, but comparatively hard to do something simple like get the errors for a pod.

We want to fix this, and we’re starting with [Tilt](https://tilt.build/). Tilt allows you to develop all your microservices locally in Kubernetes while collaborating with your team.

[Tilt](https://tilt.build/) makes common development tasks easy. It doesn’t treat Kubernetes like a black box, nor does it force you to worry about `ConfigMap`s in your day to day. Rather, Tilt treats Kubernetes like a gray box. It offers a simplified, actionable interface that doesn’t restrict you from digging in to the API when you need to.

If all cluster operators decided tomorrow that developers should never touch Kubernetes, we still think Tilt would be useful to lots of people: but I don’t see that happening. Software is getting too complex, and business requirements are evolving too rapidly to fully isolate developers from infrastructure. We need to embrace the complexity.
