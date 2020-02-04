---
slug: microservices-hidden-problem-understanding
date: 2019-03-29T11:09:12.225Z
author: dan
layout: blog
canonical_url: "https://medium.com/windmill-engineering/microservices-hidden-problem-understanding-db42c3d0a2b6"
title: "Microservices’ Hidden Problem&#58; Understanding"
subtitle: ""
image_needs_slug: true
images:
  - featuredImage.png
tags:
  - kubernetes
  - microservices
  - development
  - tilt
keywords:
  - kubernetes
  - microservices
  - development
  - tilt
---

How many times have you been iterating on code and realized your microservice app was broken, but you weren’t sure where the error was hiding? When we talk to Devs, they say they spend hours each week hunting for the right log line, forced to play 20 questions with kubectl. The problem? You’re using a tool that only solves half of your problem.

After you save a file, you want to **Update** your developer instance to use your new code. Kubernetes updating is clumsy and slow, which has led many to write tools to improve the situation.

But these tools don’t help you **Understand**. When you can’t Understand, you can’t iterate. Faster Update isn’t enough.

> The state of the art? Open N terminals, one for each microservice.

### Microservices make Understanding harder

Microservices divide the single output stream of a monolith into N output streams, one per service. A frontend request can cause an error in any downstream service (or in several!). Services generate useful error messages, but developers have to check many nooks and crannies for errors.

This was an unsolved problem even before Kubernetes. Companies like Google, Facebook, and Twitter have invested SWE-centuries in build tools like Bazel, Buck, and Pants. But these tools focus on building and running single servers. It’s still up to the user to assemble them into a useful constellation of running processes. The state of the art? Open N terminals, one for each microservice.

Kubernetes made the problem worse. Some issues are fixable bad ergonomics (investigating one service requires multiple `kubectl` calls for logs vs. status). But Kubernetes fundamentally increased the scale of this problem by being so good: when it’s so easy to run many services, teams build more services. Maybe 5 terminals was manageable, but 25 isn’t.

Many developers accept this friction as a cost of debugging. That’s cutting our tools too much slack. Debugging is answering “why did this happen?”, and a computer can’t do that. But microservice developers routinely spend hours each week trying to answer “what happened?” Existing frameworks craft useful error messages that hide among the plethora of microservices. Playing 20 questions with `kubectl` just to find the right message is a waste of developer time.

### A Tool for Understanding

Updating has clear requirements, so tools for Updating resemble each other ([Skaffold](https://skaffold.dev/) is a straightforward upgrade over your custom shell script). A tool for Understanding doesn’t have a clear outline. I propose these principles, derived from the problems described above and centered on the developer’s needs, to guide us:
> See **the** error that’s blocking progress, for as long as it’s blocking progress.
Understand the context and situation of the error.
Explore related data without copying and pasting.

`kubectl` fails these principles, hard: you don’t see errors until you think to look for them. (The right decision for ops leads to a horrible dev experience.) Tools like `skaffold` avoid this failure mode by streaming and multiplexing logs. But one burst of output can scroll the error off your screen before you notice.

These principles are about assuming a new responsibility: making sure the developer sees the right piece of feedback. It’s an impossibly huge mission. (Seemingly simple follow-up questions like “what’s an error? which errors are blocking progress? how can you know an error is fixed?” lead to a never-ending spiral of corner cases.)

### Tilt: Kubernetes Microservice Update+Understand

We’re building Tilt to offer this new take on a developer tool. Its UI reflects the richness of our engine. Tilt is more than `for`-loop around a file watcher like inotify; it watches your filesystem and your cluster, joins the data to create a complete picture of your development, and responds to your commands.

Our 2-minute demo shows off Tilt’s Updating and Understanding abilities:

* birds-eye view of the services that comprise the app

* automatic update on file save

* errors stay pinned in the UI


### A New Kind of Tool for a New Kind of Development

*We built Tilt from the ground up with microservice developers in mind. [Get in touch](https://tilt.dev/contact) if you’d like to try it today.*

![Tilt lets you see your microservice surroundings](/assets/images/microservices-hidden-problem-understanding/featuredImage.png)*Tilt lets you see your microservice surroundings*
