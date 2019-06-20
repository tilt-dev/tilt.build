---
slug: 12-gothamgo-talks-that-could-have-used-more-glitter
date: 2017-10-09T16:35:53.961Z
author: nick
layout: blog
canonical_url: "https://medium.com/windmill-engineering/12-gothamgo-talks-that-could-have-used-more-glitter-72ee38ae9d94"
title: "12 GothamGo Talks That Could Have Used More Glitter"
images:
  - featuredImage.png
  - 1*Xh2NMcuUBFQ81Yity29yRQ.png
tags:
  - software-engineering
  - go
  - golang
keywords:
  - software-engineering
  - go
  - golang
---

Windmill took our entire company to GothamGo last week. There are two of us. It’s a Go programming language conference in NYC. We both wanted to be there. It was an easy decision.

I took notes on many of the talks. Here’s a brief summary of each one, and what I learned.

## Day 1

Windmill sponsored a table! We’re not at the level of maturity yet where we know how to do “marketing” or “professional print services.” So we bought some poster board, markers, and glitter glue pens from the local art store, then made ourselves a shiny booth.

The downside was that I missed a few talks while sitting at the booth. Sorry if I missed yours!

### **“State of Go” by Steve Francia**

Steve bragged about how great Go is. He showed charts from Github, etc about how popular Go is. OK, I get it, we’re at a Go conference.

Then he transitioned into all the ways that Go has failed. For example, the Go team failed to appreciate how massive a problem dependency management would be, and how much a solution would need to integrate with the Go toolchain. But the slide that stuck with me was a screenshot of this section of “[Effective Go](https://golang.org/doc/effective_go.html#for)”:

![“Effective Go”’s explanation of the `for` loop](/assets/images/12-gothamgo-talks-that-could-have-used-more-glitter/1_P23lQP0ndbTt8cfLB1FdJg.png)*“Effective Go”’s explanation of the `for` loop*

Steve criticized the Go community for focusing so much on systems C programmers, accidentally excluding other groups and making them feel unwelcome. I thought about how hard it is to write great documentation: you want to leverage the reader’s existing background knowledge on many axes, without alienating readers who don’t have that knowledge.

### **“A Go Implementation of the Skylark Configuration Language” by Alan Donovan**

Alan has been working on [a Go implementation of Skylark](https://github.com/google/skylark), a configuration language for build systems. He talked about how “with great power comes great responsibility” as it applies to programming languages, and its converse, “with less power comes great optimizations.”

Skylark is more powerful than a JSON blob, but less powerful than a “real” language. The objects in each module are frozen after they’re loaded. A Skylark interpreter can load modules in parallel without worrying about race conditions. An interpreter written in Go is a great fit because it can cheaply create a goroutine for each module.

Alan also demonstrated it’s OK to give a talk at GothamGo that’s tenuously related to Go!

### **“Monitoring and Tracing Your Go Services” by Aditya Mukerjee**

Aditya’s talk built up a unified theory of service monitoring. We have three major ways to instrument the health of service. We have logs, which we can aggregate later. We have runtime metrics, which expose instant rollups of health stats (like number of 500s per sec). And we have traces, which allow us to visualize request flow across machines.

He gave a big shout out to logrus, the best walrus-themed logging library.

He showed sample code for instrumenting a service with all 3 types of monitoring. If you squint hard enough, it looks like we’re repeating the same code 3 times, for 3 different storage indexes. He’s optimistic about a [standard sensor format](https://github.com/stripe/veneur/tree/master/ssf) that covers all of them!

This talk reminded me of the old argument: “Figuring out the right indexing schema up-front is a pain!” vs “Our database runs faster with the right indexing!”

### **“Implicitly Impacting the Cloud with Go” by Kris Nova**

Kris’ talk was more a philosophical treatise.

“What is the Cloud?” she asked. Her glib answer is that it’s about making every API available as an HTTP API. She elaborated on how the HTTP API is full of useful technical conventions (like HTTP status codes) and cultural conventions (like expectations around trust and response latency and payload size.)

“Why is Go awesome?” she asked. Why is it so good for building cloud infrastructure? She gave props to the C interop. The Go team has spent tons of time and effort improving the syscall API. And the implicit interfaces mean you can have one massive struct implementing many APIs. In the same way that the web lets you implement APIs with a monolith server or lots of microservices, Go’s implicit interfaces make it easy to change how you divide your implementation between services.

With the movement towards infrastructure-as-code, we can think of the Cloud as anything that implements the [ResourceProvider](https://github.com/hashicorp/terraform/blob/master/terraform/resource_provider.go#L10) Go interface. This was pretty mind-bendy.

### **“From Frontend Engineer to Go Core Team Member” by Andrew Bonventre**

AndyBons described his personal arc from the Gerrit Code Review UI to Go. Even a systems programming language like Go needs UX expertise. He wrote it up as a blog post so you can read it directly:
[**Recognizing Value**
*A transcript of my talk at GothamGo 2017*writing.andybons.com](https://writing.andybons.com/recognizing-value-55969d1029d3)

He widened this into a discussion on communication barriers. Between two people from the same background, communication is easy. Between people from disparate backgrounds, those barriers grow exponentially. But all the best apps are the ones that synthesize many different areas of expertise into a cohesive interface, like [Apple’s Instruments](https://developer.apple.com/library/content/documentation/DeveloperTools/Conceptual/InstrumentsUserGuide/index.html) tool. To build cool stuff, we need to be putting tons of effort into making people from other backgrounds feel welcome and included and heard, lowering those barriers.

Even privileged white guys like us should be able to appreciate this!

## Day 2

On the second day, we wanted to hand out Windmill t-shirts. We forgot to print them. Off to the local art supply store! We came back with some blank white shirts and fabric markers, and let people make their own. We are too new to have branding guidelines so people used whatever colors they wanted.


Shout out to the awkward white dude in a suit who grabbed a blank shirt then ran away without talking to us! We love you all the same. Here are my notes from the second day’s talks.

### **“The Legacy of Go, Part 2” by Carmen Andoh**

Carmen told three personal stories: about her relationship with her husband, about Teach for America, and about raising her children. The stories were so personal that I’m blushing just thinking about summarizing them. I’m definitely not going to make wise-ass jokes about them.

Her message was that the legacy of Go is not the technology, but the community of people we build around it. She repeated a line from [Russ Cox](https://blog.golang.org/open-source): “Go needs everyone’s help. And everyone isn’t here.” But building a community isn’t scalable. The core Go team can’t do it alone. We need everyone in the community to practice everyday understanding and help each other.

It was the only talk that got a standing ovation.


### **“Performance Optimisation: How Do I Go About It?” by Kat Zień**

I adore any performance talk that’s experiment-based rather than superstition-based or memorize-these-magic-micro-optimizations-based.

In each example, Kat had a performance problem. She narrowed down the bottleneck with an appropriate perf visualization tool, then **wrote a test** to exercise the bottleneck, and finally used the test results to prove she had fixed the problem. Along the way, she sang the praises of [pprof](https://golang.org/pkg/runtime/pprof/) and [ReportAllocs](https://golang.org/pkg/testing/#B.ReportAllocs) and [flame graphs](http://www.brendangregg.com/flamegraphs.html) and [go-torch](https://github.com/uber/go-torch) and [benchcmp](https://godoc.org/golang.org/x/tools/cmd/benchcmp) and [go-wrk](https://github.com/adjust/go-wrk).

I’m looking forward to watching t[he Flame Graph talk](https://www.youtube.com/watch?v=nZfNehCzGdw) she recommended!

### **“Making Code Write Itself: How To Build Code Generation Tools in Go” by Bouke van der Bijl**

Bouke was unhappy that Go templates do so much reflection at runtime. So he wrote a tool that moves the reflection to compile-time!

If you pass his [statictemplate tool](https://github.com/bouk/statictemplate) a template and an argument type T, it will generate a Go function that takes T and prints the template. The function is faster and more type-safe than the standard templates.

I don’t know if these benefits are worth it for most apps. I wouldn’t expect template execution to be a performance bottleneck. But as an academic exercise, this was a cool way to unpack the internals of Go and the template system! Bouke took us on a tour of the template [parse tree](https://golang.org/pkg/text/template/parse/), how to use build tags to generate different dev and prod versions, and even how to play tricks on the linker that let you call private functions 🙈!

### **“I Will Debate Mark Bates About All of the Controversial Issues in Go”**
by Sean Kelly and Mark Bates
moderated by Cassandra Salisbury**

This was silly. Nothing of substance was discussed.

The debate was a set up to Cassandra’s Billy Madison homage. We wondered: do kids these days watch Billy Madison anymore? Was this joke a shibboleth to weed out the above-30s?

### **“Becoming a Go Contributor” by Kevin Burke**

Kevin wants you to know that contributing to Go isn’t hard as you’d think! Start small. Fix a typo. The Go team is always looking for ideas on how to lower the barrier to contributions. My favorite idea was [https://bit.ly/goscratch](https://bit.ly/goscratch), a sandbox repository where you can send dummy pull requests and the Go team will dummy review them.

Kevin observed that contributing free labor to Go would be even more attractive if Google wasn’t being a dick about [wage-fixing](https://en.wikipedia.org/wiki/High-Tech_Employee_Antitrust_Litigation) and [pay discrimination](https://www.nytimes.com/2017/09/08/technology/google-salaries-gender-disparity.html).

### **“Building a Multiplayer New York Times Crossword” by JP Robinson**

The NYTimes is building a multiplayer crossword game! JP described the high level architecture, which was a Who’s Who of Google Cloud services and the neat ways you can glue them together. The app builds on Firebase to store and synchronize state across multiple players. To make the app more responsive, they wrote the game state logic in Go, then used GopherJS and GoMobile to compile that logic to client code on web, Android, and iOS.

He let us play a demo, convincing everyone that multiplayer crosswords are total chaos.

![We are not good at this game.](/assets/images/12-gothamgo-talks-that-could-have-used-more-glitter/1_Xh2NMcuUBFQ81Yity29yRQ.png)*We are not good at this game.*

### **“Internals of the Go Internal Linker” by Jessica Frazelle**

This talk was like that OK Go video where they do an unbelievable stunt on one take across [eight treadmills](https://youtu.be/dTAAsCNK7RA) while singing power pop. Most of the talk was a single continuous, audacious live demo. She wrote a program that opened its own symbol table with `dlopen`, and called arbitrary functions by “string” name with `dlsym`. It was like she was writing bad JavaScript!

She passed a sampling of linker flags to the Go tool, used those flags to change the compiled executable, and ran `ldd` and `nm` to inspect the symbol tables in the compilation output.

Oh, and the font in the demo was a bit too small. Jessie gave a brief tutorial on how to fix font sizes on Linux by editing `.Xresources`.

Jessie claimed that she was not showing off deliberately.

## Closing Thoughts

Thanks to the neighboring booths for keeping us company upstairs: [MongoDB](https://mongodb.com), [BugSnag](https://www.bugsnag.com/), and [Datadog](https://www.datadoghq.com/). The MongoDB guys gave me a webcam cover, an ingenious piece of swag.

I’ll update this post with video links once the recordings are out.

We were mainly at the conference to meet potential engineers to be a part of our team. If you’re interested in working together, [come talk to us](https://windmill.engineering/jobs/).

We appreciated the love that so many people tweeted at us! We hope to see you next year!
