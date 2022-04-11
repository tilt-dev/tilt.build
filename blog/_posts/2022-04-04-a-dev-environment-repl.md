---
slug: "a-dev-environment-repl"
date: 2022-04-04
author: siegs
layout: blog
title: A REPL for your dev environment
image: /assets/images/a-dev-environment-repl/curly.jpg
image_caption: '"Curly" by <a href="https://www.flickr.com/photos/gammaman/6212822745/">Eli Christman</a>'
description: How Tilt can power experimentation and a fast feedback loop
tags:
- repl
- development
- dev environments
- devtools
---
Many of us started programming with a REPL (Read-Eval-Print-Loop), whether we knew it at the time or not. (My own introduction came via Logo and Basic on the Apple II.) The thrill of entering obscure abbreviations and commands into the computer and receiving instant feedback can be a big dopamine hit. It can feel like playing a game with infinite lives, where you always have another chance to slay the boss 🐉. 

REPLs encourage experimentation and learning by efficiently providing a tight feedback loop (almost literally; the PL in REPL being "Print Loop", where "print" serves as the feedback mechanism). Tilt, as a tool for scripting and assembling development environments, is all about tight [feedback loops][controlloop]. What do REPLs and Tilt have in common, and can we use Tilt like a REPL?

Good REPLs help with exploration by providing completion and context awareness, and always reflecting the result back to you. Here's a simple example in Ruby:

![Ruby IRB Fibonacci example](/assets/images/a-dev-environment-repl/irb-fib.gif)

Some languages use REPLs as the focal point for writing code (see Smalltalk, and to an extent, any member of the Lisp family), while others (C/C++ and many compiled languages) don't come with any built-in REPL at all. More recently, online services let you try a language or share runnable snippets without having to download any software at all (see [Ruby][tryruby], [Go][goplay], and [JavaScript][repljs]).

Tilt responds to changes in your environment when you modify your files in the same way that the REPL snaps to action when you hit ENTER. One of the events Tilt responds to is changes to the `Tiltfile`, Tilt's own [Starlark][starlark]-based configuration file. With a little creativity and flexibility, we can run Tilt in a terminal inside or next to our editor (`tilt up --stream`) and mimic the feedback and responsiveness of a REPL:

![Tilt Fibonacci example](/assets/images/a-dev-environment-repl/tilt-fib.gif)

The result is a loop that feels surprisingly responsive: write a bit of code, hit `Ctrl-S` or `⌘-S`, and see the result! If you're exploring Tilt and haven't used Starlark (or Python, Starlark's parent language), this can be a great way to fool around and get your bearings with `Tiltfile` syntax or builtins.

You may have noticed Tilt complaining at the end of the loop about "No resources found". We implemented and ran a Fibonacci function in Starlark, but didn't give Tilt anything else to do. Tilt primarily wants to build and run things for you; Starlark is the flexible medium through which you describe what to run and build. Tilt is that eager puppy that will keep fetching the ball, though finding it unsatisfying and wishing it was a bone to chew on instead. 

It's at this point in the experimentation phase where it helps to view Tilt as a [replacement for Bash](/2018/12/05/tilt-is-the-start-sh-script-of-my-dreams.html) or your command-line shell of choice. Think about activities you normally would type into your shell and see if you can wire them into your `Tiltfile` and have Tilt run them for you. For example, maybe you're sitting down at the keyboard at the beginning of your work day and would normally use `git` to pull new changes to your code. Instead, create a `local_resource` to do it for you:

```python
local_resource("update-code", "git pull")
```

Tilt responds with:

```
Initial Build
Loading Tiltfile at: /Users/nicksieger/tilt-dev/tilt-avatars/web/Tiltfile
Successfully loaded Tiltfile (413.333µs)
  update-code │
  update-code │ Initial Build
  update-code │ Running cmd: git pull
  update-code │ Already up to date.
```

Now Tilt will pull code for you when you `tilt up`. [Resources][resources] are Tilt's unit of work; in the case of a `local_resource`, it's a command to run on your local machine. Resources are stateful in that Tilt looks for changes to them every time the `Tiltfile` is executed. So you can also experiment and iterate on resources; if Tilt detects relevant differences, it will re-execute the resource. Say that you find that `git pull` is not quite what you want Tilt to do; instead, you want some conditional logic to check if you have a clean working copy and only pull new changes then. You can change the `update-code` resource, all while Tilt is running:

```python
script = """
if [ "$(git status -s)" ]; then
	echo "You have local changes:"
	git status -s
else
    echo "Pulling latest code:"
	git pull
fi
"""
local_resource("update-code", script)
```

Tilt says:

```
1 File Changed: [Tiltfile]
Loading Tiltfile at: /Users/nicksieger/tilt-dev/tilt-avatars/web/Tiltfile
Successfully loaded Tiltfile (1.407958ms)
  update-code │
  update-code │ 1 File Changed: [Tiltfile]
  update-code │ Running cmd: sh -c "if [ \"$(git status -s)\" ]; then\n\techo \"You have local changes:\"\n\tgit status -s\nelse\n    echo \"Pulling latest code:\"\n\tgit pull\nfi"
  update-code │ You have local changes:
  update-code │ ?? Tiltfile
```

Moving on, let's say you're working on a JavaScript project, and the next thing you tend to do is check if `package.json` had any updates, then you remind yourself that you need to run `yarn install` to pick up any new updates. Let's create a resource for that too:

```python
local_resource("dependencies", "yarn install")
```

However, Tilt is designed to be responsive to changes in your environment. For a local resource, the `deps` argument tells Tilt which file changes should trigger the resource to be re-executed:

```python
local_resource("dependencies", "yarn install", deps=["package.json", "yarn.lock"])
```

With this change, the next time you pull or make changes to `package.json` while Tilt is running, Tilt will run `yarn install` for you.

Of course, if your app runs as a Node.JS server as well, that can be added to the resource with a `serve_cmd`. Now the resource is handling more than dependencies: it's [building and running the app][snip].

```python
local_resource(
  'local-js-server',
  cmd='yarn install',
  deps=['package.json', 'yarn.lock'],
  serve_cmd='yarn start'
)
```

Again, all of these changes can be applied while Tilt is running, and you can see Tilt take action immediately:

![Tilt up JavaScript project](/assets/images/a-dev-environment-repl/tilt-up-js.gif)

### Summary

While Tilt is great at managing your dev environment when the `Tiltfile` is fully baked, don't sleep on the idea of using Tilt and the `Tiltfile` in a more dynamic way to experiment with your project. In addition to building and running servers, Tilt can also run tests, linters, debuggers, and other tools alongside your development servers. Using the [recently-released][catalog] [disable resources feature][disable], you can add resources for these features such that you can enable them when needed, and they won't get in the way of existing workflows.

If you and your team already have a `Tiltfile` in source control and you want to encourage more customization and experimentation, consider adding some code to check for and include a `local.tiltfile` to allow individual developers to experiment with Tilt:

```python
if os.path.exists('local.tiltfile'):
    load_dynamic('local.tiltfile')
```

Looking for ideas on where to go from here?

- Read more on options to [manage multiple applications/repositories with Tilt][repos].
- Browse [our library of snippets][snippets] for more things you can do in your `Tiltfile`.
- Use our [hot-off-the-presses][extweet] [VS Code extension][vscode] (featured in the gif videos above) to help you write `Tiltfile`s!

[tryruby]: https://try.ruby-lang.org/
[goplay]: https://go.dev/play/
[repljs]: https://repljs.com
[controlloop]: {{site.docsurl}}/controlloop.html
[starlark]: https://bazel.build/rules/language
[resources]: {{site.docsurl}}/tiltfile_concepts.html#resources
[snip]: {{site.docsurl}}/snippets.html?nodejs#snip_local_nodejs_server
[catalog]: {{site.blogurl}}/2022/03/03/resource-catalog.html
[disable]: {{site.docsurl}}/disable_resources.html
[repos]: {{site.docsurl}}/multiple_repos.html
[snippets]: {{site.docsurl}}/snippets.html
[extweet]: https://twitter.com/tilt_dev/status/1507399904846561284
[vscode]: https://marketplace.visualstudio.com/items?itemName=tilt-dev.Tiltfile&ssr=false
