---
title: Extensions Preview
layout: docs
---

Introducing Tilt Extensions! Extensions are a simple way to bundle up Tiltfile functionality that should be shared with the world.

We think that there are lots of higher level patterns that people are implementing with Tilt that could benefit from sharing, socialization and standardization. For example many users have implemented their own ways to force all kubernetes resources in to a namespace, inject sidecars or run tests. Extensions provide a way for users to package up these ideas and share them with the community.

Let's take a look at a simple example that shows why extensions are a powerful addition to Tilt. We'll follow it up with a more complicated example.

## Simple Example: API Server Logs
Depending on the kind of Kubernetes work you're doing it can be valuable to see the Kubernetes API Server logs. For example, if you were iterating on a Kubernetes controller that interacts heavily with the Kubernetes API. By default Tilt doesn't display those logs because they don't come from a resource that Tilt deployed. However, it's pretty easy to get tilt to display them using a `local_resource`:

```python
local_resource('API Server Logs', '', serve_cmd='kubectl logs -f -n kube-system kube-apiserver-docker-desktop')
```

This only works for Docker for Desktop on macOS, since it's hard coded to that pod name. But it would be easy to write a query to get the API server pod for any arbitrary Kubernetes cluster:

```python
#TODO(dmiller): is this right?
api_server_pod_name = str(local('kubectl get pods --namespace kube-system -o=jsonpath="{.items..metadata.name}" -l component=kube-apiserver')).rstrip(\n)
```

Then you could compose them together in a function:

```python
def api_server_logs():
  api_server_pod_name = str(local('kubectl get pods --namespace kube-system -o=jsonpath="{.items..metadata.name}" -l component=kube-apiserver')).rstrip(\n)
  local_resource('API Server Logs', '', serve_cmd='kubectl logs -f -n %s' % api_server_pod_name )
```

That's it. You've created your first Tilt extension! Simply [open a PR](https://github.com/windmilleng/tilt-extensions/compare) against the official [Tilt Extensions Repo](https://github.com/windmilleng/tilt-extensions) to make this extension available to all Tilt users. All a user needs to do now is add a simple call to `load` to their Tiltfile that references the extension:

```python
load('ext://api_server_logs', 'api_server_logs')
```

## More Complicated Example: Jest Test Runner

TODO(dmiller): do this

## Conclusion
Whether it's a small thing like how to get logs out of Kubernetes or a big thing like how to efficiently run tests, we think that sharing these patterns through Tilt Extensions will unlock step-level increases in engineering productivity. Just how NPM packages enabled people to do more things faster with JavaScript, we think Tilt Extensions will enable people to make their own developer experience more productive, faster.
