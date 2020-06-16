---
slug: "the-right-display-for-now"
date: 2020-06-19
author: nick
layout: blog
title: "The Right Display for Now"
image: "/assets/images/the-right-display-for-now/forest-park.jpg"
tags:
  - tilt
  - ui
---

At Tilt, [Han and I](https://tilt.dev/about) talk a lot about the different
modes developers are in and problems they're solving when using
software. Sometimes it's easier to talk about these modes when we relate them to
signs in the real world.

For example:

- Discovery - what is it possible to do here? (see: the Forest Park sign above)
- Awareness - what issues should I be aware of? (see: the estimated arrival time signs at train stations)
- Recommendations - what should I do next? (see: exit signs, recommended routes)

Tilt has always initialized your terminal with a terminal GUI. 

We previously thought of the split between terminal GUI and browser GUI as two
complementary GUIs for different modes: [awareness vs
investigation](https://blog.tilt.dev/2019/04/09/designing-a-better-interface-for-microservices-development.html). But
in the year since we launched the browser GUI, we've heard from users who
see these as two competing interfaces. At a glance, they can seem equivalent,
like it's a matter of preference which one you'd like to use.

Some devs do prefer the terminal GUI! But by starting there, we did
a poor job communicating that there might be better modes for you.

In v0.15.0, we've made your first `tilt up` a better map of
how to use it.

## What Tilt Looks Like Now

When you start Tilt in a terminal, here's what you'll see:

```
Tilt started on http://localhost:10350/
v0.15.0, built 2020-06-18

(space) to open the browser
(s) to stream logs (--hud=false)
(h) to open terminal HUD (--hud=true)
(ctrl-c) to exit
```

We expect that most users will want to hit (space) to open the browser,
where they can browse logs, check deploy status, and trigger rebuilds.

If you liked the terminal GUI and want to keep using it, you can hit the (h) key
or start Tilt with `tilt up --hud=true`.

If you just want to see logs, or don't have an interactive terminal, you can hit
(s) or start Tilt with `tilt up --hud=false`.

## What's Next?

We currently have no plans to get rid of the terminal GUI.

We may keep all 3 modes! Some people prefer a terminal, others prefer
a browser UI, and a few even run everything in an Emacs buffer 🤓.

We're keeping an eye on what modes people use, and talking to our partner teams
about which they prefer.

We want Tilt to be the dashboard you interact with when you're doing 
interactive, multi-service development. 

But if you want other types of visibility into your dev cluster, we recommend:

- [K9s](https://k9scli.io/) - a terminal-based Kubernetes dashboard
- [Octant](https://octant.dev/) - a web-based Kubernetes dashboard

They are both great tools, and have progressed a lot since we started working on
Tilt 😀.
