---
title: Hello Tilt
layout: landing
---

{% svg assets/svg/hello.svg class="landingLogoHello" %}
{% svg assets/svg/logo-wordmark.svg class="landingLogoWordmark" %}

<h2 class="subtitle">
Tilt gives you a powerful microservice dev environment that seamlessly bridges the gap between local and Kubernetes.
</h2>

<div class="subtitleAside">
Think <code>docker-compose up</code> or <code>docker build . && kubectl apply</code>
</div>

<div class="landingBlock">

  <h2>What does it do?</h2>
  
  <ul class="supportingExampleList">
  <li>Watch your files for edits</li>
  
  <li>Applies changes automatically & builds your container images in real-time</li>
  
  <li>Makes your builds way faster</li>
  
  <li>Combines all of the debug information into one clean, efficient interface</li>
  
  <li>No guessing games with kubectl ever again</li>
  </ul>
  
  <div class="u-colorRed u-marginTop1_75">
  The engineer who sent you to this page has already configured Tilt for your
  project. You can get started right now!
  </div>

</div>

## Install Locally

<div class="u-muted u-marginBottom0_25">
  The quick install downloads the Tilt command-line tool.
</div>

```bash
curl -fsSL https://raw.githubusercontent.com/windmilleng/tilt/master/scripts/install.sh | bash
```

<div class="detailBlock u-marginBottom1_75">
<a href="https://docs.tilt.dev/install">
More options in the docs
</a>
</div>

## Get Started

<div class="u-muted u-marginBottom0_25">
All you need to do is go to any project with a <code>Tiltfile</code> and <code>tilt up</code>
</div>

```bash
tilt up
```

<div class="detailBlock u-marginBottom1_75">
<a href="https://docs.tilt.dev">
To learn more about how Tilt works check out our friendly docs.
</a>
</div>

<div class="landingBlock u-colorRed">
Hack, Observe, Repeat! Now that you have run tilt up, you can...
</div>

<ol class="supportingExampleColumns">
<li>
<img class="subArrow subArrow--1" src="/assets/docimg/welcome-page-arrow-1.png">
Browse logs by server to understand what’s happening
</li>

<li>
<img class="subArrow subArrow--2" src="/assets/docimg/welcome-page-arrow-2.png">
Easily spot errors when something goes wrong
</li>

<li>
<img class="subArrow subArrow--3" src="/assets/docimg/welcome-page-arrow-3.png">
Keep an eye on build and health status as you code
</li>
</ol>

<img class="supportingExampleImage" src="/assets/docimg/welcome-page-screenshot.png">

<h2 class="u-textAlignCenter u-marginTop1_5">Watch the Demo</h2>

[![Watch the Demo](/assets/docimg/welcome-page-videothumb.png)](https://www.youtube.com/watch?v=oSljj0zHd7U)

<div class="landingBlock u-muted">
  This Welcome to Tilt README is for application engineers who have been sent
  here after Tilt was set up in your project.
  <br><br>
  Don’t have your project configured yet?
  <a href="https://docs.tilt.dev/tutorial.html">Read how here.</a>
  <br><br>
  To create your own Welcome README with project-specific instructions, just
  <a href="https://github.com/windmilleng/tilt-init">
  fork and edit the tilt-init repo on GitHub
  </a>!
</div>
