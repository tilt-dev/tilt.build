---
title: Choosing a Local Dev Cluster
description: "How do you run Kubernetes locally? There are lots of Kubernetes dev solutions out there. The choices can be overwhelming. We're here to help you figure out the right one for you."
layout: docs
sidebar: gettingstarted
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
- [Rancher Desktop](#rancher-desktop)

Advanced Level:

- [Amazon Elastic Kubernetes Service](#remote)
- [Azure Kubernetes Service](#remote)
- [Google Kubernetes Engine](#remote)
- [Custom Local Clusters](#custom-local-clusters)

---

## Kind

[Kind](https://kind.sigs.k8s.io/) runs Kubernetes inside a Docker container.

The Kubernetes team uses Kind to test Kubernetes itself. But its fast startup
time also makes it a good solution for local dev. Use `ctlptl` to set up Kind with a registry:

[**Kind Setup**](https://github.com/tilt-dev/ctlptl#kind-with-a-built-in-registry-at-a-random-port){:.attached-above}

### Pros

- Creating a new cluster is fast (~20 seconds). Deleting a cluster is even faster. 
- Much more robust than Docker for Mac. Uses containerd instead of docker-shim. Short-lived clusters tend to be more reliable.
- Supports a local image registry (with our [Kind setup tool](https://github.com/tilt-dev/ctlptl#kind-with-a-built-in-registry-at-a-random-port)).
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

---


## MicroK8s

[Microk8s](https://microk8s.io) is what we recommend most often for Ubuntu users.

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
- Optimized for Ubuntu. In theory, works on any Linux that supports
  [Snap](https://snapcraft.io/) and on MacOS/Windows with
  [Multipass](https://multipass.run/), but it's
  not as stable on those platforms.

---

## Rancher Desktop
[Rancher Desktop](https://rancherdesktop.io/) is an open source alternative for Docker Desktop. 
By default it uses `containerd` but since [v0.7.0](https://github.com/rancher-sandbox/rancher-desktop/releases/tag/v0.7.0), 
users are free to choose a `dockerd` runtime

Rancher Desktop is still `pre-release` and continuously being updated, so
be aware that features might change quickly and radically.

For more information on how to use Rancher Desktop with Tilt, you can check out 
the [`kim` Tilt extension](https://github.com/tilt-dev/tilt-extensions/tree/master/kim) and [this blogpost](https://blog.tilt.dev/2021/09/07/rancher-desktop.html).

### Pros
- Cross platform (macOS/Linux/Windows)
- Uses [k3s](https://k3s.io), which is very fast to start and light on resources

### Cons
- New and quickly evolving, might not be fully supported by all tools (including Tilt!)
- No local registry out-of-the-box

---

## Minikube

[Minikube](https://github.com/kubernetes/minikube) is what we recommend when
you're willing to pay some overhead for a more high-fidelity cluster.

Minikube has tons of options for customizing the cluster. You can choose between
a VM and a Docker container for running a machine, choose from different
container runtimes, and more.

Follow these instructions to set up Minikube for use with Tilt:

[**Minikube Setup**](https://github.com/tilt-dev/ctlptl#minikube-with-a-built-in-registry){:.attached-above}

### Pros

- The most full-featured local Kubernetes solution
- Can easily run different Kubernetes versions, container runtimes, and controllers
- Supports a local image registry (with our [cluster setup tool](https://github.com/tilt-dev/ctlptl#minikube-with-a-built-in-registry)).
  Pushing images is fast. No fiddling with image registry auth credentials.

### Cons

- We often see engineers struggle to set it up the first time, getting lost in a
  maze of VM drivers that they're unfamiliar with.
- Minikube gives you lots of options, but many of them are difficult to use
  or require manual setup. 
- Beware if using a VM instead of a Docker container to run your cluster.
  You'll usually want to shut down Minikube when you're finished because of the VM's drain on your resources.

---

## k3d

[k3d](https://github.com/rancher/k3d) runs [k3s](https://k3s.io/), a lightweight Kubernetes distro, inside a Docker container.

k3s is fully compliant with "full" Kubernetes, but has a lot of optional and legacy features removed.

### Pros

- Extremely fast to start up (less than 5 seconds on most machines)
- k3d has [a built-in local
registry](https://k3d.io/usage/guides/registries/#using-a-local-registry) that's
explicitly designed to work well with Tilt. Start k3d with the local registry to make pushing
and pulling images fast.

### Cons

- The least widely used. That's not _necessarily_ bad. Just be aware that
  there's less documentation on its pitfalls. Tools (including the Tilt team!)
  tend to be slower to add support for it.

---

## Remote

### (EKS, AKS, GKE, and [custom clusters](https://medium.com/@cfatechblog/bare-metal-k8s-clustering-at-chick-fil-a-scale-7b0607bd3541))

By default, Tilt will not let you develop against a remote cluster.

If you start Tilt while you have `kubectl` configured to talk to a remote
cluster, you will get an error. You have to explicitly allow the cluster 
using [allow_k8s_contexts](api.html#api.allow_k8s_contexts):

```python
allow_k8s_contexts('my-cluster-name')
```

If your team connects to many remote dev clusters, a common approach is to
disable the check entirely and add your own validation:

```python
allow_k8s_contexts(k8s_context())
local('./validate-dev-cluster.sh')
```

We only recommend remote clusters for large engineering teams where a
dedicated dev infrastructure team can maintain your dev cluster.

Or if you need to debug something that only reproduces in a complete cluster.

### Pros

- Can customize to your heart's desire
- Share common services (e.g., a dev database) across developers
- Use a cheap laptop and the most expensive cloud instance you can buy for development

### Cons

- Need to use a remote image registry. Make sure you have Tilt's `live_update` set up!
- Need to set up namespaces and access control so that each dev has their own sandbox
- If the cluster needs to be reset, we hope you're good friends with your DevOps team

---

## Custom Local Clusters

You can use Tilt to develop on a home lab with a locally-installed cluster like
[K3s](https://k3s.io/) or [K0s](https://k0sproject.io/).

To make a custom local cluster work, there are two things you need to do:

- Tilt needs to recognize the cluster as a dev cluster.
- Tilt needs to be able to discover any in-cluster registry.

### Allowing the Cluster

Users have to explicitly allow the cluster with this line in their Tiltfile:

```python
allow_k8s_contexts('my-cluster-name')
```

If your cluster is a dev-only cluster that you think Tilt should
recognize automatically, we accept PRs to allow the cluster in Tilt.
Here's an example:

[Recognize Red Hat CodeReady Containers as a local cluster](https://github.com/tilt-dev/tilt/pull/3242)

### Discovering the Registry

A local registry is often the fastest way to speed up your dev experience.

Every cluster sets up this registry slightly differently.

Tilt-team is currently collaborating with the Kubernetes community on protocols
for discovery, so that microservice development tools like Tilt will auto-configure
when a local registry is present.

Tilt currently supports two generic protocols for discovering your cluster's
local registry, so you don't have to do any configuration yourself. The
Kubernetes standard protocol is a
[KEP](https://github.com/kubernetes/enhancements/tree/master/keps#kubernetes-enhancement-proposals-keps)
that has been vetted by the Kubernetes community.  The annotation-based protocol
is used in legacy Tilt scripts.

You can configure the registry manually in your Tiltfile if these options
fail. We've documented all the options below.

#### Kubernetes Standard Registry Discovery

The standard protocol uses configmaps in the `kube-public` namespace of your cluster.

If you have a local registry running at `localhost:5000`, apply the following
config map to your cluster:

```
apiVersion: v1
kind: ConfigMap
metadata:
  name: local-registry-hosting
  namespace: kube-public
data:
  localRegistryHosting.v1: |
    host: "localhost:5000"
```

Tilt will automatically detect your local registry, and will push and pull
images from it.

For more details on how to use this configmap, see

- [The Kubernetes Enhancement Proposal](https://github.com/kubernetes/enhancements/tree/master/keps/sig-cluster-lifecycle/generic/1755-communicating-a-local-registry)

- [A sample implementation in Go](https://github.com/tilt-dev/localregistry-go)

We're working with local development cluster teams to ensure that clusters
support this protocol when they have a built-in registry.

#### Legacy Annotation-based Registry Discovery

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

#### Manual Configuration

You can manually configure the registry in your Tiltfile with
[`default_registry`](api.html#api.default_registry).

```python
default_registry('gcr.io/my-personal-registry')
```

Because the Tiltfile is scriptable, you can configure this to fit your team's conventions:

```python
reg = os.environ.get('MY_PERSONAL_REGISTRY', '')
if reg:
  default_registry(reg)
```
