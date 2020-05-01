---
title: Choosing a Local Dev Cluster
layout: docs
---

How do you run Kubernetes locally?

There are lots of Kubernetes dev solutions out there. The choices can be overwhelming.
We're here to help you figure out the right one for you.

Beginner Level:

- [Kind](#kind)
- [Docker for Desktop](#docker-for-desktop)
- [Microk8s](#microk8s)

Intermediate Level:

- [Minikube](#minikube)
- [k3d](#k3d)

Advanced Level:

- [Amazon Elastic Kubernetes Service](#remote)
- [Azure Kubernetes Service](#remote)
- [Google Kubernetes Engine](#remote)
- [Custom Clusters](#custom-clusters)

---

## Kind

[Kind](https://kind.sigs.k8s.io/) runs Kubernetes inside a Docker container.

The Kubernetes team uses Kind to test Kubernetes itself. But its fast startup
time also makes it a good solution for local dev. Follow these instructions to
set up Kind for use with Tilt:

[**Kind Setup Instructions**](https://github.com/windmilleng/kind-local)

### Pros

- Creating a new cluster is fast (~20 seconds). Deleting a cluster is even faster. 
- Much more robust than Docker for Mac. Uses containerd instead of docker-shim. Short-lived clusters tend to be more reliable.
- Supports a local image registry (with our [custom setup instructions](https://github.com/windmilleng/kind-local)).
  Pushing images is fast. No fiddling with image registry auth credentials.
- Can run in [most CI environments](https://github.com/kind-ci/examples) (TravisCI, CircleCI, etc.)

### Cons

- The local registry setup is still new, and changing rapidly. You need to be using Tilt v0.12.0+
- If Tilt can't find the registry, it will use the much slower `kind load` to load images. (This
con is mitigated if you use Kind with a local registry, as described in the instructions linked above.)

---
## Docker for Desktop

Docker for Desktop is the easiest to get started with if you're on MacOS.

In the Docker For Mac preferences, click
[Enable Kubernetes](https://docs.docker.com/docker-for-mac/#kubernetes)

### Pros

- Widely used and supported.
- Nothing else to install.
- Built images are immediately available in-cluster. No pushing and pulling from image registries.

### Cons

- If Kubernetes breaks, it's easier to reset the whole thing than debug it.
- Much more resource-intensive because it uses docker-shim as the container runtime.
- Different defaults than a prod cluster and difficult to customize.
- Not available on Linux.

---


## MicroK8s

[Microk8s](https://microk8s.io) is what we recommend most often for Linux users.

Install:

```bash
sudo snap install microk8s --classic && \
sudo microk8s.enable dns && \
sudo microk8s.enable registry
```

Make microk8s your local Kubernetes cluster:

```bash
sudo microk8s.kubectl config view --flatten > ~/.kube/microk8s-config && \
KUBECONFIG=~/.kube/microk8s-config:~/.kube/config kubectl config view --flatten > ~/.kube/temp-config && \
mv ~/.kube/temp-config ~/.kube/config && \
kubectl config use-context microk8s
```

### Pros

- No virtual machine overhead on Linux
- Ships with plugins that make common configs as easy as `microk8s.enable`
- Supports a local image registry with `microk8s.enable registry`.
  Pushing images is fast.  No fiddling with image registry auth credentials.

### Cons

- Resetting the cluster is slow and error-prone.
- Optimized for Linux. You can use it on MacOS and Windows with [Multipass](https://multipass.run/).

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

## k3d

[k3d](https://github.com/rancher/k3d) runs [k3s](https://k3s.io/), a lightweight Kubernetes distro, inside a Docker container.

k3s is fully compliant with "full" Kubernetes, but has a lot of optional and legacy features removed.
Follow these instructions to set up k3d for use with Tilt:

[**k3d Setup Instructions**](https://github.com/windmilleng/k3d-local-registry/)

### Pros

- Extremely fast to start up (less than 5 seconds on most machines)
- It's easy to run k3d with a [local registry that Tilt will auto-detect](https://github.com/windmilleng/k3d-local-registry/),
which means less finicky setup, and fast pushing/pulling of images

### Cons

- Tilt does not yet natively support `k3d import-images`, so for a smooth local dev experience with
Tilt, you have to use a local image registry (which you get for free if you set up k3d using the
instructions linked above)
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

---

## Custom Clusters

If you're rolling your own Kubernetes dev cluster, and
want it to work with Tilt, there are two things you need to do.

- Tilt needs to recognize the cluster as a dev cluster.
- Tilt needs to be able to discover any in-cluster registry.

### Whitelisting the Cluster

Users have to explicitly whitelist the cluster with this line in their Tiltfile:

```python
allow_k8s_contexts('my-cluster-name')
```

If your cluster is a dev-only cluster that you think Tilt should
recognize automatically, we accept PRs to whitelist the cluster in Tilt.
Here's an example:

[Recognize Red Hat CodeReady Containers as a local cluster](https://github.com/windmilleng/tilt/pull/3242)

### Discovering the Registry

A local registry is often the fastest way to speed up your dev experience.

Every cluster sets up this registry slightly differently. 

To discover the registry, Tilt reads two annotatons from the node of your Kubernetes cluster:

- `tilt.dev/registry`: The host of the registry, as seen by your local machine.
- `tilt.dev/registry-from-cluster`: The host of the registry, as seen by your
  cluster. If omitted, Tilt will assume that the host is the same as
  `tilt.dev/registry`.

Our cluster-specific setup scripts often have a shell script snippet like:

```bash
nodes=$(kubectl get nodes -o go-template --template='{% raw %}{{range .items}}{{printf "%s\n" .metadata.name}}{{end}}{% endraw %}')
if [ ! -z $nodes ]; then
  for node in $nodes; do
    kubectl annotate node "${node}" \
        tilt.dev/registry=localhost:5000 \
        tilt.dev/registry-from-cluster=registry:5000
  done
fi
```

to help Tilt find the registry.
