---
title: Why is Tilt broken?
layout: docs
---

Tilt is broken. What should you do?

There are a lot of ways to get help,
depending on how willing you are to get your hands dirty.

---

### Where can I ask questions?

Join [the Kubernetes slack](http://slack.k8s.io) and
find us in the [#tilt](https://kubernetes.slack.com/messages/CESBL84MV/)
channel. The entire Tilt team is there, and can answer any questions you have.

Or you can [file an issue](https://github.com/windmilleng/tilt/issues).

---

### Why does Tilt crash on startup?

Run:

```shell
tilt doctor
```

Tilt will print out status information:
- Tilt version
- Operating system
- Docker host and version
- Kubernetes version
- Type of Kubernetes cluster (Docker for Mac, Microk8s, etc)
- Container runtime

This can help you figure out what cluster Tilt thinks you're using. It's usually
the first thing we ask for when people file issues with Tilt.

---

### What info should I send when I need help?

A snapshot is a link that you can send to someone that will allow them to
interactively explore your current Tilt state. This is useful for async
debugging and adding context to bug reports. They look like pretty much just
like Tilt, but frozen in time:

[https://cloud.tilt.dev/snapshot/AYSV59gLhM3GVMuuR28=](https://cloud.tilt.dev/snapshot/AYSV59gLhM3GVMuuR28=)

A snapshot is a frozen "moment-in-time" version of the Tilt UI. In a snapshot
you can drill in to specific services, see alerts and Kubernetes events. Pretty
much anything you can do in normal Tilt, you can do in a snapshot!

This is also helpful to send along with bug reports.

For more information, see "[Share Errors and Cluster State with Snapshots](snapshots.html)".

---

### Why does my image build fail in Tilt when it succeeds with `docker build`?

Run:

```shell
tilt docker -- build ARGS
```

This will run Docker the same way that Tilt runs Docker.

Tilt automatically enables optimizations that you may not be using by
default. For example, if you are using minikube and run:

```shell
tilt docker -- build -t image-name .
```

Tilt may print:

```
Running Docker command as:
DOCKER_HOST=tcp://192.168.99.100:2376 DOCKER_CERT_PATH=/home/nick/.minikube/certs DOCKER_TLS_VERIFY=1 docker build -t image-name .
```

because it's running against Minikube's Docker instance, not your Docker instance.

---

### Why is Tilt using so much CPU or memory?

Please file an issue if Tilt is being a resource hog! We've made it a lot better
in the last few months but there may still be builds that cause problems.

As of v0.10.26, Tilt exposes the standard Go pprof hooks over [HTTP](https://golang.org/pkg/net/http/pprof/).

To look at a 30-second CPU profile:

```shell
go tool pprof http://localhost:10350/debug/pprof/profile?seconds=30
```

To look at the heap profile:

```shell
go tool pprof http://localhost:10350/debug/pprof/heap
```

This opens a special REPL that lets you explore the data.
Type `web` in the REPL to see a CPU graph.

For more information on pprof, see [the Go pprof guide](https://github.com/google/pprof/blob/master/doc/README.md).

---

### What does Tilt think is happening right now?

The internal Tilt engine is implemented as a control loop, just like Kubernetes.

Tilt watches lots of different inputs (your Tiltfile, your local source files,
and your Kubernetes cluster) for changes. The control loop records these
changes in a central state store. Then, Tilt kicks off updates to your cluster
based on the state store.

That means all the state Tilt knows about lives in a single place. And you can inspect it!

While Tilt is running in one terminal, open another terminal and run:

```shell
tilt dump engine
```

Tilt will print a JSON representation of everything it knows about your build state and your cluster state.

The Tilt UI has a similar control loop. Run:

```shell
tilt dump webview
```

to see the complete state of the Tilt web UI.

---

### How can I monitor Tilt usage on my team?

As of v0.10.25, Tilt has an experimental Tiltfile function: `experimental_telemetry_cmd`.

This command takes a string which is a command to run. Tilt will exec this
command every minute and pass it on stdin a series of new line separated JSON
objects representing all of the user’s activity in the last minute, to do with
what you will.

For example, here’s a command that the Tilt team uses in some of our Tiltfiles:

```python
experimental_telemetry_cmd("docker run --env USER -i telemetry")
```

The JSON format that it gets passed looks like this:

```json
{"SpanContext":{"TraceID":"00000000000000000000000000000000","SpanID":"0000000000000000","TraceFlags":1},"ParentSpanID":"0000000000000000","SpanKind":1,"Name":"tilt.dev/usage/update","StartTime":"2019-12-11T12:18:30.702255-05:00","EndTime":"2019-12-11T12:18:31.920728054-05:00","Attributes":null,"MessageEvents":null,"Links":null,"Status":0,"HasRemoteParent":false,"DroppedAttributeCount":0,"DroppedMessageEventCount":0,"DroppedLinkCount":0,"ChildSpanCount":0}
{"SpanContext":{"TraceID":"00000000000000000000000000000000","SpanID":"0000000000000000","TraceFlags":1},"ParentSpanID":"0000000000000000","SpanKind":1,"Name":"tilt.dev/usage/update","StartTime":"2019-12-11T12:18:31.922581-05:00","EndTime":"2019-12-11T12:18:32.257773437-05:00","Attributes":null,"MessageEvents":null,"Links":null,"Status":0,"HasRemoteParent":false,"DroppedAttributeCount":0,"DroppedMessageEventCount":0,"DroppedLinkCount":0,"ChildSpanCount":0}
```

The eagle eyed may notice that these are just open telemetry spans.

Here are some examples that report these spans as:

- [A datadog time series](https://github.com/jazzdan/datadog_example/blob/master/example.rb)
- [A statsd reporter](https://github.com/jazzdan/statsd_example/blob/master/main.rb)

This is an experimental feature designed for larger companies.

<script src="/assets/js/links.js" async></script>
