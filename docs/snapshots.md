---
title: Share Errors and Cluster State with Snapshots
description: "Share Tilt state with snapshots for easy remote or async debugging"
layout: docs
---
## What Is a Snapshot?

A snapshot is a link that you can send to someone that will allow them to interactively explore your current Tilt state. This is useful for async debugging and adding context to bug reports. They look like pretty much just like Tilt, but frozen in time:

[https://cloud.tilt.dev/snapshot/AYSV59gLhM3GVMuuR28=](https://cloud.tilt.dev/snapshot/AYSV59gLhM3GVMuuR28=)

In a snapshot you can drill into specific services, peruse logs, and see alerts and Kubernetes events. Pretty much anything you can do in normal Tilt, you can do in a snapshot! You don't have to be running Tilt to access a snapshot; just click the link, and you can see exactly what that user's Tilt UI looked like at that moment in time.

### Snapshots in Your Org
Snapshots and [Tilt Teams](teams.html) are two great tastes that taste great together! When running a Tiltfile associated with a team (via the `set_team` functions), any snapshots you create are *private*, and are only accessible by members of that team. You can use snapshots with confidence that any sensitive information in your logs is safe from prying eyes.

Snapshots are a great tool for debugging **remotely** and **asynchronously**--two necessities in the current age of work-from-home. Snapshots eliminate the need for Slack back-and-forth when diagnosing a problem; instead of guessing what error message to copy and paste, a developer can just send their entire Tilt state. Likewise, the frozen-in-time nature of Snapshots makes async debugging a breeze: if a dev encounters strange behavior and the right person to ask isn't online, it's easy to take a snapshot, send over the link, and go back to writing code. 

## Creating and Sharing Snapshots
Inside Tilt, click the `Create a snapshot` button at the top. If you haven't yet connected Tilt to Tilt Cloud, you'll be prompted to do so (using your GitHub account to sign in). Click `GET LINK` to create the snapshot. Click `OPEN` and Tilt will open the snapshot in Tilt Cloud in a new browser tab. Copy the URL of the snapshot and share at will.

// TOOD: maybe a gif here instead?
![create-snapshot](assets/img/create-snapshot.png)

Visit [cloud.tilt.dev/snapshots](https://cloud.tilt.dev/snapshots) for a list of all active snapshots you have created.

### Private Snapshots (aka Team Snapshots)
If your Tilt state contains sensitive or proprietary information, or you just want to protect it from outside eyes, don't worry: if your Tiltfile belongs to a [Tilt Cloud team](teams.html), any snapshots created will be viewable only be members of that team.

To create _private_ snapshots, [ensure your project is associated with a Tilt Cloud team using `set_team` in your Tiltfile.](teams.html) Make sure you are either a [`Member` or `Owner`](teams.html#add-users-to-your-team) of the team. Then follow the instructions above. The resulting snapshot will only be viewable by Tilt Cloud users  who are `Member`s or `Owners` of the associated team.

// TODO: screenshot (access denied)

**Important**: If the Tiltfile errors on its first execution when you run `tilt up`, and [`set_team`](https://docs.tilt.dev/api.html#api.set_team) has not been called yet, Tilt will not understand `set_team`. If you then take a snapshot, it will be a _public_ snapshot. (See below for public snapshots.) To work around this problem, make sure to put `set_team` as the first line in your Tiltfile. Tilt will then successfully parse `set_team` and start using the team id in it. Create a snapshot as normal and it will be a private team snapshot.

To view all snapshots associated with your team: click the `Create a snapshot` button in Tilt, and in the modal, click `View snapshots from your team`.

## FAQ

### Q: What data do you store for each snapshot?
For each snapshot we store the entirety of your Tilt's state, including all logs and build history. In addition we store two pieces of metadata: the time that the snapshot was taken and the user, if any, that created it.

### Q: I'm worried about app devs accidentally posting snapshots with secrets or private data. How can I disable snapshots?
If you call `set_team` in your Tiltfile, then any snapshot created from that Tiltfile will only be viewable by
Tilt Cloud users associated with that team. However, if you don't use [Tilt Cloud Teams](teams.html), or for an
extra layer of security, add the [`disable_snapshots`](https://docs.tilt.dev/api.html#api.disable_snapshots)
directive to your Tiltfile.

### Q: If I delete a snapshot is any data retained?
No. If you delete a snapshot all associated data is removed from the data store. There is no soft delete.

### Q: What data do you store when I create a Tilt Cloud account?
Our database table for users looks like this:

```
 id |      name      | provider | provider_user_id | provider_user_name
----+----------------+----------+------------------+--------------------
  2 | Mary Miranda   | github   | 1234567          | mmiranda
  ```
