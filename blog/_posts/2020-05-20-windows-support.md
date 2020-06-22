---
slug: "windows-support"
date: 2020-05-20
author: nick
layout: blog
title: "Tilt Windows Support"
image: "/assets/images/windows-support/windows.jpg"
image_caption: "A perfect illustation of Windows support.<br>George Arents Collection, The New York Public Library. <em>Protecting your windows - a sandbag defence</em>.<br>Retrieved from <a href='http://digitalcollections.nypl.org/items/510d47da-9591-a3d9-e040-e00a18064a99'>http://digitalcollections.nypl.org/items/510d47da-9591-a3d9-e040-e00a18064a99</a>"
tags:
  - tilt
  - windows
---

Historically, Tilt has supported multi-service dev on Linux and macOS.

Some of our users hacked it to work on Windows anyway. A few pro-active
contributors even sent us PRs occasionally to fix Windows bugs ❤. Parts of
Tilt worked well. Other parts didn't.

So we're positively chuffed to announce full Windows support!

## What Does That Mean Exactly?

We're not saying we'll never have Windows bugs.

We are saying:

- Our core language examples in 
  {[Python](https://github.com/tilt-dev/tilt-example-python), 
   [NodeJS](https://github.com/tilt-dev/tilt-example-nodejs), 
   [Go](https://github.com/tilt-dev/tilt-example-go), 
   [Java](https://github.com/tilt-dev/tilt-example-java), 
   [C#](https://github.com/tilt-dev/tilt-example-csharp)} 
  work on Windows.
- Every Tilt change runs our tests on Windows.
- We maintain binaries and installers for Windows for [every Tilt release](https://github.com/tilt-dev/tilt/releases).

In other words, Windows is now a first-class citizen alongside Linux and macOS.

Install it with:

```powershell
iex ((new-object net.webclient).DownloadString('https://raw.githubusercontent.com/tilt-dev/tilt/master/scripts/install.ps1'))
```

## Why was this hard?

If you're on a devtools team, you may wonder what it takes to get a tool to work on Windows
in 2020. We're glad you asked! 

- Even though Tilt is running on Windows, it's building and syncing files to
  Linux containers [^1].  Everywhere we handled file paths, we needed to keep
  track of whether it was on the host machine (Windows) or the target container
  (Linux) and translate correctly.

- Tilt wrangles local servers, local build jobs, and Kubernetes containers into
  a coherent dev environment.  Local process management is OS-specific, so we
  tweaked how we used process APIs to ensure Tilt doesn't leave orphaned
  processes around when it dies.

- The Tiltfile lets you integrate with your existing scripts with
  [`local()`](https://docs.tilt.dev/api.html#api.local),
  [`local_resource()`](https://docs.tilt.dev/api.html#api.local_resource), and
  [`custom_build()`](https://docs.tilt.dev/api.html#api.custom_build).  We added
  options to specify separate shell and Windows batch scripts.
  
- Cross-platform Go libraries like
  [fsnotify](https://github.com/fsnotify/fsnotify) (for file-watching) and
  [tcell](https://github.com/gdamore/tcell) (for terminal UI rendering) were an
  enormous help.  But they're not perfect abstractions. In a few places, we had
  to dig into the underlying Windows APIs, and change how we were using them to
  better align with how Windows works.

## Why was this easy?

We also want to shout out to some of the great devtools that 
made this easier than we expected 🙌:
  
- [Docker for Windows](https://docs.docker.com/docker-for-windows/) seems to get
  better every month.  We're particularly excited for the [WSL2
  backend](https://www.docker.com/blog/new-docker-desktop-wsl2-backend/).

- [Goreleaser](https://goreleaser.com/) made cross-compiling Windows binaries a
  breeze.

- [Scoop](https://scoop.sh/) is a package manager that lets you manage tools
  without annoying permissions dialogs. [Tilt's install
  script](https://docs.tilt.dev/install.html#windows) will use Scoop if it's
  available.
  
- [CircleCI Windows
  Support](https://circleci.com/blog/windows-general-availability-announcement/)
  was a huge help - just getting all our tests to pass on Windows fixed most of
  the bugs.
  
Thanks to all of these projects!

## What's next?

If you're a Windows user who passed on Tilt on the past, or have been using it
on WSL, now's a great time to pick it up again!

[Let us know](https://tilt.dev/contact) how we can make Tilt better for Windows.

[^1]: Tilt does not (yet) support Windows-based containers, mostly because no one's asked for it yet! We would need to do some work to make sure all Tilt primitives (like live-reload) work inside a Windows-based container.
