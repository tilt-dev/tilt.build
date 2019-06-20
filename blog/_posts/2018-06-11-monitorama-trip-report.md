---
slug: monitorama-trip-report
date: 2018-06-11T22:36:07.318Z
author: dmiller
layout: blog
canonical_url: "https://medium.com/windmill-engineering/monitorama-trip-report-cc07f3356eda"
title: "Monitorama Trip Report"
image: featuredImage.jpeg
tags:
  - devops
  - monitoring
  - observability
  - conference
  - monitorama
keywords:
  - devops
  - monitoring
  - observability
  - conference
  - monitorama
---

Monitorama was a 3 day conference held in Portland, Oregon that describes itself as an “Open Source Monitoring Conference Hackathon”.

I attended the 2018 edition and wanted to talk about a few talks that stood out:

## Day 1

**“Optimizing for Learning” by [Logan McDonald](https://twitter.com/loganmeetsworld)**

This was the first talk of the conference and it set a great tone. This talk centered on onboarding and emphasized that onboarding is all about how we learn. A couple key takeaways:

* When information is transparent and available in your org, certain kinds of beginners can succeed. Make this information available!

* Encourage low stakes “testing”: try things out in a low stakes environment before doing them for “real”. Whether this is a coding concept, or being on-call, people learn better in low stakes environments.

* “Observable” systems lead to more easily onboarded systems. If, for every input there is an output then it is easier to build a mental model of the system *experimentally*.

* Symmathesy is a cool word: basically means “the ways that we learn together, as a system”.

**“On-Call Simulator” by [Franka Schmidt](https://twitter.com/franschm)**

Speaking of teaching and onboarding, this talk was about using games to teach people how to be on call. This talk also emphasized how learning is better in low stakes, safe spaces. Games are great for that!

Other things Mapbox uses besides games are:

* Buddy system! Every person going in to on call gets paired with a buddy. At first they just shadow the on-call person, sit with them, look at graphs, run commands etc. Later the more experienced buddy is shadowing them.

* Onboarding bucket list: basically a checklist to measure onboarding progress. Contains things like: “Get woken up by an alert” or “Update status page”.

It’s important to have a culture of helping people check things off their list so they can get onboarded as quickly as possible.

Franka built games based off of past detailed postmortems. They were simple text adventures so that they would be easy for others to build. She did user research on her coworkers after they played the game asking them what about the game made it feel real or made it feel fake to make sure that the games were valuable. I don’t think we do enough practicing as an industry and I’m looking forward to trying this out in my work.

**“Reduce Alert Fatigue” by [Aditya Mukerjee](https://twitter.com/chimeracoder)**

My big takeaway from this talk was actually not about alert fatigue at all, but decision fatigue! [Decision fatigue](https://en.wikipedia.org/wiki/Decision_fatigue) is when the frequency or complexity of decision points causes a person to make mistakes or avoid decisions altogether. I think this is very applicable to what we’re trying to do at Windmill. We want to help people avoid decision fatigue in developer tools.

Alert fatigue deals with the *observability* of systems whereas decision fatigue deals with the *controllability* of systems. In other words the more observable your system is, the more chances for automated alerting. Similarly decisions result from controllability. The more controllable your system is (feature flags, load shedding, horizontal scaling) the more you run the risk of decision fatigue as you decide which of the many knobs that you should turn during a degradation.

It is important to not just reduce the frequency of alerts, but also the complexity in reacting to them.

## Day 2

**“Next-Generation Observability for Next-Generation Data: Video, Sensors, Telemetry” by [Peter Bailis](https://twitter.com/pbailis)**

This was one of my favorite talks of the conference. Peter Bailis is working on a [team at Stanford](https://dawn.cs.stanford.edu/) that is trying to make machine learning more accessible by reducing the actual monetary cost of running machine learning jobs.

This has happened before with search. Search used to be a hard thing that only large, well-funded engineering teams could accomplish well. Now anyone can drop Solr or Lucene in to their project and have a great search experience. Let’s bring that to machine learning.

He used the example of video analysis throughout the talk. Right now video analysis is very expensive to do because videos have lots of frames and you’re running a computation on every frame of the video. If this became cheap then small conferences like this one could set up cameras to know, in real time, how any people are in the auditorium and how many people are in the hallway track.

There are two technique he uses to speed up execution of these jobs:

* **Query-specific locality**: If we’re only detecting people from one angle (a fixed camera position) then we don’t need a general model, we can specialize it. It’s like a JIT compiler but for machine learning: generate a model that only looks for and at the things we care about. This results in 10k fewer flops and 300x faster execution on GPU. Think lossy compression but for neural networks.

* **Temporal locality**: “When did someone pass through this door?”
Frames close in time are often redundant. Train a small model to filter out redundant frames. This difference detector can run at 100k FPS on a CPU.

Roll all of these optimizations up in to something they call “NoScope”. You can think of NoScope as a query planner for machine learning where at each stage it is figuring out the cheapest model to run. Now we have an accuracy vs speed model that we can tune, too.

**“Reclaim your Time: Automating Canary Analysis” by [Megan Kanne](https://twitter.com/megankanne)**

I’ve always loved the idea of canary deploys and this talk taught me a bunch of new things about how to do them effectively.

[Canary deploys](https://www.infoq.com/news/2013/03/canary-release-improve-quality) are the idea that, instead of deploying your new version to 100% of customers almost instantly, deploy the new version to a small percentage of customers and see if anything “goes wrong”.

She introduced us to two aspects of canary deploys that I wasn’t aware of:

* Deploying a new version of your code one host in your production cluster probably isn’t a good idea: what if a bug only surfaces when multiple nodes with the new version of your code interact? Instead deploy a canary *deployment* of your cluster and route traffic to is using a proxy (or multicasting to a proxy to reduce latency).

* But don’t have only new versions in your canary cluster, make sure to have old nodes with a lot of uptime in there too to remove the variable of uptime (JITing, etc).

Megan advocated using visual pattern matching to see if a canary build is healthy, but you can also compare HTTP responses, and use machine learning! She introduced us to “Median Absolute Deviation” which I didn’t really understand, but basically when certain metrics about a canary deploy exceed a certain threshold the deploy is automatically failed.

Prior art for Twitter’s system is [Kayenta](https://cloudplatform.googleblog.com/2018/04/introducing-Kayenta-an-open-automated-canary-analysis-tool-from-Google-and-Netflix.html), which does automated canary analysis via Mann-Whitney U Test at Netflix.

They’re also running a canary deploy **per** pull request.

## Day 3

**The Present and Future of Serverless Observability by [Yan Cui](https://twitter.com/theburningmonk)**

I didn’t take very detailed notes here because I was in a [Pok Pok](https://pokpokdivision.com/) food coma for the second day in a row, but I got really excited about the future that the speaker described at the end.

After talking about the current state of the art for serverless monitoring, Yan moved in to what he would like to see happen. An interesting property of serverless is that it’s easy to visualize your requests as a series of function calls. The speaker even showed a video of visualizing all requests flowing through a system in WebGL using [Vizceral](https://github.com/Netflix/vizceral).

I thought there were a lot of parallels to be drawn between serverless observability and “build system observability”. Being able to visualize your build as a graph and click on a line connecting two nodes to see the operation that lead to that version of the filesystem would be helpful for diagnosing build issues. It seems to me that build systems are not at all “observable” by modern standards.

## **Random Takeaways Overall**

* People don’t like YAML.

* Services should hot reload configs and not crash if the config is malformed.

* Portland is a great place to spend a week!
