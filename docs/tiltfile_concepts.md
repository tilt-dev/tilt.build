---
title: Tiltfile Concepts
layout: docs
---

This doc describes concepts in the Tiltfile, expanding on the [Tutorial](tutorial.html). Unlike the [API Reference](api.html), it groups functions by themes and explains why you'd choose to use a function.

## Execution Model
`Tiltfile`s are written in [Starlark](https://github.com/bazelbuild/starlark), a dialect of Python. Tilt executes the `Tiltfile` on startup.

Functions like `k8s_yaml` and `docker_build` register information. At the end of the execution, Tilt uses the resulting configuration. In addition to the final configuration, Tilt records file accesses; Tilt watches these files, and reexecutes when one changes (but not on every source file change).

Because your Tiltfile is a program, you can configure it with familiar constructs like loops, functions, arrays, etc. This makes Tilt more extensible than a configuration that requires hard-coding all possible options up-front.

Any relative paths in your Tiltfile are evaluated relative to the location of the Tiltfile.

## Deploy
The first function in a `Tiltfile` is generally a call to `k8s_yaml`. You can call `k8s_yaml` in a variety of ways, depending on how your project organizes or generates YAML. Let's look at some alternatives:

```python
# one static YAML file
k8s_yaml('app.yaml')

# multiple YAML files in one call
k8s_yaml(['foo.yaml', 'bar.yaml'])

# multiple YAML files in multiple calls
k8s_yaml('baz.yaml')
k8s_yaml('quux.yaml')

# call out to a built-in tool
k8s_yaml(kustomize('config_dir')) # built-in support for popular tools
k8s_yaml(helm('chart_dir'))
```

Tilt has built-in functions to generate Kubernetes YAML with `kustomize` or `helm`. (If you think we're overlooking a popular tool, let us know so we can add it.)

## Custom Commands
If your project uses a custom tool to generate Kubernetes YAML, you can still use Tilt. You don't have to wait for us to add support or fork Tilt and implement it yourself. Run a custom command with the `local` function:
```python
text = local('./foo.py') # runs command foo.py
k8s_yaml(text)
```

`local` runs a command, and returns its `stdout` as a ``Blob`` (see notes on the [Blob type](#blob-type), below). Note: Tilt doesn't know what files a command accesses, so you need to use the function `read_file` to record accesses. If you don't call `read_file`, Tilt won't reexecute the `Tiltfile` when those files change. For example, if `foo.py` depends on the files `config/base.yaml` and `data/versions.txt`:

```python
read_file('config/base.yaml')
read_file('data/versions.txt')
text = local('./foo.py')
k8s_yaml(text)
```

You can also use Python features like list comprehensions. For example, if you have a script that generates YAML for one microservice at a time, you could do:

```python
# define a function that returns the config for one microservice
def microservice_yaml(name):
  # record file access, using Python string substitution to generate filename
  read_file('config/%s.yaml' % name)
  # run the script with an argument
  return local('./config/generate.py %s' % name)

# define the service names
services = ['frontend', 'backend', 'users', 'graphql']

# loop over each service and register its config
[k8s_yaml(microservice_yaml(service)) for service in services]
```

Using `local` judiciously can let you use existing tools with Tilt, without having to rewrite or abandon them immediately.

## ``Blob`` type
Broadly speaking, there are two types of strings that might pass around in your Tiltfile:
raw configuration files/data (e.g. the text of your Dockerfile, a string of YAML), or strings
indicating how to _find_ config data (i.e. a file path, though in future this category may include other things).

For functions that can accept both types of strings -- e.g. ``k8s_yaml``, which can accept either path(s)
to YAML files or the YAML itself -- we make use of typing to indicate whether a given string is _data_ or
a _pointer to data_.

Specifically, we wrap data-strings as ``Blob``s to distinguish them from plain strings, which we assume are filepaths.

Commands executed on your local system (via ``local`` or ``read_file``) return their results as a ``Blob`` because
in the most common case, they contain _data_; e.g. ``read_file('config.yaml')`` or ``local('generate_yaml.sh')`` both
return YAML.

Consider the following:
```python
# pass filepaths as regular strings
k8s_yaml([
    'foo.yaml',  # Type: str
    'bar.yaml',  # Type: str
])

k8s_yaml([
    read_file('foo.yaml')  # Type: Blob
])

# If for some reason you have YAML as a string, wrap it as a
# Blob so we know to treat it as DATA and not as a filepath
yaml_str = """
apiVersion: v1
kind: Pod
  metadata:
    name: nginx
    labels:
      app: nginx"""
k8s_yaml([
    blob(yaml_str)  # Type: Blob
])
```

## Build
The `docker_build` function aims to support most usages of docker. Here's a cheat-sheet that maps docker command lines to a `docker_build` call:

```python
# docker build -t companyname/frontend ./frontend
docker_build("companyname/frontend", "frontend")

# docker build -t companyname/frontend -f frontend/Dockerfile.dev frontend
docker_build("companyname/frontend", "frontend", dockerfile="frontend/Dockerfile.dev")

# docker build -t companyname/frontend --build-arg target=local frontend
docker_build("companyname/frontend", "frontend", build_args={"target": "local"})
```

You can combine multiple optional arguments.

## Resources
Tilt's UI makes it easier to find errors by grouping related status and output. E.g., when you edit a file, you want to know what error it caused, whether it's an error at build-time, deploy-time, or run-time. Tilt calls these groupings "Resources". Each Resource has a line in the UI that can be expanded and investigated.

Tilt generates these groups after executing your `Tiltfile`. We're actively working on how to group in ways that make the most intuitive sense, so the specific algorithm is in-flux. We'll expand this paragraph when it's more settled.

You can configure a resource with a call to `k8s_resource`. Today there are two relevant configuration arguments: `image` and `port_forwards`.

`image` allows you to specify a custom image to group by. If not specified it will try to group images by the name of the resource itself.

```python
# group pods running images named "Frontend" in to a resource named "frontend"
k8s_resource('frontend')

# group pods running images named "custom_frontend" in to a resource named "frontend"
k8s_resource('frontend', image='custom_frontend')
```

Tilt also supports a few ways to specify `port_forwards`:

```python
# connect localhost:9000 to the default container port
k8s_resource('frontend', port_forwards=9000)

# connect localhost:9000 to container port 8000
k8s_resource('frontend', port_forwards='9000:8000')

# connect localhost:9000 to container port 8000
# and localhost:9001 to container port 8001
k8s_resource('frontend', port_forwards=['9000:8000', '9001:8001'])
```

## Summary
Tilt's configuration is a program that connects your existing build and deploy configuration. We've made our functions ergonomic for simple cases and general enough to support a wide range of cases. If you're not sure how to accomplish something, we'd love to either help you find the right way, or add support for a case we've overlooked.
