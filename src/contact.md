---
layout: page
title: Contact Us
permalink: /contact
---

<div class="u-marginBottomUnit">
Curious about what we're doing? Got a problem with Tilt? Just want to say hi? Here are some ways to get in touch with us:
    <ul class="u-marginTop0_5 circle-bullet">
        <li>
            Find us in the <a href="https://kubernetes.slack.com/messages/CESBL84MV/" target="_blank"><strong>#tilt</strong> channel</a> in the Kubernetes Slack. (Not a member? <a href="https://slack.k8s.io/" target="_blank">Get your invite here</a>.)
        </li>
        <li>
            Look through our <a href="https://github.com/windmilleng/tilt/issues" target="_blank">Github issues</a> (or file your own)
        </li>
        <li>
            <a href="mailto:hi@windmill.engineering">Email us directly</a>
        </li>
        <li>
            Fill out the form below!
        </li>
    </ul>
</div>

<form action="https://www.getdrip.com/forms/934127760/submissions" method="post" data-drip-embedded-form="934127760">
<div class="formItem">
  <label for="drip-name">Name</label>
  <input type="text" id="drip-name" name="fields[name]" value="" />
</div>
<div class="formItem">
  <label for="drip-email">Email Address</label>
  <input type="email" id="drip-email" name="fields[email]" value="" />
</div>

<div class="formItem">
  <div class="formItem-label">I’m interested in…</div>

  <div class="row">
  <div class="formItem-option col-1of2">
    <label for="drip-interest-try-tilt">trying out Tilt</label>
    <input type="checkbox" id="drip-interest-try-tilt" name="fields[interest_try_tilt]" value="true" />
    <div class="formItem-checkbox"></div>
  </div>

  <div class="formItem-option col-1of2">
    <label for="drip-interest-tilt-features">requesting Tilt features</label>
    <input type="checkbox" id="drip-interest-tilt-features" name="fields[interest_tilt_features]" value="true" />
    <div class="formItem-checkbox"></div>
  </div>

  <div class="formItem-option col-1of2">
    <label for="drip-interest-job">applying for a job to help build better local Kubernetes dev tools</label>
    <input type="checkbox" id="drip-interest-job" name="fields[interest_job]" value="true" />
    <div class="formItem-checkbox"></div>
  </div>

  <div class="formItem-option col-1of2">
    <label for="drip-interest-learning">learning more</label>
    <input type="checkbox" id="drip-interest-learning" name="fields[interest_learning]" value="true" />
    <div class="formItem-checkbox"></div>
  </div>
  </div>
</div>

<div class="formItem">
  <label for="drip-message">Message</label>
  <textarea id="drip-message" name="fields[message]" rows="5"></textarea>
</div>

<div style="display: none;" aria-hidden="true">
  <label for="website">Website</label><br />
  <input type="text" id="website" name="website" tabindex="-1" autocomplete="false" value="" />
</div>

<div class="u-marginBottom2_5">
  <button class="brandButton" type="submit" data-drip-attribute="sign-up-button">
    {% include brandButtonBg.html %}
    <div class="buttonLabel brandButton-text">
      Submit
    </div>
  </button>
</div>

</form>
