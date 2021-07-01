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

**Questions:** Join [the Kubernetes slack](http://slack.k8s.io) and
 find us in the [#tilt](https://kubernetes.slack.com/messages/CESBL84MV/)
 channel. Or [file an issue](https://github.com/tilt-dev/tilt/issues). For code snippets of Tiltfile functionality shared by the Tilt community, check out [Tilt Extensions](https://github.com/tilt-dev/tilt-extensions). 
 
**Roadmap:** Help us figure out what to prioritize. Sign up for [Tilt office
hours](https://calendly.com/han-yu/user-research). We'll discuss your experience
with Tilt and ask for reactions on visuals or prototypes we're working on.

**Contribute:** Check out our [guidelines](https://github.com/tilt-dev/tilt/blob/master/CONTRIBUTING.md) to contribute to Tilt's source code. To extend the capabilities of Tilt via new Tiltfile functionality, read more about [Extensions](extensions.html).

**Follow along:** [@tilt_dev](https://twitter.com/tilt_dev) on Twitter. For updates
and announcements, follow [the blog](https://blog.tilt.dev) or subscribe to 
[the newsletter](https://tilt.dev/subscribe).

**Help us make Tilt even better:** Tilt sends anonymized usage data, so we can
improve Tilt on every platform. Details in ["What does Tilt
send?"](http://docs.tilt.dev/telemetry_faq.html). If you find a security issue
in Tilt, see our [security policy](https://github.com/tilt-dev/tilt/blob/master/SECURITY.md).

We expect everyone in our community (users, contributors, followers, and employees alike) to abide by our [**Code of Conduct**](code_of_conduct.html).

