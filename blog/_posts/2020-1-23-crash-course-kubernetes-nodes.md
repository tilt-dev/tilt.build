---
slug: crash-course-kubernetes-nodes
date: 2020-1-23
author: maia
layout: blog
title: "A Crash Course in Kubernetes #2: Nodes"
subtitle: "tbd"
image: "slide1.gif"
image_needs_slug: true
image_caption: "tbd"
tags:
  - docker
  - kubernetes
  - microservices
  - tilt
  - containers
keywords:
  - kubernetes
  - introduction
  - kubecontext
  - tilt
  - nodes
---
<script src="/assets/js/slideshow.js"></script>

Hello and welcome to our now slightly less-new blog post series, “A Crash Course on Kubernetes!” 

Our summer intern didn’t have a background in Kubernetes, so to get her up to speed, we started
giving internal Tilt University presentations on relevant concepts. This was a great crash
course for our intern, but even our experienced engineers learned things at these talks--turns
out, you can work within Kubernetes pretty effectively and still have large gaps in your
mental models.

We’re blogifying our Tilt U presentations so that other folks can benefit from the digging we did.
This is post #2 of the series, in which we talk about nodes, a.k.a "the things that hold the things
that run your app."

If you missed [Post 1: Overview](https://blog.tilt.dev/2019/10/16/crash-course-kubernetes
-overview.html), you might want to start there. Stay tuned for post #3, which will cover pods
(the things that actually run your app) and services (how pods talk to each other and the
outside world).

## What is a Node, and Why Should I Care?
In the above diagram, the blue squares are nodes. A node is just a machine (physical or virtual,
it doesn’t matter) that runs some containers, and a Kubernetes process or two. There are two
types of nodes: **worker nodes**, where your code runs, and the **master node**, which is in
charge of managing the cluster.

Like most other parts of Kubernetes, nodes are easy to ignore and abstract away when your
cluster is in a happy state. When things start to break, however, it can be really useful to
understand just what Kubernetes is doing. 

If you start getting errors like “node(s) had taints” and “could not schedule pod”, knowing how
nodes work, and how pods are assigned to nodes, will help you figure out what’s going on. And
if things start to go wrong (“Unable to connect to the [API] server”), or if your `kubectl
apply` didn’t work like you expected it to, an accurate mental model of the master node and
all the machinery that runs your cluster will be a lifesaver.

### Wait, What’s a Pod?
Simply put, a pod is one unit of your app---say, a running instance of `shopping_cart_server`.
There’s a bit more to it than that, of course, but we’ll delve into the intricacies of pods in
the next post in this series. 

For the discussion of nodes, all you need to know is that a pod runs your app in a container,
and pods themselves are containers that run on nodes. 

## Anatomy of a Node
### Master Node
First we’ll talk about the master node. It’s called the “master node” because it’s in charge of everything.

In Kubernetes, you specify your configuration _declaratively_---you tell Kubernetes the desired
state of your cluster (number of instances of your app, which scaling method to use, how to set
up the networking) and Kubernetes makes it so. 

The master node is how: it is both the means by which you specify your desired state, and the
machinery for making sure that state is maintained.

The desired cluster state lives on the master node in a datastore called **etcd**, [a consistent,
highly-available key value store](https://etcd.io/). 

The master node runs a number of [**controllers**](https://kubernetes.io/docs/concepts/architecture/controller/).
For a given type of Kubernetes object, a controller: 
* Polls the cluster for state relating to that type; 
* Compares it to the desired state stored in etcd; and if needed,
* Calls out to the **API server** to make any changes to the cluster. 

For example, if the Replication Controller sees that the desired state of ReplicaSet A is “four
copies of podA”, but only three podA’s exist in the cluster, the controller asks the API server
to spin up another podA.

The **API server** is the bit of master node machinery that makes changes in the cluster. K8s
internals call to the API server to create, update, and destroy objects, store data in etcd,
and a bunch of other stuff. The API server also accepts user commands--any `kubectl` command
you run is a request to the API server.

So when you call `kubectl apply -f pod.yaml`...

<!-- Adapted from https://codepen.io/gabrieleromanato/pen/pKrny -->
<div class="slider" id="main-slider"><!-- outermost container element -->
	<div class="slider-wrapper"><!-- innermost wrapper element -->
	    <!-- slides -->
		<div class="slide" data-image="/assets/images/crash-course-kubernetes-nodes/slide1.gif"></div>
		<div class="slide" data-image="/assets/images/crash-course-kubernetes-nodes/slide2.gif"></div>
		<div class="slide" data-image="/assets/images/crash-course-kubernetes-nodes/slide3.gif"></div>
	</div>
	<div class="slider-nav"><!-- "Previous" and "Next" actions -->
		<button class="slider-previous">Previous</button>
		<button class="slider-next">Next</button>
	</div>
</div>	


To read more about the above components, and all the other bits and pieces on the master node
that do important work, see [the Kubernetes docs](https://kubernetes.io/docs/concepts/overview/components/#master-components).

### Worker Node(s)
All the fine-grained control of the master node does no good if there’s nowhere for your apps to
run. That’s where worker nodes come in. Worker nodes are machines that run one or more pods
(i.e. units of your app).

If you’re connected to a Kubernetes cluster in the cloud, you’ll most likely run your pods across
multiple nodes. If you’re running Kubernetes locally (e.g. Docker Desktop, KinD, Minikube), you’ll
be working with a single node, which is a VM running on your computer. Regardless of the number
of worker nodes you have at your disposal, and whether they’re physical or virtual machines, the
basic anatomy is the same.

In addition to your pod(s), a worker node has some additional daemons that allow it to do its job:

* **Kubelet**: makes sure that the right containers are running on the right pods. It works a lot
like the controllers that live on the master node: the kubelet reads the state of all the pods
on its node, compares that against the desired state and, if there’s a discrepancy, makes the necessary changes
* **Kube-proxy**: proxies network traffic to/from pods (since pods aren’t themselves directly
connected to the network)

[Read more about worker nodes and their components here](https://kubernetes.io/docs/concepts/overview/components/#node-components).

A worker node is only as good as the pods it’s running, so how does it figure out which pods to
run? This is where the pod scheduler, our last piece of master node machinery, comes in.

#### Scheduling: Putting Pods on Nodes
The **pod scheduler** on the master node watches for new pods that haven’t been assigned to
nodes. These are pods that need creation, but we don’t yet know what computer they’re going to
live on. For each of these pods, the pod scheduler finds the “best” node to put it on.

First, it checks for _possible_ nodes, that is, those that have enough resources. With the list
of available nodes thus narrowed down, the scheduler chooses the “best” node, according to a set
of rules which Kubernetes calls “priorities.” (Some set of scheduling priorities are active by
default, but you can configure your cluster to use whatever priorities you want.) 

Examples of some priorities by which the scheduler might decide on the “best” node:
* `ImageLocalityPriority`: Favors nodes that already have the container images for that Pod cached locally.
* `SelectorSpreadPriority`: Spreads Pods across hosts, considering Pods that belong to the same Service, StatefulSet or ReplicaSet.

## That’s it for now
Thanks for joining us for post #2 of our “Crash Course on Kubernetes.” I hope this overview of
nodes answered at least some of your questions (even if it left you with many more). 

Our next post in this series will focus on pods---you know, the bits of Kubernetes that actually
run your app---how they work, and how they talk to each other and the outside world. 

Until then: happy kube-ing!

