---
slug: tilt-v0-9-release
date: 2019-06-21T15:26:34.743Z
author: maia
layout: blog
title: "Tilt v0.9 Release!"
subtitle: "Better Visibility and More Control"
image_needs_slug: true
images:
  - featuredImage.gif
image_type: "contain"
tags:
  - docker
  - kubernetes
  - microservices
  - tilt
  - release-notes
keywords:
  - docker
  - kubernetes
  - microservices
  - tilt
  - release-notes
---
Please give a warm welcome to [Tilt v0.9](https://github.com/windmilleng/tilt/releases/tag/v0.9.0). Here are some of the features in this release that we're most excited about.

![](/assets/images/tilt-v0-9-release/featuredImage.gif)

### Alert Pane (Web UI)
When something goes wrong with your app, you want to know about it right away. The Alerts Pane gathers warnings and alerts, so they don't scroll off-screen in the log view.

![See errors and warnings (and their relevant log lines) gathered in one place](/assets/images/tilt-v0-9-release/alerts-pane.png)
*See errors and warnings (and their relevant log lines) gathered in one place*

### Manual Update Control
When Tilt detects a file change in your project, it automatically updates the relevant resources. Usually, this is great, but sometimes it's better for you to be in control of when resources do and don't update.

Now you can configure some or all of our resources to update manually---i.e., only when you press a button in the UI. For more info, check out [Han Yu's feature announcement](/2019/06/19/new-in-tilt-fine-tune-how-your-services-get-updated.html) or [read the docs](https://docs.tilt.dev/manual_update_control.html).

![The UI for Manual Update Control](/assets/images/tilt-v0-9-release/manual-update.gif)

### Context Filters for your Builds
When you specify a Docker Build, Tilt watches the whole Docker Context, on the assumption that those are the files that affect your Docker Build. Sometimes this assumption misses the mark, and it can be really annoying when changes to an inconsequential file triggers a full Docker Build.

In v0.9, we introduced context filters for your `docker_build` calls; now you can tell Tilt specifically what files to watch (or not watch) when deciding whether it should rebuild your Docker image. Intrigued? Check out [Dan Miller's blogpost](/2019/06/07/better-monorepo-container-builds-with-context-filters.html).

### "Updates Available" Notification
We iterate on Tilt quickly, and it can be a pain for users to keep track of when updates are available. To help, we've put a(n unobtrusive) notification in the Web UI. No more running stale code or missing out on features; know right away when there's a new version to be had!

![Tilt tells you when there are updates available](/assets/images/tilt-v0-9-release/update-nudge.gif)

### Privacy Policy Updates
We know you care about your privacy. We've updated our [Privacy and Telemetry Policy](https://github.com/windmilleng/tilt/#telemetry-and-privacy) to be more explicit about what user data we do and don't collect, and why. (Also, we now ask users to opt in/out of metrics collection further into the onboarding process, so they have more time to evaluate Tilt's value before choosing whether to share their data.)

![Tilt now asks you to opt in/out of analytics later in the onboarding process, via the Web UI](/assets/images/tilt-v0-9-release/analytics-nudge.png)

Already opted into/out of analytics and want to change your mind? In your terminal, run:

```
Tilt analytics opt [in || out]
```

(If you're on the fence, we'd love it if you opted in. Analytics are like census questions: we feel queasy and invasive asking about it, but they're invaluable for helping us prioritize engineering work. We anonymize all metrics to protect your privacy.)

## Where Do I Sign??
Tilt v0.9 is [available on Github](https://github.com/windmilleng/tilt/releases/tag/v0.9.0)! (If this is your first time using Tilt, check out our [installation guide](https://docs.tilt.dev/install.html) to get started.) Download it and let us know what you think: 
* say hi in the [*#tilt* channel](https://kubernetes.slack.com/messages/CESBL84MV/) on k8s slack
* email us at [hi@windmill.engineering](mailto:hi@windmill.engineering)
* if you run into trouble, check the [Github issues](https://github.com/windmilleng/tilt/issues) or file your own

Happy Tilting!
