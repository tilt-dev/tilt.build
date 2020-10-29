---
slug: "load-dynamic"
date: 2020-11-03
author: nick
layout: blog
title: "Load Dynamic"
subtitle: "Or: How Build Tools Grow"
image: "/assets/images/load-dynamic/briggs_house.jpg"
image_caption: "Chicago used to load their buildings at runtime. <a href='https://commons.wikimedia.org/wiki/File:Briggs_house.jpg'>Photo from the Chicago Historical Society via Wikipedia.</a>"
tags:
  - tilt
  - bazel
---

If you have more than one service, you probably need to share some common
functions and constants between services.

The way we solve this in Tilt is with two primitives: `load()` and
`load_dynamic()`. They have slightly different syntaxes.

Load is static: it takes a literal string, and loads new variables into the
current scope. Here's how you load a helper function `create_namespace`:

```
load('./lib/Tiltfile', 'create_namespace')
create_namespace('frontend')
```

LoadDynamic is...well...dynamic! It's an imperative function that takes a string
as input, and returns a dictionary of values:


```
values = load_dynamic('./lib/Tiltfile')
create_namespace = values['create_namespace']
create_namespace('frontend')
```

This is helpful if you want to load Tiltfiles in all subdirectories, to
determine the files to load at runtime, or to simply inspect the choices of what
you can load:

```
values = load_dynamic(os.path.join(base_dir, 'Tiltfile'))
print(values)
```

If you want more detail on how to use them, head on over to [the Tilt API
reference](https://docs.tilt.dev/api.html#api.load_dynamic).

## Why do you need an imperative load_dynamic()?

You may wonder why we have two ways to load files.

A simple explanation is that `load_dynamic()` is more flexible, but `load()` is a
shorter syntactic sugar for the 90% case.

But the longer, more complicated explanation has a long history!

Let's zoom out a bit.

A few years ago, I wrote a blog post ["Bazel is the Worst Build System, Except
for all the
Others"](https://medium.com/windmill-engineering/bazel-is-the-worst-build-system-except-for-all-the-others-b369396a9e26). I
wrote this:

> The build language of the future will be imperative. Novice programmers should
> be able to pick it up easily. The language should help them to visualize the
> results.

Antonio D'Souza wrote [this
reply](https://medium.com/@quikchange/this-may-not-be-wise-ebeeb8b5e578):

> This may not be wise. Google once allowed imperative build rules but they
> eventually grew too complex to wrangle and had to be phased out painfully.

I've been thinking about this comment for two years! Because it really gets at
the core question of how Bazel[^1] got traction at Google, and how it's doing
outside Google.

I was not on the Bazel team. But I remember working with them when they were first
rolling it out inside Google.

Bazel was a drop-in replacement for gconfig, a Python-based system for
generating Makefiles.

When Bazel rolled out, here was the plan:

1) Everybody make sure your gconfig BUILD files obey a SUPER strict subset of Python.

2) Bazel will tell you if you did it right, and you can use gconfig or Bazel during the transition.

3) If you did it right, Bazel will run your build WAY faster.

And when I say SUPER strict, as I remember it, that meant only function calls
were allowed: no local variables and no loops, for example.

They would have been fine with `load()`, but not with `load_dynamic()`.

But when they tried to roll it out, they hit reality hard. Because there was simply no way
to express most builds with this strict subset of Python and small feature set.

They introduced a new directive you could add to your config file:
`PYTHON-PREPROCESSING-REQUIRED`. That told Bazel to let your code use some
"normal" python. This was a stopgap until Bazel had all the features they needed
to support complex builds. Then they went back and phased out all the old
`PYTHON-PREPROCESSING-REQUIRED` stuff.

## The trade-off of load() vs load_dynamic()

Tiltfiles (Tilt's configuration files) are written in
[Starlark](https://github.com/bazelbuild/starlark), the same underlying
configuration language as Bazel.

`load()` is a core feature of Starlark. `load_dynamic()` is not.

There's certainly a camp of people that believe supporting imperative Python in
build systems was a huge mistake. It made rollout easier, but the pain of
phasing it out was not worth the benefits of making rollout easier.

I'm not convinced that it's a simple either/or. The pendulum swung back and
forth a few times. Early Bazel had a lot of "imperative" features that made it
easier to adopt, and easier to integrate with other tools. Once Google adopted
Bazel entirely, the Bazel team didn't need Python pre-processing anymore, and
removed it.

<figure>
<blockquote class="twitter-tweet"><p lang="en" dir="ltr">A periodic &quot;WHYYYYYYYYY BAZELLLLLLL?!&quot;.</p>&mdash; Stephen Augustus (@stephenaugustus) <a href="https://twitter.com/stephenaugustus/status/1318721602050269184?ref_src=twsrc%5Etfw">October 21, 2020</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script> 
  <figcaption>To be fair, I don't think Stephen and I are complaining about the same
    things, but I saw myself in this tweet.</figcaption>
</figure>

I don't blame them for removing it! They made Bazel harder to
optimize, which is critical for a large codebase like Google's.

`load()` vs `load_dynamic()` in Tilt has the same trade-off.

We see this pattern often when teams investigate Tilt. 

Their initial proof of concept loads files and runs shell commands synchronously, because
that interoperates well with their existing tools.

Over time, this approach gets slower and harder to parallelize, so they refactor
to use functions that are more declarative and asynchronous.

Long-term, `load()` is easier for us to optimize and parallelize. But don't feel
guilty if you reach for `load_dynamic()` to get started! You can always come
back and refactor if you need to. We're experimenting with tools to help you
better measure your builds and determine when to make these trade-offs. Stay tuned!

[^1]: To be precise, Blaze is the name of Google's internal build system, and
    [Bazel](https://en.wikipedia.org/wiki/Bazel_(software)) is the name of the
    open-source part. In this post, we use Bazel/Blaze interchangeably to avoid
    confusion.  The part we care about here (the configuration language,
    Starlark) isn't meaningfully different between them.

