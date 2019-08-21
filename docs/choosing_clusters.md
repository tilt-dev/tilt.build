---
title: Choosing a Local Dev Cluster
layout: docs
---

How do you run Kubernetes locally?

There are lots of Kubernetes dev solutions out there. The choices can be overwhelming.
We're here to help you figure out the right one for you.

Beginner Level:

- [Docker for Desktop](#docker-for-desktop)
- [Microk8s](#microk8s)

Intermediate Level:

- [Minikube](#minikube)
- [KIND](#kind)
- [K3D](#k3d)

Advanced Level:

- [Amazon Elastic Kubernetes Service](#remote)
- [Azure Kubernetes Service](#remote)
- [Google Kubernetes Engine](#remote)

---

## Docker for Desktop

Docker for Desktop is what we recommend most often for MacOS users.

In the Docker For Mac preferences, click
[Enable Kubernetes](https://docs.docker.com/docker-for-mac/#kubernetes)

### Pros

- Widely used and supported.
- Nothing else to install.
- Built images are immediately available in-cluster. No pushing and pulling from image registries.

### Cons

- If Kubernetes breaks, it's easier to reset the whole thing than debug it.
- Different defaults than a prod cluster and difficult to customize.
- Not available on Linux.

---

## MicroK8s

[Microk8s](https://microk8s.dev) is what we recommend most often for Linux users.

Install:

```bash
sudo snap install microk8s --classic && \
microk8s.enable dns && \
microk8s.enable registry
```

Make microk8s your local Kubernetes cluster:

```bash
sudo microk8s.kubectl config view --flatten > ~/.kube/microk8s-config
KUBECONFIG=~/.kube/microk8s-config:~/.kube/config kubectl config view --flatten > ~/.kube/temp-config
mv ~/.kube/temp-config ~/.kube/config
kubectl config use-context microk8s
```

### Pros

- No virtual machine overhead
- Ships with plugins that make common configs as easy as `microk8s.enable`
- The in-cluster registry makes image updates much faster. When you enable the registry, Tilt will use it automatically.

### Cons

- Resetting the cluster is slow and error-prone
- Containerd-only
- Linux-only

---

## Minikube

[Minikube](https://github.com/kubernetes/minikube) is what we recommend when
you're willing to pay some overhead for a more high-fidelity cluster.

Minikube creates a Kubernetes cluster in a VM, and has tons of options for
customizing the cluster.

### Pros

- The most full-featured local Kubernetes solution
- Can easily run different Kubernetes versions, container runtimes, and controllers
- You can build images in-cluster with `minikube docker-env`. When you use
Minikube, Tilt will automatically use Minikube's Docker, so that you don't need
to push to a remote registry.

### Cons

- The VM makes everything much slower, both at start-time and run-time
- We often see engineers struggle to set it up the first time, getting lost in a
  maze of VM drivers that they're unfamiliar with
- You usually want to shutdown minikube when you're finished

---

## KIND

[KIND](https://kind.sigs.k8s.io/) runs Kubernetes inside a Docker container.

The Kuberetes team uses KIND to test Kubernetes itself. But its fast startup
time also makes it a good solution for local dev. Run it with:

```bash
GO111MODULE="on" go get sigs.k8s.io/kind@v0.4.0
kind create cluster
export KUBECONFIG="$(kind get kubeconfig-path)"
```

### Pros

- Fast to startup (less than 45 seconds on most machines)
- Creating and deleting ephemeral clusters feels great
- Can run in [most CI environments](https://github.com/kind-ci/examples) (TravisCI, CircleCI, etc)

### Cons

- Pushing images into the cluster is slow.
- KIND can copy images into the cluster with `kind load`. This is slower than an
  in-cluster registry because it copies the whole image even if a single layer
  has changed. But it's still faster than a remote registry. Tilt will use `kind
  load` if it detects KIND.
- We have [examples](https://github.com/windmilleng/kind-local) on how to run an
  in-cluster registry, but it's brittle.

---

## K3D

[K3D](https://github.com/rancher/k3d) runs K3s, a lightweight Kubernetes distro, inside a Docker container.

K3s is fully compliant with "full" Kubernetes, but has a lot of optional and
legacy features removed.

```bash
curl -sfL https://get.k3s.io | sh -
k3d create cluster
export KUBECONFIG="$(k3d get-kubeconfig --name='k3s-default')"
```

### Pros

- Extremely fast to start up (less than 5 seconds on most machines)

### Cons

- Pushing images into the cluster is slow.
- Tilt does not yet natively support `k3d import-images`, which has all the same problems as `kind load`.
- The least widely used. That's not _necessarily_ bad. Just be aware that there's less documentation on its pitfalls. Tools (including the Tilt team!) tend to be slower to add support for it.

---

## Remote

### (EKS, AKS, GKE, and [custom clusters](https://medium.com/@cfatechblog/bare-metal-k8s-clustering-at-chick-fil-a-scale-7b0607bd3541))

By default, Tilt will not let you develop against a remote cluster.

If you start Tilt while you have `kubectl` configured to talk to a remote
cluster, you will get an error. You have to explicitly whitelist the cluster with:

```python
allow_k8s_contexts('my-cluster-name')
```

We only recommend remote clusters for large engineering teams where a
dedicated dev infrastructure team can maintain your dev cluster.

Or if you need to debug something that only reproduces in a complete cluster.

### Pros

- Can customize to your heart's desire
- Share common services (e.g., a dev database) across developers
- Use a cheap laptop and the most expensive cloud instance you can buy for development

### Cons

- Need to use a remote image registry. Make sure you have Tilt's [live_update](live_update_tutorial.html) set up!
- Need to set up namespaces and access control so that each dev has their own sandbox
- If the cluster needs to be reset, we hope you're good friends with your DevOps team





