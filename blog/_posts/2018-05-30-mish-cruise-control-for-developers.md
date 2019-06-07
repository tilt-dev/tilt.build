---
slug: mish-cruise-control-for-developers
date: 2018-05-30T06:47:55.083Z
author: dan
layout: blog
title: "mish&#58; cruise control for developers"
image_caption: "mish in action"
image: "1_5SyGWMKZ3wyZq_iNOp2g_g.gif"
tags:
  - devops
  - shell
  - development
  - golang
  - python
keywords:
  - devops
  - shell
  - development
  - golang
  - python
---

Our next Windmill experiment is [live](https://github.com/windmilleng/mish). `mish` is a terminal app that automates your development loop. `mish` watches your files, reruns commands, and displays the output. Refining the commands as your workflow changes is easy and ergonomic.

`mish` is cruise control for developers. It takes minutes to start using it. It automates the repetitive so you can focus on the important. Keep your eyes on the road/code. Stay in [Flow](https://en.wikipedia.org/wiki/Flow_(psychology)).

## Why Automate

Navigating through shell history isn’t hard, but it is unnecessary. Our commands are repeated because we’re in an edit-compile-test(-restart-etc.) loop. Contorted key combos, even when etched in muscle memory, take effort and steal attention in the best case.

In the worst case, they waste time. Like when you spend 5 (15? 30?) minutes figuring out why your code is having no effect, only to realize you were building the wrong binary.

Computers perform rote steps accurately and quickly. `mish` makes you more productive during the day, and less exhausted at the end of it.

## What’s New

[Autorunning](https://github.com/emcrisostomo/fswatch) [tools](https://www.emacswiki.org/emacs/FlyMake) [exist](https://marketplace.visualstudio.com/items?itemName=gabrielgrinberg.auto-run-command), but the number of people who use them rounds to 0. (Heck, I don’t use them.) Why is `mish` different?

It recognizes that your workflow is dynamic: you futz with a flag or change the set of packages under test. Autorunning tools are meant to keep you in Flow, but refinement requires stopping, editing an invocation, and restarting. Cruise control needs a dial that can be tuned after ignition.

`mish` can be tuned by editing a file instead of a command-line. A `Millfile` is easy and fun to refine because it’s a program in the Mill language.

## Mill: a Language for Refinement

Mill is a dialect of Python (built with`[skylark`](https://github.com/google/skylark), a great Python interpreter) that makes scripting dev workflows easy. A new configuration language can be intimidating. Let’s look at a useful `Millfile`:

```
sh("go test -v ./pkg/foo") # run a unit test
```


That’s it!

The [README](https://github.com/windmilleng/mish) describes growing your `Millfile`. You can run multiple commands, or watch/ignore files that trigger runs.

Because Mill deals with commands, not libraries, it works with any language, testing framework, or backend.

## It’s Dangerous to Go Alone; Take Mi(chel)

![Bonjour! Je m’appelle Michel](/assets/images/mish-cruise-control-for-developers/1_KbCt7S4W2Eh8EK7mqor4Pg.png)*Bonjour! Je m’appelle Michel*

Adopting a new tool, especially a CLI, is intimidating because so many are so inscrutable. `mish` means to break that trend. It offers a contextual help bar in the footer. And a mascot!

`mish` is also short for “Michel”. Every hermit crab has to find a shell to live in; Michel picked yours. Over time, expect Michel to make more appearances; DevTools don’t have to be soulless. We hope Michel makes you smile, and they make your workflow more enjoyable. (yes, “they”; `mish` is a binary but Michel is [non-binary](https://en.wikipedia.org/wiki/Genderqueer))

## The Earliest of Days

We started coding `mish` 2 weeks ago. We’re sharing it this early because our mission is fast feedback. We think this primordial state can get you fast feedback about your code. And we hope it can get us fast feedback about our hypothesis.

Sounds compelling? Or mildly intriguing? Or even totally wrong-headed? Great!

* [Get `mish` from github](https://github.com/windmilleng/mish)

* 15 minutes of setup

* A day or two of developing as it runs in the background

* 20 minutes to [tell us how it feels](https://docs.google.com/forms/d/e/1FAIpQLSf8UXLG0FOeMswoW7LuUP02CeUwKBccJishJKDE_VyOqe7g_g/viewform?usp=sf_link). Better? Worse? Bugs getting in the way of the vision? Let us know.
