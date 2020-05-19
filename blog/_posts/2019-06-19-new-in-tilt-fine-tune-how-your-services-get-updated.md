---
slug: new-in-tilt-fine-tune-how-your-services-get-updated
date: 2019-06-19T18:28:23.213Z
author: han
canonical_url: "https://medium.com/windmill-engineering/new-in-tilt-fine-tune-how-your-services-get-updated-9a1d3e8480c1"
layout: blog
title: "New in Tilt&#58; Fine-Tune How Your Services Get Updated"
subtitle: "“Wait, so Tilt updates every single time I save my code?”"
image_needs_slug: true
images:
  - featuredImage.gif
  - 1_DQ_aNDR0le3dcUsb9Eknaw.gif
tags:
  - microservices
  - kubernetes
  - developer
  - devtools
keywords:
  - microservices
  - kubernetes
  - developer
  - devtools
---

You might like the premise that Tilt keeps your development cluster updated as you work. But maybe the whole update-on-each-save thing isn’t always great for your particular workflow. What if some change you’re not quite ready to deploy puts your development database into an inconsistent state? What if you’d rather not see errors and warnings on some service that you know is busted because it’s still work in progress? What if super-frequent updates for certain services just seem kind of…expensive?

In the [latest version](https://github.com/windmilleng/tilt/releases) of Tilt, you can control just how updates get triggered for each of your services. You can set any resource’s Trigger Mode to Manual by editing the Tiltfile. As an example, let’s rein in updates on our handy Snack Generator:

```
k8s_resource('snack', trigger_mode=TRIGGER_MODE_MANUAL)
```


Then, you’ll see that “snack” looks different from its neighbors on the sidebar:

![The Update icon becomes active once you make edits in the “snack” service](/assets/images/new-in-tilt-fine-tune-how-your-services-get-updated/featuredImage.gif)*The Update icon becomes active once you make edits in the “snack” service*

Then when you’re ready, hit the Update button and Tilt will do its thing. (Oops, looks like we have a syntax error here!):

![After you’ve edited a service, hit the Update icon to trigger an update](/assets/images/new-in-tilt-fine-tune-how-your-services-get-updated/1_DQ_aNDR0le3dcUsb9Eknaw.gif)*After you’ve edited a service, hit the Update icon to trigger an update*

Check it out for yourself in [Tilt v0.9.0](https://github.com/windmilleng/tilt/releases), and see more details in [the docs](https://docs.tilt.dev/manual_update_control.html). Does this make Tilt better suited for your workflow? And if you’re wondering where we’re headed next, the [Manual Update Control spec](https://github.com/windmilleng/tilt.specs/blob/master/manual_update_control.md) describes some of the paths we considered but haven’t tried yet.

We’d love to hear your thoughts, so please [get in touch](https://tilt.dev/contact)!
