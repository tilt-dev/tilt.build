---
slug: "demystified"
date: 2020-11-13
author: l
layout: blog
title: "Tilt Demystified: Inside Tilt's Control Loop"
image: "/assets/images/demystified/image.jpg"
video: "https://www.youtube.com/embed/mN31_O-B4ss"
tags:
  - tilt
  - control loop
---

We want Tilt to feel like magic. All you need is a Tiltfile and some configs, and Tilt can spin up your entire app on Kubernetes, and respond instantly to changes.

Anyone from the most senior developer to a new hire to QA to an engineer who’s terrified of Kubernetes should be able to run tilt up and have it just work.

When someone first encounters Tilt, usually their mental model’s something like this:

![Magic](/assets/images/demystified/02.jpg)

That is, write the Tiltfile, magic happens, and it’s all live. 

For most people, this level of understanding is plenty. Tilt responds to your changes, and the right code is always running in your cluster.

 But sometimes you need to know a little more about what’s going on: 
 
 - Maybe for debugging. 
 - Maybe for creating custom functionality. 
 - Or maybe you’re just curious.
 
 In this article, we’re going to clarify this flow, and show you--at a high level--what actually happens to go from Tiltfile to services running in Kubernetes.

## What is a resource?

On the cluster part of the diagram above, that’s your application running in Kubernetes. As far as Tilt is concerned, these objects—and they can be pods, jobs, deployments, ingresses, anything—as well as any other bit of work Tilt might have to do… they’re organized into resources. 

![Magic](/assets/images/demystified/03.jpg)

That’s what those things on the Tilt sidebar really represent.

So a resource is any bundle of work managed by Tilt. 

- It can be a container image to build plus some Kubernetes YAML to deploy—maybe this is one of the microservices you’re working on. 
- It can be just Kubernetes YAML to deploy—like a database instance. 
- Or it can be a command to run on localhost—like a script that generates some artifact, which you then sync into a running container. 

Now how does Tilt know what your resources are, and how to execute them? That happens in the Tiltfile.

## The Tiltfile

A Tiltfile, as you might know, is a configuration file written in Starlark, a dialect of Python. It’s real code and you can use conditionals, loops, functions, and so on.

![Tiltfile](/assets/images/demystified/01.jpg)

Now, this is important: The Tiltfile itself does *not*  execute anything in your cluster. Instead, it stitches together all the information about your resources, and relays them to the Tilt engine.

![Resources](/assets/images/demystified/04.jpg)

For example, in the Tiltfile above we’re using the `k8s_yaml` function to tell Tilt about Kubernetes objects that need deploying, and the `docker_build` function to tell Tilt how to build images. 

Let's take the `k8s_yaml` call. It doesn’t apply YAML to your cluster directly--instead, it registers that YAML internally. 

At the end of Tiltfile execution, Tilt will package that YAML into a resource and send that resource to the Tilt engine, where it can then be applied.

In addition, Tilt has some heuristics to group related bits of work into the same resource. If you tell Tilt to build a “myservice” image, and give it YAML to deploy an image called “myservice”, Tilt puts two and two together and groups those instructions into a single resource.

Lastly, Tilt watches the Tiltfile, and any files that feed into it. If Tilt detects any changes that might affect the output of the Tiltfile, it evaluates the Tiltfile again.

![Tiltfile Watch](/assets/images/demystified/05.jpg)

## Applying resources

Now that we know what resources are, and how to define those resources in the Tiltfile, let’s talk about *how* Tilt executes those resources, and *when* it does so.

![Resources](/assets/images/demystified/07.jpg)

To execute a resource, the "how" depends on what the resource is. As we discussed earlier, a resource can be:

- an image and some YAML
- just the YAML
- a local command 

So: 

- If it’s a local resource, run the command locally. 
- If image build instructions are present, build the image. 
- If Kubernetes YAML is present, deploy it to the cluster. 
- (And when configured, Tilt can modify a running container in place for faster updates.) 

Now, a very important part of Tilt is that it updates your cluster in real time. It is always running the most current code, and the most current configuration. How does Tilt do that? 

![Resource Watch](/assets/images/demystified/06.jpg)

By watching for certain key events. Generally those are: 

- A change to the resource’s definition in the Tiltfile. 
- A user manually triggering the execution of that resource. 
- Or change to a file that the resource cares about.

You might be wondering, how does Tilt know what files a resource cares about? 

Explicitly, you can specify in the Tiltfile that a resource depends on certain files and folders. 

And implicitly, Tilt assumes that if you’re building an image and the context is the “myservice” directory, any file changes in that directory will affect that resource.

## Summary

To wrap this up, let’s have a quick recap of Tilt’s control flow: 

- First, execute the Tiltfile in its entirety, and create resource definitions. Some of these are configured manually, and some Tilt uses heuristics to assemble. 
- Whenever the Tiltfile changes, re-execute it and update the internal resource definitions.
-  Next, the engine  executes the resources, and if any resources contain Kubernetes objects, these end up deployed to your cluster. 
- Lastly, resources get updated whenever there’s a triggering event. These can be a definition changing, a relevant file changing, or the user manually triggering the resource.

Hopefully this article was helpful in giving you a better understanding about how Tilt’s control flow works internally. 

This knowledge should make it easier for you to debug your applications, and to create custom functionality. 

Thanks for reading, and see you next time!
