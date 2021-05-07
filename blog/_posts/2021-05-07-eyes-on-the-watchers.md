---
slug: "eyes-on-the-watchers"
date: 2021-05-07
author: nick
layout: blog
title: "Eyes on the Watchers"
subtitle: "Introducing the Tilt FileWatch API"
image: "/assets/images/eyes-on-the-watchers/statue.jpg"
image_caption: "'Someone placed googly eyes on our historic #NathanaelGreene statue in #JohnsonSquare.'. Via <a href='https://www.facebook.com/cityofsavannah/posts/10161094314505525'>The City of Savannah</a>."
tags:
  - api
  - filewatch
---

I've been writing Makefiles almost two decades. And I still struggle to debug two classic problems:

- I changed a file. Why didn't Make rebuild the stuff that depends on it?

- Nothing changed. Make rebuilt all my stuff anyway. Why didn't Make cache it?

And it's not just because Make is old. Even new technology has this problem! We still see people 
go through the same pain with Docker builds:

- I changed a file. Why did Docker ignore it?

- Nothing changed. Why did Docker rebuild all the layers?

The devtools community has made great breakthroughs in fancy file ignore
patterns in the last two decades!  But still don't have standard ways to debug
them to help test if they're working.

At Tilt, we've been trying to be mindful about this problem, and what we can do
to make sure we don't fall into the same trap. I want to use this post to explore
some of what we've built, and how to use it.

## Reading FileWatches

Tilt now runs an API server to help debug status and stitch together state.

One of the first things we added is a general-purpose [FileWatch
API](https://api.tilt.dev/core/file-watch-v1alpha1.html).

Anytime you run Tilt, you can inspect all the files it's watching.

```shell
$ git clone git@github.com:tilt-dev/tilt-example-html
Cloning into 'tilt-example-html'...
$ cd tilt-example-html/0-base
$ tilt up &
$ tilt get filewatches
NAME                       CREATED AT
configs:singleton          2021-05-04T22:00:32Z
image:example-html-image   2021-05-04T22:00:32Z
```

In this example, Tilt has two filewatches: one for reloading the Tiltfile
("configs:singleton"), and one for rebuilding the Docker image
("image:example-html-image").

Let's unpack those filewatches in more detail.

```shell
$ tilt get filewatches configs:singleton -o yaml
apiVersion: tilt.dev/v1alpha1
kind: FileWatch
metadata:
  annotations:
    tilt.dev/target-id: configs:singleton
  creationTimestamp: "2021-05-04T22:00:32Z"
  name: configs:singleton
  resourceVersion: "1"
  uid: 86e69fd0-c2e0-41f1-99ab-2c307c8a9e27
spec:
  watchedPaths:
  - /home/nick/src/tilt-example-html/0-base/.dockerignore
  - /home/nick/src/tilt-example-html/0-base/.tiltignore
  - /home/nick/src/tilt-example-html/0-base/Dockerfile
  - /home/nick/src/tilt-example-html/0-base/Tiltfile
  - /home/nick/src/tilt-example-html/0-base/kubernetes.yaml
status:
  lastEventTime: null
  monitorStartTime: "2021-05-04T22:00:32.286554Z"
```

When I print the full specification, I can see that we're watching 5 files. But
we haven't seen any changes yet.

Let's touch one of the files and see what happens:

```shell
$ touch /home/nick/src/tilt-example-html/0-base/Tiltfile
$ tilt get filewatches configs:singleton -o yaml
apiVersion: tilt.dev/v1alpha1
kind: FileWatch
metadata:
  annotations:
    tilt.dev/target-id: configs:singleton
  creationTimestamp: "2021-05-04T22:00:32Z"
  name: configs:singleton
  resourceVersion: "4"
  uid: 86e69fd0-c2e0-41f1-99ab-2c307c8a9e27
spec:
  watchedPaths:
  - /home/nick/src/tilt-example-html/0-base/.dockerignore
  - /home/nick/src/tilt-example-html/0-base/.tiltignore
  - /home/nick/src/tilt-example-html/0-base/Dockerfile
  - /home/nick/src/tilt-example-html/0-base/Tiltfile
  - /home/nick/src/tilt-example-html/0-base/kubernetes.yaml
status:
  fileEvents:
  - seenFiles:
    - /home/nick/src/tilt-example-html/0-base/Tiltfile
    time: "2021-05-04T22:04:09.056840Z"
  lastEventTime: "2021-05-04T22:04:09.056840Z"
  monitorStartTime: "2021-05-04T22:00:32.286554Z"
```

The file watch status field is immediately updated with the file change. Other
objects in Tilt read this change to figure out whether to reload.

## Hacking FileWatches

Reading APIs is boring. Let's make some changes.

The `tilt edit` command lets us change file watches on the fly.

```
$ EDITOR=emacs tilt edit filewatch configs:singleton
```

![Emacs, the best editor for filewatches](/assets/images/eyes-on-the-watchers/editor.jpg)

I'm going to go ahead and remove all the files.

Now, when I touch the Tiltfile again, nothing reloads:

```
$ touch /home/nick/src/tilt-example-html/0-base/Tiltfile
$ tilt get filewatches configs:singleton -o yaml
apiVersion: tilt.dev/v1alpha1
kind: FileWatch
metadata:
  annotations:
    tilt.dev/target-id: configs:singleton
  creationTimestamp: "2021-05-04T22:00:32Z"
  name: configs:singleton
  resourceVersion: "5"
  uid: 86e69fd0-c2e0-41f1-99ab-2c307c8a9e27
spec:
  watchedPaths:
  - /home/nick/src/tilt-example-html/0-base/.dockerignore
status:
  lastEventTime: null
  monitorStartTime: "2021-05-04T22:08:23.820911Z"
```

`tilt edit` is a convenient way to debug file watch problems. I sometimes turn file watches
off if I don't want them to trigger reloads. Or I add new ignore patterns to test them.

When I reload the Tiltfile (e.g., by clicking the reload button in the Tilt UI),
Tilt will regenerate all the file watches from scratch, blowing any of my
temporary edits away.

## More Fun with File Watches

In a future blog post, we'll show how to stitch this together with
other [API types](https://api.tilt.dev/) to trigger reloads of anything.

Our docs have [much more detail](https://docs.tilt.dev/file_changes.html) on the
kinds of file watches Tilt sets up for each resource type by default, and how to tweak the
ignore patterns.

But reading docs is way slower and less fun than breaking things to see what happens 😈.





