---
title: Contribute an Extension
layout: docs
---

This page explains how to contribute an open source extension. If you're interested in only using extensions, visit [Extensions](extensions.html).

## Create and test a function in your Tiltfile
Tiltfiles are written in a Python dialect called [Starlark](https://github.com/bazelbuild/starlark/blob/master/spec.mdl). And so for the purpose of writing a new extension, it is no different from writing your Tiltfile, namely following typical Python syntax.

Create a new function, following the `def func_name(args):` syntax and add it to your Tiltfile. (Refer to any [existing extension](https://github.com/tilt-dev/tilt-extensions) as an example.) Invoke the function later in your Tiltfile. Run Tilt as normal, and verify that the function works as expected.

You can load an existing extension and use it, in the new extension you are creating. Follow the same syntax as explained in [Extensions](extensions.html). 

## Package your function and submit a pull request
Clone the [tilt-extensions repo](https://github.com/tilt-dev/tilt-extensions), and create a new extension, following the directory structure of other existing extensions. Namely, there should be a root-level directory with the name of your extension, a Tiltfile, and a README.md inside that directory. Copy the function you previously tested into that Titfile. Also update [README.md](https://github.com/tilt-dev/tilt-extensions/blob/master/README.md), explaining your extension. I.e. you should have these changes:

```
extension_name/Tiltfile
extension_name/README.md
README.md
```

Create and submit a pull request to the repo, and @-mention `@victorwuky` for review.

Currently there's no way to directly test the end-to-end workflow of using an extension. The Tilt team will ensure that the extension is working correctly before publishing it.

## Next steps

If you run into any problems, [contact us](https://tilt.dev/contact). If you have an extension idea (but aren't interested in contributing), [request it](https://github.com/tilt-dev/tilt/issues).


## Example extension: API Server Logs
Depending on the kind of Kubernetes work you're doing it can be valuable to see the Kubernetes API Server logs. For example, if you were iterating on a Kubernetes controller that interacts heavily with the Kubernetes API. By default Tilt doesn't display those logs because they don't come from a resource that Tilt deployed. However, it's pretty easy to get tilt to display them using a `local_resource`:

```python
local_resource('API Server Logs', '', serve_cmd='kubectl logs -f -n kube-system kube-apiserver-docker-desktop')
```

This only works for Docker for Desktop on macOS, since it's hard coded to that pod name. But it would be easy to write a query to get the API server pod for any arbitrary Kubernetes cluster:

```python
api_server_pod_name = str(local('kubectl get pods --namespace kube-system -o=jsonpath="{.items..metadata.name}" -l component=kube-apiserver')).rstrip(\n)
```

Then you could compose them together in a function:

```python
def api_server_logs():
  api_server_pod_name = str(local('kubectl get pods --namespace kube-system -o=jsonpath="{.items..metadata.name}" -l component=kube-apiserver')).rstrip(\n)
  local_resource('API Server Logs', '', serve_cmd='kubectl logs -f -n %s' % api_server_pod_name )
```

## Example extension: Jest Test Runner

Tilt is great at building your code and running your services, and with extensions it's easy to make Tilt great at running your tests. Let's use the [Jest](https://jestjs.io/) JavaScript test runner as an example.

To run Jest you simply do `yarn run jest`. Unlike a lot of test runners Jest runs in the foreground, watches your filesystem for changes and runs the correspond tests. So to translate `yarn run jest` in to a `local_resource` we'll actually set it as the _serve_ cmd:

```python
local_resource("jest", "", serve_cmd="yarn run jest")
```

This works well except there's no indication in the Tilt UI when your tests fail. That's because Tilt only considers a `local_resource` as failing if the process exits, which Jest never does. Fortunately you can tell Jest to exit by passing the `--bail` flag. Let's just wrap it in a function that takes a path to run Jest from and we have ourselves a Jest extension:

```python
def jest(path):
  local_resource("jest", "", serve_cmd="cd %s && yarn run jest --bail" % path)
```

Now Tilt is running your tests, how cool is that?
