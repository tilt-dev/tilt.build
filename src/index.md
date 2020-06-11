---
title: Tilt
layout: home
---

<section class="Home2-hero">
  <div class="Home2-heroText">
    <h2 class="Home2-heroText-title">
      Productivity for teams building Kubernetes apps.
    </h2>
    <p class="Home2-heroText-subtitle">
      Smart Rebuilds, Continuous Feedback, Live Updates, Snapshots, and a lot more. <code class="Home2-heroText-subtitle-code">tilt up</code> and grok your workflow.
    </p>
  </div>
  <div class="Home2-heroIllustration">
    {% svg assets/svg/illustration-hero.svg %}
  </div>
</section>

{% include index_cta.html %}

<section class="Home2-product">
  <div class="Home2-product-UI">
    <img src="/assets/img/product-tilt.png">
  </div>

  <div class="Home2-product-Tiltfile">
    <header class="Home2-product-Tiltfile-header">
      <div class="Home2-product-Tiltfile-header-chromeDecoration">
        {% svg assets/svg/chrome-button.svg class="chrome-button1" %}
        {% svg assets/svg/chrome-button.svg class="chrome-button2" %}
        {% svg assets/svg/chrome-button.svg class="chrome-button3" %}
      </div>
      Tiltfile
    </header>
    <code class="Home2-product-Tiltfile-code">
      <p class="tiltfile-comment"># Deploy: tell Tilt what YAML to deploy</p>
      <p>k8s_yaml(<span class="tiltfile-arg">'app.yaml'</span>)</p>
      <p></p>
      <p class="tiltfile-comment"># Build: tell Tilt what images to build from which directories</p>
      <p>docker_build(<span class="tiltfile-arg">'companyname/frontend'</span>, <span class="tiltfile-arg">'frontend'</span>)</p>
      <p>docker_build(<span class="tiltfile-arg">'companyname/backend'</span>, <span class="tiltfile-arg">'backend'</span>)</p>
      <p class="tiltfile-comment"># ...</p>
      <p></p>
      <p class="tiltfile-comment"># Watch: tell Tilt how to connect locally (optional)</p>
      <p>k8s_resource(<span class="tiltfile-arg">'frontend'</span>, port_forwards=<span class="tiltfile-arg-value">8080</span>)</p>
    </code>
  </div>
  <p class="Home2-product-caption">Tilt understands your entire system, and makes it understandable to you.</p>
</section>

<section class="Home2-featuresIntro">
  <p class="Home2-featuresIntro-text">
    We’re focused on three feature verticals:<br/>
    <button class="Home2-featuresIntro-text-button Home2-featuresIntro-text-button--pillar1">Understand & orchestrate</button> your services, work <button class="Home2-featuresIntro-text-button Home2-featuresIntro-text-button--pillar2">smarter & faster</button> wherever you are, and <button class="Home2-featuresIntro-text-button Home2-featuresIntro-text-button--pillar3">team-based</button> productivity.
  </p>
</section>

<script async src="/assets/js/features.js"></script>

<h3 class="Home2-sectionHeading">What We Have in Store</h3>
<section class="Home2-features">
  <ul class="Home2-features-navList">
    {% for feature in site.data.features %}
      <li class="Home2-features-navItem Home2-features-navItem--pillar{{ feature.pillar }} js-featuresNavItem">
        <button class="Home2-features-navItem-button js-featuresNavItemButton" 
           data-feature-target="{{forloop.index}}"
           onclick="featureScroll(this)">
           {{feature.title}}
        </button>
        <div class="Home2-features-navItem-description">
        <div class="Home2-features-navItem-descriptionInner">
          {{feature.description}}
        </div>
        </div>
      </li>
    {% endfor %}
  </ul>
  <ul class="Home2-features-contentList">
    {% for feature in site.data.features %}
      <li class="Home2-features-contentItem js-featuresContentItem" 
          data-feature-id="{{ forloop.index }}">
        <button class="Home2-features-contentItem-title Home2-features-contentItem-title--pillar{{ feature.pillar }}" 
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

<script async src="/assets/js/testimonials.js"></script>

<h3 class="Home2-sectionHeading Home2-sectionHeading--testimonials">
  What People Are Saying
  <div class="Home2-testimonials-navList">
    <button class="Home2-testimonials-navItem is-selected"
            data-testimonial="yext"
            onclick="testimonialScroll(this)">
      {% svg assets/svg/testimonial-yext-logo.svg class="Home2-testimonials-navItem-svg Home2-testimonials-navItem-svg--yext" %}
    </button>
    <button class="Home2-testimonials-navItem" 
            data-testimonial="cluster-api"
            onclick="testimonialScroll(this)">
      {% svg assets/svg/testimonial-kubernetes-logo.svg class="Home2-testimonials-navItem-svg Home2-testimonials-navItem-svg--clusterApi" %}
    </button>
  </div>
</h3>

<div class="Home2-testimonialBlock">
<ul class="Home2-testimonialList">
  <li class="Home2-testimonial" data-testimonial="yext">
    <div class="Home2-testimonial-profile">
      <div class="Home2-testimonial-profile-photo"><img src="/assets/img/testimonial-profile-yext.jpg"></div>
      <div class="Home2-testimonial-profileInfo">
        <p class="Home2-testimonial-profileInfo-name">Tom Elliott</p>
        <p class="Home2-testimonial-profileInfo-role">Software Eng. Lead</p>
      </div>
      <div class="Home2-testimonial-profileSocial">
        <a href="https://twitter.com/theotherelliott" rel="noopener noreferrer" target="_blank"  class="Home2-testimonial-profileSocial-link Home2-testimonial-profileSocial-link--twitter" >
          {% svg assets/svg/social-twitter.svg %}
        </a>
        <a href="http://engblog.yext.com/author/telliott" rel="noopener noreferrer" target="_blank" class="Home2-testimonial-profileSocial-link Home2-testimonial-profileSocial-link--web">
          {% svg assets/svg/social-web.svg %}
        </a>
      </div>
    </div>
    <div class="Home2-testimonial-content">
      <p class="Home2-testimonial-content-quote">Tilt has helped us accelerate our adoption of Kubernetes by letting us iterate rapidly on configuration and cross cutting concerns, which previously proved difficult to test effectively. The versatility of Tiltfiles has helped Tilt slot into our existing workflows with ease.</p>
      <div class="Home2-testimonial-content-meta">
        {% svg assets/svg/testimonial-yext-logo.svg class="Home2-testimonial-content-meta-svg" %}
        <p class="Home2-testimonial-content-meta-text">Yext builds a Search Experience Cloud platform, which puts customers in control of their facts online. They have a team of over 900 employees.</p>
      </div>
    </div>
  </li>
  <li class="Home2-testimonial" data-testimonial="cluster-api">
    <div class="Home2-testimonial-profile">
      <div class="Home2-testimonial-profile-photo"><img src="/assets/img/testimonial-profile-cluster-api.jpg"></div>
      <div class="Home2-testimonial-profileInfo">
        <p class="Home2-testimonial-profileInfo-name">Jason DeTiberus</p>
        <p class="Home2-testimonial-profileInfo-role">Co-Maintainer</p>
      </div>
      <div class="Home2-testimonial-profileSocial">
        <a href="https://blogs.vmware.com/cloudnative/author/jasondetiberus/" rel="noopener noreferrer" target="_blank" class="Home2-testimonial-profileSocial-link Home2-testimonial-profileSocial-link--web">
          {% svg assets/svg/social-web.svg %}
        </a>
      </div>
    </div>
    <div class="Home2-testimonial-content">
      <p class="Home2-testimonial-content-quote">Not only did Tilt help us with orchestrating the deployment of changes for testing, live_update allowed us to start testing the changes without needing to wait for image builds. Tilt enabled us to move from painstakingly long dev and test cycles to rapid iterative development across the project.</p>
      <div class="Home2-testimonial-content-meta">
        {% svg assets/svg/testimonial-kubernetes-logo.svg class="Home2-testimonial-content-meta-svg" %}
        <p class="Home2-testimonial-content-meta-text">Cluster API is an open-source Kubernetes project to bring declarative, Kubernetes-style APIs to cluster creation, configuration, and management. It has over 230 contributors.</p>
      </div>
    </div>
  </li>
</ul>
</div>

<h3 class="Home2-sectionHeading">Learn More</h3>
<section class="Home2-resources">
  <ul class="Home2-resources-list">
    <li class="Home2-resources-listItem">
      <div class="Home2-resources-listItem-text">
        <h4 class="Home2-subsectionHeading Home2-subsectionHeading--resources">
          {% svg assets/svg/resources-docs.svg class="Home2-resources-svg" %}
          Read the Docs
        </h4>
        <p>Already have a Dockerfile and a Kubernetes config? Set up Tilt in no time and start getting things done. </p>
      </div>
      <a href="{{site.docsurl}}/" class="Home2-resources-link">Check out Docs</a>
    </li>
    <li class="Home2-resources-listItem">
      <div class="Home2-resources-listItem-text">
        <h4 class="Home2-subsectionHeading Home2-subsectionHeading--resources">
        {% svg assets/svg/social-slack.svg class="Home2-resources-svg" %}
          Chat with Us
        </h4>
        <p>Find us in the #tilt channel of the official Kubernetes Slack. We’re there Mon-Fri EST business hours. We don’t bite.</p>
      </div>
      <a href="https://slack.k8s.io/" class="Home2-resources-link">Get Your Invite</a>
    </li>
    <li class="Home2-resources-listItem">
      <div class="Home2-resources-listItem-text">
        <h4 class="Home2-subsectionHeading Home2-subsectionHeading--resources">
          {% svg assets/svg/resources-videos.svg class="Home2-resources-svg" %}
          Quick Start
        </h4>
        <p>Short & sweet videos about Tilt</p>
      </div>
      <div class="Home2-resources-listItem-cta">
        <a href="https://www.youtube.com/watch?v=MIzf9vDs9JU" rel="noopener noreferrer" target="_blank" class="Home2-resources-link">Tilt’s Main Features <span class="Home2-resources-link-meta">6m</span></a>
        <a href="https://www.youtube.com/watch?v=HSFGKxvxsWs&t=69s" rel="noopener noreferrer" target="_blank" class="Home2-resources-link">Basic Concepts <span class="Home2-resources-link-meta">5.5m</span></a>
        <a href="https://www.youtube.com/watch?v=MhYIsTwwPC8" rel="noopener noreferrer" target="_blank" class="Home2-resources-link">Setting up Tilt <span class="Home2-resources-link-meta">15.5m</span></a>
      </div>
    </li>
    <li class="Home2-resources-listItem">
      <div class="Home2-resources-listItem-text">
        <h4 class="Home2-subsectionHeading Home2-subsectionHeading--resources">
          {% svg assets/svg/resources-github.svg class="Home2-resources-svg" %}
          GitHub Issues
        </h4>
        <p>Have an idea or a bug to report? Check our GitHub issues. In case you want to tackle some of your own we have a collection for that.</p>
      </div>
      <a href="https://github.com/{{site.github_username}}/tilt" rel="noopener noreferrer" target="_blank" class="Home2-resources-link">Tilt GitHub</a>
    </li>
    <li class="Home2-resources-listItem">
      <div class="Home2-resources-listItem-text">
        <h4 class="Home2-subsectionHeading Home2-subsectionHeading--resources">
          {% svg assets/svg/resources-contact.svg class="Home2-resources-svg" %}
          Email us
        </h4>
        <p>Have questions or feature requests for Tilt? Want to use it for your company? Just want to say hi? We love hearing from you!</p>
      </div>
      <a href="mailto:hi@tilt.dev" class="Home2-resources-link">hi@tilt.dev</a>
    </li>
    <li class="Home2-resources-listItem">
      <div class="Home2-resources-listItem-text">
        <h4 class="Home2-subsectionHeading Home2-subsectionHeading--resources">
          {% svg assets/svg/resources-mailing-list.svg class="Home2-resources-svg" %}
          Our Mailing List
        </h4>
        <p>Keep up with Multi-Service Development and all things Tilt.</p>
      </div>
      <div class="Home2-resources-listItem-cta">
        <form action="https://www.getdrip.com/forms/507796156/submissions" method="post" data-drip-embedded-form="507796156">
          <label for="drip-email" class="Home2-resources-label">Your Email</label>
          <input class="Home2-resources-input" type="email" id="drip-email" name="fields[email]" value="" placeholder="me@company.com" />
          <button class="Home2-resources-button" type="submit" data-drip-attribute="sign-up-button">
            Subscribe
          </button>
          <div style="display: none;" aria-hidden="true">
            <label for="website">Website</label><br />
            <input type="text" id="website" name="website" tabindex="-1" autocomplete="false" value="" />
          </div>
        </form>
      </div>
    </li>
  </ul>
</section>
