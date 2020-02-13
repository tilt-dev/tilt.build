---
title: Writing Tilt Extensions (Preview)
layout: docs
---

Introducing Tilt Extensions! Extensions are a simple way to bundle up Tiltfile functionality that should be shared with the world.

Lots of Tilt users have implemented useful Tiltfile functionality that'd be great for others to be able to use as well. We've seen functions that force resources in to different namespaces, inject sidecars or even run tests. We created extensions to make it easy for Tiltfile authors to share those ideas, and for new Tiltfile authors to stand on the shoulders of giants by building on top of them.

Let's take a look at a simple example that shows how to make an extension in Tilt. We'll follow it up with a more complicated example.

## Simple Example: API Server Logs
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

That's it. You've created your first Tilt extension! Simply brush up on the Extension Repo [README](https://github.com/windmilleng/tilt-extensions/blob/master/README.md) and [open a PR](https://github.com/windmilleng/tilt-extensions/compare) to make this extension available to all Tilt users.

## Slightly More Complicated Example: Jest Test Runner

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

## Conclusion
Whether it's a small thing like how to get logs out of Kubernetes or a big thing like how to efficiently run tests, we think that sharing these patterns through Tilt Extensions will unlock step-level increases in engineering productivity. Just how NPM packages enabled people to do more things faster with JavaScript, we think Tilt Extensions will enable people to make their own developer experience more productive, faster.
