---
title: "Example: Plain Old Static HTML"
layout: docs
---

Maybe you want to try Tilt but don't have a suitable project on hand.

That's OK! Let's look at a project that just serves static HTML.

These projects can also be useful to confirm Tilt is working as expected in your environment.

## oneup

Oneup is a simple app that uses busybox to serve HTML files.

First, check out the Tilt repo.

```
git clone https://github.com/windmilleng/tilt
cd tilt/integration/oneup
```

We'll be looking at the [oneup](https://github.com/windmilleng/tilt/tree/master/integration/oneup) project
in `integration/oneup`.

In the oneup directory, run

```
tilt up
```

Your terminal will turn into a status box that lets you watch your server come up. When it's ready,
you will see the status icon turn green. The logs in the botton pane will display
"Serving oneup on container port 8000."

<div class="block u-margin1_5">
 <img src="assets/img/oneup.png">
</div>

Type `b` to open `oneup` in a browser window.
Your browser will open `http://localhost:8100`.
You should see the text `🍄 One-Up! 🍄`.

Congratulations! You've run your first server with `tilt`.

Type `ctrl-C` to quit the status box. When you're finished, run

```
tilt down
```

to turn off the server.
