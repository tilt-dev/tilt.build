---
slug: put-down-particle-accelerator
date: 2019-09-05
author: dan
layout: blog
title: "Microservice Devs: Put Down the Particle Accelerator"
subtitle: "Pick Up The MDE Chemistry Set"
image: slac.jpg
image_needs_slug: true
image_caption: "More Science than is strictly necessary for daily work"
tags:
  - kubernetes
  - microservices
  - tilt
keywords:
  - tilt
  - development
---

## The Right Tool for the Right Job
Build tools don't work for microservices. We need a new kind of tool: the Microservice Development Engine (MDE). For decades, apps grew by building bigger binaries. So tools got better by getting faster at building big binaries. Now apps grow by adding more binaries ("microservice”), and each binary is smaller. Building each binary is easier, but requires more wrangling across binaries.

Google, Facebook and others invested Engineer-Millenia in making build tools that build huge binaries quickly, such as [Bazel](https://bazel.build) and [Buck](https://buck.build). These became big science projects delivering amazing technical achievements, comparable to building a two-mile long particle accelerator.

(Particle accelerators show up a few times in this post, so some background: atomic physics experiments smash atoms together to see what happens. The first particle accelerator had a 4-inch diameter and cost $25. Over time, physicists got more demanding. Today's best particle accelerator is [CERN](https://en.wikipedia.org/wiki/CERN): a 17 mile tunnel straddling the France-Switzerland border that cost $4.75 Billion to build.)

For most chemists, a $15 chemistry set helps more than a multi-billion dollar particle accelerator. If you want to develop microservices, a tool built for that will be better than a build tool like Bazel.

What does a Microservice Development Engine look like? It looks more like the build tools of 40 years ago: handling incremental updates to free you to focus on your app, not your build.

## Why We Use Build Tools
Stu Feldman created the first build tool, [Make](https://en.wikipedia.org/wiki/Make_(software)), to replace a script like `build.sh` because he kept making a mistake: he'd [debug the wrong code](https://www.princeton.edu/~hos/mike/transcripts/feldman.htm). After changing a file, he'd run a program only to realize it didn't even contain his change. Compiling the whole program was so slow that he'd avoid doing it by compiling just the file he'd changed. This trick is fast but dangerous: forget to compile a file and you end up with the wrong program. Make gave developers the best of both worlds: as fast as compiling just what you'd changed; as correct as a complete build.

Build tools free you from having to remember what to do after you hit save. Just run "make" (or "ant", "yarn", "bazel", etc.) and you're set. Today's build tools share this goal, and improve on Make:
* Unit-testing as a first-class feature (like `go test`)
* Dependency management and releases (like `npm update` or `mvn publish`)
* Parallel cloud builds (like Bazel's RBE)
* Automatic rebuild after hitting save (like [Webpack](https://webpack.js.org/), [Jest](https://jestjs.io/), or IDEs)

Build tools make projects more inclusive. You can contribute on day 1 without having to go to a bootcamp to learn all the dependencies of the codebase. New team members can have an  impact without having to go to a build boot camp.

## Build Tools Focus on Files
Build tool optimizations are based on a model: they're pure functions from input files to output files. This view makes caching and parallelism easy. Need to compile a file? Check if you've already compiled it, and if so, just return that output. Need to compile 100 files? Send each to a different worker in the datacenter. This model even fits unit testing: it's just generating a file that's the output of running the test binary. Getting this correct and fast takes lots of effort, but it's worth it given the productivity gains.

Build tools are particle accelerators. They're both large engineering projects that combine small pieces into progressively larger results. Compiling a C++ file with headers is like smashing protons and neutrons to create a Carbon atom. Linking many libraries to create a binary results in an Iron atom. Container images are even larger, like a Uranium atom. Want to combine files? Nothing's better.

But what about when you your operation doesn't involve a file? If you need to run a server, what's the file that's output? How do you represent seeding a running database as a file operation? If your build failed because GitHub was down while it tried to download a dependency, how do you evict that entry from the cache? "Make everything as simple as possible, but no simpler." Files are too simple for microservice dev.

## Development Today Needs New Tools
For decades, the ways apps changed fit into make's model: projects got bigger, and thus build tools got faster. The move to microservices is different: it's a change in quality, not quantity.

Microservices means your app isn't just one binary; your app (the experience your users care about) is the sum total of lots of individual binaries. Linking happens not at build-time but at run-time, over HTTP. Each individual build is smaller and faster. Starting the app is now more involved, as you have to connect all the components together in some way. You aren't delivering an atom; you're assembling a molecule.

The new layer of working with molecules introduces new workflows. For example, `kubectl log` lets you get the independent stdout/stderr for each resource as it's running. Build tools don't automate this because it doesn't fit with their model, so it's up to the developer to make sure they're looking at the right log. It's easy to forget to check every nook and cranny, so developers end up missing an error and continue on a wild goose chase.

An example of a missing tool in this new level: when I was at Google, I loved that our [monorepo](https://cacm.acm.org/magazines/2016/7/204032-why-google-stores-billions-of-lines-of-code-in-a-single-repository/fulltext) meant I could build and test any project with one command. It was cool that even though I never worked on GMail, I could refactor it easily. But if I wanted to actually change GMail, I'd have to go dig up a team-specific Wiki page or shell script that described how to start up the constituent pieces, spread across terminal tabs. Running your full app should be as easy as building a monolith.

## Microservice Development Engine: the Chemistry Set
Microservice development requires a new kind of tool: a Microservice Development Engine, or MDE. An MDE targets the same goal that first drove build tools: freeing you from remembering what to do after you hit save. New teammates should be able to ship code without learning the entire stack. We can't be sure exactly what an MDE will look like, but the history of build tools lets us make informed guesses.

Make offered a faster and more consistent experience than the `build.sh` it replaced. It was able to do better because the engine could understand the structure of the Makefile (as opposed to the imperative flow of a script).  MDEs will need a declarative description of how to build and deploy your microservice app. Because distributed systems involve the state of running services, you'll need a richer language to describe dependencies beyond the file-level data that build tools encode.

This description of your app's molecule will include how to build each component microservice's atom. Crafting a great experience at the molecular level won't leave much time to work on lower levels. The same way MDEs shouldn't write their own network stacks, a good MDE will let you use whatever build tool you already use.

MDEs will be reactive to provide the best of both IDEs and Kubernetes. Like IDEs, MDEs will watch your filesystem to upate when you save. Like Kubernetes they'll watch your cluster to respond to unexpected events. The same way Kubernetes frees you from restarting a process, MDEs free you from remembering to do a build or refresh a log.

## Early MDEs
One popular declarative description of how to build and deploy your microservice app is Docker Compose. [Docker Compose](https://docs.docker.com/compose/) is a proto-MDE: it can build and start, but won't react as you edit with incremental updates. To be clear: we love Docker Compose! It's incredibly popular, a testament to the value it delivers, and users can hack in updates via mount points. Other proto-MDEs work outside containers, like [foreman](https://github.com/ddollar/foreman), the cleverly-named go-implementetation [goreman](https://github.com/mattn/goreman), and [modd](https://github.com/cortesi/modd) offer similar functionality outside containers.

I work building [Tilt](https://tilt.dev), a Kubernetes-focused MDE. If you use Kubernetes in production, you need Tilt in development. There are other MDE projects, like [Skaffold](https://skaffold.dev), [Tekton](https://tekton.dev) (sort of an MDE), [Garden](https://garden.io), [Okteto](https://okteto.com), or [Kelda](https://kelda.io).

I'm especially proud of a few Tilt features that really exemplify what MDEs can be, how they can offer a better experience, and how Tilt's going to grow:
* The [Tiltfile](https://docs.tilt.dev/tiltfile_authoring.html) is an ergonomic way to define how to assemble the molecule of your app, from the simple (our [Write a Tiltfile Guide](https://docs.tilt.dev/tiltfile_authoring.html) highlights getting started with just Dockerfiles and Kubernetes YAML) or complex (calling out to an existing YAML generator like Helm or a custom script using [`local`](https://docs.tilt.dev/tiltfile_concepts.html)).
* [`custom_build`](https://docs.tilt.dev/custom_build.html) lets you call out to an existing build tool. (A community member was able to integrate their Bazel builds without requiring any changes to Tilt)
* Tilt's localhost Web UI is a Heads-Up Display that gives you context across your app so you see problems faster, without having to play 20 questions with Kubectl
* [Live Update](https://blog.tilt.dev/2019/04/02/fast-kubernetes-development-with-live-update.html) lets you skip image builds altogether: it updates running containers with new code, even for compiled languages.

## MDEs: the Right Tool for the Job
An MDE is going to supercharge your development in the times when you want to see and understand what's happening across your app. Tilt's still just a fraction of what it will be; if you want to help us realize this vision and have it for your inner loop, try Tilt and tell us what you think.
