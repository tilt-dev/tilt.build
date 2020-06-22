---
title: Before you ask your team to tilt up...
description: "Here's a handy list of questions you might want to consider to ensure the best possible Tilt onboarding experience"
layout: docs
---

Before you ask your teammates to `tilt up`, here's a handy list of questions you
might want to consider to ensure the best possible onboarding experience:

## Setup and Compatibility

- Have you tested Tilt on all of the Operating Systems your team runs on their
  development machines?

- Do your colleagues know how to run Kubernetes locally? The choices can be
  overwhelming. Our guide to [choosing a cluster](choosing_clusters.html) can
  help.

- Which services do your colleagues hack on? Do all of them start up OK in Tilt?

- Are there any known gotchas or spurious error messages when you `tilt up` a
  server? Are they documented somewhere?

## Enhancements, errors, and optimizations

- `tilt up` each server and edit a file. Do you see the server auto-update with
  your changes?

- Are updates slow to show up? Could you add
  [a live_update rule](live_update_tutorial.html) to sync changes much faster?

- Do some file edits trigger unnecessary rebuilds? Have you added
  [ignore rules](file_changes.html) to prevent wasted work?

- Is auto-update the right behavior for all your servers? Are there servers
  where you'd rather they
  [only update when you're ready?](manual_update_control.html)

- When you introduce a syntax error into your code, does Tilt pop up an error?
  Would your teammates be able to find it?

- When you log a runtime error in your code, does it show up in the Tilt logs?

## Support, socialization, and followup

- Do you have a dedicated place to discuss dev environment improvements with your
  team, like a mailing list or Slack?

- Do your teammates know where to ask for help if their dev workflow breaks or
  gets frustratingly slow?

- Do you have a README to help your teammates `tilt up` and go?
  [Here's one that we use](welcome_to_tilt.html) that you're welcome to link to.

- Are there other teams in your org that could benefit from a cloud-native dev
  environment like Tilt?

---

Once you're ready, add a link to your README to the
[Welcome to Tilt](welcome_to_tilt.html) guide.

If you want the same guide but with project-specific instructions,
fork the [tilt-init repo](https://github.com/tilt-dev/tilt-init) and edit away!
