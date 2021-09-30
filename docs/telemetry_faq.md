---
title: What does Tilt send?
description: "Tilt sends anonymized data about how you use it."
layout: docs
sidebar: gettingstarted
---

Tilt sends anonymized data about how you use it.

The first time you visit the web UI, Tilt nudges you to explicitly opt in or out
of analytics.

You can opt-in from the command-line with:

```bash
tilt analytics opt in
```

You can change your mind at any time by running:

```bash
tilt analytics opt out
```

and restarting Tilt.

---

### Why does Tilt want analytics?

We're a small company trying to make Tilt awesomer.

We can do this better if we understand which features people are using and which bugs people are running into.

---

### Where does the analytics data go?

Tilt sends telemetry data to our in-house analytics ingestion server at `events.windmill.build`.

This data may be stored in managed database services (like Google Cloud) or
managed analytics services (like Datadog) to help us analyze it.

We will not resell or give away this data to advertisers.

---

### What kinds of data does Tilt record if I opt-in?

We're interested in how people, in aggregate, use Tilt -- which Tiltfile
built-ins people use, what parts of the Web UI people interact with, etc.

We don't want to collect data about you or your project.

When possible, strings that may contain information about your project (repo names, service
names, directory names) are hashed to protect your privacy.

The hashing system isn't foolproof. It's possible that some of the data we collect
could include snippets of data about your project (e.g. that you have a service
named `deathray-backend` or an error message that includes the string it failed
to parse). You should probably not opt-in if you're working on a classified
project.

---

### Can you give some examples?

Here's an example of the data Tilt sends when you run `tilt up` with analytics enabled:

```
{
  "watch": "true",
  "version": "0.10.18-dev",
  "user": "a62525469776f5b299733bdc95718d47",
  "os": "linux",
  "name": "tilt.cmd.up",
  "mode": "auto",
  "machine": "8c581ff2fc00c6a47ecbd50abe47fb40",
  "git.origin": "3QLdKIWhsYTCsPI0vtsx6Q=="
}
```

Here's an example of the data Tilt sends when a Tiltfile loads:

```
{
  "version": "0.10.18-dev",
  "user": "a62525469776f5b299733bdc95718d47",
  "tiltfile.invoked.docker_build.arg.ref": "3",
  "tiltfile.invoked.docker_build.arg.live_update": "3",
  "tiltfile.invoked.docker_build.arg.ignore": "3",
  "tiltfile.invoked.docker_build.arg.dockerfile": "3",
  "tiltfile.invoked.docker_build.arg.context": "3",
  "tiltfile.invoked.docker_build": "3",
  "tiltfile.invoked.default_registry.arg.name": "1",
  "tiltfile.invoked.default_registry": "1",
  "os": "linux",
  "name": "tilt.tiltfile.loaded",
  "machine": "8c581ff2fc00c6a47ecbd50abe47fb40",
  "git.origin": "3QLdKIWhsYTCsPI0vtsx6Q=="
}
```

We've talked about adding a command that displays everything Tilt is sending in
a part of the web UI, for transparency. If you're interested in this, let us
know.

---

### What other ways can I control analytics?

You can disable analytics in the current environment by running:

```bash
export TILT_DISABLE_ANALYTICS="true"
```

Tilt also respects the DO_NOT_TRACK environment variable used 
for [other TUI/console apps](https://consoledonottrack.com/):

```bash
export DO_NOT_TRACK="1"
```

You can also enable analytics in the Tiltfile by adding:

```python
analytics_settings(enable=True)
```

The Tiltfile setting overrides user preferences. It's intended for
devtools teams opting-in all users on the team.

The environment setting overrides both the Tiltfile and user preferences.

