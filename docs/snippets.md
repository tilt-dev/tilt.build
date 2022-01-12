---
title: Tilt Snippets
layout: docs
sidebar: reference
---

# Snippets Library

<ul>
{% for item in site.data.snippets %}
{% assign name = item[0] %}
{% assign snippet = item[1] %}
<li id="snip_{{name}}">
<div>{{snippet.title}}</div>
<div>{{snippet.description}}</div>
<div>stage: {{snippet.release_stage}}</div>
{% if snippet.docs_link %}<a href="{{snippet.docs_link}}">Reference</a>{% endif %}
{% highlight python %}
{{snippet.code}}
{% endhighlight %}
</li>
{% endfor %}
</ul>

# Outline

## Tiltfile Concepts snippets

Items from [Tiltfile Concepts](tiltfile_concepts.html) page

- Build a docker image (docker_build)
- Deploy k8s yaml (k8s_yaml)
- Deploy a local helm chart (helm)
- Deploy k8s objects with kustomize (kustomize)
- Run a custom command to generate k8s yaml (k8s_yaml + local)
- Port-forward a k8s resource (k8s_resource with port_forward)
- Configure k8s resources


## K8s snippets

- Create a k8s secret (secret extension)
- Create a k8s configmap (configmap extension)


## Docker Compose snippets

- Use a docker-compose file (docker_compose)
- Add overrides to [docker-compose](api.html#api.docker_compose)


## Local snippets

Items from [Local Resource](local_resource.html)

- Run yarn
- Build and run a go server locally
- Build and run a js server locally
- Display the k8s api server logs
- Run a generic local build + server
- Proxy a remote port to localhost with socat
- Run an ngrok tunnel


## Language snippets

Take simple examples from the following, and link to the full example.

- [Go](example_go.html)
- [Python](example_python.html)
- [Nodejs](example_nodejs.html)
- [Java](example_java.html)
- [C#](example_csharp.html)


## Extensions snippets

- Useful things from [extensions list](api.html#extensions)

## New snippets

- Run a docker container (*new* `docker_run` extension that uses inline docker_compose?)
- Deploy an image to k8s (e.g., redis) (*new* deployment/service extensions modeled after configmap, secret)
