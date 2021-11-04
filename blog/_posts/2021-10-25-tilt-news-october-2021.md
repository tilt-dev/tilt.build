---
slug: "tilt-news-october-2021"
date: 2021-10-25
author: lian
layout: blog
title: "Tilt News, October 2021"
image: "/assets/images/tilt-news-october-2021/pexels-kristina-paukshtite-3095465.jpg"
image_caption: "Bowl of Halloween treats. Photo by Kristina Paukshtite from <a href='https://www.pexels.com/photo/halloween-candies-3095465/'>Pexels</a>"
description: "KubeCon, Blogposts and an exclusive World Premiere! 🎉"
youtubeId: A4IRnU_wXTg
tags:
  - news
---
Howdy Tilters,

I am beyond excited to greet you for the first of what I hope to be many, many newsletters.

My name is Lian, and I've taken up the mantle of Developer Advocacy at Tilt. We will try different ways of community interaction to understand your needs better and get direct feedback for our product. We are aiming for a monthly cadence for this newsletter in which we’ll share exciting news and blog posts from the world of Kubernetes. You’ll also receive updates on upcoming features and other Tilt announcements.

Also, I cannot wait to meet all of you once we're back to in-person events.  
Speaking of...

## KubeCon 2021

We’re still recovering from KubeCon 2021, where we got to speak to Tilt users and friends - face to face! We were also proud to have two Tilters give excellent talks there.

Nick spoke about "[The Control Loop As An Application Development Framework,](https://kccncna2021.sched.com/event/lV1E/the-control-loop-as-an-application-development-framework-nick-santos-tilt)" a topic very dear to our hearts here at Tilt.

L appeared in "[Beyond Kubernetes Security,](https://kccncna2021.sched.com/event/lV4f/beyond-kubernetes-security-ellen-korbes-tilt-tabitha-sable-datadog)" an action-packed thriller featuring all your favorites from the world of Kubernetes and Hacking.

All talks will be made available for free to the public by the organizers, and we will make sure to let you know where to find them!

![The Tilt team, hanging out in our KubeCon booth. From left to right: Nick, Milas, Lizz, Dan, and Surbhi](/assets/images/tilt-news-october-2021/tilt-kubecon.png)
*The Tilt team hanging out in our KubeCon booth. From left to right: Nick, Milas, Lizz, Dan, and Surbhi*

## Remocal Development

We heard a new phrase at KubeCon from InfluxData's Developer experience team: “remocal” dev.

Here's the idea: if you think about dev as local or remote, you misunderstand the world we live in. Modern dev environments are “remocal”—they figure out how your local machine fits into a dev environment with remote components.

We've been thinking more and more about this problem. And experimenting! And writing posts about what we learned, including:

- [Using kubefwd to connect Kubernetes to your local machine](https://blog.tilt.dev/2021/09/09/kubefwd-operator.html)
- [Using ngrok to connect your local machine to a public URL](https://blog.tilt.dev/2021/09/21/ngrok-operator.html)
- [Using Tailscale to connect your laptop to a dev docker](https://blog.tilt.dev/2021/10/11/old-school-remote-dev-clusters.html)

![Tilt UI resource view with custom button that reads 'start ngrok'](/assets/images/tilt-news-october-2021/ngrok.gif)

## The Future of Docker

The Docker licensing changes have kicked off a larger conversation about the place of Docker in local dev environments. Is this the right tool? How can we use it better? Should we be considering alternatives?

We've written some posts to help people think through this:

- [Improving Docker performance](https://blog.tilt.dev/2021/09/13/docker-does-not-mean-slow.html)
- [Switch from Docker Desktop to Rancher Desktop in 5 Minutes](https://blog.tilt.dev/2021/09/07/rancher-desktop.html)

## Kubernetes Cluster API

In other Kubernetes news, Cluster API is now officially production-ready!

Cluster API is a Kubernetes project that enables declarative management for Kubernetes, using APIs to easily create, configure, and update clusters. It is an end-to-end approach that can simplify the repetitive tasks of the Kubernetes lifecycle, while maintaining consistency and repeatability across a unified infrastructure.

They are also the biggest open-source project that uses Tilt. Check out [their developer guide](https://cluster-api.sigs.k8s.io/developer/tilt.html) to see how they are leveraging Tilt for rapid iterative development.

## Tilt News

We were thrilled to see Tilt mentioned in three blogposts:

Kevin Lindsay, Full-Stack Web Developer at Surge and OpenFaaS community member, writes about using Tilt to bring smart rebuilds and live updates to [OpenFaaS functions](https://www.openfaas.com/blog/tilt/).

Archera.ai uses a Machine Learning approach to help optimize the provisioning and management of cloud resources. In this blog post, Jason Burt, Product at Archera.ai explains how they are using Tilt to [accelerate their product feedback loop](https://archera.ai/blog/how-we-used-tilt/).

Evgeny Khabarov, Consultant and Gopher, wrote this [four part series](https://dev.ms/2021/10/envoy-as-an-api-gateway-part-iii/) on building a RESTful API with Envoy. Tilt is featured as the tool of choice for developing on a local Kubernetes cluster with ease. 

### We want to hear from you!

We're always trying to design and improve our product as close to the community's needs as possible. Whether you've been a long-time fan of Tilt or have never used it before, we'd love to invite you for a user-research session. You might be able to catch a glimpse of upcoming features!

A session is typically between 45 and 60 minutes long. You will receive a gift card of around USD 50 (or local currency equivalent) as a thank you.

Sound right up your alley? Then head on over to our [intake form](https://forms.gle/gecjWQ6ErHGfJNm66).

### Exclusive World Premiere
Last but not least, we’re excited to present to you the world premiere of our first How-To video: How to Create Custom UI Buttons! Enjoy!

{% include youtubePlayer.html id=page.youtubeId %}

And that’s all from us for now. Speak to you all again next month!
If you have any questions, comments, or ideas, please join our channel in the [Kubernetes Slack](https://slack.k8s.io/) or message us on [Twitter](https://twitter.com/tilt_dev) or [email](mailto:news@tilt.dev?subject=Tilt%20News%20October%202021) 👋


_Originally sent to [the Tilt News mailing
list](https://tilt.dev/subscribe). View
[in-browser](https://mailchi.mp/tilt.dev/tilt-news-october-2021)._
