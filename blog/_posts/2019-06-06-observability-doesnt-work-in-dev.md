---
slug: observability-doesnt-work-in-dev
date: 2019-06-06T14:43:58.636Z
author: dmiller
layout: blog
canonical_url: "https://medium.com/windmill-engineering/observability-doesnt-work-in-dev-c214a9fb3e2d"
title: "Observability Doesn’t Work in Dev"
image: featuredImage.png
image_needs_slug: true
image_caption: Spot the bug
tags:
  - microservices
  - software-development
  - observability
  - devops
  - local-development
keywords:
  - microservices
  - software-development
  - observability
  - devops
  - local-development
---

A couple of years ago, diagnosing a problem in production would involve poring over log messages to produce an image in your head of what was happening. It felt like playing the world’s worst designed murder mystery game.

Now we have a slew of complementary tools that, when used in conjunction, make debugging and understanding production systems way easier. Instead of looking at static graphs and hunting around for suspicious looking logs I can notice a systemic problem in Datadog then dive in to specific examples with Honeycomb. As a new hire I can look at traces in Lightstep for all of the requests I’m making and get a high-level overview of the system. It has never been easier to understand our production systems.

Yet, when I talk to engineers and ask them if they have those same tools available to them in dev the answer is often no. This is very frustrating: dev should be simpler than prod! I can sample problematic request traces from millions of requests in prod, but can’t get traces for the 100 or so requests I make in a given day in dev? Why do we not use these great tools in dev? I think there are two answers.

### Dev is not necessarily a cluster

One reason we don’t use these production observability tools in dev is that dev does not resemble prod very closely. It could be that prod runs on ECS, and you start things manually on your laptop for dev. Or you might be using Kubernetes in prod but Docker Compose in dev. If everything runs on your laptop where does your tracing service live? Is that a shared service that all devs use? If so, how do they connect to it, who operates and maintains it? If instead it runs on your laptop then what starts it? Where do the traces get stored?

You might be tempted to solve some of these problems by treating developer machines like prod and provisioning them with something like Chef. But what if developers are using macOS, gentoo and Arch Linux? That’s going to make chef recipes a lot more complicated. We keep running into the problem that, whether it’s Zipkin or Chef, these tools are just not designed to be run on individual developer’s machines.

Say you did manage to have all of your services running locally, replete with stuff like ELK, Chef and Docker. Now you’re running into another problem: resource exhaustion. ELK is not designed to be run on your laptop and your laptop isn’t designed to be running dozens of services. One local request to your dev environment can generate a ton of work, and more work means less battery life. When this happens to me I’m tempted to throw it all out and just work on one service with grep as my log analyzer. Now dev is even more different from prod.

So then the logical thing to do is give every developer their own cloud cluster. Then I can run all of our prod observability tools against it while saving my lap from overheating hardware. Right?

### Dev clusters have different requirements from prod, and one another

Not so fast: now I have different problems! If I was using LightStep on-prem in prod, how should our team set this up in dev? Should all the dev clusters point to a shared LightStep install? How will I differentiate my data from someone else’s, with the code constantly changing? If I use the prod installation then I have the same problem: how can I make sure that I don’t accidentally look at a dev trace when trying to diagnose a problem in prod?

A few months ago, [LightStep announced Developer Mode](https://lightstep.com/blog/announcing-developer-mode/) to address this need. We’re watching it closely. As it evolves, which parts of the dev tracing experience will stay aligned with prod, and which parts will diverge?

Plus there are the classic problems with remote development: jumping through networking hoops to use YourKit with a remote JVM, or connecting an IDE to a remote filesystem so you can edit files in the IDE and have them quickly appear in a remote server. These things are tricky to get set up, and can be flakey when things in your environment change.

So where does that leave me? Can I have my observability cake and eat a simple, grokkable responsive local dev environment too?

## The Fact is: Local Dev is a Different Thing

Local development is sufficiently different from prod to require different kinds of tools. Good local development tools adhere to three principles.

### One-stop shop

Production tools seemingly adhere to the first principle of the Unix Philosophy:

*Write programs that do one thing and do it well.*

For example, like I mentioned above: I use Datadog for graphs, Lightstep for traces, Honeycomb for digging in, etc.

Prod is operated by multiple teams with multiple concerns and workflows, so it’s natural there are multiple tools. In dev, I’m the only admin, and I’d rather not be doing it. I don’t want to manage dozens of services locally to get observability. I can’t afford to be slowed down by the siloing. I’d rather have one tool that makes it easy to do common tasks: I should be able to start my debugging in one window. Some problems may be so unique or special that I end up going to other tools to resolve them, but I can’t be having to tab through twelve windows just to check for one problem.

If there’s a problem in dev, I should switch to one window and know that I can start my debugging there.

### Record everything, retain little

In prod I have two competing priorities: I want to record everything and retain it for as long as possible, but I also want to control costs. Sometimes this means sacrificing how much I’m recording so that I can retain things longer and cheaper. My priorities are different in dev: I want to record everything, full stop. After all it’s just my laptop and I’m the only user so it’s not that much data. But I want to *retain* as little of it as possible. While hard drives are cheap, hard drive space can be limited on a laptop and it’s annoying to expand.

Imagine this: you make a request and you get a 500 response code back. Today you might turn on your tracer, adding logging statements, reissue the request and hope that it reproduces reliably. Instead wouldn’t it be amazing if the last request you made locally is always traced and that trace is always persisted? Then whenever this happens you can pull up the last trace and immediately see where to look next.

Every time I do something in dev I should be able to see *everything* that happened with 100% fidelity.

### Shareable

Shareability is a concept local dev tools should steal from production. Many production tools allow you to create a link to a log search, dashboard or request trace and send them to people. It’s so useful for debugging, especially in a remote/distributed environment! If I’m connected to the network my local dev tools should let us do the same thing. I want to include a snapshot of my current state when I ask a teammate for help.

Every time I do something in dev I should be able to quickly share the result with a colleague.

## Let’s Take Local Development Seriously

Why does observability suck in dev? We can’t lift and shift our production tools in to dev and expect it to work. These tools are great for finding the needle in a haystack. But in dev there’s just 4 needles, and you want to see them all. So what do we do?

Let’s start treating local development as seriously as we do production debugging. Local development is a unique, challenging environment that requires specialized tooling. It’s an environment that we as engineers spend a lot of time working in.

It’s time the state of the art advanced beyond `grep` and `ps`. It’s time for specialized local development tools.

---

*For our first take on a specialized local development tool, check out [Tilt](https://tilt.dev/)! Tilt manages local development instances for teams that deploy to Kubernetes. Get started easily, get more done, and never play twenty questions with `kubectl` ever again.*

---

### Correction: June 20, 2019

An earlier version of this post had some incorrect statements about pricing for observability services. We also weren’t aware of LightStep’s new dev mode, which looks cool, so we added a link to it.
