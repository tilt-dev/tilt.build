---
title: Frequently Asked Questions
layout: docs
---

Troubleshooting
----------------------------

### Q: How do I get help with Tilt?

For real-time support, find us on the Kubernetes slack. Get an invite at [slack.k8s.io](http://slack.k8s.io) and find
us in [the **#tilt** channel](https://kubernetes.slack.com/messages/CESBL84MV/).

You can also file an issue in [our GitHub repo](https://github.com/windmilleng/tilt/issues/new).

For help with private issues (like security vulnerabilities or just concerning non-public code),
please email [help@tilt.dev](mailto:help@tilt.dev).

### Q: When I run `tilt version`, I see "template engine not found for: version". What do I do?

There is another project called Tilt for
[developing Ruby templates](https://github.com/rtomayko/tilt).

You're accidentally running that Tilt instead.

Common fixes include deleting the other Tilt, always using an absolute path, or
renaming Tilt to `tlt` to avoid the conflict. Tilt is a static binary so it is OK to
rename it.

### Q: I'm getting push errors like "unauthorized: You don't have the needed permissions". What do I do?

If Tilt is trying to do a push, that means it thinks you wanted to deploy to a
remote cluster. See [below](faq.html#q-how-do-i-change-what-kubernetes-cluster-tilt-uses) on how
to configure for a local cluster.

### Q: Tilt fails with "Unable to connect to cluster" errors. What do I do?

The Kubernetes server that you're trying to deploy to is misbehaving.

Two common things to try are:

1. Turn it off and turn it back on again (really!).

2. Reset the cluster state.

But the specific way to do these depend on your environment.

If you're using Docker For Mac, click the Docker icon in the upper-right hand
corner of your screen. Choose "Preferences..." to open a dialog. The
"Kubernetes" tab has a button that allows you to enable/disable Kubernetes. The
"Reset" tab has a button that allows you to reset the cluster state.

If you're using Minikube, `minikube stop` and `minikube start` will restart the
environment. `minikube delete` will reset the cluster state.

### Q: Tilt is using a lot of CPU. What is it doing?

We're always working to improve Tilt performance.

If you send us a CPU profile, that can help us to narrow down and fix any performance issues you're having.

To collect a CPU profile:

1. Run `tilt`

2. Press `ctrl-p` in the terminal to start recording. You should see a message like "starting pprof profile to tilt.profile"

3. Interact with Tilt normally

4. Press `ctrl-p` again to stop recording

Tilt will create a file `tilt.profile` with CPU statistics. It shouldn't contain
any personally identifiable info, but just to be safe, email the file to
[help@tilt.dev](mailto:help@tilt.dev). We will do our
best to figure it out!

### Q: Tilt says it's building images. But I can't find them with the Docker CLI. What's going on?

If you are using Minikube or MicroK8s, Tilt will automatically connect to the
Docker server inside the cluster. This helps performance because Tilt doesn't need to waste time
copying Docker images around.

To check which Docker server Tilt is connecting to, run:

```bash
tilt doctor
```

Tilt will print the Docker host. You can then run commands against that Docker host:

```
DOCKER_HOST=tcp://my-url/ docker images
```

### Q: All the Tilt examples store the image at `gcr.io`. Isn't it really slow to push images up to Google's remote repository for local development?

You're right, that would be slow!

Most local Kubernetes development solutions let you build images directly inside
the cluster. There's no need to push the image to a remote repository.

When you're using Docker for Mac, Minikube, or MicroK8s, Tilt will automatically build the
images in-cluster. When it detects this case, it will even modify your
Kubernetes configs to set ImageNeverPull, so that Kubernetes will emit an error
if it even tries to pull an image from a remote server.

### Q: Docker Buildkit is cool! How do I use it?

[BuildKit](https://github.com/moby/buildkit) is a new build engine in
Docker for building container images.

Tilt will automatically enable Buildkit if your local Docker installation
supports it.

BuildKit is supported on Docker v18.06 when Experimental mode is enabled, and on
Docker v18.09+

### Q: How do I tell Tilt to build my images with a remote Docker server?

Tilt reads the same environment variables as the `docker` command for choosing a
server. Specifically:

- `DOCKER_HOST`: Set the url to the docker server.
- `DOCKER_API_VERSION`: Set the version of the API.
- `DOCKER_CERT_PATH`: Set the path to load the TLS certificates from.
- `DOCKER_TLS_VERIFY`: To enable or disable TLS verification when using `DOCKER_CERT_PATH`, off by default.

This is helpful if you have a more powerful machine in the cloud that you want
to build your images.

### Q: How do I change what Kubernetes cluster Tilt uses?

Tilt uses the default Kubernetes cluster configured in `kubectl`.

To see what cluster `kubectl` uses, run:

```bash
kubectl config current-context
```

To see what clusters are available, run:

```bash
kubectl config get-contexts
```

To change the cluster you're deploying to, run:

```bash
kubectl config use-context docker-desktop
```

The most common options we see in local development are
`microk8s`, `docker-desktop` (Docker For Mac stable), and
`docker-for-desktop` (older Docker for Mac versions).

### Q: What local Kubernetes solution should I choose?

Check out our [Guide to Choosing a Local Cluster](choosing_clusters.html).

<script src="/assets/js/links.js" async></script>
