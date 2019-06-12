---
title: Play and Pause Resources with Manual Update Control
layout: docs
---

By default, Tilt watches your filesystem for edits and, whenever it detects a change affecting Resource X, triggers an update of that resource. All your local code, synced to your cluster as you edit it! What could be better?

Well, sometimes that's _not_ what you want. Maybe updating Resource X takes a long time and so you only want to run updates when you're actually ready. Maybe you're about to check out a branch and don't want all the spurious file changes to launch a lot of updates. Whatever your reason, Manual Update Control is here to help.

The behavior described above is `TriggerMode: Auto` (Tilt's default); that is, updates are _automatically_ triggered whenever Tilt detects a change to a relevant file.

Now there's another way of doing things: `TriggerMode: Manual`. The UI will show you when Tilt has detected changes relevant to your resource, but it's up to you to _manually_ trigger the update, by means of a button in the UI.

###### SCREENSHOT GOES HERE!

## How to Set TriggerMode
You can change the trigger mode(s) of your resources in your Tiltfile in two different ways:

1. [`k8s_resource()`](/api.html#api.k8s_resource) has an optional arg, `trigger_mode`; for that specific resource, you can pass either `TRIGGER_MODE_AUTO` or `TRIGGER_MODE_MANUAL`.
2. if you want to adjust all of your resource at once, call the top-level function [`trigger_mode()`](/api.html#api.trigger_mode) with one of those two constants. This sets the _default trigger mode for all manifests_. (You can still use `k8s_resource()` to set the trigger mode for individual manifests.)

Here are some examples:
```python
...
k8s_resource('foo')  # TriggerMode = Auto by default
```

```python
...
# TriggerMode = Manual
k8s_resource('foo', trigger_mode=TRIGGER_MODE_MANUAL)
```

```python
trigger_mode(TRIGGER_MODE_MANUAL)
...
# TriggerMode = Manual (default set above)
k8s_resource('foo')

# TriggerMode = Auto (can override the above default
# for specific resources)
k8s_resource('bar', trigger_mode=TRIGGER_MODE_AUTO)
```
