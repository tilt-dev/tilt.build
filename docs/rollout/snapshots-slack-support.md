---
title: Attach Snapshots in Slack Support Channel
layout: rollout
---

## Attach a snapshot with Slack support messages

If you're using Slack to support users, encourage folks to create a [snapshot](../snapshots) of their Tilt state, and include the snapshot link in their Slack message, every time they report a new problem or offer a piece of feedback. (This also applies if folks report in via email or an issue tracker.)

## Why it's effective

- Support problems are best triaged with maximum context, and in the case of Tilt, a snapshot provides the most context with very little effort on the part of the reporter.
- When a snapshot is provided up front, there's less back and forth required since you're more likely able to pinpoint the root cause earlier. Thus you save even more time if your support channel is async. As the DevEx person, you can resolve the issue with one round trip interaction, which may be within a day, versus several days if multiple round trips are required.
- Developers naturally intuit providing maximum context. They often ask for reproducibility steps or screenshots when fixing problems themselves. So once they've used snapshots a few times with fast support turnaround times, they will quickly internalize the benefits and use them consistently.
- Everyone on the team can access the snapshot, so developers (who are naturally collaborative) are enabled to support each other, perhaps even before you get to a support issue.
- [A future Tilt enhancement](https://github.com/tilt-dev/tilt/issues/3741) would streamline snapshots and support requests.

## Encourage consistent snapshot use
- As the DevEx person, consistently remind users to link to a snapshot which each support request, signaling clear expectations, especially in a public Slack channel.
- Update the [Slack channel topic](https://slack.com/help/articles/201654083-Set-a-channel-topic-or-description) to remind users that it's required.
- In the last step of onboarding, require a user to attach a snapshot in the Slack support channel, reporting a problem (if there is one) or offering an improvement suggestion to your team's dev workflow. As the DevEx person, be sure to respond, giving them positive feedback in their first encounter of snapshots.

## Evaluation

**Use this if**
- You have a dedicated supported channel, in Slack or otherwise.
- You are [prioritizing inactive users](../rollout/prioritize-inactive).

**Skip this if**
- You currently are not offering your team to use snapshots.

**You know it's successful when** new support requests consistently have snapshots attached, without prodding required. Developer teammates are opening the snapshots and supporting each other,
even before you get to the problems.
