---
title: Tilt Snippets
layout: docs
---

# Snippets Library

<ul>
{% assign snippets = site.data.snippets %}
{% assign ordered = site.data.snippet_order %}
{% assign nonordered = snippets.keys - ordered %}
{% assign keys = ordered + nonordered %}
{% for name in keys %}
{% assign snippet = snippets[name] %}
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

# TBD

## Local snippets

Items from [Local Resource](local_resource.html)

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
