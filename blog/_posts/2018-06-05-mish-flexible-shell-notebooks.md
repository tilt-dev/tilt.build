---
slug: mish-flexible-shell-notebooks
date: 2018-06-05T22:01:37.684Z
author: dan
layout: blog
title: "mish&#58; Flexible Shell Notebooks"
image_caption: "easier refining and repeating"
image: "1_w-2_vusBqdbQA_1oxcBFKw.gif"
tags:
  - terminal
keywords:
  - terminal
---

Shell makes it easy to rerun previous commands, but hard to edit them. Rerunning is `&lt;up&gt;-&lt;enter&gt;`, but editing requires `&lt;up&gt;-&lt;left&gt;-&lt;left&gt;-&lt;backspace&gt;-&lt;wait-how-many-backspaces-was-it&gt;-&lt;etc.&gt;`. If you’ve ever been irritated editing in shell, our [new tool `mish`](https://github.com/windmilleng/mish) can save you time and hassle.

`mish` is a terminal app that augments easy-rerun with a better editing experience: your existing editor. By storing data in a file (`notes.mill`)instead of as command-line arguments, `mish` lets you flex your muscle memory to tweak your workflow. Your cursor stays put; your keyboard shortcuts are familiar.

Your `notes.mill` file is your personal notebook. It’s scratch space; edit as frequently as you need to change an argument. It’s durable; you won’t lose tuned commands to the shell history limit. It’s organized; different workflows can be separated and organized.

You can get `[mish` from github](https://github.com/windmilleng/mish). In 5 minutes, you’ll have a better shell experience. Have fun! If you’re still here, I’ll give a quick tour of `mish`.

## Hello World

`mish` works best when you run two apps side-by-side: on the left, your editor with your code and a new file `notes.mill` in the root of your project. Open a terminal on the right and run `mish`.

`notes.mill` is written in Mill, a dialect of python (if you tell your editor that .mill files are python, you’ll get syntax highlighting, etc.). A good hello world is:

```
sh("ls")
sh("echo hello mish")
```


Switch into the `mish` window and hit `r` to rerun.

![selecting a workflow](/assets/images/mish-flexible-shell-notebooks/1*1iZGUcjmLf8mvYYjtU0ZLg.gif)*selecting a workflow*

## Workflows

Sometimes I want to run unittests; other times I want to start a server. Mill supports this by letting you define workflows:

```
def wf_hello():
  sh("ls")
  sh("echo hello mish")

def wf_serve():
  sh("./server/main.py") # run the server
```


Now pressing `r` will reload the Mill file, but the interesting workflows are in functions. Hit `f` to list available workflows, and pick one to focus on.

## Refine

My magic moment with `mish`, when it became an indispensable tool, is when I’m modifying command lines. I end up with a section like:

```
def wf_scratch():
  sh("go test -run TestWatchOneFile$ ./os/watch") # run one test
  sh("go test ./os/watch") # run all tests in the watch package
  sh("go test ./...") # run all tests in the project
```


Because `mish` will error after a failing command, this helps me iterate while I’m seeing red, until everything passes and I’m seeing green.

## Mish your way

What will make `mish` click for you? Maybe it’s the way it can take fewer keystrokes to restart a server. Or making sure you generate code as you’re editing your protocol buffers. But we’re pretty sure the next time you’re editing a command in shell, you’ll have a better day if you [try `mish`](https://github.com/windmilleng/mish).

Make sure to let us know by filling out our [5-minute survey](https://docs.google.com/forms/d/e/1FAIpQLSf8UXLG0FOeMswoW7LuUP02CeUwKBccJishJKDE_VyOqe7g_g/viewform?usp=sf_link).

![](/assets/images/mish-flexible-shell-notebooks/1*KbCt7S4W2Eh8EK7mqor4Pg.png)
