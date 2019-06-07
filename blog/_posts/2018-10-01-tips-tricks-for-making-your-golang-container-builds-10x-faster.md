---
slug: tips-tricks-for-making-your-golang-container-builds-10x-faster
date: 2018-10-01T20:09:54.364Z
author: nick
layout: blog
title: "Tips & Tricks for Making Your Golang Container Builds 10x Faster"
tags:
  - docker
  - golang
  - containers
  - build-tool
keywords:
  - docker
  - golang
  - containers
  - build-tool
---

A couple weeks ago, I was wrestling with a bug.

Maybe you’ve had a night like this. I was tired, cranky. I probably should have taken a nap. But I felt like I was on the precipice of figuring it out.

I Googled around for tools that might help. And I found one! But it didn’t compile on the version of Go I was using. What should I do?

<p>1. Try installing a different version of Go, but risk hosing my machine and getting into an even more broken state</p>

<p>Try fixing the tool to compile on my version of Go</p>

But then I realized I have a third option! An option that makes upgrading libraries safe again!!

<p>3. Build everything in a container</p>

Yessssssss.

Now I’m developing in a container. I can switch versions of Go safely. I can try out alpha versions of packages without accidentally breaking other tools. It feels like The Future.

But The Future is slowing me down to a crawl. I’m spending a lot of time waiting for containers to build. How can I make it faster?

### Methodology

I put together a simple test sandbox called [buildbench](https://github.com/windmilleng/buildbench) for timing Go compile times inside a container.

The program imports the Kubernetes Go client, an easy way to make your compile time 100x slower!

```go
package main

import (
  "fmt"

  _ "k8s.io/client-go/kubernetes"
)

var nonce = "Friday"

func main() {
  fmt.Printf("Yay! TGI%s!\n", nonce)
}
```

To measure build speed, we change `nonce` to the current time, then run the compiler. This is easy to do with a small Makefile snippet:

```makefile
define inject-nonce
  sed -i -e 's/nonce = .*$$/nonce = "$(shell date)"/' cmd/example/main.go
endef

naked:
  $(call inject-nonce)
  go run ./cmd/example/main.go
```

We run each Make rule twice: once to prime the cache, and a second time to get the incremental build speed. We compare this against a baseline naked build, outside a container, of ~1.5–2 seconds. (A better test would run Make N times and find the median. But this makes the demo slower to run and less punchy.)

If you want to see the results, scroll to the bottom. If you want to read about the optimization tricks, read on!

### Naive Build

The most simple possible Dockerfile we can write needs to:

1. Add our Go code

1. Download the dependencies

1. Compile the Go code

Here’s what it looks like:

```dockerfile
FROM golang:1.10
RUN go get github.com/golang/dep/cmd/dep
WORKDIR /go/src/github.com/windmilleng/buildbench
ADD . .
RUN dep ensure
RUN go install github.com/windmilleng/buildbench/cmd/example
ENTRYPOINT /go/bin/example
```

**Pros:** It’s simple!

**Cons: **It’s slow! Every time we change the nonce, and incremental build needs to re-download all the dependencies and re-compile from scratch. This takes ~50 seconds.

### Cache Deps Pattern

The slowest part of the build is downloading the dependencies. Let’s see if we can skip it.

The Docker build cache can skip steps that have already been done in previous builds. If the input is the same, and the `RUN` command is the same, then you can use the last result instead of building a new one.

In this case, we first add Gopkg.toml and Gopkg.lock, our list of dependencies, then run `dep ensure`. As long as the dependency lists don’t change, Docker will cache the download.

```dockerfile
FROM golang:1.10
RUN go get github.com/golang/dep/cmd/dep
WORKDIR /go/src/github.com/windmilleng/buildbench
ADD Gopkg.* ./
RUN dep ensure --vendor-only
ADD . .
RUN go install github.com/windmilleng/buildbench/cmd/example
ENTRYPOINT /go/bin/example
```

**Pros:** With a very small change, we make it 2x as fast, going from 50 seconds to 25 seconds.

**Cons:** 25 seconds is still much slower than a naked build 😢

### Cache Objects Pattern

Why is it still so slow? When you build locally, the Go tool only re-compiles source that has changed. It uses a cache of compiled object files. When you build in a container, the Go tool has to re-compile everything from scratch.

Let’s try to do the same thing with our containers, using compiled object files from previous builds. This one is a bit more complicated, so let’s walk through it.

```dockerfile
# Start builder
ARG baseImage="golang:1.10"
FROM ${baseImage} as builder
RUN go get github.com/golang/dep/cmd/dep
WORKDIR /go/src/github.com/windmilleng/buildbench
ADD Gopkg.* ./
RUN dep ensure --vendor-only
ADD . .
RUN go install github.com/windmilleng/buildbench/cmd/example
# Done builder

# Start obj-cache
FROM golang:1.10 as obj-cache
COPY --from=builder /root/.cache /root/.cache
# Done obj-cache

# Start main
FROM builder
ENTRYPOINT /go/bin/example
# Done main
```

This Dockerfile lets you build two different images: the “main” image with the binary, and the “obj-cache” image that only contains the Go cache. This Dockerfile also lets you set the base image from the command-line, so that you can use the obj-cache on subsequent builds.

```makefile
cacheobjs-base:
  if [ "$(shell docker images windmill.build/buildbench/cacheobjs-base -q)" = "" ]; then \
    docker build -t windmill.build/buildbench/cacheobjs-base -f Dockerfile.cacheobjs --target=obj-cache .; \
  fi;

cacheobjs: cacheobjs-base
  $(call inject-nonce)
  docker build --build-arg baseImage=windmill.build/buildbench/cacheobjs-base \
               -t windmill.build/buildbench/cacheobjs \
               -f Dockerfile.cacheobjs .
  docker run --rm -it windmill.build/buildbench/cacheobjs
```

Our Makefile automates the do-si-do. The first time we build cacheobjs, we build an object cache. On subsequent builds, we can re-use those objects.

**Pros:** Another 2x speed improvement, down to 10-12 seconds.

**Cons:** Needs a Makefile folk dance to build the base image. Also needs tooling to periodically delete the object cache. Still much slower than naked builds.

### Taily Build Pattern

Can we do even better? Each build needs to create a new container. What if we left the container open?

The last pattern I want to tell you about is the Taily Build pattern, named after [the vengeful cat demon who just wants his tail back](https://en.wikipedia.org/wiki/Tailypo).

A Taily Build Dockerfile uses a `tail -f /dev/null` to keep the container open forever.

```dockerfile
FROM golang:1.10
RUN go get github.com/golang/dep/cmd/dep
WORKDIR /go/src/github.com/windmilleng/buildbench
ADD Gopkg.* ./
RUN dep ensure --vendor-only
ADD . .
RUN go install github.com/windmilleng/buildbench/cmd/example

# Keep the container open
ENTRYPOINT tail -f /dev/null
```

When we want to re-compile, we use the docker tool to copy files and exec commands in the running container:

```makefile
tailybuild-base:
  if [ "$(shell docker ps --filter=name=tailybuild -q)" = "" ]; then \
    docker build -t windmill.build/buildbench/tailybuild-base -f Dockerfile.tailybuild .; \
    docker run --name tailybuild -d windmill.build/buildbench/tailybuild-base; \
  fi;

tailybuild: tailybuild-base
  $(call inject-nonce)
  docker exec -it tailybuild rm -fR cmd
  docker cp cmd tailybuild:/go/src/github.com/windmilleng/buildbench/
  docker exec -it tailybuild go install github.com/windmilleng/buildbench/cmd/example
  docker exec -it tailybuild /go/bin/example
```

If you’re building containers locally, you can make this even faster. Instead of removing and copying files, you can create mount your local directory directly in the container. The [buildbench repo](https://github.com/windmilleng/buildbench) has examples of both: tailybuild (which uses file copying) and tailymount (which uses mounts).

**Pros:** An additional 4x speed improvement, down to 2-3 seconds, pretty close to naked builds. This works especially well in environments that use a persistent build server, like FlowJS or Scala/SBT or Java/Gradle.

**Cons:** Requires a lot of tooling to get right. Ideally, you want to copy as few files into the container as possible to keep it fast. Mounts help with the speed, but are coarse-grained (each directory is all-or-nothing), making it easy to accidentally leak files into the container that you don’t want in there. If you do it wrong, you can get weird results.

### The Results

These were the results on my laptop, running Docker 18.06.1-ce on Ubuntu 18.04.1:

```
Make naive: 51.616401s
Make cachedeps: 25.491433s
Make cacheobjs: 12.217298s
Make tailybuild: 2.723723s
Make tailymount: 2.180016s
Make naked: 1.906474s
```


Your mileage may vary depending on hardware & OS. You can reproduce the results yourself by cloning [the buildbench repo](https://github.com/windmilleng/buildbench) and running `make profile`.

This shows that there’s hope for building inside a container without giving up performance!

### The Future!!

I think that 10 years from now, we’ll look back on containers as the software development equivalent of the discovery of kitchenware.

Sure, you can eat soup with your hands.

It’s probably OK when you’re 5 years old and still developing motor skills.

But you’ll make a mess every time. Eventually you’ll get tired of cleaning it up.

The promise of containers is like the promise of plates and dishwashers: they are easier to clean up when you’re done.

Unfortunately, building in containers is often still too slow and hard to debug. It’s like we’ve figured out soup bowls, but trying to scoop the soup out with forks and knives.

At Windmill, we’re building tools that have these tips & tricks built-in so that you can develop fast without fiddling with container optimizations. Curious to learn more? Know some tricks we missed? [I’d love to hear from you.](mailto:nick@windmill.engineering)
