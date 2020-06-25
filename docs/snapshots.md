---
title: Private Team Snapshots
description: "Securely receive private team snapshots from team members uing Tilt, helping you debug their Tilt state."
layout: docs
---

As the Developer Experience (DevEx) engineer responsible for managing the Tiltfile and Tilt workflows for your team, you can securely receive private team snapshots from team members using Tilt, helping you asynchronously debug Tilt setup problems or any development issues more generally. A snapshot is a frozen moment-in-time representation of a team member's Tilt state from _their_ local machine running Tilt. You access it on Tilt Cloud (so you don't even have to be running Tilt). It looks and works exactly like Tilt, so you can interactively explore the team member's current Tilt state, including services, alerts, and Kubernetes events.

Developer team members can also share snapshots with each other, to better collaborate on development tasks.

Visit [https://cloud.tilt.dev/snapshot/Afygp-8LJ4vRmVdGtHU=](https://cloud.tilt.dev/snapshot/Afygp-8LJ4vRmVdGtHU=) and interact with it. It's a real snapshot on Tilt Cloud. (You can view it because it's an _internet-public_ snapshot. See below for public snapshots.)

![snapshot](assets/img/snapshot.png)

## Creating and sharing private team snapshots

[Ensure your project is associated with a Tilt Cloud team using `set_team` in your Tiltfile.](teams.html) Make sure you are either a [`Member` or `Owner`](teams.html#add-users-to-your-team) of the team.

Inside Tilt, click the `Create a snapshot` button at the top. If you haven't yet connected Tilt to Tilt Cloud, you'll be prompted to do so (using your GitHub account to sign in). Click `GET LINK` to create the snapshot. Click `OPEN` and Tilt will open the snapshot in Tilt Cloud in a new browser tab. Copy the URL of the snapshot and share it with other team members (via Slack or email, for example). The snapshot is only accessible to Tilt Cloud signed-in users who are a member (or owner) of the team

![create-snapshot](assets/img/create-snapshot.png)

## Viewing all private team snapshots

Click the `Create a snapshot` button in Tilt. In the modal, click `View snapshots from your team`. to see a list of all private team snapshots, for that team, in Tilt Cloud.

## Public snapshots

If your project is not associated with a Tilt Cloud team (i.e. your Tiltfile is not using `set_team`), you will still be able to create snapshots. Following the same flow as above, the snapshots you create will be public. Everyone on the internet will be able to access them, without having to sign into Tilt Cloud.

In the same modal as above, click `Manage your snapshots on Tilt Cloud` to see a list of public snapshots that you've created, in Tilt Cloud.

## FAQ

### Q: What data do you store for each snapshot?
For each snapshot we store the entirety of your Tilt's state, including all logs and build history. In addition we store two pieces of metadata: the time that the snapshot was taken and the user, if any, that created it.

### Q: I'm worried about app devs accidentally posting snapshots with secrets or private data. How can I disable snapshots?
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
