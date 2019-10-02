---
slug: solving-the-laggy-human-shell-problem
date: 2019-10-01
author: dmiller
layout: blog
title: "Solving the Laggy Human Shell Problem"
image: ships_pass.png
image_caption: "Two ships pass in the middle of the night"
tags:
  - kubernetes
  - developer-tools
  - snapshot
keywords:
  - kubernetes
  - developer-tools
---

Tilt highlights problems so you can focus on fixing them, not finding them. When you see a build breakage in the service you just edited, you can respond while you're still thinking about it. What can you do when the failing service is one you've never touched? We see Slack channels turn into poor excuses for shells: Dan reports an error; Han asks him to copy/paste the output; Dan pastes it; no, not that output, the lines above it--

Has this ever happened to you?

![Two engineers discussing a problem across timezones](/assets/images/solving-the-laggy-human-shell-problem/without_snapshots.png)

After lots of back and forth and a few misaligned lunch breaks Dan gets a solution thanks to Han's help. All told, it took Dan hours to get an answer to his question, just so he could get started working on a service that is new to him.

## The Laggy Human Shell

I call this the Laggy Human Shell problem: when two coworkers are communicating over text and asking each other to run commands, but keep missing each other, like ships passing in the night, with a 20 minute - 24 hour turnaround time on each message. It would be so much faster if you had access to their environment, but that's not always possible if it's a laptop or an external person's machine.

To solve this problem, we built snapshots. Snapshots allow you to send a link to someone with a frozen “moment-in-time” version of the Tilt UI. In a snapshot you can drill in to specific services, see alerts, Kubernetes events, and everything else you can see in the Tilt UI!

With snapshots, Dan and Han's laggy human shell session would have looked like this:

![A snapshot link simplifies Dan and Han's conversation](/assets/images/solving-the-laggy-human-shell-problem/with_snapshots.png)

Since a Tilt snapshot contains the state of your Kubernetes cluster, sending someone a Tilt snapshot allows them to asynchronously diagnose your problem, rather than waiting for both of you to have bandwidth at the same time.

## Introducing Tilt Snapshots

A snapshot is a link that you can send to someone that will allow them to interactively explore your current Tilt state. This is useful for async debugging and adding context to bug reports. They look like pretty much just like Tilt, but frozen in time. Here's an example:

[https://cloud.tilt.dev/snapshot/AYSV59gLhM3GVMuuR28=](https://cloud.tilt.dev/snapshot/AYSV59gLhM3GVMuuR28=)

![A screenshot of a snapshot](/assets/images/solving-the-laggy-human-shell-problem/with_snapshots.png)

### Sharing Snapshots

If you are running a recent version of Tilt, you'll see 'Create Snapshot' in the Tilt web UI:

![share snapshot](/assets/images/solving-the-laggy-human-shell-problem/share-snapshot-button.png)

Clicking brings up a modal.

![snapshot modal](/assets/images/solving-the-laggy-human-shell-problem/snapshot-modal.png)

You'll need to create and link a TiltCloud account if you haven't already.

![link to TiltCloud](/assets/images/solving-the-laggy-human-shell-problem/link-to-tiltcloud.png)

Once you've done that, just click "Get Link" and you should be presented with a
URL like: [https://cloud.tilt.dev/snapshot/AYSV59gLhM3GVMuuR28=](https://cloud.tilt.dev/snapshot/AYSV59gLhM3GVMuuR28=).

Click the button that appeared to see the snapshot. Or you can take the generated link, post it in a Slack channel, bug report or on Twitter so _anyone_ will be able to what you were seeing in Tilt when you ran in to an issue.

### Managing Snapshots

You can view and delete all of the snapshots associated with your account on TiltCloud. Go to [https://cloud.tilt.dev/snapshots](https://cloud.tilt.dev/snapshots) (this is also linked from the bottom of the "Share Snapshot" window). This will display a list of all of your snapshots, with the ability to delete old snapshots.

![snapshots list](/assets/images/solving-the-laggy-human-shell-problem/snapshots-list.png)

## Learn More

Can’t wait to enhance your productivity with snapshots? If you have the latest version of Tilt installed you can get started today! For more information, check out the [snapshots documentation](https://docs.tilt.dev/snapshots).
