---
title: Who is Tilt for?
layout: docs
---

Tilt is a cloud-native development engine for teams that deploy to Kubernetes.

It's free and open-source.

That's a lot to unpack! Let's break it down.

---

### What is a cloud-native development environment?

For decades, developer environments focused on files. You change a source
file. You compile a binary. Your binary reads input files and writes output files.

Your app isn't one binary anymore. It's a managed database, and a frontend server,
and a web app -- all talking to each other over HTTP.

Development today needs new tools.

[A cloud-native development environment](https://blog.tilt.dev/2019/09/05/put-down-particle-accelerator.html)
is a new kind of tool that understands how your files and your servers fit
together, and can help you better understand your system.

---

### What kinds of teams should use Tilt?

Currently, we're focused on helping teams that develop multi-service apps, because that's where
the pain is most acute.

- Do you always have 5 terminal windows open to stream the logs of all your
  servers, because
  [you're not sure where to look](https://blog.tilt.dev/2019/04/09/designing-a-better-interface-for-microservices-development.html)?
- Are devs [always asking questions in team chat](https://blog.tilt.dev/2019/10/01/solving-the-laggy-human-shell-problem.html) about how to distinguish meaningful error logs from noise?
- Do you have [a complicated Bash script that sets up all your dev servers](https://blog.tilt.dev/2018/12/05/tilt-is-the-start-sh-script-of-my-dreams.html), but is always breaking?

Once you've set up Tilt, any contributor should be able to run `tilt up` to get
[a complete dev environment](https://docs.tilt.dev/welcome_to_tilt.html).

---

### Why does Tilt focus on Kubernetes?

Kubernetes defines well-thought-out building blocks for running servers together --
such as containers, pods, and services. They're quickly becoming
standards for our industry.

We should be using these building blocks for all our development environments,
not just when we're running on big managed clouds like AWS, AKS, or GKE.

Tilt does support other systems for building and running servers. For example,
you can run your containers with [docker-compose](docker_compose.html), or
building with [local shell commands](api.html#api.local_resource).  But we
expect that the industry will converge on Kubernetes. Tilt's support for other
systems is mostly about
[making it easier for teams to migrate](https://blog.tilt.dev/2019/09/16/tips-on-moving-your-dev-env-from-docker-compose-to-kubernetes.html).

---

### What's Next?

Tilt is just the first step towards blurring the line between your laptop and the cloud.

The next step -- [Tilt Cloud](snapshots.html) -- is a platform for
making all kinds of data from your tilt instance available to your team. And
making your team’s data available to you.

---

## Governance

### Who Develops Tilt?

We're a start-up! "The Tilt Team" or "Tilt.dev" is fine. Nice to e-meet you.

Our mission is to build a platform for cloud-native development.

{% assign total = site.data.people | where: "active","true" | size %}
We’re a small team of {{total}} people. We’re based at
[Work-Bench](https://www.work-bench.com/) in New York City, 
but also have teammates in Berlin, Germany and Richmond, VA.

We used to call ourselves "Windmill Engineering." 
You may hear us use that name sometimes when we slip up.

---

### If you're a startup, does that mean you will collapse?

We have funding from top-tier VCs we love, and have plans. Talk to us if you're nervous.

Tilt (the local dev environment) will always be free and open-source. If we
can't turn this into a business, the community should be able to continue using
it.

---

### Where can I chat with the team?

For real-time support, find us on the Kubernetes slack. Get an invite at
[slack.k8s.io](http://slack.k8s.io) and find us in
[the **#tilt** channel](https://kubernetes.slack.com/messages/CESBL84MV/).

We have a weekly rotation so that there's always a Tilt developer active in the
channel during NYC business hours (10am-5pm Monday through Friday).

---

### How do I file an issue?

You can file an issue in [our GitHub repo](https://github.com/windmilleng/tilt/issues/new).

On normal work days (Monday through Friday), a developer should acknowledge your
issue to confirm we saw it. If you don't hear anything after a day or two, it's
OK to ping the thread or ask in Slack. We probably just missed it.

For help with private issues (like security vulnerabilities or just concerning non-public code),
please email [help@tilt.dev](mailto:help@tilt.dev).

---

### How do new features get added to the roadmap?

Filing a GitHub issue helps a lot, even if it's not always obvious from the outside.

We also have a number of partnerships with teams that we meet with
semi-regularly to get feedback and help prioritize things that are affecting
many people. If you're interested in [partnering](partner_program.html) with us,
please email our CEO [Dan](mailto:dan@tilt.dev?subject=Tilt partner program).

---

### Why did you call it Tilt?

It's a [Don Quixote reference](https://en.wikipedia.org/wiki/Don_Quixote#Tilting_at_windmills).

Our demo app is called [Servantes](https://en.wikipedia.org/wiki/Miguel_de_Cervantes).

We have plenty more puns if you ask.

