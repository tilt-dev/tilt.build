---
title: Many Tiltfiles and Many Repos
layout: docs
sidebar: guides
---

Most of our example projects use a single Tiltfile. All the source files,
Dockerfiles, and Kubernetes configs are in a single folder.

But your project may be organized differently!

## How to Organize Your Project for Tilt

Tilt does not require a particular project structure. We try to provide 
APIs to help you pull the services you need into your dev environment, no matter
where they're defined.

Do NOT restructure your project for Tilt. Instead, restructure your Tiltfiles
to match your project structure!

We've seen many patterns, including:

- One main Tiltfile that subincludes a subdirectory Tiltfile for each service.

- Individual service Tiltfiles that include a library of common functions.

- Conditional loading of sets of services based on what you have checked out.

- Loading some services for editing and some services for running read-only.

- Loading prebuilt services from other repos.

- Checking out git repos or git submodules from the Tiltfile.

In this doc, we'll take a tour of the APIs that make these patterns possible.

## Loading Library Functions

Suppose you have two services that share dev conventions. Maybe you run them
together sometimes! Or maybe you don't. But you want to factor out common logic
for setting up their dev environment.

This is where [`load()`](api.html#api.load) can help. You can use it to load
shared constants or functions from a relative path:

```python
load('../common/Tiltfile', 'VERSION', 'common_config_yaml')

print('Loading version: ', VERSION)
k8s_yaml(common_config_yaml())
```

## Loading sub-Tiltfiles

Another pattern is where two services have independent Tiltfiles. 
But sometimes you want to load them together!

The [`include()`](api.html#api.include) function loads files that don't export
any helper functions.

```python
include('./frontend/Tiltfile')
include('./backend/Tiltfile')
```

## Loading Services Conditionally

We have an example project with an auth service. Sometimes we want to run it
with fake user data.  Sometimes we want to run it with real Github OAuth
login. Sometimes we want to run it with HTTPS instead of HTTP.

The [`load_dynamic()`](api.html#api.load_dynamic) function doesn't have the nice
syntax for loading constants, but does give you the flexibility to conditionally
load services.

Here's [an
example](https://github.com/tilt-dev/ephemerator/blob/3f4c3c7d045f1f012ad70afe3907c83b5645d565/ephconfig/Tiltfile)
that uses `os.path.exists` to see if you have OAuth client secrets or localhost
HTTPS certificates. If you do, it uses the real Github OAuth login
server. Otherwise, it uses fake user data.

```python
USE_OAUTH2 = os.path.exists('../.secrets/values-dev.yaml')
USE_TLS = False
if USE_OAUTH2:
  symbols = load_dynamic('../oauth2-proxy/Tiltfile')
  USE_TLS = symbols['USE_TLS']
```

## Configuring to-run vs to-edit Services

As you have more services, you may need to run subsets of them.

One way to handle this is to have a Tiltfile for each common configuration.

Other teams load all the services in a single Tiltfile, then add controls to enable/disable
sets of them.

Tilt has some built-in support for this!

* `tilt enable a b`: enable service 'a' and 'b'
* `tilt enable --only a b`: enable 'a' and 'b', and disables all others
* `tilt enable --all`: enable all services
* `tilt disable a b`: disable 'a' and 'b'
* `tilt disable --all`: disable all services

For more complicated configurations, you can define your own flags to `tilt up`
to specify sets of services to run or to edit. For more examples, see the
[per-user config guide](tiltfile_config.html).

## Managing other git Repositories

The simplest way to handle multi-repository projects is to ask the user to check
out other repos as a sibling directory.

```python
if os.path.exists('../backend'):
  fail('Please "git clone" the backend repo in ../backend!')
  
include('../backend/Tiltfile')
```

You can also supply the repository as an environment variable.

```python
backend_dir = os.environ.get('BACKEND_REPO_DIR', '../backend')
if os.path.exists(backend_dir):
  fail('Please "git clone" the backend repo in %s!' % backend_dir)
  
include(os.path.join(backend_dir, 'Tiltfile'))
```

Many sophisticated projects use this approach, including [the ClusterAPI
project](https://cluster-api.sigs.k8s.io/developer/tilt.html) for loading
servers for each host they deploy to!

Other teams in the Tilt community handle multi-repo projects directly from their
Tiltfile. The `git_resource` extension has functions for checking out arbitrary
repos and deploying the resources they contain.

```python
load('ext://git_resource', 'git_checkout')
git_checkout('git@github.com:tilt-dev/tilt-example-html.git#master', '/path/to/local/checkout')
```

Go to the [`git_resource`
README](https://github.com/tilt-dev/tilt-extensions/tree/master/git_resource)
for more details.

## Managing Extension Repositories

Finally, Tilt has a set of community-contributed extensions in [the
`tilt-extensions` repo](https://github.com/tilt-dev/tilt-extensions).

The community extensions contain both common functions to define your dev
environment, and common servers you may want to use.

Many teams manage their own extension repos for extensions that are specific to
their orgs! You can read more about how to use them in the [Extensions
Guide](./extensions.html).
