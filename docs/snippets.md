---
title: Tiltfile Snippets
layout: docs
sidebar: guides
---

<ul class="Docs-snippets-list">
  {% assign snippets = site.data.snippets %}
  {% assign keys = snippets | keys %}
  {% assign ordered = site.data.snippet_order %}
  {% assign allkeys = ordered | concat: keys | uniq %}

  {% for name in allkeys %}
  {% assign snippet = snippets[name] %}
  <li id="snip_{{name}}" class="Docs-snippets-item">
    <header class="Docs-snippets-item-header">
      <div>
        <h3 class="Docs-snippets-item-title">{{snippet.title}}</h3>
        <p class="Docs-snippets-item-description">{{snippet.description}}</p>
      </div>
      <a class="Docs-snippets-item-permalink" href="#snip_{{name}}">Permalink</a>
    </header>
    
    <!-- <div>stage: {{snippet.release_stage}}</div> -->

    {% highlight python -%}
      {{snippet.code | strip}}
    {% endhighlight -%}

    <footer class="Docs-snippets-item-footer">
      {% if snippet.docs_link %}
        <a href="{{snippet.docs_link}}">Read More…</a>
      {% endif %}
    </footer>
  </li>
  {% endfor %}
</ul>
