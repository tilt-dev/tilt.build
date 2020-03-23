---
title: Python Debuggers in Tilt
layout: docs
---

Debuggers are an invaluable part of many development workflows. When you're running your app(s) in Kubernetes, using debuggers suddenly gets much harder, but Tilt's port forwarding functionality makes it easy again.

Currently, our recommended Python debugger for use with Tilt is [`remote-pdb`](https://pypi.org/project/remote-pdb/), but you can generalize this guide to any Python debugger that exposes a port for external connections.

## Debugging your project with Tilt and a remote debugger

We'll use [this example project](https://github.com/windmilleng/tilt-example-python/tree/master/debugger-example), which is configured to use `remote-pdb`. Clone it and follow along!

### Set-up
To prepare your project for remote debugging, follow these steps:
1. Decide what port you'll expose the debugger on. This example uses `5555`.
2. Add your debugger of choice in [requirements.txt](https://github.com/windmilleng/tilt-example-python/tree/master/debugger-example/requirements.txt).
3. Expose your chosen port as a `containerPort` in the [Kubernetes YAML](https://github.com/windmilleng/tilt-example-python/tree/master/debugger-example/kubernetes.yaml) of the Deployment or Pod that you want to debug (in addition to any ports you're already exposing for normal development; e.g. here we expose port 8000 just to see the app running):
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
4. In the [Tiltfile](https://github.com/windmilleng/tilt-example-python/tree/master/debugger-example/Tiltfile), tell Tilt to forward that port (again, in addition to any ports you're already forwarding for normal development):
    ```python
   k8s_resource('example-python', port_forwards=[
       8000,  # app
       5555,  # debugger
   ])
    ```

### You're ready to debug!
Congrats, now you can add breakpoints with your chosen debugger, and connect to it at your chosen port however is appropriate. Check out [this example repo](https://github.com/windmilleng/debugger-examples/tree/master/python/remote-pdb) to try it with `remote-pdb`:
1. Insert the breakpoint. In the example repo, there's already a breakpoint inserted in [app.py](https://github.com/windmilleng/tilt-example-python/tree/master/debugger-example/app.py):
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

#### Remember to wait for your debugger
Some debuggers start listening on their port as soon as the app starts, and you can connect immediately. With the approach described here, the debugger doesn't start until the first `set_trace` call, so don't try to connect until then, or you'll just see a bunch of errors.

When using `remote-pdb`, the log line that tells you that your debugger is active is:
> CRITICAL:root:RemotePdb session open at 127.0.0.1:5555, waiting for connection ...
> RemotePdb session open at 127.0.0.1:5555, waiting for connection ...

(See [this interactive snapshot](https://cloud.tilt.dev/snapshot/Aer7necLsNHx2TGFkfc=) for a closer look.)

## Future Work
As we find more Python debuggers that fit well into Tilt-based workflows, we'll create guides/example projects for them. Have a favorite remote-connection-friendly Python debugger that you'd like to see us cover? [Let us know](https://tilt.dev/contact)!
