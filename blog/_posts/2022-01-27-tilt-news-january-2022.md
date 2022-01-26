---
slug: "tilt-news-january-2022"
date: 2022-01-27
author: lian
layout: blog
title: "Tilt News, January 2022"
image: "/assets/images/tilt-news-january-2022/pexels-cottonbro-3401897.jpg"
image_caption: "Golden candles shaped to spell 2022. Photo by cottonbro from <a href='https://www.pexels.com/photo/2022-candles-3401897/'>Pexels</a>"
description: "Get your Tilt workflow ready for 2022! 💅"
tags:
  - news
---
Hola Tiltores!

And a Happy New Year! At Tilt, we hit the ground running and have been working tirelessly on exciting new features and improving the onboarding experience. 
Read on to find out more.

## State of Developer Tooling

According to the CNCF’s [State of Cloud Native Development Report](https://www.cncf.io/wp-content/uploads/2021/12/Q1-2021-State-of-Cloud-Native-development-FINAL.pdf), 5.6M developers used Kubernetes in Q1 of 2021 and adoption continues to grow.  
We’ve been seeing more and more tools, best practices and solutions to help developers work with multiple environments on Kubernetes in a standardized way: 
- RedHat, AWS and JetBrains have teamed up to create [Devfiles](https://devfile.io/), “an open standard defining containerized development environments that enables developer tools to simplify and accelerate workflows.”
- A CNCF sandbox project from China, [Nocalhost](https://nocalhost.dev/) is an “open-source IDE plugin for cloud-native applications development”
- James Turnbull, VP Engineering at Sotheby’s, [explores best practices](https://github.com/readme/guides/developer-onboarding) to onboard new developers. Among Skaffold, Garden and Telepresence, he mentions Tilt as tool to manage local workflows 

The space around dev tooling is becoming more crowded and competitive. But, ultimately, we believe that having multiple tools to choose from, is a good thing for the ecosystem as a whole.

## What's New With Tilt?
### Arm Wrestling the Tilt Way
Since Apple released the M1 chip, many users have had issues working with Docker, having to create workarounds to make containers work on their machines. However, production environments are mainly running on Intel architectures.  
Tilt can now detect the target environment and automatically select the correct architecture to build your docker image with. For more information, check out [Nick’s blog post](https://blog.tilt.dev/2022/01/04/arm-wrestling-in-dev.html).

### Optimizing Your Tilt Workflow
If you’re using Tilt, you probably have some kind of deployment manifest for prod that you want to reuse for dev, without having to touch it.  
We now have a guide explaining [how to modify your YAML](https://docs.tilt.dev/templating.html) for dev with Tilt.

#### ... With Helm
If you are already using Helm with Tilt, you might be interested to know that we have enhanced the `helm_resource` function and now recommend its usage over `helm_remote`. Check out the [updated guide](https://docs.tilt.dev/helm.html), and keep your eyes peeled for a blog post on this topic that we’ll release shortly.

#### ... Without a YAML
Maybe you’re just at the beginning of your Kubernetes journey and are still experimenting with resources. In that case, you can use the new [`deployment` extension](https://github.com/tilt-dev/tilt-extensions/tree/master/deployment) to deploy Kubernetes resources without the need of an existing YAML.

#### ... With Many Resources
Avid Tilt docs readers might have already discovered that we have silently released a feature in Beta: [Disabling Resources](https://docs.tilt.dev/disable_resources.html) through the Tilt UI. Now you can stop and delete resources you are currently not working on to keep your feedback loop fast and reactive.

Need to bring them back? Just re-enable them, and they will be brought back to life, just as you are used to!
![Disabling and enabling a specific resource through the Tilt UI](/assets/images/tilt-news-january-2022/disable-resources-small.gif)


### Making Your First (or Second, or Tenth) Time With Tilt Easier
A blank screen can be daunting. Sometimes it’s faster to copy, paste and edit something that already exists.  
From `v0.23.8`, Tilt will offer to generate a starter Tiltfile for you with examples to get you started. 
![Tilt CLI prompting creation of a starter Tiltfile, quick scroll through the generated Tiltfile](/assets/images/tilt-news-january-2022/starter-tiltfile-small.gif)

But even as a veteran Tilt user, you can’t know all the Tiltfile functions by heart, and you shouldn’t have to!

Our new [Tiltfile Snippet Library](https://docs.tilt.dev/snippets.html) will show you best practices and examples for building docker images, deploying helm resources, and more.  
Even better: You can contribute your own snippets. All you need to do is copy and modify an existing snippet [like this one](https://github.com/tilt-dev/tilt.build/blob/master/src/_data/snippets/docker_build_simple.yml) and submit a pull request.
![Snippet Library in the Tilt Docs](/assets/images/tilt-news-january-2022/snippet-library.png)

## Your Feedback Is Needed
Have you tried any of our new features and find that it’s not entirely solving your use case? Are you just getting started with Tilt and are finding it tricky to define your environment in a Tiltfile? Found any weird quirks in the Tilt interface that are irritating you?

[Sign up](https://calendly.com/han-yu/user-research) for a 25-minute session to give feedback or simply share your experience. In return, you’ll receive a small thank you and our eternal gratitude.  
Or, just reply to this email and let us know what you think.



And that's a wrap for the first newsletter of 2022! We’re excited to see what this year will bring, especially hoping that we’ll be able to meet the community again face to face for KubeCon EU in May.

---

If you have any questions, comments, or ideas, please join our channel in the [Kubernetes Slack](https://slack.k8s.io/) or message us on [Twitter](https://twitter.com/tilt_dev) or [email](mailto:news@tilt.dev?subject=Tilt%20News%20January%202022) 👋


_Originally sent to [the Tilt News mailing
list](https://tilt.dev/subscribe). View
[in-browser](https://mailchi.mp/tilt.dev/tilt-news-january-2022)._
