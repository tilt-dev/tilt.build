---
title: "Example: NodeJS"
layout: docs
---

You're a NodeJS developer. You want to set up Tilt with your project.

We hear you! We're working on a better guide for this.

For now, [this GitHub issue](https://github.com/windmilleng/tilt/issues/2703) has some sample code.

For now, check out:

- [abc123](https://github.com/windmilleng/abc123) a mini microservice app with a simple HTTP NodeJS server called `letters`.
- The [NodeJS microservice with Hot Reloading](nodejs_microservice_hotreloading.html) tutorial for using `live_update`.
- Servantes (below), our microservice app in multiple languages.


## Servantes

[Servantes](https://github.com/windmilleng/servantes) is a personalized homepage
app implemented with many microservices in multiple languages. You can run it
with the commands

```
git clone https://github.com/windmilleng/servantes
cd servantes; tilt up
```

Each widget is implemented by a different microservice backend.

Servantes uses many features of Tilt, and so can be a useful reference.

For an example of a Python server, look at the `hypothesizer` directory.
