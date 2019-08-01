---
slug: july-tilt-commit-of-the-month
date: 2019-08-01
author: maria
layout: blog
title: "Tilt Commit of the Month: July 2019"
subtitle: "No Browser - Flag to Disable the Web UI"
images:
  - featuredImage.png
image_type: "contain"
tags:
  - docker
  - kubernetes
  - microservices
  - tilt
  - cotm
keywords:
  - web-interface
  - terminal
  - tilt
  - flag 
---


Welcome the second edition of Commit of the Month, a series of blog posts where we highlight some of the work done on Tilt this month! 

This month’s Commit of the Month is the command line flag that disables the webUI:

* [web: flag for opening browser](https://github.com/windmilleng/tilt/pull/1830)

## What does it do?


When you Tilt Up, usually you will see two UIs - the one that shows up on your terminal and the webUI.

This one pops up on your _browser_..
![Web UI](/assets/images/july-tilt-commit-of-the-month/webUI.png) 

And this one pops up on your _terminal_.. 
![Terminal UI](/assets/images/july-tilt-commit-of-the-month/TUI.png)

Look familiar? 

Well now, if you want to disable the web UI, you can now tilt up along with “--no-browser” 
```
tilt up --no-browser
```

## But.. why do we have two interfaces in the first place? 
This is something we are still trying to figure out as well. At first, the terminal UI was the original Tilt - where you can see your services and their status. As we progressed through our Tilt journey, we experimented with building the web UI, which made it easier to navigate through logs and preview the services.  

Then again there are advantages to having a terminal UI. For certain engineers it feels more similar to their day-to-day workflows. 

Our next steps will be investigating what it would be like if you only want to see the web UI and the terminal UI.  

## Let us know your experience using the flag! 

Tilt v9.7 is [available on Github](https://github.com/windmilleng/tilt/releases)! (If this is your first time using Tilt, check out our [installation guide](https://docs.tilt.dev/install.html) to get started.) Download it and let us know what you think: 
* say hi in the [*#tilt* channel](https://kubernetes.slack.com/messages/CESBL84MV/) on k8s slack
* email us at [hi@windmill.engineering](mailto:hi@windmill.engineering)
* if you run into trouble, check the [Github issues](https://github.com/windmilleng/tilt/issues) or file your own

Happy Tilting!
