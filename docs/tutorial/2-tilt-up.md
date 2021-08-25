---
title: Tilt Up, Up, And Away
subtitle: Tilt Tutorial
layout: docs
---
## Tilt Avatars
[Tilt Avatars][repo-tilt-avatars] is a small sample project created for this guide.

It consists of a Python web API backend to generate avatars and a Javascript SPA (single page app) frontend.
If you are not a Python or Javascript guru, don't panic!

![Randomized Tilt avatar generation](/assets/img/tutorial/tilt-avatars.gif)

The focus of this project is on introducing the `Tiltfile` and other Tilt concepts: the services are demonstrative to support the guide, but you do not need to understand the code within them to be successful.

> **We know that no two projects are alike!**
>
> While, this project uses `Dockerfile`s with Docker as the build engine and `kubectl`-friendly YAML files,
> these only cover a small subset of Tilt functionality.
> 
> Even if you're using other technologies (e.g. Helm, CRDs, `podman`), we recommend starting here to learn the Tilt fundamentals.
>
> Once you're comfortable with how Tilt works, we've got comprehensive guides on `Tiltfile` authoring that cover these topics and much more!

## Run `tilt up` for the First Time
Navigate to the [`tilt-avatars` directory][tutorial-prerequisites-sample-project] in a terminal and launch Tilt:
```bash
tilt up --port=3366
```

> The `--port` argument (or `TILT_PORT` environment variable) is optional.
>
> The default port is `10350`.
> You can run multiple instances of Tilt by specifying a different port for each.

You should see output similar to the following in your terminal:
![Running tilt up in a Terminal window shows "Tilt started on http://localhost:3366/" message](/assets/img/tutorial/tilt-up-cli.gif)

Press `Spacebar` while your terminal is active and Tilt will launch your default browser.
Alternatively, navigate to [http://localhost:3366/]() yourself.

In the next section, we'll explain the Tilt UI: but first, let's dissect what's happening in the background.
<!-- TODO(milas): this would be a great place for a cheeky graphic about how we're stalling while the builds happen -->

## `Tiltfile`
When you run `tilt up`, Tilt looks for a special file named `Tiltfile` in the current directory which defines your dev-environment-as-code.

A `Tiltfile` is written in [Starlark][starlark], a simplified dialect of Python.

> 🐍 Not a Python expert? No worries! Our guides have lots of examples, so you can copy & paste your way to success!

Because your `Tiltfile` is a program, you can configure it with familiar constructs like loops, functions, and arrays.
This makes the `Tiltfile` more extensible than a configuration file format like JSON or YAML that requires hard-coding all possible options up-front.

Built-in functions like [`k8s_yaml`][api-k8s_yaml] and [`docker_build`][api-docker_build] register information with the Tilt engine.
At the end of the execution, Tilt uses the resulting configuration to assemble resources to build and deploy.

Additionally, based on the assembled resources, Tilt watches your source code files to trigger a rebuild on the associated service(s).
Later, in the [Smart Rebuilds with Live Update][tutorial-live-update] section, we'll explore how Tilt makes it possible to optimize this process even more to skip container re-builds and Pod re-deployments entirely!  

For now, that's all you need to know!
<!-- TODO(milas): snarky graphic about how that ^^^ was a galaxy brain info dump? -->

If you're curious, go ahead and open the [`tilt-avatars` Tiltfile][repo-tilt-avatars-tiltfile] and read through it.
We won't tell anyone you peeked.

## Resources
A "resource" is a bundle of work managed by Tilt such as a Docker image to build + Kubernetes YAML to apply.

> 😶‍🌫️ **Resources don't have to be containers!**
>
> Tilt can also [manage locally-executed commands][local-resource] to provide a unified experience no matter how your code runs.  

Resource bundling is automatic in most cases: Tilt finds the relationship between bits of work (e.g. `docker_build` + `kubectl apply`).
When that's not sufficient, `Tiltfile` functions like [`k8s_resource`][api-k8s_resource] let you configure resources on top of Tilt's automatic assembly.

Because Tilt assembles multiple bits of work into a single resource, it's much easier to determine status and find errors across build, deploy, and runtime!

### Update Status
Whenever you run `tilt up` or change a source file, Tilt determines which resources need to be "updated".

> 🔥️ When you `tilt up`, if your services are already running and haven't changed, Tilt won't unnecessarily re-deploy them!

Some examples of actions that can occur during an update:
 * Compile code locally on your machine (e.g. `make`)
 * Build a container image (e.g. `docker build`)
 * Deploy a modified K8s object or Helm chart (e.g. `kubectl apply -f` or `helm install`)

Tilt know which files correspond to a given resource and update action.
It won't re-build a container just because you changed a Pod label or re-compile your backend after modifying some JSX. 

### Runtime Status
Unfortunately, just because it builds does not mean it works.

In Tilt, the runtime status lets you know what's happening with your code _after_ it's been deployed.

<!-- TODO(milas): this section is chaotic, needs a CrashLoopBackOff joke graphic, and probably some more actual detail -->

More importantly, Tilt lets you know _why_.
There's a lot of ways things can go wrong, and Tilt will save you from playing "20 Questions with `kubectl`".

## The Control Loop
Many traditional build systems like `make` are oriented around tasks that are invoked on-demand by the user.
Even many service-oriented development tools like `docker-compose up` don't react to changes once started.
Some tools such as Webpack (`npm run start`) often include hot module reload, but that often comes with its own limitations: for example, changes to `webpack.config.js` require manual user intervention to restart the tool.

Tilt is based around the idea of a [control loop][control-loop] to give you real-time, circular feedback: something watches, something reacts, and equilibrium is maintained.

![Diagram of Tilt's control loop architecture](/assets/img/controlloop/06.jpg)

Some examples of how this manifests more concretely:
 * Source code file changes -> sync to running container
 * Dependency changes (e.g. `package.json`) -> sync to running container and then run code in the container (e.g. `npm install`)
 * Build spec changes (e.g. `Dockerfile`) -> re-build container image + re-deploy
 * Deployment spec changes (e.g. `app.yaml`) -> reconcile deployment state (e.g. `kubectl apply -f ...`)
 * `Tiltfile` changes -> re-evaluate and create new resources, modify existing, and delete obsolete as needed

In short, once you've run `tilt up`, you can focus on your code and let Tilt continuously react to your changes without worrying if they're the "right" type of changes.

This has other benefits: for example, when you run `tilt up`, Tilt won't re-deploy any services that are already running and up-to-date!

If you'd like a more in-depth look at Tilt's control loop, check out [Tilt's Control Loop Demystified][control-loop].

[api-docker_build]: /api.html#api.docker_build
[api-k8s_resource]: /api.html#api.k8s_resource
[api-k8s_yaml]: /api.html#api.k8s_yaml
[control-loop]: /controlloop.html
[local-resource]: /local_resource.html
[repo-tilt-avatars]: https://github.com/tilt-dev/tilt-avatars
[repo-tilt-avatars-tiltfile]: https://github.com/tilt-dev/tilt-avatars/blob/master/Tiltfile
[starlark]: https://docs.bazel.build/versions/main/skylark/language.html
[tutorial-live-update]: ./4-live-update.html
[tutorial-prerequisites-sample-project]: ./1-prerequisites.html#clone-the-sample-project
