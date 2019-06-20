---
slug: bazel-is-the-worst-build-system-except-for-all-the-others
date: 2018-02-01T16:04:41.722Z
author: nick
layout: blog
canonical_url: "https://medium.com/windmill-engineering/bazel-is-the-worst-build-system-except-for-all-the-others-b369396a9e26"
title: "Bazel is the Worst Build System, Except for All the Others"
tags:
  - bazel
  - developer-tools
  - build-system
keywords:
  - bazel
  - developer-tools
  - build-system
---

The Go community sometimes argues about whether Go projects should use go build or bazel build.

We talk about this at Windmill Engineering too! We’ve been trying to reconcile two statements:

1. Bazel is magic inside Google

1. Bazel is a pain to integrate in open source projects

Why?

Before we start picking apart Bazel, it’s important to frame this discussion. We love Bazel! And we think our industry has problems with [contempt culture](https://blog.aurynn.com/2015/12/16-contempt-culture). We don’t want to shame Bazel so much as open up discussion on the design decisions that Bazel made. There are zero-sum trade-offs between supporting different types of projects. Even when it’s the right trade-off to make, it’s still useful to articulate the downsides.

## What is Bazel?

If you have no idea what I’m talking about, here’s a brief explanation of Bazel. (If you’ve already used Bazel, you can skip straight to the complaining below.)

Bazel is a tool for compiling large projects with multi-language dependencies. For example, you might have a Go server that depends on generated Thrift code, or a Python server that depends on transpiled JS. To use Bazel, we write `BUILD` files that declare rules. Each rule declares a target, the rules it depends on, the input files, and the output files. That’s it!

Bazel comes with built-ins for compiling C, Java, Python, etc. It also has `genrule` for generic rules. Here’s a toy example with generic rules:

```
genrule(
  name = 'hello',
  outs = ['hello.txt'],
  cmd = 'echo hello > $(location hello.txt)')

genrule(
  name = 'hello-world',
  srcs = [':hello'],
  outs = ['hello-world.txt'],
  cmd = ('cat $(location :hello) > $(location hello-world.txt); ' +
         'echo world >> $(location hello-world.txt)'))
```


If we squint, it looks like a Makefile. The first rule `hello` creates a file `hello.txt`. The second rule `hello-world` takes the first rule as an input, and creates a file `hello-world.txt`.

You can read more about Bazel at [https://www.bazel.build/](https://www.bazel.build/).

## What’s the Matter With Bazel?

We have lots of complaints! Some are small and fixable. Some are big and unfortunate.

### Depends on the Java Runtime

I can’t believe it’s 2018 and managing a local Java installation is still painful.

### No Easy Way to Version Bazel Itself

At my last job, one of the most common build errors was “you have the wrong version of Bazel.” We had to add a wrapper script around the build process that checked that you had the right version installed.

### Distributed Builds

Google has a distributed build cluster! Slow builds can be parallelized! If two people are building the same file, they can share the same results!

Bazel-team wrote [instructions](https://docs.bazel.build/versions/master/remote-caching.html) on how to run a build cache yourself. It’s non-trivial. Bully for you if you have a dedicated Ops team to run and maintain your build cluster.

### Explicit Dependency Bookkeeping

Bazel assumes we live in a world where we don’t know where our dependencies live on disk. We have to explicitly list them.

Meanwhile, modern languages have become super opinionated about where dependencies live! Go wants all your code in a rigidly formatted `src` [tree](https://golang.org/doc/code.html#Workspaces). Our imports are paths into that tree. Rust and Maven have a local dependencies registry. NodeJS wants your dependencies to live in a relative `node_modules` directory.

The big idea is that we can read the source file and automatically figure out where the dependencies live. Bazel doesn’t exploit this information. It wants a strict separation between dependency information from the code. There are projects that [auto-generate Bazel rules](https://github.com/bazelbuild/rules_go#generating-build-files), but they don’t integrate cleanly with the rest of the tooling.

### Step 1 to Adopting Bazel: Boil the Ocean

Bazel needs to know all the inputs and outputs of rules. The flip side of this is that to adopt Bazel, we need to give it a total description of our build process. It does not have good integration points for inter-operating with other build systems, or for “partial” adoption.

I’m conflicted about this! Walled gardens are nice. You can guarantee that everything in the garden is pretty and well-groomed. It’s nice that there’s a wall to keep you inside and protect you from O(n²) performance problems.

On the flip side, my friend Jason likes to say that the optimal time to adopt Bazel is before you need it. If you try it early, it doesn’t give much value. If you try it later, the migration is a massive engineering project.

### Declarative Programming Languages are Hard To Debug

Bazel’s configuration is “declarative-ish.” The BUILD files declare rules in a build graph. There are ways to break out into imperative code, but most configuration is declarative.

We are still not good at building debuggers for declarative languages. CSS is the example that proves the rule: it took decades for good CSS debuggers to come out. CSS is still a struggle for many.

Too much of the Bazel configuration forces you to visualize build graphs in your head.

### Local Build Systems are Inherently A Pain

This reminds me of a great joke:


Running a local hermetic build system is like being a doctor in a medical drama, but you have the same infection and everything you do re-infects the patient.

Any engineering team with more than a few people needs processes to make sure that everyone has the same tools installed. Woe be to you if you install something to make the build work, but forget what you did.

Bazel tries to sandbox your build process to help make the build hermetic and reproducible across computers. But the sandboxing primitives are OS-specific and sometimes leaky. It’s often hard to debug things inside the sandbox.

## How Do We Fix These Problems?

We don’t know! But we have a lot of ideas. Windmill is starting from a couple axioms:

1. The build servers in the future will look like the git servers of today. Many novices use git. You can certainly run your own git server, but most people use a hosted provider.

1. The build language of the future will be imperative. Novice programmers should be able to pick it up easily. The language should help them to visualize the results.

1. Any build system in widespread use must be easy to use incrementally and on small projects. It should integrate with other build tools, so that you can start seeing value without days or weeks of effort.

What other pains have you felt with Bazel? What do you think build tools will look like in five years? If you’re interested in exploring these problems with us, [we’d love to chat](https://windmill.engineering/contact/).
