---
title: Teams
description: "Tilt Cloud let you create a team to manage access to Snapshots"
layout: docs
---

[Tilt Cloud](tilt_cloud.html) is now deprecated. The Teams feature allowed you to manage permissions for [Snapshots](snapshots.html), and see a Tilt usage dashboard for members of your team.

A single team could be associated with one or more Tiltfiles. The team id (which is the string of text after `/team` in the URL, e.g. `27d7ad9c-53f8-4700-80b8-b217eeb8effg`) is added to the Tiltfile using the [`set_team( )` function](./api.html#api.set_team), for example:

`set_team('27d7ad9c-53f8-4700-80b8-b217eeb8effg')`


Tilt Cloud let you see everyone running Tilt across all projects. You could see when they last ran Tilt and their version.

<figure>
    <img src="/assets/img/last-seen-versions.png" class="no-shadow" alt="Last seen versions">
</figure>
