---
slug: force-update
date: 2019-11-14
author: maia
layout: blog
title: "Introducing: Force Update"
subtitle: "'Turn it off and on again' the Tilt way"
image: featuredImage.jpg
image_needs_slug: true
image_caption: "From 'The IT Crowd'"
tags:
  - docker
  - kubernetes
  - tilt
  - containers
  - development
keywords:
  - kubernetes
  - dev tools
  - connectivity
  - transient errors
  - docker
  - tilt
---
As a software engineer, the most common advice I give when my family comes to me
with tech problems is: “turn it off and on again.” And indeed, there’s a class of
problems where the solution is really just to try again (perhaps after tweaking a
setting). For instance, while developing, you might run into:
* Connectivity blips/request timeouts (just try again and hope that the network is okay)
* Expired credentials (run a command to re-up the creds, then try again)
* Disk space errors (clear up some disk space---maybe
[prune your docker images](https://blog.tilt.dev/2019/10/28/build-cache-spark-joy.html)?---and try again)
* Your database got into a weird state (blow it away, re-seed it, and try again)

You can probably think of a few problems in this category that you’re used to
running into as you develop, and probably have go-to fixes for them---as discussed,
often a variation of “[run command and] try again”. But what happens when one of
those transient problems causes a Tilt update to fail? Luckily, we have a solution for that.

Now, when you run into these transient problems on Tilt, you have an escape hatch:
we’ve added a “force update” button so you can trigger and re-trigger workflows at
will. Docker build failed because your image pull timed out due to a network blip?
No problem, just rerun it! Service X didn’t come up as expected because it was
missing a dependency? Wait for the dependency to come up, and then re-run the
deploy for Service X.

!["Force update" sidebar button](/assets/images/force-update/trigger-button.png)

Simply click the button in the sidebar to force an update of the resource in
question. If it’s a Docker resource, Tilt will do a full build and deploy
(not a Live Update[^1]---forced updates are a blunt instrument, ensuring the
whole build + deploy gets retried); if it’s a Kubernetes-only resource, Tilt
re-applies the YAML; and if it’s a local resource, Tilt re-executes the command.

## Sounds Neat, What’s Next?

So, now you can rerun workflows with transient failures---great! But we at
Team Tilt think that this new “force update” is good for more than just that.

Use this feature in conjunction with [Local Resource](https://docs.tilt.dev/local_resource.html)
to run common workflows at will: maybe that’s refreshing credentials, or seeding
your database, or _blowing away_ your database… Whatever the command, you can run it
right from the Tilt UI. Moreover, by making all of these common workflows
available from Tilt, you give your teammates insight into what tools they
have at their disposal. We think this brings us one step’s closer to Tilt’s
promise of being a truly [holistic dev environment](https://blog.tilt.dev/2019/09/05/put-down-particle-accelerator.html):
we want you to have all the tools you need for developing your app right
at your fingertips, so that you can stay in flow.

Stay tuned for a blog post digging into Local Resource, how to use it in conjunction with Force Update, and much more. In the meantime, we hope you enjoy!

[^1]: a _forced_ update will always be a full build+deploy; this is distinct from releasing pending changes for a manual update, which may be a Live Update if the resource is so configured.



