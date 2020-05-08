---
title: Kubernetes Migration Guide
layout: docs
---

_Document outline_

## Migrating to Kubernetes
- Are you migrating to Kubernetes?
- This guide is for you.
- Tilt helps developments teams do development, that are already deploying to Kubernetes now, or are planning to do so in the future.
- Many teams focus on the production aspect of Kubernetes. They often don't realize that it has downstream impacts on development. This guides puts both together in perpsective.

## Production migration
- Here are some resources on production migration of Kubernetes.
- Tilt is not designed for deploying to production.

## Development migration
- We've seen many teams migrate to Kubernetes for production, without much thought of the impacts on development.
- In the worst case, development teams have needed to scramble to adjust existing development workflows to accommodate Kubernetes in production, on strict timelines.
- We recommend that you have a development migration plan in conjunction with your production migration plan.
- It's a best practice to decouple (as much as possible) the dev plan and the prod plan. Lots of moving pieces and inherent risk to get things working altogether at once.
- If you are the dev team, there's no need to wait for production migration. You can do development migration first, in short:

| Stage | Development | Production |
| --- | --- | --- |
| 0 | Not using Kubernetes | Not using Kubernetes |
| 1 | Using Kubernretes | Not using Kubernetes |
| 2 | Using Kubernetes | Using Kubernetes |

- As the dev team, it's also advantageous to move to a Kubernetes-aware dev workflow earlier so that you won't be locked into whatever the production migration results in.
- Tilt allows your development team to work in both stages 1 and 2.

## Start with one service for Tilt
Whether your production already uses Kubernetes or not:

- Install a Kubernetes cluster for local development.
- Install Tilt.
- Get one service working with Tilt first. Configure it so that it can talk to other services that are not yet started with Tilt.
- Ensure production deployments are working fine.
- Run things as normal for a week. Monitor for problems.
- Get the next batch of services into Tilt.
- Repeat.
