---
slug: github-propelled-git-to-escape-velocity
date: 2018-06-04T17:34:46.001Z
author: dan
layout: blog
title: "GitHub propelled Git to escape velocity"
images:
  - featuredImage.jpeg
tags:
  - github
  - git
  - mercurial
  - devops
keywords:
  - github
  - git
  - mercurial
  - devops
---

[Microsoft + GitHub](https://blogs.microsoft.com/blog/2018/06/04/microsoft-github-empowering-developers/)! Is it more [Chocolate + Peanut Butter](https://www.youtube.com/watch?v=DJLDF6qZUX0) or [Dogs + Cats](https://www.youtube.com/watch?v=JmzuRXLzqKk)? Hot Take Tuesday falls on Monday this week:

* HackerNews is full of [Sound](https://news.ycombinator.com/item?id=17229848) and [Fury](https://news.ycombinator.com/item?id=17226225), signifying nothing.

* [GitLab](https://news.ycombinator.com/item?id=17223116) usage is skyrocketing.

* SourceForge abides.

* Glitch says it’s good (I agree!) and [outlines a new vision for social coding](https://medium.com/glitch/github-glitch-and-the-future-of-social-coding-5e6faa45c8f2).

Adding my congratulations seems insufficient; I’ll try to provide a hot take. Conventional Wisdom is GitHub succeeded because it made good bets (on Ruby as community and git as source control).

I think GitHub’s key bet was forking, and it was so successful that GitHub spread git to new developers.

![Spongebob Squaregit](/assets/images/github-propelled-git-to-escape-velocity/featuredImage.jpeg)*Spongebob Squaregit*

## My History at Google Code

I saw GitHub’s early years from working at Google. In 2009, I was on the Open Source team and Google Code Project Hosting (aka code.google.com) [added Mercurial support](https://www.youtube.com/watch?v=ri796Hx8las) to their original Subversion backend. It seemed like a reasonable bet: Mercurial had a nicer interface, better Windows support, and a wire format more compatible with Google’s request routing infrastructure.

In 2011, I started managing Google Code. It was clear that GitHub was making open source development easier. Was it because git was more popular? We added git support (as did Kiln and Bitbucket). But GitHub was more than Git.

## Pull Requests Encourage Contribution

Open Source projects on Sourceforge and Google Code felt Professional. They had owners and issue tracking and workflows and releases. If I wanted a new feature, it felt intimidating to imagine running the gauntlet of contributing. In many cases, this intimidation was unfair because the “Owner” was one person who would have loved help.

Pull Requests were the easiest way to submit a code review. No new tools to install, no separate UI to navigate. Pull Requests made you feel like your voice mattered.

Pull Requests get the credit as GitHub’s big innovation, but this misses the bigger barrier that GitHub broke.

## Fork Doesn’t Have to Be a Four-Letter Word.

GitHub reduced the hassle if your Pull Request was rejected (whether for a good reason or just ignored). Step 1 of making a Pull Request is to make a Fork.

Before GitHub, a Fork was an insult. “You’re so unreasonable I’m taking my toys and going home.” GitHub made it a way of life.

A rejected Pull Request isn’t a big deal if you have a fork. And it doesn’t rule out a later merge. And who knows, maybe your fork will end up becoming the most popular.

Code Review is great, but I’m an ex-Googler, so of course I think that. What really drives collaboration is freedom to try, fail, and move forward. Forking normalized that way more than Pull Requests. GitHub made it accessible and acceptable.

## Git allowed the workflow; GitHub made it popular

This freedom to fork wasn’t built-in to git; other hosts offering git didn’t enable this workflow. (Conversely, GitHub could have built this on Mercurial)

Developers didn’t flock to git because it powered the biggest projects (Linux or gcc). They flocked to get their next project done, which was may more likely to need to change a library like “twitter-oauth-client-ruby”.

GitHub helped Git more than Git helped GitHub.

## My story, continued

At Google Code, we realized that GitHub was great and the world didn’t need us to be another GitHub. Since then, Social Coding has grown further. Glitch is upgrading “Forking” into “Remixing”. Editors like Jetbrains and VSCode are bringing real-time collaboration to IDEs.

I moved to other projects. Google Code shut down (with lots of work to make it easy to migrate archives). But I kept thinking about how to make game-changing developer tools.

The next frontier is the part of development before source control; the workflows locked up in individual developers’ shell histories/brains. It’s hard to understand what files feed into which build commands that necessitate restarting which microservices. Who knows what files are created by which steps that could be parallelized/moved to the cloud?

We at Windmill call this Live Development: showing you the Illuminating Output that will move you forward. You spend more time in your workflow than in your source control; workflow tools can make a bigger difference than source control tools. Interested? [Sign up to be a Fan](https://medium.com/windmill-engineering/windmill-fan-program-a4c0066c356d) and we’ll let you in on all our secrets.
