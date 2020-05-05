---
title: Setting a Personal Registry with a shared Tiltfile
layout: docs
---

You should be able to start an app on Kubernetes from just the source code. One stumbling block is when YAML and scripts hard-code the image repository (the `gcr.io/windmill` in `gcr.io/windmill/user-service`). Tilt's `default_registry` function lets you change the image repository so you don't have to ask permission to get started. This guide walks you through two cases:
* for users, how to experiment with an existing Tilt project by adding one line to the Tiltfile
* for maintainers, how to configure your project so users don't need to modify the Tiltfile at all

## Experiment with an existing Tilt project
You've cloned a repo, run `tilt up`, and see push errors saying you lack permission. Pick a registry that you can push to, like `gcr.io/my-personal-project`. Add the following line to the `Tiltfile`:

```python
default_registry('gcr.io/my-personal-project')
```

Tilt will rewrite an image like `user-service` to `gcr.io/my-personal-project/user-service`. You can learn more details in the [api reference](api.html#api.default_registry).

## Configure a Project to support Personal Registries
The above solution isn't a good long-term solution: users have to make sure to not commit their personal registry. It's especially frustrating if the user is trying to change other lines in the `Tiltfile`. A better solution is to read the option from a personal settings file that is `.gitignore`'d.

We're going to modify the `Tiltfile` to look for a file called `tilt_option.json` next to the Tiltfile. You can add more settings here (do different team members want different services to behave differently? Put it in `tilt_option.json`). For now, we'll expect the file to either be nonexistent, or JSON like

```json
{
  "default_registry": "gcr.io/my-personal-project"
}
```

Add this code to the `Tiltfile`:

```python
settings = read_json('tilt_option.json', default={})
default_registry(settings.get('default_registry', 'gcr.io/shared-project-registry'))
```

Add a line to your `.gitignore`:
```
# personal tilt settings
tilt_option.json
```

Team members don't need to set anything, but new users can change it without modifying the Tiltfile.

### Different URLs from Inside Your Cluster

Some clusters/registries require that your Kubernetes YAML reference images by a different name: e.g. you might push your image to `localhost:5000/my-image` but reference it from within your YAML as `registry:5000/my-image`. Tilt supports this use case; use the `host_from_cluster` parameter of `default_registry` to configure the registry host as referenced from your K8s YAML. E.g. for the example above, you would call:
```python
default_registry(
    'localhost:5000',
    host_from_cluster='registry:5000'
)
```

## Config in Files, not Flags
Other tools might make this a command-line flag, or an environment variable. Tilt encourages you to put it in a file. Why the difference? Tilt wants to be a responsive tool. You can't change a command-line flag without restarting the tool, and we want you to be able to use Tilt without restarting.

We also want to let you write `Tiltfile`'s that support your project. If you have lots of services, you may not want to run all of them all of the time. With a `tilt_option.json` that you can change, you can switch services on or off.

This functionality is in the early stages, and we'd like to make it better supported. If you have thoughts/ideas/needs, please [talk to us](index.html#community).
