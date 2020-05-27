---
title: Tilt
layout: home2
---

<section class="Home2-hero">
  <div class="Home2-heroText">
    <h2 class="Home2-heroText-title">
      Productivity for teams building Kubernetes apps.
    </h2>
    <p class="Home2-heroText-subtitle">
      Smart Rebuilds, Continuous Feedback, Live Updates, Snapshots and a lot more. <code class="Home2-heroText-subtitle-code">tilt up</code> and grok your workflow.
    </p>
  </div>
  <div class="Home2-heroIllustration">
    <img src="/assets/img/hero-illustration.png">
  </div>
</section>

{% include index2_cta.html %}

<section class="Home2-product">
  <div class="Home2-product-UI">
    <img src="/assets/img/product-tilt.png">
  </div>

  <div class="Home2-product-Tiltfile">
    <img src="/assets/img/product-tiltfile.png" class="Home2-product-Tiltfile-imgPlaceholder">
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


<section class="Home2-features">
  <p class="Home2-features-introText">We’re focused on three feature verticals:<br/><span class="Home2-features-introText-pillar1">Understand & orchestrate</span> your services, work <span class="Home2-features-introText-pillar2">smarter & faster</span> wherever you are and <span class="Home2-features-introText-pillar3">team-based</span> productivity.</p>

  <h3>What We Have in Store</h3>
  <div class="Home2-features-menu">
    <ul class="Home2-features-menu-nav">
      <li><a href="#">Very Holistic</a></li>
      <li><a href="#">Orderly Orchestration</a></li>
      <li><a href="#">Magic UI</a></li>
      <li><a href="#">live_update</a></li>
      <li><a href="#">Code in Flow</a></li>
      <li><a href="#">Fastr Workflow</a></li>
      <li><a href="#">Snapshots</a></li>
      <li><a href="#">Built-In Best Practices</a></li>
      <li><a href="#">Painless Onboarding</a></li>
      <li><a href="#">Quantified Dev Experience</a></li>
    </ul>
    <ul class="Home2-features-menu-content">
      <li>
        <a class="Home2-features-link Home2-features-link--pillar1" href="#">Very Holistic</a>
        <div>
          <h4>Very Holistic</h4>
          <p>See all the pieces of your app, and trigger custom workflows like seeding databases or creating infrastructure.</p>
        </div>
      </li>
      <li>
        <a class="Home2-features-link Home2-features-link--pillar1" href="#">Orderly Orchestration</a>
        <div>
          <h4>Orderly Orchestration</h4>
          <p>Our engine starts the whole app runs automated rebuilds as you edit in your IDE. Get a continuous feedback loop with your logs, broken builds, runtime errors.</p>
        </div>
      </li>
      <li>
        <a class="Home2-features-link Home2-features-link--pillar1" href="#">Magic UI</a>
        <div>
          <h4>Magic UI</h4>
          <p>Work with Kubernetes without needing to be an expert. And if you are an expert, no more 20 questions with Kubectl. 🙌</p>
        </div>
      </li>
      <li>
        <a class="Home2-features-link Home2-features-link--pillar2" href="#">live_update</a>
        <div>
          <h4>live_update</h4>
          <p>Tilt's live_update deploys code to running containers, in seconds not minutes. Even for compiled languages or changing dependencies, live_update is fast and reliable.</p>
        </div>
      </li>
      <li>
        <a class="Home2-features-link Home2-features-link--pillar2" href="#">Code in Flow</a>
        <div>
          <h4>Code in Flow</h4>
          <p>Tilt responsively handles the tedious and repetitive parts of your workflow and gives you peripheral vision so you find errors faster. Recapture the magic of hacking with immediate feedback.</p>
        </div>
      </li>
      <li>
        <a class="Home2-features-link Home2-features-link--pillar2" href="#">Fastr Workflow</a>
        <div>
          <h4>Fastr Workflow</h4>
          <p>Tilt’s flexible integration points let you use your existing workflows. Supercharge your process with optimized build caching and powerful K8s-aware scripting. Shave time off your iterative loops.</p>
        </div>
      </li>
      <li>
        <a class="Home2-features-link Home2-features-link--pillar3" href="#">Snapshots</a>
        <div>
          <h4>Snapshots</h4>
          <p>Snapshots lets you share your dev environment & collaborate on issues as quickly as looking at the monitor next to you.</p>
        </div>
      </li>
      <li>
        <a class="Home2-features-link Home2-features-link--pillar3" href="#">Built-In Best Practices</a>
        <div>
          <h4>Built-In Best Practices</h4>
          <p>We’ve codified best practices to give your team a common development path and ensure reproducibility. Anyone can start the app – new hires just `tilt up`.</p>
        </div>
      </li>
      <li>
        <a class="Home2-features-link Home2-features-link--pillar3" href="#">Painless Onboarding</a>
        <div>
          <h4>Painless Onboarding</h4>
          <p>We made Tilt platform agnostic, versatile and easy to configure, because we know every setup is different. You can integrate Tilt in stages for a smooth transition.</p>
        </div>
      </li>
      <li>
        <a class="Home2-features-link Home2-features-link--pillar3" href="#">Quantified Dev Experience</a>
        <div>
          <h4>Quantified Dev Experience</h4>
          <p>We care about a good developer experience and we know its hard to measure. Our team features include analytics to help you understand usage and fix slowdowns proactively and show impact.</p>
        </div>
      </li>
    </ul>
  </div>
</section>

{% include index2_cta.html %}

<section class="Home2-testimonials">
  <h3>What People Are Saying</h3>

  <h4>Tom Elliott</h4>
  <p>Software Eng. Lead</p>
  <a href="#">TWITTER</a>
  <a href="#">WEBSITE</a>

  <p>Tilt has helped us accelerate our adoption of Kubernetes by letting us iterate rapidly on configuration and cross cutting concerns, which previously proved difficult to test effectively. The versatility of Tiltfiles has helped Tilt slot into our existing workflows with ease.</p>

  <p>Yext builds a Search Experience Cloud platform, which puts customers in control of their facts online. They have a team of over 900 employees.</p>
</section>

<section class="Home2-resources">
  <h3>Learn More</h3>

  <ul>
    <li>
      <h4>Read the Docs</h4>
      <p>Already have a Dockerfile and a Kubernetes config? Set up Tilt in no time and start getting things done. </p>
      <button>Check out Docs! </button>
    </li>
    <li>
      <h4>Chat with Us</h4>
      <p>Find us in the #tilt channel inside of the Kubernetes Slack. We’re there Mon-Fri EST business hours. We don't bite.</p>
      <button>Get Your Invite</button>
    </li>
    <li>
      <h4>Screen Time</h4>
      <p>Short & sweet videos about Tilt</p>
      <button>Tilt’s Main Features <span>6m</span></button>
      <button>Basic Concepts <span>5.5m</span></button>
      <button>Setting up Tilt <span>15.5m</span></button> 
    </li>
    <li>
      <h4>GitHub Issues</h4>
      <p>Have an idea or a bug to report? Check our GitHub issues. In case you want to tackle some of your own we have a collection for that.</p>
      <button>Tilt GitHub</button>
    </li>
    <li>
      <h4>Email us</h4>
      <p>Have questions or feature requests for Tilt? Want to use it for your company? Just want to say hi? We love hearing from you!</p>
      <button>hi@tilt.dev</button>
    </li>
    <li>
      <h4>Our Mailing List</h4>
      <p>Keep up with Multi-Service Development and all things Tilt.</p>
      <button>Submit</button>
    </li>
  </ul>
</section>