---
title: "Example: NodeJS"
layout: docs
lang: nodejs
---

The best indicator of a healthy development workflow is a short feedback loop.

Kubernetes is a huge wrench in the works.

Let's fix this.

In this example, we're going to take you through a simple “hello world” server written in NodeJS that uses [Mustache](https://mustache.github.io/) for templating and [Express](https://expressjs.com/) for serving.

We'll use Tilt to:

- Run the server on Kubernetes
- Measure the time from a code change to a new process
- Optimize that time for fast feedback

This particular example server doesn't do much, but it's useful to confirm that Tilt is working as expected in your environment.

All the code is in this repo:

[tilt-example-nodejs](https://github.com/windmilleng/tilt-example-nodejs)

To skip straight to the fully optimized setup, go to this subdirectory:

[Recommended Tiltfile](https://github.com/windmilleng/tilt-example-nodejs/tree/master/3-recommended)

## Step 0: The Simplest Deployment

Our server is just a few lines long, and all it does is serve us an HTML page:

```javascript
const express = require('express');
const app = express();
const path = require('path');

app.use(express.static('public'));

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname + '/index.html'));
});

app.listen(8000, () => {
    console.log('Server running at http://localhost:8000/');
});
```

To start this server on Kubernetes, we need 3 configs:

1. A [Dockerfile](https://github.com/windmilleng/tilt-example-nodejs/blob/master/0-base/Dockerfile) that builds the image
2. A [Kubernetes deployment](https://github.com/windmilleng/tilt-example-nodejs/blob/master/0-base/kubernetes.yaml) that runs the image
3. And finally, a [Tiltfile](https://github.com/windmilleng/tilt-example-nodejs/blob/master/0-base/Tiltfile) that ties them together:

```python
docker_build('example-nodejs-image', '.')
k8s_yaml('kubernetes.yaml')
k8s_resource('example-nodejs', port_forwards=8000)
```

The first line tells Tilt to build an image with the name `example-nodejs-image`
in the directory `.` (the current directory).

The second line tells Tilt to load the Kubernetes
[Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#creating-a-deployment)
YAML. The image name in the `docker_build` call must match the container `image`
reference in the `example-nodejs` Deployment.

The last line configures port-forwarding so that your server is
reachable at http://localhost:8000/. The resource name in the `k8s_resource` call
must match the Deployment's `metadata.name` in `kubernetes.yaml`.

Try it! Run:

```
git clone https://github.com/windmilleng/tilt-example-nodejs
cd tilt-example-nodejs/0-base
tilt up
```

Tilt will open a browser showing the web UI, a unified view that shows you app
status and logs. Your terminal will also turn into a status box if you'd like to
watch your server come up there.

When the server is ready, you will see the status icon turn green. The log pane will display:
> Server running at http://localhost:8000/

{% assign case = "base" %}
{% include example_guide_image.html %}

## Step 1: Let's Add Benchmark Trickery

Before we try to make this faster, let's measure it.

In addition to running things in your cluster, Tilt can run commands locally.
You can direct Tilt to execute existing scripts or arbitrary shell commands on your own machine.

We want to measure the time from code change to new process. To do that, we'll
use [`local_resource`](local_resource.html), which lets you locally
run scripts, shell code, or servers, and manage them from your sidebar like any
other Tilt resource.

First, we add a `local_resource` to our
[Tiltfile](https://github.com/windmilleng/tilt-example-nodejs/blob/master/1-measured/Tiltfile)
that records the current time, then kicks off an update.

```python
# Records the current time, then kicks off a server update.
# Normally, you would let Tilt do deploys automatically, but this
# shows you how to set up a custom workflow that measures it.
local_resource(
  'deploy',
  'date +%s > start-time.txt'
)

k8s_resource('example-nodejs', port_forwards=8000,
    resource_deps=['deploy']
)
```

The `local_resource()` call creates a local resource named `deploy`. The second
argument is the command that it runs.

We've also modified our server itself to read that start time and display the time elapsed in the HTML it serves:
```javascript
const fs = require('fs');
let timeSince = 'N/A';
...
app.get('/', (req, res) => {
    res.render('index.mustache', {
        time: timeSince,
    });
});

app.listen(8000, () => {
    timeSince = getSecsSinceDeploy();
    console.log('Server running at http://localhost:8000/');
});

function getSecsSinceDeploy() {
    let curTimeMs = new Date().getTime();
    let contents = fs.readFileSync('/app/start-time.txt', 'utf8');
    let startTimeMs  = parseInt(contents.trim()) / 10**6;
    return ((curTimeMs - startTimeMs) / 10**3).toFixed(2)
}
```
Whenever the app starts up, it calls `getSecsSinceDeploy()`, calculates the time elapsed, and displays that value in the served webpage. (We've added a new dep for this purpose: the templating engine [mustache-express](https://www.npmjs.com/package/mustache-express).)

See that button next to the `deploy` resource? Let's click it and see what happens!

{% assign content = site.data.example_guides.nodejs.measured %}
{% include example_guide_image.html %}

| Approach | Deploy Time[^1]
|---|---|
| Naive | 11.31-14.21s |
{:.benchmark-report}

If you look closely, the elapsed time displayed in the Tilt sidebar is different
than the benchmark our app logged. That's OK! In multi-service development,
there are many benchmarks we care about---the time to build the image, the time
to schedule the process, and the time until the server is ready to serve
traffic.

The Tilt sidebar gives you some default benchmarks, _and_ the tools to capture
your own benchmarks.

Our benchmarks show this is slow. Can we do better?

## Step 2: Why Is the Docker Build So Slow?

The first thing I notice when I click "deploy" is a bunch of logs from `yarn install`; and not just once, but _every dang time_. This is a hint that we can optimize our Dockerfile to be smarter about caching. With a little rearranging, our [new Dockerfile]((https://github.com/windmilleng/tilt-example-nodejs/blob/master/2-optimized-dockerfile/Dockerfile)) looks like this:
```
FROM node:10

WORKDIR /app

ADD package.json .
ADD yarn.lock .
RUN yarn install

ADD . .

ENTRYPOINT [ "node", "/app/index.js" ]
```

Here's what it looks like when we build with our new Dockerfile:

{% assign case = "dockerfile" %}
{% include example_guide_image.html %}

Hooray, we're now using the cache instead of running `yarn install` for every single build. (For more on the principles at work here, [check out this guide](https://nodejs.org/en/docs/guides/nodejs-docker-webapp/#creating-a-dockerfile).)

Here's what our timing looks like now:

| Approach | Deploy Time
|---|---|
| Naive | 11.31-14.21s |
| Optimized Dockerfile | 3.25-4.12s |
{:.benchmark-report}

Pretty good! But Tilt has some tricks up its sleeve to make it even faster.

## Step 3: Let's Optimize It _Even More_

When we make a change to a file, we currently have to build an image, deploy new Kubernetes configs,
and wait for Kubernetes to schedule the pod.

With Tilt, we can skip all of these steps, and instead
[live_update](live_update_tutorial.html) the pod in place.

The first thing we need to do is change how our app is invoked: we're going to run it via [nodemon](https://nodemon.io/), a utility that monitors source files for changes and restarts your app as necessary.  In this branch, as reflected in [package.json](https://github.com/windmilleng/tilt-example-nodejs/blob/master/3-recommended/package.json), we've already run `yarn add --dev nodemon` to add nodemon as a dev dependency.

[Our new Tiltfile](https://github.com/windmilleng/tilt-example-nodejs/blob/master/3-recommended/Tiltfile) contains the following new code:

```python
# Add a live_update rule to our docker_build
congrats = "🎉 Congrats, you ran a live_update! 🎉"
docker_build('example-nodejs-image', '.',
    build_args={'node_env': 'development'},
    entrypoint='yarn run nodemon /app/index.js',
    live_update=[
        sync('.', '/app'),
        run('cd /app && yarn install', trigger=['./package.json', './yarn.lock']),

        # if all that changed was start-time.txt, make sure the server
        # reloads so that it will reflect the new startup time
        run('touch /app/index.js', trigger='./start-time.txt'),

        # add a congrats message!
        run('sed -i "s/Hello cats!/{}/g" /app/views/index.mustache'.
            format(congrats)),
])
```
We've added some new parameters to `docker_build` that tell the container to use nodemon:
1. The `entrypoint` parameter overrides the `ENTRYPOINT` specified in the Dockerfile; now when the container executes, it will run `yarn run nodemon /app/index.js`
2. The `build_args` parameter corresponds to this Dockerfile change:
    ```
    # Default value; will be overridden by build_args, if passed
    ARG node_env=production

    ENV NODE_ENV $node_env
    ```
   Together, these changes mean that when we build this Dockerfile via this Tiltfile, we set the env var `$NODE_ENV=development`, and our `yarn install` call will install dev dependencies.

With the help of Tilt, we've done a pretty cool thing: we've set it up so this Dockerfile can run the app for development (when invoked via Tilt) or for production (when invoked otherwise).

The other new addition to our Tiltfile is the `live_update` argument to `docker_build`, which enables super-fast in-place updates of your app. When a [live_update](https://docs.tilt.dev/live_update_tutorial.html) is triggered, Tilt will, in order:
1. Sync the code from the current directory (`.`) into the container at directory `/app`
2. IF `package.json` or `yarn.lock` has changed, run `yarn install`
3. Poke `index.js` if necessary to make sure that nodemon reloads the server
4. Congratulate you on finishing this guide!

Let's see what this new configuration looks like in action:

{% assign case = "live_update" %}
{% include example_guide_image.html %}

Tilt and nodemon together updated the container in less than two seconds!

## Our Recommendation

### Final Score

| Approach | Deploy Time
|---|---|
| Naive | 11.31-14.21s |
| Optimized Dockerfile | 3.25-4.12s |
| With live_update | 1.1-1.8s |
{:.benchmark-report}

You can try the server here:

[Recommended Structure](https://github.com/windmilleng/tilt-example-nodejs/blob/master/3-recommended)

This is a very simple example, but we hope it gives you a good starting point for running your NodeJS app via Tilt!

## Further Reading

### Other sample NodeJS projects:
- [abc123](https://github.com/windmilleng/abc123) is a mini microservice app with a NodeJS server called `letters`
- [Servantes](https://github.com/windmilleng/servantes), our multi-language microservice demo app, contains a NodeJS service called `spoonerisms`

### Examples in other languages:

<ul>
  {% for page in site.data.examples %}
     {% if page.href contains "nodejs" %}
       <!-- skip -->
     {% else %}
        <li><a href="/{{page.href | escape}}">{{page.title | escape}}</a></li>
     {% endif %}
  {% endfor %}
</ul>

[^1]: Tilt's first deployment of a service takes a few seconds longer than subsequent ones, due to some behind-the-scenes setup. Measurements in this guide focus on non-initial builds.
