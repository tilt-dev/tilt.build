---
title: Tilt Transition Guide
layout: rollout
---

Write a transition guide that will make an AppDev excited to try Tilt and able to see benefit in minutes.

* you'll like Tilt more because...
* how to get started
  * what to do after you start Tilt
* advanced features
* known issues
* what to do next

If you have existing docs, it's worth tailoring it to this audience. For example, a design doc might cover much of the same material but it's meant to discuss implementation trade-offs. The goal of a transition guide is that a single link will let an AppDev get started.


## You'll Like Tilt More Because...

Start with why Tilt is better, and focus on why it's better for the AppDev right now. A piece of perspective: some Tilt benefits are more exciting to the DevEx who have to support the tooling than to the AppDevs using it. Instead of leading with attributes like "easier to maintain" or "closer to prod", we'd suggest focusing on advantages like being faster, having a better UI, or supporting new workflows.

Highlight benefits of Tilt for your project compared to the legacy tool. Don't just list features of Tilt: some may not be new compared to the legacy tool and some you may not use yet.

Include a screenshot to make it easy to understand the difference. (If your team uses Tilt Cloud, you can also use Snapshots to let potential users interact with the UI before installing Tilt).

## How To Get Started

Describe how to install Tilt and any prereqs you need.

### What To Do After You Start Tilt
It's useful after you say how to start Tilt to give a simple example workflow that shows off getting quick feedback with Tilt. For example:
* Start Tilt (probably running `tilt up` in some directory in a repo)
* Access the running app and see it looks good(maybe in a web browser or as an API)
* Change a file (for extra credit give an example file and line to change)
* See Tilt perform the update and then see the change live

An example workflow makes it easy for a user to map Tilt onto their existing mental model of the dev workflow.

## Advanced Features

As you configured Tilt you may have added convenient features in the Tiltfile. E.g. making it easy to recreate the database with a `local_resource` or use config values to choose what servers to set up as editable. Tell users about the bells and whistles so they can enjoy them too!

## Known Issues

At the beginning there are probably ways that Tilt is worse or even just different than the legacy dev environment. Telling users about these differences before they experience them builds trust. Soemthing as simple as a list of links to issues in your issue tracker helps manage users' expectations.

## Next Steps

Tell users how to give feedback and get support. Mabye they should join a Slack channel or subscribe to an email list. If you're looking for volunteers to help improve Tilt, mention that here.

## The Transition Guide is Temporary

A transition guide is meant to help users get over the hump of switching tools. This makes it different than a design doc or even new hire onboarding docs, though they can share a lot of content. A small effort describing the move from the legacy tool to Tilt reduces the friction of trying a new tool.

## Evaluation

**Use this if** AppDev is using a legacy tool today and you think they'd have a better experience with Tilt.

**Skip this if**
* You're still evaluating Tilt and want to share it with a collaborator who will learn Tilt for themselves. This advice is for when you have users you want to use Tilt without having to study it themselves.
* AppDev doesn't have an existing workflow. (e.g. it's a new project that's used Tilt since you started it).

**You know it's successful when** an AppDev can go from hearing about Tilt to using it to develop in a half-hour using just the guide.