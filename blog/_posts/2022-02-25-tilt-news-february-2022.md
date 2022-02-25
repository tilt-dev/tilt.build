---
slug: "tilt-news-february-2022"
date: 2022-02-25
author: lian
layout: blog
title: "Tilt News, February 2022"
image: "/assets/images/tilt-news-february-2022/pexels-designecologist-887349.jpg"
image_caption: "A person in the dark, holding a red heartshaped neon light. Photo by Designecologist from <a href='https://www.pexels.com/photo/heart-shaped-red-neon-signage-887349/'>Pexels</a>"
description: "Introducing a long-awaited feature and a little bit of kink 😏"
tags:
  - news
---
Привіт Tilters,

a brief update for a brief month from the Tilt team.


## Tilt Mentions

More and more we are seeing Tilt integrated in a bigger framework of tools and practices, and we are delighted about that!

- AppUiO, a container platform based on RedHat’s OpenShift, recently introduced [a guide](https://docs.appuio.cloud/user/how-to/use-tilt.html) detailing how to use Tilt with their cloud offering. 


- And longtime friend of the project, [Jérôme Petazzoni](https://twitter.com/jpetazzo), included Tilt as the tool of choice to manage developer workflow in his workshop on deploying services to k8s. Go check out [his course](https://www.eventbrite.com/e/deploying-microservices-and-traditional-applications-with-kubernetes-tickets-225546243887)!



## Blog posts

Nick has spent some time to make it easy to spin up short-lived dev environments to showcase Tilt. In his [latest blog post](https://blog.tilt.dev/2022/02/17/preview-environments.html), he explains what he learned working on this, and how that all relates to `kink` 🤭.


One of our most popular blog posts got a revamp! A lot has changed, since Milas first wrote about how to [switch from Docker to Rancher Desktop](https://blog.tilt.dev/2021/09/07/rancher-desktop.html), so we felt it necessary to bring it up to date. A new blog post detailing the pros and cons of each technology is soon to follow. Stay tuned.


## Using Tilt got even better. Whether you're...

### ...starting from scratch
Starting from scratch can be daunting. We want Tilt users to have a pleasant experience, getting their projects up and running quickly and without any hassle. Our recently released [Snippet Library](https://docs.tilt.dev/snippets.html) should help new users browse through a catalog of Best Practices for standard tasks, so they can focus on what’s really important to them.

### ...or handling multiple resources
Most modern applications go beyond the one backend service / one frontend service example. They consist of many microservices, some of which need to run together in some circumstances. So far, you were able to manage this case by using `tilt args`, but many of our users have asked for a more convenient way, and now you finally can!  
With the [Disable resources feature](https://docs.tilt.dev/disable_resources.html), you can simply disable unused resources from the Tilt UI, then enable them at a later point when you’re ready to test the entire suite.
![Disable and enable a single resources through the Tilt UI](/assets/images/tilt-news-february-2022/disable-resource-1.gif)


Cool things you can do now:
- Start tilt with only some resources by running `tilt up my-service`
- Start tilt with all resources disabled by adding `config.clear_enabled_resources()` to Tiltfile
- Disable and enable multiple services at once with bulk disable

![Enable multiple resources grouped together with labels through the Tilt UI](/assets/images/tilt-news-february-2022/disable-resource-2.gif)


## What else is new with Tilt

In January, we donated $900 to [All Star Code](https://allstarcode.org/about/) to help young men of color achieve their dreams through the power of coding.  
We are grateful to work in the tech industry, doing what we love, with people we respect. To extend the same opportunities to more people, we donate $100 per Tilter to an organization working to make tech less toxic and more accessible. You can read more about our donation policy in our [company repo](https://github.com/tilt-dev/company/tree/master/donations).


When people work on the same codebase for a long time, they might develop [inattentional blindness](https://en.wikipedia.org/wiki/Inattentional_blindness). Being too comfortable and familiar with the quirks of an application, might lead to overlooking inconsistencies in the usage of a service. Because of this, outside contributions are invaluable to us. They help us see Tilt from a different perspective that approaches the project from an objective view.  
So, here’s a huge THANK YOU to everyone who contributed, small or big! 💚

---

If you have any questions, comments, or ideas, please join our channel in the [Kubernetes Slack](https://slack.k8s.io/) or message us on [Twitter](https://twitter.com/tilt_dev) or [email](mailto:news@tilt.dev?subject=Tilt%20News%20February%202022) 👋


_Originally sent to [the Tilt News mailing
list](https://tilt.dev/subscribe). View
[in-browser](https://mailchi.mp/tilt.dev/tilt-news-february-2022)._
