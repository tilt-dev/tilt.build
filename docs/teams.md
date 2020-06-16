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

## Associate team with multiple projects

Tilt is designed to have a single team be associated with one or more Tiltfiles in potentially multiple projects. As the team owner, after you've created a team, copy the team id (which is the string of text after `/team` in the URL, e.g. `27d7ad9c-53f8-4700-80b8-b217eeb8effg`), and enter it into each Tiltfile with the [`set_team( )` function](./api.html#api.set_team), for example:

`set_team('27d7ad9c-53f8-4700-80b8-b217eeb8effg')`

Commit the changes to source control.

It's a best practice to add the same team_id to as many Tiltfiles in your organization as possible, especially if you as a DevEx engineer, want to see all information aggregated across all those projects, together in one place.

## Last seen versions

You'll now see all folks who run Tilt across all projects with the updated Tiltfiles, appear on the team page, including when they last ran Tilt and the version they are using. Ask users to sign in to Tilt Cloud in Tilt for their name to appear on the team page. Otherwise, they will appear as anonymous.

<figure>
    <img src="/assets/img/last-seen-versions.png" class="no-shadow" alt="Last seen versions">
</figure>

## Canary Tilt releases before your team upgrades

Tilt's web UI will nudge users to upgrade when a new release is available, at the bottom right of the screen.

When running Tilt with a Tiltfile that specifies a team id, the default behavior is that users are only notified about Tilt releases once they're one week old<sup>[\*](#minimum-suggested-version)</sup>.

However, the team's *owners* are notified of Tilt releases as soon as they come out, giving them an opportunity to canary the new version before the rest of their team. If no action is taken, Tilt will begin notifying non-`Owner`s of a release once it's a week old. (If [`version_settings(check_updates=False)`](./api.html#api.version_settings) is set in the Tiltfile, users don't get notified, regardless of their role.)

A team owner can choose to prompt their teammates to upgrade to new Tilt release sooner than a week. If they visit their team's page on Tilt Cloud, they will find a button to "promote" the new version to their team. If they promote, all users (not just `Owner`s) will now start getting the version nudge corresponding to that latest Tilt version (the next time their Tilt checks for updates, which is on startup and hourly).

<figure>
    <img src="/assets/img/team-promote-version.png" class="no-shadow" alt="Promote Team Version">
</figure>

<a name="minimum-suggested-version"></a><small>\* For technical reasons, there is no 1-week waiting period on Tilt 0.13.5.</small>

## Add users to your team

New users on the team page will appear with the role `None` as they run Tilt. A team owner (`Owner`) can change any other user's role to `Member` or `Owner`.
An `Owner` cannot change their own role. Only `Owner`s can change the team name. Both `Member`s and `Owner`s can view the team page.
