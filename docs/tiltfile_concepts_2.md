---
title: Tiltfile Concepts 2
layout: docs
---

A Tiltfile is a Starlark program that Tilt runs to generate Resources (Tilt's configuration). This doc describes Resources, how Tilt runs a Tiltfile, and how to debug a Tiltfile.

## Resources
Tilt's engine and UI are based on "Resources". A Resource contains the configuration to build Images and Objects to deploy (either to Kubernetes or Docker Compose).