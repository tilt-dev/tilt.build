---
title: Capture Attention with a Tilt-enabled Shiny Feature
layout: rollout
---

## Leverage a Tilt-enabled shiny feature to catch attention

Tilt is a powerful tool that allows you, as the DevEx person, to offer an optimized developer experience for your team. You may be tempted to get everything right before rolling out Tilt to AppDevs. But just as you should [focus on a small set of AppDevs to start](../rollout/focus), spend effort on delivering just one or at most two Tilt-enabled functionalities that will really wow your AppDevs. AppDevs are already bogged down during a busy work day, often switching between many devl tools. So catch their attention with a new shiny feature that your new Tilt-focused DevEx platform provides.

## Polish the shiny feature 

Tilt out the box already provides an elevated AppDev experience, such as a streamlined web UI consolidating all parts of your app. But the real magic of Tilt lies in the fully customizable [Tiltfile](..tiltfile_concepts), allowing for a truly unique experience that targets your team's specific needs, different from any other company, or even any other team within your company. Invest in the extra effort to polish a shiny feature that really stands out, beyond what was previously possible prior to rolling out out Tilt. It bears repeating: Focus on depth over breadth. Identify one feature to make really shiny with your limited time, instead of delivering multiple features that will turn out to be less memorable. Only once you've captured the hearts of those initial AppDevs with that first shiny feature, you can move on to the next one.

## Shiny ideas

**Surface all parts of your app in Tilt**: Apps, especially cloud-native apps have increasingly many components. Oftentimes AppDevs have simply given up trying to see the big picture, and only focus on setting up a small handful of microservices at a time during development, resulting in frustrating problems such as inconsistent data or outdated APIs. Consider including as many resources in the Tiltfile as you, that's still relevant to development. Using [Tiltfile Configs](../tiltfile_config) to further offer customized scenarios, for example, the frontend config vs the backend config.


- Extensions


- extensions


The [transition guide](../rollout/introduce-tilt) and [in-product onboarding](../rollout/in-product-onboarding) provide methodical ways to ease some of this complexity. But especially with folks that are bogged down during a busy work day, it's helpful to catch a user's attention with a shiny feature early on during onboarding, in order to really get them interested in seeing how Tilt significantly improves their workflow.

As the DevEx person deploying Tilt, consider leading with a short 2 minute demo in an introductory meeting. Or embedding a gif in an introductory email. Really catch the attention of folks early on.

## Pick a shiny feature that your team will understand

Tilt has many shiny features, in general. But likely only a subset of them would be most relevant to your team and your team's current dev workflow. And even only a few from there would be immediately understandable to your users. So pick one, or at most two Tilt features to wow your users early on. Remember the purpose here is just to get folks hooked and generate excitement. Once they're on board with Tilt, you can spend more time discussing more nuanced functionality.

## Some shiny features to consider

- Tilt puts all the pieces of your app in a single UI. If your team struggles with a lengthy dev environment set up, juggling multiple services with many error-prone steps, then show how a single `tilt up` command and a streamlined web UI fixes that.
- Tilt abstracts away local Kubernetes clusters. If your team is new to Kubernetes and finds it dizzying, show how Tilt removes this friction.
- Tilt uses [`live_update`](../live_update_tutorial) to deploy code to containers directly in seconds, instead of minutes with images traditionally. If your team complains about slow dev cycles because of image deploys, show them this.
- Tilt uses [snapshots](../snapshots) to facilitate async code collaboration and team support. If your team finds it hard to collaborate because of tooling shortcomings, show them this.

## Evaluation

**Use this if**

- You are just starting to create an onboarding strategy and considering ways to get buy-in from developers.
- You've had some success converting users, but many of them tell you the benefits of Tilt wasn't obvious at first.

**Skip this if**

- Users are already quickly onboarding to Tilt and understanding the benefits right away.

**You know it's successful when** you consistently see more aha moments from new users.
.
