---
slug: "kubefwd-operator"
date: 2021-09-09
author: nick
layout: blog
title: "How to Automagically Setup `kubefwd` to Bulk-Forward Ports"
subtitle: "A walkthrough of Tilt's kubefwd operator"
description: "A walkthrough of Tilt's kubefwd operator"
image: "/assets/images/kubefwd-operator/bulk.jpg"
image_caption: "A truck bulk-forwarding glass, plastic, and metal. Kubernetes networking isn't trash! From Tilt Dev's field trip to the <a href='https://en.wikipedia.org/wiki/Sunset_Park_Material_Recovery_Facility'>Sunset Park Material Recovery Facility.</a>"
tags:
  - api
  - bash
  - extensions
  - kubefwd
---

[`kubefwd`](https://kubefwd.com/) is a tool that makes network magic so
you can access services from localhost the same way you would from inside a
cluster. For example, I could access `http://elasticsearch:9200/` directly from
localhost -- something that would normally only work for services within a cluster.

It's a great tool for getting started with Kubernetes. We even recommend it for
folks who want to learn more about how Kubernetes works.

But it can be hard to use unless you understand how it works under the
hood. When you start `kubefwd`, it:

1) Watches all the services in your cluster.

2) Creates DNS entries in /etc/hosts [the same way Kubernetes DNS would](https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/).

3) Resolves the services to pods in your cluster.

4) Forwards the DNS traffic from your local network to the right pods.

Because `kubefwd` needs to edit `/etc/hosts`, it needs `sudo` access.

Some Tilt users run `kubefwd` on the side (in a separate terminal)
so they can give it `sudo` access without giving all of Tilt `sudo` access.
They also want to be able to restart it, because sometimes it can get wedged
and stuck forwarding traffic to the wrong pod.

But what if we could make running `kubefwd` less awkward?!

It turns out we can! 

In this post, we'll talk a bit about the ideal dev experience we aimed for with
`kubefwd`, and about the extension we came up with to implement that goal

In the process, we also hope to show you that writing operators for your own
tasks doesn't have to be complicated at all!

## The `kubefwd` extension

If you simply want to use `kubefwd` right now, add this to your Tiltfile:

```
v1alpha1.extension_repo(name='default', url='https://github.com/tilt-dev/tilt-extensions')
v1alpha1.extension(name='kubefwd:config', repo_name='default', repo_path='kubefwd')
```

When Tilt starts, you should get a GUI prompt for your `sudo` password.

You'll see two new resources appear in your dashboard: the `kubefwd`
configuration and the `kubefwd` runner:

![kubefwd Dashboard](/assets/images/kubefwd-operator/kubefwd-dashboard.jpg)

If you click into the runner, you'll see what URLs it's forwarding. You'll also
see a "Refresh" button that you can use to restart `kubefwd` when it gets
wedged.

![kubefwd Logs](/assets/images/kubefwd-operator/kubefwd-logs.jpg)

But unlike when using the CLI, the "Refresh" button doesn't require `sudo`! And
we didn't need to tell `kubefwd` what namespaces to watch.  It figured it out on
it's own.

How does that work?

## The dev experience we wanted for `kubefwd`

We had a couple basic requirements in mind:

1. `kubefwd` can be a dangerous tool! We do think you should get a security prompt when Tilt wants to use it.

1. You shouldn't need an extra terminal open for `sudo` passwords.

1. Restarting it when it's wedged shouldn't require the same prompt.

1. We should automatically `kubefwd` any namespaces that Tilt is deploying to.

With that in mind, we broke down our `kubefwd` operator into a few different pieces:

### Coordinating `kubefwd` restarts

The `kubefwd` extension creates a temp file for sharing state between
pieces. The configuration looks [like
this](https://github.com/tilt-dev/tilt-extensions/tree/e43897e7f540b7a5023d87aefe8941ddb3bb8c3a/kubefwd/Tiltfile):

```python
# Tiltfile

# Creates a temp file for sharing state.
trigger_file = str(local('mktemp --suffix -tilt-kubefwd')).strip()

# Creates a button that refreshes the kubefwd without
# requiring new credentials.
local(['./create-refresh-button.sh', trigger_file])

# Runs a server that watches the tempfile.
local_resource(
  name='kubefwd:run',
  serve_cmd=['./sudo-kubefwd.sh', trigger_file])
```

This lets us use `entr`, another great tool, to automatically restart kubefwd
whenever our state file changes.

```bash
echo "$TRIGGER" | "$ENTR" -rn "$DIR/run-kubefwd-internal.sh"
```

We've written a lot about `entr` in the past. It's a perfect little tool for
[steering auto-restarts](https://eradman.com/entrproject).

### Restarting `kubefwd` on click

When the extension starts, it registers a button with the Tilt API. Here's [the
script that registers the
button](https://github.com/tilt-dev/tilt-extensions/tree/e43897e7f540b7a5023d87aefe8941ddb3bb8c3a/kubefwd/create-refresh-button.sh):

```bash
# create-refresh-button.sh

cat <<EOF | tilt apply -f -
apiVersion: tilt.dev/v1alpha1
kind: UIButton
metadata:
  name: kubefwd:refresh
spec:
  text: Refresh
  location:
    componentType: resource
    componentID: kubefwd:run
---
apiVersion: tilt.dev/v1alpha1
kind: Cmd
metadata:
  name: kubefwd:refresh
  annotations:
    "tilt.dev/resource": "kubefwd:run"
spec:
  args: ["touch", "$TRIGGER"]
  startOn:
    uiButtons:
    - kubefwd:refresh
EOF
```

Tilt users frequently [use the button
API](https://blog.tilt.dev/2021/07/08/uibutton-navbar.html) to add their own dev
env tasks.

### Automagically watching namespaces

Lastly, we can use the [KubernetesDiscovery
API](https://api.tilt.dev/kubernetes/kubernetes-discovery-v1alpha1.html) to
figure out [what namespaces](https://github.com/tilt-dev/tilt-extensions/tree/e43897e7f540b7a5023d87aefe8941ddb3bb8c3a/kubefwd/watch-namespaces.sh) Tilt is deploying your resources to.

```bash
#!/bin/bash
# watch-namespaces.sh
#
# Continuously watch the namespaces that we're deploying to, and write them to
# the trigger file.

TRIGGER_FILE="$1"

tilt get kubernetesdiscovery --watch -o name | while read -r; do
    NEW_NAMESPACES=$(tilt get kubernetesdiscovery -o=jsonpath='{.items[*].spec.watches[*].namespace}' | tr -s ' ' '\n' | sort -u)
    OLD_NAMESPACES=$(cat "$TRIGGER_FILE")
    if [[ "$NEW_NAMESPACES" != "$OLD_NAMESPACES" ]]; then
        echo "$NEW_NAMESPACES" > "$TRIGGER_FILE"
    fi
done
```

(When we're writing tooling, we often abbreviate `tilt get kubernetesdiscovery`
to `tilt get kd` or `tilt get kdisco` 🕺).

Our namespace watcher is a simple reconciler: it's continuously watching what
namespaces we're deploying to and what namespaces we're `kubefwd`-ing, then
making sure they match.

## Wrapping Up

There are still a few things we'd like to add to the extension.

We're working with our partner teams to make it work well even if you're running
Tilt in an SSH session. Or to configure it to `kubefwd` to namespaces you're not
deploying to.

We're also happy to pair on how to adapt it to your own environment!
