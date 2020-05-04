---
title: "Example: Python + Flask"
layout: docs
lang: python
---

The best indicator of a healthy development workflow is a short feedback loop.

Kubernetes is a huge wrench in the works.

Let's fix this.

In this example, we're going to take you through a simple “hello world” server written in Python that uses [Flask](https://palletsprojects.com/p/flask/), a lightweight web application framework.  (Want this guide for Django or another framework? [Let us know](https://tilt.dev/contact).)

We'll use Tilt to:

- Run the server on Kubernetes
- Measure the time from a code change to a new process
- Optimize that time for faster feedback

This particular example server doesn't do much, but it's useful to confirm that Tilt is working as expected in your environment.

All the code is in this repo:

[tilt-example-python](https://github.com/windmilleng/tilt-example-python){:.attached-above}

To skip straight to the fully optimized setup, go to this subdirectory:

[Recommended Setup](https://github.com/windmilleng/tilt-example-python/blob/master/3-recommended){:.attached-above}

## Step 0: The Simplest Deployment

Our server is just seven lines long, and all it does is serve us an HTML page:

```python
from flask import Flask, render_template
app = Flask(__name__)


@app.route("/")
def serve():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(port=8000)
```

To start this server on Kubernetes, we need three config files:

1. A [Dockerfile](https://github.com/windmilleng/tilt-example-python/blob/master/0-base/Dockerfile) that builds the image
2. A [Kubernetes deployment](https://github.com/windmilleng/tilt-example-python/blob/master/0-base/kubernetes.yaml) that runs the image
3. And finally, a [Tiltfile](https://github.com/windmilleng/tilt-example-python/blob/master/0-base/Tiltfile) that ties them together:

```python
docker_build('example-python-image', '.')
k8s_yaml('kubernetes.yaml')
k8s_resource('example-python', port_forwards=8000)
```

The first line tells Tilt to build an image with the name `example-python-image`
in the current directory.

The second line tells Tilt to load the Kubernetes
[Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#creating-a-deployment)
YAML. The image name in the `docker_build` call must match the container `image`
reference in the `example-python` Deployment.

The last line configures port-forwarding so that your server is
reachable at `localhost:8000`. The resource name in the `k8s_resource` call
must match the Deployment's `metadata.name` in `kubernetes.yaml`.

Try it! Run:

```
git clone https://github.com/windmilleng/tilt-example-python
cd tilt-example-python/0-base
tilt up
```

Tilt will open a browser showing the web UI, a unified view that shows you app
status and logs. Your terminal will also turn into a status box if you'd like to
watch your server come up there.

When the server is ready, you will see the status icon turn green. The log pane will display some output from Flask, starting with:
> Serving Flask app "app"

{% include example_guide_image.html
    img="example-python-0-base.png"
    url="https://cloud.tilt.dev/snapshot/AcTG0ucLlISGcy3NXSU="
    title="The server is up!"
    caption="The server is up! (Click the screenshot to see an interactive view.)"
%}

## Step 1: Let's Add Benchmark Trickery

Before we try to make this faster, let's measure it.

Using [`local_resource`](local_resource.html), you can direct Tilt to execute existing scripts or arbitrary shell commands on your own machine, and manage them from your sidebar like any other Tilt resource. We're going to use this functionality to benchmark our deployments.

First, we add a `local_resource` to our
[Tiltfile](https://github.com/windmilleng/tilt-example-python/blob/master/1-measured/Tiltfile)
that records the current time, then kicks off an update.

```python
# Records the current time, then kicks off a server update.
# Normally, you would let Tilt do deploys automatically, but this
# shows you how to set up a custom workflow that measures it.
local_resource(
  'deploy',
  'date +%s > start-time.txt'
)
…
k8s_resource('example-python', port_forwards=8000,
             resource_deps=['deploy'])
```

The `local_resource()` call creates a local resource named `deploy`. The second
argument is the command that it runs.

We've also modified our server itself to read that start time and print the time elapsed:
```python
def get_update_time_secs() -> float:
    with open('/app/start-time.txt', 'r') as file:
        start_ns_since_epoch = float(file.read().strip())

    start_secs_since_epoch = start_ns_since_epoch / 10**9
    now_secs_since_epoch = time.time()

    return round(now_secs_since_epoch - start_secs_since_epoch, 2)
...
if __name__ == "__main__":
    UPDATE_TIME = get_update_time_secs()
    app.run(port=8000)
```
Whenever the app starts up, it calls `get_update_time_secs()`, does the math to figure out the time elapsed since the timestamp in `start-time.txt`, and stores that value in a global variable; when the app serves `index.html`, it passes that value into the HTML template so that it shows up in the webpage.

See that button next to the `deploy` resource?

{% assign case = "deploy_button" %}
{% include example_guide_image.html %}

Let's click it and see what happens!

{% include example_guide_image.html
    img="example-python-1-measured.png"
    url="https://cloud.tilt.dev/snapshot/AeTJ0ucLJor0hnfdg7s="
    title="Result of clicking the button on the 'deploy' resource."
    caption="Clicking the button triggers the 'deploy' local_resource, which in turn kicks off an update to the server. (Click the screenshot to see an interactive view.)"
%}

| Approach | Deploy Time[^1]
|---|---|
| Naive | 10-11s |
{:.benchmark-report}

If you look closely, the elapsed time displayed in the Tilt sidebar is different
than the benchmark our app logged. That's OK! In multi-service development,
there are many benchmarks we care about -- the time to build the image, the time
to schedule the process, and the time until the server is ready to serve
traffic. 

Tilt offers you some default benchmarks, _and_ the tools to capture your own.

Our benchmarks show this is slow. Can we do better?

## Step 2: Why Is the Docker Build So Slow?

The first thing I notice when I click "deploy" is a bunch of logs from `pip install`; and not just once, but _every dang time_. This is a hint that we can optimize our Dockerfile to be smarter about caching. With a little rearranging, our [new Dockerfile](https://github.com/windmilleng/tilt-example-python/blob/master/2-optimize-dockerfile/Dockerfile) looks like this:
```
ADD requirements.txt .
RUN pip install -r requirements.txt

ADD . .
```

Here's what it looks like when we build with our new Dockerfile:

{% include example_guide_image.html
    img="example-python-2-dockerfile.png"
    url="https://cloud.tilt.dev/snapshot/AZjdiecL6XcZBu5kO3Y="
    title="A Docker build making good use of caching."
    caption="Dependency installation now uses the cache instead of actually running a long, slow command. (Click the screenshot to see an interactive view.)"
%}

Hooray, we're now using the cache instead of running `pip install` for every single build. (For more on the principles at work here, [check out this guide](https://pythonspeed.com/articles/docker-caching-model/).)

Here's what our timing looks like now:

| Approach | Deploy Time
|---|---|
| Naive | 10-11s |
| Optimized Dockerfile | 2.5-3.1s |
{:.benchmark-report}

Pretty good! But Tilt has some tricks up its sleeve to make it even faster.

## Step 3: Let's Optimize It _Even More_

When we make a change to a file, we currently have to build an image, deploy new Kubernetes configs,
and wait for Kubernetes to schedule the pod.

With Tilt, we can skip all of these steps, and instead
[live_update](live_update_tutorial.html) the pod in place.

[Our new Tiltfile](https://github.com/windmilleng/tilt-example-python/blob/master/3-recommended/Tiltfile) contains the following new code:

```python
# Add a live_update rule to our docker_build
congrats = "🎉 Congrats, you ran a live_update! 🎉"
docker_build('example-python-image', '.', build_args={'flask_env': 'development'},
    live_update=[
        sync('.', '/app'),
        run('cd /app && pip install -r requirements.txt',
            trigger='./requirements.txt'),

        # if all that changed was start-time.txt, make sure the server
        # reloads so that it will reflect the new startup time
        run('touch /app/app.py', trigger='./start-time.txt'),

        # add a congrats message!
        run('sed -i "s/Hello cats!/{}/g" /app/templates/index.html'.
            format(congrats)),
])
```

We've added two new parameters to `docker_build()`: `build_args` and `live_update`. Let's look at the latter first.

When a [live_update](https://docs.tilt.dev/live_update_tutorial.html) is triggered, Tilt will, in order:
1. Sync the code from the current directory (`.`) into the container at directory `/app`.
2. IF `requirements.txt` has changed, run `pip install`
3. Poke `app.py` if necessary to make sure that Flask reloads the server
4. Congratulate you on finishing this guide!

The second additional parameter, `build_args={'flask_env': 'development'}`, corresponds to this Dockerfile change:
```
# Default value; will be overridden by build-args, if passed
ARG flask_env=production

ENV FLASK_ENV $flask_env
```
Together, these changes mean that when we build this Dockerfile via this Tiltfile, our Flask app will run in development mode.  When in development mode, Flask watches for file changes and reloads the server when necessary.

Let's see what this new configuration looks like in action:

{% include example_guide_image.html
    img="example-python-3-liveupdate.png"
    url="https://cloud.tilt.dev/snapshot/AfLO0ucLqMHzz2JA5ls="
    title="Tilt state after a live_update."
    caption="The result of a live_update. (Click the screenshot to see an interactive view.)."
%}

Tilt was able to update the container in less than two seconds! (And a chunk of that time was overhead from Flask, not from Tilt.)

## Our Recommendation

### Final Score

| Approach | Deploy Time
|---|---|
| Naive | 10-11s |
| Optimized Dockerfile | 2.5-3.1s |
| With live_update | 1-2s |
{:.benchmark-report}

You can try the server here:

[Recommended Structure](https://github.com/windmilleng/tilt-example-python/blob/master/3-recommended){:.attached-above}

This is a very simple example, but we hope it gives you a good starting point for running your Flask app (or other Python app) via Tilt!

## Further Reading

### Other sample Python projects:
- [abc123](https://github.com/windmilleng/abc123) is a mini microservice app with a Python server called `numbers`
- Our [blog post about Live Update](https://blog.tilt.dev/2019/04/02/fast-kubernetes-development-with-live-update.html) includes an [example Python server](https://github.com/windmilleng/live_update/tree/master/python)
- [Servantes](https://github.com/windmilleng/servantes), our multi-language microservice demo app, contains a Python service called `hypothesizer`

### Examples in other languages:

<ul>
  {% for page in site.data.examples %}
     {% if page.href contains "python" %}
       <!-- skip -->
     {% else %}
        <li><a href="/{{page.href | escape}}">{{page.title | escape}}</a></li>
     {% endif %}
  {% endfor %}
</ul>

[^1]: Tilt's first deployment of a service takes a few seconds longer than subsequent ones, due to some behind-the-scenes setup. Measurements in this guide focus on non-initial builds.

<script src="/assets/js/links.js" async></script>
