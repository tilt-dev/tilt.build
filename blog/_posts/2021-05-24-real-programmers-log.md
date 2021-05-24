---
slug: "real-programmers-log"
date: 2021-05-24
author: nick
layout: blog
title: "Real Programmers log('HERE')"
subtitle: "Tools for viewing logs in multi-service dev, and the PodLogStream API"
image: "/assets/images/real-programmers-log/logs.jpg"
image_caption: "Heranschaffen von Holz für Unterstände auf einer Feldbahn im Westen. Via <a href='https://digitalcollections.nypl.org/items/510d47de-0163-a3d9-e040-e00a18064a99'>The New York Public Library</a>."
tags:
  - api
  - log
---

A long time ago, I was cleaning out my work desk. I found a hand-written note. I
laughed out loud at what it said. I don't remember the exact words. But I
remember the sentiment:

> Dear [Andy Bons](https://twitter.com/andybons),
>
> Thank you for showing me how to use console.log()
>
> [Brian Kernighan](https://en.wikipedia.org/wiki/Brian_Kernighan)[^1]

This should be proof that there is nothing more fundamental to programming than
adding a log('HERE') statement. It's the most basic scientific method:

1. Hypothesis - I'm skeptical that this code path is running when I expect.

2. Experiment - I add log('HERE') and run it.

3. Conclusion - My skepticism has been proven/disproven!

That's why we've spent a lot of time thinking about the log experience in Tilt,
and the log experience in multi-service development more broadly.[^2]

In this post, we're going to talk about the approaches that we recommend to people,
what Tilt users do, and some of the things we're building.

## Logging Level 0 - Open five terminal windows

Don't let anyone judge you for opening up five terminal windows, 
starting a different service for each one, and watching the logs!

If you are a nerd you can lean hard into creating more and more terminal windows:

- [Tmux](https://github.com/tmux/tmux#welcome-to-tmux) controls multiple terminals with one screen.
- [i3](https://i3wm.org/) tiles the terminals on your desktop.

## Logging Level 1 - Multiplexing logs

If you use Kubernetes for local dev, `kubectl` has a more powerful log viewer than you
would expect.

Most people know how to fetch logs from one pod. Here's how you get the logs of Kind's apiserver:

``` 
kubectl logs -n kube-system kube-apiserver-kind-control-plane
```

If you want to stream the logs as they come in, add `-f` for Follow:

``` 
kubectl logs -n kube-system kube-apiserver-kind-control-plane -f
```

And if I want to get all the logs from a set of pods, I can use labels to select labels from multiple pods:

```
kubectl logs -n kube-system -l tier=kube-control-plane
```

For even more advanced tooling, there's [stern](https://github.com/wercker/stern), which will give each pod
a different color.

```
stern -n kube-system -l tier=control-plane
```

## Accessing the Logs Tilt Collects 

When you bring multiple services up in Tilt for dev, Tilt provides a unified
view of logs from local build commands, local servers, and remote servers. `tilt
up` presents you with both a browser log viewer or a text stream:

```
$ tilt up
Tilt started on http://localhost:10350/
v0.20.3-dev, built 2021-05-20

(space) to open the browser
(s) to stream logs (--stream=true)
(t) to open legacy terminal mode (--legacy=true)
(ctrl-c) to exit
```

If you need to feed those logs to other tools, the `tilt logs` command has
similar ergonomics to `kubectl logs` for interacting with the logs of a running
Tilt environment.

```
# View all logs
tilt logs

# Follow all logs
tilt logs -f

# View logs of one service
tilt logs blog-site
```

There are currently two main types of API objects in Tilt that produce logs:

- The [Cmd](https://api.tilt.dev/core/cmd-v1alpha1.html) API represents all
  commands on the local machine.
- The
  [PodLogStream](https://api.tilt.dev/kubernetes/pod-log-stream-v1alpha1.html)
  API represents all the pods that Tilt is currently streaming logs from.
  
So if we're not seeing logs we expect, we can use `tilt get` to view these objects
and see where Tilt is pulling logs from.

For example, if I'm running this [Tilt example project](https://github.com/tilt-dev/tilt-example-html):

```
$ tilt get podlogstream
NAME                                    CREATED AT
default-example-html-76d57856d7-dtvd2   2021-05-21T18:39:23Z
```

I can see that we're pulling logs from exactly one pod. I can use `tilt describe` to get more detail.

```
$ tilt describe podlogstream
Name:         default-example-html-76d57856d7-dtvd2
Namespace:    
Labels:       <none>
Annotations:  tilt.dev/log-span-id: pod:example-html:example-html-76d57856d7-dtvd2
              tilt.dev/resource: example-html
API Version:  tilt.dev/v1alpha1
Kind:         PodLogStream
Metadata:
  Creation Timestamp:  2021-05-21T18:39:23Z
  Resource Version:    3
  UID:                 8fc0327d-6f8f-4953-8614-054e463a7ea3
Spec:
  Ignore Containers:
    istio-init
    istio-proxy
  Namespace:   default
  Pod:         example-html-76d57856d7-dtvd2
  Since Time:  2021-05-21T18:39:22Z
Status:
  Container Statuses:
    Active:  true
    Name:    example-html
```

This tells me that Tilt is streaming logs from one container in that pod, 
the `example-html` container.

## Changing what Logs Tilt Collects

A complaint we hear about multi-service development is what happens when you
have the wrong logs in your dev enironment. 

- One annoying container is too chatty and hard to filter out.

- You're calling a remote API server and want to see its logs
  interspersed with your local logs to help visualize the API calls.

Normally, you'd need to tear everything down, configure everything with the
right logs, and bring it back up.

The big advantage of a declarative API for streaming logs is that we can
dynamically change the logs that are currently streaming.

- `tilt delete` can [delete](https://docs.tilt.dev/cli/tilt_delete.html) a PodLogStream so that the Tilt environment stops
streaming the logs.

- `tilt apply` can create a new PodLogStream or modify an existing one, so that
  you can add new containers, or ignore annoying ones. Usually you
  write the PodLogStream config in YAML in a file, then feed it to [apply](https://docs.tilt.dev/cli/tilt_apply.html).
  
Here's an example of how to add the Kubernetes apiserver logs to my current Tilt view:

```
$ tilt apply -f - << EOF
> apiVersion: tilt.dev/v1alpha1
> kind: PodLogStream
> metadata:
>   name: system
> spec:
>   namespace: kube-system
>   pod: kube-apiserver-kind-control-plane
> EOF
podlogstream.tilt.dev/system created
```

- `tilt edit` will open up the PodLogStream object in your favorite editor [^3],
   let you [edit](https://docs.tilt.dev/cli/tilt_edit.html) it, then try to
   apply it to the current Tilt environment. Let's edit the log stream I just created.
   
```
$ EDITOR=emacs tilt edit podlogstreams system
```

![PodLogStream in an editor](/assets/images/real-programmers-log/editor.jpg)
   
We're still building out more logging APIs like this for dev environments. Our
end goal is to have both a [full-fledged
API](https://api.tilt.dev/kubernetes/pod-log-stream-v1alpha1.html) that you can
interact with for experimentation, plus a set of pre-packaged
[extensions](https://docs.tilt.dev/extensions.html) for common operations.

But Pods are a small building block of the Kubernetes ecosystem. How does Tilt
capture logs for more complex API objects, like Deployments and Jobs, that might
create multiple Pods? We're going to cover that in a future post!

## Wrapping Up

I hope this post gave you a sense of how we're thinking about logs in
multi-service dev, other tools you can reach for to help you explore them, and
some of the APIs we're working on in Tilt to make them easier to grok.

[^1]: I don't have any proof that Brian wrote this note. It's a
      great joke if he did and a great joke if he didn't.

[^2]: I'm approaching logs with the axiom that logs for development 
      (where you're talking to yourself) 
      are a different style of communication than logs for production 
      (where you're talking to other people).
      There are people on the internet who disagree. 
      Maybe they also keep personal journals full of
      grammatically correct sentences. That's a whole post in itself!
      
[^3]: The right answer is Emacs.

