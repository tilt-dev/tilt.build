---
title: "Tutorial: The First 15 Minutes"
description: "This tutorial walks you through setting up Tilt for your project."
layout: docs
---

This tutorial walks you through setting up Tilt for your project. 

It should take 15 minutes, and assumes you've already [installed Tilt](install.html). Before you begin, you may want to join the `#tilt` channel in [Kubernetes Slack](http://slack.k8s.io) for technical and moral support.

Start by `cd`'ing into a project you can already build and deploy to Kubernetes.

## Example Tiltfile
At the end of this guide, your Tiltfile will look something like this:
```python
# Deploy: tell Tilt what YAML to deploy
k8s_yaml('app.yaml')

# Build: tell Tilt what images to build from which directories
docker_build('companyname/frontend', 'frontend')
docker_build('companyname/backend', 'backend')
# ...

# Watch: tell Tilt how to connect locally (optional)
k8s_resource('frontend', port_forwards=8080)
```

## Hello World
In your terminal, run `tilt up`. Hit `space` and a browser tab will open showing Tilt. Instead of writing your Tilt configuration all at once, we'll use Tilt interactively. Each time you save your configuration, Tilt will reexecute it.

Right now, Tilt should be complaining that there's no file named `Tiltfile`. 

<figure>
  <img src="/assets/img/no-tiltfile.png" class="no-shadow" alt="No Tiltfile">
</figure>

Create a new file named `Tiltfile` (note the capitalization) in your project directory with a single line:

```python
print('Hello Tiltfile')
```

Now save the file. Congrats, you just ran your first Tiltfile since Tilt has automatically reexecuted with it. Tilt's configurations are programs in [Starlark](https://github.com/bazelbuild/starlark#tour>), a dialect of Python. Go back to your browser to see "Hello Tiltfile" in Tilt. Tilt is also warning you there are no declared resources. Let's add some.

## Step 1: Deploy
The [Tiltfile API](api.html) function [`k8s_yaml`](api.html#api.k8s_yaml) registers Kubernetes objects you want to deploy:
```python
k8s_yaml('app.yaml')
```

Tilt supports many deployment configuration practices (for more details, check out the [Deploy](tiltfile_concepts.html#deploy) section of "Tiltfile Concepts"):
```python
# multiple YAML files; can be either a list or multiple calls
k8s_yaml(['foo.yaml', 'bar.yaml'])

# run a command to generate YAML
k8s_yaml(local('gen_k8s_yaml.py')) # a custom script
k8s_yaml(kustomize('config_dir')) # built-in support for popular tools
k8s_yaml(helm('chart_dir'))
```

Use the pattern that matches your project (if you're not sure, feel free to ask in [Slack](index.html#community)). You can see when it works because Tilt will display the registered objects.

## Step 2: Build
The function [`docker_build`](api.html#api.docker_build) tells Tilt how to build a container image. Tilt automatically builds the image, injects the ID into Kubernetes objects and deploys. (The [Build](tiltfile_concepts.html#build) section of "Tiltfile Concepts" describes optional arguments.)

```python
# docker build -t companyname/frontend ./frontend
docker_build('companyname/frontend', 'frontend')
```

 Try editing a source file; you should see Tilt automatically build and deploy as soon as you save. Add additional images; you should have one `docker_build` call for each container image you're developing.

## Step 3: Watch (Optional)
Tilt can give you consistent port forwards to running pods (whether they're running locally or in the cloud). Call the function [`k8s_resource`](api.html#api.k8s_resource) with the name of the resource you want to access (taken from the UI):
```python
k8s_resource('frontend', port_forwards='9000')
```

(Note that the first parameter of `k8s_resource` must match the name of a pod-having k8s object that was passed to `k8s_yaml`. If you'd like to name it something else you can use the [`new_name` parameter](api.html#api.k8s_resource) to change its name.)

You can also use `k8s_resource` to forward multiple ports. Cf. the [Resources](tiltfile_concepts.html#resources) section of `Tiltfile Concepts`.

## Congrats

Tilt is now setup for your project. Explore Tilt further. Introduce a build error and then a runtime crash; see Tilt respond and surface the relevant problem.

## Next Steps

If you had any trouble using this guide,
now's a great time to [file bugs or feature requests](https://github.com/tilt-dev/tilt/issues).

If you'd like to see examples in your programming language, we have example projects for:

<ul>
  {% for page in site.data.examples %}
    <li><a href="/{{page.href | escape}}">{{page.title | escape}}</a></li>
  {% endfor %}
</ul>

