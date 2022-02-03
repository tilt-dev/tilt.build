---
title: Tiltfile API Reference
description: "A complete reference of functions available in your Tiltfile."
layout: docs
sidebar: reference
---

Tiltfiles are written in _Starlark_, a dialect of Python. For more information on Starlark's built-ins, [see the **Starlark Spec**](https://github.com/bazelbuild/starlark/blob/master/spec.md). The rest of this page details Tiltfile-specific functionality.

> 👀 **Looking for Examples?**
> Check out our new [Tiltfile Snippets](/snippets.html)!

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

---

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

## Extensions

Can't find what you're looking for in this reference?

Tilt users can contribute [extensions](extensions.html) to share with other users. Browse them for
examples of what you can do with a Tiltfile. Load them into your own Tiltfile. Includes:

- [`api_server_logs`](https://github.com/tilt-dev/tilt-extensions/tree/master/api_server_logs): Print API server logs. Example from [Contribute an Extension](https://docs.tilt.dev/contribute_extension.html).
- [`cancel`](https://github.com/tilt-dev/tilt-extensions/tree/master/cancel): Adds a cancel button to the UI.
- [`cert_manager`](https://github.com/tilt-dev/tilt-extensions/tree/master/cert_manager): Deploys cert-manager.
- [`color`](https://github.com/tilt-dev/tilt-extensions/tree/master/color): Allows colorful log prints.
- [`configmap`](https://github.com/tilt-dev/tilt-extensions/tree/master/configmap): Create configmaps from files and auto-deploy them.
- [`conftest`](https://github.com/tilt-dev/tilt-extensions/tree/master/conftest): Use [Conftest](https://www.conftest.dev/) to test your configuration files.
- [`coreos_prometheus`](https://github.com/tilt-dev/tilt-extensions/tree/master/coreos_prometheus): Deploys Prometheus to a monitoring namespace, managed by the CoreOS Prometheus Operator and CRDs
- [`current_namespace`](https://github.com/tilt-dev/tilt-extensions/tree/master/current_namespace): Reads the default namespace from your kubectl config.
- [`custom_build_with_restart`](https://github.com/tilt-dev/tilt-extensions/tree/master/restart_process): Wrap a `custom_build` to restart the given entrypoint after a Live Update
- [`deployment`](https://github.com/tilt-dev/tilt-extensions/tree/master/deployment): Create K8s deployments, jobs, and services without manifest YAML files.
- [`docker_build_sub`](https://github.com/tilt-dev/tilt-extensions/tree/master/docker_build_sub): Specify extra Dockerfile directives in your Tiltfile beyond [`docker_build`](https://docs.tilt.dev/api.html#api.docker_build).
- [`docker_build_with_restart`](https://github.com/tilt-dev/tilt-extensions/tree/master/restart_process): Wrap a `docker_build` to restart the given entrypoint after a Live Update
- [`dotenv`](https://github.com/tilt-dev/tilt-extensions/tree/master/dotenv): Load environment variables from `.env` or another file.
- [`file_sync_only`](https://github.com/tilt-dev/tilt-extensions/tree/master/file_sync_only): No-build, no-push, file sync-only development. Useful when you want to live-reload a single config file into an existing public image, like nginx.
- [`git_resource`](https://github.com/tilt-dev/tilt-extensions/tree/master/git_resource): Deploy a dockerfile from a remote repository -- or specify the path to a local checkout for local development.
- [`hasura`](https://github.com/tilt-dev/tilt-extensions/tree/master/hasura): Deploys [Hasura GraphQL Engine](https://hasura.io/) and monitors metadata/migrations changes locally.
- [`hello_world`](https://github.com/tilt-dev/tilt-extensions/tree/master/hello_world): Print "Hello world!". Used in [Extensions](https://docs.tilt.dev/extensions.html).
- [`helm_remote`](https://github.com/tilt-dev/tilt-extensions/tree/master/helm_remote): Install a remote Helm chart (in a way that gets properly uninstalled when running `tilt down`)
- [`helm_resource`](/helm_resource): Deploy with the Helm CLI. New Tilt users should prefer this approach over `helm_remote`.
- [`honeycomb`](https://github.com/tilt-dev/tilt-extensions/tree/master/honeycomb): Report dev env health metrics to [Honeycomb](https://honeycomb.io).
- [`jest_test_runner`](https://github.com/tilt-dev/tilt-extensions/tree/master/jest_test_runner): Jest JavaScript test runner. Example from [Contribute an Extension](https://docs.tilt.dev/contribute_extension.html).
- [`k8s_attach`](https://github.com/tilt-dev/tilt-extensions/tree/master/k8s_attach): Attach to an existing Kubernetes resource that's already in your cluster. View their health and live-update them in-place.
- [`kim`](https://github.com/tilt-dev/tilt-extensions/tree/master/kim): Use [kim](https://github.com/rancher/kim) to build images for Tilt
- [`knative`](https://github.com/tilt-dev/tilt-extensions/tree/master/knative): Use [knative serving](https://knative.dev/docs/serving/) to iterate on scale-to-zero servers.
- [`ko`](https://github.com/tilt-dev/tilt-extensions/tree/master/ko): Use [Ko](https://github.com/google/ko) to build Go-based container images
- [`kubebuilder`](https://github.com/tilt-dev/tilt-extensions/tree/master/kubebuilder): Enable live-update for developing [Kubebuilder](https://github.com/kubernetes-sigs/kubebuilder) projects.
- [`kubectl_build`](https://github.com/tilt-dev/tilt-extensions/tree/master/kubectl_build): Get faster build cycles and smaller disk usage by building docker images directly in the k8s cluster with [BuildKit CLI for kubectl](https://github.com/vmware-tanzu/buildkit-cli-for-kubectl).
- [`kubefwd`](https://github.com/tilt-dev/tilt-extensions/tree/master/kubefwd):  Use [Kubefwd](https://kubefwd.com/) to bulk-forward Kubernetes services.
- [`local_output`](https://github.com/tilt-dev/tilt-extensions/tree/master/local_output): Run a `local` command and get the output as string
- [`min_k8s_version`](https://github.com/tilt-dev/tilt-extensions/tree/master/min_k8s_version): Require a minimum Kubernetes version to run this Tiltfile.
- [`min_tilt_version`](https://github.com/tilt-dev/tilt-extensions/tree/master/min_tilt_version): Require a minimum Tilt version to run this Tiltfile.
- [`namespace`](https://github.com/tilt-dev/tilt-extensions/tree/master/namespace): Functions for interacting with namespaces.
- [`nix`](https://github.com/tilt-dev/tilt-extensions/tree/master/nix): Use [nix](https://nixos.org/guides/install-nix.html) to build nix-based container images.
- [`ngrok`](https://github.com/tilt-dev/tilt-extensions/tree/master/ngrok): Expose public URLs for your services with [`ngrok`](https://ngrok.com/).
- [`pack`](https://github.com/tilt-dev/tilt-extensions/tree/master/pack): Build container images using [pack](https://buildpacks.io/docs/install-pack/) and [buildpacks](https://buildpacks.io/).
- [`podman`](https://github.com/tilt-dev/tilt-extensions/tree/master/podman): Build container images using [podman](https://podman.io)
- [`print_tiltfile_dir`](https://github.com/tilt-dev/tilt-extensions/tree/master/print_tiltfile_dir): Print all files in the Tiltfile directory. If recursive is set to True, also prints files in all recursive subdirectories.
- [`procfile`](https://github.com/tilt-dev/tilt-extensions/tree/master/procfile): Create Tilt resources from a foreman Procfile.
- [`restart_process`](https://github.com/tilt-dev/tilt-extensions/tree/master/restart_process): Wrap a `docker_build` to restart the given entrypoint after a Live Update (replaces `restart_container()`)
- [`secret`](https://github.com/tilt-dev/tilt-extensions/tree/master/secret): Functions for creating secrets.
- [`snyk`](https://github.com/tilt-dev/tilt-extensions/tree/master/snyk): Use [Snyk](https://snyk.io) to test your containers, configuration files, and open source dependencies.
- [`syncback`](https://github.com/tilt-dev/tilt-extensions/tree/master/syncback): Sync files/directories from your container back to your local FS.
- [`tarfetch`](https://github.com/tilt-dev/tilt-extensions/tree/master/tarfetch): Fetch new and updated files from a container to your local FS.
- [`tests`](https://github.com/tilt-dev/tilt-extensions/tree/master/tests): Some common configurations for running your tests in Tilt.
- [`tilt_inspector`](https://github.com/tilt-dev/tilt-extensions/tree/master/tilt_inspector): Debugging server for exploring internal Tilt state.
- [`uibutton`](https://github.com/tilt-dev/tilt-extensions/tree/master/uibutton): Customize your Tilt dashboard with [buttons to run a command](https://blog.tilt.dev/2021/06/21/uibutton.html).
- [`wait_for_it`](https://github.com/tilt-dev/tilt-extensions/tree/master/wait_for_it): Wait until command output is equal to given output.

{% include api/extensions.html %}
