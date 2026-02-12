---
title: Tilt
layout: home
---

<section class="Home-hero">
  <div class="Home-heroText">
    <h2 class="Home-heroText-title">
      A toolkit for fixing the pains of microservice development.
    </h2>
    <p class="Home-heroText-subtitle">
      Are your servers running locally? In Kubernetes? Both? 
      Tilt gives you smart rebuilds and live updates everywhere so that you can make progress.
    </p>
  </div>
  <div class="Home-heroIllustration">
    {% svg assets/svg/illustration-hero.svg %}
  </div>
</section>

{% include index_cta.html %}

<section class="Home-product">
  <div class="Home-product-UI">
    <img src="/assets/img/product-tilt.png">
  </div>

  <div class="Home-product-Tiltfile">
    <header class="Home-product-Tiltfile-header">
      <div class="Home-product-Tiltfile-header-chromeDecoration">
        {% svg assets/svg/chrome-button.svg class="chrome-button1" %}
        {% svg assets/svg/chrome-button.svg class="chrome-button2" %}
        {% svg assets/svg/chrome-button.svg class="chrome-button3" %}
      </div>
      Tiltfile
    </header>
    <code class="Home-product-Tiltfile-code">
      <p class="tiltfile-comment"># Deploy: tell Tilt what YAML to deploy</p>
      <p>k8s_yaml(<span class="tiltfile-arg">'app.yaml'</span>)</p>
      <p></p>
      <p class="tiltfile-comment"># Build: tell Tilt what images to build from which directories</p>
      <p>docker_build(<span class="tiltfile-arg">'companyname/api'</span>, <span class="tiltfile-arg">'api'</span>)</p>
      <p>docker_build(<span class="tiltfile-arg">'companyname/web'</span>, <span class="tiltfile-arg">'web'</span>)</p>
      <p class="tiltfile-comment"># ...</p>
      <p></p>
      <p class="tiltfile-comment"># Watch: tell Tilt how to connect locally (optional)</p>
      <p>k8s_resource(<span class="tiltfile-arg">'api'</span>, port_forwards=<span class="tiltfile-arg-value">"5734:5000"</span>, labels=[<span class="tiltfile-arg-value">"backend"</span>])</p>
    </code>
  </div>
  <p class="Home-product-caption">Tilt understands your entire system, and makes it understandable to you.</p>
</section>

<section class="Home-featuresIntro">
  <p class="Home-featuresIntro-text">
    We’re focused on three feature verticals:<br/>
    <button class="Home-featuresIntro-text-button Home-featuresIntro-text-button--pillar1">Understand & orchestrate</button> your services, work <button class="Home-featuresIntro-text-button Home-featuresIntro-text-button--pillar2">smarter & faster</button> wherever you are, and <button class="Home-featuresIntro-text-button Home-featuresIntro-text-button--pillar3">team-based</button> productivity.
  </p>
</section>

<script async src="/assets/js/features.js"></script>

<h3 class="Home-sectionHeading Home-sectionHeading--features">What We Have in Store</h3>
<section class="Home-features">
  <ul class="Home-features-navList">
    {% for feature in site.data.features %}
      <li class="Home-features-navItem Home-features-navItem--pillar{{ feature.pillar }} js-featuresNavItem">
        <button class="Home-features-navItem-button js-featuresNavItemButton" 
           data-feature-target="{{forloop.index}}"
           onclick="featureScroll(this)">
           {{feature.title}}
        </button>
        <div class="Home-features-navItem-description">
        <div class="Home-features-navItem-descriptionInner">
          {{feature.description}}
        </div>
        </div>
      </li>
    {% endfor %}
  </ul>
  <div class="Home-features-contentList-gradient"></div>
  <ul class="Home-features-contentList">
    {% for feature in site.data.features %}
      <li class="Home-features-contentItem js-featuresContentItem" 
          data-feature-id="{{ forloop.index }}">
        <button class="Home-features-contentItem-title Home-features-contentItem-title--pillar{{ feature.pillar }}" 
          data-feature-target="{{forloop.index}}"
          onclick="featureScroll(this)">
          {{feature.title}}
        </button>
        <div>
          {{feature.description}}
        </div>
      </li>
    {% endfor %}
  </ul>
</section>

{% include index_cta.html %}

<script async src="/assets/js/cta.js"></script>

<h3 class="Home-sectionHeading">See Tilt in Action</h3>
<div class="Home-video">
  <iframe width="560" height="315" src="https://www.youtube.com/embed/FSMc3kQgd5Y?controls=0" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>

<h3 class="Home-sectionHeading">Learn More</h3>
<section class="Home-resources">
  <ul class="Home-resources-list">
    <li class="Home-resources-listItem">
      <div class="Home-resources-listItem-text">
        <h4 class="Home-subsectionHeading Home-subsectionHeading--resources">
          {% svg assets/svg/resources-docs.svg class="Home-resources-svg" %}
          Read the Docs
        </h4>
        <p>Already have a Dockerfile and a Kubernetes config? Set up Tilt in no time and start getting things done. </p>
      </div>
      <a href="{{site.docsurl}}/" class="Home-resources-link">Check out Docs</a>
    </li>
    <li class="Home-resources-listItem">
      <div class="Home-resources-listItem-text">
        <h4 class="Home-subsectionHeading Home-subsectionHeading--resources">
        {% svg assets/svg/social-slack.svg class="Home-resources-svg" %}
          Chat with Us
        </h4>
        <p>Find us in the #tilt channel of the official Kubernetes Slack. We’re there Mon-Fri EST business hours. We don’t bite.</p>
      </div>
      <a href="https://slack.k8s.io/" class="Home-resources-link">Get Your Invite</a>
    </li>
    <li class="Home-resources-listItem">
      <div class="Home-resources-listItem-text">
        <h4 class="Home-subsectionHeading Home-subsectionHeading--resources">
          {% svg assets/svg/resources-videos.svg class="Home-resources-svg" %}
          Quick Start
        </h4>
        <p>Short & sweet videos about Tilt</p>
      </div>
      <div class="Home-resources-listItem-cta">
        <a href="https://www.youtube.com/watch?v=MIzf9vDs9JU" rel="noopener noreferrer" target="_blank" class="Home-resources-link">Tilt’s Main Features <span class="Home-resources-link-meta">6m</span></a>
        <a href="https://www.youtube.com/watch?v=HSFGKxvxsWs&t=69s" rel="noopener noreferrer" target="_blank" class="Home-resources-link">Basic Concepts <span class="Home-resources-link-meta">5.5m</span></a>
        <a href="https://www.youtube.com/watch?v=MhYIsTwwPC8" rel="noopener noreferrer" target="_blank" class="Home-resources-link">Setting up Tilt <span class="Home-resources-link-meta">15.5m</span></a>
      </div>
    </li>
  </ul>
  <ul class="Home-resources-list Home-resources-list-2">
    <li class="Home-resources-listItem Home-resources-listItem--spacer"></li>
    <li class="Home-resources-listItem">
      <div class="Home-resources-listItem-text">
        <h4 class="Home-subsectionHeading Home-subsectionHeading--resources">
          {% svg assets/svg/resources-github.svg class="Home-resources-svg" %}
          GitHub Issues
        </h4>
        <p>Have an idea or a bug to report? Check our GitHub issues. In case you want to tackle some of your own we have a collection for that.</p>
      </div>
      <a href="https://github.com/{{site.github_username}}/tilt" rel="noopener noreferrer" target="_blank" class="Home-resources-link">Tilt GitHub</a>
    </li>
    <li class="Home-resources-listItem Home-resources-listItem--spacer"></li>
  </ul>
</section>
