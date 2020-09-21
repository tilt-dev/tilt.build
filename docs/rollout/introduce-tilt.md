---
title: Introduce Tilt with a Tilt Transition Guide
layout: rollout
---
You can have the greatest tool in the world, and it won't mean a thing unless you can show AppDevs how to use it and persuade them that they should care. This article will walk you through our recommended structure for a "Transition Guide", which is a document intended to help AppDevs transition off of their current workflow and to a new tool (in this case, Tilt, but the format can be generalized to any tool).

## What's a "Transition Guide"?

You've probably read many a README for an internal tool, but a transition guide is more than just a README: it's your case to an AppDev that this new workflow is better than their old one.

AppDevs have generally sunk lots of time and effort into their tooling. In our experience, it takes an especially persuasive argument to get an AppDev to switch from a tried-and-true workflow to something new. They need to know not just why the new tool is _good_, but why it's _better than what they're currently using_. 

A good Transition Guide should illustrate the benefits of the new tool vis-a-vis the old tool, and give clear enough setup instructions that an AppDev can experience those benefits within minutes.

Here's our recommended format (we'll dig into each section below):

```
1. You'll Like Tilt More Because...
2. How to Get Started
  2a. How to Install Tilt
  2b. What to Do After You Start Tilt
3. Known Issues
4. What to Do Next
```

Remember that a Transition Guide is more than just a README. Its job is to get an AppDev up and running with minimal friction, but also to drive home why they should be excited about Tilt.

It's also not a design doc or implementation proposal: focus on what makes this tool compelling to a day-to-day developer, not to a DevEx team (e.g. "easy to maintain") or a VP of Eng (e.g. "will boost overall productivity by X%").

### You'll Like Tilt More Because...

Start with why Tilt is better than the current way of doing things. Don't just list features of Tilt: highlight Tilt's benefits as compared to the legacy tool.

This part of the doc can also be a great place to re-contextualize or justify what AppDevs might see as sticking points. For instance, if initial `tilt up` is noticeably slower than launching your old tool, consider a note like:
> You may notice that Tilt is a little slower to start up than $OLDTOOL, but if you stick with it, you'll see that once your app is up and running, _updates_ are 10x faster than on $OLDTOOL.

A Transition Guide is about making your case to an AppDev, so focus on the features that most benefit someone who writes code day-to-day. Instead of leading with attributes like "easier to support users" or "dev is closer to prod." (which are more exciting to those maintaining a tool than those using it), we'd suggest focusing on advantages like being faster, having a better UI, or supporting new workflows.

Remember that screenshots/screen recordings can be great tools to get your point across, and may be particularly good for comparing Tilt to the legacy tool. (If your team uses Tilt Cloud, you can also use [Snapshots](../snapshots) to let potential users interact with the UI before installing Tilt.)

### How To Get Started

#### How to Install Tilt
Describe how to install Tilt and any of its dependencies. The more streamlined an AppDev's experience with Tilt, the better, so call out any known gotchas here: e.g. if you're a Ruby shop and expect a lot of devs to run into [this error](https://docs.tilt.dev/faq.html#q-when-i-run-tilt-version-i-see-template-engine-not-found-for-version-what-do-i-do) because of a name conflict with a Ruby gem, note it in your guide instead of making the AppDev Google a lot of error messages.

#### What To Do After You Start Tilt
An example workflow can help AppDevs get a feel for Tilt, and allow you to call attention to the places that Tilt shines. Consider providing an example workflow like:
* Start Tilt (probably running `tilt up` in some directory in a repo)
* Access the running app (by curling an endpoint or clicking the URL surfaced in the Web UI) and see that it's working
* Change a file (for extra credit give an example file and line to change)
* See Tilt perform the update and then see the change live
* Optionally: suggest a file and line at which to introduce an error; see the app crash and see Tilt report the error.

An example workflow makes it easy for a user to map Tilt onto their existing mental model of the dev workflow. It's also a great way to drive home the advantages of Tilt over your old tool. For instance, if resetting the database used to require an elaborate terminal incantation and can now be done by simply triggering a [`local_resource`](../local_resource) from the Web UI, make that part of your example workflow. (If you had a group of [Focus Users](../rollout/focus) alpha-testing your Tilt setup, the features they were most excited about will generally be good ones to mention here.)

### Known Issues

As you first build out Tilt support, there will probably be ways that Tilt is worse than the legacy tool---or even just different. Telling users about these regressions before they run into them builds trust. Something as simple as a list of links to issues in your issue tracker helps manage users' expectations. (As noted above, many perceived "regressions" stem from misconceptions about how Tilt works, or are necessary trade-offs for big benefits down the road: explaining this context can help your users feel less annoyed.)

### Next Steps

Tell users how to give feedback and get support (by joining a Slack channel, subscribing to an email list, etc.). If you're looking for volunteers to help improve the Tilt experience, mention that here.

Your goal in this section should be to catch underwhelmed users before they give up entirely---it's better to get their feedback now than to hunt them down later as [inactive users](../rollout/prioritize-inactive). The easier (or more mandatory) you make it for AppDevs to give you feedback, the greater the chance an underwhelmed AppDev will come give you useful information (rather than giving up and walking away).

## The Transition Guide is Temporary

A transition guide is meant to help AppDevs get over the hump of switching tools. This makes it different than your average README or new hire onboarding doc, though they can share a lot of content. Telling people _why_ to use a tool takes a bit more effort than just telling them _how_, but it's hugely helpful in overcoming the inertia of an existing workflow. When your Tilt rollout is wildly successful, you can deprecate this document in favor of a more straight-forward README.

## Evaluation

**Use this if**
* You have promising feedback from [Focus Users](../rollout/focus) and are ready to start rolling Tilt out to a broader audience of AppDevs (who may or may not understand or care about this new tool).
* AppDevs are entrenched in their current tooling/workflow(s), but you think they'd have a better experience with Tilt.

**Skip this if**
* You're still evaluating Tilt and want to share it with a collaborator who will learn Tilt for themselves. This advice is for when you have users you want to use Tilt without having to study it themselves.
* AppDev doesn't have an existing workflow. (e.g. it's a new project that's used Tilt since you started it).

**You know it's successful when** an AppDev can go from hearing about Tilt to using it to develop in a half-hour using just the guide, and understand why Tilt is relevant to them.
