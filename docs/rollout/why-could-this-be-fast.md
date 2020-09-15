---
title: Why Could This Be Fast?
layout: rollout
---

Identify the most severe issues and find easier solutions to them by framing conversations with AppDev. When a user complains that something is slow, ask "Why Could This Be Fast?". This lens focuses users on explaining a mental model they have that you may not (e.g. because you don't perform that operation that frequently).

It's tough to choose which issues to work on. You can't just drop everything when a user says something is too slow: users always want faster tooling, so it's not a useful signal. It's easy to get so calloused to user feedback that you miss the issues that lose users' trust and hinder adoption.

## Obviously Wrong Behavior
This tip is best for understanding certain kinds of issues: when the tooling is "obviously wrong". What's obviously wrong? It's something taking 2 minutes when it could take 2 seconds. Or having to always perform a manual step when it should be automatic.

Obviously Wrong behavior wastes time, but worse: it destroys trust. If a tool can't see it can reuse the last build, why should I trust it for anything else?

This tip won't help you identify across-the-board slowdowns. You won't find a 10% improvement in all parts of the system this way. But you will find a pathological corner case that's so irritating that users looked away. This is especially useful when the user is doing work that you don't personally do.

You can find easy improvements to Obviously Wrong behavior. You can make a special case that applies only to the broken corner case, which is often easier to implement than a general solution.

## Breaking the Logjam

Frustrated users often have a good basis for being frustrated, but that frustration can get in the way of communicating that reason. Asking "Why Could This Be Fast?" helps you both focus on potential improvements.

For example, say a frustrated user complains "this build is taking 2 minutes". It's hard to know what to do with that: Scala users might be thrilled if their build only took 2 minutes. So you ask "why could it be faster?" When the user says "builds shouldn't have to download any dependencies when I don't change the set of dependencies", you go to the Dockerfile and improve caching.

Eliciting the user's intuition illuminated how to fix it.


## Stay with "Why", now "How"

A similar question is "How Could This Be Fast?", but asking that has a problem.  Frustrated users can quickly move to designing solutions. Their proposed solutions may be impractical because they ignore other constraints. And it may not be clear what elements of their proposal are really necessary to solve their problems.

Asking "Why" keeps the focus on them sharing their mental model, and leaves the solving to you. Even when you're open to their assistance, it's good to make sure you understand the problem well enough to evaluate solutions. That way, if you have an idea you'll be able to understand if it will help without having to wait to talk again (or worse, find out it doesn't adress the issue only after you've already implemented it).

## Evaluation

**Use this if** users complain that Tilt is slow. Tilt should be able to be as fast as your existing system when it's doing the same work.

**Skip this if** you are also an AppDev and experience all of the use cases.

**You know it's successful when** you can fix an issues that's been complained about many times with just an afternoon of coding because you understand the problem more completely.
