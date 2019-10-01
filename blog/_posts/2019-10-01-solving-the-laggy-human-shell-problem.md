---
slug: solving-the-laggy-human-shell-problem
date: 2019-10-01
author: dmiller
layout: blog
title: "Solving the Laggy Human Shell Problem"
image: ships_pass.png
image_caption: "Two ships pass in the middle of the night"
tags:
  - kubernetes
  - developer-tools
  - snapshot
keywords:
  - kubernetes
  - developer-tools
---

Dan opens his laptop and orients himself after his last meeting of the day. He knows that today he needs to make his first ever change to the shopping cart service to add support for the feature that his team is working on. Step one will be getting a dev environment set up so that he can make changes locally.

Dan hits an endpoint test the cart service but it returns a 500. Looking at the logs it appears to be related to the database connection.

```
com.sun.jersey.spi.container.ContainerResponse mapMappableContainerException
SEVERE: The RuntimeException could not be mapped to a response, re-throwing to the HTTP container
org.hibernate.exception.JDBCConnectionException: Cannot open connection
```
Hmm. Dan is unfamiliar with Java and has no idea what Hibernate is.  Dan would love to dig in to the architecture of this service but his project is on a tight deadline. Surely someone on the cart team knows the answer.

![Dan asks a question about the java error](/assets/images/solving-the-laggy-human-shell-problem/1.png)

Dan waits for an answer. And waits… and waits…

Then he realizes: the cart team is based out of the New York office, and it’s 3:30 PM in San Francisco but 6:30 PM on the east coast. He’ll have to until tomorrow to get an answer to his question.

**The next day, in New York City**

Han sits down at their desk and notices an unread message in their team’s Slack channel. It’s Dan asking about some trouble he's having with the cart service. Han immediately asks a question to help narrow down the problem:

![Han asks: is the database running?](/assets/images/solving-the-laggy-human-shell-problem/is_running.png)

But, of course, Dan is in San Francisco and won’t get this message for a couple hours. It’s 9:30 AM in New York, but 6:30 AM in San Francisco. Han context switches to something else.

**Later that day, in San Francisco, Dan comes online**

![Lots of back and forth between Dan and Han](/assets/images/solving-the-laggy-human-shell-problem/all_told.png)

After lots of back and forth and a few misaligned lunch breaks Dan gets a solution thanks to Han's help. All told, it took Dan 24 hours to get an answer to his question.

## The Laggy Human Shell
Does this story sound familiar? I call it the Laggy Human Shell problem: when two coworkers are communicating over text and asking each other to run commands, but keep missing each other, like ships passing in the night, with a 20 minute - 24 hour turnaround time.

To solve this problem, we built snapshots. Snapshots allow you to send a link to someone with a frozen “moment-in-time” version of the Tilt UI. In a snapshot you can drill in to specific services, see alerts, Kubernetes events, and everything else you can see in the Tilt UI!

With snapshots, Dan and Han's lagging human shell sessions would have looked like this:

![A snapshot link simplifies Dan and Han's conversation](/assets/images/solving-the-laggy-human-shell-problem/with_snapshots.png)

Since Tilt knows the entire state of your Kubernetes cluster, with tons of information relevant to your app contained within it, sending someone a Tilt snapshot allows them to quickly investigate things, rather than wait on a human who might be out to lunch for answers.

Can’t wait to enhance your productivity with snapshots? If you have the latest version of Tilt installed you can get started today! For more information, check out the snapshots documentation.
