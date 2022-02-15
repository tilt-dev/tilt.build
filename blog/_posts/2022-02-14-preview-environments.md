---
slug: "preview-environments"
date: 2022-02-14
author: nick
layout: blog
title: "How I Built a Toy Preview Environment Platform and What Happened Next"
subtitle: "Or: Some Stuff I Learned about How to Create Toy Environments and Write Kubernetes Operators."
description: "Or: Some Stuff I Learned about How to Create Toy Environments and Write Kubernetes Operators."
image: "/assets/images/preview-environments/jade.jpg"
image_caption: "Sometimes an <a href='https://en.wikipedia.org/wiki/Jadeite_Cabbage'>imitation</a> can be even harder to create than the real thing."
tags:
  - operators
  - kubernetes
  - preview environments
---

On most apps I've worked on, we've needed to run our app in different
environments.  We had the the "real" app (prod). We had the "preview" or
"staging" app that product managers, designers, and QA had access to. And we had
the "dev" app for iterating on locally.

The preview and dev environments grew organically. People hacked in little
quality of life improvements to make devs' lives better. Or to make designers' lives
better. They ended up diverging a lot, even though they were both "fake"
environments.

At Tilt, we help teams define dev environments, whereas our friends at
[Shipyard](https://shipyard.build/) help teams define preview environments.

Sometimes, Shipyard's CEO Benjie and I argue about why dev envs and preview envs
always seem to diverge so much. And if there are ways we could bring them back into alignment.
We have different takes on this:

- Benjie thinks that it should be easier to attach dev env tools to a preview env!

- I think that it should be easier to attach sharing/preview tools to a dev env!

You might notice the [obvious fallacy](https://danluu.com/cocktail-ideas/)
here. If you don't know much about a field, you think all its problems are
easily fixable.

But there's an easy way to fix this problem! I should build a toy preview env
platform and see what happens. In this post, I'm going to show you what I tried
to build, what I ended up building, and what I learned about it.

You should read this post if:

- You're a platform team trying to figure out how to set up dev envs and preview
  envs.

- You think Kubernetes is cool and want to write a Kubernetes operator (this is
  a great toy project for learning about operators).

- You're an infra nerd who wants to run throwaway Kubernetes clusters inside an
  existing Kubernetes cluster.

- You're a normal non-infra engineer who needs a way to test SSL subdomains locally.

We will cover all these things incidentally and try to be entertaining along the
way!

## What I Wanted to Build

We currently have a guide for [Tilt on CI](https://docs.tilt.dev/ci.html).

Most of our example projects have a CI job that creates a one-time-use
Kubernetes cluster, deploys servers to it, and waits for them all to be healthy.

For a preview environment platform, I wanted to create a small dashboard that
let you pick a repo, a branch, and a Tiltfile from a set of preconfigured
projects.

![Choose your preview environment](/assets/images/preview-environments/dashboard-1.jpg)

Once you choose your environment, we would create a new Kubernetes cluster, use
Tilt to set up the environment, then expose URLs for every service in the
environment.  Here's an example of what it should look like with two services:
the `tilt` dashboard and the `example-html` static HTML server.

![The preview environment has been chosen!](/assets/images/preview-environments/dashboard-2.jpg)

We want to be able to share this URL with other people on the team. We'll need
some sort of access control, but it's OK if the access control is coarse-grained
(e.g., everyone in my Github org.)

## What I Built

My preview app is called the ephemerator!

You can try it out here:

[preview.tilt.build](https://preview.tilt.build/){:.attached-above}

or you can checkout the code and run it locally here:

[ephemerator source code](https://github.com/tilt-dev/ephemerator){:.attached-above}

(We call it the ephemerator as a silly play on "**Ephemer**al environments).

You can skip this section if you don't care how it works.

The ephemerator consists of four services:

![preview.tilt.build architecture diagram](/assets/images/preview-environments/diagram.jpg)

- A dashboard that shows the status of your preview environment and lets you
  update the desired state (aka the spec).

- A controller that reads the desired state, the current status, and does work
  to make the current status match the desired state.

- An ingress that directs traffic. Once the environment is ready, the controller
  adds traffic rules to the ingress to create a subdomain for each service in
  the enviornment. This is an off-the-shelf [Ingress NGINX Controller](https://kubernetes.github.io/ingress-nginx/).
  
- An auth service that authenticates people with their Github logins. This is an
  off-the-shelf [OAuth2 Proxy](https://oauth2-proxy.github.io/). (Note that we
  don't use it as a proxy. The project has grown to support non-proxy modes 😁.)

Our platform stores all its desired state as Kubernetes ConfigMaps in the
namespace it runs in. When a user asks for a new environment, the dashboard
creates a new ConfigMap. The controller builds on top of the excellent [controller-runtime](https://github.com/kubernetes-sigs/controller-runtime) library. 

The controller continuously watches the ConfigMaps for changes.  When a new
ConfigMap appears, it creates a pod with two containers: a standalone
Docker-in-Docker container, and a Tilt Up container. The Tilt Up container
creates a brand new Kubernetes cluster using [K3D](https://k3d.io/).
Then uses Tilt to create all the services inside the inner cluster.

On our platform, the ConfigMap has a default expiration of 15 minutes. When the
ConfigMap expires, the controller tears down the one-time-use K3D cluster.

## What I Learned

OK! So this works. You can try it yourself. I hit a lot of gotchas. Some of them
surprised me but some of them are probebly obvious. There's one that all the
security nerds are probably screaming at me as they read this:

### Kubernetes In Kubernetes is not secure at all!!!

Or more precisely: Docker in Docker does not provide real isolation. There are
ways to break out. I loved this recent blog post about [security
vulnerabilities](
https://research.nccgroup.com/2022/01/13/10-real-world-stories-of-how-weve-compromised-ci-cd-pipelines/)
in CI/CD pieplines.

A preview environment is, after all, "Remote Code Execution Vulnerability as a Service."

In our preview environment service, we've tried to do a number of things to
reduce the chances that people will turn our cluster into a Bitcoin mining service:

- You can only run services from a whitelisted set of repos (which the Tilt team controls).

- Each user can only run one environment at a time.

- Although [preview.tilt.build](https://preview.tilt.build/) is open to anyone, the auth service
  can be configured to restrict access to a Github org or a set of accounts.
  
- Each change to an environment is logged and posted to a Slack channel.

- The environment pods run on their own service account without account tokens.

For members of the Tilt team, this is very much guardrails-level security. If a
team member with commit access to the example repos wanted to break out of the
environment into the outer cluster, they could without too much
trouble. But it should provide good guardrails against unintentional breakouts.

### Kubernetes in Kubernetes is easier than ever!

With all the security caveats out of the way, I do want to shout out to all the
people who have been working to make this possible at all. We appreciated:

- Radu Matei's [blog post on Kubernetes in Kubernetes for
  testing](https://radu-matei.com/blog/kubernetes-e2e-kind-brigade/)

- This [KIND issue](https://github.com/kubernetes-sigs/kind/issues/303)
  documenting additional settings for running Kubernetes in a pod.

- The K3D team's work on creating [a fast cluster and
  registry](https://k3d.io/v5.3.0/usage/registries/).

### Developing with Real Subdomains Locally Reveals so Many Issues

I'm still deeply bothered that so many apps run on random HTTP ports locally
(e.g., `localhost:3000`, `localhost:8080`). People have been lobbying for dev
environment subdomains like `*.localhost` and `*.test` [since
1999](https://datatracker.ietf.org/doc/html/rfc2606)! But it's still a PITA to
use them.

When I was developing `preview.tilt.build`, I set it up locally
as `preview.localhost`. Here's how I did it:

- I installed [`dnsmasq`](https://wiki.debian.org/dnsmasq) to map `localhost` subdomains to `127.0.0.1`.

- I used [the KIND team's guide](https://kind.sigs.k8s.io/docs/user/ingress/) to setting up 
  a cluster ingress mapped to port `127.0.0.1:80`.
  
- I created an ingress that mapped the subdomains and paths of `localhost` to different
  servers in my dev environment (e.g., the auth server, the dashboard server).

This worked well! I got to use human-readable names for my servers. I could test
authentication and real GitHub user accounts. And I could debug problems with
how cookies are shared across domains (cookies behave very differently for
top-level domains like `localhost` then for two- or three-level domains like
`preview.localhost`).

### Open Source Services FTW

I also wanted to shout out to the many open-source service I used to put this together:

- [`nginx`](https://www.nginx.com/) and
  [`nginx-ingress-controller`](https://kubernetes.github.io/ingress-nginx/) for
  traffic routing.

- [`controller-runtime`](https://github.com/kubernetes-sigs/controller-runtime)
  for writing a Kubernetes controller. If you haven't written a controller in a
  while, you should try it again, because the libraries have improved by leaps
  and bounds.
  
- [`cert-manager`](https://cert-manager.io/) for managing TLS certificates.

- [`mkcert`](https://github.com/FiloSottile/mkcert) for testing HTTPS locally.

## What I Left Out Because I'm Busy

When I finished up `ephemerator`, I compared it to the guide at
[`ephemeralenvironments.io`](https://ephemeralenvironments.io/). There are so
many things I wanted to build that I didn't even get to!

### Pull Request Triggers

Currently, you have to go to a dashboard to manually spin up a preview environment.

More and more, users are expecting the [env to spin up
automatically](https://ephemeralenvironments.io/features/dev-workflow/) on each
PR. And this seems to be becoming table stakes in Jamstack platforms like
Netlify and Vercel.

### Cost Control

A more mature preview env platform would destroy or scale down envs that aren't
  being used [to save on
  cost](https://ephemeralenvironments.io/features/cost-control/).
  
The ephmerator is very native: every env has a 15 minute expiry. Then it's destroyed.

I briefly considered using a framework like [`knative`
serving](https://knative.dev/docs/serving/). `knative` monitors the traffic to
your pod, turns it off if no one's using it, and spins it up again when a new request comes in.

But for learning purposes, I wanted to keep this tied to built-in Kubernetes
primitives.

### Scaling to Multiple Nodes

The ephemerator users Docker in Docker on a single node. So all the servers in
your dev environment must fit on a single machine.

A more secure architecture could use a dedicated VM per environment, or multiple
VMs per environment, with Kubernetes managing them.

### Secrets

All of the Tilt example repos are public. Checking them out and running them
doesn't require any secrets. So I didn't bother trying to propagate secrets to
the environments. If I did, I would need to handle two distinct sets of secrets:

- The auth token for the user creating the environment (e.g., the engineer who opened the PR).

- The auth token for the user interacting with the environment (e.g., the PM or designer testing the app).

In the ephemerator architecture, the OAuth2 Proxy passes a github access token
to both the dashboard service and the individual env services. Currently this
token is only authorized to read your email! But you could imagine requesting
more privileges, like the ability to checkout code from private repos, or to fetch
more secrets from a privileged secret store.

If the tokens had more privileges, we would need to be careful [to keep them
secure](https://ephemeralenvironments.io/features/security/)!

### Shared Data

When I've needed a preview environment in the past, a critical part has been
how we handled shared data. In particular:

- Product Managers and Designers want the data to reflect natural-looking user behavior.
  There's a whole industry around generating [good placeholder text](https://en.wikipedia.org/wiki/Lorem_ipsum)!
  
- QA and Integration Tests want the data to exercise lots of edge cases in ways
  that "normal users" wouldn't think to test. Like that [Reply All
  episode](https://gimletmedia.com/shows/reply-all/n8hxzr7/176-twicarus) about
  people that were accidentally able to register impossible Twitter usernames.
  
One idea I'd like to explore is to use the Kubernetes-in-Kubernetes structure for
shared services. You could have some sort of shared staging database in the
"host" cluster that all the "inner" envs can access. And you could switch
between a database of "natural" data and a database of "pushing-the-limits
edge-case" data.

## Future Work

We have no plans to build a Tilt-hosted preview enviroment service! This was a
wild experiment.

If you want to hack on it, the `ephemerator` repo [has
instructions](https://github.com/tilt-dev/ephemerator/blob/main/CONTRIBUTING.md)
on how to run it locally.

It's _probably_ safe for a small- to medium-sized team to run it on their own
Kubernetes cluster. Use it at your own risk. But I highly recommend you restrict
it to a whitelist of users and a whitelist of repos. The repo contains helm
charts for deploying it. Because it's experimental, it's probably not ready
for a place like [`artifacthub`](https://artifacthub.io/) for distributable Helm
charts.

If you don't want to build your own preview env service, check out
[Shipyard](https://shipyard.build)! You can give them money to think about the
security and operational issues. Maybe we will add some special Tilt/Shipyard
magic if people are interested.

I also want to experiment with the other direction: adding a way to attach dev
environment tools to an existing preview environment.
