---
title: In-product Onboarding
layout: rollout
---

## In-product onboarding

Tilt is a powerful tool, and thus requires some investment on the part of a new user to learn the basics. We recommend providing a [transition guide](../rollout/introduce-tilt) to help developers during this initial stage. Additionally, many onboarding steps can be driven with _in-product onboarding_, where Tilt itself guides the new user through initial set up, and usage of features, from basic to advanced.

## Why it's effective

- With in-product onboarding, you don't need to maintain a separate onboarding doc, where steps can get out of date over time. The source of truth is the product itself.
- The system keeps track of where you are, as the user, during the onboarding process, and provides customized help and reminders. If you do onboarding over several sittings, you immediately pick up where you left off at the beginning of each session, since the system saves state.
- As the DevEx person, the system provides you real-time state of where each user is in their individual onboarding, as well as metrics of how past users performed at certain steps. You see bottlenecks and improve onboarding over time from this insight.

## Custom scripts

Consider using offering custom scripts to help a new user install the preferred [local Kubernetes cluster](../choosing_clusters.html) or [install](../install.html)/[upgrade](../upgrade) the preferred version of Tilt. You can also take advantage of [Tiltfiles being written in the Python-dialect of Starklark](../tiltfile_concepts) to create custom logic to help new users when the first run Tilt, in particular with `local_resource`(../local_resource). We'd love to help your team with these ideas, accounting for your specific needs. [Schedule a chat with us.](https://calendly.com/dbentley/tilt-enterprise)

## Future enhancement

Tilt itself doesn't have in-product onboarding yet. If this sounds interesting to you, let us know which parts of onboarding you'd want to see in Tilt.

## Evaluation

**Use this if**
- You are starting to get more new users regularly and want to streamline onboarding.

**Skip this if**
- You are just starting to get your initial batch of users and are figuring out the onboarding steps.

**You know it's successful when** each subsequent new user onboards more smoothly and quickly, and gives you feedback saying so.
