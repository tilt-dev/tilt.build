---
slug: how-i-built-a-simple-static-jekyll-site-without-installing-ruby-a-rant
date: 2019-02-18T05:41:05.350Z
author: nick
layout: blog
title: "How I Built a Simple Static Jekyll Site Without Installing Ruby: A Rant"
tags:
  - docker
  - build-system
  - containers
  - jekyll
keywords:
  - docker
  - build-system
  - containers
  - jekyll
---

Sometimes I have to make a static website.

It’s 2019. There are great tools to help build static websites. They let you write the content in Markdown and style with SCSS.

I want to try [Jekyll](https://jekyllrb.com/). It looks cool.

I read the [install instructions](https://jekyllrb.com/docs/).

The first step says:
> Install a full [Ruby development environment](http://Ruby development environment)

No

No no no no no no no

**Nooooooo**

Why?

Ruby is fine. If you like Ruby, that’s great! But I don’t want a new language dev environment. I don’t want to install Ruby on every machine I own. I don’t want to keep Ruby up to date. I don’t want to install `rvm` when I inevitably have a version conflict.

When you get furniture from Ikea, do the instructions say:

“Step 1: Install a drill press on your table and subscribe to *Drill Press Monthly Magazine*”

I like drill presses too but I don’t want one on my table.

### How I Create the Site

But I am fine installing Ruby if it’s isolated in a container.

Can I build this static site in a container? This seems like a fun challenge.

First I need to create a Ruby container with a shell.

```
$ docker pull ruby
$ docker run --name my-jekyll-env -it ruby sh
```


That opens a terminal in the container.

```
# gem install jekyll bundler
...
# jekyll new src
Running bundle install in /src...
...
New jekyll site installed in /src.
```


Now I’ve got a container with the auto-generated new site.

I can exit out of the container and copy the source code out like this:

```
# exit
$ docker cp my-jekyll-env:/src .
$ docker rm my-jekyll-env
```


Success!

```
$ ls src
404.html  about.md  _config.yml  Gemfile  Gemfile.lock  index.md  _posts  _site
```


Now I have the beginnings of a Jekyll site without installing Ruby.

### How I Make Changes to the Site

I have a separate container for running the Jekyll server. Docker mounts are a good way to share these source files with the container.

Here’s what the Dockerfile looks like:

```
FROM ruby:2.6
RUN gem install jekyll bundler
WORKDIR /src
ENTRYPOINT bundle update && bundle exec jekyll serve \
  --host 0.0.0.0 --config _config.yml
```


It starts with the Ruby environment above. The container runs the `jekyll serve` command that automatically picks up any changes to source files.

Then I run it with:

```
docker build -t my-jekyll-env -f Dockerfile .
docker run --name my-jekyll-env \
  --mount type=bind,source=$(pwd)/src,target=/src \
  -p 4000:4000 \
  -it \
   my-jekyll-env
```


The `--mount` flag shares my local files with the container.

The `-p` flag automatically forwards port 4000 outside the container to port 4000 inside the container.

The `-it` flag connects my terminal to the server, so that I can use Ctrl-C to quit.

And that’s it! I have a full Jekyll environment without installing Ruby.

### Disclosure

I work on Tilt. Tilt is a development environment for building services in containers. The site I built is [https://tilt.dev/](https://tilt.dev/). It’s hosted on [Netlify](https://netlify.com/) (yay Netlify!) and is only [a little bit more complicated](https://github.com/windmilleng/tilt.build) than the starter site described above.

You’re probably saying “Oh! He’s a hype man for containers. He’s trying to sell me something.”

But you have the causality reversed! The reason I work on Tilt is because reproducible dev environments are a problem worth solving, and containers seem like a plausible way to solve them.

I don’t care if you use [Docker Compose](https://docs.docker.com/compose/) or [Bazel](https://bazel.build/) or [Buck](https://buckbuild.com/) something else. It’s about getting to a local dev environment that’s on any computer, wherever you are.

The machinery can be overwrought and fussy. You need an opinionated way to:

* Create the environment (where? in a VM? in an OS sandbox?)

* Put input files inside (how? rsync? symlinks? mounts?)

* Get artifacts out

* Keep the environment alive when you’re using it and put it to sleep when you’re not

The Bazel team has thought about this more than anyone I know. But I want to see more tools in this space!
