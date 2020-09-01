---
title: Get Feedback with Snapshots
layout: rollout
---

Getting feedback early and often helps unblock users, creates a channel for engagement, and ultimately improves adoption. This doc specifies steps to set up an effective feedback loop.

## Monthly check-in and async feedback
- Host a monthly check-in meeting with users to solicit feedback and provide major updates.
- Encourage frictionless and transparent feedback. Invite users to submit problems and ideas in the team Slack channel, and the team issue tracker. Label the issues with `tilt`. Don't use private or low-trafficked channels.
- Acknowledge any feedback immediately and for everyone to see, even if you don't act on it right away. Indicate [priority](../rollout/prioritize-inactive) of issues to be fixed. An issue tracker enables this. (Don't worry about maintaining due dates, that's too much overhead.)

## In-context feedback with snapshots
- Developers are uniquely motivated and aspire to submit effective feedback. Effective feedback has context: Screenshots, bug reproducibility steps, rough sketches, etc. 
- Encourage users to use the native Tilt [snapshots](../snapshots) feature, providing a lot of context with little effort.
- Users should create a snapshot and attach it to the GitHub issue as part of feedback submission. Use an [issue template](https://docs.github.com/en/github/building-a-strong-community/configuring-issue-templates-for-your-repository) to remind users of snapshots.
- [A future Tilt enhancement](https://github.com/tilt-dev/tilt/issues/3741) would combine all this into a single step.

## Make feedback submission part of onboarding
- Submitting feedback is part of the core Tilt experience.
- The last step of onboarding should require the user to submit an issue (with a template) that includes:
  - An attached snapshot.
  - Answers to a short survey regarding onboarding.
  - At least one feedback item regarding Tilt or the onboarding process.
- As the DevEx person deploying Tilt, review the issue, provide feedback, and close it if there are no remaining action items.

## Different types of feedback
- Consider tailoring your issue templates and/or Slack channels to accommodate different types of feedback.
- **Errors or problems using Tilt**: Help users distinguish between Tilt problems, problems with the greater dev infrastructure set up, or problems specific to the individual user's machine. Probably address this feedback with [higher priority](../rollout/prioritize-inactive).
- **Feature/improvement request**: Solicit this type of feedback often, since it will be rare. But don't over-index on it too much.
- **Sentiment**: Periodically gauge overall user emotion toward Tilt, as it is an early indicator of adoption. Excitement is best. Distaste is bad. But apathy is the worst. Use simple emoji polling (😀/🙁/🥱) in Slack or during a monthly check-in meeting to maximize voter turnout. 

## Team collaboration over personal help
- Developers are collaborative problem solvers that thrive in teams. Tilt is an open-source tool where the user can easily review a pre-configured Tiltfile. Tilt is the opposite of a black box.
- You can offer personal help to a developer. But a developer is more motiviated to contribute to improving the team's local dev infrastruture. Facilitate this by using the above strategies to create an open and collaborative environment.

## Evaluation

**Use this if**
- You are already getting a lot of feedback, and want to leverage it to foster community and create excitement.
- You are [prioritizing inactive users](../rollout/prioritize-inactive) and want to streamline efforts.

**Skip this if**
- You currently have a small number of users, less than 3; you should just work with the users individually to get feedback.

**You know it's successful when** the issue tracker has a lot of activity. Teammates are supporting each other and answering each other's problems,
even before you get to them.

