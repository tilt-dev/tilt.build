---
title: "Example: C#"
layout: docs
lang: csharp
---

The best indicator of a healthy development workflow is a short feedback loop.

Kubernetes is a huge wrench in the works.

Let's fix this.

In this example, we're going to take you through a simple “hello world” web server written in C# that uses [ASP.NET Core](https://docs.microsoft.com/en-us/aspnet/core/?view=aspnetcore-3.1) as a Model View Controller framework.

We'll use Tilt to:

- Run the server on Kubernetes
- Measure the time from a code change to a new process
- Optimize that time for faster feedback

This particular example server doesn't do much, but it's useful to confirm that Tilt is working as expected in your environment.

All the code is in this repo:

[tilt-example-csharp](https://github.com/windmilleng/tilt-example-csharp){:.attached-above}

To skip straight to the fully optimized setup, go to this subdirectory:

[Recommended Setup](https://github.com/windmilleng/tilt-example-csharp/tree/master/3-live-update){:.attached-above}

# Step 0: The Simplest Deployment

Our server has only one page, and all it does is serve us an almost entirely static HTML page:

```csharp
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.Extensions.Logging;

namespace hello_tilt.Pages
{
    public class IndexModel : PageModel
    {
        private readonly ILogger<IndexModel> _logger;

        public IndexModel(ILogger<IndexModel> logger)
        {
            _logger = logger;
        }

        public void OnGet()
        {

        }
    }
}
```

To start this server on Kubernetes, we need three config files:

1. A [Dockerfile](https://github.com/windmilleng/tilt-example-csharp/blob/master/0-base/hello-tilt/Dockerfile) that builds the image
2. A [Kubernetes deployment](https://github.com/windmilleng/tilt-example-csharp/blob/master/0-base/kubernetes.yaml) that runs the image
3. And finally, a [Tiltfile](https://github.com/windmilleng/tilt-example-csharp/blob/master/0-base/Tiltfile) that ties them together:

```python
docker_build('hello-tilt', './hello-tilt')
k8s_yaml('kubernetes.yaml')
k8s_resource('hello-tilt', port_forwards='8080:80')
```

The first line tells Tilt to build an image with the name `hello-tilt` in the directory `./hello-tilt`.

The second line tells Tilt to load the Kubernetes Deployment YAML. The image name in the `docker_build` call must match the container `image` reference in the `hello-tilt` Deployment.

The last line configures port-forwarding so that your server is reachable at `localhost:8080`. The resource name in the `k8s_resource` call must match the Deployment's `metadata.name`.

Try it! Run:

```
git clone https://github.com/windmilleng/tilt-example-csharp
cd tilt-example-csharp/0-base
tilt up
```

Tilt will open a browser showing the web UI, a unified view that shows you app status and logs. Your terminal will also turn into a status box if you'd like to watch your server come up there.

When the server is ready, you will see the status icon turn green. The log pane will display:
```
info: Microsoft.Hosting.Lifetime[0]
      Now listening on: http://[::]:
```

{% include example_guide_image.html
    img="example-csharp-0-base.png"
    url="https://cloud.tilt.dev/snapshot/AeCx3ucLBiMYtPnPTuc="
    title="The server is up!"
    caption="The server is up! (Click the screenshot to see an interactive view.)"
%}

## Step 1: Let's Add Benchmark Trickery

Before we try to make this faster, let's measure it.

Using [`local_resource`](local_resource.html), you can direct Tilt to execute existing scripts or arbitrary shell commands on your own machine, and manage them from your sidebar like any other Tilt resource. We're going to use this functionality to benchmark our deploys.

First we add a `local_resource` to our [Tiltfile](https://github.com/windmilleng/tilt-example-csharp/blob/master/1-measure/Tiltfile) that records the start time in a C# file.

```python
local_resource(
    'deploy',
    './record-start-time.sh',
    deps=['./record-start-time.sh']
)
```

The `local_resource()` call creates a local resource named `deploy`. The second argument is the script that it runs.

We've also modified our server to read that start itme, calculate the time elapsed, then display this in the rendered HTML.

Let's click the button on the `deploy` resource and see what happens!

{% include example_guide_image.html
    img="example-csharp-image-2.png"
    url="https://cloud.tilt.dev/snapshot/AdKa5ucLVfFH0lRxn7I="
    title="Step 1 complete."
    caption="Step 1 complete. Click the screenshot to see an interactive snapshot"
%}

| Approach | Deploy Time[^1] |
|---|---|
| Naive | 10.4s |
{:.benchmark-report}

If you look closely, the elapsed time displayed in the Tilt sidebar is different than the benchmark our app logged. That's OK! In multi-service development there are many benchmarks we care about -- the time to build the image, the time to schedule the process, and the time until the server is ready to serve traffic.

Tilt offers you some default benchmarks _and_ the tools to capture your own.

Our benchmarks show this is slow. Can we do better?

## Step 2: Let's Optimize for the C# Toolchain

What's taking up so much time? The logs show that when we make a change to a file, we:

1) Copy the csproj file, run `dotnet restore` to install any dependencies
2) Copy the rest of the code and run a build from scratch with `dotnet publish`
3) Copy the build output to the ASP.NET runtime image

But the C# community has done a lot of work to make caching dependendencies and incremental compiles fast. How can we better use the tools how they're meant to be used?

With `local_resource`, we can compile the project locally, and copy the build output files to the container.

Here's our [new Tiltfile](https://github.com/windmilleng/tilt-example-csharp/blob/master/2-build-locally/Tiltfile) with the following new code:

```python
local_resource(
    'build',
    'dotnet publish -c Release -o out',
    deps=['hello-tilt'],
    ignore=['hello-tilt/obj'],
    resource_deps=['deploy'],
)
```

We've added a `local_resource()` that compiles the executable locally with `dotnet`.

We've adjusted the [Dockerfile](https://github.com/windmilleng/tilt-example-csharp/blob/master/2-build-locally/Dockerfile) so that it only includes the build output under `out`:

```dockerfile
FROM mcr.microsoft.com/dotnet/core/aspnet:3.1
COPY . /app/out
WORKDIR /app/out
ENTRYPOINT ["dotnet", "hello-tilt.dll"]
```

We also modified the context that we pass the `docker_build` call to only include the output directory:

```python
docker_build('hello-tilt', 'out', dockerfile='Dockerfile')
```

Let's see what this looks like!

{% include example_guide_image.html
    img="example-csharp-image-3.png"
    url="https://cloud.tilt.dev/snapshot/AdC35ucLJSe0a4XNTFc="
    title="Step 2 complete."
    caption="Step 2 complete. Click the screenshot to see an interactive snapshot"
%}

| Approach | Deploy Time |
|---|---|
| Naive | 10.4s |
| Local Compile | 8.2s |
{:.benchmark-report}

# Step 3: Let's Live Update It

When we make a change to a file, we currently have to build an image, deploy new Kubernetes configs, and wait for Kubernetes to schedule the pod.

With Tilt, we can skip all of these steps, and instead [live_update](live_update_tutorial.html) the pod in place.

Here's our [new Tiltfile](https://github.com/windmilleng/tilt-example-csharp/blob/master/3-live-update/Tiltfile) with the following new code:

```python
docker_build(
    'hello-tilt',
    'out',
    dockerfile='Dockerfile',
    live_update=[
        sync('out', '/app/out'),
    ],
    entrypoint='find . | entr -r dotnet hello-tilt.dll',
)
```

We've added a `live_update` parameter to `docker_build()` with a `sync` step. This copies the build output from the `out` directory into container.

We've also added a new parameter: `entrypoint='find . | entr -r dotnet hello-tilt.dll'`.

`entr` is a tool that automatically restarts a shell command whenever the watched
file changes. This command restarts our server every time the pod is updated.

Let's see what this new configuration looks like in action:

{% include example_guide_image.html
    img="example-csharp-image-4.png"
    url="https://cloud.tilt.dev/snapshot/AYSC5-cLzxRU0Wiuvrg="
    title="Step 3 complete."
    caption="Step 3 complete. Click the screenshot to see an interactive snapshot"
%}

Tilt was able to update the container in less than 5 seconds!

## Our Recommendation

### Final Score

| Approach | Deploy Time |
|---|---|
| Naive | 10.4s |
| Local Compile | 8.2s |
| With live_update | 4.8s |
{:.benchmark-report}

You can try the server here:

[Recommended Structure](https://github.com/windmilleng/tilt-example-csharp/tree/master/3-live-update){:.attached-above}

Congratulations on finishing this guide!

### Examples in other languages:

<ul>
  {% for page in site.data.examples %}
     {% if page.href contains "csharp" %}
       <!-- skip -->
     {% else %}
        <li><a href="/{{page.href | escape}}">{{page.title | escape}}</a></li>
     {% endif %}
  {% endfor %}
</ul>

[^1]: Tilt's first deployment of a service takes a few seconds longer than subsequent ones, due to some behind-the-scenes setup. Measurements in this guide focus on non-initial builds.
