---
slug: whats-easier-than-clicking-run-test-not-clicking-it
date: 2018-05-22T15:48:40.809Z
author: dmiller
layout: blog
title: "What’s Easier than Clicking “Run Test”? Not Clicking It."
images:
  - 1*KMMk--1EiY0CwrGZC-QJgA.gif
  - featuredImage.gif
tags:
  - testing
  - vscode
  - golang
keywords:
  - testing
  - vscode
  - golang
---

Have you ever been banging your head against the wall, trying to get that one test to pass? It can be frustrating to make a small tweak in your editor and then have to switch to a terminal to run the test, over and over again. VS Code makes this easier by offering CodeLenses to run tests right in the editor.

But it’s not live. It’s not responsive. We believe your tools should know what you’re working on. They should give you relevant feedback before you ask for them.

Windmill is running some small experiments on how to make your existing devtools more alive. We’re starting with Go testing in VSCode.

### Autotest for Go

Introducing [Go Autotest for VS Code](https://marketplace.visualstudio.com/items?itemName=windmilleng.vscode-go-autotest#overview)! Go Autotest automates the running of your Go tests so you can spend less time turning the crank and more time building things. It does this through two features: autorun and test pinning.

Autorun is simple: every time you open a Go file that contains tests the extension will run those tests in the background and provide the result as a CodeLens atop the test function.

![](/assets/images/whats-easier-than-clicking-run-test-not-clicking-it/1*KMMk--1EiY0CwrGZC-QJgA.gif)

Test pinning allows you to focus on just one test and see the new result immediately on save of any file. This is useful when you’re just trying to get that *one pesky test* to pass*.*

![](/assets/images/whats-easier-than-clicking-run-test-not-clicking-it/1__jKIdDTho2gaznMzy-7fQg.gif)

### Become a fan

At Windmill Engineering we want to make developer tools (build, source, and test) cloud-based, simple, and easy. We don’t entirely know what that means yet! We’re still building it. Go Autotest is the first of several experiments we will run aimed at improving developers workflows. If this mission excites you, or you want to try future experiments, consider becoming a [fan](https://medium.com/@dbentley/a4c0066c356d)!
