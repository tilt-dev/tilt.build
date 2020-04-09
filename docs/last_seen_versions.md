---
title: Last Seen Versions
layout: docs
---

Tilt is designed to have a single [team](./teams.html) be associated with a single Tiltfile. As the team owner, after you've created a team, copy the team id (which is the string of text after `/team` in the URL, e.g. `27d7ad9c-53f8-4700-80b8-b217eeb8effg`), and enter it into your Tiltfile with the [`set_team( )` function](./api.html#api.set_team), for example: 

`set_team('27d7ad9c-53f8-4700-80b8-b217eeb8effg')`

Commit the change so that all folks who run Tilt will now have that in their Tiltfile. You'll now be able to see when a user last ran Tilt and the version of Tilt they are using.

<figure>
  <img src="/assets/img/last-seen-versions.png" class="no-shadow" alt="Last seen versions">
</figure>
