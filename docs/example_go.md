---
title: "Example: Go"
layout: docs
---

The best indicator of a healthy development workflow is a short feedback loop.

Kubernetes is a huge wrench in the works.

Let's fix this.

In this example, we're going to take you through a simple server that uses Go
templates to serve HTML.

We'll use Tilt to:

- Run the server on Kubernetes
- Measure the time from a code change to a new process
- Optimize that time for faster feedback

All the code is in this repo:

[tilt-example-go](https://github.com/windmilleng/tilt-example-go){:.attached-above}

To skip straight to the fully optimized setup, go to this subdirectory:

[Recommended Tiltfile](https://github.com/windmilleng/tilt-example-go/blob/master/3-recommended/Tiltfile){:.attached-above}

## Step 0: The Simplest Deployment

Our server uses [gorilla/mux](http://www.gorillatoolkit.org/pkg/mux) for routing requests:

```go
func main() {
	http.Handle("/", NewExampleRouter())

	log.Println("Serving on port 8000")
	err := http.ListenAndServe(":8000", nil)
	if err != nil {
		log.Fatalf("Server exited with: %v", err)
	}
}
```

To start this server on Kubernetes, we need three config files:

1) A [Dockerfile](https://github.com/windmilleng/tilt-example-go/blob/master/0-base/deployments/Dockerfile) that builds the image

2) A [Kubernetes deployment](https://github.com/windmilleng/tilt-example-go/blob/master/0-base/deployments/kubernetes.yaml) that runs the image

3) And finally, a [Tiltfile](https://github.com/windmilleng/tilt-example-go/blob/master/0-base/Tiltfile) that ties them together:

```python
docker_build('example-go-image', '.', 
    dockerfile='deployments/Dockerfile')
k8s_yaml('deployments/kubernetes.yaml')
k8s_resource('example-go', port_forwards=8000)
```

The first line tells Tilt to build an image with the name `example-go-image`
in the current directory.

The second line tells Tilt to load the Kubernetes
[Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#creating-a-deployment)
YAML. The image name in the `docker_build` call must match the container `image`
reference in the `example-go` Deployment.

The last line configures port-forwarding so that your server is
reachable at `localhost:8000`. The resource name in the `k8s_resource` call
must match the Deployment's `metadata.name` in `kubernetes.yaml`.

Try it! Run:

```
git clone https://github.com/windmilleng/tilt-example-go
cd tilt-example-go/0-base
tilt up
```

Tilt will open a browser showing the web UI, a unified view that shows you app
status and logs. Your terminal will also turn into a status box if you'd like to
watch your server come up there.

When it's ready, you will see the status icon turn green. The logs in the
bottom pane will display "Serving files on port 8000."

{% include example_guide_image.html
    img="example-go-image-1.png"
    url="https://cloud.tilt.dev/snapshot/AZzpx-YL_-WxDmRFwlk="
    title="The server is up!"
    caption="The server is up! (Click the screenshot to see an interactive view.)"
%}

## Step 1: Let's Add Benchmark Trickery

Before we try to make this faster, let's measure it.

Using [`local_resource`](local_resource.html), you can direct Tilt to execute existing scripts or arbitrary shell commands on your own machine, and manage them from your sidebar like any other Tilt resource. We're going to use this functionality to benchmark our deployments.

First, we add a `local_resource` to our
[Tiltfile](https://github.com/windmilleng/tilt-example-go/blob/master/1-measured/Tiltfile)
that records the start time in a Go file.

```python
k8s_resource(
    'example-go', 
    port_forwards=8000, 
    resource_deps=['deploy'])

# Records the current time, then kicks off a server update.
# Normally, you would let Tilt do deploys automatically, but this
# shows you how to set up a custom workflow that measures it.
local_resource(
    'deploy',
    './record-start-time.sh',
)
```

The `local_resource()` call creates a local resource named `deploy`. The second
argument is the script that it runs.

We've also modified our server to read that start time, calculate the time
elapsed, then display this in both logs and HTML.

Let's click the button on the `deploy` resource and see what happens!

{% include example_guide_image.html
    img="example-go-image-2.png"
    url="https://cloud.tilt.dev/snapshot/Ady3yOYL5yQatiGjVL0="
    title="Result of clicking the button on the 'deploy' resource."
    caption="Clicking the button triggers the 'deploy' local_resource, which in turn kicks off an update to the server. (Click the screenshot to see an interactive view.)"
%}

| Approach | Deploy Time[^1] |
|---|---|
| Naive | 4.2s |
{:.benchmark-report}

If you look closely, the elapsed time displayed in the Tilt sidebar is different
than the benchmark our app logged. That's OK! In multi-service development,
there are many benchmarks we care about -- the time to build the image, the time
to schedule the process, and the time until the server is ready to serve
traffic. 

Tilt offers you some default benchmarks, _and_ the tools to capture your own.

Our benchmarks show this is slow. Can we do better?

## Step 2: Let's Optimize for the Go Compiler

What's taking up so much time? The logs show that when we make the change to a file, we:

1) Copy the source files to the image.

2) Download the `gorilla/mux` dependency.

3) Compile the Go binary from scratch.

But the Go team has done a lot of work to make caching dependencies and
incremental compiles fast.  How can we better use the Go tools how they're meant
to be used?

With `local_resource`, we can compile the Go binary locally, and copy the binary to
the container.

Here's our [new Tiltfile](https://github.com/windmilleng/tilt-example-go/blob/master/2-optimized/Tiltfile) 
with the following new code:

```python
local_resource(
  'example-go-compile',
  'CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o build/tilt-example-go ./',
  deps=['./main.go', './start.go'],
  resource_deps = ['deploy'])
  
docker_build(
  'example-go-image',
  '.',
  dockerfile='deployments/Dockerfile',
  only=[
    './build',
    './web',
  ])
```

We've added a `local_resource()` that compiles the Go binary locally for our
Linux container.

We've also added a new `only` parameter to `docker_build()`.  We don't need the
source files in the Docker build context. We only need the `./build` directory
(for the compiled binary) and the `./web` directory (for the template and image
files). When we include only these directories, we ensure other changes don't
trigger builds.

Finally, we've modified the Dockerfile to only copy the `./build` and `./web`
directories.

Let's see what this looks like!

{% include example_guide_image.html
    img="example-go-image-3.png"
    url="https://cloud.tilt.dev/snapshot/AcK4yOYLQObve-87cQ4="
    title="Step 2 complete."
    caption="Step 2 complete. (Click the screenshot to see an interactive snapshot.)"
%}


| Approach | Deploy Time |
|---|---|
| Naive | 4.2s |
| Local Compile | 3.5s |
{:.benchmark-report}


## Step 3: Let's Live Update It

When we make a change to a file, we currently have to build an image, deploy new Kubernetes configs,
and wait for Kubernetes to schedule the pod.

With Tilt, we can skip all of these steps, and instead
[live_update](live_update_tutorial.html) the pod in place.

Here's our [new Tiltfile](https://github.com/windmilleng/tilt-example-go/blob/master/3-recommended/Tiltfile) 
with the following new code:

```python
docker_build(
  'example-go-image',
  '.',
  dockerfile='deployments/Dockerfile',
  only=[
    './build',
    './web',
  ],
  live_update=[
    sync('./build', '/app/build'),
    sync('./web', '/app/web'),
  ],
  entrypoint = 'find . | entr -r ./build/tilt-example-go')
```

We've added a `live_update` parameter to `docker_build()` with two `sync` steps.
They copy the code from the `./build` and `./web` directories into the container.

We've also added a new parameter: `entrypoint="find . | entr -r ./build/tilt-example-go"`.

`entr` is a tool that automatically restarts a shell command whenever the watched
file changes. This command restarts our server every time the pod is updated.

Let's see what this new configuration looks like in action:

{% include example_guide_image.html
    img="example-go-image-4.png"
    url="https://cloud.tilt.dev/snapshot/AbC5yOYLwib41yocobg="
    title="Tilt state after a live_update."
    caption="The result of a live_update. (Click the screenshot to see an interactive view.)"
%}

Tilt was able to update the container in less than 2 seconds!

## Our Recommendation

### Final Score

| Approach | Deploy Time |
|---|---|
| Naive | 4.2s |
| Local Compile | 3.5s |
| With live_update | 1.5s |
{:.benchmark-report}

You can try the server here:

[Recommended Structure](https://github.com/windmilleng/tilt-example-go/blob/master/3-recommended){:.attached-above}

Congratulations on finishing this guide!

## Further Reading

This guide recommends an approach to Go development that shines with Tilt.

If you're curious about other approaches to multi-service Go development and
their trade-offs, we're working on a talk and workshop:

[The Quest For The Fastest Deployment Time](https://github.com/windmilleng/fast){:.attached-above}

### Other sample Go projects:

- [abc123](https://github.com/windmilleng/abc123) a mini microservice app with a Go server called `fe`.
- The [Live Update Tutorial](live_update_tutorial.html), which optimizes a Go server.
- [Servantes](https://github.com/windmilleng/servantes), our multi-language microservice demo app.

### Examples in other languages:

<ul>
  {% for page in site.data.examples %}
     {% if page.href contains "go" %}
       <!-- skip -->
     {% else %}
        <li><a href="/{{page.href | escape}}">{{page.title | escape}}</a></li>
     {% endif %}
  {% endfor %}
</ul>

[^1]: Tilt's first deployment of a service takes a few seconds longer than subsequent ones, due to some behind-the-scenes setup. Measurements in this guide focus on non-initial builds.
