---
title: Tilt User Guide
layout: docs
---

Kubernetes for Prod, Tilt for Dev

Modern apps are made of too many services. They're everywhere and in constant
communication.

[Tilt]({{site.landingurl}}/) powers multi-service development and makes sure they behave!
Run `tilt up` to work in a complete dev environment configured for your team.

Tilt automates all the steps from a code change to a new process: watching
files, building container images, and bringing your environment
up-to-date. Think `docker build && kubectl apply` or `docker-compose up`.

## Watch: Tilt in Two Minutes

<div class="Docs-video">
  <iframe width="560" height="315" src="https://www.youtube.com/embed/FSMc3kQgd5Y?controls=0" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>

## Install Tilt

Installing the `tilt` binary is a one-step command.

### macOS/Linux

```bash
curl -fsSL https://raw.githubusercontent.com/tilt-dev/tilt/master/scripts/install.sh | bash
```

### Windows

```powershell
iex ((new-object net.webclient).DownloadString('https://raw.githubusercontent.com/tilt-dev/tilt/master/scripts/install.ps1'))
```

For specific package managers (Homebrew, Scoop, Conda, asdf), see the [Installation Guide](install.html).

## Run Tilt

**New to Tilt?** Our tutorial will [get you started](tutorial.html).

**Configuring a Service?** We have best practice guides for:

<ul>
  {% for page in site.data.examples %}
    <li><a href="/{{page.href | escape}}">{{page.title | escape}}</a></li>
  {% endfor %}
</ul>

**Optimizing a Tiltfile?** Search for the function you need in our 
[complete API reference](api.html).

## Don’t Tilt Alone, Take This

<img src="/assets/svg/TiltCloud-illustration.svg" alt="Tilt Cloud" class="no-shadow u-marginBottomUnit">

Are you seeing an error from a server that you don't even work on?

With Tilt Cloud, create web-based interactive reproductions of your local cluster’s state.

Save and share [a snapshot](snapshots.html) with your team
so that they can dig into the problem later. A snapshot lets you explore the
status of running services, errors, logs, and more.

## Community

**Questions and feedback:** Join [the Kubernetes slack](http://slack.k8s.io) and
 find us in the [#tilt](https://kubernetes.slack.com/messages/CESBL84MV/)
 channel. Or [file an issue](https://github.com/tilt-dev/tilt/issues).

**Contribute:** Tilt is open source, developed on [GitHub](https://github.com/tilt-dev/tilt). Check out our [contribution](https://github.com/tilt-dev/tilt/blob/master/CONTRIBUTING.md) guidelines. 

**Follow along:** [@tilt_dev](https://twitter.com/tilt_dev) on Twitter. Updates
and announcements on the [Tilt blog](https://blog.tilt.dev).

**Help us make Tilt even better:** Tilt sends anonymized usage data, so we can
improve Tilt on every platform. Details in ["What does Tilt
send?"](telemetry_faq.html).

We expect everyone in our community (users, contributors, and employees alike) to abide by our [**Code of Conduct**](code_of_conduct.html).
