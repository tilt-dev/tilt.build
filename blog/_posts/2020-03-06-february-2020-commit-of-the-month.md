---
slug: february-2020-commit-of-the-month
date: 2020-03-06
author: maia
layout: blog
title: "It's 10PM; Do You Know Where YOUR Progress Meter Is?"
subtitle: "Commit(s) of the Month(s): Docker Push & Pull Progress"
image: /assets/images/february-2020-commit-of-the-month/featuredImage.jpg
image_caption: "Photo by Dylan (newchaos) on <a href='https://www.flickr.com/photos/newchaos/411409012/in/photolist-CmzyQ-F61dsG-6F3spX-mbzo9P-4zUE6i-4sNtuF-2d5kfHa-gvc6SZ-8Jms3t-Pn8o5D-7qbih-fsMbTJ-7oi3xg-ekgkNn-8HbgUT-6v43xq-7JBbWG-haQasf-du5kXV-81eEex-7Jxg16-2zc92-5KF6Zw-5KASgB-7Mc9cm-akYWET-8CTya-k1bGyi-98qSsb-4B7y9i-4B7y9Z-8CTQZ-a12btq-8CTN3-5xUp5h-efQEZt-bpA9kC-s5hAvG-cdD8Bh-99hp5v-8CTvj-8CTMB-hAJuZS-8CTKw-8CTQu-7EHjNt-77vUt2-8CTEC-8CTrQ-8CTpu'>Flickr</a>."
image_type: "contain"
tags:
  - docker
  - tilt
  - cotm
keywords:
  - tilt
  - docker pull
  - docker push
  - transparency
  - visibility
---
This post discusses two exciting commits (one of which is technically from January 🤐) which are two sides of the same coin: [e77be9fe](https://github.com/windmilleng/tilt/commit/e77be9fe2d97f5893ea99f131a1ef2ffdb4ec576) and [467f1913](https://github.com/windmilleng/tilt/commit/467f1913ea08b562e2e16b26d8d7e458b92c941b) print `docker push` and `docker pull` progress (respectively) to the Web UI, so you're not in the dark about where your deployment time is going.

Tilt tries to make microservice development as fast as possible, but sometimes there's just stuff you've gotta wait around for. However, when you inevitably have to wait around for something, you should know exactly what you're waiting for and how it's progressing (and that your process isn't just permanently hung somewhere).

These commits print `docker push / pull` progress output, updating lines in the Web UI in place as status meters creep forward. Users now have real-time visibility into what Docker is doing, instead of staring at a blank screen and hoping things are still working.

![See docker push status in real time](/assets/images/february-2020-commit-of-the-month/push-output.gif)

To write these features, the Tilt team dug deep into the Docker CLI, and we were really impressed with what we found there. We've all felt the frustration of a command-line tool that sits their churning with no output. What is it doing? Will it ever finish?

A good command-line tool at least gives you a simple progressbar or loading animation.

The Docker CLI goes way beyond that. It updates your terminal in-place with how big your layers are, whether they were cached, how much time each one is taking. It's responsive to your terminal width, summarizing the information differently depending on how much screen real estate it has to work with.

We wanted our web UI to do that progress display justice, so there was really only one way forward: updating Web UI log lines in place to show progress with as much liveness as possible. As a bonus, we can use this new functionality (the ability to update log lines) to show all sorts of information, all in service of improved visibility into what Tilt is doing at any given time. We've already used it to, e.g., monitor pod rollout for resources:

![Pod rollout status updating in real time](/assets/images/february-2020-commit-of-the-month/pod-rollout.gif)

We hope you enjoy the newer, more transparent Tilt---thanks [**@nicks**](https://github.com/nicks) and [**@hyu**](https://github.com/hyu)! Comments, questions, feature requests? [Let us know](https://tilt.dev/contact)!
