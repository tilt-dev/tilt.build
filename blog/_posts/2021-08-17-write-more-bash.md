---
slug: "write-more-bash"
date: 2021-08-17
author: nick
layout: blog
title: "Write More Bash to Hack Features Faster and with Less Testing"
subtitle: "A walkthrough of the 'cancel' button extension"
description: "A walkthrough of the 'cancel' button extension"
image: "/assets/images/write-more-bash/bonk.jpg"
image_type: "contain"
tags:
  - api
  - bash
---

The KubeCon schedule was announced last week. The Tilt team is giving two talks
😇.

- ["Beyond Kubernetes Security"](https://sched.co/lV4f) - A "blockbuster action thriller."
- ["The Control Loop as an Application Development Framework"](https://sched.co/lV1E) - How to write apps with more control loops.

Both talks are tangentially related to Tilt at best! They're mostly about
Kubernetes, the ideas behind Kubernetes, and how those ideas can (and should!)
affect your life as a dev.

In the Control Loop talk, I'm going to talk more about the Kubernetes ideas and
libraries that Tilt is built on top of. The Kubernetes libraries have a lot of
tools to help us build robust systems, which, sure, some people find value in.
But far, far more importantly, they also have a lot of tools that let you hack
together shit fast in Bash.

What does this look like when we're developing Tilt? I'm going to show you a
Bash-based Tilt extension I wrote last week! And as we go through it, you'll learn:

- Why Kubernetes stuff lends itself so well to Bash
- What a Bash-based Tilt extension looks like
- How you too can hack stuff into Tilt with Bash

## Why Kubernetes stuff lends itself so well to Bash

The core idea of Kubernetes is simple: if you want to manage servers, you need a way
to react to changes at runtime.

On top of that, Kubernetes offers a suite of data models, HTTP APIs, and CLIs
that are really consistent and well thought-out! (See: ["Kubernetes Is So Simple
You Can Explore it with
Curl"](https://blog.tilt.dev/2021/03/18/kubernetes-is-so-simple.html).)

This API platform allows teams to create very complex, robust features.
But few people appreciate that you can also use it to build simple, hacky features!

Tilt is built on top of the Kubernetes API server. So we can use these hacky
features too. To contribute to Tilt, you don't have to worry about getting code
into `main`, or sending pull requests, or asking for review, or breaking
existing code. You can can write it in any language you want.

A few weeks ago [L](https://twitter.com/ellenkorbes) asked if we could add a
cancel button to the Tilt UI to kill a running local server. And I realized that you could
hack this together with a couple dozen lines of Bash without modifying core Tilt! Here it is!

[Cancel](https://github.com/tilt-dev/tilt-extensions/tree/master/cancel) - adds a 'cancel' button for any resource that adds a `local_resource()`.

All you need to do is add this line to your Tiltfile!

```python
include('ext://cancel')
```

## What a Bash-based Tilt extension looks like

A reactive control loop looks the same for every feature: 

1. Watch objects
2. When objects change, check if the expected state matches the desired state.
3. If they don't match, do stuff

For a cancel button, that means:

1. Watch all local resources
2. When the local resources change, check if they want cancel buttons or need cancel buttons.
3. If "want" != "need", do stuff!

OK. To start, we add a new server for adding cancel buttons. We call it `operator:cancel`. Here's
what [the configuration](https://github.com/tilt-dev/tilt-extensions/blob/master/cancel/Tiltfile) looks like:

```python
local_resource(
  name='operator:cancel',
  serve_cmd='./cancel_btn_controller.sh')
```

"Operator" and "Controller" are both common words the Kubernetes ecosystem uses for 
the implementation code behind a feature.

Next, we write [a basic
loop](https://github.com/tilt-dev/tilt-extensions/blob/master/cancel/cancel_btn_controller.sh)
in Bash that watches objects for changes:

```bash
#!/bin/bash
#
# Starts a controller that watches for new Cmds, and
# creates buttons to cancel them.

set -eou pipefail


echo "operator:cancel runs in the background and listens to Tilt
When there are commands to cancel, operator:cancel adds a Cancel button to the Tilt UI
"

tilt get cmd --watch -o name | while read -r cmd_full_name; do
    cmd_short_name=${cmd_full_name#cmd.tilt.dev/}
    ./reconcile_cancel_btn.sh "$cmd_short_name"
done
```

This code uses Tilt's [Cmd API](https://api.tilt.dev/core/cmd-v1alpha1.html) to
watch all local commands. Tilt's CLI reuses large parts of `kubectl`, and has
many of the same verbs.  You can use `tilt api-resources` to look at all the
available objects, `tilt get` to view a summary of those objects, and `tilt get
--watch` to watch for updates to those objects.

This Bash loop streams Cmd changes and passes them to a "reconciler."

"Reconciler" is another common phrase in the Kubernetes ecosystem for the part
of a controller that implements steps (2) and (3) of the reactive control loop
above: it compares the live state to the desired state, and applies changes to
the live state to bring it to the desired state.

You can read more about reconcilers
in [The Kubebuilder Tutorial](https://book.kubebuilder.io/cronjob-tutorial/controller-overview.html)
or in the [Cloud-Native Infrastucture book](https://www.oreilly.com/library/view/cloud-native-infrastructure/9781491984291/).

The reconciler checks to see if the Cmd should have a cancel button, then
generates the description of that button. Here's an abridged version that
handles creating the button but not deleting the button. (You can read [the full
source
code](https://github.com/tilt-dev/tilt-extensions/blob/master/cancel/reconcile_cancel_btn.sh)
to see how we delete buttons.)

```bash
cancel_cmd_name="$cmd_name:cancel"
cancel_button_name="$cmd_name:cancel"
cmd=$(tilt get cmd "$cmd_name" -o json --ignore-not-found)

# If the command isn't running or doesn't exist, disable the button
pid=$(echo "$cmd" | jq -r '.status.running.pid')
disabled="false"
if [[ "$pid" == "" || "$pid" == "null" ]]; then
    disabled="true"
fi

dir=$(realpath "$(dirname "$0")")
cat <<EOF | tilt apply -f -
apiVersion: tilt.dev/v1alpha1
kind: UIButton
metadata:
  name: $cancel_button_name
spec:
  disabled: $disabled
  text: Cancel
  location:
    componentType: resource
    componentID: $resource
---
apiVersion: tilt.dev/v1alpha1
kind: Cmd
metadata:
  name: $cancel_cmd_name
  annotations:
    "tilt.dev/resource": "$resource"
    "tilt.dev/log-span-id": "$cancel_cmd_name"
spec:
  args: ["./kill_cmd.sh", "$cmd_name"]
  dir: $dir
  startOn:
    uiButtons:
    - $cancel_button_name
EOF
```

The `cancel` command and the button that triggers this `cancel` command are
objects. They're specified like any other object in the Kubernetes ecosystem -
as YAML. Because our control loop reacts to all changes, it can disable the
`cancel` button when the command exits.

`tilt apply` is a thin wrapper around `kubectl apply`. Like `kubectl apply`, it
checks if a resource already exists, and applies any changes.

That's it! That's the feature!

## How you too can hack stuff into Tilt with Bash

In this example, we took two very simple tools in a local dev environment: a
local shell command (`Cmd`) and a button (`UIButton`).

The core components are very flexible.

Then we used a reconciler pattern to stitch them together in new ways,
create a new button that cancels other commands. We can even make the button reactive,
disabling it when the command it acts upon exits.

And we did this all without modifying core Tilt. We didn't even have to compile our code!

In our travels, we meet lots of teams that want to be able to hack tasks ntto
their dev environment.  Maybe they need to reset a database, or create a fake
user account, or test an API.  And they need these tasks to have runtime checks,
to make them fast and diagnose common errors.

That's why we think the control loop pattern is a great pattern for setting up
dev environments, and can help teams develop faster and with more confidence.

Have an idea for a control loop that steers your servers? We're going to be
writing more about how to write tools this way, and are always [happy to pair
with our community](https://docs.tilt.dev/#community) on how to do it.
