---
slug: whats-wrong-with-microservice-dev
date: 2019-02-07T17:14:29.873Z
author: maia
layout: blog
canonical_url: "https://medium.com/windmill-engineering/whats-wrong-with-microservice-dev-1bb424d2e14e"
title: "What’s Wrong With Microservice Dev?"
image_needs_slug: true
images:
  - 1_2ecTbOses842YP2DyKEziA.png
  - 1_bmz5fPs8hRMjYgVSaHxAEA.png
  - 1_9nlX5cxWOPxi4XztMbc9bA.png
  - featuredImage.png
  - 1_40IXe2qBuWw8_LpUZvbFZg.png
tags:
  - microservices
  - development
  - software-development
  - workflow
  - devtools
keywords:
  - microservices
  - development
  - software-development
  - workflow
  - devtools
---

Here at Windmill, we talk a lot about how much it sucks to develop on microservices. If you haven’t experienced this pain firsthand, or if you’ve never known anything better, you might wonder what we’re going on about.

Well, wonder no more! Here’s a quick overview of a few different development cycles, how microservice dev stacks up (spoiler: not well), and how developing with [Tilt](http://tilt.build/) makes it suck less.

### The Core Dev Workflow

The basic loop of development is the same no matter what sort of service(s) you’re working on:

![](/assets/images/whats-wrong-with-microservice-dev/1_2ecTbOses842YP2DyKEziA.png)

1. edit some code

1. make your change go

1. see the effects of your change

1. based on #3, go make another change

The interesting work of development is in the top left corner of the diagram above (steps #3 & #4): looking at the results of your change and figuring out which bit of code to tweak next. All the stuff in between is just filler, and we want to get it over with as soon as possible.

That’s where your dev tools come in — they streamline the slow, boring bits of coding so that you can do the fun stuff. In an ideal world, development is:

1. **responsive** (you don’t need to do a bunch of elaborate steps to make your code change propagate);

1. **fast **(because nothing kills flow like waiting around for your server to reload); and

1. **transparent **(to know what code to write next, you need to be able to easily see the effects of your last change).

As you can imagine, the details look pretty different depending on the type of development you’re doing. Here are some common workflows by type of development.

### Front-End Dev

![](/assets/images/whats-wrong-with-microservice-dev/1_bmz5fPs8hRMjYgVSaHxAEA.png)

For most front-end devs, life goes like this: you write a line of code, hot-reload magic happens almost instantly, and you can see the results of your change in your browser, which tells you what code you need to change next. Lather, rinse, and repeat!

This is the gold standard of dev workflows. It’s **responsive** — your code propagates automatically. It’s **fast** — compilation and propagation usually takes only a few seconds. And it’s **transparent** — it’s really obvious where you have to look to get feedback about the code you just wrote, cuz it’s all right there in the browser.

All in all, front-end devs have it pretty good. (Don’t get me wrong, front-end devs have *plenty* to be getting on with — but thankfully, their dev workflow doesn’t get in their way.) But what happens when you’re writing backend code?

### Backend Monolith Dev

![](/assets/images/whats-wrong-with-microservice-dev/1_9nlX5cxWOPxi4XztMbc9bA.png)

The development loop takes a little longer when you’re working on a monolithic backend app. You write some code, and need to manually do something to make it go; run a command or restart a script, say. Then the code compiles/the script runs (often slower for backend code than for frontend code), and you need to piece together what’s going on by looking at a combination of app behavior and logs. Luckily, if you’re developing a monolith, you can expect the logs to be in one place.

Is it **responsive**? Often not; you have to manually restart your script or process, though certainly there are hacks around this. Is it **fast**? Ehhh; you’re probably waiting around a bit for code to compile and servers to start, but it’s not the longest wait in the world. It *is* **transparent**, though: you can see what’s going on by poking around the app and looking at the logs. So that’s something, at least.

Finally, our feature presentation: how does microservice dev compare to all this?

### Microservice Dev

![](/assets/images/whats-wrong-with-microservice-dev/1_9r-gJy5fuJbHGYLOGR9wMA.png)

Say you’re making a code change that spans multiple services; that means that you need to go restart all those services, and wait for them all to compile/spin up, and then you look at the app and the logs, but you have a million panes of logs to sift through because you’re running so many services, and why isn’t the thing working, oh whoops you forgot to restart one of the services, and then you have to find its log among a million logs, and only you *then *can figure out what’s going on and make your next code change.

Is it **responsive**? Nope: you’re probably restarting services by hand — and you have to remember which ones to restart, so there’s a whole human error component introduced.

Is it **fast**? Nope: you’re waiting for any compilation or server start-up, multiplied by how many services you have, plus the time lost to above-mentioned human error (“Oh shoot, I forgot to restart service X”).

Is it **transparent**? Heck no — you’re drowning in a sea of log panes. Often, a service will break without you even knowing it, leading to many minutes lost digging through the wrong logs before you finally figure out what’s up.

So basically, microservice dev comes in dead last as far as ease of development. There are tools out there that alleviate some of this pain, or you can roll your own, but the result is that developers end up crouched in a rickety lean-to of custom tooling that’s brittle, hard to maintain, and even harder to explain to new devs.

Luckily, we’ve got a solution, and that solution is [*Tilt](https://tilt.build/)*, the new tool for microservice development. Let’s look at how it changes your workflow.

### Developing Microservices with Tilt

![](/assets/images/whats-wrong-with-microservice-dev/1_40IXe2qBuWw8_LpUZvbFZg.png)

As you can see, this flow looks a lot more similar to front-end development than to microservice development. To use Tilt, you connect your existing configs with a bit of glue code called a Tiltfile (written in a dialect of Python), and then `tilt up` and go!

Developing with Tilt is **responsive**: Tilt knows via your config file which files affect which services, so when you make a code change, Tilt just restarts the right servers for you; no more manual script-jiggering.

It’s also **fast**: Tilt uses container magic under the hood to speed up build and deploy. If you’re curious, you can [read more here](https://medium.com/windmill-engineering/how-tilt-updates-kubernetes-in-seconds-not-minutes-28ddffe2d79f), Tl/dr: your services will be up and running in seconds.

Finally, Tilt is **transparent**: we’ve replaced that forest of log panes with a single Heads-Up Display that shows you the status of all of your services at a glance, lets you easily see logs for particular service, and auto-surfaces errors when things are broken.

In sum, we think that Tilt checks all the boxes of the ideal dev workflow, leaving engineers free to do the work that actually matters. Need a last-minute Valentines Day gift for the struggling microservice dev in your life? Send them [Tilt](http://tilt.build/) today!
