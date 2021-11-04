---
title: Launching & Managing Resources
subtitle: Tilt Tutorial
layout: docs
sidebar: gettingstarted
---
## Tilt Avatars
We made [Tilt Avatars][repo-tilt-avatars] so you can try Tilt without first setting it up for your own project.

Tilt Avatars consists of a Python web API backend to generate avatars, and a JavaScript SPA (single page app) frontend.
**It doesn't matter if you're not a Python or JavaScript guru** — you won't need to deeply understand the project code to learn about the `Tiltfile` and other Tilt concepts.

![Randomized Tilt avatar generation](/assets/docimg/tutorial/tilt-avatars.gif)

> **We know that no two projects are alike!**
>
> This project uses `Dockerfile`s with Docker as the build engine and `kubectl`-friendly YAML files.
> But that's only a small subset of Tilt functionality.
>
> Even if you're using other technologies (e.g. Helm, CRDs, `podman`), we recommend starting here to learn the Tilt fundamentals.
>
> Once you're comfortable with how Tilt works, we've got comprehensive guides on `Tiltfile` authoring that cover these topics and much more!

## Run `tilt up` for the First Time
Tilt brings consistency to your development not only due to ensuring a reproducible dev-environment-as-code, but launching any Tilt project is the same with the `tilt up` command, so you always have a familiar starting point.
`tilt up` starts the Tilt control loop, which we'll explore in more detail in a moment.

For this tutorial, however, we're going to use a special `tilt demo` command, which will perform a few steps:
 1. Create a temporary, local Kubernetes development cluster in Docker
 2. Clone the [Tilt Avatars][repo-tilt-avatars] sample project
 3. Launch a `tilt up` session for the sample project using the temporary Kubernetes cluster
 4. Clean everything up on exit 🧹

Run the following command in your terminal to get started:
```bash
tilt demo
```

You should see output similar to the following in your terminal:
![Running tilt up in a Terminal window shows "Tilt started on http://localhost:3366/" message](/assets/docimg/tutorial/tilt-up-cli.gif)

First, open the sample project directory in your preferred editor so that you can make changes in the following steps.

Once you've got the sample project open, return focus to the terminal window and press `(Spacebar)`, and the Tilt UI will be opened in your default browser.

In the next section, we'll explain the Tilt UI. But first, let's dissect what's happening in the background.
<!-- TODO(milas): this would be a great place for a cheeky graphic about how we're stalling while the builds happen -->

> **Already Have a Local Kubernetes Cluster? (Advanced)**
>
> You can clone the sample project and run `tilt up` directly:
> ```bash
> git clone https://github.com/tilt-dev/tilt-avatars.git
> cd tilt-avatars/
> tilt up
> ```
>
> Once finished, run `tilt down` from the `tilt-avatars` directory to clean up.

## `Tiltfile`
When you run `tilt up`, Tilt looks for a special file named `Tiltfile` in the current directory, which defines your dev-environment-as-code.

A `Tiltfile` is written in [Starlark][starlark], a simplified dialect of Python.

> 🐍 Not a Python expert? No worries. Our guides have lots of examples, so you can copy & paste your way to success!

Because your `Tiltfile` is a program, you can configure it with familiar constructs like loops, functions, and arrays.
This makes the `Tiltfile` more extensible than a configuration file format like JSON or YAML, which requires hard-coding all possible options upfront.

When Tilt executes the `Tiltfile`:
 1. Built-in functions like [`k8s_yaml`][api-k8s_yaml] and [`docker_build`][api-docker_build] register information with the Tilt engine
 2. Tilt uses the resulting configuration to assemble resources to build and deploy
 3. Tilt watches **relevant** source code files so it can trigger an update of the associated resource(s) 

Within Tilt, the `Tiltfile` is itself a resource, so **you can even modify your `Tiltfile` and see the changes without restarting Tilt**!

![Sample Tiltfile code](/assets/docimg/tutorial/tiltfile.png){:class="no-shadow"}

Later on, we'll explore how Tilt makes it possible to optimize this process even more.
You can skip container re-builds and Pod re-deployments entirely via [Smart Rebuilds with Live Update][tutorial-live-update].

(If you're curious, go ahead and open the [`tilt-avatars` Tiltfile][repo-tilt-avatars-tiltfile] and read through it.
We won't tell anyone you peeked.)

For now, that's all you need to know!
<!-- TODO(milas): snarky graphic about how that ^^^ was a galaxy brain info dump? -->

## On Resources
A "resource" is a bundle of work managed by Tilt. For example: a Docker image to build + a Kubernetes YAML to apply.

> 😶‍🌫️ **Resources don't have to be containers!**
>
> Tilt can also [manage locally-executed commands][local-resource] to provide a unified experience no matter how your code runs.  

Resource bundling is **automatic** in most cases: Tilt finds the relationship between bits of work (e.g. `docker build` + `kubectl apply`).
When that's not sufficient, `Tiltfile` functions like [`k8s_resource`][api-k8s_resource] let you configure resources on top of what Tilt does automatically.

Because Tilt assembles multiple bits of work into a single resource, it's much easier to determine status and find errors across update (build/deploy) and runtime.

### Update Status
Whenever you run `tilt up` or change a source file, Tilt determines which resources need to be changed to bring them up-to-date.

To execute these updates, Tilt might:
 * Compile code locally on your machine (e.g. `make`)
 * Build a container image (e.g. `docker build`)
 * Deploy a modified K8s object or Helm chart (e.g. `kubectl apply -f` or `helm install`)

![Resource pane showing an update error](/assets/docimg/tutorial/tilt-ui-update-status.png)

Tilt knows which files correspond to a given resource and update action.
It won't re-build a container just because you changed a Pod label, or re-compile your backend when you've only edited some JSX.

> 🔥️ When you `tilt up`, if your services are already running and haven't changed, Tilt won't unnecessarily re-deploy them!

### Runtime Status
Unfortunately, just because it builds does not mean it works.

In Tilt, the runtime status lets you know what's happening with your code _after_ it's been deployed.

![Resource pane showing a runtime error](/assets/docimg/tutorial/tilt-ui-runtime-status.png)

More importantly, Tilt lets you know _why_.
There's a lot of ways things can go wrong, and Tilt will save you from playing "20 Questions with `kubectl`."

## The Control Loop
Tilt is based around the idea of a [control loop][control-loop].
This gives you real-time, circular feedback: something watches, something reacts, and equilibrium is maintained.

This is intentionally more "hands-free" than other dev tools.
Traditional build systems like `make` are oriented around tasks that are invoked on-demand by the user.
Even many service-oriented development tools like `docker-compose up` don't _react_ to changes once started.
Newer tools, such as Webpack, often include hot module reload, but have limitations.
(For example, changes to `webpack.config.js` require a manual restart.)

![Diagram of Tilt's control loop architecture](/assets/img/controlloop/06.jpg)

Some examples of what Tilt handles for you:
 * Source code file changes → sync to running container
 * Dependency changes (e.g. `package.json`) → sync to running container and then run code in the container (e.g. `npm install`)
 * Build spec changes (e.g. `Dockerfile`) → re-build container image + re-deploy
 * Deployment spec changes (e.g. `app.yaml`) → reconcile deployment state (e.g. `kubectl apply -f ...`)
 * `Tiltfile` changes → re-evaluate and create new resources, modify existing, and delete obsolete as needed

**So, once you've run `tilt up`, you can focus on your code and let Tilt continuously react to your changes without worrying if they're the "right" type of changes.**

This has other benefits: for example, when you run `tilt up`, Tilt won't re-deploy any services that are already running and up-to-date!

If you'd like a more in-depth look at Tilt's control loop, check out [Tilt's Control Loop Demystified][control-loop].


[api-docker_build]: /api.html#api.docker_build
[api-k8s_resource]: /api.html#api.k8s_resource
[api-k8s_yaml]: /api.html#api.k8s_yaml
[control-loop]: /controlloop.html
[local-resource]: /local_resource.html
[repo-tilt-avatars]: https://github.com/tilt-dev/tilt-avatars
[repo-tilt-avatars-tiltfile]: https://github.com/tilt-dev/tilt-avatars/blob/main/Tiltfile
[starlark]: https://docs.bazel.build/versions/main/skylark/language.html
[tutorial-live-update]: ./5-live-update.html
[tutorial-prerequisites-sample-project]: ./1-prerequisites.html#clone-the-sample-project
