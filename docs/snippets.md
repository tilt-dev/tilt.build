---
title: Tiltfile Snippets
layout: docs
sidebar: gettingstarted
hideHelpfulForm: true
---

> **Want to contribute?**  
> Follow [this guide](https://github.com/tilt-dev/tilt.build/blob/master/contributing-snippets.md) to find out how to submit your own snippets!

<h3>Filter by tags</h3>
<div class="Docs-snippets-tag-cloud">
</div>

<ul class="Docs-snippets-list">
  {% assign snippets = site.data.snippets %}
  {% assign keys = snippets | keys %}
  {% assign ordered = site.data.snippet_order %}
  {% assign allkeys = ordered | concat: keys | uniq %}

  {% for name in allkeys %}
  {% assign snippet = snippets[name] %}
  <li id="snip_{{name}}" class="Docs-snippets-item" data-codeblock="snip_{{name}}" data-tags="{{ snippet.tags | sort | join: ' '}}">
    <div class="Docs-snippets-content">
      <header class="Docs-snippets-item-header">
        <div>
          {% if snippet.contributor %}
          <div class="Docs-snippets-item-contributor">✉️ submitted by <a href="https://github.com/{{snippet.contributor}}">{{snippet.contributor}}</a></div>
          {% endif %}
          <a class="Docs-snippets-item-permalink" href="#snip_{{name}}">Permalink</a>
        </div>
        <div>
          <h3 class="Docs-snippets-item-title">{{snippet.title}}</h3>
          <p class="Docs-snippets-item-description">{{snippet.description}}</p>
        </div>
      </header>

      {%- highlight python -%}
        {{snippet.code | strip}}
      {%- endhighlight -%}

      {% if snippet.link %}
        <footer class="Docs-snippets-item-footer">
          <h5>Reference</h5>
          <a href="{{snippet.link.href}}">
            {{ snippet.link.title }}
          </a>
        </footer>
      {% endif %}
    </div>
  </li>
  {% endfor %}
</ul>

<script src="{{ '/assets/js/snippets.js' | relative_url }}" defer></script>
