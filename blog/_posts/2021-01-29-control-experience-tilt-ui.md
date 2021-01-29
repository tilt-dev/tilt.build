---
slug: "new-tilt-interface"
date: 2021-01-29
author: han
layout: blog
title: "A New Interface for Tilt"
image: "/assets/images/new-tilt-interface/Lukasz-Szmigiel-unsplash.jpg"
image_caption: "Photo by <a href='https://unsplash.com/@szmigieldesign'>Lukasz Szmigiel</a> via Unsplash"
tags:
  - tilt
  - ui
---

As of v0.18.6, Tilt has a new interface. If you haven't already, check it out by toggling "New UI":
![Try the New UI](/assets/images/new-tilt-interface/new-ui.png)

Among other improvements, a new **Overview** helps you understand the status of all your resources at a glance. (The familiar log-browsing layout is still available, under "All Resources.")
![Overview to All Resources](/assets/images/new-tilt-interface/overview-all-resources.gif)


## Why The Change?
Tilt is a shared dashboard for multi-service dev environments. “Shared” means we're trying to serve everyone on your team:

- The person who set up the dashboard and understands how it works
- Everyone else who has to glance at the dashboard and _infer_ how it works

Since last summer, we've been thinking a lot about [the right display](https://blog.tilt.dev/2020/06/19/the-right-display-for-now.html) for Tilt. But everyone has their own "right." 

In hours of interviews with engineers, we learned that not everyone finds logs useful. Maybe you prefer `kubectl` for checking logs, and only use Tilt to monitor and restart services. Or maybe your logs are such a verbose profusion that it's best to ignore them, for now. The Overview reclaims the space devoted to logs, for those situations where you want to see more of your resources at a glance.

We built Tilt to nimbly reflect and respond to the state of your file system, and your multi-service app. We're investing in the interface because we believe Tilt should _also_ reflect and respond to the focus of your attention.

#### Other Features to Note…
Filter Logs to find errors more easily. (Replaces the "Alerts" tab.)
![Resource View - log filtering](/assets/images/new-tilt-interface/resource-view-error.gif)

Tabs help you keep track of the services you're working with. (Ctrl + click on Sidebar items; Command + click on Mac.)
![Resource View - tabs](/assets/images/new-tilt-interface/resource-view-tabs.gif)

The new Log browser is re-written to be fast, even if you have tons of logs.
![Resource View - log speed](/assets/images/new-tilt-interface/resource-view-log-browser.gif)



## What's Next

We want your feedback on this new interface, so we can make it better. We're confident that we've overlooked things! But, we do have some ideas for next steps:

- **Persist interface across Tilt launches** - e.g., If the Resource View with logs is more useful for you, you should always see that first.
- **More log browsing tools** - You should be able to clear logs, zoom, toggle light theme, etc...so even the noisiest logs are easier to read.
- **Custom views for the Overview** - so you can organize resources in a way that makes sense at a glance. Do you want tests to be grouped with services, or in a section of their own? You decide.
- **More Extensibility** - Tilt is your team’s dashboard, so it should support your unique workflows. In that spirit, we're researching and working on making Tilt more extensible. More coming soon! 

Please [let us know](https://docs.tilt.dev/#community) what you think!
