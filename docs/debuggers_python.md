---
title: Python Debuggers in Tilt
layout: docs
---

Debuggers are an invaluable part of many development workflows. When you're running your app(s) in Kubernetes, using debuggers suddenly gets much harder, but Tilt's port forwarding functionality makes it easy to use any debugger that exposes a port for external connect.

At the current moment, our recommended Python debugger for use with Tilt is [`remote-pdb`](https://pypi.org/project/remote-pdb/) (we will list other debugger options here as we validate and write guides for them).

## Debugging your project with Tilt and a remote debugger

I'll be referring to [this example repo](https://github.com/windmilleng/debugger-examples/tree/master/python/remote-pdb), which is configured to use `remote-pdb`. Clone it and follow along!

### Set-up
To prepare your project for remote debugging, follow these steps:
1. Decide what port you'll expose the debugger on. For this example, I'm using 5555.
2. Add your debugger of choice in [requirements.txt](https://github.com/windmilleng/debugger-examples/blob/master/python/remote-pdb/requirements.txt).
3. Expose your chosen port as a `containerPort` in the [Kubernetes YAML](https://github.com/windmilleng/debugger-examples/blob/master/python/remote-pdb/kubernetes.yaml) of the Deployment or Pod that you want to debug (in addition to any ports you're already exposing for normal development; e.g. here we expose port 8000 just to see the app running):
    ```yaml
    kind: Deployment
    ...
    spec:
        spec:
          containers:
            - name: example-python
              image: example-python-image
              ports:
                - containerPort: 5555
                - containerPort: 8000
    ```
4. Tell Tilt to port-forward that port in the [Tiltfile](https://github.com/windmilleng/debugger-examples/blob/master/python/remote-pdb/Tiltfile) (again, in addition to any ports you're already forwarding for normal development):
    ```python
   k8s_resource('example-python', port_forwards=[
       '8000:8000',  # app
       '5555:5555',  # debugger
   ])
    ```

### You're ready to debug!
Congrats, now you can add breakpoints with your chosen debugger, and connect to it at your chosen port however is appropriate. Check out [this example repo](https://github.com/windmilleng/debugger-examples/tree/master/python/remote-pdb) to try it with `remote-pdb`:
1. Insert the breakpoint:
    ```python
   from remote_pdb import RemotePdb
   RemotePdb('127.0.0.1', 5555).set_trace()
    ```
2. Connect to port 5555 via TCP
    * with Netcat: `nc -c 127.0.0.1 5555`
    * with Telnet: `telnet 127.0.0.1 5555`
    * with Socat: `socat readline tcp:127.0.0.1:5555`
