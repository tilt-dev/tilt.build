---
slug: "entr-the-dragon"
date: 2021-05-18
author: nick
layout: blog
title: "Draggin' the Entr"
subtitle: "A brief love letter to 'entr'"
image: "/assets/images/entr-the-dragon/two-buttons.jpg"
tags:
  - api
  - entr
---

`entr` stands for Event Notify Test Runner.

It's a  command line tool that makes it easy to re-run tests and live reload servers.

You give `entr`:

1) A list of files

2) A command to run

`entr` listens to those files and restarts the command when they change. You can
trigger restarts manually by pressing [spacebar].

`entr` is so simple and Unix-y, it's hard to believe someone didn't come up with
it at Bell Labs in the 70s. But it's actually a pretty recent tool that [Eric
Radman first released in
2012](https://github.com/eradman/entr/blob/master/NEWS).

This post is a brief love letter to `entr`: what its options are, why they're
there, and how to build a similar experience on top of the Tilt API once your
logic gets too complex for `entr`.

We will also have some good `entr` puns!

## `entr` the Options

The old rule of thumb of bodegas is that every sign behind the cash register
has a great story where someone tried to do something so ridiculous that they
had to post a sign to prevent it from happening again.

I feel the same way about `man` pages! And the `entr` manual is no exception.

The `entr` [manual](http://eradman.com/entrproject/entr.1.html) is a history of
all the reasons why a command re-runner might seem simple but is more
complicated than you would expect. Here's an abridged version of how that manual
reads to me:

> `-a`: What happens if to the command writes to a file that makes the command
> restart? You don't really want infinite loops...or do you?

> `-d`: Can new files trigger commands?

> `-p`: OK, I get how restarts are triggered, but what triggers the initial start?

> `-r`: Are servers and test commands the same? Or are they fundamentally
> different and need different restart behavior? What about subprocesses?

> `-z`: Does it really make sense to restart a server that's crashing?

These are all good questions! And how you answer them can have a big impact on how you 
run `entr`.

### Example #1: fast iterative testing

For day-to-day running of unit tests, something like

```
find pkg/model | entr go test ./pkg/model/...
```

does what I need. `find pkg/model` lists all tests in that directory. `entr`
reruns the test when any of them change.

### Example #2: reload a server

We use `entr` in Tilt for restarting servers! You can read the full script [in
our `restart_process`
extension](https://github.com/tilt-dev/tilt-extensions/blob/master/restart_process/tilt-restart-wrapper.go#L1).

A simpler version of this script looks like:

```
echo /.restart-proc | entr -rz run-server
```

with some custom handling of exit codes when the server is crashing. Then Tilt
can touch the `/.restart-proc` file to trigger a restart.

## Speak, Friend, and `entr`

For even more complex logic, Tilt has a [FileWatch
API](https://api.tilt.dev/core/file-watch-v1alpha1.html) and a [Cmd
API](https://api.tilt.dev/core/cmd-v1alpha1.html) that you can stitch together
to build `entr`-like reloading.

Let's reimplement our test re-runner above on the Tilt API.

```
find pkg/model | entr go test ./pkg/model/...
```

First, start a Tilt server for your project's dev environment:

```shell
tilt up &
```

Then run three lines:

```shell
tilt create filewatch pkg-model ./pkg/model
tilt create cmd --filewatch=pkg-model pkg-model-test go test ./pkg/model/...
tilt logs -f
```

Let's break down these lines one at a time.

### create filewatch

The first line creates a filewatch object.

```
$ tilt create filewatch pkg-model ./pkg/model
filewatch.tilt.dev/pkg-model created
```

Because a filewatch is a full-fledged Tilt API object, I can inspect it directly
to make sure it's working.

```shell
$ tilt get filewatch pkg-model
NAME        CREATED AT
pkg-model   2021-05-12T23:42:20Z

$ touch pkg/model/secret.go

$ tilt describe filewatch pkg-model
Name:         pkg-model
Namespace:    
Labels:       <none>
Annotations:  <none>
API Version:  tilt.dev/v1alpha1
Kind:         FileWatch
Metadata:
  Creation Timestamp:  2021-05-12T23:42:20Z
  Resource Version:    4
  UID:                 9c3a72df-18e5-4ea7-9ea5-4dcffa305667
Spec:
  Watched Paths:
    /home/nick/src/tilt/pkg/model
Status:
  File Events:
    Seen Files:
      /home/nick/src/tilt/pkg/model/secret.go
    Time:              2021-05-12T23:42:27.064831Z
  Last Event Time:     2021-05-12T23:42:27.064831Z
  Monitor Start Time:  2021-05-12T23:42:20.056037Z
```

For more on how to inspect Tilt's file watches, see [this post](/2021/05/07/eyes-on-the-watchers.html).

### create cmd

The second line creates a command that restarts whenever the FileWatch sees new events.

```
$ tilt create cmd --filewatch=pkg-model pkg-model-test go test ./pkg/model/...
cmd.tilt.dev/pkg-model-test created
```

Cmd is also a first-class Tilt API object, so we can inspect it:

```
$ tilt describe cmd pkg-model-test
Name:         pkg-model-test
Namespace:    
Labels:       <none>
Annotations:  <none>
API Version:  tilt.dev/v1alpha1
Kind:         Cmd
Metadata:
  Creation Timestamp:  2021-05-12T23:45:53Z
  Resource Version:    3
  UID:                 7c0645ce-ca60-4849-910a-f44cd9d733f2
Spec:
  Args:
    go
    test
    ./pkg/model/...
  Dir:  /home/nick/src/tilt
  Restart On:
    File Watches:
      pkg-model
Status:
  Ready:  true
  Terminated:
    Exit Code:    0
    Finished At:  2021-05-12T23:45:54.911704Z
    Pid:          1032214
    Started At:   2021-05-12T23:45:53.915968Z
```

In this example, I can see that the command immediately ran in about 1 second.

### logs -f

The third line tails the Tilt logs. 

The `-f` argument streams the logs and waits for new logs.

To put it all together, I can delete a file and look at the logs to see the
result of the command re-run:

```
$ rm pkg/model/secret.go

$ tilt logs | tail
Running cmd: go test ./pkg/model/...
# github.com/tilt-dev/tilt/pkg/model/logstore [github.com/tilt-dev/tilt/pkg/model/logstore.test]
pkg/model/logstore/logstore.go:237:51: undefined: model.SecretSet
pkg/model/logstore/logstore.go:246:48: undefined: model.SecretSet
pkg/model/logstore/logstore_test.go:122:15: undefined: model.SecretSet
ok  	github.com/tilt-dev/tilt/pkg/model	(cached)
FAIL	github.com/tilt-dev/tilt/pkg/model/logstore [build failed]
FAIL
go test ./pkg/model/... exited with exit code 2
```

Tilt immediately ran the tests, which failed, because the symbols
defined in `secret.go` are missing.

And with only three lines of `tilt` invocations, we recreated our `entr` one-liner.

## `entr` Stage Right

I honestly think `entr` should be a go-to tool for anyone that messes around
a lot in the terminal.

We don't want Tilt to replace `entr`! But we think it can complement `entr` when
you're ready to move from hackable one-offs to composable systems.

One of the goals we're trying to accomplish with the Tilt API server is to have
a more robust, Kubernetes-inspired API for building dev environments. It will definitely
be more verbose than `entr`! But it will also be more debuggable and maintainable
for the next person on your team.
