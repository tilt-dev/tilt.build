---
slug: "wip-vs-harness"
date: 2021-06-21
author: nick
layout: blog
title: "WIP Development vs Harness Development"
subtitle: "Local K8s dev, GitOps, and when to use them together"
description: "Local K8s dev, GitOps, and when to use them together"
image: "/assets/images/wip-vs-harness/cover.jpg"
image_caption: "<i>Everybody Rides in the Whip at Midland Beach</i>. Via <a href='https://digitalcollections.nypl.org/items/510d47d9-c024-a3d9-e040-e00a18064a99'>The New York Public Library</a>."
tags:
  - gitops
  - localdev
---

In the #tilt chat last month, `renaudguerin` asked:

> I’m the new DevOps guy in a small startup, and migrating us [...]
> towards a more modern GitOps workflow (ArgoCD/CodeFresh), and
> local k8s dev environments (either Skaffold or garden.io, tilt.dev ...) 
>
> But how do you bridge the gap between the two ?

This is a deep question! I've been thinking about an illuminating way to explore
it.

Here's an analogy that I've been toying with:

Look around at some public Git repos you like. Pick some popular ones and some
single-user ones.

The single-user ones might have lots of commit messages that simply say "WIP".

The popular ones have lots of instructions on how to review and test the PR.

Imagine you've never used Git before. You look at the published commits. You
conclude: these are mutually exclusive approaches. Some projects are WIP
projects. And some projects are verbose projects.

Maybe that analogy is illuminating. But if it's not, I'm going to go into more
detail on some of the patterns we've seen on:

- What problems GitOps & local Kubernetes dev solve

- How these two toolsets approach those problems

- How to bridge the gap between them

## More Service, More Problems

If you're working on a multi-service app, you have two modes of development:

- WIP mode - You're actively working on a solution to a problem. You want
  as-fast-as-possible feedback. Correctness and reliability take a back seat 
  to sheer speed of iteration. Kubernetes and Docker and anyone else --
  get out of the way!  You're going to iterate as fast as possible and you might break
  some stuff.

- Harness mode - You know the answer. The unknown bits have been solved. Now you're
  trying to fit the code into the larger system so you can merge to prod. 
  Here you care about correctness, reliability, and security. It's OK to slow
  down a bit to get things right.

These two sets may sound the same but they are mostly *non-overlapping*!

Here's a table to help illustrate the differences:

|          | WIP Changes | Harness Changes |
----------------|-------------|------------------
| Add segfaults to see what breaks                 | ✅ | ❌️                             |
| Bring up all services from scratch               | ✅ | Something terrible has happened |
| Reset the database                               | ✅️ | ❌ ❌ ❌                      |
| Sacrifice correctness for faster updates | ✅  |     ❌️                            |
| Security is not a concern | ✅ | 🚑 |
| Add stars to all your RBAC rules | ✅ | 🚑 |
| Audit records of every change | ❌️| ✅ |
| Only one update at a time | ❌️| ✅ |
| Rolling restarts | ❌ | ✅ |
| Rollbacks | 🤷 | 🙏 |
| Automatic reverts if too many errors | ❌ | ✅ |
| Immutable containers for security | ❌ | ✅ |

GitOps (ArgoCD, CodeFresh) is an approach to Harness development:

- A service in the cloud listens to changes to your Git repo.

- When your Git repo changes, the GitOps server updates your prod env to match
  what's in your Git repo.

- Git serves as the system of record for changes to your prod env.

Local K8s (Tilt, Skaffold) is an approach to WIP development:

- A service locally listens to changes to your filesystem.

- When your file system changes, the Tilt server updates your dev env to match
  what's on disk.

- Tilt doesn't worry to much about recording the history of changes, assuming
  that you can throw it all away when you're done.

## Blurred Lines

We recommend you use both GitOps and local K8s together! The Tilt team does this.

For local dev and CI, we use Tilt to run services against [a one-time-use KIND
cluster](https://blog.tilt.dev/2021/04/02/kubernetes-on-ci.html).

For production releases, we push a tag to our GitHub repo, and the CI system
will automatically create release binaries and update services.

We even work with teams who use Tilt to run ArgoCD in dev, to make changes to
how their GitOps pipeline works together.

---

But there are teams who mix and match these tools in ways they aren't intended! They
use WIP tools for harness mode, or Harness tools for dev mode.

### Local K8s for Harness Development

- I once met a team who needed to deploy to an on-prem mainframe. They created
  one big image with all the services and used Docker Compose to run them
  together.
  
- There are teams that use Tilt to deploy their app to prod. This is OK if
  you're getting started but we don't recommend this!!

### GitOps for WIP Development

- The JAMStack world is big on [Deploy
  Previews](https://www.netlify.com/blog/2016/07/20/introducing-deploy-previews-in-netlify/).
  Push your code to a GitHub branch and get a preview of your app. For
  sufficiently simple apps with fast deploys, you can do all your WIP
  development this way!
  
---

But sometimes the best way to learn how to use a tool is to use it incorrectly!








