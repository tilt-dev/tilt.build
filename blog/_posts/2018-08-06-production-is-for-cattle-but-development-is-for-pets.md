---
slug: production-is-for-cattle-but-development-is-for-pets
date: 2018-08-06T17:22:38.794Z
author: nick
layout: blog
canonical_url: "https://medium.com/windmill-engineering/production-is-for-cattle-but-development-is-for-pets-5f4ecba11f7d"
title: "Production is for Cattle, but Development is for Pets"
image: featuredImage.png
image_needs_slug: true
tags:
  - kubernetes
  - cloud-services
  - golang
keywords:
  - kubernetes
  - cloud-services
  - golang
---

Kubernetes makes it easy to manage herds of cattle: lots of servers running in production.

Today we're announcing [a simple, open-source tool `pets`](https://github.com/windmilleng/pets). `pets` makes it easy to manage herds of cats: lots of servers running on your machine that you want to keep a close eye on for local development.

### The Big Idea

`pets` is for the cloud-service developer who has multiple servers that they run for day-to-day feature work. Maybe the servers run as bare processes. Maybe they run in containers. Or in minikube. Or in a remote Kubernetes cluster.

We should be able to express the constellation of servers independently of how we start them. A `Petsfile` is like a `Makefile` for expressing how servers start and fit together. This lets us switch back and forth quickly between servers running locally and servers running in the cloud.

### When You Have Two Servers in One Repo

The simplest example of a `Petsfile` is when you have two servers in a single repo. This example uses the Go tools, but `pets` works with any programming language.

```
def backend_local():
  server = start("go run ./cmd/backend/main.go")
  return service(server, "localhost", 8080)

backend = "backend"
register(backend, "local", backend_local)

def frontend_local(b):
  server = start("go run ./cmd/frontend/main.go --backend=%s" % b["host"])
  return service(server, "localhost", 8081)

frontend = "frontend"
register(frontend, "local", frontend_local, deps=[backend])
```


Then run

```
$ pets up frontend
Pets ran "go run ./cmd/backend/main.go"
The service backend-local is now running
Pets ran "go run ./cmd/frontend/main.go --backend=localhost:8080"
The service frontend-local is now running
```


`pets` will automatically start frontend and all of its dependencies!

`pets` keeps track of which servers are currently running. You can list them with `pets list` :

```
$ pets list
Name                          Age
backend-local                 1m
frontend-local                1m
```


Or tear them down with `pets down` :

```
$ pets down
Stopping backend-local
Stopping frontend-local
```


### **When You Have Two Servers in Two Repos**

If you have servers in multiple repos that you want to run with `pets`, that’s OK too!

```
load("go-get://github.com/username/pets-example-backend", "backend")

def frontend_local(b):
  server = start("go run ./cmd/frontend/main.go --backend=%s" % b["host"])
  return service(server, "localhost", 8081)

frontend = "frontend"
register(frontend, "local", frontend_local, deps=[backend])
```


Then run

```
$ pets up frontend
```


The `load` function will use `go get` to fetch the repo. You can also use `load` with a relative path to point to another repo on your disk, if you expect the repo to be already checked out.

### **When You Want to Develop on Kubernetes**

Lastly, let’s talk about how this works when you want to run a frontend talking to a backend server in Kubernetes. This is when `pets` starts to shine.

```
# default backend with 'pets up'
def backend_local():
  server = start("go run ./cmd/backend/main.go")
  return service(server, "localhost", 8080)

backend = "backend"
register(backend, "local", backend_local)

# alternate backend with 'pets up --with=backend=k8s'
def backend_k8s():
  run("kubectl apply -f backend.yaml")
  server = start("kubectl port-forward deployment/backend 8080:8080")
  return service(server, "localhost", 8080)

register(backend, "k8s", backend_k8s)
```


Then, from the frontend repo, run:

```
$ pets up frontend --with=backend=k8s
Pets ran "kubectl apply -f backend.yaml"
Pets ran "kubectl port-forward deployment/backend 8080:8080"
The service backend-k8s is now running
Pets ran "go run ./cmd/frontend/main.go --backend=localhost:8080"
The service frontend-local is now running
```


Now you have a local frontend talking to a cloud-based backend. As you run more and more services, `pets` helps you to run them in increasingly complicated combinations.

For more documentation, check out [pets on Github](https://github.com/windmilleng/pets). Have fun!
