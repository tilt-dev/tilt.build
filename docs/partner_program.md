---
title: Tilt Partner Program
description: "We have a number of partnerships with teams that we meet with to get feedback and help prioritize things."
layout: docs
---

We have a number of partnerships with teams that we meet with
to get feedback and help prioritize things.

Our attention is limited. We can only run active partnerships with a select few
teams at a time. We want to make sure this is a good use of time for both of
us. Here's what we look for:

- A team of at least five engineers that expect to use something like Tilt for their day-to-day development
- A microservice app where Tilt would be able to add value
- A dev or dev-ops person who's willing to evaluate Tilt and get it setup

When we kick off a partnership, we ask that you:

- Check in with us bi-weekly over video chat to help with the first month or two of onboarding
- Join a shared Slack channel for one-off support
- Enable analytics in Tiltfile

```
analytics_settings(enable=True)
```

- `cd` into the repo where you're using Tilt. Run `tilt doctor`. Send us the analytics settings at the bottom, e.g.:

```
Analytics Settings
- Mode: opt-in
- Machine: 8c581ff2fc00c6a47ecbd50abe47fb40
- Repo: 3QLdKIWhsYTCsPI0vtsx6Q==
```

We use the aggregate data so that both of us (our team and your dev-ops team)
has an accurate picture of how your team is using Tilt and what parts of it are
slow. For more info, see ["What does Tilt send?"](telemetry_faq.html).

If this sounds interesting to you, please email our CEO
[Dan](mailto:dan@tilt.dev?subject=Tilt partner program) to get set up.
