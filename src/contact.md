---
layout: page
title: Contact Us
permalink: /contact
---

<div class="col-3of4 u-marginBottomUnit">
If you'd like to learn more about what we're doing, you can either
email <a href="mailto:dan@windmill.engineering">Dan</a> or <a href="mailto:nick@windmill.engineering">Nick</a>,
or fill out the form below.
</div>

<form action="https://formspree.io/hi@windmill.engineering" method="POST">
<div class="formItem">
  <label for="name">Name</label>
  <input id="name" name="name" required>
</div>

<div class="formItem">
  <label for="email">Email Address</label>
  <input type="email" id="email" name="email" required>
</div>

<div class="formItem">
  <div class="formItem-label">I’m interested in…</div>

  <div class="row">
  <div class="formItem-option col-1of2">
    <label for="interest-trying">trying out Tilt.</label>
    <input type="checkbox" id="interest-trying" name="interest" value="trying out Tilt">
    <div class="formItem-checkbox"></div>
  </div>

  <div class="formItem-option col-1of2">
    <label for="interest-feedback">requesting Tilt features.</label>
    <input type="checkbox" id="interest-feedback" name="interest" value="requesting Tilt features">
    <div class="formItem-checkbox"></div>
  </div>

  <div class="formItem-option col-1of2">
    <label for="interest-job">applying for a job to help build better local Kubernetes dev tools.</label>
    <input type="checkbox" id="interest-job" name="interest" value="applying for a job">
    <div class="formItem-checkbox"></div>
  </div>

  <div class="formItem-option col-1of2">
    <label for="interest-other">learning more.</label>
    <input type="checkbox" id="interest-other" name="interest" value="learning more">
    <div class="formItem-checkbox"></div>
  </div>
  </div>
</div>

<div class="formItem">
  <label for="message">Message</label>
  <textarea id="message" name="message" rows="5"></textarea>
</div>

<div class="u-marginBottom2_5">
  <button class="brandButton" type="submit">
    {% include common/brandButtonBg.html %}
    <div class="buttonLabel brandButton-text">
      Submit
    </div>
  </button>
</div>

<input type="hidden" name="_next" value="{{site.landingurl}}thanks"/>
</form>
