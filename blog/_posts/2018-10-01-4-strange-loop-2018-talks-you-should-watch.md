---
slug: 4-strange-loop-2018-talks-you-should-watch
date: 2018-10-01T15:00:40.627Z
author: dmiller
layout: blog
canonical_url: "https://medium.com/windmill-engineering/4-strange-loop-2018-talks-you-should-watch-ccb181fec53c"
title: "4 Strange Loop 2018 Talks You Should Watch"
image: featuredImage.jpeg
tags:
  - programming
  - conference
  - strangeloop
  - programming-languages
  - talks
keywords:
  - programming
  - conference
  - strangeloop
  - programming-languages
  - talks
---

[Strange Loop](https://thestrangeloop.com/) is the only conference I’ve ever been back to. It has a great balance of academic and industry talks aimed at the practitioner with a healthy strain of artistic whimsy running through it all. Here are five talks that I’ve been thinking about since the conference ended:

## Rosie Pattern Language

This is the talk that I am most excited to apply to my daily work. [Rosie](https://gitlab.com/rosie-pattern-language/rosie) is a modern version of Regular Expressions. It has a lot of cool features, but these three are what sold it to me:

1. Rosie reads like a programming language, which means that it *diffs* like a programming language.

2. Comments! Finally you can explain all the different parts of your regex.

3. Modules! `import date` does exactly what you think it does

<div class="block block--video">
<iframe width="560" height="315" src="https://www.youtube.com/embed/MkTiYDrb0zg" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>

## All the Languages Together

There are a lot of programming languages out there, especially if you include domain-specific languages like regex. Right now there are two common ways you use multiple programming languages together: foreign function interfaces (FFI) and microservices. Both of these can be really painful. So painful, in fact, that at Windmill we’re actively working on making microservices development easier. This talk shows us a better way to mix programming languages in one system using type-preserving intermediary representations.

<div class="block block--video">
<iframe width="560" height="315" src="https://www.youtube.com/embed/3yVc5t-g-VU" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>

## Hazel

At Windmill we focus on the “inner loop” of development: that under-explored space where a programmer is typing, compiling, deploying and restarting rapidly in an attempt to change the behavior of a system. [Cyrus Omar](http://www.cs.cmu.edu/~comar) showed how our typical inner loop tools (compilers, type checkers, IDEs, etc) fall apart when the program has a syntax error or is incomplete. “Typed holes” take the place of these incomplete parts of your program to allow static (type checker, automated refactors) and dynamic (debuggers) tools to continue to function. [Hazel](http://hazel.org/) is a programming environment which implements typed holes.

<div class="block block--video">
<iframe width="560" height="315" src="https://www.youtube.com/embed/UkDSL0U9ndQ" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>

## A Tale of Two Asyncs

My favorite talk of the conference. Ashley Williams covers the technical and philosophical differences between node.js and Rust’s approaches to asynchronous programming. What really put this talk over the top were her thoughts on what it means for a programming language to have a *vision*.

<div class="block block--video">
<iframe width="560" height="315" src="https://www.youtube.com/embed/aGJTXdXQN2o" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>
