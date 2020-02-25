---
title: "Example: Go"
layout: docs
---

You're a Go developer. You want to set up Tilt with your project.

We here you! We're working on a better guide for this.

For now, check out:

- [abc123](https://github.com/windmilleng/abc123) a mini microservice app with a Go server called `fe`.
- The [Live Update Tutorial](live_update_tutorial.html), which optimizes a Go server.
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

For an example of a Go server, look at the `doggos` directory.
