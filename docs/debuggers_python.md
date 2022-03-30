---
title: Connecting Debuggers
description: "Debuggers are an invaluable part of many development workflows. This guide contains examples of how to make them work again in Kubernetes."
layout: docs
sidebar: guides
---

Debuggers are an invaluable part of many development workflows. When you're running your app(s) in Kubernetes, using debuggers suddenly gets much harder, but Tilt's port forwarding functionality makes it easy again.

In this guide, we'll walk you through an example of how to connect a Python
debugger to a container in a Tilt env. Debuggers in most languages use these patterns.

[This repository](https://github.com/tilt-dev/tilt-example-python/tree/master/debugger-examples) contains some examples of how to use various remote debuggers against Tilt. We'll examine the `remote-pdb` case in detail below (see [this directory](https://github.com/tilt-dev/tilt-example-python/tree/master/debugger-examples/remote-pdb)), but the bulk of these steps apply when setting up Tilt with _any_ remote debugger, and only the very end of this guide varies based on your choice of tool. 

## Debugging your project with Tilt and a remote debugger

### Set-up
To prepare your project for remote debugging, follow these steps:
1. Decide what port you'll expose the debugger on. This example uses `5555`.
2. Add your debugger of choice in [requirements.txt](https://github.com/tilt-dev/tilt-example-python/tree/master/debugger-examples/remote-pdb/requirements.txt).
3. Expose your chosen port as a `containerPort` in the [Kubernetes YAML](https://github.com/tilt-dev/tilt-example-python/tree/master/debugger-examples/remote-pdb/kubernetes.yaml) of the Deployment or Pod that you want to debug (in addition to any ports you're already exposing for normal development):
    ```yaml
    kind: Deployment
    ...
    spec:
        spec:
          containers:
            - name: example-python
              image: example-python-image
              ports:
                - containerPort: 8000  # the app itself
                - containerPort: 5555  # debugger
    ```
4. In the [Tiltfile](https://github.com/tilt-dev/tilt-example-python/tree/master/debugger-examples/remote-pdb/Tiltfile), tell Tilt to forward that port (again, in addition to any ports you're already forwarding for normal development):
    ```python
   k8s_resource('example-python', port_forwards=[
       8000,  # app
       5555,  # debugger
   ])
    ```

### You're ready to debug!
Congrats, now you can add breakpoints with your chosen debugger, and connect to it at your chosen port however is appropriate. For `remote-pdb`, the steps are as follows:
1. Insert the breakpoint. In the example repo, there's already a breakpoint inserted in [app.py](https://github.com/tilt-dev/tilt-example-python/tree/master/debugger-examples/remote-pdb/app.py):
    ```python
   from remote_pdb import RemotePdb
   RemotePdb('127.0.0.1', 5555).set_trace()
    ```
2. Trip the breakpoint you set. In the example repo, this means hitting `localhost:8000`. (You'll see the request hang---this is expected! It means that execution of your app paused at the breakpoint.)
3. Connect to your debugger. For `remote-pdb`, this means opening a TCP connection on 5555. We recommend using [Netcat](http://netcat.sourceforge.net/):
   ```
   nc 127.0.0.1 5555
   ```
   (The [remote-pdb guide](https://pypi.org/project/remote-pdb/) has some other connection options, if you prefer.)
4. Debug to your heart's content!

(If you'd prefer to access your debugger in a browser instead of in your terminal/via TCP connection, check out [our `web-pdb` example](https://github.com/tilt-dev/tilt-example-python/tree/master/debugger-examples/web-pdb/).)

#### Remember to wait for your debugger
Some debuggers start listening on their port as soon as the app starts, and you can connect immediately. With the approach described here, the debugger doesn't start until the first `set_trace` call, so don't try to connect until then, or you'll just see a bunch of errors.

When using `remote-pdb`, the log line that tells you that your debugger is active is:
> CRITICAL:root:RemotePdb session open at 127.0.0.1:5555, waiting for connection ...
> RemotePdb session open at 127.0.0.1:5555, waiting for connection ...

(See [this interactive snapshot](https://cloud.tilt.dev/snapshot/Aer7necLsNHx2TGFkfc=) for a closer look.)

## Connecting Your Own Debugger

Tilt itself does not have any code for connecting to a particular debugger. None
of the examples in this guide use "magic" primitives.

Instead, Tilt provides a standardized API for coordinating any debugger with your dev environment.

Do you use a debugger that's not listed here?

Use [`local_resource`](/local_resource.html) to spin it up. 

Once you've got it running, consider packaging it up as [a Tilt
extension](/extensions.md) for others to use.

## Sample Code

- [Python Remote PDB](https://github.com/tilt-dev/tilt-example-python/tree/master/debugger-examples/remote-pdb)
- [Python Web PDB](https://github.com/tilt-dev/tilt-example-python/tree/master/debugger-examples/web-pdb)
- [NodeJS](https://github.com/tilt-dev/tilt-example-nodejs/blob/master/101-debugger/Tiltfile)
