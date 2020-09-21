---
title: Attach Snapshots in Slack Support Channel
layout: rollout
---

## Attach a snapshot with Slack support messages

If you're using Slack to support users, encourage folks to create a [snapshot](../snapshots) of their Tilt state, and include the snapshot link in their Slack message, every time they report a problem or offer feedback. (This also applies if users report in via email or an issue tracker.)

## Encourage consistent snapshot use

- As the DevEx person, consistently remind users to link to a snapshot with each support request, signaling clear expectations, especially in a public Slack channel.
- Update the [Slack channel topic](https://slack.com/help/articles/201654083-Set-a-channel-topic-or-description) to remind users that it's required.
- In the last step of onboarding, require a user to attach a snapshot in the Slack support channel, reporting a problem (if there is one) or offering an improvement suggestion to your team's dev workflow. As the DevEx person, be sure to respond, giving them positive feedback in their first encounter of snapshots.

## Why it's effective

- Support problems are best triaged with maximum context, and in the case of Tilt, a snapshot provides the most context with very little effort required on the part of the reporter.
- If a snapshot is provided up front, there's less back and forth required since as the DevEx person, you're more likely able to pinpoint the root cause earlier. Thus you save even more time if your support channel is async. You can resolve the issue with one round trip interaction, which may be within a day, versus several days if multiple round trips are required.
- Developers naturally intuit providing maximum context. They often ask for reproducibility steps or screenshots when fixing problems themselves. So once they've used snapshots a few times with fast support turnaround times, they will quickly internalize the benefits and use them consistently.
- Everyone on the team can access snapshots, so naturally collaborative developers may support each other, perhaps even before you get to a particular support issue.
- [A future Tilt enhancement](https://github.com/tilt-dev/tilt/issues/3741) would streamline snapshots and support requests.

## Evaluation

**Use this if**
* Your team asks a lot of support questions on Slack.
* You find that triaging or debugging issues spends a lot of time on back and forth (see [The Laggy Human Shell Problem](https://blog.tilt.dev/2019/10/01/solving-the-laggy-human-shell-problem.html)
* You are [prioritizing inactive users](../rollout/prioritize-inactive).

**Skip this if**
* You have disabled snapshots for your team.

**You know it's successful when**
* Your Slack channel is less full of people asking other people to run shell commands for more information.
