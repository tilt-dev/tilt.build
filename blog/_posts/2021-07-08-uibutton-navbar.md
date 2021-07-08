---
slug: "uibutton-navbar"
date: "2021-07-08"
author: milas
layout: blog
title: "Buttons. Icons. APIs."
image: "/assets/images/uibutton-navbar/header.jpg"
description: "Extend Tilt to simplify gathering internal feedback from your team"
tags:
  - api
  - ui
  - button
---

Recently I showed you how to add [a custom button to a resource][uibutton-intro-blog] and cloyingly teased there was more to come.

Well, dear reader, more has come!
The latest version of Tilt not only comes with a shiny new resource overview layout but also adds support for navbar buttons.
Navbar buttons appear in the fixed header, so you can always access them regardless of which resource you have selected.

![navbar button demo](/assets/images/uibutton-navbar/example.gif)

Adding navbar buttons to your `Tiltfile` is very similar to adding resource-specific buttons: the [`uibutton` extension][uibutton-ext] can take care of it with a couple argument tweaks.
The hardest part of adding a navbar button is picking the icon!
Tilt includes the [Material Icons][material-icons] set or you can provide your own SVG (ideal for brand icons or [honking][goose-tweet]).

As the Tilt champion at your company, you might be used to helping debug configuration issues with your coworkers.
Let's build a button to gather some useful information about their Tilt setup and pre-compose a report to save ourselves some time!

![report issue button](/assets/images/uibutton-navbar/report-issue-btn.png)

We'll use a Python script that runs `tilt doctor ` and `tilt get session` to pre-populate an email:
<details>
<summary>tilt-feedback.py</summary>

{% highlight python %}
#!/usr/bin/env python3

import subprocess
import sys
import webbrowser

from urllib.parse import quote


if __name__ == "__main__":
    tilt_bin = sys.argv[1]
    doctor = subprocess.run(
        args=[tilt_bin, "doctor"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    ).stdout

    session = subprocess.run(
        args=[tilt_bin, "get", "session", "Tiltfile", "-o=yaml"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    ).stdout

    mailto = "mailto:help@example.com?subject={subject}&body={body}".format(
        subject=quote("Tilt Issue"),
        body=quote(
            "DESCRIBE YOUR ISSUE HERE\n\n--------------------\n{doctor}\n{session}".format(
                doctor=doctor, session=session
            ),
        ),
    )

    webbrowser.open(mailto)
{% endhighlight %}
</details><br/>

We add a new button to invoke the script by using the [`uibutton` extension][uibutton-ext] in our `Tiltfile`:
```python
load('ext://uibutton', 'cmd_button', 'location')

# create a button to run the linter for the 'frontend' resource
cmd_button(name='tilt-feedback',
           argv=['python3', 'tilt-feedback.py', sys.executable],
           location=location.NAV,
           text='Report Issue',
           icon_name='support_agent')
```
> ℹ️ `sys.executable` contains the path to the Tilt binary, which our Python script uses to invoke Tilt to gather diagnostics

This is pretty similar to creating a [resource-specific button][uibutton-intro-blog], but instead of specifying a `resource`, we passed `location=location.NAV`.
Additionally, since navbar buttons in Tilt are icons with text-on-hover, we provided an icon name from the [Material Icons][material-icons] font.

Let's `tilt up` and check it out!

![navbar button demo](/assets/images/uibutton-navbar/demo.gif)

You're now ready to go on your way to bedazzle your Tilt, but if you're curious about the APIs used by this extension under the hood, read on...

### Deep Dive
More and more parts of Tilt are being exposed as APIs to allow building upon and extending built-in Tilt functionality. You might have seen our post a while back introducing [the Tilt apiserver][apiserver-intro-blog].

One of the newer types is `UIButton` - we can view the `tilt-feedback` button we created above using the Tilt CLI:
<details>
<summary><code>tilt get -o=yaml uibuttons tilt-feedback</code></summary>

{% highlight yaml %}
apiVersion: tilt.dev/v1alpha1
kind: UIButton
metadata:
  creationTimestamp: "2021-07-07T21:17:24Z"
  name: tilt-feedback
  resourceVersion: "2"
  uid: ef00ec53-c949-4ab4-8174-b98b653072f3
spec:
  iconName: support_agent
  location:
    componentID: nav
    componentType: Global
  text: Report Issue
status:
  lastClickedAt: "2021-07-07T21:17:42.827000Z"
{% endhighlight %}
</details><br/>

If you've edited Kubernetes YAML files, this hopefully looks familiar!
The `spec` is our configuration including the icon and placement while the `status` is the current state, which in the case of a button just includes the last time that it was clicked.

What is _not_ part of the `UIButton` resource is anything related to the Python command, but we know a command runs when we click the button because I included a GIF above and everything on the internet is true, right?

For the skeptics, one of the core Tilt types in the apiserver is `Cmd`, which handles execution commands on the local machine running Tilt.
The extension created a `Cmd` resource along with the `UIButton` resource, so let's take a look at it:
<details>
<summary><code>tilt get -o=yaml cmd btn-tilt-feedback</code></summary>

{% highlight yaml %}
apiVersion: tilt.dev/v1alpha1
kind: Cmd
metadata:
  annotations:
    tilt.dev/log-span-id: cmd:tilt-feedback
  creationTimestamp: "2021-07-07T21:17:24Z"
  name: btn-tilt-feedback
  resourceVersion: "11"
  uid: f84a9e14-f42d-453b-b0db-1e8a115d904e
spec:
  args:
  - python3
  - tilt-feedback.py
  - /usr/local/bin/tilt
  dir: /Users/milas/demo/navbar-btn
  startOn:
    startAfter: "2021-07-07T21:17:28Z"
    uiButtons:
    - tilt-feedback
status:
  ready: true
  terminated:
    exitCode: 0
    finishedAt: "2021-07-07T21:17:43.621569Z"
    pid: 29295
    startedAt: "2021-07-07T21:17:42.834889Z"
{% endhighlight %}
</details><br/>

Here, the extension populated `spec` with the `argv` we specified as well as `startOn`.
Tilt uses the `startOn` field to watch other resources and invoke the command when any of those resources change appropriately. In this case, whenever the `UIButton` named `tilt-feedback` has its `lastClickedAt` field in the status updated, the command will execute.

There's a lot of power here: Tilt's `local_resource` uses a similar pattern with the `restartOn` field and `FileWatch` objects, for example.

As Tilt's API grows, there will be more and more possibilities to connect these foundational types in new and inventive ways!

If you're using the Tilt API, be sure to [let us know][community]!


[uibutton-intro-blog]: /2021/06/21/uibutton.html
[uibutton-ext]: https://github.com/tilt-dev/tilt-extensions/tree/master/uibutton
[material-icons]: https://fonts.google.com/icons
[goose-tweet]: https://twitter.com/tilt_dev/status/1411034612822851593
[apiserver-intro-blog]: /2021/04/30/how-many-servers.html
[community]: https://docs.tilt.dev/#community
