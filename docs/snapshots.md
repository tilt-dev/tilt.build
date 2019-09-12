---
title: Share Errors and Cluster State with Snapshots
layout: docs
---

Thanks for trying out the snapshots alpha! This page explains what snapshots are and how to manage them. There's also a [FAQ section](/snapshots#faq) at the end.

As this feature is in alpha the screenshots here may not exactly match what is currently in the UI. Thanks for understanding!

## What is a snapshot?
A snapshot is a link that you can send to someone that will allow them to interactively explore your current Tilt state. This is useful for async debugging and adding context to bug reports. They look like pretty much just like Tilt, but frozen in time:

[https://cloud.tilt.dev/snapshot/AfCRlNcLyfhEJR97q8o=](https://cloud.tilt.dev/snapshot/AfCRlNcLyfhEJR97q8o=)

A snapshot is a frozen "moment-in-time" version of the Tilt UI. In a snapshot you can drill in to specific services, see alerts and Kubernetes events. Pretty much anything you can do in normal Tilt, you can do in a snapshot!

## Sharing Snapshots
In order to share a snapshot first make sure that the feature is enabled for you in your Tiltfile:

```python
enable_feature("snapshots")
```

A button will then appear in the upper right corner of the Tilt Web UI:

![share snapshot](assets/img/share-snapshot-button.png)

If you click this button a modal will appear.

![snapshot modal](assets/img/snapshot-modal.png)

Click "Get Link" and you should be presented with a URL that looks something like this: [https://cloud.tilt.dev/snapshot/AfCRlNcLyfhEJR97q8o=](https://cloud.tilt.dev/snapshot/AfCRlNcLyfhEJR97q8o=).

Simply click the button that appeared to see the snapshot. Or you can take the generated link, post it in a Slack channel, bug report or on Twitter so _anyone_ will be able to what you were seeing in Tilt when you ran in to an issue.

## Managing your snapshots

You can share snapshots anonymously as described above. If you'd like the ability to list
or delete snapshots you've shared, you need to link your instance of Tilt to a TiltCloud account.

From the share snapshot modal (accessible from the Share Snapshot button in the Tilt web UI) click "Connect to TiltCloud".

![connect to TiltCloud](assets/img/connect-to-tiltcloud.png)

From there simply log in to your GitHub account to create a TiltCloud account.

If you go back to Tilt, you should see that your GitHub username in the share snapshot modal.

![snapshot modal username](assets/img/snapshot-modal-username.png)

From here on out all snapshots that you share from Tilt will be associated with your account, and will be manageable as described in the next section.

## Managing Snapshots
You can view and delete all of the snapshots associated with your account on TiltCloud. Simply go to [https://cloud.tilt.dev/snapshots](https://cloud.tilt.dev/snapshots) (this is also linked from the bottom of the "Share Snapshot" window). This will display a list of all of your snapshots, with a button to delete the ones you don't want anymore.

![snapshots list](assets/img/snapshots-list.png)

## FAQ

### Q: What data do you store for each snapshot?
For each snapshot we store the entirety of your Tilt's state, including all logs and build history. In addition we store two pieces of metadata: the time that the snapshot was taken and the user, if any, that created it.

### Q: Can I delete a snapshot that I created before I linked my TiltCloud account?
No. Any snapshot created while you were signed out can't be deleted.

### Q: If I delete a snapshot is any data retained?
No. If you delete a snapshot all associated data is removed from the data store. There is no soft delete.

### Q: What data do you store when I create a TiltCloud account?
Our database table for users looks like this:

```
 id |      name      | provider | provider_user_id | provider_user_name
----+----------------+----------+------------------+--------------------
  2 | Mary Miranda   | github   | 1234567          | mmiranda
  ```
