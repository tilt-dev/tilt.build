---
slug: tilt-a-better-ux-for-docker-compose
date: 2019-01-16T17:18:00.294Z
author: maia
layout: blog
canonical_url: "https://medium.com/windmill-engineering/tilt-a-better-ux-for-docker-compose-52e80d0625d0"
title: "Tilt&#58; a Better UX for Docker Compose"
image_needs_slug: true
images:
  - featuredImage.png
tags:
  - docker
  - docker-compose
  - developer-tools
  - microservices
  - containers
keywords:
  - docker
  - docker-compose
  - developer-tools
  - microservices
  - containers
---

We’ve done a lot of demos of Tilt in the past few months.

Sometimes, people’s eyes light up and they say, “That’s exactly the tool I’ve been looking for! Now I can develop against all of my microservices at once, see exactly what’s going on with each of them, and have my local changes propagate up in seconds!”

And sometimes they say, “Oh man, I’d love all that visibility into my microservices, but I’m already using Docker Compose and I don’t want to write a whole new config file.”

Well if that’s you, we’ve got great news: **Tilt now supports `docker-compose.yml` files!** That means that you can get the slick experience of Tilt even if you’re not on Kubernetes (…yet). There’s no need to even write any new configs[¹](#6f43); just tell Tilt where to find your `docker-compose.yml`, and we’ll take care of the rest.

```
$ echo 'docker_compose("/path/to/docker-compose.yml")' > Tiltfile
$ tilt up
```


## Why Not Stick With Docker Compose?

If you’re used to a tool — say, Docker Compose — it can seem pretty unappealing to learn a new one. Why switch to Tilt when what you’ve got works just fine already?

Well, you’re hardly switching, since Tilt calls out to Docker Compose under the hood. It’s still Docker Compose running all your services, but Tilt adds some extra features that we think make your microservice development even easier.

In particular, Tilt via Docker Compose strives to make your experience fast, live, and transparent.

### Tilt x Docker Compose is *TRANSPARENT*

With Tilt, you can see the state of all your services at a glance. Why deal with something ugly and uninformative like `watch -d docker-compose ps` when there’s a better option? Tilt tells you right away whether your services are red, green, or pending; and when something goes wrong, we automatically surface the error message to you.

Speaking of logs, Tilt lets you summon and dismiss per-service logs with a single keystroke; we think it’s *much* nicer than digging through log barf of all of your services, or tracking ten different log tails.

![This is no way to live.](/assets/images/tilt-a-better-ux-for-docker-compose/featuredImage.png)*This is no way to live.*

### Tilt x Docker Compose is LIVE

How many times have you run `docker-compose stop && docker-compose up --build`? With Tilt, you’ll never have to again. Tilt knows which files will affect your Docker image, and when you edit one, Tilt auto-rebuilds your service for you. You don’t need to hunt through your terminal history for the right commands; you get to focus on writing code, and Tilt does the rest.

### Tilt x Docker Compose is FAST

If the point above made you cringe because your Docker build is *just too slow*, don’t worry, we’re here to help. We have some [optimizations up our sleeve](https://blog.tilt.dev/2018/08/28/how-tilt-updates-kubernetes-in-seconds-not-minutes.html) that will make your behemoth of a Docker build fast enough to actually incorporate into your dev flow. Man, being able to write a line of code and spin it up to check if everything works, because it’ll only take seconds — imagine that!

*(Note: this feature is still in development; check back in a week or so for the lightning-fast build of your dreams.)*

## Where Do I Sign??

Want to get started? [Check out our docs](https://docs.tilt.build/docker_compose.html).

We’re still hard at work on Docker Compose support, adding and refining features to make the experience even better and more customizable. We welcome your feedback: come say hi in [`#tilt` on the Kubernetes Slack](https://kubernetes.slack.com/messages/CESBL84MV/), or [file a GitHub issue](https://github.com/windmilleng/tilt/issues) if you run into any problems. Until then: happy Composing!

<hr>

1: though we think that it’s pretty easy to write a `Tiltfile`. [Our docs](https://docs.tilt.build/first_config.html) are comprehensive, and we hope that writing your configs in *code* (and not just an endless pile of YAML) feels more familiar and comfortable for you.
