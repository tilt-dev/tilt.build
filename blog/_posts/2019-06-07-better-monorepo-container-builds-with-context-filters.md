---
slug: better-monorepo-container-builds-with-context-filters
date: 2019-06-07T15:12:49.521Z
author: dmiller
title: "Better Monorepo Container Builds with Context Filters"
layout: blog
canonical_url: "https://medium.com/windmill-engineering/better-monorepo-container-builds-with-context-filters-94717ecdb7a3"
image: featuredImage.png
image_caption: My Docker contexts, visualized
tags:
  - docker
  - kubernetes
  - devops
  - development
  - programming
keywords:
  - docker
  - kubernetes
  - devops
  - development
  - programming
---

If your project has multiple microservices in one git repo, Docker builds can be frustrating.

Changing a file that’s only used in one service can cause a slow image build in another service. If you’re using a tool like Tilt that builds each time you save a file that same save now kicks off multiple builds. Your workflow shouldn’t be slower just because of how you organize your code.

You can now eliminate slow and spurious rebuilds by using Tilt’s new context filters. Let’s look at an example, but basically this is a Tiltfile with 4 services built from the same context so they can share code.

## Example

Let’s look at an app with 4 services:

* frontend

* shopping_cart

* users

* fulfillment

The repo has code for each in a directory, common code for your app, and vendored dependencies:

* `common/`

* `frontend/`

* `shipping/`

* `cart/`

* `users/`

* `vendor/`

The simple Tiltfile looks like

```
docker_build(‘frontend’, ‘.’, dockerfile=’Dockerfile.frontend’)

docker_build(‘cart’, ‘.’, dockerfile=’Dockerfile.cart’)

docker_build(‘users’, ‘.’, dockerfile=’Dockerfile.users’)

docker_build(‘shipping’, ‘.’, dockerfile=’Dockerfile.shipping’)
```


When you change a file in the users service, Tilt rebuilds every image (because it’s in the context `.`). This causes extraneous rebuilds and wastes time.

`.dockerignore` solves this problem on a per directory basis. However, if you want to exclude a directory only from *some* builds you’re out of luck. This is what Tilt’s new context filters enable.

## Per-Image Context Filters

With the `only`context filter you can specify which patterns should trigger a build.

```
docker_build(‘frontend’, ‘.’, dockerfile=’Dockerfile.frontend’, only=[‘frontend’, ‘common’, ‘vendor’])

docker_build(‘cart’, ‘.’, dockerfile=’Dockerfile.cart’, only=[‘cart’, ‘common’, ‘vendor’)

docker_build(‘users’, ‘.’, dockerfile=’Dockerfile.users’, only=[‘users’, ‘common’, ‘vendor’])

docker_build(‘shipping’, ‘.’, dockerfile=’Dockerfile.shipping’, only=[‘shipping’, ‘common’, vendor’)
```


Now when we change a file in the users service, only the user service rebuilds. But when we change a common file, all the services rebuild.

We can tidy up our Tiltfile with a helper function:

```
def service_build(name):

docker_build(name, ‘.’, dockerfile=’Dockerfile.’+name, only=[name, ‘common’, ‘vendor’]

service_build(‘frontend’)

service_build(‘cart’)

service_build(‘users’)

service_build(‘shipping’)
```


## Tools Shouldn’t Care How You Organize Your Code

If you’re using a monorepo with multiple microservices now is a great time to [give Tilt a spin](https://docs.tilt.dev/install.html). We’ve designed Tilt to work with any setup, any architecture, no matter how complex. If you have a funky architecture [get in touch](https://tilt.dev/contact) and we’ll show you how to get Tilt up and running.
