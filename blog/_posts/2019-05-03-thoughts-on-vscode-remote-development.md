---
slug: thoughts-on-vscode-remote-development
date: 2019-05-03T00:09:30.481Z
author: nick
layout: blog
title: "Thoughts on VSCode Remote Development"
subtitle: "Can we stop reinventing version managers now?"
tags:
  - docker
  - kubernetes
  - vscode
  - containers
  - local-development
keywords:
  - docker
  - kubernetes
  - vscode
  - containers
  - local-development
---

Yesterday, the VSCode team announced a pack of Remote Development extensions. You can now edit code directly inside a container 😍. I have Thoughts.

Read more here: [**Remote Development with Visual Studio Code**](https://code.visualstudio.com/blogs/2019/05/02/remote-development)

I’ve spent the last few years focused on smoothing and optimizing the microservice dev experience. This launch dovetails with some trends:

First, it’s clear to me that the future of software development is going to happen inside containers.

We’ve been seeing this trend for a while now. Every modern language reinvents sandboxing. Python has `pyenv`. Node has `nvm`. Ruby has `rvm`.

From the VSCode announcement: “we hesitate to try out a new stack like Rust, Go, Node, or Python3, for fear of ‘messing up’ our current, well-tuned environment.”

**The community is crying out for a general-purpose sandbox dev env.** Containers have potential, but the developer experience is still finicky and unstable.

The [`devcontainer.json` API reference](https://code.visualstudio.com/docs/remote/containers#_devcontainerjson-reference) is a cool start. Auto-port-exposing! Docker-compose files! I’m excited to see how this develops.

I’ve learned a lot from the teams that are pioneering this workflow. Some foreshadowing on what comes next:

1. **There is no such thing as a “standard” development environment.** Even very small teams have to hack in plugins to make their chosen combination of tools work. Will `devcontainer.json` have a plugin ecosystem?

1. **Docker-compose is a great file format, but the runtime engine is on its way out.** Teams hate having separate docker-compose and k8s configs that work differently. What will replace it as the go-to for dev envs?

1. **More services == more containers.** VSCode says: “Currently you can only connect to one container per VS Code window.” No one wants to have 5 windows open to understand their service.

1. **As development environments get more complicated, teams need tools to test them.** Will there be a `devcontainer.json` test framework? Will a DevOps engineer be able to do staged rollouts to the team, or help debug env problems?

The VSCode team is doing exciting work here. And there are so many problems left to solve! If these extensions can deliver on the promise of making in-container editing as seamless as local editing, this will be a huge step forward.

<hr>

*Obligatory log rolling: If your team deploys to Kubernetes and you’re looking to make local development fun again, check out [Tilt](https://tilt.dev/)!*
