---
title: Tiltfile API Reference
description: "A complete reference of functions available in your Tiltfile."
layout: docs
sidebar: reference
---

Tiltfiles are written in _Starlark_, a dialect of Python. For more information on Starlark's built-ins, [see the **Starlark Spec**](https://github.com/bazelbuild/starlark/blob/master/spec.md). The rest of this page details Tiltfile-specific functionality.

## Extensions

Can't find what you're looking for in this reference?

Tilt users can contribute [extensions](extensions.html) to share with other users. Browse them for
examples of what you can do with a Tiltfile. Load them into your own Tiltfile. Includes:

- [`api_server_logs`](https://github.com/tilt-dev/tilt-extensions/tree/master/api_server_logs): Print API server logs. Example from [Contribute an Extension](https://docs.tilt.dev/contribute_extension.html).
- [`cert_manager`](https://github.com/tilt-dev/tilt-extensions/tree/master/cert_manager): Deploys cert-manager.
- [`configmap`](https://github.com/tilt-dev/tilt-extensions/tree/master/configmap): Create configmaps from files and auto-deploy them.
- [`conftest`](https://github.com/tilt-dev/tilt-extensions/tree/master/conftest): Use [Conftest](https://www.conftest.dev/) to test your configuration files.
- [`coreos_prometheus`](https://github.com/tilt-dev/tilt-extensions/tree/master/coreos_prometheus): Deploys Prometheus to a monitoring namespace, managed by the CoreOS Prometheus Operator and CRDs
- [`current_namespace`](https://github.com/tilt-dev/tilt-extensions/tree/master/current_namespace): Reads the default namespace from your kubectl config.
- [`docker_build_sub`](https://github.com/tilt-dev/tilt-extensions/tree/master/docker_build_sub): Specify extra Dockerfile directives in your Tiltfile beyond [`docker_build`](https://docs.tilt.dev/api.html#api.docker_build).
- [`file_sync_only`](https://github.com/tilt-dev/tilt-extensions/tree/master/file_sync_only): No-build, no-push, file sync-only development. Useful when you want to live-reload a single config file into an existing public image, like nginx.
- [`git_resource`](https://github.com/tilt-dev/tilt-extensions/tree/master/git_resource): Deploy a dockerfile from a remote repository -- or specify the path to a local checkout for local development.
- [`hello_world`](https://github.com/tilt-dev/tilt-extensions/tree/master/hello_world): Print "Hello world!". Used in [Extensions](https://docs.tilt.dev/extensions.html).
- [`helm_remote`](https://github.com/tilt-dev/tilt-extensions/tree/master/helm_remote): Install a remote Helm chart (in a way that gets properly uninstalled when running `tilt down`)
- [`jest_test_runner`](https://github.com/tilt-dev/tilt-extensions/tree/master/jest_test_runner): Jest JavaScript test runner. Example from [Contribute an Extension](https://docs.tilt.dev/contribute_extension.html).
- [`ko`](https://github.com/tilt-dev/tilt-extensions/tree/master/ko): Use [Ko](https://github.com/google/ko) to build Go-based container images
- [`kubebuilder`](https://github.com/tilt-dev/tilt-extensions/tree/master/kubebuilder): Enable live-update for developing [Kubebuilder](https://github.com/kubernetes-sigs/kubebuilder) projects.
- [`kubectl_build`](https://github.com/tilt-dev/tilt-extensions/tree/master/kubectl_build): Get faster build cycles and smaller disk usage by building docker images directly in the k8s cluster with [BuildKit CLI for kubectl](https://github.com/vmware-tanzu/buildkit-cli-for-kubectl).
- [`kubefwd`](https://github.com/tilt-dev/tilt-extensions/tree/master/kubefwd):  Use [Kubefwd](https://kubefwd.com/) to bulk-forward Kubernetes services.
- [`local_output`](https://github.com/tilt-dev/tilt-extensions/tree/master/local_output): Run a `local` command and get the output as string
- [`min_k8s_version`](https://github.com/tilt-dev/tilt-extensions/tree/master/min_k8s_version): Require a minimum Kubernetes version to run this Tiltfile.
- [`min_tilt_version`](https://github.com/tilt-dev/tilt-extensions/tree/master/min_tilt_version): Require a minimum Tilt version to run this Tiltfile.
- [`namespace`](https://github.com/tilt-dev/tilt-extensions/tree/master/namespace): Functions for interacting with namespaces.
- [`pack`](https://github.com/tilt-dev/tilt-extensions/tree/master/pack): Build container images using [pack](https://buildpacks.io/docs/install-pack/) and [buildpacks](https://buildpacks.io/).
- [`print_tiltfile_dir`](https://github.com/tilt-dev/tilt-extensions/tree/master/print_tiltfile_dir): Print all files in the Tiltfile directory. If recursive is set to True, also prints files in all recursive subdirectories.
- [`procfile`](https://github.com/tilt-dev/tilt-extensions/tree/master/procfile): Create Tilt resources from a foreman Procfile.
- [`restart_process`](https://github.com/tilt-dev/tilt-extensions/tree/master/restart_process): Wrap a `docker_build` to restart the given entrypoint after a Live Update (replaces `restart_container()`)
- [`secret`](https://github.com/tilt-dev/tilt-extensions/tree/master/secret): Functions for creating secrets.
- [`snyk`](https://github.com/tilt-dev/tilt-extensions/tree/master/snyk): Use [Snyk](https://snyk.io) to test your containers, configuration files, and open source dependencies.
- [`syncback`](https://github.com/tilt-dev/tilt-extensions/tree/master/syncback): Sync files/directories from your container back to your local FS.
- [`wait_for_it`](https://github.com/tilt-dev/tilt-extensions/tree/master/wait_for_it): Wait until command output is equal to given output.

## Data

<ul>
{% for name in site.data.api.data.data %}

{% assign anchor = "api." | append: name %}
{% if name contains "." %}
  {% assign anchor = "modules." | append: name %}
{% endif %}

<li><a href="#{{anchor}}">{{ name }}</a></li>
{% endfor %}
</ul>

---

{% include api/data.html %}

---

## Functions

<ul>
{% for name in site.data.api.functions.functions %}

{% assign anchor = "api." | append: name %}
{% if name contains "." %}
  {% assign anchor = "modules." | append: name %}
{% endif %}
  
<li><a href="#{{anchor}}">{{ name }}</a></li>
{% endfor %}
</ul>

---

{% include api/functions.html %}

---

## Types

<ul>
{% for name in site.data.api.classes.classes %}

{% assign anchor = "api." | append: name %}
{% if name contains "." %}
  {% assign anchor = "modules." | append: name %}
{% endif %}
  
<li><a href="#{{anchor}}">{{ name }}</a></li>
{% endfor %}
</ul>

---

{% include api/classes.html %}
