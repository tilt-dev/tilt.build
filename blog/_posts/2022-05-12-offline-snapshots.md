---
slug: "offline-snapshots"
date: 2022-05-12
author: milas
layout: blog
title: "Offline Snapshots & Tilt Cloud Deprecation"
image: "/assets/images/offline-snapshots/title.jpg"
image_caption: 'Photo by <a rel="noopener noreferrer" href="https://unsplash.com/photos/jvPTh8YAgYM">
TheRegisti</a> on Unsplash'
description: "Same Snapshots, New Workflow"
tags:
- tilt
- snapshot
---

Starting with Tilt v0.30.0, Snapshots will work a little differently!

If you haven't used [Snapshots][docs-snapshots] in Tilt before, it's a great way to share the state of your local development environment with someone else for troubleshooting or debugging a failed CI run.

So, what's changing?

We've decided to make taking and viewing Snapshots a purely offline experience and will be shutting off the Tilt Cloud connection in the coming weeks.

Let's check out the revised experience and then touch on what the Tilt Cloud deprecation means for you.

### Take a Snapshot
Taking a Snapshot from the Tilt UI is as easy as clicking "Save Snapshot": 

![Screenshot of the Snapshot dialog in the Tilt UI](/assets/images/offline-snapshots/dialog.png)

It's also possible to take a Snapshot for a running Tilt instance on-demand from the CLI:
```shell
tilt snapshot create snapshot.json
```
Or, you can have your CI job automatically save a Snapshot at the end of its run: 
```shell
tilt ci --output-snapshot-on-exit snapshot.json
```

### View a Snapshot
Tilt now includes a built-in snapshot viewer that you can launch by running:
```shell
tilt snapshot view snapshot.json
```

After a moment, you should see your Snapshot in the browser:
![Screenshot of a Tilt Snapshot viewed locally](/assets/images/offline-snapshots/snapshot.png)


### Tilt Cloud Shutdown
Starting May 19, 2022, we'll move Tilt Cloud into read-only mode.
No new users will be able to register, no new teams can be created, and most importantly, no new cloud Snapshots can be saved.

On June 17, 2022, we'll be turning off the Tilt Cloud servers and deleting all saved cloud Snapshots.

If you currently have cloud Snapshots you want to keep, you can download them from the [My Snapshots][cloud-snapshot-list] page before then:
![Screenshot of Tilt Cloud interface showing the download button](/assets/images/offline-snapshots/cloud.png)
Snapshots downloaded from Tilt Cloud can then be viewed with `tilt snapshot view`.

We know Snapshots help save teams time every day, and Tilt Cloud has been a key part of this experience to date.
Now we're excited for you to try out this next phase! 📷  

[docs-snapshots]: https://docs.tilt.dev/snapshots.html
[cloud-snapshot-list]: https://cloud.tilt.dev/snapshots
