---
title: Custom Buttons
description: "Describes how to add buttons with custom actions to your Tilt Web UI"
layout: docs
---

Many of the actions in a team's development workflow can be added to Tilt as `local_resource`s,
but for some use cases, that can feel a bit heavyweight.

For these use cases, Tilt offers the ability to add a button to the web ui and
define a command to run when that button is clicked. These buttons can even
take input from the UI!

The simplest way to do this is via the [uibutton extension][uibutton-docs].

(More complex use cases can create buttons directly via Tilt's api--one good
example is the [cancel extension](https://github.com/tilt-dev/tilt-extensions/blob/master/cancel/README.md)).

Here are some examples:

(This page focuses on conveying general functionality. For usage specifics, refer to the [uibutton docs][uibutton-docs])

1. You have a web service that uses yarn and occasionally need to re-run
`yarn install`. You can add a button to that resource to do so:
```python
load('ext://uibutton', 'cmd_button')
cmd_button('yarn install',
           argv=['sh', '-c', 'cd letters && yarn install'],
           resource='letters',
           icon_name='cloud_download',
           text='yarn install',
)
```

This will attach a button to the "letters" resource, which will appear in two
places: the table view and the resource view. When clicked, it will run
"yarn install", with the logs going into the "letters" resource's logs.

<img src="assets/img/button-in-action-bar.png">


<img src="assets/img/button-in-table-view.png">

2. Your project has a script that can be a bit risky / expensive and sometimes
you want to pass a --dry-run flag to see how it looks before actually running it.

```python
load('ext://uibutton', 'cmd_button', 'bool_input')
cmd_button('dothething',
           argv=['sh', '-c', 'echo doing the thing $DRY_RUN'],
           location=location.NAV,
           icon_name='front_hand',
           text='Hello!',
           inputs=[
             bool_input('DRY_RUN', true_string='--dry-run', false_string=''),
           ],
)
```

This creates a button that has a boolean option, which the UI renders as a checkbox:
<img src="assets/img/button-example-dry-run.png">
(this form pops up when the user clicks the arrow attached to the button)

`bool_input` says to add a checkbox, and set the command's `$DRY_RUN`
 environment variable to the value of the checkbox. `true_string` and `false_string`
 specify the value of that environment variable when the input is true or false.
 i.e., if checked, the button will echo `"doing the thing --dry-run"`, else, `"doing the thing"`

 3. Similarly, you can specify a `text_input` that adds a text field to the button,
 where the user can input arbitrary text:
 ```python
 load('ext://uibutton', 'cmd_button', 'text_input')
 cmd_button('hello',
            argv=['sh', '-c', 'echo Hello, $NAME'],
            location=location.NAV,
            icon_name='front_hand',
            text='Hello!',
            inputs=[
              text_input('NAME'),
            ],
 )
 ```

4. Add a button to quickly run a command in a pod:
```python
# note: if you're actually doing this you probably ought to put the bash script in
# a separate file
pod_exec_script = '''
set -eu
# get k8s pod name from tilt resource name
POD_NAME="$(tilt get kubernetesdiscovery "$resource" -ojsonpath='{.status.pods[0].name}')"
kubectl exec "$POD_NAME" -- $command
'''
cmd_button('podexec',
           argv=['sh', '-c', pod_exec_script],
           location=location.NAV,
           icon_name='',
           text='Exec in a pod',
           inputs=[
             text_input('resource'),
             text_input('command'),
           ]
)
```

<img src="assets/img/button-exec-in-pod.png">

Hopefully that's enough to get you interested and started!

If you have any feedback, feature requests, or inventive uses of this that you'd
like to share with us, please [reach out](/contact)!

[uibutton-docs]: https://github.com/tilt-dev/tilt-extensions/blob/master/uibutton/README.md
