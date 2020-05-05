---
title: Teams
layout: docs
---

## Create a team

Many Tilt Cloud features are based on the concept of a Tilt team. Once you've signed in to Tilt Cloud, create a team by selecting the option at the top right, entering a team name, and clicking Create My Team. This will bring you to the team page of your new team. You are the team owner as a result. To navigate to an existing team that you own, hover over the Teams dropdown at the top right of the screen.

You can also change the team name on this page. 

<figure>
    <img src="/assets/img/new-team.png" class="no-shadow" alt="New team">
</figure>

## Associate team with a project

Tilt is designed to have a single team be associated with a single Tiltfile of a project. As the team owner, after you've created a team, copy the team id (which is the string of text after `/team` in the URL, e.g. `27d7ad9c-53f8-4700-80b8-b217eeb8effg`), and enter it into your Tiltfile with the [`set_team( )` function](./api.html#api.set_team), for example: 

`set_team('27d7ad9c-53f8-4700-80b8-b217eeb8effg')`

Commit the change to source control. 

## Last seen versions

You'll now see all folks who run Tilt with the updated Tilfile, appear on the team page, including when they last ran Tilt and the version they are using. Ask users to sign in to Tilt Cloud in Tilt for their name to appear on the team page. Otherwise, they will appear as anonymous.

<figure>
    <img src="/assets/img/last-seen-versions.png" class="no-shadow" alt="Last seen versions">
</figure>


## Add users to your team

New users on the team page will appear with the role `None` as they run Tilt. A team owner (`Owner`) can change any other user's role to `Member` or `Owner`.
An `Owner` cannot change their own role. Only `Owner`s can change the team name. Both `Member`s and `Owners` can view the team page.