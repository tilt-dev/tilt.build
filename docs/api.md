---
title: Tiltfile API Reference
description: "A complete reference of functions available in your Tiltfile."
layout: docs
---

Tiltfiles are written in _Starlark_, a dialect of Python. For more information on Starlark's built-ins, [see the **Starlark Spec**](https://github.com/bazelbuild/starlark/blob/master/spec.md). The rest of this page details Tiltfile-specific functionality.

## Extensions

Can't find what you're looking for in this reference?

Tilt users can contribute [extensions](extensions.html) to share with other users. Browse them for
examples of what you can do with a Tiltfile. Load them into your own Tiltfile. Includes:

- [`conftest`](https://github.com/tilt-dev/tilt-extensions/tree/master/conftest): Use [Conftest](https://www.conftest.dev/) to test your configuration files.
- [`docker_build_sub`](https://github.com/tilt-dev/tilt-extensions/tree/master/docker_build_sub): Specify extra Dockerfile directives in your Tiltfile beyond [`docker_build`](https://docs.tilt.dev/api.html#api.docker_build).
- [`git_resource`](https://github.com/tilt-dev/tilt-extensions/tree/master/git_resource): Deploy a dockerfile from a remote repository -- or specify the path to a local checkout for local development.
- [`helm_remote`](https://github.com/tilt-dev/tilt-extensions/tree/master/helm_remote): Install a remote Helm chart (in a way that gets properly uninstalled when running `tilt down`)
- [`jest_test_runner`](https://github.com/tilt-dev/tilt-extensions/tree/master/jest_test_runner): Jest JavaScript test runner. Example from [Contribute an Extension](https://docs.tilt.dev/contribute_extension.html).
- [`local_output`](https://github.com/tilt-dev/tilt-extensions/tree/master/local_output): Run a `local` command and get the output as string
- [`min_tilt_version`](https://github.com/tilt-dev/tilt-extensions/tree/master/min_tilt_version): Require a minimum Tilt version to run this Tiltfile.
- [`min_k8s_version`](https://github.com/tilt-dev/tilt-extensions/tree/master/min_k8s_version): Require a minimum Kubernetes version to run this Tiltfile.
- [`namespace`](https://github.com/tilt-dev/tilt-extensions/tree/master/namespace): Functions for interacting with namespaces.
- [`pack`](https://github.com/tilt-dev/tilt-extensions/tree/master/pack): Build container images using [pack](https://buildpacks.io/docs/install-pack/) and [buildpacks](https://buildpacks.io/).
- [`print_tiltfile_dir`](https://github.com/tilt-dev/tilt-extensions/tree/master/print_tiltfile_dir): Print all files in the Tiltfile directory. If recursive is set to True, also prints files in all recursive subdirectories.
- [`procfile`](https://github.com/tilt-dev/tilt-extensions/tree/master/procfile): Create Tilt resources from a foreman Procfile.
- [`restart_process`](https://github.com/tilt-dev/tilt-extensions/tree/master/restart_process): Wrap a `docker_build` to restart the given entrypoint after a Live Update (replaces `restart_container()`)
- [`secret`](https://github.com/tilt-dev/tilt-extensions/tree/master/secret): Functions for creating secrets.

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
