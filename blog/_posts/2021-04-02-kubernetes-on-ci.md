---
slug: "kubernetes-on-ci"
date: 2021-04-02
author: nick
layout: blog
title: "Three Ways to Run Kubernetes on CI and Which One is Right for You!"
image: "/assets/images/kubernetes-on-ci/tarot.jpg"
image_caption: "A tarot deck, suitable for choosing Kubernetes topologies in CI. <a href='https://en.wikipedia.org/wiki/Rider-Waite_tarot_deck'>Via Wikipedia.</a>"
tags:
  - kubernetes
  - ci
  - test
---

When we first started developing Tilt, we broke ALL THE TIME.

Either Kubernetes changed. Or we had a subtle misunderstanding in how the API
works. Our changes would pass unit tests, but fail with a real Kubernetes cluster.

I built out an integration test suite that used the latest version of Tilt to
deploy real sample projects against a real cluster.

At the start, it was slow and flakey. But the tooling around running Kubernetes
in CI has come a long way, especially in the last 1-2 years. Now
it's less flakey than our normal unit tests 😬. Every new example repo we set
up uses a one-time Kubernetes cluster to run tests against.

A few of our friends have been asking us how we set it up and how to run their
own clusters in CI. I've now explained it enough times that I should probably
write down what we learned.

Here are three ways to set it up, with the pros and cons of each!

## Strategy #1: Local Cluster, Remote Registry

Here's how I set up our first integration test framework.

1. I created a dedicated gcr.io bucket for us to store images, and a GCP service
  account with permission to write to it.

2. I added the GCP service account credentials as a secret in our CI build.

3. I forked [`kubeadm-dind-cluster`](https://github.com/kubernetes-retired/kubeadm-dind-cluster),
  a set of Bash scripts to set up Kubernetes with Docker-in-Docker techniques.
  
All our test projects had Tilt build images, push them to the gcr.io bucket,
then deploy servers that used these images.

I barely got this working. A huge breakthrough! It caught so many subtle bugs
and race conditions.

I wouldn't call the Bash scripts _readable_. But they are hackable,
cut-and-pasteable. There were examples of how to run it on CircleCI and
TravisCI. `kubeadm-dind-cluster` has been deprecated in favor of more modern
approaches like [`kind`](https://kind.sigs.k8s.io). But I learned a lot from its
Bash scripts. We still use a lot of the techniques in this project today.

There were other downsides though:

- When drive-by contributors sent us PRs, the integration tests failed.
  They didn't have access to to write to the gcr.io bucket. This made me so sad.
  Contributors felt unwelcome. I never figured out a way to make this secure.
  
- We didn't reset the gcr.io bucket between test runs. So it was hard to guarantee
  that images weren't leaking between tests. For example, if image pushing failed,
  we wanted to be sure we weren't picking up a cached image from a previous test.

## Strategy #2: Local Registry On a VM

When I revisited this, I wanted to make sure:

- Anyone could write to the image registry.

- The image registry would reset between runs.

By this time, `kind` was taking off as the default choice for testing Kubernetes
itself. `kind` also comes with the ability to run a local registry, so
you can push images to the registry on `localhost:5000` and pull them from inside `kind`.

I set up a new CI pipeline that:
 
1. Creates a VM.

2. Installs all our dependencies, including Docker.

3. Creates a `kind` cluster with a local registry, using their script.

This worked well! And because the registry was local, it was faster than pushing
to a remote registry. We still use this approach to test `ctlptl` with both
`minikube` and `kind`. Here's [the CI
config](https://github.com/tilt-dev/ctlptl/blob/b6f808a09b05b6cf7aa0b3365e4781d2c23e4851/.circleci/config.yml#L30).

But I wasn't totally happy! Most of our team is more comfortable managing
containers than managing VMs. VMs are slower. Upgrading dependencies is
more heavyweight. We wondered: can we make this work in containers?

## Strategy #3: Local Registry On Remote Docker

The last approach (and the one we use in most of our projects) uses some of the
tricks that `kubeadm-dind-cluster` uses.

The CI pipeline:

1. Creates a container with our code.

2. Sets up [a remote Docker environment](https://circleci.com/docs/2.0/building-docker-images) outside the container.
   (This avoids the pitfalls of running Docker inside Docker.)

3. Starts a `kind` cluster with a local registry inside the remote Docker environment.

4. Uses `socat` networking jujitsu to expose the remote registry and Kubernetes
   cluster inside the local container.

The `socat` element makes this a bit tricky. But if you want to fork and hack it, check out
[this Bash script](https://github.com/tilt-dev/kind-local/blob/master/.circleci/with-kind-cluster.sh).

But once it's set up: it's fast, robust, and easy to upgrade dependencies.

## Putting it Together

Hacking together this with Bash was the hard part.

Tilt-team maintains [`ctlptl`](https://ctlptl.dev/), a CLI 
for declaratively setting up local Kubernetes clusters.

I eventually folded all the logic in the Bash script into `ctlptl`. As of
`ctlptl` 0.5.0, it will try to detect when you have a remote docker environment
and set up the `socat` forwarding.

The Go code in `ctlptl` is _far_ more verbose than the Bash script, comparing
number of lines. But it includes error handling, cleanup logic, and idempotency,
which makes it more suitable for local dev. (CI environments don't need any of this
because we tear them down at the end anyway.)

We use image-management tools that [auto-detect the registry location from
the
cluster](https://github.com/kubernetes/enhancements/tree/master/keps/sig-cluster-lifecycle/generic/1755-communicating-a-local-registry),
which helps with the configuration burden. I like the general trend of
Kubernetes as a general-purpose config-sharing system so that tools can
interoperate, rather than having to configure each tool individually.

We currently use `ctlptl` to set up clusters and test the services on real Kube
clusters in all of [our example projects](https://github.com/tilt-dev/tilt-example-html/blob/master/.circleci/config.yml).

It's been a long journey! But I hope the examples here will make that journey a lot
shorter for the next person 🙈.

## Shout-outs

- [CircleCI's](https://circleci.com/) remote Docker environment is good!

- Thanks to [the `kind` team](https://kind.sigs.k8s.io) for working with us on
  the local registry wiring!

- [`kubeadm-dind-cluster`](https://github.com/kubernetes-retired/kubeadm-dind-cluster),
  we salute you as an early adventurer in this problem space!
