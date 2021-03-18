---
slug: "kubernetes-is-so-simple"
date: 2021-03-18
author: nick
layout: blog
title: "Kubernetes is so Simple You Can Explore it with Curl"
image: "/assets/images/kubernetes-is-so-simple/curling.jpg"
image_caption: "\"Curling;--a Scottish Game, at Central Park\" by John George Brown. <a href='https://commons.wikimedia.org/wiki/File:John_George_Brown_-_Curling;--a_Scottish_Game,_at_Central_Park_-_Google_Art_Project.jpg'>Via Wikipedia.</a>"
tags:
  - kubernetes
  - api
  - api-server
---

A common take on Kubernetes is that it's very complicated. 

... and because it's complicated, the configuration is very verbose. 

... and because there's so much config YAML, we need big toolchains just to handle that config.

I want to convince you that the arrow of blame points in the opposite direction!

Kubernetes has a simple, genius idea about how to manage configuration.

Because it's straightforward and consistent, we can manage more config than we
ever could before! And now that we can manage oodles more config, we can build
overcomplicated systems. Hooray!

The configs themselves may be complicated. So in this post, I'm going to skip
the configs. I'll focus purely on the API machinery and how to explore that
API.

Building APIs this way could benefit a lot of tools.

## What is the Idea?

To explain the simple, genius idea, let's start with the simple, genius idea of Unix:

```
Everything is a file.
```

Or to be more precise, everything is a text stream. Unix programs read and write
text streams. The filesystem is an API for finding text streams to read. Not all
of these text streams are files!

- `~/hello-world.txt` is a text file
- `/dev/null` is an empty text stream
- `/proc` is a set of text streams for reading about processes

Let's take a closer look at `/proc`. [Here's a Julia Evans comic about it](https://wizardzines.com/comics/proc/).

You can learn about what's running on your system by looking at `/proc`, like:

- How many processes are running (`ls /proc` - List the processes)
- What command line started process PID (`cat /proc/PID/cmdline` - Get the
  process specification)
- How much memory process PID is using (`cat /proc/PID/status` - Get the process status)

## What is the Kubernetes API?

The Kubernetes API is `/proc` for distributed systems.

Everything is a resource over HTTP. We can explore every Kubernetes resource
with a few HTTP GET commands.

To follow along, you'll need:

- [`kind`](https://kind.sigs.k8s.io/) - or any small, throwaway Kubernetes cluster
- `curl` - or any CLI tool for sending HTTP requests
- `jq` - or any CLI tool for exploring JSON
- `kubectl` - to help `curl` authenticate

Let's start by creating a cluster:

```
$ kind create cluster
Creating cluster "kind" ...
 ✓ Ensuring node image (kindest/node:v1.19.1) 🖼
 ✓ Preparing nodes 📦  
 ✓ Writing configuration 📜 
 ✓ Starting control-plane 🕹️ 
 ✓ Installing CNI 🔌 
 ✓ Installing StorageClass 💾 
Set kubectl context to "kind-kind"
You can now use your cluster with:

kubectl cluster-info --context kind-kind

Have a nice day! 👋

$ kubectl proxy &
Starting to serve on 127.0.0.1:8001
```

`kubectl proxy` is a server that handles certificates for us, so that we don't
need to worry about auth tokens with `curl`.

The Kubernetes API has more hierarchy than `/proc`. It's split into folders by
version and namespace and resource type.  The API path format looks like:

```
/api/[version]/namespaces/[namespace]/[resource]/[name]
```

On a fresh `kind` cluster, there should be some pods already running in the
`kube-system` namespace we can look at. Let's list all the system processes in
our cluster:

```
$ curl -s http://localhost:8001/api/v1/namespaces/kube-system/pods | head -n 20
{
  "kind": "PodList",
  "apiVersion": "v1",
  "metadata": {
    "selfLink": "/api/v1/namespaces/kube-system/pods",
    "resourceVersion": "1233"
  },
  "items": [
    {
      "metadata": {
        "name": "coredns-f9fd979d6-5zxtx",
        "generateName": "coredns-f9fd979d6-",
        "namespace": "kube-system",
        "selfLink": "/api/v1/namespaces/kube-system/pods/coredns-f9fd979d6-5zxtx",
        "uid": "a30e70cc-2b53-4511-a5de-57c80e5b68ad",
        "resourceVersion": "549",
        "creationTimestamp": "2021-03-04T15:51:21Z",
        "labels": {
          "k8s-app": "kube-dns",
          "pod-template-hash": "f9fd979d6"
```

That's a lot of text! We can use `jq` to pull out the names of objects.

```
$ curl -s http://localhost:8001/api/v1/namespaces/kube-system/pods | jq '.items[].metadata.name'
"coredns-f9fd979d6-5zxtx"
"coredns-f9fd979d6-bn6jz"
"etcd-kind-control-plane"
"kindnet-fcjkd"
"kube-apiserver-kind-control-plane"
"kube-controller-manager-kind-control-plane"
"kube-proxy-sn64n"
"kube-scheduler-kind-control-plane"
```

The `/pods` endpoint lists out all the processes, like `ls /proc`. If we want to
look at a particular process, we can query `/pods/POD_NAME`.

```
$ curl -s http://localhost:8001/api/v1/namespaces/kube-system/pods/kube-apiserver-kind-control-plane | head -n 10
{
  "kind": "Pod",
  "apiVersion": "v1",
  "metadata": {
    "name": "kube-apiserver-kind-control-plane",
    "namespace": "kube-system",
    "selfLink": "/api/v1/namespaces/kube-system/pods/kube-apiserver-kind-control-plane",
    "uid": "a8f893b7-1cdb-48fd-9505-87d71c81adcb",
    "resourceVersion": "458",
    "creationTimestamp": "2021-03-04T15:51:17Z",
```

Or, again, we can use `jq` to fetch a particular field.

```
$ curl -s http://localhost:8001/api/v1/namespaces/kube-system/pods/kube-apiserver-kind-control-plane | jq '.status.phase'
"Running"
```

## How to unpack what `kubectl` is doing

All of the things above can be done with `kubectl`. `kubectl` provides a more
friendly interface. But if you're ever wondering what APIs `kubectl` is calling,
you can run it with `-v 6`:

```
$ kubectl get -v 6 -n kube-system pods kube-apiserver-kind-control-plane
I0304 12:47:59.687088 3573879 loader.go:375] Config loaded from file:  /home/nick/.kube/config
I0304 12:47:59.697325 3573879 round_trippers.go:443] GET https://127.0.0.1:44291/api/v1/namespaces/kube-system/pods/kube-apiserver-kind-control-plane 200 OK in 5 milliseconds
NAME                                READY   STATUS    RESTARTS   AGE
kube-apiserver-kind-control-plane   1/1     Running   0          116m
```

For more advanced debugging, use `-v 8` to see the complete response body.

The point isn't that you should throw away `kubectl` in favor of `curl` to
interact with Kubernetes. Just like you shouldn't throw away `ps` in favor of
`ls /proc`.

But I've found disecting Kubernetes like this is helpful to think of it
as a process-management system built on a couple straightforward principles:

- Everything is a resource over HTTP.
- Every object is read and written the same way.
- All object state is readable.

These are powerful ideas[^1]. They help us build tools that fit together well.

In the same way that we can pipe Unix tools together (like `jq`), we can define
new Kubernetes objects and combine them with existing ones. 

Sometimes they're silly! Like in this Ellen Körbes talk on [how to build a
Useless Machine](https://www.youtube.com/watch?v=85dKpsFFju4).

<div class="block block--video">
<iframe width="560" height="315" src="https://www.youtube.com/embed/85dKpsFFju4" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>

In future posts, I want to talk about how to write code that uses these APIs
effectively. And how we're leaning into [these ideas in
Tilt](https://github.com/tilt-dev/tilt-apiserver). Stay tuned!


[^1]: [REST](https://en.wikipedia.org/wiki/Representational_state_transfer) is
    an old idea (measured on the scale of Internet Time). What I like about
    Kubernetes' take on REST is that it's less focused on "how do we make sure
    new API endpoints we define obey the REST gospel", and more focused on "how
    do we autogenerate APIs from data types?"
