---
slug: how-to-compile-protobufs-when-you-have-friends-who-want-to-use-them-too
date: 2018-10-01T21:19:26.715Z
author: nick
layout: blog
canonical_url: "https://medium.com/windmill-engineering/how-to-compile-protobufs-when-you-have-friends-who-want-to-use-them-too-b76d7fdc247e"
title: "How to Compile Protobufs When You Have Friends Who Want to Use Them Too"
tags:
  - docker
  - protocol-buffers
  - protobuf
  - grpc
  - software-development
keywords:
  - docker
  - protocol-buffers
  - protobuf
  - grpc
  - software-development
---
  
I love GRPC, but hate compiling protobufs.

Protobufs make me feel productive! I can write a small `.proto` file that describes my interface. The protobuf compiler will generate all the client/server code that I need.

When I want to introduce protobufs into a codebase, I start with a Make rule:

```
proto:
  protoc --go_out=plugins=grpc:../../../ -I. proto/*.proto
```


Whenever I change the proto file, I run `make proto` and commit the generated code into git.

This works when you have no friends! When I do bring friends onto my project, that’s when the complaining begins:

* How do I install `protoc`?

* Ugh, it doesn’t work, I also need to install the Go `protoc` plugin!

* Wait, why did all the generated code change when I ran it on my machine?

* Oops, it’s because I installed the wrong version of `protoc`! Do we all need to be on the same version?

* Agh, the Go `protoc` plugin instructions only tell me how to install HEAD, how do I install a fixed version?

* Why are we on such on old version? How do I upgrade without breaking everyone?

It adds work to each new team member onboarding. And coordinating upgrades is A Big Event.

### How do we compile protobufs consistently?

One way to fix this is to switch to a hermetic build system with protobuf support, like Bazel. But you’d have to rewrite your build system, which is a drag.

Instead, we wrote a little shell script to compile the protobufs inside a Docker container. The Dockerfile looked something like this:

```
# Dockerfile.protogen
FROM golang:1.11

ENV PROTOC_VERSION 3.6.1
ENV PROTOC_GEN_GO_VERSION v1.2.0

RUN something something install protoc
RUN something something install protoc-gen-go

WORKDIR /go/src/github.com/windmilleng/tilt

COPY my.proto my.proto
RUN protoc --go_out=plugins=grpc:../../../ -I. my.proto
```


The Makefile rule turned into this:

```
proto:
  docker build -t protogen -f Dockerfile.protogen
  docker run --name protogen protogen
  docker cp protogen:/go/src/github.com/windmilleng/tilt/my.pb.go ./
  docker rm protogen
```


That worked fiiiine…for a while. It was finicky when adding new `.proto` files. It wasn’t easy to share across projects.

### Making this pattern reusable

We wrote a small python script to help us apply this pattern in multiple projects.

We thought about calling it GRIND (“GRpc IN Docker”). But that would be silly. Instead we call it `protocc`.

[windmilleng/protocc - Compile protobufs (protoc) inside a container (protocc)!](https://github.com/windmilleng/protocc)

Just copy `protocc.py` and run:

```
python protocc.py --out go
```


to run `protocc` inside a container in your own repo. No need to install `protoc` or manage `protoc` plugins yourself!

It currently only generates Go code. If this sounds like something you want for your target language, [let us know](https://github.com/windmilleng/protocc/issues) and we’d be happy to add it!
