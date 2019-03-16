---
title: Extending Tilt
layout: docs
---

There's nothing more frustrating than using a tool that works perfectly except for _one_ small thing. Even if the tool is open source it can be a daunting task to get a change accepted to it.

We recognize that everyone's set up is different and that we cannot foresee all possible features and use cases that folks will need. Software is complicated! As a result we designed Tilt to be customizable from the beginning. If there's functionality you wish Tilt had you can often add it yourself, right in your Tiltfile, no external pull requests necessary!

Let's check out how this works with a simple feature request: I want Tilt to error if it is executed with a Kubernetes context other than the one that I have safelisted. There's a catch though: each developer's allowed context name will be entirely up to them so we'll need to allow users to specify their own context names.

## Step 1: `enforce_allowed_context`
Let's write the core functionality first before worrying about user input. `enforce_allowed_context` should be a function that takes the allowed context, checks it against the current context and fails if the current context does not much the allowed context. We'll need to make use of a couple standard bits of the Starlark language as well as some Tilt-specific facilities.

```python
def enforce_allowed_context(allowed_context):
  if allowed_context == "": # If no allowed_context is empty, assume none was set
    return

  current_context = str(local('kubectl config current-context')).rstrip('\n')
  if current_context != allowed_context:
    fail("Context %s is not allowed. Only the %s context is allowed." % (current_context, allowed_context))
```

This function uses two Tilt-specific functions: `local` and `fail`.

`local` takes a shell command, executes it and returns its output. Here we're calling out to `kubectl` to get the current context, casting it to a string and removing any trailing new lines from the output.

`fail` causes Tiltfile execution to fail with the provided message. We want to let the user know which context they are using and which one is permitted.

With those two ingredients it's a simple matter to check the current context against the allowed one and fail the Tiltfile build if they don't match.

## Step 2: user input
This works great, but we want to let the user supply their own value for `allowed_context` at runtime. To do this we will make use of one more built in Tilt function: `read_json`.

```python
settings = read_json(".tilt.json")
allowed_context = settings.get("allowed_context", "")
enforce_context(allowed_context)
```

`read_json` reads the file at the specified path and deserializes its contents in to a Starlark dictionary. Then we try to get the `"allowed_context"` key from that dictionary and either return it if it's present or return the empty string. Then we simply pass that in to `enforce_context`.

## Step 3: Profit!
That's it! We've added a feature to Tilt that does some non-trivial things, like talking to Kubernetes and reading files off of disk, all without having to open a pull request.
