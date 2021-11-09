---
title: Choosing an Image Registry
description: "A guide to dev image registries and how to get your code into a cluster."
layout: docs
sidebar: guides
---

If you're building container images in dev, you'll need a place to put those
images where your cluster can pull them.

## The Easy Way (for 95% of Users)

Here's how you set up a dev image registry.

Step 1) [Choose a cluster](choosing_clusters.html).

Step 2) There is no step 2!!!

### Your Registry is Usually Already Set Up For You

For almost all clusters, the cluster will have a registry for you.

- If you're using Docker for Desktop, there's no registry at all. You build
  directly into the container runtime.

- If you're using Kind, [our setup scripts](choosing_clusters.html) will set up
  a registry for you.

- If you're using a remote cluster (like AKS, EKS, GKE, and DigitalOcean
  Kuberentes), you'll have a registry that's colocated with your cluster.

### Your Registry Secrets are Usually Already Set Up For You

You also don't have to worry about authentication.

Our local cluster guides set up registries without any auth (because they're purely local).

If you're using an authenticated registry, that's usually not a problem either.
Tilt never talks directly to a registry. When Tilt builds images, it tells the
image builder to push to the registry when it's done. If you need to login to a
registry, you'll login with the image builder.

For Docker Hub, you run:

```
docker login
```

with a username and password (or token).

Other registries have their own login command, e.g.,

```
docker login quay.io
```

Some managed Kubernetes services have their own credential helpers:

- [Amazon ECR](https://github.com/awslabs/amazon-ecr-credential-helper)

- [Google Artifact Registry](https://cloud.google.com/artifact-registry/docs/docker/quickstart)

- [Google Container Registry](https://cloud.google.com/container-registry/docs/advanced-authentication)

These will ensure that your login credentials for kubectl and your login
credentials for the registry stay in-sync.

## The Medium-Easy Way (for 4% of users)

If you're using a cluster that doesn't have a registry,
there's a medium-easy option to get you unblocked fast.

[`ttl.sh`](https://ttl.sh/) is an anoymous, ephemeral image registry that you can use for development.
It's operated by our friends at [Replicated](https://www.replicated.com/).

Add the following function to your Tiltfile:

```
default_registry('ttl.sh/[my-user-name]-[random-string]')
```

First, Tilt will try to load the image directly to the cluster (if the cluster supports this.)

If it can't do that, Tilt will rename the image under the ttl.sh URL, push it to
the ephemeral registry, and pull it into your cluster.

`ttl.sh` is encrypted over HTTPS but not authenticated. It will delete your
image after an hour. So it's a good option if you're trying out a sample
project (like one of the Tilt examples).

## The Medium Way (for 1% of users)

In almost all cases, it's OK for a team to all share the same registry. 

Tilt uses content-based image tags, so you don't have to worry about one user
overwriting another users' images if they're pushing dev images at the same
time.

But in some exotic cases, organizations may set up a registry per developer or a
registry per team.

Fortunately, the Tiltfile `default_registry` system can be scripted to support this.

We're going to modify the `Tiltfile` to look for a file called `tilt_option.json` next to the Tiltfile. 

You can add more settings here (do different team members want different
services to behave differently? Put it in `tilt_option.json`). For now, we'll
expect the file to either be nonexistent, or JSON like:

```json
{
  "default_registry": "gcr.io/my-personal-project"
}
```

Add this code to the `Tiltfile`:

```python
settings = read_json('tilt_option.json', default={})
default_registry(settings.get('default_registry', 'gcr.io/shared-project-registry'))
```

Add a line to your `.gitignore`:
```
# personal tilt settings
tilt_option.json
```

Team members don't need to set anything, but new users can change it without
modifying the Tiltfile.

## Registries that are Special Snowflakes

### When Your Registry Has Multiple URLs

URLs on your laptop resolve differently than URLs in your cluster.

In some cases, the URL of a registry (as seen from your laptop) may be different
from the URL of the same registry (as seen from your clsuter).

For example, your laptop might push your image to `localhost:5000/my-image`,
while your cluster pulls the image from `registry:5000/my-image`.

Most modern cluster setup tools try to set up DNS to prevent this from
happening. But if you do hit this scenario (and you'll usually know if you are),
you can use the `host_from_cluster` parameter of `default_registry` to configure
the registry host as referenced from your cluster.

```python
default_registry(
    'localhost:5000',
    host_from_cluster='registry:5000'
)
```

### Elastic Container Registry's Repository Dance

The AWS container registry, ECR, forces you to create a
[repository](https://docs.aws.amazon.com/AmazonECR/latest/userguide/Repositories.html)
ahead of time for each image name.

For teams that use ECR, Tilt offers the option to push all your images to a
single repository in the registry.

```python
default_registry(
  'aws_account_id.dkr.ecr.region.amazonaws.com',
  single_name='my-team-name/dev')
```

Teams can have a shared repository, or a repository per developer:

```python
default_registry(
  'aws_account_id.dkr.ecr.region.amazonaws.com',
  single_name='%s/dev' % os.environ.get('AWS_USERNAME'))
```

## The Hard Way (for 0% of users)

We don't expect setting up a registry to be hard!

Every single cloud provider is working to make it as easy as possible (including
cloud non-providers like Replicated's [ttl.sh](https://ttl.sh) above).

If you're struggling to set up and authenticate to a registry, come [talk to
us](index.html#community) and a support engineer will point you in the right
direction.
