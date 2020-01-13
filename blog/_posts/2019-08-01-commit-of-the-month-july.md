---
slug: july-tilt-commit-of-the-month
date: 2019-08-02
author: maria
layout: blog
title: "Tilt Commit of the Month: July 2019"
subtitle: "No Browser - Flag to Disable the Web UI"
image: featuredImage.png
image_needs_slug: true
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

July’s Commit of the Month gives you more control over your Tilt experience: it’s a command line flag that stops the Tilt web UI from opening automatically on `tilt up`.

Commit: 
* [web: flag for opening browser](https://github.com/windmilleng/tilt/pull/1830)

Though it’s a small quick change, I wanted to highlight this commit as Commit of the Month because it shows how our team responds to our users' input and having this flag improves the user‘s Tilt experience. It alleviates the annoying bit of having a new web UI pop up fresh every time.  


## What does it do?

When you `tilt up`, usually you will see two UIs: the one that shows up on your terminal and one that pops up on your browser. 


Look familiar? 
![Web UI](/assets/images/july-tilt-commit-of-the-month/twoUI.jpg) *UI that pops up on your terminal and the web UI that opens up in your browser*


On startup, Tilt automatically opens up a new tab on your browser displaying our web interface.  We made it this way because the web interface is fairly new and we want people to know about it.

Well now, if you want to stop Tilt from automatically opening a new tab for the web UI, you can `tilt up` along with `--no-browser` like so:
```
tilt up --no-browser
```

## Wait... shouldn't Tilt detect if a tab is already open? 
It totally should!  

Usually, Tilt is smart enough that it detects whether or not you already have Tilt browser tab open. 

But then, one of our fellow Tilters came to us in the [*#Tilt* channel in the K8s slack](https://kubernetes.slack.com/messages/CESBL84MV/) with a use case we hadn’t thought about! 
 
As they mentioned, if you keep the Tilt tab overnight, sometimes browsers like Chrome will decide that said tab isn’t active anymore and will put it to sleep. Since the tab is asleep, Tilt isn’t able to detect that the tab is already open, causing it to open another Tilt tab with the Tilt web UI. 

## But... why do we have two interfaces in the first place? 
This is something we are still trying to figure out as well. The original Tilt was just the terminal UI--your services and their status, with logs for each service available on a keypress. As we progressed through our Tilt journey, we experimented with the web UI, which made it easier to navigate through logs and preview the services.  

Lots of people love the web UI, but then again there are advantages to having a terminal UI as well. For some engineers, it feels more similar to their day-to-day workflows. 

Our next steps will be investigating what it would be like to show users just one UI or the other.

## Let us know your experience using the flag!

Happy Tilting!
