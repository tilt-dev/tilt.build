---
title: "Example: Java"
description: "Best practices for developing Java projects with Tilt"
layout: docs
lang: java
---

The best indicator of a healthy development workflow is a short feedback loop.

Kubernetes is a huge wrench in the works.

Let's fix this.

In this example, we're going to take you through a simple server that uses
[Spring Boot](https://spring.io/projects/spring-boot) and templates to serve
HTML. Our example is loosely based on 
[Serving Web Content with Spring MVC](https://spring.io/guides/gs/serving-web-content/).

We'll use Tilt to:

- Run the server on Kubernetes
- Measure the time from a code change to a new process
- Optimize that time for faster feedback

All the code is in this repo:

[tilt-example-java](https://github.com/tilt-dev/tilt-example-java){:.attached-above}

To skip straight to the fully optimized setup, go to this subdirectory:

[Recommended Setup](https://github.com/tilt-dev/tilt-example-java/blob/master/4-recommended){:.attached-above}

## Step 0: The Simplest Deployment

Our server uses Spring Web for routing requests.

```java
package dev.tilt.example;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
public class IndexController {

  @GetMapping("/")
  public String index(Model model) {
    // Serves the index.html template under
    // src/main/resources/templates/index.html
    return "index";
  }

}
```

To start this server on Kubernetes, we need three config files:

1) A [Dockerfile](https://github.com/tilt-dev/tilt-example-java/blob/master/0-base/Dockerfile) that builds the image

2) A [Kubernetes deployment](https://github.com/tilt-dev/tilt-example-java/blob/master/0-base/kubernetes.yaml) that runs the image

3) And finally, a [Tiltfile](https://github.com/tilt-dev/tilt-example-java/blob/master/0-base/Tiltfile) that ties them together:

```python
docker_build('example-java-image', '.')
k8s_yaml('kubernetes.yaml')
k8s_resource('example-java', port_forwards=8000)
```

The first line tells Tilt to build an image with the name `example-java-image`
in the current directory.

The second line tells Tilt to load the Kubernetes
[Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#creating-a-deployment)
YAML. The image name in the `docker_build` call must match the container `image`
reference in the `example-java` Deployment.

The last line configures port-forwarding so that your server is
reachable at `localhost:8000`. The resource name in the `k8s_resource` call
must match the Deployment's `metadata.name` in `kubernetes.yaml`.

Try it! Run:

```
git clone https://github.com/tilt-dev/tilt-example-java
cd tilt-example-java/0-base
tilt up
```

Tilt will open a browser showing the web UI, a unified view that shows you app
status and logs. Your terminal will also turn into a status box if you'd like to
watch your server come up there.

When it's ready, you will see the status icon turn green. The logs in the
bottom pane will display "Tomcat initialized with port(s): 8000."

{% include example_guide_image.html
    img="example-java-image-1.png"
    url="https://cloud.tilt.dev/snapshot/AfbdiucLHi33cqQwrG4="
    title="The server is up!"
    caption="The server is up! (Click the screenshot to see an interactive view.)"
%}

## Step 1: Let's Add Benchmark Trickery

Before we try to make this faster, let's measure it.

Using [`local_resource`](local_resource.html), you can direct Tilt to execute existing scripts or arbitrary shell commands on your own machine, and manage them from your sidebar like any other Tilt resource. We're going to use this functionality to benchmark our deployments.

First, we add a `local_resource` to our
[Tiltfile](https://github.com/tilt-dev/tilt-example-java/blob/master/1-measured/Tiltfile)
that records the start time in a Java file.

```python
k8s_resource(
    'example-java', 
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
    img="example-java-image-2.png"
    url="https://cloud.tilt.dev/snapshot/AeDqiucLr-00XLJpiWc="
    title="Result of clicking the button on the 'deploy' resource."
    caption="Clicking the button triggers the 'deploy' local_resource, which in turn kicks off an update to the server. (Click the screenshot to see an interactive view.)"
%}

| Approach | Deploy Time[^1] |
|---|---|
| Naive | 87.7s |
{:.benchmark-report}

If you look closely, the elapsed time displayed in the Tilt sidebar is different
than the benchmark our app logged. That's OK! In microservice development,
there are many benchmarks we care about -- the time to build the image, the time
to schedule the process, and the time until the server is ready to serve
traffic. 

Tilt offers you some default benchmarks, _and_ the tools to capture your own.

Our benchmarks show this is slow. Can we do better?

## Step 2: Let's Optimize for the Java Toolchain

What's taking up so much time? The logs show that when we make the change to a file, we:

1) Copy the source files to the image.

2) Download Gradle.

3) Download all the Spring dependencies.

4) Compile the Java jar from scratch.

But the Java community has done a lot of work to make caching dependencies and
incremental compiles fast.  How can we better use the tools how they're meant
to be used?

With `local_resource`, we can compile the executable Jar locally, and copy it
to the container.

Here's our [new Tiltfile](https://github.com/tilt-dev/tilt-example-java/blob/master/2-optimized/Tiltfile) 
with the following new code:

```python
local_resource(
  'example-java-compile',
  './gradlew bootJar',
  deps=['src', 'build.gradle'],
  resource_deps = ['deploy'])
  
docker_build(
  'example-java-image',
  './build/libs',
  dockerfile='./Dockerfile')
```

We've added a `local_resource()` that compiles the executable Jar locally
with Gradle.

We've adjusted the Docker context so that it only includes the build artifacts
under `./build/libs`.

Finally, we've modified the Dockerfile to only copy the executable jar.

Let's see what this looks like!

{% include example_guide_image.html
    img="example-java-image-3.png"
    url="https://cloud.tilt.dev/snapshot/AabuiucL7NKgfiTa1uI="
    title="Step 2 complete."
    caption="Step 2 complete. (Click the screenshot to see an interactive snapshot.)"
%}

| Approach | Deploy Time |
|---|---|
| Naive | 87.7s |
| Local Compile | 13.4s |
{:.benchmark-report}

## Step 3: Why Is the Docker Build So Slow?

Currently, our image contains a fat executable Jar.

If we unpacked the fat Jar, we would find that the Jar contains many files
internally. These files naturally lend themselves to Docker layers. 
Java Jars were using layer caches before Docker made them cool. How can we take
advantage of this?

We've updated [our
Tiltfile](https://github.com/tilt-dev/tilt-example-java/blob/master/3-unpacked/Tiltfile)
to unpack the Jar in the `build/jar` directory:

```python
local_resource(
  'example-java-compile',
  './gradlew bootJar && ' +
  'unzip -o build/libs/example-0.0.1-SNAPSHOT.jar -d build/jar',
  deps=['src', 'build.gradle'],
  resource_deps = ['deploy'])
```

We've also updated our [Dockerfile](https://github.com/tilt-dev/tilt-example-java/blob/master/3-unpacked/Dockerfile):

```
FROM openjdk:8-jre-alpine

WORKDIR /app
ADD BOOT-INF/lib /app/lib
ADD META-INF /app/META-INF
ADD BOOT-INF/classes /app

ENTRYPOINT java -cp .:./lib/* dev.tilt.example.ExampleApplication
```

This Dockerfile adds files from `build/jar` in order from least frequently
used to most frequently used, to improve caching.

The Dockerfile also has a new the entrypoint to load the main application class,
since we're no longer using an executable Jar.

Let's see what this looks like!

{% include example_guide_image.html
    img="example-java-image-4.png"
    url="https://cloud.tilt.dev/snapshot/AcaQnucLOBUS4TGQauw="
    title="Step 3 complete."
    caption="Step 3 complete. (Click the screenshot to see an interactive snapshot.)"
%}

| Approach | Deploy Time |
|---|---|
| Naive | 87.7s |
| Local Compile | 13.4s |
| Optimized Dockerfile | 6.5s |
{:.benchmark-report}

If you don't want to optimize the Dockerfile yourself,
check out [Jib](https://github.com/GoogleContainerTools/jib)!

Jib is a Java image builder that re-packs Java Jars as container images using
similar tricks. There are Jib plugins for Maven and Gradle.  The
[tilt-example-java](https://github.com/tilt-dev/tilt-example-java) repo has
an example
[Tiltfile](https://github.com/tilt-dev/tilt-example-java/blob/master/101-jib/Tiltfile)
that uses `custom_build` to generate images with Jib.

## Step 4: Let's Live Update It

When we make a change to a file, we currently have to build an image, deploy new
Kubernetes configs, and wait for Kubernetes to schedule the pod.

With Tilt, we can skip all of these steps, and instead
[live_update](live_update_tutorial.html) the pod in place.

Here's our [new Tiltfile](https://github.com/tilt-dev/tilt-example-java/blob/master/4-recommended/Tiltfile) 
with the following new code:

```python
load('ext://restart_process', 'docker_build_with_restart')
...
local_resource(
  'example-java-compile',
  gradlew + ' bootJar && ' +
  'unzip -o build/libs/example-0.0.1-SNAPSHOT.jar -d build/jar-staging && ' +
  'rsync --inplace --checksum -r build/jar-staging/ build/jar',
  deps=['src', 'build.gradle'],
  resource_deps = ['deploy'])

docker_build_with_restart(
  'example-java-image',
  './build/jar',
  entrypoint=['java', '-noverify', '-cp', '.:./lib/*', 'dev.tilt.example.ExampleApplication'],
  dockerfile='./Dockerfile',
  live_update=[
    sync('./build/jar/BOOT-INF/lib', '/app/lib'),
    sync('./build/jar/META-INF', '/app/META-INF'),
    sync('./build/jar/BOOT-INF/classes', '/app'),
  ],
)
```

The first thing to notice is the `live_update` parameter, which consists of some `sync` steps.
They copy the library and compiled `.class `files from the `./build/jar`
directory into the container.

After syncing the files, we want to re-execute our updated binary. We accomplish this with the
[`restart_process` extension](https://github.com/windmilleng/tilt-extensions/tree/master/restart_process),
which we imported with the `load` call on the first line. (For more on extensions, [see the docs](/extensions.html).)
We swap out our `docker_build` call for function we imported, `docker_build_with_restart`: it's
almost exactly the same as `docker_build`, only it knows to restart our process at the end
of a `live_update`. The `entrypoint` parameter specifies what command to re-execute.

Lastly, our `local_resource` first unzips the jar to `build/jar-staging`, and
then uses `rsync --checksum` to copy that to `build/jar`.
Tilt's live_update will copy any files that have been touched.
`rsync --checksum` copies the directory, but doesn't touch any files that haven't changed.

Let's see what this new configuration looks like in action:

{% include example_guide_image.html
    img="example-java-image-5.png"
    url="https://cloud.tilt.dev/snapshot/AeKPnucLESM6hHyx8HY="
    title="Tilt state after a live_update."
    caption="The result of a live_update. (Click the screenshot to see an interactive view.)"
%}

Tilt was able to update the container in less than 5 seconds!

## Our Recommendation

### Final Score

| Approach | Deploy Time |
|---|---|
| Naive | 87.7s |
| Local Compile | 13.4s |
| Optimized Dockerfile | 6.5s |
| With live_update | 4.8s |
{:.benchmark-report}

You can try the server here:

[Recommended Structure](https://github.com/tilt-dev/tilt-example-java/blob/master/4-recommended){:.attached-above}

Congratulations on finishing this guide!

## Further Reading

### CI

Once you're done configuring your project, set up a CI test to ensure
your setup doesn't break! In the example repo, CircleCI uses
[`ctlptl`](https://github.com/tilt-dev/ctlptl) to create a single-use Kubernetes
cluster. The test script invokes `tilt ci`.  The `tilt ci` command deploys all
services in a Tiltfile and exits successfully if they're healthy.

- [CircleCI config](https://github.com/tilt-dev/tilt-example-java/blob/master/.circleci/config.yml)
- [Test script](https://github.com/tilt-dev/tilt-example-java/blob/master/test/test.sh)

### Optimizations

This guide recommends an approach to Java development that shines with Tilt.

There are even more optimizations you can add. Many are toolchain-specific. 
We've heard that you can get the JVM to hot-reload class files
(e.g. with [Spring Loaded](https://github.com/spring-projects/spring-loaded)) 
but we've had mixed results using this with live_update.

For more discussion of build optimization, see:

- [Spring Boot Docker](https://spring.io/guides/topicals/spring-boot-docker/), a
  discussion of how to better optimize Spring Boot apps for Docker. We used
  many of the lessons in this guide. There are still more tricks for improving
  performance in containers.
- Tilt's [Java Examples repo](https://github.com/tilt-dev/tilt-example-java/), which besides the code
  from this guide, contains examples of how to use Tilt with a number of different Java tools, including:
  - [Jib](https://github.com/GoogleContainerTools/jib), a Java image builder
    that re-packs Java Jars as container images, and integrates well with
    existing Maven or Gradle builds ([example here](https://github.com/tilt-dev/tilt-example-java/blob/master/101-jib/Tiltfile)).
  - [Quarkus](https://quarkus.io/), a container-first, hot-reloading framework for writing Java
    applications ([example here](https://github.com/tilt-dev/tilt-example-java/tree/master/201-quarkus-live-update)).
  
### Examples in other languages:

<ul>
  {% for page in site.data.examples %}
     {% if page.href contains "java" %}
       <!-- skip -->
     {% else %}
        <li><a href="/{{page.href | escape}}">{{page.title | escape}}</a></li>
     {% endif %}
  {% endfor %}
</ul>

[^1]: Tilt's first deployment of a service takes a few seconds longer than subsequent ones, due to some behind-the-scenes setup. Measurements in this guide focus on non-initial builds.
