---
slug: can-microservices-make-things-simpler
date: 2019-02-21T15:49:15.649Z
author: dmiller
layout: blog
canonical_url: "https://medium.com/windmill-engineering/can-microservices-make-things-simpler-f169d540955a"
title: "Can Microservices Make Things Simpler?"
images:
  - featuredImage.png
  - 1*9aBt8gH0RfsBhoyhboBfJg.gif
  - 1*b0Ge745IQ8mMnsf2zchWEw.png
  - 0*hpmaQOdQyFHa7B_2.png
tags:
  - microservices
  - erlang
  - development
  - devops
  - elixir
keywords:
  - microservices
  - erlang
  - development
  - devops
  - elixir
---

When I think about microservices “simple” is not the first word that comes to mind. Quite the opposite, in fact. Microservices have a reputation of increasing complexity, making code sharing difficult and making it hard to develop locally. In the abstract though the idea of microservices seems like it should make a lot of these things simpler not harder. After all, what are microservices except a specific manifestation of a component model?

I have evidence that a well executed component model can simplify software development. Allow me to introduce you to Erlang.

## Hello Mike, Hello Joe

I first encountered Erlang in college through a class called “Language Study”. As a non-CS-major at the time I found it intimidating. The syntax was weird and what little I had learned from Java didn’t apply in the slightest. Classes? Out the window. Print statements? Surprisingly hard.

Erlang encourages a component model in two ways. First it’s easy to create named processes, which are kind of like actors or goroutines. It’s even easy to send messages between them. In fact there’s a built-in operator, `!`, for this. Processes are in turn is used to create higher level constructs called “applications”. Applications can be started and stopped, live reloaded and more. A given Erlang system is often made up of one or more applications. This application pattern is the second way in which Erlang encourages components. Applications can manage (“supervise”) other applications/processes, to ensure that they are always running or handle errors appropriately.

Erlang gives you an easy out of the box way to explore this structure with the observer application. Open it up, navigate to the applications tab and you get this:

![](/assets/images/can-microservices-make-things-simpler/1*-f4YHuXmE_ED-w1Z9_KZZQ.png)

Wow, this tells me a lot! So this “RealWorld” application has some concept of Repos and Endpoints. This repos thing has a pool of processes, and endpoint involve subpub in some way. This is a great jumping off point to learn more about this application.

If Erlang is too esoteric for you take a look at the React.js component model. Coupled with the React DevTools extension it also demonstrates the power of good modularization.

Let’s compare this level of visibility to what I get out of the box with the [Google Cloud Platform microservices demo](https://github.com/GoogleCloudPlatform/microservices-demo).

## Logs Logs Everywhere

Right now the README [recommends](https://github.com/GoogleCloudPlatform/microservices-demo#option-1-running-locally-with-docker-for-desktop) that you use [Skaffold](https://github.com/GoogleContainerTools/skaffold) and run `skaffold dev` to start all the services.

![](/assets/images/can-microservices-make-things-simpler/1*9aBt8gH0RfsBhoyhboBfJg.gif)

Wow, that’s a lot of logs! I can tell that there are a lot of services running but unfortunately it’s hard to say much beyond that as the info logs are drowning everything else out. Did all of my services start correctly? What even are the names of my services? How do they relate?

We can spend some time and read through the code and configs and discover, slowly, that there are eleven services and one data store that they all talk to. But how nice would it have been if this application had presented me with an Erlang-esque view?

![](/assets/images/can-microservices-make-things-simpler/1*b0Ge745IQ8mMnsf2zchWEw.png)

From this image I know that if I want to change the cart behavior, I should probably look at the cart service. The cart service in turn depends on a service called, Redis. It’s safe to say Redis is the backing store here.

This is much better. In fact this looks a lot simpler than any equivalent visualization you could auto generate from a monolithic application. In most languages the best you can hope for is a class dependency graph. That quickly turns ugly and uninformative:

![](/assets/images/can-microservices-make-things-simpler/0*hpmaQOdQyFHa7B_2.png)

What does this thing do? How am I expected to use it? Where do I look if I want to change some behavior?

## Give Me All of the Benefits of Modularization

If I’m going to spend all of this time building an application with microservices I want to get *all *of the benefits of such an architecture, not just some. Alongside technological flexibility and individual scalability I want discoverability, visibility and ease of use. If microservices doesn’t make my app simpler, then what’s the point?

<hr>

*[Tilt](https://tilt.dev) makes it possible to develop all your microservices locally in Kubernetes while collaborating with your team. See a complete view of your system, from building to deploying to logging to crashing. [Give it a try](https://tilt.dev)!*
