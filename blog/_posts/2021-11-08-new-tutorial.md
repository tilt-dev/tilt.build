---
slug: "new-tutorial"
date: 2021-11-08
author: lian
layout: blog
title: "Welcome to Tilt: Revamped!"
image: "/assets/images/new-tutorial/pexels-harry-cunningham-harrydigital-3405489.jpg"
image_caption: "Brown and red windmills in front of blue sky. Photo by Harry Cunningham @harry.digital from <a href='https://www.pexels.com/photo/brown-and-red-wind-mill-3405489/'>Pexels</a>"
description: "making old things new"
tags:
  - tutorial
  - tilt
  - devx
---
Hallo Tilters,

Big announcement incoming: we have redesigned the Tilt onboarding experience! 🥳  
Most of you who are reading this are probably already acquainted with Tilt — and don’t worry, we’ve got something coming for you, too, but today we are focusing on onboarding.

As one can only make one first impression, it better count, right? With that in mind, we wanted to create an onboarding experience that is quick, easy and fun, even if a user is starting from zero. (So yes, if you've been looking for the perfect way to introduce Tilt to your colleagues, this is it!)

## Docs!
If you've been a Tilter for some time, you probably already noticed that our docs have received a makeover.  
We want you to have the best possible experience with Tilt, getting started quickly and continue to work with Tilt autonomously. But that can be tricky when everyone has very unique requirements. So, we're always adding more docs to address a wide variety of use cases.  
We updated the navigation so it'll be easier to find what you're looking for — whether you're just getting started, figuring out how to optimize your update times, or looking to extend Tilt's functionality!

![New Tilt docs startpage](/assets/images/new-tutorial/docs.png)

## Tutorial!

So we went out and collected, considered, and reflected on the feedback you all provided (thanks again for that!), and overhauled the entire thing!  
The new tutorial helps you to get Tilt up and running with just one command, so you can quickly tour Tilt’s best features, and learn about all the possibilities to boost your developer workflow.  
All you need to get started is Docker, Tilt and the sample source code (maybe; see below). You’ll be able to play around with an actual microservice application and see Tilt in action. [Try it out yourself](https://docs.tilt.dev/tutorial/index.html) and let us know what you think!

If you already know all of this and just want to learn how to write your own Tiltfile yourself, the [old tutorial](https://docs.tilt.dev/tiltfile_authoring.html) is still up.

![Screenshot of the new Tilt docs showing the Tutorial overview](/assets/images/new-tutorial/docs-tutorial.png)

## And one more thing

Still reading? Excellent!  
One issue that often gets in the way of showing Tilt to one's colleagues is the non-Tilt parts of the setup e.g. setting up a Kubernetes cluster isn't for the faint of heart.
To help you with that, we’ve created a self-contained demo. Just install Docker and Tilt, then run `tilt demo` and Tilt will spin up an entire dev cluster for you with our sample application. From scratch!

![Tilt demo, from running tilt demo to spinning up the entire web service](/assets/images/new-tutorial/tilt-demo.gif)


Do you have any onboarding-related issues we haven’t addressed yet? Let us know!