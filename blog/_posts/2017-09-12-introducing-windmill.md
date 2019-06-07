---
slug: introducing-windmill
date: 2017-09-12T18:56:02.768Z
author: nick
layout: blog
title: "Introducing Windmill"
image: 1_m-VXibfLnJvJ0_uCPF17Tg.png
tags:
  - continuous-integration
  - software-engineering
  - test-automation
keywords:
  - continuous-integration
  - software-engineering
  - test-automation
---

Windmill is exploring how to make developer tools (source control, build, and test) cloud-based, simple, and easy.

### Our Product

Every good codebase we’ve worked on has a testing document:

*“If you’re working on the UI, run test suite X. If you’re working on the DB layer, run test suite Y. Running all tests in Y is slow, so use command Z to test one file. Or command ZZ to only do one test case. But don’t forget to run lint first to catch dumb mistakes. Install the linter with steps A-K.”*

Every bad codebase we’ve seen locks this in the senior developer’s head.

The product we’re building will unlock this knowledge. Every time you save, Windmill uploads your change to the cloud and immediately runs the best analysis (lint, compile, test, etc.) It gives you live, intelligent feedback that makes your inner loop tighter.

Unlike your IDE, it’s faster and deeper because it runs in the cloud.

Unlike your CI server, it’s part of your inner loop, running on each save and keeping you in flow.

Windmill uses your workflow with no extra sync or push commands. We integrate at the Unix level (filesystem and processes). We use machine learning to run the right test first so you get fast feedback. You keep your editor and our plugins pull error messages from Windmill.

### Our Hypothesis

Developers waste time waiting for their development tools.

Continuous feedback makes developers more productive.

Our product is powered by new abstractions that make it easy to build reactive developer tools. Our insight is the common shape of developer tools: they’re composed of functions over immutable snapshots of filesystem state. When you express your tool in this framework, Windmill can run your tool at the right time, in isolation and in parallel.

Our technical hypothesis is that this framework will open up new possibilities for development tools, like how MapReduce opened up data analytics, or how Deep Learning opened up AI. More cloud capacity will let developers waste less time waiting.

Our business hypothesis is that we can turn cheap cloud compute time into valuable developer productivity. We’ll have revenue and positive gross margin starting with our first customer. Customers can make their developers more productive by increasing their budget.

### Our Values

Continuous feedback makes us *all* more productive.

We want to build an organization where everyone can succeed; not just white cishet male software engineers with good pedigrees. We need to be diverse to have enough teammates and perspectives to build good products.

We’ll do the work of inclusion to help everyone succeed. We’ve started by donating every month to orgs that make tech less toxic (e.g. [Black Girls Code](http://www.blackgirlscode.com/), [Code2040](http://www.code2040.org/), [Hack The Hood](http://www.hackthehood.org/), [Project Alloy](http://projectalloy.org/)). We want to help explain why these orgs are important. We’re a partial sponsor of the diversity tickets for this year’s [GothamGo](http://gothamgo.com).

### Our Team

We’re currently tiny (two people, NYC-based, VC-backed).

We’re publishing this post because we’re looking to hire people that want to help build the next generation of tools, and figure out how to make our peers more productive.

[Dan Bentley](https://twitter.com/dbentley) — Ten years as a software engineer at Google: Google Code, Open Source Programs Office, internal build tools/continuous integration, Google Sheets. Two years on internal development tools at Twitter. $2.56 [check from Donald Knuth](https://en.wikipedia.org/wiki/Knuth_reward_check).

[Nick Santos](https://twitter.com/nicksantos) — Seven years as a software engineer at Google building consumer editing tools (Sheets, Forms) and Closure Compiler (a type checker for JavaScript). Four years at Medium, leading the implementation of its writing tools. David Carr [wrote](https://www.nytimes.com/2014/05/26/business/media/a-platform-and-blogging-tool-medium-charms-writers.html?_r=0) “[The editor] is such a pleasure to work with, Medium has become something of a pleasure object for writers.”

We saw Google change office productivity tools by building a technical foundation for cloud-based collaboration. We’d love to do that for developer tools.

Interested? Curious? [We’d love to chat](https://windmill.engineering/contact). You can find us at [Work-Bench](https://www.work-bench.com/) in New York City. Follow us [@windmill_eng](https://twitter.com/windmill_eng).

![](/assets/images/introducing-windmill/1*yD6p1m8vR9yAS8ciOzl0zQ@2x.png)
