---
title: Share Errors and Cluster State with Snapshots
layout: docs
---

As this feature is new and being improved the screenshots here may not exactly match what is currently in the UI. Thanks for understanding!

## What is a snapshot?

A snapshot is a link that you can send to someone that will allow them to interactively explore your current Tilt state. This is useful for async debugging and adding context to bug reports. They look like pretty much just like Tilt, but frozen in time:

[https://cloud.tilt.dev/snapshot/AYSV59gLhM3GVMuuR28=](https://cloud.tilt.dev/snapshot/AYSV59gLhM3GVMuuR28=)

A snapshot is a frozen "moment-in-time" version of the Tilt UI. In a snapshot you can drill in to specific services, see alerts and Kubernetes events. Pretty much anything you can do in normal Tilt, you can do in a snapshot!

## Sharing Snapshots

If you have upgraded Tilt since Snapshots were released, you'll have a button in
the Tilt web UI:

![share snapshot](assets/img/share-snapshot-button.png)

If you click this button a modal will appear.

![snapshot modal](assets/img/snapshot-modal.png)

If you haven't already connected Tilt to Tilt Cloud, you'll need to click a couple
buttons to create a Tilt Cloud account:

![link to TiltCloud](assets/img/link-to-tiltcloud.png)

Once you've done that, just click "Get Link" and you should be presented with a
URL that looks something like this: [https://cloud.tilt.dev/snapshot/AYSV59gLhM3GVMuuR28=](https://cloud.tilt.dev/snapshot/AYSV59gLhM3GVMuuR28=).

Click the button that appeared to see the snapshot. Or you can take the generated link, post it in a Slack channel, bug report or on Twitter so _anyone_ will be able to what you were seeing in Tilt when you ran in to an issue.

## Managing Snapshots
You can view and delete all of the snapshots associated with your account on Tilt Cloud. Go to [https://cloud.tilt.dev/snapshots](https://cloud.tilt.dev/snapshots) (this is also linked from the bottom of the "Share Snapshot" window). This will display a list of all of your snapshots, with a button to delete the ones you don't want anymore.

![snapshots list](assets/img/snapshots-list.png)

## FAQ

### Q: What data do you store for each snapshot?
For each snapshot we store the entirety of your Tilt's state, including all logs and build history. In addition we store two pieces of metadata: the time that the snapshot was taken and the user, if any, that created it.

### Q: How private are snapshots?
A snapshot is accessible to anyone who has the link, which includes an unguessable ID.
Providing stricter access control is on our roadmap. If this is important to you,
[let us know](https://tilt.dev/contact)!

### Q: My company doesn't allow sharing data with a SaaS. How can I disable snapshots?
Add the [`disable_snapshots`](https://docs.tilt.dev/api.html#api.disable_snapshots)
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
### Q: I'm sometimes seeing 500 errors when creating a snapshot. Is that expected?
There's a [known bug](https://github.com/windmilleng/tilt/issues/3194) for larger snapshots.
