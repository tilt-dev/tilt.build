---
slug: tilt-is-the-start-sh-script-of-my-dreams
date: 2018-12-05T23:11:55.828Z
author: nick
layout: blog
title: "Tilt is the `start.sh` Script of my Dreams"
images:
  - 1*Hu6PC-bmdzhrUoaQzUi7hA.png
  - 1*tO_khyEJs281wPBheBPXDQ.png
  - 1*ytSR_5nrIB2TRytHvCiQpg.png
  - 1*PQz8kxs1o-aP4JU-s_3QNQ.png
  - 1*bd7CA1YFEfje6Rd3WiVbXg.png
  - featuredImage.png
tags:
  - docker
  - kubernetes
  - minikube
  - microservices
keywords:
  - docker
  - kubernetes
  - minikube
  - microservices
---
  
I heard Alex Clemmer give a talk at the NYC Kubernetes Meetup a few weeks ago. He started with a slide I loved:

**“Kubernetes competes with Bash”**

I immediately knew what he meant. I used to deploy servers by writing lots of Bash. One Bash script to build the image. Another Bash script to provision a machine. Another Bash to copy the image to the machine. Another to start the process.

Kubernetes takes care of all of that now.

It made me wonder what other stupid things we’re still doing with Bash that should have a more opinionated framework.

### The `start.sh` `script of my nightmares

Every server I’ve worked on has some Bash script, `start.sh`.

It starts simple enough.

![](/assets/images/tilt-is-the-start-sh-script-of-my-dreams/1*Hu6PC-bmdzhrUoaQzUi7hA.png)

Then you add a dependency on a database, then an API server. Of course it’s important to parallelize the builds!

![](/assets/images/tilt-is-the-start-sh-script-of-my-dreams/1*tO_khyEJs281wPBheBPXDQ.png)

Sometimes the backend servers misbehave. You’re sick of wasting time poking at the server without realizing that the database went down in the background. So you add a healthcheck.

![](/assets/images/tilt-is-the-start-sh-script-of-my-dreams/1*ytSR_5nrIB2TRytHvCiQpg.png)

Then the team’s designer runs the server. The script fails. Why? Because they have the wrong version of the Go compiler installed. So you start adding dependency checks for all the things you need.

![](/assets/images/tilt-is-the-start-sh-script-of-my-dreams/1*PQz8kxs1o-aP4JU-s_3QNQ.png)

Now your junior backend engineer starts writing SQL queries. Sometimes they’re malformed. It would be great if we could get some of the Postgres server logs interspersed with the server logs.

![](/assets/images/tilt-is-the-start-sh-script-of-my-dreams/1*bd7CA1YFEfje6Rd3WiVbXg.png)

Congratulations!

You’ve built a miniature process orchestration engine on your local machine!!

And it’s written in a complicated Bash script that only you know how to maintain.

![](/assets/images/tilt-is-the-start-sh-script-of-my-dreams/1*eZeg5hDlvrCIm-Nxg-fItQ.png)

How could we do better next time?

### Why We Built Tilt

One of our major goals when we built [Tilt](https://tilt.build/) was to help write better `start.sh` scripts that scale up as the server configuration gets more complicated.

With Tilt, you develop your microservices locally on a Kubernetes platform like Docker-for-Mac or Minikube. Developers everywhere are using Kubernetes’ thoughtful concepts and APIs for connecting servers together in prod. Now you can use it for local code too.

You write a Tiltfile to tell Tilt how to set up the cluster. No need for complicated Bash scripts to string together inflexible YAML configs. Tiltfiles are written as [Starlark](https://docs.bazel.build/versions/master/skylark/language.html) code, a subset of Python, so that your scripts are more flexible that YAML but easier for your team to maintain than Bash.

And Tilt monitors the full build/run lifecycle of your servers. You can navigate the logs of each server in one UI, rather than tailing and awk-ing a bunch of different log streams together.

If [Tilt](https://tilt.build/) helps you throw your old `start.sh` script away, we will consider it a great success. 😊
