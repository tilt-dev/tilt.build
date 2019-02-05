---
layout: page
title: Contact Us
permalink: /contact
---

<div class="col-3of4 u-marginBottom1_5">
If you'd like to learn more about what we're doing, you can either
email <a href="mailto:dan@windmill.engineering">Dan</a> or <a href="mailto:nick@windmill.engineering">Nick</a>,
or fill out the form below.
</div>

<form>
<div class="formItem">
  <label for="name">Name</label>
  <input id="name" required>
</div>

<div class="formItem">
  <label for="email">Email Address</label>
  <input type="email" id="email" required>
</div>

<div class="formItem">
  <div class="formItem-label">I’m interested in…</div>

  <div class="row">
  <div class="formItem-option col-1of2">
    <label for="interest-trying">trying out Tilt.</label>
    <input type="checkbox" id="interest-trying" name="interest" value="interest-trying">
  </div>

  <div class="formItem-option col-1of2">
    <label for="interest-feedback">requesting Tilt features.</label>
    <input type="checkbox" id="interest-feedback" name="interest" value="interest-feedback">
  </div>

  <div class="formItem-option col-1of2">
    <label for="interest-job">applying for a job to help build better live development tools.</label>
    <input type="checkbox" id="interest-job" name="interest" value="interest-job">
  </div>

  <div class="formItem-option col-1of2">
    <label for="interest-other">learning more.</label>
    <input type="checkbox" id="interest-other" name="interest" value="interest-other">
  </div>
  </div>
</div>

<div class="formItem">
  <label for="message">Message</label>
  <textarea id="message" rows="5"></textarea>
</div>

<div class="svgButton u-marginBottom2_5">
  <button type="submit" class="imageButton">
    {% svg assets/svg/button.svg class="svgButton" %}
    <div class="buttonLabel svgButton-text">
      Submit
    </div>
  </button>
</div>

</form>
