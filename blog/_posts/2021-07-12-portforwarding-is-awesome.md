---
slug: "portforwarding-is-awesome"
date: 2021-07-12
author: nick
layout: blog
title: "Portforwarding should be a tool in every dev toolbox"
subtitle: "An overview of socat, kubectl port-forward, and how Tilt manages portforwards"
description: "An overview of socat, kubectl port-forward, and how Tilt manages portforwards"
image: "/assets/images/portforwarding-is-awesome/tunnel.jpg"
image_caption: "The Joralemon Street Tunnel, via <a href='https://commons.wikimedia.org/wiki/File:Joralemon_Street_Tunnel_postcard,_1913.jpg'>commons.wikipedia.org</a>."
tags:
  - api
  - networking
---

In the Unix mindset, every program reads and writes files. So it's important to have a toolkit of basic
tools like `cat` for working with files!

In 2021, we mostly write servers. That's why it's important to have a toolkit for working with 
network sockets!

In this post, we're going to do a quick tour of the tools we (the Tilt team) work
with everyday and how we use them. In particular:

1. `socat`, the assembly language of socket tools.

2. `kubectl port-forward`, an essential building block of any Kubernetes-based dev environment.

3. Tilt's `PortForward` API, a self-healing wrapper around `kubectl port-forward`.

I've been thinking through what different tools are good for, looking at how
they interoperate with each other, and came up with a framework for figuring out
which one is right for what I'm working on.

You don't have to use these tools in particular, but I hope you'll learn
something new!

## Reverse-engineering multi-service apps with `socat`

I really like Cindy Sridharan's introduction to `socat`:

> `socat` truly is the Swiss Army Knife of network debugging tools.

> `socat` stands for SOcket CAT. It is a utility for data transfer between two addresses.

> I personally use `socat` not so much as a production debugging tool than for
> troubleshooting local development issues (especially when developing network
> services).

[Open it in a tab right
now](https://copyconstruct.medium.com/socat-29453e9fc8a6) because you'll
want to read it later. It's long but worth it.

I personally tend to use `socat` to debug and/or reverse-engineer services that I don't understand.

For example, suppose I have a service listening on port 8080. I don't know
what's sending it requests.

I can restart the service on port 8081, then use a socat command listening on
8080 to inspect its traffic:

```
socat -v TCP-LISTEN:8080,reuseaddr,fork TCP:localhost:8081
```

Cindy's post dissects this command in more detail. It basically says: listen on
8080, copy the data to 8081, and print out everything you see. Here's an example
of what it might print:

```
Host: localhost:8080\r
User-Agent: curl/7.74.0\r
Accept: */*\r
\r
< 2021/07/07 13:18:16.172097  length=356 from=0 to=355
HTTP/1.1 200 OK \r
```

A `socat` process can intercept lots of different types of connections! For
example, the Docker Daemon listens on a unix socket
`/var/run/docker.sock`. `socat` is a great tool for seeing how the Docker CLI
interacts with the Docker Service!

```
sudo mv /var/run/docker.sock /var/run/docker.sock.original
sudo socat -v UNIX-LISTEN:/var/run/docker.sock,mode=777,reuseaddr,fork UNIX-CONNECT:/var/run/docker.sock.original
```

Now, when I run a Docker CLI command, I can see which HTTP requests it makes:

```
# docker ps
...
GET /v1.41/containers/json HTTP/1.1\r
Host: docker\r
User-Agent: Docker-Client/20.10.7 (linux)\r
\r
< 2021/07/07 13:40:15.162007  length=6647 from=280 to=6926
HTTP/1.1 200 OK\r
...
```

Remember to restore the socket when you're done!

```
sudo mv /var/run/docker.sock.original /var/run/docker.sock
```

## Connecting to multi-service apps with `kubectl port-forward`

Pretty much every time I do development in Kubernetes, I use `kubectl
port-forward`. You can think of it as a chain of `socat` commands that copy socket data
from a local port (`localhost:8080`) to the Kubernetes API server, then to the inside of
a Pod running in Kubernetes.

In this post, I'm mostly going to focus on how we use `port-forward` in dev. If
you want to learn more about how it works under the covers, Ivan Sim wrote [a
deep dive](https://itnext.io/how-it-works-kubectl-exec-e31325daa910) into
`kubectl exec` that I like. Even though it's about `exec`, not `port-forward`,
they follow a similar flow.

The simplest way to use `kubectl port-forward` is to connect to a pod:

```
kubectl port-forward example-go-7ff5965bbb-6jblq 8080:8000
```

This copies socket data from `localhost:8080` to port 8000 inside the pod `example-go-7ff5965bbb-6jblq`.

But we usually don't deal directly with Kubernetes pods! We deal with
Deployments / StatefulSets (resources that manage pods) or Services / Ingresses
(resources that redirect traffic to pods).

Fortunately, `kubectl port-forward` has some nice utilities that infer pods from deployments and services:

```
kubectl port-forward deployment/example-go 8080:8000
```

But beware! This doesn't behave like most people expect! This uses the
Deployment to choose a single pod.  If that pod is deleted, the port-forward
breaks and emits errors until you restart it (which will force it to choose a
new pod).

Meanwhile, the borked port-forward is using up a terminal.

Can we do better?

## Inside the Box: A port-forward as Just Another Server

One way to think about `kubectl port-forward` is just another server. It's a
very simple server!  But it goes great with lots of other tooling that we use to
manage multiple servers and auto-restart them when they're not healthy.

For example, I like setting up `entr`'s `-r` flag to restart processes when I hit
spacebar. Here's how you'd do this with port-forwarding:

```
ls | entr -r kubectl port-forward deployment/example-go 8080:8000
```

Or I might use Tilt to run it as a local resource:

```python
local_resource(
  name='example-go-8000',
  serve_cmd='kubectl port-forward deployment/example-go 8080:8000')
```

That will make it show up as a separate server in the Tilt UI with a restart
button.

Tilt also has tools to add links and health-checking for servers, so I can
see when it breaks.

```python
local_resource(
  name='example-go-8000',
  serve_cmd='kubectl port-forward deployment/example-go 8080:8000',
  links=['http://localhost:8080'],
  readiness_probe=probe(http_get=http_get_action(port=8080)))
```

Tilt will periodically check that the portforward is running. Other tools for
managing multiple services (e.g. tmux) will work well too!

## Outside the Box: A port-forward is A Special Dynamic Server!

But most Tilt users don't think of the port-forward as a separate server. We
think about it as a property of the primary server! In Tilt, you specify it as a
property of a Kubernetes resource:

```python
k8s_resource('example-go', port_forwards=[port_forward(8080, 8000)])
```

If we delete the primary server, we want the port-forward to go away.

If we delete a pod and replace it with a new one, we want the port-forward to send
traffic to the new pod.

How does Tilt accomplish this?

Tilt has two important tools to stitch this together: 
the [PortForward](https://api.tilt.dev/kubernetes/port-forward-v1alpha1.html) object 
and the [KubernetesDiscovery](https://api.tilt.dev/kubernetes/kubernetes-discovery-v1alpha1.html) object.

PortForward tracks all the port-forwards that Tilt is managing. If I'm running
[the example-go project](https://github.com/tilt-dev/tilt-example-go), I can
inspect them like this:

```
$ tilt get portforwards
NAME                                     CREATED AT
example-go-example-go-5cc87c754d-9ngn4   2021-07-07T18:36:05Z

$ tilt describe portforwards
Name:         example-go-example-go-5cc87c754d-9ngn4
...
API Version:  tilt.dev/v1alpha1
Kind:         PortForward
Metadata:
  Creation Timestamp:  2021-07-07T18:36:05Z
  ...
Spec:
  Forwards:
    Container Port:  8000
    Host:            localhost
    Local Port:      8000
  Namespace:         default
  Pod Name:          example-go-5cc87c754d-9ngn4
Status:
  Forward Statuses:
    Addresses:
      127.0.0.1
      ::1
    Container Port:  8000
    Local Port:      8000
    Started At:      2021-07-07T18:36:06.022789Z
```

This lets you see what pods Tilt is connecting to and when it started port-forwarding.

But each PortForward object only works for a single pod.

Tilt has a second API object, KubernetesDiscovery, which tracks which pods belong to which
resource.

```
$ tilt get kubernetesdiscovery
NAME         CREATED AT
example-go   2021-07-07T18:35:51Z
$ tilt describe kubernetesdiscovery
Name:         example-go
...
Spec:
  ...
  Port Forward Template Spec:
    Forwards:
      Container Port:  0
      Host:            localhost
      Local Port:      8000
  Watches:
    Name:       example-go
    Namespace:  default
    UID:        bcb9e5bd-bd8c-4683-87b1-b7b7b7276c7f
Status:
  Monitor Start Time:  2021-07-07T18:36:04.509869Z
  Pods:
    ...
    Name:                    example-go-5cc87c754d-9ngn4
    ...
```

The KubernetesDiscovery object contains a port-forward template. As pods are
created, updated, and deleted, this object will select the "best" pod for
portforwarding, and sets up a PortForward object to manage the connection.

## Why am I telling you this??? 
 
This post has been an overview of how we use `socat`, `kubectl port-forward`,
and Tilt's own `PortForward` and `KubernetesDiscovery` APIs. But let's take a
step back from the implementation details to pull out some general trends:

1) More and more, in multi-service dev, tools that copy socket data around are
helpful.

2) Copying socket data, in practice, means you're creating a new server (albeit
a very simple server).

3) The fundamental Kubernetes pattern -- watch for changes to an API, and update
our servers in response -- is really useful when managing servers!

We're not building this API only for internal Tilt use. Tilt exposes them
publicly, to help connect new tools that build on top of them.

What will those new tools be? This post is already a bit long so it will have to
wait for another post. But let us know if you'd like to see some ideas, or
want to build on this API together. 😀



